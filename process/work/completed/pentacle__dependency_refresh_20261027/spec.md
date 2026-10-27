---
id: spec_dependency_refresh_20261027
title: Update vulnerable desktop runtime and tooling without workflow regressions
type: spec
status: completed
canonical: false
created_at: '2026-10-27'
updated_at: '2026-10-27'
completed_at: '2026-10-27'
source_path: work/completed/pentacle__dependency_refresh_20261027/spec.md
machine: local
owner: maintainer
tags: [security, dependencies, electron]
summary: Patch Electron and vulnerable tooling, rebuild and exercise existing desktop and agent workflows.
related: [work_dependency_refresh_20261027]
---

## Goal and authority

User authorized dependency remediation, rebuild and desktop/security checks while preserving workflows. Lead implements directly; independent plan and final QA required. Preserve all application APIs, daemon auth, Electron isolation and existing agent task authority/approval behavior. No personal service activation, provider login, paid model call, physical microphone/clipboard capture or fleet deployment. Build and exercise a disposable local runtime; source and rebuilt local artifacts are delivery. Keep credentials and raw receipts outside the public repository. Commit owned changes locally; no remote push unless separately authorized (the preceding upstream pull was local-only).

## Tracking and diagnosis

Intended and actual checkout: authorized pentacle workspace; absolute path in private receipt. Main base 2afe201699d0119ac0d491559c8452a79a45592c. Origin https://github.com/Suyogry/pentacle.git; upstream https://github.com/HJK6/pentacle.git. Read back branch, toplevel, remotes, clean tree before edits. Original full npm audit RED: five packages, four high/one moderate; omit-dev audit 0. Electron is a devDependency but is the actual desktop runtime, locked 44.3.0. Official certificate advisory GHSA-jr5w-w6x2-84p9 requires 44.9.1+ on 44.x. Other vulnerable dev/tooling chains: brace-expansion 1/2/5, undici 6/7, http-cache-semantics 4.2.0, fast-uri 3.1.7. Raw RED receipts retained privately.

Isolated resolution (not production edits) with same-major Electron floor and npm audit fix --package-lock-only --ignore-scripts resolves Electron 44.9.3, brace-expansion 1.1.21/2.1.7/5.0.12, undici 6.29.1/7.30.1, http-cache-semantics 4.3.0, fast-uri 3.1.9; full audit 0. Only 11 package version nodes change; production-library versions unchanged. No forced/major upgrade or overrides expected. Inspect final diff rather than assume the trial remains identical.

## Contract

Raise Electron's manifest floor to the tested patched 44.9.3 and refresh only the vulnerable lockfile nodes through compatible resolution. Do not alter application code merely to satisfy an invalid harness. Install the exact lockfile, review changed install hooks, provision the actual Electron 44.9.3 binary and rebuild native addons for that runtime. Preserve required native executable permissions. All full and omit-dev npm audits must report 0 advisories without suppressions. Keep the packaged runtime version bound to the lockfile and actual executable. A successful audit is not a claim that every application or Python flaw is absent.

Keep web build/start, desktop start/package, native terminal attach/write, authentication and task flows working. Document refreshed runtime/tooling and reproducible checks. If an actual compatibility failure occurs, repair only its diagnosed surface and review the bounded repair, retaining valid evidence for unchanged inputs.

## Validation

Before production edits: independent plan review; retain actual baseline audit/lock/toolchain identity. After installation: full and production-only audit; clean dependency-tree check; compare production library versions unchanged; actual new Electron version readback. Where useful, reproduce a relevant library flaw with a bounded synthetic case and verify the patched dependency, without broad benchmark/implementation-mirroring tests.

Run full Node/renderer/terminal-logic suite with 120s file budget and explicit PENTACLE_PYTHON pointing at Python 3.14 venv; shared chat-core tests and typecheck; desktop and web builds. Rehearse production Electron main/preload/generated renderer against an isolated actual daemon, synthetic provider and real tmux/native PTY: spawn/send/rendered reply, terminal data, settings, asset popout/reload/dock, retained chat manager context, reconnect/main reload/disconnected rejection; Node globals absent, CSP blocks inline/eval, unregistered same-URL/wrong-document/child-frame IPC denied. Preserve screenshot and cleanup proof; no physical mic or user clipboard. Build macOS package and read back actual packaged version/main/preload/browser assets; run one final disposable confirmation with final dependencies and built artifacts. No signed distribution/personal installation or Windows/Linux/hardware/provider certification claimed.

Dependencies changing are desktop runtime/tooling; retain accepted Python daemon/mic unit evidence from the preceding upstream integration because their code/interpreter/dependencies are unchanged. The actual authenticated daemon adapter is exercised again by desktop smoke. If transitive non-development runtime nodes change, reassess certification rather than reuse an unrelated baseline. Freeze source/tests/docs content and final evidence hashes for independent final code/build/docs QA. Catalog/metadata validation at closure. Keep the work active until all in-scope outcomes are satisfied; document actual limitations explicitly.

## Acceptance

- [x] Patched Electron actually installed and packaged; full/production audits clear without suppressions.
- [x] Existing agent/desktop/security workflows pass under the new runtime; authority and approval behavior unchanged.
- [x] Full scoped automated gates, real adapter rehearsal/final proof and independent QA accepted.
- [x] Owned source committed locally, package rebuilt, metadata validated and worktree clean; no personal activation.

## Checkpoint

Completed local source/package delivery within the accepted authority. Electron
44.9.3 is installed and present in the rebuilt macOS arm64 package. Both npm
audits report zero advisories. Independent final QA ACCEPT binds the frozen
source/docs diff 42a06834f4e1017721476db905d3159624b3c53f27fe991ad2cdc05e5643e680.
Automated checks, actual desktop rehearsal/final confirmation, package readback
and cleanup are recorded in [_artifacts/validation.md](_artifacts/validation.md).
The full Node runner's one process-inspection timeout is retained as a harness
failure; its missing file passed a bounded rerun. No product failure remains.
Closure includes metadata validation and an owned local commit. No remote push
or personal runtime activation is part of this delivery; an existing separate
installed app must be replaced to acquire the new runtime.

## Retro

Verify the executable and native addons, not just the npm manifest: Electron is
both a development dependency and the actual desktop runtime. Preserve original
harness failures and recover only their missing coverage without weakening the
runner. Check advisory semantics against the actual consumer; a clean audit does
not establish that a disputed cache behavior changed.
