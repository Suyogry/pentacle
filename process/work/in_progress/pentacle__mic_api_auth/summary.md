---
id: work_mic_api_auth
title: Authenticate the microphone API and proxy browser clients
type: work
status: in_progress
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
source_path: work/in_progress/pentacle__mic_api_auth/summary.md
machine: local
owner: maintainer
tags: [security, microphone]
summary: Require private credentials and reject browser-origin access to the microphone backend.
related: [spec_mic_api_auth]
---

# Microphone API authentication

Owner: implementation lead. Current checkpoint: implementation and independent final review accepted; 2455 Node tests and 451 portable mic tests pass, with the existing ffprobe-dependent test explicitly excluded. Next: commit/push reviewed source, then close the work record. Runtime activation is not authorized by this source-change task.
