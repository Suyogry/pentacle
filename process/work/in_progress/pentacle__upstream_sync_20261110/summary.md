---
id: work_pentacle__upstream_sync_20261110
title: Merge official updates while preserving fork workflows
type: work
status: in_progress
canonical: false
created_at: '2026-11-10'
updated_at: '2026-11-10'
source_path: work/in_progress/pentacle__upstream_sync_20261110/summary.md
machine: local
owner: maintainer
tags: [pentacle, integration]
related: [spec_pentacle__upstream_sync_20261110]
summary: Isolated upstream merge; explicit desktop compatibility retained; plan accepted; resolution in progress.
---

Clean fork main is `31a8ae2c037f158ea4b1f056362c95d0e1cce48f`;
official target `9b91da896f31c7abf8fb06918ce78dca70d0b465`.
Official target advanced to `0b0a64f38967888c58952d9975f3403aeca8581e`.
Lead owns source integration and fork push. Merge retains desktop/security
compatibility and all protected preimages. CLI 8,122 passing, final affected
controls 491 passing, mic 46 passing; desktop/web native-fixture smoke passes.
Root Node's two harness failures pass isolated recheck. Nineteen broad-daemon
failures are each reproduced on untouched upstream or original fork; no claim
of full fleet/runtime certification. Next: independent final source/docs QA,
then accepted main fast-forward and normal personal-fork push. Services,
private configuration and separate PIMR branch remain untouched. Private receipts use bundle
`upstream-sync-20261110`.
