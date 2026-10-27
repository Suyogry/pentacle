---
id: work_provider_signin_format_20261027
title: Recognize the installed Claude CLI authorization URL format
type: work
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__provider_signin_format_20261027/summary.md
machine: local
owner: maintainer
tags: [desktop, authentication, compatibility]
summary: Handle Claude CLI prefixed authorization lines without broadening URL trust.
related: [spec_provider_signin_format_20261027]
---

Fixed the installed Claude CLI's prefixed authorization URL format. Pentacle
now advances from Starting sign-in to the waiting state with the complete URL.
Complete-line validation, provider allowlist, hidden-metadata rejection, Codex
behavior, cancellation and separate verification remain unchanged.

Three RED regressions before fix;59 focused tests, both builds and actual isolated
production Electron/native PTY fixture proof pass. Independent final QA accepted
with38 focused tests. Local source/build delivery and safe source-app restart;
no real account completion, package replacement or remote push.

Evidence: [_artifacts/validation.md](_artifacts/validation.md).
