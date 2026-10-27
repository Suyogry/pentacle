---
id: spec_pentacle__provider_usage_setup_20261027
title: Restore provider quota updates across desktop launches
type: spec
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__provider_usage_setup_20261027/spec.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Discover the private user profile and document external quota collection
  for packaged desktop launches.
related:
- work_pentacle__provider_usage_setup_20261027
---

## Goal and diagnosis

Restore actual Claude/Codex quota readings across ordinary packaged-app launches.
The desktop shows dashes when no external usage state exists. Packaged apps also
fall back to the example's disabled subscription when launched without the
private-profile environment. Read-only real-provider probes succeed independently.
Raw paths, readings, configuration and runtime receipts stay private.

## Ownership and tracking

Lead maintainer implements one laptop lane. Intended/actual checkout pentacle,
origin https://github.com/Suyogry/pentacle.git, branch main, base
66d511e067e874c76da6d76726810beff5aa862e. Exact local toplevel readback and
accepted private plan/spec-QA are retained outside the distribution. Final
content identity and evidence digest freeze before independent final QA.

## Contract and plan

Explicit PENTACLE_CONFIG remains authoritative. Existing app-local overlays
retain priority. Otherwise load ~/.config/pentacle/pentacle.config.js before
bundled defaults, including ordinary Finder launches. Existing broken profiles
fail visibly. No private config is bundled. Document external collector setup
with daemon-adjacent state, executable pins and already-trusted workspace.
Enable private usage subscription and a private scheduled collector, retain
preimages/rollback, stage a package, then safely replace/reopen the idle app.
No daemon restart, inference, credential change, workspace trust acceptance,
microphone startup or unrelated session mutation.

## Validation

Independent spec QA ACCEPT before implementation. Regression RED then GREEN
covers precedence, environment-free user-profile loading, explicit missing and
broken user failures with isolated homedir. Focused config/security tests,
existing usage probe/collector tests and full root gate on final source.
Scoped package activation on unchanged Electron/native dependencies reuses
baseline native/security proof for unchanged surfaces. Verify actual packaged
loader, installed scheduler command/env/state, fresh successful observations,
authenticated daemon delivery and actual UI. Preserve existing idle chats,
profile, credentials and owned-resource cleanup. Independent final QA includes
source, tests, docs and private activation receipts; no live inference claimed.

## Acceptance

- [x] Scope, constraints and acceptance recorded; independent spec QA accepted.
- [x] Source/tests/docs implement persistent config discovery and setup.
- [x] Required checks pass and independent final QA accepts the frozen candidate.
- [x] Installed scheduler and actual app display both providers with chats preserved.
- [x] Owned source pushed normally to fork main; clean tree and closure recorded.

## Closure

Shipped scoped source/package/private deployment. Reviewed implementation and
installed bundle ac47ce1225cb6186778db8d4f3df671425c864e6 load the private user
profile without a launch environment. The installed collector writes to the
actual daemon-adjacent path every600s. Actual UI shows both providers' measured
quota with both existing idle conversations/history restored. Daemon and
accounts preserved; rollback package/config retained privately. Independent
final QA ACCEPT. Normal fork push and clean readback complete closure.

Root203-file gate covered with scoped recovery: original run had an unsupported
system-Python fixture failure and one process-inspection cleanup timeout. Both
unchanged files passed with the correct interpreter/clean cleanup proof; no
original failure was relabeled green. Focused29 and Python usage108 passed.
A later scheduled provider RPC error retained last-good values; same-binary
diagnostic and actual installed-schedule confirmation succeeded. No permanent
provider availability or live inference qualification is claimed.
Evidence: [_artifacts/validation.md](_artifacts/validation.md).

## Retro

Provider authentication does not provision quota collection. Bind its state
path to the real daemon database and test ordinary packaged launches without
shell environment. Collector exit0 alone is insufficient: inspect both provider
health outcomes, then verify the actual displayed values. Preserve successful
checks while recovering only demonstrated environment/cleanup failures.
