---
id: spec_pentacle__upstream_sync_20261105_2
title: Integrate coordinated helper deployment and launcher verification updates
type: spec
status: in_progress
canonical: false
created_at: '2026-11-05'
updated_at: '2026-11-05'
source_path: work/in_progress/pentacle__upstream_sync_20261105_2/spec.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Merge three official updates while preserving fork security and the running local services.
related:
- work_pentacle__upstream_sync_20261105_2
---

## Scope and tracking

Lead owns requested source update and standing personal-fork push. Intended and
actual repository pentacle, origin https://github.com/Suyogry/pentacle.git,
base `ac9cec6894228265589c0969cb31e2fadc7e41ea`, branch
`codex/upstream-sync-20261105-2`. Official https://github.com/HJK6/pentacle.git
main `e4d744ccc59f07f161acc7716977903abde23bf0` adds three commits and 24 files.
Clean base/refs and conflict-free merge preview verified. Independent private
plan QA ACCEPT before normal isolated merge. Local identities and receipts stay
outside public source.

## Contract

Preserve both histories and all fork authentication, mic Host/Origin/proxy,
desktop isolation/sign-in/configuration, Cursor receipt framing and provider
workflows. Eighteen protected preimage files remain unchanged. No dependency or
lockfile changes. Incoming work coordinates immutable account helpers with
explicit daemon deployments and verifies native launchers by resolved target
and hash. Importing source does not authorize a deployment or helper activation.

No PIMR implementation, provider login/inference, credential/policy changes,
service restart or package replacement is part of this task. The personal daemon
is already running in source mode from an earlier startup revision. Promotion
updates checkout files; it is not a coordinated runtime release. Preserve the
running PID/listener/authenticated usage delivery and state explicitly that new
backend code is not qualified as activated. No branch switching in the live
checkout until the isolated candidate is accepted for fast-forward promotion.

## Validation

Dedicated private worktree, exact-lock root npm install and Python 3.14 testenv.
Freeze explicit manifests covering every changed daemon/CLI test, coordinated
helper transaction and resource guards, native launcher variants, capability
manifest, related account pin/launch/maintenance/recovery, deployment selection
and fork authentication. Tests use synthetic temp resources and mock transports;
real deploy logic may run only inside the tests' disposable test-label/port-zero
bindings. No production or fleet installer/deployer/provider invocation.

Focused Node security/config/sign-in/limits checks, desktop/web builds, and one
scoped isolated Electron/authenticated disposable daemon/synthetic provider/native
PTY smoke with owned cleanup. Reuse recent full Node/CLI/core evidence only for
unchanged inputs; no full fleet/runtime/default-CI certification. Capture audits
without automatic fixes. Preserve failed evidence and recover only relevant cells.
Independent final source/tests/docs review receives a frozen candidate and gate
hashes before normal main fast-forward/push. Refetch refs, preserve live service
readbacks, rebuild ignored assets for next launch, close metadata, validate and
push. Remove only the owned worktree and leave personal main clean.

## Acceptance

- [x] Scope, identity and independent plan review established.
- [ ] Official source integrated and fork contracts preserved.
- [ ] Scoped gates and independent final QA accepted.
- [ ] Personal fork pushed normally with clean and live-service readbacks.

## Checkpoint

Conflict-free isolated merge prepared; protected preimages unchanged. Next:
scoped account/deployment/auth checks, isolated desktop proof and final review.
