---
id: work_daemon_auth
title: Require credentials for local daemon clients
type: work
status: in_progress
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
source_path: work/in_progress/pentacle__daemon_auth/summary.md
machine: local
owner: maintainer
tags: [security, daemon]
summary: Remove anonymous localhost authority and migrate trusted clients to existing credentials.
related: [spec_daemon_auth]
---

Mandatory daemon authentication and caller migration implemented. Spec review
accepted; first final review found two CLI identity defects, now repaired with
real-socket regressions. Bounded repair QA ACCEPT on the frozen candidate in
spec.md. Relevant source checks pass; full tmux certification unavailable. No
personal runtime activation. Next: commit and push.
