---
id: work_daemon_auth
title: Require credentials for local daemon clients
type: work
status: completed
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
completed_at: '2026-10-26'
source_path: work/completed/pentacle__daemon_auth/summary.md
machine: local
owner: maintainer
tags: [security, daemon]
summary: Remove anonymous localhost authority and migrate trusted clients to existing credentials.
related: [spec_daemon_auth]
---

Shipped `6b68a998bd9cee0cb8939fefdedcee9b97bb327c` to origin/main and verified the remote ref.
Independent spec/final repair QA ACCEPT. Localhost RPCs and subscriptions require
credentials; CLI and worker launch paths migrate together, preserving trusted
operator command authority and rejecting ambient operator fallback for workers.

Validation: daemon combined 615 pass, probes/diagnostics 125 pass, full CLI before
bounded repair 7257 pass (13 skip, one unrelated installer discovery prerequisite
deselected), affected repair selection 6223 pass, new actual-socket suite 19 pass,
Node 2455 tests (3 skip, no failures), web build pass. See validation receipt for
scope and reuse. Full tmux certification unavailable. Private launch credentials
verified offline; no personal runtime activation.

## Retro

Separate authenticated caller identity from relationship metadata, and test
operator success alongside worker no-fallback denial.
