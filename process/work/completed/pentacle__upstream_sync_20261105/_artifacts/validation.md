# Official Cursor/Codex integration — 2026-11-05

Personal preimage `a966dc423585d4193bd0e8b9233f382415cd5331`; official
`e2ab95f514198f3eb2a2a1e169ddaa41cd99ec58`, rechecked before promotion.
Five incoming commits across 38 files. Normal merge `8dffc7b3` retains both
histories. Final source candidate `56d0eb78c06e20c5d6f94a5e0f8575a31fff1ab3`.

## Behavior and preservation

Adds optional local Cursor CLI seats and the Codex native-worker primary-rollout
discovery fix. Cursor installation/sign-in/version pinning remain explicit setup;
no Cursor or provider account was installed, configured or invoked for inference.
Existing Codex/Claude/Gemini branches remain tested. Fifteen protected security,
sign-in and dependency files match the preimage byte for byte. Mandatory daemon
operator/seat proof, mic authentication/Host/Origin/proxy, desktop isolation/CSP,
working provider sign-in and Settings sizing remain unchanged. No orchestrator
permission or command-authority policy changed.

Independent review found a new upstream Cursor receipt-framing flaw: provider
tool metadata could inject a newline and imitate an input-admission marker.
The fork sanitizes terminal controls and prefixes each logical display line,
leaving original transcript data intact. Ten actual output-to-predicate regression
cases were RED (four failures) then GREEN; independent replay confirms the
original forged receipt is rejected. Existing tmux capture joins wrapped lines.

## Validation and bounded recovery

- Full bounded root Node suite: 210 files pass, no runner or cleanup errors.
- Full CLI: 8,068 passed, 13 optional instruction-memory snapshot skips.
- Explicit daemon manifest: 38 root test files, including every changed daemon
  test and existing provider/launch/ingest/Codex/satellite/auth/token-staging checks.
  Original result: 719 passed and four fixture failures, retained as failed.
  Three repaired files then pass all 76 tests, covering every failed case and
  all 52 Cursor cases, including native default-shell/retained-shell journeys.
  Accepted unchanged coverage is reused within its actual input bounds.
- The two catalog fixtures now prove a real issued operator challenge and reject
  forged anonymous context. The telemetry fixture asserts the earlier mandatory
  denial, reason/count/log/no-placeholder behavior and no invalid handler entry.
  The timeout fixture shortens only its intended status probe. Production auth
  and timeout rules were not relaxed to satisfy tests.
- Desktop/web builds pass. Actual isolated Electron plus an authenticated daemon,
  synthetic provider and native PTY/tmux passes chat rendering, terminal, popout/
  dock, reconnect, notifications/schedules, isolation negatives and disconnected
  refusal. Cleanup confirms owned Electron/daemon exited and tmux/credentials
  absent, with no errors. Screenshot inspected; fixture reply is visible along
  with the baseline transient loading label, not a claim of cosmetic perfection.
- Core/typecheck and broader mic/security evidence are reused from the unchanged
  prior baseline only within the paths/harness/interpreter bounds in the private
  reuse receipt. No fresh microphone capture occurred.

Source Node/CLI checks used merge candidate `8dffc7b3`; later production changes
are limited to the daemon's Cursor REPL framing, fully covered by final provider
checks and native smoke. Builds ran on `b41db408`; later changes are fixtures and
process metadata only. Native smoke ran on final source `56d0eb78`. No receipt
is relabeled with a source identity it did not execute.

## Scope and receipts

macOS arm64, Node 24.17.0 and Python 3.14.6 local validation. Exact root lock
installed; no manifest/lock changes. Production npm audit is zero. Full audit
retains the existing minimatch advisory represented by six moderate build-tool
entries; no high or critical findings. No automatic dependency fixes were made.

No personal runtime restart, provider login/inference, fleet/mobile/full soak or
full default-CI certification is claimed. Raw receipts, screenshots and private
paths remain in the maintainer's `upstream-sync-20261105` bundle. The public
receipt inventory contains names and SHA256 digests only.

## Independent acceptance and source disposition

Independent final QA ACCEPT on the frozen source candidate above. The reviewer
ran 93 focused checks, verified all 32 original receipt hashes and inspected
source, docs, preserved hashes and native proof/cleanup. Personal main was
fast-forwarded and pushed normally; desktop/web assets were rebuilt there for
next launch. This closure changes process metadata only; accepted runtime source
remains unchanged.

Final catalog generation and full/source-only metadata validation passed for
44 documents. Five pre-existing stale-work warnings remain.
