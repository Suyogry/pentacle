# Official helper deployment and launcher verification integration

Date: 2026-11-05. Personal base `ac9cec6894228265589c0969cb31e2fadc7e41ea`.
Official main `e4d744ccc59f07f161acc7716977903abde23bf0`, rechecked before
promotion. Three commits across 24 files: attachment publishing documentation,
coordinated immutable account-helper/daemon deployment, and resolved-target/hash
native launcher verification. Normal merge source candidate
`541c5ba5f0d23b86e14d48c48ca2b332c9c10da9` retains both histories.

## Preservation and source scope

No conflicts or custom source repairs were needed. Eighteen protected files match
the personal preimage, including daemon authentication, seat/operator client
boundaries, mic Host/Origin/authenticated proxy, desktop isolation/sign-in/config,
renderer/Settings, Cursor receipt framing and dependency manifests/lock. Existing
application and orchestration policies are preserved.

This is source integration, not a helper deployment or daemon upgrade. Personal
services and account helpers were not restarted, replaced or activated. The
existing source-mode daemon retains its prior startup revision and PID. Updating
checkout files does not make that running process an immutable new release:
code-identity helpers can read source bytes dynamically. No new live account-
helper or runtime release qualification is claimed. Named-account policy is not
configured in the existing service/environment/manager; the source default is off.

## Scoped checks

- Explicit daemon manifest: 29 root files, including every changed daemon test,
  coordinated transaction/disposable-resource guards, launcher process/hash
  variants, account pin/maintenance/recovery, capability manifest, deployment
  selection/rollback and fork authentication. 1,228 passed plus 720 subtests.
- CLI installer/profile/spawn/credential-boundary/close selection: 1,595 passed.
- Focused Node security/config/sign-in/limits/governance: nine files passed,
  exit zero and clean process/directory cleanup.
- Desktop and web builds passed. Actual isolated Electron, authenticated daemon,
  synthetic provider and native PTY/tmux passed the owned desktop smoke. Chat
  reply/terminal, popout/dock, schedules/notifications, reload/reconnect and
  disconnected refusal plus isolation negatives pass. Owned Electron/daemon
  exited; tmux and generated credentials are absent; no cleanup errors.
  Screenshot inspected: synthetic reply visible with the known transient loading
  label, not a claim of cosmetic perfection.
- The new coordinated-harness test exercises real disposable process/helper
  forward failure and explicit rollback. Test bindings reject production labels,
  ports and paths before effects. No production/fleet deploy CLI was invoked.
- Recent full Node 210, CLI 8,068 and core/typecheck coverage is reused only for
  unchanged paths/harness/interpreter/configuration bounds recorded privately.
- Exact root lock installed under Node 24, dedicated Python 3.14 testenv. No
  dependencies changed. Production audit is zero; full audit retains the same
  minimatch advisory represented by six moderate build-tool entries, no high or
  critical findings. No automatic audit fixes performed.

## Personal service continuity and observer correction

Read-only authenticated usage snapshot matches the actual collector state, with
both providers healthy; service PID and configuration hash match preimages.
No extra provider probe was started. An ancillary observer initially requested
RPC/no-snapshot mode while waiting for a snapshot, then used desktop proof for
an optional account status operation requiring seat proof. Both failures are
retained as observer mistakes. Correct snapshot subscription and configuration-
metadata policy checks pass without bypassing authentication or changing a
credential, service, data record or production guard. Observer connections close.

## Limits and receipts

Local macOS arm64/Node 24.17/Python 3.14.6 source validation, with separately
installed default release-selection toolchain prerequisites. This is not full
fleet/mobile/default-CI, live-provider inference or production launcher
certification. Raw local data, screenshots and readbacks remain in the private
`upstream-sync-20261105-2` bundle; public receipt references contain names and
SHA256 values only. Source and tested artifact identities are explicit.

## Independent acceptance and source disposition

Independent final QA ACCEPT on the frozen merge candidate. Reviewer verified all
30 original evidence hashes, 18 protected-file hashes, reuse bounds, source/docs,
34 focused tests and the native macOS self-image proof, gates and screenshot/
cleanup. Main was fast-forwarded and pushed normally, both assets rebuilt, and
post-promotion readback confirms same service PID/config and healthy usage.
Closure is process metadata only; accepted source bytes remain unchanged.
