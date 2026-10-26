# Daemon credentials, including localhost

Every client needs credentials to read private daemon state, subscribe to
events, or execute commands. A localhost address, omitted browser Origin, and
claimed client/stream name grant no authority. The public welcome challenge
and ping remain available; enrollment and satellite producers verify their own
owner-issued codes or service secrets. There is no anonymous development mode.

Authentication preserves the trusted operator's existing command authority.
Pentacle's web backend already supports operator proof authentication and keeps
its credential out of the browser. This change adds no command approval prompts
and does not change provider permission flags or existing authenticated seat
policies. An operator can still launch arbitrary shell commands as the daemon's
OS user. The explicitly configured `PENTACLE_SEAT_OPERATOR_AUTHORITY=1` policy
still elevates all internal authenticated seats; its default remains off.

## Operator and trusted orchestrator setup

Issue credentials on the daemon host as its OS owner using
`services/chat-stream-v2/tools/operator_auth_cli.py issue --client-kind pentacle`.
The JSON `code` is a secret v2 credential envelope. Save it without printing it
to a private regular file with mode 0600 under a private directory with mode
0700. The [local setup recipe](../README.md#local-setup) shows a pipeline that
writes `~/.config/pentacle/desktop.token`. Do not commit the file.

The web host reads `chatStream.tokenPath` in its private config. For `agent-orch`
and maintenance tools, export the path in the actual launch environment:

```sh
export AGENT_ORCH_TOKEN_FILE="$HOME/.config/pentacle/desktop.token"
agent-orch list
```

`PENTACLE_OPERATOR_TOKEN_FILE` is an alias for launch wrappers. The CLI resolves
operator sources in this order: explicit programmatic `Config.token`, or for
`load_config()` callers, `AGENT_ORCH_TOKEN` (even when empty), then
`AGENT_ORCH_TOKEN_FILE`, `PENTACLE_OPERATOR_TOKEN_FILE`,
`chat_stream.token_path` in `~/.agent-orch/config.json`, then
`~/.config/pentacle-stream/token`. Use a v2 envelope. Legacy bearer strings do
not confer operator authority. File paths must be absolute after home expansion;
symlinks, unsafe permissions, empty files and oversized values are refused.
No secret is auto-generated on client connection and there is no anonymous
fallback. A credential error requires fixing the launch configuration.

Run a trusted orchestrator's operator CLI outside a worker's seat identity
environment, with its explicitly provisioned operator credential. Worker identity
variables (`AGENT_ORCH_INTERNAL_LEADER_STREAM_ID`, `AGENT_ORCH_STREAM_ID`, and
`PENTACLE_STREAM_ID`) deliberately select worker authentication instead. A missing
worker credential never falls back to an ambient operator credential. Do not
share operator credentials with agents you intend to restrict. Authentication
alone cannot protect a secret from a process with unrestricted access to the
same OS user's files; a separate OS identity or sandbox is needed for that.

## Workers, existing sessions and schedules

Provider and raw shell launches automatically receive a fresh seat credential
in a private file on the target host. Only its path is exported through
`AGENT_ORCH_STREAM_TOKEN_FILE`, together with the stream identity. The daemon
stores the token hash. Compound raw commands receive exported identity variables
too. Tokens are staged only after admission; retries retain the admitted token.
Existing provider resume/handoff and internal scheduled execution keep their
existing authorization policies. CLI commands that create or manage schedules
now authenticate just like other RPCs.

Upgrade the daemon, web backend and CLI together. Already-running workers that
relied on anonymous access need an explicit migration before they issue more
RPCs. Prefer closing/relaunching them through the authenticated UI. For a legacy
session with no token hash, an owner can use `agent-orch grant-self-token --stream
host:session` with an operator credential to mint its initial token once, then
place it in a private file and set the worker's identity/token-file environment.
That command prints the new secret to stdout: capture it directly to a private
file, not logs or chat. Existing tokens are never overwritten by this command.
Ordinary seats and fixed service identities cannot use it to become operators.

Restart operator clients after replacing their credential file. Reconnects use a
fresh server nonce and proof, never the proof key. Revoking an operator with
`operator_auth_cli.py revoke` takes effect on the next protected RPC and private
broadcast even on an already-open connection. Registry read failures deny access.
Seat credentials keep their existing per-request status/hash checks.

## Recovery and operational tools

Local-admin consent-key ceremonies, lifecycle inspection/emergency revocation,
and emergency transfer operations still use their separate owner-only secret
and actual native loopback transport. This secret grants no general command,
inventory subscription or shell authority. These commands send their per-RPC
credential directly; they do not require an operator hello.

`read_daemon_stats.py`, `client_contract_probe.py`, `picker_under_load_probe.py`
and `tools/working_state_probe.py` read `AGENT_ORCH_TOKEN_FILE` or
`PENTACLE_OPERATOR_TOKEN_FILE` (otherwise the default operator file) and use v2
proof authentication. Live-window tools keep their explicit token-path option.
Satellite event/host producers keep their own secret protocol. Deployment health
checks use only the public welcome/build SHA and ping; that proves liveness,
not authenticated command readiness.

Anonymous sockets can no longer read `screen.lease.status`. Third-party clients
must implement the documented challenge proof or carry their provisioned seat
or service credential. Removing CORS or checking Origin cannot replace this
authentication boundary.
