---
id: spec_pentacle__upstream_sync_20261110
title: Merge official updates while preserving fork workflows
type: spec
status: in_progress
canonical: false
created_at: '2026-11-10'
updated_at: '2026-11-10'
source_path: work/in_progress/pentacle__upstream_sync_20261110/spec.md
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
- [ ] Dedicated Python 3.14 and exact-lock Node environment. Full CLI and root
  Node suites, changed daemon tests plus auth/account/spawn/assistant/lane/
  deployment regressions, core tests/typecheck, mic security tests, desktop/web
  builds. Audit dependencies without automatic fixes. Pin tested manifests.
- [ ] Run isolated real desktop/daemon/native PTY smoke with synthetic provider
  and private temp state, plus web checks where changed. Preserve RED receipts;
  compare failures with exact untouched upstream/base before classifying them.
  No passing claim for skipped or pre-existing failing gates. Do not execute
  production/fleet deployment tools or infer live provider correctness.
- [ ] Independent final source/test/cold-doc QA on frozen candidate and receipt
  hashes; no claim of full fleet/runtime certification from source checks.
- [ ] Refetch before normal main fast-forward/push, verify personal main/config/
  daemon continuity and unchanged PIMR branch. Keep current installed desktop
  untouched. Clean only owned test resources/worktree; close with exact evidence.

## Checkpoint

Source integration complete on the isolated branch; both official histories
are ancestors. Independent plan QA accepted before resolution. Retained desktop
entry/preload/native dependency closure, patched Electron tooling and native
bridge tests; upstream web/backend/lane/account/auth/recovery changes integrated.
No PIMR branch, personal configuration or service was changed.

Validation: CLI 8,122 passed/13 skipped; core tests and both type checks passed;
46 mic boundary tests passed; 491 final affected auth/account/lane/recovery/
spawn controls passed; desktop real PTY/authenticated synthetic-provider smoke
and six browser scenarios passed with owned cleanup. Root Node run has 206
passing files plus two harness failures (pre-push file budget and native process
inspection); both original files passed isolated recheck with clean cleanup,
without changing guards. Broad daemon capture: 5,127 passed/29 failed; ten
failures were corrected with authentic test credentials, faithful token staging,
correlated probe reads and stale-proof refusal handling. The 19 remaining IDs
are each reproduced on untouched official upstream or the original fork;
`baseline-failure-classification.json` records the exact sets. They remain
explicit failed gates, not claimed passing results. Owner maintainer retains
follow-up before any full fleet/runtime certification.

Production npm audit is zero; full audit retains six moderate tooling entries,
no high/critical. All 14 protected preimage files and existing production lock
versions are unchanged. Source-only integration; no runtime/fleet certification
or live provider inference is claimed. Next: freeze candidate/evidence for
independent final source, test and cold-documentation QA, then normal main
fast-forward and personal-fork push if accepted.

## Retro

An upstream removal is a product decision, not an instruction to erase a
fork's concrete desktop consumer. Keep that compatibility boundary explicit.
Authenticate positive test controls rather than restoring localhost exemptions;
retain negative proof and native cleanup guards. Captured RED distinguished
stale test assumptions from product regressions and system-inspection timeouts.
Baseline comparisons and unchanged artifacts bound reused evidence.
