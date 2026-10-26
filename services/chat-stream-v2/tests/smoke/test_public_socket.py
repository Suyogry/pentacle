"""Public smoke tier: the actual WebSocket accept loop serves a local snapshot."""
import asyncio
import json
import websockets
from server import Server
from _shared.operator_auth import OperatorCredentialRegistry
from _shared.operator_client import operator_hello


def test_loopback_hello_snapshot_and_unknown_command_error(tmp_path):
    async def run():
        server = Server(host="127.0.0.1", port=0)
        directory = tmp_path / "auth"
        directory.mkdir(mode=0o700)
        server.operator_credential_registry = OperatorCredentialRegistry(directory / "registry.json")
        _, envelope = server.operator_credential_registry.issue("pentacle")
        token_path = directory / "operator.token"
        token_path.write_text(envelope)
        token_path.chmod(0o600)
        port = await server.bind()
        try:
            async with websockets.connect(f'ws://127.0.0.1:{port}') as socket:
                welcome = json.loads(await socket.recv())
                assert welcome['type'] == 'welcome'
                await socket.send(json.dumps(operator_hello(welcome, token_path=token_path, subscribe={'all': True})))
                frames = [json.loads(await socket.recv()) for _ in range(2)]
                assert any(frame['type'] == 'snapshot' for frame in frames)
                await socket.send(json.dumps({'type': 'public_unknown_command', 'request_id': 'negative'}))
                async with asyncio.timeout(3):
                    while True:
                        reply = json.loads(await socket.recv())
                        if reply.get('error_code') == 'unsupported_in_v2':
                            break
                assert reply['type'].endswith('error')
        finally:
            await server.close()
    asyncio.run(run())
