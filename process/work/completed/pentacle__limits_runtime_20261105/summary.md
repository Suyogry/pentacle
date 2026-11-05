---
id: work_pentacle__limits_runtime_20261105
title: Restore live Claude and Codex Limits delivery
type: work
status: completed
canonical: false
created_at: '2026-11-05'
updated_at: '2026-11-05'
completed_at: '2026-11-05'
source_path: work/completed/pentacle__limits_runtime_20261105/summary.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Restore authenticated daemon delivery of healthy collected provider quotas to the installed desktop.
related:
- spec_pentacle__limits_runtime_20261105
---

Shipped private operational fix: the existing authenticated daemon now runs at
login with keep-alive, restoring collected Claude/Codex quotas to the installed
Limits section. Fresh readings and live refresh agree across state, wire and
actual UI; zero is retained correctly and both conversation histories remain.
Independent final operational QA ACCEPT. No production code, credential or
provider-account change, and no desktop restart. Details are in
[_artifacts/validation.md](_artifacts/validation.md).
