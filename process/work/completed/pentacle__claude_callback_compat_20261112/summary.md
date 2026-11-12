---
id: work_claude_callback_compat_20261112
title: Qualify Claude callback sign-in with the real CLI
type: work
status: completed
canonical: false
created_at: '2026-11-12'
updated_at: '2026-11-12'
completed_at: '2026-11-12'
source_path: work/completed/pentacle__claude_callback_compat_20261112/summary.md
machine: local
owner: maintainer
tags: [authentication, compatibility]
summary: Reproduce the reported Claude 2.1.318 browser handoff failure and qualify a bounded repair.
related: [spec_claude_callback_compat_20261112]
---

Shipped to personal main at fcfb3ca5ea3e7d8b5825adeb5b32b0130e27b881 and
activated as a scoped macOS desktop hotfix. Source QA, package-plan/artifact QA,
63 focused regressions, exact real318 compatibility and post-install packaged
checks passed. The running app shows the browser handoff; the user's attempt
remains open. Complete rollback and private deployment receipts retained.

## Retro

Real CLI coverage found the endpoint migration; no-op builds and physical native
permission comparisons kept the installation bounded and recoverable.
