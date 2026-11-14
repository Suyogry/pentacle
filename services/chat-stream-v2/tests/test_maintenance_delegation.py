"""Delegated holds use authenticated seats and durable, synthetic grants only."""
import asyncio
from contextlib import asynccontextmanager
import hashlib
import os

from assistant_composite import AssistantComposite, AssistantCompositeConfig
from store import STREAM_TOKEN_HASH_VERSION
from test_loopback_privileged_rpc import rpc
from test_provider_cli_maintenance import ready_daemon

ACTOR = "fixture-fd:primary"
GENERATION = "fd-generation"
ADVISOR = "fixture-advisor:advisor"
ADVISOR_GENERATION = "advisor-generation"
COMPOSITE = "fixture-chat:assistant"
DISPATCH = "fixture-operator-dispatch"
TELL = "fixture-advisor-ruling"
TOKEN = "synthetic-fd-token"


@asynccontextmanager
async def delegated_daemon(tmp_path, monkeypatch):
    async with ready_daemon(tmp_path, monkeypatch) as fixture:
        daemon, store, runtime, host, selected, row, request = fixture
        await store.open_session("fixture-fd", "primary", session_generation=GENERATION, provider="codex")
        await store.grant_stream_token("fixture-fd", "primary", hashlib.sha256(TOKEN.encode()).hexdigest(), STREAM_TOKEN_HASH_VERSION)
        await store.open_session("fixture-advisor", "advisor", session_generation=ADVISOR_GENERATION,
                                 provider="codex", pane_status="pane_alive")
        config = AssistantCompositeConfig.from_env({
            "PENTACLE_ASSISTANT_COMPOSITE_ENABLED": "1",
            "PENTACLE_ASSISTANT_COMPOSITE_STREAM_ID": COMPOSITE,
            "PENTACLE_ASSISTANT_DIRECT_PRIMARY_STREAM_ID": ACTOR,
            "PENTACLE_ASSISTANT_DIRECT_PRIMARY_GENERATION": GENERATION,
            "PENTACLE_ASSISTANT_AUTHORITY_STREAM_ID": ADVISOR,
        })
        daemon.assistant_composite = AssistantComposite(store, config=config)
        await store.submit(lambda conn: conn.execute(
            "INSERT INTO v2_assistant_composite_routes "
            "(route_id,stream_id,input_identity,payload_digest,input_request_id,event_id,body,actor_stream_id,"
            "routing_state,delivery_state,dispatch_id,route_target,route_target_generation,created_at,updated_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            ("fixture-route", COMPOSITE, "fixture-input", "fixture-digest", "fixture-request", 42,
             "Delegate one repair hold", "operator:fixture-credential", "resolved", "landed", DISPATCH,
             ACTOR, GENERATION, "2026-11-14T00:00:00Z", "2026-11-14T00:00:00Z")))
        line = (f"DELEGATED-HOLD v1 dispatch={DISPATCH} actor={ACTOR}/{GENERATION} "
                f"host={selected.host} maintenance={request['maintenance_id']} ttl_max_s=900")
        await store.put_tell_delivery(TELL, {"payload_digest": "fixture-ruling-digest", "reply": {"type": "tell.ok"},
            "delivery": {"from_stream_id": ADVISOR, "to_stream_id": ACTOR, "text": line,
                         "sender_verified": True, "sender_kind": "peer", "sender_generation": ADVISOR_GENERATION}})
        request = {k: v for k, v in request.items() if k != "local_admin_token"}
        request.update(from_stream_id=ACTOR, stream_token=TOKEN,
                       delegation={"source_dispatch_id": DISPATCH, "ruling_tell_id": TELL})
        yield daemon, store, runtime, selected, request


def test_fd_delegated_freeze_records_grant_and_actual_actor(tmp_path, monkeypatch):
    async def run():
        async with delegated_daemon(tmp_path, monkeypatch) as (daemon, store, runtime, selected, request):
            result = await rpc(daemon, "spawn_freeze", **request)
            assert result.get("error_code") is None, result.get("error_code")
            assert result["type"] == "spawn_freeze.ok"
            owner = result["receipt"]["owner"]
            assert owner["stream_id"] == ACTOR
            assert owner["session_generation"] == GENERATION
            assert not owner["operator_authenticated"] and not owner["local_admin_verified"]
            grant = owner["delegation"]
            assert grant["source_dispatch_id"] == DISPATCH
            assert grant["source_event_id"] == 42
            assert grant["source_operator_principal"] == "operator:fixture-credential"
            assert grant["ruling_tell_id"] == TELL
            assert grant["ruling_sender_stream_id"] == ADVISOR
            assert grant["ruling_sender_generation"] == ADVISOR_GENERATION
            assert grant["advisor_binding"] == {"stream_id": ADVISOR, "generation": ADVISOR_GENERATION, "source": "env"}
            assert (await rpc(daemon, "spawn_freeze", **request))["receipt"] == result["receipt"]
            assert "PENTACLE_SEAT_OPERATOR_AUTHORITY" not in os.environ
    asyncio.run(run())
