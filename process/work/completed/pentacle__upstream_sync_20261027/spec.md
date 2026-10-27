---
id: spec_upstream_sync_20261027
title: Merge official Pentacle updates while preserving fork security fixes
type: spec
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__upstream_sync_20261027/spec.md
machine: local
owner: maintainer
tags: [upstream, maintenance, security]
summary: Integrate official changes in isolation, preserve fork hardening, validate and push the personal fork.
related: [work_upstream_sync_20261027]
---

## Scope and authority

User requests latest official code integrated into their fork and explicitly
requests push to Suyogry/pentacle after passing checks. Lead owns normal merge,
conflict repair, tests and push to origin main. Use an isolated Git worktree;
keep existing personal desktop/daemon running their current processes. No
provider/account login, credential change, paid provider call, mic capture,
force/reset/rebase or personal runtime restart. Source push is delivery; loading
new code into personal services is a separate activation step.

## Tracking and diagnosis

Intended and actual repository pentacle, origin https://github.com/Suyogry/pentacle.git,
official upstream https://github.com/HJK6/pentacle.git. Personal main preimage
50e53b5cc0904e04245779389c91798fac41f720, origin main9feb8c310ff52fe353202d2f912db5f7a53b1693, merge base
42698e64dcb33e2e6329fc9faf8c6a689226f7cd. Official main 30a8acea51ad05951eeeb480e66015591c0ce4ac,
50 incoming commits and100 changed files. Source tree clean. Isolated branch
codex/upstream-sync-20261027 starts at the exact personal main preimage.
Read-only merge preview identifies three conflicts: docs/REMOTE_AUTH.md,
services/chat-stream-v2/server.py and tests/test_remote_rpc_admission.py.
Upstream fixes privileged-loopback admission while this fork already enforces
mandatory operator/seat authentication on all transports. Preserve the stronger
fork boundary and add upstream privileged-RPC defense behind it; never restore
anonymous ordinary-RPC bootstrap. Reconcile tests/docs to the combined policy.
No dependency manifests/locks change in the incoming diff.

## Contract

Normal merge retains both histories and all prior microphone Host/Origin/auth,
mandatory daemon auth, safe operator/seat propagation, Electron isolation,
Electron44.9.3 tooling updates, Settings scrolling and Claude sign-in prefix fix.
Keep upstream chat optimistic identity, held-send payload checks, bounded-event
previews, satellite history recovery, QA verdict validation, Terra catalog and
spawn-spec diagnostics. Inspect automatic merges for authorization compatibility.
Use separate install/build outputs in the isolated worktree. Preserve original
failure evidence and repair only diagnosed merge/fixture compatibility defects.

## Validation

Independent plan review before merge. Inspect conflict resolutions and unchanged
fork-security file hashes. Exact-lock install/tree audit; shared-core tests and
typecheck; full root Node suite with supported Python and120s per-file budget;
affected daemon tests plus mandatory-auth/admission/security regressions; full
agent-orch tests; focused mic auth/action checks; changed gate/selection tests.
Desktop/web builds and disposable actual production Electron authenticated
daemon/synthetic provider/native PTY/tmux smoke, rehearsal then final confirmation.
No personal profile/account/audio/clipboard or fleet deployment checks. Code,
shared harness and renderer changes need these broad gates; no paid-provider,
cross-platform or actual fleet qualification claimed. If shared Node process
inspection times out, preserve valid cells and explicitly recover only missing
coverage under unchanged inputs rather than weakening its budget.

Freeze source candidate and evidence for independent final QA. Recheck official
and origin refs before promotion; normal fast-forward personal main to accepted
integration, validate process metadata, push to Suyogry/pentacle main without force,
and verify remote SHA and clean worktree. If official main moves materially,
assess the delta before expanding scope; do not silently call an older ref latest.
Raw receipts are private under upstream-sync-20261027 with public hash pointers.

## Acceptance

- [x] Official captured main is ancestor, fork hardening and local fixes preserved.
- [x] Relevant broad gates and actual isolated desktop flows pass; independent QA accepts.
- [x] Local main and remote fork updated normally; metadata valid and tree clean.

## Closure

Shipped source update to the personal fork: normal merge 66bd92dd7ce5df4ca9096434a33609ae7dbf152e retains personal
main50e53b5 and official30a8ace as parents, promoted by fast-forward and pushed
to Suyogry/pentacle main. Remote SHA readback matched the merge. Reviewed source
diff remainsc626e25f8e06a31351bb02d39d40e9687ac2e98d21d5dca020b6034809aaeea6.
Independent plan/final QA ACCEPT; all final gates passed. Both personal checkout
renderer artifacts rebuilt for the next launch. No running personal process was
restarted or provider account touched. Closure metadata is committed/pushed as a
follow-up, with final remote/clean readback retained privately.
Evidence: [_artifacts/validation.md](_artifacts/validation.md).

## Retro

An upstream security fix can retain a trust assumption that this fork already
removed. Merge policies explicitly instead of preferring a whole side. Give
upstream fixtures the same private authentication and staging contracts as real
clients; retain their no-effects assertions. Run installer dry-run checks with
the documented explicit interpreter rather than assuming a platform's optional
fixed-version discovery paths exist.
