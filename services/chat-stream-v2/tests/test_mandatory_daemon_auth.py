"""Real loopback journeys: operator clients, revocation and raw worker identity."""
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess

import pytest
import websockets

from _shared import operator_auth
from _shared.operator_client import operator_hello
from _shared.private_credentials import read_private_token
from agent_orch.config import Config
from agent_orch import wsclient
from server import Server
from sessions import Sessions
from spawnctl import SpawnCtl
from store import Store, STREAM_TOKEN_HASH_VERSION
import launch


def credentials(tmp_path):
    directory = tmp_path / "auth"
    directory.mkdir(mode=0o700)
    registry = operator_auth.OperatorCredentialRegistry(directory / "registry.json")
    credential_id, envelope = registry.issue("pentacle", label="synthetic test")
    path = directory / "operator.token"
    path.write_text(envelope)
    path.chmod(0o600)
    return registry, credential_id, envelope, path


@pytest.mark.parametrize("journey", ["snapshot", "normal", "rpc", "persistent", "reconnect", "parent", "handoff"])
def test_real_cli_operator_journeys(tmp_path, monkeypatch, journey):
    for name in ("AGENT_ORCH_STREAM_ID", "PENTACLE_STREAM_ID", "AGENT_ORCH_INTERNAL_LEADER_STREAM_ID"):
        monkeypatch.delenv(name, raising=False)
    async def run():
        registry, _, envelope, _ = credentials(tmp_path)
        daemon = Server(host="127.0.0.1", port=0, local_host="fixture")
        daemon.operator_credential_registry = registry
        calls = []
        async def privileged(msg):
            assert msg["_auth_context"]["operator_authenticated"] is True
            calls.append(msg)
            return {"type": "spawn.ok"}
        daemon.handlers["spawn"] = privileged
        try:
            port = await daemon.bind()
            config = Config(f"ws://127.0.0.1:{port}", envelope, "fixture", tmp_path)
            if journey == "snapshot":
                assert (await wsclient._fetch_snapshot_async(config, 2))["type"] == "snapshot"
            elif journey == "normal":
                socket, snapshot = await wsclient._connect_ready(config, 2)
                assert snapshot["type"] == "snapshot"
                await socket.close()
            elif journey in {"persistent", "reconnect"}:
                client = wsclient.WebsocketClient(config)
                original = client._handle_message
                async def handle(message):
                    await original(message)
                    if message.get("type") == "snapshot":
                        client._stop.set()
                client._handle_message = handle
                await client._connect_and_read()
                if journey == "reconnect":
                    client._stop.clear()
                    await client._connect_and_read()  # fresh nonce on a fresh socket
                assert client._snapshot_ready.is_set()
            elif journey in {"parent", "handoff"}:
                fields = ({"parent_stream_id": "fixture:parent"} if journey == "parent" else
                          {"handoff": True, "handoff_from_stream_id": "fixture:previous"})
                result = await wsclient.spawn_once(config,
                    {"request_id": "operator-lineage", "command": "synthetic", **fields}, timeout=2)
                assert result["type"] == "spawn.ok" and len(calls) == 1
                assert not calls[0]["_auth_context"]["token_verified"]
            else:
                result = await wsclient._one_shot_rpc(config,
                    {"type": "spawn", "request_id": "full-authority", "command": "synthetic"},
                    prefix="spawn", timeout=2)
                assert result["type"] == "spawn.ok" and len(calls) == 1
        finally:
            await daemon.close()
    asyncio.run(run())


@pytest.mark.parametrize("operation", ["grant", "dashboard"])
def test_worker_maintenance_never_falls_back_to_ambient_operator(tmp_path, monkeypatch, operation):
    monkeypatch.setenv("AGENT_ORCH_STREAM_ID", "fixture:missing-worker")
    monkeypatch.delenv("AGENT_ORCH_INTERNAL_LEADER_STREAM_ID", raising=False)
    monkeypatch.delenv("AGENT_ORCH_STREAM_TOKEN", raising=False)
    monkeypatch.delenv("AGENT_ORCH_STREAM_TOKEN_FILE", raising=False)
    async def run():
        registry, _, envelope, _ = credentials(tmp_path)
        daemon = Server(host="127.0.0.1", port=0, local_host="fixture")
        daemon.operator_credential_registry = registry
        calls = []
        async def must_not_dispatch(msg):
            calls.append(msg)
            return {"type": f'{msg["type"]}.ok'}
        daemon.handlers["grant_token"] = must_not_dispatch
        daemon.handlers["dashboard.owner.transfer"] = must_not_dispatch
        try:
            port = await daemon.bind()
            config = Config(f"ws://127.0.0.1:{port}", envelope, "fixture", tmp_path)
            with pytest.raises(wsclient.SeatCredentialUnavailable):
                if operation == "grant":
                    await wsclient.grant_token_once(config, "fixture:legacy", timeout=2)
                else:
                    await wsclient.dashboard_once(config, {"type": "dashboard.owner.transfer"}, timeout=2)
            assert calls == []
        finally:
            await daemon.close()
    asyncio.run(run())


def test_operator_revocation_blocks_rpc_and_private_fanout_on_open_socket(tmp_path):
    async def run():
        registry, cid, _, path = credentials(tmp_path)
        daemon = Server(host="127.0.0.1", port=0, local_host="fixture")
        daemon.operator_credential_registry = registry
        try:
            port = await daemon.bind()
            async with websockets.connect(f"ws://127.0.0.1:{port}") as socket:
                welcome = json.loads(await socket.recv())
                await socket.send(json.dumps(operator_hello(welcome, token_path=path,
                    subscribe={"exclude_event_types": ["hosts.stats"]})))
                assert json.loads(await socket.recv())["type"] == "hello"
                assert json.loads(await socket.recv())["type"] == "snapshot"
                registry.revoke(cid)
                await socket.send('{"type":"list_sessions","request_id":"revoked"}')
                assert json.loads(await socket.recv())["error_code"] == "authentication_required"
                await daemon.broadcast({"type": "private.fixture", "payload": "private"})
                with pytest.raises(asyncio.TimeoutError):
                    await asyncio.wait_for(socket.recv(), .05)
        finally:
            await daemon.close()
    asyncio.run(run())


def test_scoped_clients_receive_only_their_own_events_and_revocation_stops_egress(tmp_path):
    async def run():
        registry, _, _, _ = credentials(tmp_path)
        daemon = Server(host="127.0.0.1", port=0, local_host="fixture")
        daemon.operator_credential_registry = registry
        sockets = []
        ids = []
        try:
            port = await daemon.bind()
            for name in ("a", "b"):
                cid, envelope = registry.issue("pentacle", scope={"stream": f"fixture:{name}"})
                ids.append(cid)
                path = tmp_path / f"{name}.token"
                path.write_text(envelope)
                path.chmod(0o600)
                socket = await websockets.connect(f"ws://127.0.0.1:{port}")
                sockets.append(socket)
                welcome = json.loads(await asyncio.wait_for(socket.recv(), 1))
                await socket.send(json.dumps(operator_hello(welcome, token_path=path, subscribe={"all": True})))
                assert json.loads(await asyncio.wait_for(socket.recv(), 1))["type"] == "hello"
                assert json.loads(await asyncio.wait_for(socket.recv(), 1))["type"] == "snapshot"
            frame = {"type": "session.inventory", "sessions": [
                {"stream_id": "fixture:a"}, {"stream_id": "fixture:b"}, {"stream_id": "fixture:private"}]}
            await daemon.broadcast(frame)
            for socket, name in zip(sockets, ("a", "b")):
                assert json.loads(await asyncio.wait_for(socket.recv(), 1))["sessions"] == [{"stream_id": f"fixture:{name}"}]
            registry.revoke(ids[0])
            frame["revision"] = 2  # inventory broadcasts suppress byte-identical repeats
            await daemon.broadcast(frame)
            assert json.loads(await asyncio.wait_for(sockets[1].recv(), 1))["sessions"] == [{"stream_id": "fixture:b"}]
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(sockets[0].recv(), .05)
        finally:
            for socket in sockets:
                await socket.close()
            await daemon.close()
    asyncio.run(run())


def test_raw_command_worker_gets_private_identity_and_can_use_real_cli(tmp_path, monkeypatch):
    async def run():
        store = Store(str(tmp_path / "state.db"))
        store.start()
        sessions = Sessions(store, local_host="fixture")
        ctl = SpawnCtl(store, sessions, machine=launch.local_machine("fixture", cwd=str(tmp_path)))
        daemon = Server(host="127.0.0.1", port=0, store=store, sessions=sessions, local_host="fixture")
        try:
            command, resolution, fields = await ctl._resolve_launch(
                {"command": "printf '%s' \"$AGENT_ORCH_STREAM_ID\"", "_defer_launch_token_stage": True},
                "fixture", "worker")
            plan = resolution["_deferred_launch_plan"]
            class Stager:
                async def stage_text(self, path, data):
                    Path(path).parent.mkdir(mode=0o700)
                    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                    with os.fdopen(fd, "wb") as output:
                        output.write(data)
            await ctl._stage_launch_token(plan, host="fixture", name="worker", provider="command", transport=Stager())
            assert read_private_token(Path(plan.stream_token_file)) == plan.stream_token
            assert fields["token_hash"] == hashlib.sha256(plan.stream_token.encode()).hexdigest()
            assert plan.stream_token not in command
            assert subprocess.check_output(["/bin/sh", "-c", command], text=True) == "fixture:worker"
            await store.open_session("fixture", "worker", **fields)
            port = await daemon.bind()
            monkeypatch.setenv("AGENT_ORCH_STREAM_ID", "fixture:worker")
            monkeypatch.setenv("AGENT_ORCH_STREAM_TOKEN_FILE", plan.stream_token_file)
            monkeypatch.delenv("AGENT_ORCH_INTERNAL_LEADER_STREAM_ID", raising=False)
            # Ambient operator material must never be used by this worker.
            config = Config(f"ws://127.0.0.1:{port}", "pentacle-auth-v2:INVALID", "fixture", tmp_path)
            assert (await wsclient._fetch_snapshot_async(config, 2))["type"] == "snapshot"
            Path(plan.stream_token_file).unlink()
            with pytest.raises(wsclient.SeatCredentialUnavailable):
                await wsclient._fetch_snapshot_async(config, 2)
        finally:
            await daemon.close()
            store.stop()
    asyncio.run(run())


def test_independent_local_admin_recovery_does_not_grant_shell_or_inventory(tmp_path, monkeypatch):
    import local_admin
    path = tmp_path / "local-admin.token"
    path.write_text("a" * 64)
    path.chmod(0o600)
    monkeypatch.setattr(local_admin.verify, "__defaults__", (path,))
    monkeypatch.setenv("AGENT_ORCH_STREAM_ID", "fixture:missing-seat")
    async def run():
        store = Store(str(tmp_path / "admin.db"))
        store.start()
        daemon = Server(host="127.0.0.1", port=0, store=store,
                        sessions=Sessions(store, local_host="fixture"), local_host="fixture")
        async def must_not_dispatch(msg):
            raise AssertionError("local-admin credential reached a general handler")
        daemon.handlers["screen.lease.status"] = must_not_dispatch
        try:
            port = await daemon.bind()
            config = Config(f"ws://127.0.0.1:{port}", "pentacle-auth-v2:INVALID", "fixture", tmp_path)
            result = await wsclient.consent_once(config, "assistant.lifecycle",
                {"action": "inspect", "local_admin_token": "a" * 64}, timeout=2, local_admin=True)
            assert result["type"] == "assistant.lifecycle.ok"
            async with websockets.connect(config.ws_url) as socket:
                await socket.recv()
                for verb, fields in (("spawn", {"command": "must-not-run"}),
                                     ("list_sessions", {}), ("screen.lease.status", {}),
                                     ("assistant.lifecycle", {"action": "designate"})):
                    await socket.send(json.dumps({"type": verb, "local_admin_token": "a" * 64, **fields}))
                    assert json.loads(await socket.recv())["error_code"] == "authentication_required"
        finally:
            await daemon.close()
            store.stop()
    asyncio.run(run())


@pytest.mark.parametrize("kind", ["mode", "symlink", "empty", "directory", "oversize", "relative"])
def test_private_credential_loader_rejects_unsafe_sources(tmp_path, kind):
    path = tmp_path / "token"
    path.write_text("synthetic")
    path.chmod(0o600)
    if kind == "mode":
        path.chmod(0o644)
    elif kind == "symlink":
        other = tmp_path / "link"
        other.symlink_to(path)
        path = other
    elif kind == "empty":
        path.write_text("")
    elif kind == "directory":
        path = tmp_path
    elif kind == "oversize":
        path.write_text("x" * 8193)
    elif kind == "relative":
        path = Path("relative.token")
    with pytest.raises(PermissionError, match="unavailable or unsafe"):
        read_private_token(path)
