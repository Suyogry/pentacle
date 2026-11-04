---
id: work_pentacle__upstream_sync_20261104
title: Integrate official updates while preserving fork workflows
type: work
status: completed
canonical: false
created_at: '2026-11-04'
updated_at: '2026-11-04'
completed_at: '2026-11-04'
source_path: work/completed/pentacle__upstream_sync_20261104/summary.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Merge captured official main into the personal fork, retaining authentication
  hardening and supported desktop sign-in.
related:
- spec_pentacle__upstream_sync_20261104
---

Shipped: official main `318c8f17` merged normally into the personal fork; accepted
source `8df132e1` is pushed to main. Security, corrected provider sign-in and
orchestrator authority are preserved. Authenticated account-pin, screen and
close/restart seams are reconciled. Independent final QA ACCEPT, including
93 focused tests; affected daemon, CLI recovery, JS/core, builds and isolated
native workflows pass within the documented evidence bounds. Existing moderate
build-tool advisory and optional/live/provider limits are recorded in
[_artifacts/validation.md](_artifacts/validation.md).
