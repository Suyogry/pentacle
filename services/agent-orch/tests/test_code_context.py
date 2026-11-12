"""Real temporary Git source, syntax parsers and standalone worker contracts."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import pytest

from agent_orch.code_context import MAX_OUTPUT, capabilities
from agent_orch.code_context.engine import run
from agent_orch.code_context.source import Tree, Unavailable
from agent_orch.code_context.units import extract


@pytest.fixture
def repo(tmp_path):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "logic.py").write_text('LIMIT = 4\n\ndef allow_task(value):\n    if value > LIMIT:\n        raise ValueError("over_limit")\n    return value\n')
    return tmp_path


def query(repo, query="allow_task", **kwargs):
    return run({"root": str(repo), "mode": "query", "query": query, **kwargs})


def test_complete_function_constants_hash_and_lines(repo):
    result = query(repo)
    unit, = result["evidence"]
    raw = (repo / "logic.py").read_bytes()
    assert unit["unit_complete"] is True
    assert unit["sha256"] == hashlib.sha256(raw).hexdigest()
    assert unit["excerpt"] == "".join(raw.decode().splitlines(keepends=True)[unit["start"]-1:unit["end"]])
    assert 'raise ValueError("over_limit")' in unit["excerpt"]
    assert unit["supporting_constants"][0]["excerpt"] == 'LIMIT = 4\n'
    assert "closures" in unit["dependency_boundary"]


def test_decorators_async_nested_class_and_unicode(repo):
    (repo / "logic.py").write_text('@decorator\nasync def fetch_thing():\n    return "café"\n\nclass Client:\n    def fetch_thing(self):\n        return False\n')
    result = query(repo, "fetch_thing")
    assert len(result["evidence"]) == 2
    assert any('@decorator' in e['excerpt'] for e in result['evidence'])
    assert any(e['enclosing'] == ['Client'] for e in result['evidence'])
    assert query(repo, 'café')['evidence']


@pytest.mark.parametrize("suffix,text,name", [
    ('.js', 'export function checkThing(x) { if (!x) throw Error("required"); return x; }\n', 'checkThing'),
    ('.jsx', 'export const DrawThing = () => <div>hello</div>;\n', 'DrawThing'),
    ('.ts', 'export const checkThing = (x: number): number => { if (x < 0) throw Error("negative"); return x; };\n', 'checkThing'),
    ('.tsx', 'export const DrawThing = (p: {x:string}) => <div>{p.x}</div>;\n', 'DrawThing'),
    ('.js', 'class Thing { checkThing(x) { return x; } }\n', 'checkThing'),
])
def test_actual_optional_parsers(repo, suffix, text, name):
    pytest.importorskip('tree_sitter')
    pytest.importorskip('tree_sitter_typescript' if suffix in {'.ts', '.tsx'} else 'tree_sitter_javascript')
    (repo / ('sample' + suffix)).write_text(text)
    units = query(repo, name)['evidence']
    assert units and units[0]['unit_complete'] is True
    assert units[0]['excerpt'].strip() in text
    assert name in units[0]['excerpt']
    if text.startswith('export'):
        assert units[0]['excerpt'].lstrip().startswith('export')


def test_missing_parser_is_explicit_lexical_evidence(repo, monkeypatch):
    monkeypatch.setitem(sys.modules, 'tree_sitter', None)
    (repo / 'task.js').write_text('function allowTask() { return false; }\n')
    result = query(repo, 'allowTask')
    assert result['status'] == 'partial'
    assert 'parser_missing' in result['limitations']
    assert result['evidence'] and all(not e['unit_complete'] for e in result['evidence'])


def test_current_bytes_even_when_mtime_and_size_preserved(repo):
    path = repo / 'logic.py'; old = path.stat()
    first = query(repo)['evidence'][0]['sha256']
    path.write_bytes(path.read_bytes().replace(b'over_limit', b'over_quota'))
    os.utime(path, ns=(old.st_atime_ns, old.st_mtime_ns))
    unit = query(repo)['evidence'][0]
    assert unit['sha256'] != first and 'over_quota' in unit['excerpt']


def test_add_rename_delete_and_negative_identifier(repo):
    assert not query(repo, 'nonexistent_symbol_991')['evidence']
    path = repo/'new.py';path.write_text('def new_feature():\n    return 7\n')
    assert query(repo, 'new_feature')['evidence'][0]['path'] == 'new.py'
    path.rename(repo/'renamed.py')
    assert query(repo, 'new_feature')['evidence'][0]['path'] == 'renamed.py'
    (repo/'renamed.py').unlink()
    assert not query(repo, 'new_feature')['evidence']


@pytest.mark.parametrize('path', ['.env', '.env.example', 'credentials.json', 'private.key', '.aws/config', '.codex/state.py', 'node_modules/thing.py'])
def test_tracked_secrets_and_dependency_paths_never_return(repo, path):
    target = repo/path;target.parent.mkdir(parents=True, exist_ok=True);target.write_text('def excluded_sentinel():\n    return "EXCLUDED-SENTINEL"\n')
    subprocess.run(['git','-C',str(repo),'add','-f','--',path], check=True)
    result = query(repo, 'excluded_sentinel')
    assert 'EXCLUDED-SENTINEL' not in json.dumps(result)
    read = run({'root':str(repo),'mode':'read','path':path,'symbol':'excluded_sentinel'})
    assert read['status'] == 'unavailable' and not read['evidence']


def test_tracked_gitignored_source_and_custom_exclusions(repo):
    (repo/'logic.py').write_text('def ignored_symbol():\n    return "HIDDEN"\n')
    subprocess.run(['git','-C',str(repo),'add','logic.py'],check=True)
    (repo/'.gitignore').write_text('logic.py\n')
    assert not query(repo,'ignored_symbol')['evidence']
    (repo/'.gitignore').unlink();(repo/'.pentacle-context-ignore').write_text('logic.py\n')
    assert not query(repo,'ignored_symbol')['evidence']


@pytest.mark.parametrize('path', ['../logic.py','/etc/passwd','a/../../logic.py','a\\logic.py'])
def test_read_scope_rejects_traversal(repo, path):
    result=run({'root':str(repo),'mode':'read','path':path,'start':1,'end':10})
    assert result['status']=='unavailable' and not result['evidence']


def test_symlinks_fifo_and_nested_repository_are_not_evidence(repo, tmp_path_factory):
    outside=tmp_path_factory.mktemp('outside');(outside/'leak.py').write_text('def escape_sentinel():\n    return "OUTSIDE"\n')
    (repo/'escape.py').symlink_to(outside/'leak.py');(repo/'dir').symlink_to(outside, target_is_directory=True)
    os.mkfifo(repo/'pipe.py')
    nested=repo/'nested';nested.mkdir();subprocess.run(['git','init','-q',str(nested)],check=True)
    (nested/'leak.py').write_text((outside/'leak.py').read_text())
    subprocess.run(['git','-C',str(repo),'add','-N','logic.py'],check=True)
    result=query(repo,'escape_sentinel')
    assert 'OUTSIDE' not in json.dumps(result)
    tree = Tree(str(repo),time.monotonic()+3)
    try:
        with pytest.raises(OSError):
            tree.read('dir/leak.py')
        with pytest.raises(Unavailable):
            tree.read('nested/leak.py')
        with pytest.raises(Unavailable):
            tree.read('pipe.py')
    finally:
        tree.close()


def test_final_source_change_and_ignore_change_suppress_indexed_bytes(repo, monkeypatch):
    import agent_orch.code_context.engine as engine
    original=engine.rank
    def mutate(*args):
        ranked=original(*args);(repo/'logic.py').write_text('def changed():\n    return 1\n');return ranked
    monkeypatch.setattr(engine,'rank',mutate)
    result=query(repo,'allow task value limit')
    assert not result['evidence'] and 'source_changed' in result['limitations']


def test_parent_symlink_swap_is_rejected_on_final_read(repo, tmp_path_factory, monkeypatch):
    import agent_orch.code_context.engine as engine
    inner=repo/'src';inner.mkdir();(inner/'logic.py').write_text((repo/'logic.py').read_text());(repo/'logic.py').unlink()
    outside=tmp_path_factory.mktemp('outside');(outside/'logic.py').write_text('def allow_task():\n    return "OUTSIDE"\n')
    original=engine.rank
    def swap(*args):
        ranked=original(*args);inner.rename(repo/'old');inner.symlink_to(outside,target_is_directory=True);return ranked
    monkeypatch.setattr(engine,'rank',swap)
    result=query(repo,'allow task limit value')
    assert not result['evidence'] and 'OUTSIDE' not in json.dumps(result)


def test_large_unit_returns_locator_and_expansion_not_truncated_body(repo):
    (repo/'logic.py').write_text('def enormous_unit():\n    value = '+repr('x'*60000)+'\n    return value\n')
    unit,=query(repo,'enormous_unit')['evidence']
    assert not unit['unit_complete'] and 'excerpt' not in unit and unit['expansion']['command']=='read'


def test_literal_search_punctuation_and_line_expansion(repo):
    result=run({'root':str(repo),'mode':'search','query':'raise ValueError("over_limit")'})
    assert result['evidence'] and not result['evidence'][0]['unit_complete']
    result=run({'root':str(repo),'mode':'read','path':'logic.py','start':3,'end':6})
    assert result['evidence'][0]['excerpt'].startswith('def allow_task')
    assert not result['evidence'][0]['unit_complete']
    assert query(repo,'" OR * : (foo)')['status'] in {'no_match','partial','candidates'}


def test_cli_real_worker_and_project_import_shadow(repo):
    marker=repo/'EXECUTED';(repo/'tree_sitter.py').write_text('from pathlib import Path\nPath('+repr(str(marker))+').touch()\n')
    (repo/'agent_orch').mkdir();(repo/'agent_orch/__init__.py').write_text('raise RuntimeError("project import")')
    cmd=[str(Path(sys.executable).parent/'pentacle-code-context'),'query','--root',str(repo),'--query','allow_task']
    result=subprocess.run(cmd,cwd=repo,env={**os.environ,'PYTHONPATH':''},capture_output=True,text=True,timeout=12)
    assert result.returncode==0,result.stdout+result.stderr
    assert json.loads(result.stdout)['evidence'] and not marker.exists()
    assert len(result.stdout.encode())<=MAX_OUTPUT


def test_shadowed_constant_is_not_attached_as_global_evidence(repo):
    (repo/'logic.py').write_text('LIMIT = 9\n\ndef check_limit(LIMIT):\n    return LIMIT\n')
    assert not query(repo,'check_limit')['evidence'][0]['supporting_constants']
    (repo/'logic.js').write_text('const LIMIT = 9;\nfunction checkLimit(LIMIT) { return LIMIT; }\n')
    result=query(repo,'checkLimit')
    assert result['evidence'] and not result['evidence'][0].get('supporting_constants')


def test_ignore_rule_change_during_query_suppresses_evidence(repo, monkeypatch):
    import agent_orch.code_context.engine as engine
    original=engine.rank
    def mutate(*args):
        ranked=original(*args);(repo/'.pentacle-context-ignore').write_text('logic.py\n');return ranked
    monkeypatch.setattr(engine,'rank',mutate)
    result=query(repo,'allow task limit')
    assert not result['evidence'] and 'source_changed' in result['limitations']


def test_fts5_unavailable_is_a_real_degraded_search(repo, monkeypatch):
    import agent_orch.code_context.engine as engine
    class NoFTS:
        def execute(self,*args): raise engine.sqlite3.OperationalError('no such module: fts5')
        def close(self): pass
    monkeypatch.setattr(engine.sqlite3,'connect',lambda *args,**kwargs: NoFTS())
    result=query(repo,'allow task limit')
    assert result['evidence'] and result['lexical']=='literal_degraded'


def test_git_fsmonitor_configuration_cannot_execute(repo):
    marker=repo/'HOOK-EXECUTED';script=repo/'monitor.sh'
    script.write_text('#!/bin/sh\ntouch '+str(marker)+'\nprintf "\\0"\n');script.chmod(0o700)
    subprocess.run(['git','-C',str(repo),'add','logic.py'],check=True)
    subprocess.run(['git','-C',str(repo),'config','core.fsmonitor',str(script)],check=True)
    assert query(repo)['evidence'] and not marker.exists()


def test_encoded_control_characters_and_odd_filename_remain_bounded(repo):
    path=repo/'odd café "file".txt';path.write_text('escape_marker '+('\x01'*40000))
    result=query(repo,'escape_marker')
    encoded=json.dumps(result,ensure_ascii=False).encode()
    assert result['evidence'] and not result['evidence'][0]['unit_complete']
    assert len(encoded)<MAX_OUTPUT


def test_weak_natural_match_returns_locators_not_unrelated_bodies(repo):
    result=query(repo,'allow task frobnication unrelated special magical')
    assert not result['evidence'] and 'weak_match' in result['limitations'] and result['locators']


def test_plain_identifier_prefers_exact_definition(repo):
    (repo/'logic.py').write_text('def eligibility():\n    return True\n\ndef check_eligibility_tests():\n    return eligibility()\n')
    result=query(repo,'eligibility')
    assert result['evidence'] and all(e['symbol']=='eligibility' for e in result['evidence'])
