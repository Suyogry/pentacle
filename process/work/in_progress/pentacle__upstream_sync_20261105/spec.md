---
id: spec_pentacle__upstream_sync_20261105
title: Integrate official Cursor and Codex updates
type: spec
status: in_progress
canonical: false
created_at: '2026-11-05'
updated_at: '2026-11-05'
source_path: work/in_progress/pentacle__upstream_sync_20261105/spec.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Merge official updates while preserving fork security and existing provider workflows.
related:
- work_pentacle__upstream_sync_20261105
---

## Scope and tracking

Lead owns the user-requested careful source merge, with standing personal-fork
push authority. Intended/actual repository pentacle, origin
https://github.com/Suyogry/pentacle.git, base
`a966dc423585d4193bd0e8b9233f382415cd5331`, integration branch
`codex/upstream-sync-20261105`. Official https://github.com/HJK6/pentacle.git
main `e2ab95f514198f3eb2a2a1e169ddaa41cd99ec58`: five new commits, 38 files.
Clean main, refs and merge-tree identity verified; independent private plan QA
ACCEPT before merge. Local identities and raw receipts remain private.

## Contract

Normal merge preserves both histories, mandatory daemon/seat/operator proof,
mic Host/Origin/authenticated proxy, isolated desktop/CSP, working provider
sign-in, Settings sizing, and autonomous authenticated operator authority.
Incoming work adds optional local Cursor CLI seats and prevents Codex native
workers from becoming primary rollout candidates. No provider install/login,
real inference, personal app/daemon/mic restart, credentials/configuration change
or dependency upgrade is in scope.

Inspect automatic merges and all new launch/admission/ingest/receipt paths.
Preserve private seat-token staging and fail-closed identity separation. Fix
only demonstrated compatibility defects; keep failed receipts and meaningful
negative assertions. Fifteen security/sign-in/dependency preimage files match
byte-for-byte after merge.

## Validation plan

Scoped source integration; runtime/native dependencies and shared harnesses
are unchanged. Exact-lock isolated root npm install, private Python testenv.
Full bounded root Node suite, full CLI suite, explicit affected-daemon root-file
manifest including every changed test, Cursor fake-CLI/default and retained-shell
pane variants, Codex worker/guardian/ambiguity cases, existing provider launch/
boot/ingest/defaults/catalog/account/token-staging and mandatory-auth checks.
Exclude soak/fleet/live suites as documented; retain explicit skip prerequisites.
Build desktop/web and one scoped real isolated Electron/authenticated daemon/
synthetic-provider/native PTY/tmux smoke with unchanged owned-cleanup harness.
Reuse previous core/typecheck and unchanged broader mic/auth baseline within
actual input bounds. Capture full/production npm audit without auto-fixes.
No full fleet/mobile/paid-provider/default-CI certification claimed.

Freeze source/evidence for independent final code/tests/docs QA. Refetch refs,
fast-forward clean personal main and push normally only after ACCEPT. Rebuild
ignored assets for next launch, without restarting personal services. Verify
remote/local identity and clean checkout; close metadata with validation/digest
pointers and remove only the owned worktree. After a failure classify product,
fixture or cleanup and recover only affected cells, preserving accepted evidence.

## Acceptance

- [x] Scope, identity and independent plan QA established.
- [ ] Official main integrated and supported fork contracts preserved.
- [ ] Required scoped gates and independent final QA accepted.
- [ ] Personal main/fork pushed normally and clean readback verified.

## Checkpoint

Conflict-free integration prepared; critical preimages unchanged. Next: scoped
source gates, isolated desktop proof, final QA and normal promotion.
