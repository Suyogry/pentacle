---
id: work_claude_callback_compat_20261112
title: Qualify Claude callback sign-in with the real CLI
type: work
status: in_progress
canonical: false
created_at: '2026-11-12'
updated_at: '2026-11-12'
source_path: work/in_progress/pentacle__claude_callback_compat_20261112/summary.md
machine: local
owner: maintainer
tags: [authentication, compatibility]
summary: Reproduce the reported Claude 2.1.318 browser handoff failure and qualify a bounded repair.
related: [spec_claude_callback_compat_20261112]
---

Root owns the accepted repair. Exact 2.1.318 RED/GREEN and 63 focused
regressions plus both builds pass. Next: independent final QA and the authorized
Suyogry/pentacle issue. Source changes are local and runtime activation is pending.

Independent final QA ACCEPT. Team report and full tested patch filed and read
back at https://github.com/Suyogry/pentacle/issues/1. Local changes remain
uncommitted/undeployed. Next action: maintainer reviews and activates the fix;
this record does not claim shipped account authentication.
