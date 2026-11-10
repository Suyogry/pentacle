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
494 changed files. Private receipt bundle `upstream-sync-20261110` records
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

- [ ] Independent spec QA accepts scope and evidence plan before resolution.
- [ ] Merge includes official history; explicit desktop retention and all fork
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

Clean fork main and remote verified. Isolated worktree created; merge-tree
preview identifies content and Electron modify/delete conflicts. Independent spec QA ACCEPT; source integration and validation plan locked.
Next: resolve the isolated merge, run the pinned gates, then independent final QA. Owner is maintainer.

## Retro

Pending integration and validation.
