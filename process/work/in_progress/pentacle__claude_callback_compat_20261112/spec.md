---
id: spec_claude_callback_compat_20261112
title: Qualify Claude callback sign-in with the real CLI
type: spec
status: in_progress
canonical: false
created_at: '2026-11-12'
updated_at: '2026-11-12'
source_path: work/in_progress/pentacle__claude_callback_compat_20261112/spec.md
machine: local
owner: maintainer
tags: [authentication, compatibility]
summary: Reproduce the reported Claude 2.1.318 browser handoff failure and qualify a bounded repair.
related: [work_claude_callback_compat_20261112]
---

## Goal and ownership

The user requests a check of the Pentacle fix, a team report requesting an update
to provider_relogin.js for Claude Code 2.1.318 callback authentication, and a real
compatibility test. Root owns investigation and delivery; an independent worker
inspects the exact provider version. Independent spec and final QA review apply.

## Tracking

Intended and actual checkout: the existing pentacle workspace (private absolute
path retained in tool receipts), origin https://github.com/Suyogry/pentacle.git,
branch main, base main / 9caadf1736c3c03cc8b373a9f8f2edfd8ea6bec7.
The tree was clean before this work. Do not restart or deploy the user's app,
upgrade the installed CLI, change real credentials, or push source without a
concrete delivery reason. Team-report destination is pending user preference.

## Current state and diagnosis

Reported, not yet reproduced: Claude launches, Pentacle remains starting without
awaiting_browser, Claude opens a localhost callback listener, Pentacle times out
after five minutes, and auth status remains logged out. Existing controller
defaults to 300000 ms. All 52 existing focused tests pass; native PTY coverage
replaces the provider executable with a fixture. Installed CLI is 2.1.246 and its
normal profile is authenticated. Preserve that profile.

Exact official npm native 2.1.318 is available for isolated investigation. Binary
inspection confirms distinct callback and manual-code paths. Do not assume the
reported failure is only a printed prefix or relax URL trust without real RED.

## Contract and validation plan

1. Use exact Claude 2.1.318 under real node-pty and the production controller,
   with disposable HOME, CLAUDE_CONFIG_DIR and secure-storage directory plus a
   constructed environment. Never copy user credentials. Record binary hash,
   version, Node version, source identity and sanitized observations.
2. Before changing production behavior, reproduce and classify the first failed
   predicate. If exact production flow works, report that result and identify
   the still-missing deployment/host input; do not invent a production patch.
3. Add an explicit opt-in real compatibility test, outside the default fixture
   suite. Require an absolute CLI path and expected version. Assert actual
   awaiting_browser with a valid URL, an owned localhost callback listener,
   no automatic browser navigation or false success, timeout/cancellation cleanup,
   listener closure, and a still-logged-out disposable profile. A reduced test
   timeout must be labeled as such; only a default-timeout run proves five minutes.
   Do not log authorization URLs, PKCE/state, codes or account identity.
4. Repair only demonstrated defects in the controller/browser guidance. Preserve
   origin/path/query validation, terminal metadata rejection, ownership, target
   cleanup receipts, timeout bounds and separate authentication verification.
   Add focused negative controls that fail on the previous behavior.
5. Run focused controller/UI/transport/security regressions and desktop/web
   builds for changed behavior. Freeze the candidate content and evidence for
   independent final QA, including a cold docs read. Full paid-account sign-in
   requires the user and must not be implied by a logged-out handoff test.

## Acceptance

- [x] Independent spec review locks the scope and validation plan.
- [x] Exact-version real evidence distinguishes reported observations from reproduced results.
- [x] A real opt-in compatibility test detects a broken browser handoff and validates cleanup.
- [x] Any production repair is supported by RED/GREEN evidence and focused regressions.
- [x] Documentation, independent final review and a concrete team report are complete.

## Demonstrated repair and checkpoint

Independent spec review ACCEPT. Exact 2.1.318 reproduces the product failure:
its `https://claude.com/cai/oauth/authorize` URL is rejected by the old origin
and path allowlist while its owned callback listener remains open. The new
real compatibility test fails against unchanged production code at the
awaiting_browser assertion; cleanup succeeds. Two new unit tests also fail RED.

Root is the execution owner for this accepted bounded repair. Implementation
pairs the exact new origin/path while preserving previous endpoints; callback
browser guidance is updated. No new endpoint cross-product, listener or tunnel.
The real CLI compatibility test passes after repair, as do 63 focused tests and
both builds. Timeout coverage is accelerated to four seconds, not a five-minute
endurance run. Account authorization and app activation are not exercised.

Next: freeze source/evidence, independently review final code/tests/docs, and
file the user-authorized issue in Suyogry/pentacle. Local source delivery only;
no restart or credential changes. Evidence index: `_artifacts/validation.md`.

## Delivery and remaining activation

Independent final review ACCEPT on the frozen content and evidence-index hash.
Issue https://github.com/Suyogry/pentacle/issues/1 is OPEN; full body and attached
315-line tested candidate patch were read back and matched the submitted text.
GitHub connector could not create an issue (integration 403). Authenticated
Suyogry CLI fallback found fork Issues disabled; enabled that reversible feature
and filed the authorized report. Active global gh account was not changed.

Local source/test/doc changes remain uncommitted and undeployed for review.
The user request to report and ask the team is fulfilled; runtime activation,
account authorization and any source merge remain with the maintainer. Do not
interpret the local patch or open issue as shipped runtime behavior. Keep this
item active until a maintainer takes implementation disposition/activation.

Source-only process metadata validation passes with five pre-existing stale-work
warnings; system Python 3.9 was unsuitable, and a temporary Python 3.13 environment
with declared requirements performed the successful check. Both builds, 63 focused
checks and the real exact-version test passed; full npm test was not run.

## Authorized deployment — 2026-11-12

User now requests deployment. This supersedes the prior no-activation boundary.
Root owns the scoped local desktop activation. Preserve the installed app's
existing baseline and native dependencies; apply only the accepted callback
repair and browser guidance, with rebuilt renderer from the installed sources.
The app is closed, so no live sign-in or UI session needs interruption. Preserve
real provider credentials and existing daemon/profile configuration.

Private deployment receipts contain installed app identity, complete preimage,
rollback, candidate content comparisons and running process/UI readbacks.
Reuse accepted source evidence only for unchanged source/harness inputs. Review
the bounded packaging/activation plan independently, test real 2.1.318 in an
isolated profile on the packaged runtime, then launch the actual installed app
and inspect Settings without starting login on the authenticated normal profile.
Record deployed content hashes, process path/PID, screenshot and rollback.

## Current checkpoint — deployed locally

Registered macOS desktop hotfix activated and observed in its real window.
Independent release-plan/artifact QA ACCEPT; packaged rehearsal and post-install
real2.1.318 compatibility each pass1/1, zero skips. Original native files and
profile retained, complete rollback copy verified. Live user-started login
reaches awaiting_browser and is left open. Receipt: `_artifacts/deployment.md`.
Next: save/push owned source and deployment record to the personal fork, then
close this item with the source disposition. No further provider interaction.
