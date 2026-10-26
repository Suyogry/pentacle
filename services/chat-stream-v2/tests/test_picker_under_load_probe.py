"""The picker probe drives authenticated event.push, then fails closed if slow."""

from __future__ import annotations

import json
import sqlite3
import time
from pathlib import Path

import picker_under_load_probe as probe


SHA = "a" * 40


class StubSocket:
    def __init__(self, harness: "StubHarness", *, kind: str, delay: float) -> None:
        self.harness = harness
        self.kind = kind
        self.delay = delay
        self.sent: list[dict] = []
        self.received: list[dict] = []
        self.catalog_sent_at = 0.0
        from server import _welcome_frame
        from _shared import operator_auth
        self._incoming = [_welcome_frame(nonce=operator_auth.encode_b64url(b"n" * 32), expires_at=time.time()+10)]

    def __enter__(self):
        return self

    def __exit__(self, *_args: object) -> None:
        return None

    def send(self, payload: str) -> None:
        frame = json.loads(payload)
        self.sent.append(frame)
        if frame.get("type") == "hello":
            self._incoming.extend([
                {"type": "hello", "request_id": frame["request_id"]},
                {"type": "snapshot"},
            ])
        if frame.get("type") == "event.push":
            events = frame["events"]
            pushed = [
                {"type": "chat.event", "event": dict(event)}
                for event in events
            ]
            # The producer sees its own broadcast before its correlated ack;
            # the observer receives every frame while catalog is in flight.
            self._incoming.extend(pushed)
            self._incoming.append({
                "type": "event.push.ok", "request_id": frame["request_id"],
                "accepted": len(events), "inserted": len(events),
                "version": {"status": "ok", "target_sha": SHA},
            })
            self.harness.observer._incoming.extend(pushed)
        if frame.get("type") == "spawn_catalog_get":
            self.catalog_sent_at = time.monotonic()
            self._incoming.append({"type": "spawn_catalog_get.ok", "request_id": "picker-catalog"})

    def recv(self, *, timeout: float) -> str:
        if not self._incoming:
            raise AssertionError(f"{self.kind} received with no scripted frame")
        frame = self._incoming.pop(0)
        if frame.get("type") == "spawn_catalog_get.ok":
            remaining = self.delay - (time.monotonic() - self.catalog_sent_at)
            if remaining > 0:
                time.sleep(min(remaining, timeout))
        self.received.append(frame)
        return json.dumps(frame)


class StubHarness:
    def __init__(self, *, delay: float) -> None:
        self.observer = StubSocket(self, kind="observer", delay=delay)
        self.producer = StubSocket(self, kind="producer", delay=delay)
        self._connections = iter((self.observer, self.producer))

    def connect(self, *_args: object, **_kwargs: object) -> StubSocket:
        return next(self._connections)


def _secret_db(tmp_path: Path) -> Path:
    path = tmp_path / "sessions.db"
    with sqlite3.connect(path) as conn:
        conn.execute("CREATE TABLE kv (k TEXT PRIMARY KEY, v TEXT)")
        conn.execute("INSERT INTO kv(k, v) VALUES (?, ?)", ("event_push.secret", "TEST"))
    return path


def test_probe_exit_contract(monkeypatch, tmp_path: Path) -> None:
    from _shared import operator_auth
    envelope = operator_auth.encode_envelope("00000000-0000-4000-8000-000000000001", "pentacle", b"k" * 32)
    credential_path = tmp_path / "operator.token"
    credential_path.write_text(envelope)
    credential_path.chmod(0o600)
    monkeypatch.setenv("AGENT_ORCH_TOKEN_FILE", str(credential_path))
    db = _secret_db(tmp_path)
    fast = StubHarness(delay=0.01)
    monkeypatch.setattr(probe, "connect", fast.connect)
    args = [
        "--url", "ws://stub", "--stream", "hosta:history", "--burst", "2",
        "--target-sha", SHA, "--db", str(db),
    ]
    assert probe.main(args) == 0
    pushed = next(frame for frame in fast.producer.sent if frame["type"] == "event.push")
    assert pushed["push_secret"] == "TEST"
    assert pushed["satellite_sha"] == SHA
    assert len(pushed["events"]) == 2
    assert [frame["type"] for frame in fast.observer.received].count("chat.event") == 2

    slow = StubHarness(delay=1.01)
    monkeypatch.setattr(probe, "connect", slow.connect)
    assert probe.main(args) != 0
