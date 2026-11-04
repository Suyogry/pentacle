"""Client cleanup must carry its owned generation to the daemon fence."""
import asyncio
import json

from agent_orch import wsclient
from agent_orch.config import Config


def test_close_owned_generation_reaches_wire(monkeypatch, tmp_path):
    class Socket:
        sent = None
        closed = False

        async def send(self, raw):
            self.sent = json.loads(raw)

        async def recv(self):
            return json.dumps({"type": "close.ok", "request_id": self.sent["request_id"], "stale_generation": True})

        async def close(self):
            self.closed = True

    socket = Socket()

    async def connect(*args, **kwargs):
        return socket

    monkeypatch.setattr(wsclient, "_connect_rpc_ready", connect)
    result = asyncio.run(wsclient.close_once(Config("ws://fixture", "", "fixture", tmp_path),
                                             "fixture:worker", expected_generation="owned-old"))
    assert socket.sent["expected_generation"] == "owned-old"
    assert result["stale_generation"] and socket.closed


def test_close_ambient_seat_proves_request_without_operator(monkeypatch, tmp_path):
    import os
    from agent_orch import send_boundary
    monkeypatch.setattr(os, "environ", {"AGENT_ORCH_STREAM_ID": "fixture:seat",
                                       "AGENT_ORCH_STREAM_TOKEN": "synthetic-seat-token"})

    def forbidden(*args, **kwargs):
        raise AssertionError("seat close loaded operator credentials")
    monkeypatch.setattr(wsclient, "resolve_operator_token", forbidden)
    monkeypatch.setattr(send_boundary, "resolve_operator_token", forbidden)

    class Socket:
        closed = False
        frames = []
        async def send(self, raw):
            frame = json.loads(raw)
            self.frames.append(frame)
            assert frame["type"] == "close", "retired seat must not authenticate a general hello"
            assert frame["from_stream_id"] == "fixture:seat"
            assert frame["stream_token"] == "synthetic-seat-token"
            assert "token" not in frame and "auth_v2" not in frame
        async def recv(self):
            return json.dumps({"type": "close.already_closed", "request_id": self.frames[-1]["request_id"]})
        async def close(self):
            self.closed = True
    socket = Socket()
    async def connect(*args, **kwargs):
        return socket
    monkeypatch.setattr(wsclient.websockets, "connect", connect)
    result = asyncio.run(wsclient.close_once(Config("ws://fixture", "", "fixture", tmp_path),
                                             "fixture:seat", expected_generation="owned"))
    assert result["type"] == "close.already_closed" and socket.closed
    assert len(socket.frames) == 1
