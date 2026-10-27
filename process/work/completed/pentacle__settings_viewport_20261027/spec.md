---
id: spec_settings_viewport_20261027
title: Keep Settings and provider sign-in inside the desktop viewport
type: spec
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__settings_viewport_20261027/spec.md
machine: local
owner: maintainer
tags: [desktop, layout]
summary: Bound Settings to the viewport and keep expanded provider sign-in controls reachable.
related: [work_settings_viewport_20261027]
---

## Goal and authority

User reports Settings/provider sign-in content not fitting the laptop screen.
Lead owns a bounded CSS repair, builds and actual Electron geometry/screenshot
checks. Keep all settings/provider behavior and security boundaries unchanged.
No provider login, paid call, credential capture, mic activation, remote push or
application restart that could interrupt a user login. Deliver locally; the
running source app can reload after any active sign-in finishes.

## Tracking and diagnosis

Intended and actual checkout: pentacle workspace, origin
https://github.com/Suyogry/pentacle.git, main, base
c03f51b2e4aa99e6fa696d78c45bb470627ba061. Clean tree before edits. Actual UI
inspection confirms a tall Settings dialog. Disposable production main/preload
and generated renderer reproduces all 12 failing cases at content sizes
1280x800, 1024x600 and 720x480, with both styles and collapsed/expanded sign-in.
The dialog extends outside the viewport; Done and expanded Start sign-in are
unreachable. Parent overlay centers an unconstrained modal, while body hides
overflow. Settings minimum width and footer nowrap add narrow-width pressure.
Raw metrics/screenshots are private under layout-check-20261027; no personal
provider process or account was used by the probe. Native window interactions
are unavailable for the existing user window; screenshot inspection works.

## Contract and validation

Change only Settings sizing/wrapping rules: viewport-relative width and maximum
height, internal vertical scrolling, text/action wrapping as needed. Avoid
application-wide scaling, permission changes or unrelated modal refactors.
Document scrolling briefly in desktop docs. No shared harness change or vendor
update. Independent spec/final QA required by repository process.

Rebuild desktop and web. Rerun actual isolated Electron geometry checks on the
same three sizes, both styles and sign-in expanded/collapsed; modal fits, no
horizontal content overflow, Done and Start sign-in can scroll into view. Inspect
before/after screenshots. Also test long URL/code/status expansion with synthetic
content only, footer pending-reload controls and keyboard focus reachability.
Run focused existing settings/provider UI/transport/security tests. Reuse prior
accepted full daemon/root/native evidence for unchanged dependencies/backend and
IPC. This is a scoped CSS release, not full hardware/provider certification.
Freeze source/docs diff and receipts for independent final QA, validate metadata,
commit locally and leave a clean tree. Existing packaged copy is not activated.

## Acceptance

- [x] Settings fits supported desktop sizes and expanded sign-in stays reachable.
- [x] Focused behavior/security tests and both builds pass; independent QA accepts.
- [x] Documentation/evidence and owned local commit complete; clean tree.

## Checkpoint

Completed local source/build delivery. Independent plan and final QA ACCEPT;
source/docs diff ea882a1a39b8854bfa821e073da58d42b0359e3d0175f17d3b42ce5ecc1ad4c7.
Actual Electron geometry12/12 and expanded-content/native-keyboard6/6 pass;
62 focused tests and both builds pass. Independent QA reproduced geometry12/12
and 21 focused tests. Evidence: [_artifacts/validation.md](_artifacts/validation.md).
Closure includes metadata validation and the owned local commit. No remote push
or personal app reload/package replacement. Reloading during provider sign-in
would cancel it, so the user can restart the source desktop after sign-in ends.

## Retro

Centering a dialog is insufficient when content grows beyond viewport height.
Bound the modal, give its list a shrinkable scroll area, and keep header/footer
outside that area. Verify native keyboard dispatch with the fixture focused and
await focus completion; do not change product code for an invalid test setup.
