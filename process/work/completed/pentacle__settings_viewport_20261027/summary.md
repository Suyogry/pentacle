---
id: work_settings_viewport_20261027
title: Keep Settings and provider sign-in inside the desktop viewport
type: work
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__settings_viewport_20261027/summary.md
machine: local
owner: maintainer
tags: [desktop, layout]
summary: Bound Settings to the viewport and keep expanded provider sign-in controls reachable.
related: [spec_settings_viewport_20261027]
---

Fixed Settings/provider sign-in clipping through bounded modal dimensions,
a scrolling list and wrapping footer. Heading/Done remain visible; sign-in
checkbox no longer inherits full-width text-field sizing. Behavior/auth unchanged.

Actual Electron:12/12 original geometry cases plus6/6 expanded URL/code/status,
pending footer and keyboard cases pass. Both builds and62 focused tests pass.
Independent final QA accepted after12 geometry and21 focused checks.

Completed local source/build delivery; no push or personal app reload/package
replacement. Restart the source desktop after any active sign-in ends to load
the rebuilt UI. Evidence: [_artifacts/validation.md](_artifacts/validation.md).
