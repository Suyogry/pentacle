---
id: spec_pentacle__upstream_sync_20261110
title: Merge official updates while preserving fork workflows
type: spec
status: completed
canonical: false
created_at: '2026-11-10'
updated_at: '2026-11-10'
completed_at: '2026-11-10'
source_path: work/completed/pentacle__upstream_sync_20261110/spec.md
machine: local
owner: maintainer
tags: [pentacle, integration]
related: [work_pentacle__upstream_sync_20261110]
summary: Merge official source, retain authenticated desktop compatibility and fork protections.
---

## Scope and tracking

Lead owns the requested official-source merge and standing personal-fork push
authorization. Intended and actual repository: isolated
`pentacle-upstream-20261110` worktree, origin
`https://github.com/Suyogry/pentacle.git`, branch
`codex/upstream-sync-20261110`, base fork main
`31a8ae2c037f158ea4b1f056362c95d0e1cce48f` (also origin/main).
Official `https://github.com/HJK6/pentacle.git` main at fetch:
`9b91da896f31c7abf8fb06918ce78dca70d0b465`.
Merge base `e4d744ccc59f07f161acc7716977903abde23bf0`; 199 incoming commits,
494 changed files at the initial fetch. A second fetch added three commits
and the front-desk/lane input guard, ending at official
`0b0a64f38967888c58952d9975f3403aeca8581e` (202 incoming commits). Private receipt bundle `upstream-sync-20261110` records
absolute paths, refs, conflicts and runtime/configuration preimages.

## Contract and integration decisions

Preserve both histories. Merge updated daemon admission, lane ownership,
account selection, authenticated socket rejection, recovery/deployment tools,
usage cleanup, design gallery and web renderer changes. Resolve conflicts by
contract, never by taking one whole side of shared authentication/spawn code.

Upstream removes Electron. This fork has a concrete desktop consumer and owned
isolation/sign-in/layout fixes: retain its desktop entry/preload, necessary
native adapters/builds/tests and existing patched Electron tooling as an explicit
fork compatibility layer. Keep current web/backend improvements. Public docs
must distinguish upstream's web recommendation from this fork's retained desktop
support. Do not resurrect the obsolete no-provider-sign-in test.

Preserve mandatory daemon authentication on localhost and credential separation,
mic per-request credentials and Host/Origin checks/authenticated web proxy,
desktop sandbox/context isolation, provider sign-in/limits/configuration fixes,
Cursor safe receipt framing and updated dependencies. Reconcile incoming sticky
auth-rejection and nonce/deadline protections with these fork contracts.

The separate `feat/intelligent-model-routing` branch stays byte-identical at
`c9757199674f79eac04b59e6ed0dc8f24488267f`; no PIMR code is promoted or rebased.
No personal provider calls, account enrollment/helper deployment, mic activation,
credential/configuration change, service restart or desktop package replacement.
The running daemon uses checkout source. Main promotion changes on-disk files;
it is not a qualified coordinated runtime deployment. Record continuity and
source-mode identity caveats without claiming new runtime activation.

## Acceptance and validation

- [x] Independent spec QA accepts scope and evidence plan before resolution.
- [x] Merge includes official history; explicit desktop retention and all fork
  security contracts survive; no conflict markers or accidental PIMR merge.
- [x] Dedicated Python 3.14 and exact-lock Node environment. Full CLI and root
  Node suites, changed daemon tests plus auth/account/spawn/assistant/lane/
  deployment regressions, core tests/typecheck, mic security tests, desktop/web
  builds. Audit dependencies without automatic fixes. Pin tested manifests.
- [x] Run isolated real desktop/daemon/native PTY smoke with synthetic provider
  and private temp state, plus web checks where changed. Preserve RED receipts;
  compare failures with exact untouched upstream/base before classifying them.
  No passing claim for skipped or pre-existing failing gates. Do not execute
  production/fleet deployment tools or infer live provider correctness.
- [x] Independent final source/test/cold-doc QA on frozen candidate and receipt
  hashes; no claim of full fleet/runtime certification from source checks.
- [x] Refetch before normal main fast-forward/push, verify personal main/config/
  daemon continuity and unchanged PIMR branch. Keep current installed desktop
  untouched. Clean only owned test resources/worktree; close with exact evidence.

## Checkpoint

Disposition: **Shipped source integration**. Accepted candidate
`a86a8524918ee0deedadf38d3ff573270fb61ac7` was fast-forwarded onto local main
and normally pushed to `Suyogry/pentacle` main, preserving official history
through `0b0a64f38967888c58952d9975f3403aeca8581e` and the original fork history.
Independent final source/security review accepted its unchanged source scope;
a bounded cold-doc rejection was repaired and independently accepted with a
real credentialed profile-to-host-to-isolated-daemon connection, missing-token
refusal and owned cleanup. QA receipt hashes are in `_artifacts/validation.md`.

Validation: CLI 8,122 passed/13 skipped; core runtime tests and type checks
passed; 46 mic boundary tests and 491 affected auth/account/lane/recovery/spawn
controls passed. Desktop synthetic-provider/native PTY/auth/isolation smoke and
web chat/config/voice/gallery/dashboard plus terminal type/resize/detach passed.
Root Node has 206 passing files and two harness failures; both unchanged files
passed isolated recheck. The broad daemon run captured 5,127 passed/29 failed;
ten failures were repaired and passed focused controls. The 19 residual IDs each
reproduce on untouched official upstream or original fork. These remain failed
gates; maintainer owns follow-up before full fleet/runtime certification. No
criterion claims those broad runs were green. Production audit zero; full audit
six moderate tooling entries, no high/critical. Existing production dependency
versions and all fourteen protected preimage files are unchanged.

Main desktop/web assets rebuilt successfully. Actual daemon authenticated hello
and spawn catalog readbacks pass before/after promotion, with the same PID and
unchanged private wrapper/service/configuration hashes. PIMR ref is unchanged.
No provider inference, personal service restart/activation, mic capture or
packaged desktop replacement occurred. Main source files changed on disk; these
readbacks establish continuity, not activation or certification of the new
backend. Private receipts remain in bundle `upstream-sync-20261110`. Only owned
comparison/integration worktrees are eligible for cleanup after remote readback.

## Retro

An upstream removal is a product decision, not an instruction to erase a
fork's concrete desktop consumer. Keep that compatibility boundary explicit.
Authenticate positive test controls rather than restoring localhost exemptions;
retain negative proof and native cleanup guards. Captured RED distinguished
stale test assumptions from product regressions and system-inspection timeouts.
Baseline comparisons and unchanged artifacts bound reused evidence.
