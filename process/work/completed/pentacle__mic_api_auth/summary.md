---
id: work_mic_api_auth
title: Authenticate the microphone API and proxy browser clients
type: work
status: completed
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
completed_at: '2026-10-26'
source_path: work/completed/pentacle__mic_api_auth/summary.md
machine: local
owner: maintainer
tags: [security, microphone]
summary: Require private credentials and reject browser-origin access to the microphone backend.
related: [spec_mic_api_auth]
---

# Microphone API authentication — completed

Shipped source commit `7986a3b3a9f2e288711398f99f50acc90484ec49` to origin/main
and verified the remote ref. Independent review ACCEPT; Node 2455 tests pass,
portable mic 451 pass, one unchanged ffprobe-dependent test excluded for an
unavailable prerequisite. Native callers 50 pass plus 17 subtests. See
`_artifacts/validation.md` for scope and receipt digests. No runtime activation.

## Retro

Protect status and recovery probes along with action routes; proxy UI requests
through the authenticated host and keep the backend credential private.
