---
id: work_pentacle__upstream_sync_20261105
title: Integrate official Cursor and Codex updates
type: work
status: completed
canonical: false
created_at: '2026-11-05'
updated_at: '2026-11-05'
completed_at: '2026-11-05'
source_path: work/completed/pentacle__upstream_sync_20261105/summary.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Merge official updates while preserving fork security and existing provider workflows.
related:
- spec_pentacle__upstream_sync_20261105
---

Shipped five official updates through `e2ab95f5` into personal main; accepted
source `56d0eb78` pushed normally. Optional local Cursor support and the Codex
worker-discovery correction are included; review also fixed Cursor tool-output
receipt forgery. Protected security/sign-in files and dependency records remain
unchanged. Independent final QA ACCEPT; builds, Node/CLI, bounded daemon recovery
and isolated desktop checks passed within the documented provenance bounds.
Details: [_artifacts/validation.md](_artifacts/validation.md).
