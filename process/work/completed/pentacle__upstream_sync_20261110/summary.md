---
id: work_pentacle__upstream_sync_20261110
title: Merge official updates while preserving fork workflows
type: work
status: completed
canonical: false
created_at: '2026-11-10'
updated_at: '2026-11-10'
completed_at: '2026-11-10'
source_path: work/completed/pentacle__upstream_sync_20261110/summary.md
machine: local
owner: maintainer
tags: [pentacle, integration]
related: [spec_pentacle__upstream_sync_20261110]
summary: Shipped official-source integration to fork main with desktop/auth protections and bounded QA evidence.
---

Shipped accepted source candidate `a86a8524918ee0deedadf38d3ff573270fb61ac7`
to local and personal-fork main, including official history through
`0b0a64f38967888c58952d9975f3403aeca8581e`. Fork desktop/auth/mic protections
remain; separate PIMR ref remains unchanged. Independent final source/security
and repaired cold-doc/profile QA accepted. Desktop/web builds and isolated native
smokes passed; actual personal daemon's authenticated readbacks and PID are
unchanged. Nineteen residual daemon tests reproduce on untouched baselines;
full fleet/runtime certification is not claimed. No personal runtime restart,
provider inference or packaged desktop upgrade. Raw receipts and hashes use
private bundle `upstream-sync-20261110`; see `_artifacts/validation.md`.
