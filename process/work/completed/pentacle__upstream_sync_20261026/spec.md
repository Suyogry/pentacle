---
id: spec_upstream_sync_20261026
title: Pull official Pentacle main while preserving fork security fixes
type: spec
status: completed
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
completed_at: '2026-10-26'
source_path: work/completed/pentacle__upstream_sync_20261026/spec.md
machine: local
owner: maintainer
tags: [maintenance, upstream]
summary: Merge the official main branch into the local fork without discarding its security commits.
related: [work_upstream_sync_20261026]
---

## Scope and authority

User requested checking the official GitHub repository and pulling its latest code. Lead owns a local main-branch merge; preserve the fork's mic authentication, daemon mandatory authentication and Electron isolation fixes. No personal runtime activation, credentials changes, microphone capture, paid provider, deployment or force/reset/rebase. A remote push is outside this pull request's scope. Local pull completion is the delivery condition.

## Tracking and diagnosis

Intended and actual checkout: authorized local pentacle workspace (absolute path in private receipts). Current main/origin main: 9feb8c310ff52fe353202d2f912db5f7a53b1693. Origin https://github.com/Suyogry/pentacle.git; official upstream https://github.com/HJK6/pentacle.git. Read back remotes, branch and clean worktree. Merge base 2bcab76dea486813839d0faf98a6296b7b128a26. Fetched official main 42698e64dcb33e2e6329fc9faf8c6a689226f7cd (2026-10-26); local has 8 unique commits and upstream has 19. Read-only merge-tree succeeds without conflicts. Upstream modifies 47 files: chat summaries/previews, wake idle timeout, Darwin process identity/close behavior, delayed provider identity checks, deployment smoke/gate tests and documentation. Lockfiles and installed dependencies are unchanged.

## Contract and validation

Use a normal merge, preserving both parent histories. Retain every fork security change; inspect the upstream edits to daemon server/session paths and mic state machine and verify the security admission files unchanged except upstream's additive close validation. Preserve the existing daemon auth gate before dispatch and desktop policy/bootstrap/build entry points. No manual conflict-resolution code is expected; any real conflict or regression is repaired within this same task and reviewed.

Run the full Node suite with the already-established 120s per-file budget, shared chat-core tests/typecheck, the changed daemon test files plus mandatory-auth regression tests, mic authentication/wake tests without audio/model initialization, desktop/web builds, and the disposable production Electron/daemon/native-provider/tmux smoke. No personal services. Full fleet/deployment, hardware audio, paid provider and cross-platform certification are not claimed. Validate process metadata/catalogs. Independent plan review precedes merge; final independent review verifies committed merge identity, security preservation and actual evidence. Keep raw logs/configuration identities outside the public source tree, with hashes in _artifacts/validation.md.

## Acceptance

- [x] Official main is an ancestor of the updated local main; fork security history preserved.
- [x] Security admission paths and relevant workflows pass regression checks.
- [x] Local merge committed, independent QA accepted, worktree clean; no personal runtime activation.

## Closure

Local pull complete: merge a79150ed1ffe6405651a3b403a85f43987c481a9 incorporates official main 42698e64dcb33e2e6329fc9faf8c6a689226f7cd and preserves the fork's previous main as its other parent. Candidate a4118a47b42a621bd7f45fa26513902eb5afa9f7 adds only authenticated test fixtures for the fork's mandatory boundary. Independent final QA ACCEPT; receipt and validation in [_artifacts/validation.md](_artifacts/validation.md). Official main ref rechecked unchanged before closure. No personal runtime activated and no remote push performed; the user's requested delivery is the updated local checkout.

## Retro

A clean merge can still expose upstream test assumptions about localhost authentication. Authenticate those fixtures rather than relaxing the daemon. Use the documented Python 3.11+ environment for embedded Python probes; retain the original full-run failure and bind the focused corrected-interpreter proof explicitly.
