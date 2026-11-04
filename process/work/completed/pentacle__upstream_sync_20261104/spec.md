---
id: spec_pentacle__upstream_sync_20261104
title: Integrate official updates while preserving fork workflows
type: spec
status: completed
canonical: false
created_at: '2026-11-04'
updated_at: '2026-11-04'
completed_at: '2026-11-04'
source_path: work/completed/pentacle__upstream_sync_20261104/spec.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Merge captured official main into the personal fork, retaining authentication
  hardening and supported desktop sign-in.
related:
- work_pentacle__upstream_sync_20261104
---

## Scope and tracking

Source-only integration requested by the user, including the existing standing
push authorization for the personal fork. Lead owns this lane. Actual and
intended checkout pentacle, origin https://github.com/Suyogry/pentacle.git,
branch codex/upstream-sync-20261104, base183838435a949425c94095a0df18590db79a36bb.
Official captured main318c8f17f9471e5ee4b6f5c1c3ac70592a5179cf contributes301commits
and368files. Independent private plan QA ACCEPT before merge; exact local
identity and raw receipts remain outside public source. No personal application,
daemon, provider login/inference, microphone or fleet activation is authorized
by this source update.

## Contract and implementation

Normal merge retains both histories and the fork's mandatory operator/seat
credentials, recovery-only local-admin proof, mic authentication/Host/Origin
checks and proxy, isolated Electron bridge/CSP, Settings scrolling, private
profile discovery, dependency refresh and quota updates. Preserve upstream's
queued-send/draft, outbound voice commit/recovery, attachments, dashboard policy,
authority restoration and account-health updates.

Reconcile six conflicts semantically. Retain the complete corrected fork
provider sign-in flow, which is an existing supported user workflow; upstream
removed its broken version. Restore matching handler, web origin guard, shim,
Settings UI, tests and docs. Reconcile absence-only test/scenario expectations
with explicit fork retention, retaining unknown-method and origin negatives.
Keep upstream changes elsewhere. Preserve fork hello identity isolation in the
new shared operator-envelope helper, including upstream deadline and push fixes.

Account pin recovery is a new compatibility seam: upstream assumes a localhost
hello exemption which this fork removed. Use the existing independent recovery
transport only for pin-status/pin-set with verified daemon-user local-admin
proof on native loopback. Keep the account handler's own authorization and all
ordinary account/spawn/inventory denials. Real socket regression covers the
success path, stale seat independence, wrong proof and no authority expansion.

## Validation

Freeze exact candidate and evidence before independent final QA. Root npm
exact-lock install; core has no tracked lock, so install without generating one
and retain resolved dependency identity. Dedicated Python environment for tests.
Full bounded root Node suite, shared-core tests/typecheck, affected daemon file
manifest plus mandatory-auth/operator/scope/recovery regressions, full agent-orch
suite, relevant gate/selection and mic security checks, desktop/web builds and
npm audits. Local tuple Node24/Python3.14/macOS is recorded separately from
upstream default CI Node22/Python3.13. No default-CI or cross-platform claim.

Run real isolated production Electron/authenticated disposable daemon/synthetic
provider/native PTY/tmux rehearsal and final smoke, with actual configuration
and owned cleanup. Adapt only demonstrated harness interfaces and retain failed
receipts. No paid provider or personal profile used. Classify and recover failed
cells without rerunning accepted unchanged coverage or weakening assertions.

## Acceptance

- [x] Scope, identity, requirements and independent plan review established.
- [x] Captured upstream main is ancestor; supported fork behavior preserved.
- [x] Relevant gates and isolated native workflows pass; final QA accepts.
- [x] Personal main and remote fork updated normally with clean readback.

## Closure — shipped

Independent final QA accepted source candidate
`8df132e1ade2b4995cde4c22011333b82239b39b`. Personal main was fast-forwarded
and pushed normally to origin/main. All acceptance criteria are satisfied.
Validation and bounded recovery details are in `_artifacts/validation.md`;
private receipt names and hashes are indexed in `_artifacts/evidence.json`.
No personal runtime activation was part of this source delivery.

## Retro

Preserving the fork's stronger authentication requires composing new upstream
clients and test fixtures with real proof. Exercise restart/idempotency paths
as well as initial login. Select unit files with the official directory exclusions,
keep original failed evidence, and reuse unchanged passing coverage within its
actual input bounds. Independent review caught credential-loader and ambient-seat
edge cases before promotion.

## Compatibility fixture repairs

The new screen lease operator path loads operator credentials only for an
operator identity. Authenticated seats continue through their own transport;
service and ambiguous identities cannot fall back to operator authority.
Regression tests forbid both operator loaders for every seat lease action.

New upstream daemon tests are adapted to the fork's mandatory-auth contract:
maintenance and log probes prove disposable operator credentials, inventory
fanout fixtures establish verified trust, seat exchange uses one identity per
socket, and fake spawn transports implement private token staging. Anonymous,
forged-context and local-admin-only privilege negatives remain denied. These
are fixture changes, without restoring the removed localhost exemption.

The initial daemon file selection incorrectly included two long soak files.
The interrupted result is retained as failed evidence. The corrected unit
manifest excludes that directory as the official unit gate does. Default
release-selection toolchain prerequisites are installed separately; this does
not qualify an entire default-toolchain or fleet run.

The real close/restart journey exposed an additional client seam: retired seat
credentials cannot establish a general hello before replaying their close.
Seat close uses existing independent per-request authentication; the server's
existing token-hash/closed-target/generation checks remain authoritative.
The native fixture verifies exactly one termination, durable close replay after
restart, and rejection when that retired seat targets another live seat.
