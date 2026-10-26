#!/usr/bin/env python3
"""Exercise the shipped Electron UI against an isolated daemon and native provider fixture."""
from __future__ import annotations
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import sys
import tempfile
import time

REPO = Path(__file__).resolve().parents[1]


def main() -> int:
    tmux = shutil.which('tmux')
    if not tmux or not shutil.which('lsof'):
        raise SystemExit('Install tmux and lsof before running the desktop smoke.')
    root = Path(tempfile.mkdtemp(prefix='pentacle-public-smoke-')).resolve()
    root.chmod(0o700)
    daemon = None
    electron = None
    terminal = root / 'tmux-fixture'
    credential = root / 'desktop.token'
    try:
        projects = root / '.claude' / 'projects'
        projects.mkdir(parents=True)
        provider = REPO / 'services/chat-stream-v2/tests/smoke/ingest_provider_stub.py'
        launcher = root / 'claude-fixture'
        launcher.write_text(f'#!{sys.executable}\nimport os,runpy\nos.environ["CHAT_STREAM_STUB_ROOT"]={str(projects)!r}\nrunpy.run_path({str(provider)!r},run_name="__main__")\n')
        launcher.chmod(0o755)
        terminal = root / 'tmux-fixture'
        terminal.write_text(f'#!/bin/sh\nexec {shlex.quote(tmux)} -L {shlex.quote(root.name)} "$@"\n')
        terminal.chmod(0o755)
        sys.path.insert(0, str(REPO / 'services'))
        from _shared.operator_auth import OperatorCredentialRegistry
        registry = OperatorCredentialRegistry(root / '.config/pentacle-stream/operator-credentials.json')
        registry.initialize()
        credential = root / 'desktop.token'
        credential.write_text(registry.issue('pentacle', label='public-smoke')[1])
        credential.chmod(0o600)
        env = {**os.environ, 'PENTACLE_MACHINES_JSON': json.dumps({'machines': [{
            'name': 'local', 'ssh_target': None, 'claude_bin': str(launcher),
            'tmux_bin': str(terminal), 'projects_root': str(projects), 'cwd': str(root),
        }]}), 'PENTACLE_INGEST_INTERVAL_S': '0.1'}
        daemon_launcher = root / 'daemon-fixture.py'
        daemon_launcher.write_text(
            'import os,sys,runpy\nfrom pathlib import Path\n'
            f'_root={str(root)!r}\n'
            'Path.home=classmethod(lambda cls: Path(_root))\n'
            '_expanduser=os.path.expanduser\n'
            'os.path.expanduser=lambda value: _root+value[1:] if value == "~" or value.startswith("~/") else _expanduser(value)\n'
            f'sys.path.insert(0,{str(REPO / "services/chat-stream-v2")!r})\n'
            f'runpy.run_path({str(REPO / "services/chat-stream-v2/main.py")!r},run_name="__main__")\n')
        args = [sys.executable, str(daemon_launcher), '--port', '0', '--local-host', 'local',
            '--db', str(root / 'sessions.db'), '--notifications-db', str(root / 'notifications.db'),
            '--assets-db', str(root / 'assets.db'), '--blob-root', str(root / 'blobs'),
            '--claude-bin', str(launcher), '--spawn-cwd', str(root), '--projects-root', str(projects), '--tmux-bin', str(terminal)]
        with (root / 'daemon.log').open('w') as output:
            daemon = subprocess.Popen(args, cwd=REPO, env=env, stdout=output, stderr=output, start_new_session=True)
        deadline = time.monotonic() + 20
        port = None
        while time.monotonic() < deadline:
            match = re.search(r'chat_streamd_v2 listening on 127\.0\.0\.1:(\d+)', (root / 'daemon.log').read_text())
            if match:
                port = int(match[1]); break
            if daemon.poll() is not None:
                raise RuntimeError('Daemon exited during startup; see daemon.log')
            time.sleep(0.05)
        if port is None:
            raise RuntimeError('Daemon did not bind before the startup deadline')
        config = {'appName': 'Pentacle public smoke', 'dashboardHub': {'url': 'https://example.invalid', 'token': 'fixture-adapter-secret'}, 'agents': {'claude': {}, 'codex': {}},
            'features': {'chatUi': True, 'chatHarnessTelemetry': True, 'mic': False}, 'tmux': str(terminal), 'chatStream': {
                'url': f'ws://127.0.0.1:{port}', 'hosts': ['local'], 'localHost': 'local', 'tokenPath': str(credential)}}
        (root / 'pentacle.config.js').write_text('module.exports = ' + json.dumps(config) + ';\n')
        electron_env = {**os.environ, 'PENTACLE_SMOKE_ROOT': str(root), 'PENTACLE_SMOKE_PID': str(daemon.pid)}
        electron_env.pop('ELECTRON_RUN_AS_NODE', None)
        with (root / 'electron.log').open('w') as output:
            electron = subprocess.Popen([str(REPO / 'node_modules/.bin/electron'), str(REPO / 'tools/public_desktop_smoke.cjs')],
                cwd=REPO, env=electron_env, stdout=output, stderr=output, start_new_session=True)
            electron.wait(timeout=100)
        if electron.returncode:
            raise RuntimeError('Desktop smoke failed; see electron.log')
        proof = json.loads((root / 'proof.json').read_text())
        assert proof['assistantRendered'] and proof['disconnectedRejected']
    finally:
        cleanup_errors = []
        for child in [electron, daemon]:
            if child is None or child.poll() is not None:
                continue
            try:
                os.killpg(child.pid, signal.SIGTERM)
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(child.pid, signal.SIGKILL)
                    child.wait()
            except ProcessLookupError:
                child.wait(timeout=5)
            except Exception as error:
                cleanup_errors.append(str(error))
        tmux_absent = True
        if terminal.exists():
            subprocess.run([str(terminal), 'kill-server'], capture_output=True)
            check = subprocess.run([str(terminal), 'list-sessions'], capture_output=True, text=True)
            tmux_absent = check.returncode != 0 and any(message in check.stderr.lower()
                for message in ['no server running', 'no such file or directory'])
            if not tmux_absent:
                cleanup_errors.append('owned tmux server absence not established')
        credential.unlink(missing_ok=True)
        shutil.rmtree(root / '.config', ignore_errors=True)
        shutil.rmtree(root / '.pentacle-stream-tokens', ignore_errors=True)
        cleanup = {'electronExited': electron is None or electron.poll() is not None,
            'daemonExited': daemon is None or daemon.poll() is not None, 'tmuxAbsent': tmux_absent,
            'credentialsAbsent': not credential.exists() and not (root / '.config').exists()
                and not (root / '.pentacle-stream-tokens').exists(), 'errors': cleanup_errors}
        (root / 'cleanup.json').write_text(json.dumps(cleanup, indent=2))
        print(f'Smoke artifacts: {root}')
        if cleanup_errors or not all(cleanup[key] for key in ['electronExited', 'daemonExited', 'tmuxAbsent', 'credentialsAbsent']):
            raise RuntimeError('Desktop smoke cleanup incomplete; see cleanup.json')
    print(f'PASS: desktop isolation, authenticated workflows and owned-resource cleanup. Evidence: {root}')
    return 0



if __name__ == '__main__':
    raise SystemExit(main())
