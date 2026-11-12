"""Optional launch path with actual installed helper and fake providers only."""
import asyncio
from dataclasses import replace
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
from types import SimpleNamespace

import pytest
import launch
import code_context_launch as context
from provider_accounts import Binding
from sessions import VerbError
from spawnctl import SpawnCtl


READY = json.dumps({'schema':'pentacle.code-context.v1','status':'ready','read_only':True})


@pytest.mark.parametrize('message', [
    {'provider':'codex','code_context':'true'}, {'provider':'codex','code_context':1},
    {'provider':'gemini','code_context':True}, {'provider':'cursor','code_context':True},
    {'provider':'codex','code_context':True,'command':'custom'},
    {'provider':'claude','code_context':True,'resume_session_id':'old'},
    {'provider':'codex','code_context':True,'handoff':True},
])
def test_unsupported_opt_in_is_rejected_before_launch(message):
    ctl = object.__new__(SpawnCtl)
    with pytest.raises(VerbError, match='code_context'):
        asyncio.run(ctl._resolve_launch(message, 'host-a', 'new'))


def test_off_default_does_not_change_launch_bytes_or_permissions(tmp_path, monkeypatch):
    monkeypatch.setattr(launch,'mint_stream_token',lambda:'fixture-token')
    monkeypatch.setattr(launch.uuid,'uuid4',lambda:'fixture-id')
    machine=launch.local_machine('host-a',cwd=str(tmp_path),codex_bin='/bin/echo',claude_bin='/bin/echo')
    for provider in ['claude','codex']:
        args=dict(provider=provider,tmux_session='new',launch_model=None,launch_effort=None)
        assert launch.build_launch(machine,**args).command == launch.build_launch(machine,**args,code_context_instruction='').command


@pytest.mark.parametrize('output', ['', '[]', '{}', READY.replace('v1','v0'), READY.replace('true','false'), 'x'*4097])
def test_bad_target_probe_falls_back_without_guidance(tmp_path, output):
    class Hosts:
        async def run_command_bounded(self, host, *args, timeout):
            assert host=='peer' and args[0]==str(tmp_path/'pentacle-code-context')
            return 0, output
    machine=replace(launch.local_machine('peer'),agent_orch_bin_dir=str(tmp_path),resolve_cwd_locally=False)
    instruction, disposition=asyncio.run(context.prepare(Hosts(),'peer',machine,'codex'))
    assert instruction=='' and disposition=={'requested':True,'active':False,'reason':'helper_unavailable'}


def test_remote_does_not_resolve_daemon_local_ambient_binary():
    machine=replace(launch.local_machine('peer',codex_bin='codex'),resolve_cwd_locally=False)
    assert context.helper_path(machine,'codex') is None


def test_bounded_helper_output_and_timeout(tmp_path):
    noisy=tmp_path/'noisy'
    noisy.write_text('#!'+sys.executable+'\nimport sys,time\nsys.stdout.write("x"*10000);sys.stdout.flush();time.sleep(20)\n');noisy.chmod(0o700)
    code, output=asyncio.run(context.limited_exec(str(noisy),timeout=.2))
    assert code != 0 and not output


@pytest.mark.parametrize('provider',['claude','codex'])
@pytest.mark.parametrize('named',[False,True])
def test_actual_argv_preserves_instructions_and_installed_helper_runs(tmp_path, provider, named):
    bin_dir=tmp_path/"tool's bin";bin_dir.mkdir()
    installed=Path(sys.executable).parent/'pentacle-code-context'
    assert installed.is_file(), 'Install this checkout with the code-context extra before this integration test'
    helper=bin_dir/'pentacle-code-context';helper.write_text('#!/bin/sh\nexec '+shlex.quote(str(installed))+' "$@"\n');helper.chmod(0o700)
    fake=bin_dir/'fake provider';fake.write_text('#!'+sys.executable+'\nimport json,sys,os\nprint(json.dumps({"argv":sys.argv[1:],"env":dict(os.environ)}))\n');fake.chmod(0o700)
    repo=tmp_path/'project';repo.mkdir();subprocess.run(['git','init','-q',str(repo)],check=True)
    (repo/'rule.py').write_text('def enforce_limit(x):\n    if x > 4:\n        raise ValueError("over_limit")\n    return x\n')
    machine=launch.local_machine('host-a',cwd=str(repo),claude_bin=str(fake),codex_bin=str(fake),agent_orch_bin_dir=str(bin_dir))
    binding=Binding(provider,'primary','host-a',str(tmp_path/'named'),'login','browser',str(fake),'fixture','macos') if named else None
    instruction, disposition=asyncio.run(context.prepare(None,'host-a',machine,provider,binding))
    assert disposition['active'] and shlex.quote(str(helper)) in instruction
    plan=launch.build_launch(machine,provider=provider,tmux_session='fixture',launch_model='fixture-model',launch_effort='high',
        code_context_instruction=instruction,operator_facing=True,account_binding=binding)
    done=subprocess.run(['/bin/sh','-c',plan.command],env={**os.environ,'HOME':str(tmp_path)},capture_output=True,text=True,timeout=5)
    assert done.returncode==0,done.stderr
    observed=json.loads(done.stdout);argv=observed['argv']
    if provider=='claude':
        assert argv.count('--append-system-prompt')==1
        text=argv[argv.index('--append-system-prompt')+1]
        assert '--dangerously-skip-permissions' in argv
    else:
        values=[argv[i+1] for i,a in enumerate(argv[:-1]) if a=='-c' and argv[i+1].startswith('developer_instructions=')]
        assert len(values)==1;text=values[0]
        assert launch.CODEX_OPERATOR_QUESTION_INSTRUCTION in text and '--approve-for-me' in argv
    assert instruction in text and launch.VISIBLE_SESSION_METADATA_INSTRUCTION in text
    answer=subprocess.run([str(helper),'query','--root',str(repo),'--query','enforce_limit'],capture_output=True,text=True,timeout=12)
    evidence=json.loads(answer.stdout)['evidence']
    assert answer.returncode==0 and evidence[0]['unit_complete'] and 'over_limit' in evidence[0]['excerpt']


def test_requested_choice_changes_idempotent_payload_identity():
    base={'provider':'codex','host':'host-a','model':'gpt-6.1-sol','effort':'high'}
    assert SpawnCtl._spawn_payload_hash(base) != SpawnCtl._spawn_payload_hash({**base,'code_context':True})


@pytest.mark.parametrize('ready', [True, False])
def test_real_resolver_probes_only_opt_in_and_keeps_fallback_spawn(tmp_path, ready):
    from sessions import Sessions
    from store import Store
    class Hosts:
        peers = {}
        def __init__(self): self.calls = []
        async def run_command_bounded(self, host, *argv, timeout):
            self.calls.append((host, argv))
            return (0, READY) if ready else (127, '')
    async def scenario():
        store = Store(':memory:'); store.start()
        try:
            hosts = Hosts()
            ctl = SpawnCtl(store, Sessions(store, local_host='host-a'), hosts=hosts,
                machine=launch.local_machine('host-a', cwd=str(tmp_path), codex_bin='/bin/echo', agent_orch_bin_dir=str(tmp_path)))
            message = {'provider':'codex', '_defer_launch_token_stage':True}
            ordinary, off, _ = await ctl._resolve_launch(message, 'host-a', 'ordinary')
            assert hosts.calls == [] and 'code_context' not in off
            command, resolution, _ = await ctl._resolve_launch({**message, 'code_context':True}, 'host-a', 'enabled')
            assert len(hosts.calls) == 1
            assert resolution['code_context']['active'] is ready
            assert ('Optional Pentacle local code context' in command) is ready
            assert '--approve-for-me' in ordinary and '--approve-for-me' in command
            # Stored retry receipts retain the disposition without a second probe.
            receipt = {'state':'delivered', 'code_context':resolution['code_context']}
            ctl._admitted_for_key = lambda *_: asyncio.sleep(0, result={})
            await store.open_session('host-a', 'enabled', objective='Test retry disposition')
            await ctl.sessions.refresh()
            await store.set_spawn_outcome('host-a', 'enabled', 'delivered', request_id='r', delivery_receipt=receipt)
            recorded = await store.get_spawn_outcome('host-a', 'enabled')
            replay = await ctl._reply_from_replay('host-a', 'r', 'terminal',
                recorded, 'key', dead_is_error=False)
            assert replay['session']['code_context'] == resolution['code_context']
            assert len(hosts.calls) == 1
        finally:
            store.stop()
    asyncio.run(scenario())
