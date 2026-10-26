---
id: spec_daemon_auth
title: Require credentials for local daemon clients
type: spec
status: completed
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
completed_at: '2026-10-26'
source_path: work/completed/pentacle__daemon_auth/spec.md
machine: local
owner: maintainer
tags: [security, daemon]
summary: Remove anonymous localhost authority and migrate trusted clients to existing credentials.
related: [work_daemon_auth]
---

# Require credentials for local daemon clients

## Goal and ownership

The lead implements and ships to the personal fork. Bounded investigation and independent spec/final QA support the lead. Source changes and private launch configuration are authorized; starting personal services, paid providers, audio devices, or fleet deployment is outside scope.

## Tracking

- Intended and actual checkout: repository root pentacle in the authorized workspace; absolute local path remains private.
- Intended and actual origin: https://github.com/Suyogry/pentacle.git
- Intended and actual branch/base: main / origin/main, 9d1d1f48edcde8cb763a43a4960bf501b697de0a. Read back toplevel, origin, branch and merge-base before editing.
- Candidate: staged source/tests/docs diff SHA256 `5ab7c099594622d0b0be0bb2ab3ced2d35664c641e8ae6af2d8ae010ec89bb33` against the base above. Process bookkeeping excluded. Evidence in `_artifacts/validation.md`; raw receipts outside the public tree.

## Current behavior

Native localhost sockets bypass command admission and inventory/fanout authentication. An anonymous process can invoke commands with the daemon owner's authority. Operator trust is cached after hello without ordinary registry revocation revalidation. CLI connection paths mostly send a legacy token rather than the existing v2 challenge proof. Raw command launches omit automatic seat credentials.

## Required behavior

1. Require verified credentials on every protected RPC, hello snapshot, subscription and private outbound event, including localhost. Keep only ping/hello negotiation, owner-code enrollment, and independently secret-authenticated producer routes pre-connection-auth. The minimal public welcome carries protocol/build metadata and challenge only. No anonymous screen lease status.
2. Keep existing authenticated operator and orchestrator command authority, agent permission policies and explicit seat-operator opt-in. Do not add approval prompts or redefine ordinary seat permissions. Physical loopback remains transport metadata and a restriction on independently authenticated local-admin recovery, never authority itself. Preserve narrow existing local-admin consent/transfer/lifecycle operations and existing narrowly verified retired-seat recovery.
3. Revalidate operator credential revocation for RPC and private egress, failing closed on unavailable registry. Preserve existing seat/scoped/Dot/service credential checks.
4. CLI operator paths use existing v2 welcome challenge proof for persistent, snapshot, normal and one-shot connections. Add explicit private operator token-file configuration (AGENT_ORCH_TOKEN_FILE, with PENTACLE_OPERATOR_TOKEN_FILE as supported launch alias). Worker identities use their own seat credentials without ambient operator fallback. Missing/invalid configured credentials fail closed. Keep fixed service and local-admin per-RPC paths usable without granting general operator status.
5. Auto-stage private credentials for raw command launches as for provider launches and persist their token hash; preserve resume/reconnect/scheduled internal execution. Bootstrap new operator credentials through the existing owner-side CLI, never anonymous grant-token. Document migration of existing workers and operator environments. Migrate shipped operational clients and isolated test harnesses that depend on anonymous admission.
6. Private token loading uses owner-only regular files, no symlinks, bounded reads, descriptor checks and fixed errors; never expose keys on the wire or logs. No new runtime dependencies.

## Validation plan

Capture RED on real isolated loopback WebSockets before fixing. Test anonymous RPC/hello/fanout denial, valid operator full command admission, seat access, source identity spoofing, revoked credentials on an open connection, wrong proof and replay, local-admin restricted recovery, service producers, and preauth negotiation. Test actual CLI operator and worker connections, credential source precedence and failures, reconnect, raw launch credential staging/hash, and internal scheduled paths with synthetic credentials and disposable stores.

Run focused daemon and CLI suites, Node auth/client regressions and web build. Cross-cutting certification requires real tmux plus host-specific test isolation; determine prerequisites and record unavailable cells accurately. Avoid real provider/account/device use. Preserve failures and classify harness versus product. Independent spec review locks validation before implementation; independent final review covers code/tests/docs on a frozen candidate. No live runtime activation is claimed.

## Acceptance

- [x] No anonymous local command or private subscription access.
- [x] Credentialed orchestrator retains full existing authority with automatic worker credentials.
- [x] Revocation and missing/bad credentials fail closed, with no seat-to-operator fallback.
- [x] CLI, web, launch, recovery and operational consumers migrate coherently.
- [x] Relevant checks, independent QA, migration docs and push complete.

## Checkpoint and closure

Shipped source commit `6b68a998bd9cee0cb8939fefdedcee9b97bb327c` to origin/main and read back the
matching remote SHA. The committed source diff matches the independently
accepted digest above. Spec QA ACCEPT; initial final review accepted server,
private loading, scoped egress and docs, and rejected two CLI identity migration
defects. Repaired caller/relationship separation and removed worker maintenance
operator fallback; bounded final repair review ACCEPT with 19 independent
actual-socket checks. The source working tree was clean after shipment. This
closure record is a documentation follow-up. No runtime activation was requested
or performed; personal services remain stopped. Private orchestrator credential
and all three launch environments were verified offline without exposing keys.

## Validation disposition

Scoped source verification passes on macOS arm64/Python 3.14 and Node 24.
Cross-cutting full certification is unavailable: tmux is absent (including the
smoke-tier autouse isolation prerequisite), the macOS multi-bind loopback alias
has not been provisioned, and provider/device/fleet activation is outside scope.
The real socket and shell-envelope checks use disposable stores and synthetic
credentials; they do not prove a real tmux/provider launch. The unrelated CLI
installer's automatic macOS Python 3.13 discovery test lacks that interpreter;
its supported explicit Python override passes a no-install dry run. No missing
prerequisite has been represented as a passed certification gate.

## Retro

- Authenticate transport before dispatch and private fanout; locality is not identity.
- Migrate worker provisioning and operator clients in the same source change.
- Relationship targets must not select the caller's credential. Maintenance paths
  must preserve worker identity rather than use ambient operator material.
- Scope event grouping by stream as well as negotiated subscription settings.
- Disposable WebSockets verify admission and revocation without starting providers;
  they do not replace unavailable real tmux workflow certification.
