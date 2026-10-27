---
id: spec_provider_signin_format_20261027
title: Recognize the installed Claude CLI authorization URL format
type: spec
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__provider_signin_format_20261027/spec.md
machine: local
owner: maintainer
tags: [desktop, authentication, compatibility]
summary: Handle Claude CLI prefixed authorization lines without broadening URL trust.
related: [work_provider_signin_format_20261027]
---

## Goal and authority

User reports Start sign-in stays at Starting sign-in. Lead owns bounded parser
compatibility repair, regression tests and disposable actual desktop/PTY proof.
No real provider login or credential capture is required by validation; the
user completes account authentication after restart. The existing stuck attempt
was cancelled through its own UI; UI reported clean cancellation. Do not start
another real login or alter auth stores. Local source/build delivery, no push.

## Tracking and diagnosis

Intended and actual checkout: pentacle workspace, main, origin
https://github.com/Suyogry/pentacle.git, base a4fa51dab27378a2e99bac6372b9b8c03b973c2b. Clean tree before edits.
Actual user UI showed Starting sign-in; its owned Claude2.1.246 child was running.
Read-only installed binary inspection confirms output:
If the browser didn't open, visit: <OSC8 hyperlink whose visible label is URL>.
Plain-line authorizationUrl accepts a standalone fixture URL but rejects the
same URL with this exact prefix. Existing terminalText discards OSC metadata and
preserves visible text. Independent issue on official Claude repository75099
corroborates hyperlink formatting; no actual authorization URL was captured.

## Contract and scoped validation

Accept this exact Claude-only complete-line prefix in addition to current bare
URL output. Preserve allowlisted HTTPS origin/path, no userinfo/fragment, required
state/client_id/code_challenge, newline completeness and all OSC metadata rejection.
Keep Codex behavior unchanged and authorization links/code unlogged. No generic
URL scraping, automatic browser open, timeout relaxation or fake sign-in success.

Independent spec review before production change. Add failing controller tests
for realistic prefixed OSC8 output split across chunks, with complete query only
after newline. Add rejection controls for wrong domain/path/scheme/query, arbitrary
prefix and title/incomplete OSC metadata. Bare URL, both providers, cancellation,
verification, origin/ownership and URL/code privacy tests must still pass. Run
focused relogin/controller/UI/transport/security suites, desktop/web builds.
Disposable production Electron main/preload uses only a replaced provider fixture
under real native PTY to show Waiting for you to complete sign-in and its complete
fixture URL. No real auth store or provider invocation. Inspect screenshot and
prove cleanup. Prior unchanged layout/dependency/backend evidence is reused;
this is scoped compatibility validation, not live paid-provider certification.
Freeze diff/evidence for independent final QA; document supported output format,
validate metadata and commit locally. User restart loads main-process changes.

## Acceptance

- [x] Prefixed installed-Claude format produces awaiting_browser with complete URL.
- [x] Negative URL/metadata controls, provider workflows and security gates pass.
- [x] Real isolated desktop/PTY proof, independent QA, builds and local commit complete.

## Checkpoint

Completed local source/build delivery; independent plan/final QA ACCEPT.
Frozen source/tests/docs diff68671295d8d558e7fd0e45b973578c37f9150214580a96a7443362a0f841c15f.
59/59 focused tests, both builds and actual isolated production desktop/native
PTY sign-in/verification/cancellation proof pass. Independent QA38/38 tests.
Evidence: [_artifacts/validation.md](_artifacts/validation.md).
Closure includes metadata validation and owned local commit. Source desktop
restart follows a readback confirming the original attempt remains cancelled;
activation/readback and preimage remain private. Browser/account steps belong
to the user. No remote push, package replacement or paid provider call.

## Retro

Synthetic output must represent the installed CLI's full visible line, not just
its URL. Strip terminal metadata first, then accept only the exact known prefix
and retain the same URL validator. Actual native PTY and renderer proof catches
handoff bugs that a bare URL helper test misses.
