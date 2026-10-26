"""Operator authentication for maintenance clients using the public challenge."""
import os
from pathlib import Path

from . import operator_auth
from .private_credentials import read_private_token


def operator_hello(welcome: dict, *, token_path: Path | None = None,
                   subscribe: dict | None = None, **fields) -> dict:
    path = token_path or Path(os.environ.get("AGENT_ORCH_TOKEN_FILE")
                              or os.environ.get("PENTACLE_OPERATOR_TOKEN_FILE")
                              or "~/.config/pentacle-stream/token").expanduser()
    credential = operator_auth.decode_envelope(read_private_token(path))
    challenge = welcome.get("auth", {}).get("operator", {})
    if (welcome.get("type") != "welcome" or challenge.get("protocol_version") != 2
            or challenge.get("scheme") != operator_auth.AUTH_SCHEME):
        raise PermissionError("operator credential challenge unavailable")
    return {**fields, "type": "hello", "client": credential["client_kind"],
            "subscribe": subscribe if subscribe is not None else {"snapshot": False, "mode": "rpc"},
            "auth_v2": {"scheme": operator_auth.AUTH_SCHEME,
                        "credential_id": credential["credential_id"],
                        "proof": operator_auth.make_proof(credential["proof_key"], challenge.get("nonce"),
                                                          credential["credential_id"], credential["client_kind"])}}
