---
id: spec_pentacle__limits_runtime_20261105
title: Restore live Claude and Codex Limits delivery
type: spec
status: completed
canonical: false
created_at: '2026-11-05'
updated_at: '2026-11-05'
completed_at: '2026-11-05'
source_path: work/completed/pentacle__limits_runtime_20261105/spec.md
machine: local
owner: maintainer
tags:
- pentacle
summary: Restore authenticated daemon delivery of healthy collected provider quotas to the installed desktop.
related:
- work_pentacle__limits_runtime_20261105
---

## Scope and diagnosis

Lead owns one laptop runtime repair requested by the user. Intended and actual
repository pentacle, origin https://github.com/Suyogry/pentacle.git, main base
`07ba5e6b4d020e29acec8358fb655ecd29b84d6c`. The actual installed app shows
provider dashes. The collector has fresh healthy Claude/Codex observations,
the private profile enables usage, and the matching loopback daemon is stopped.
The prepared daemon service was never loaded; only the quota collector starts
at login. Independent private plan QA ACCEPT before activation. Real paths,
readings, account data, preimages and raw receipts remain private.

## Contract and implementation plan

Enable the existing authenticated loopback daemon at login with keep-alive,
using the prepared private wrapper, unchanged environment, existing credential
registry and same runtime database/state paths. Preserve source-mode identity:
the wrapper runs the reviewed checkout, not an immutable packaged daemon.
No product patch is indicated by the diagnosis. No credentials, authority,
provider login/trust, microphone or web services are changed. No inference is
needed. Current app should reconnect without replacement or restart.

Before activation verify installed interpreter/imports, native dependencies,
existing desktop proof, no competing listener and optional assistant auto-restore
disabled. Take consistent SQLite backups and service/config/app preimages.
Copy the prepared private plist to user LaunchAgents with RunAtLoad/KeepAlive
and bounded throttle. Preserve the disabled preparation template. Rollback
unloads only the owned label and restores/removes only the new service file;
do not overwrite newer database writes as a routine rollback.

## Validation

Verify actual daemon PID, executable, source and loopback-only port; anonymous
protected reads fail. Authenticate using the existing desktop credential and
compare snapshot limits with fresh collector state and actual installed app UI.
Zero must display as zero, with matching resets. Preserve conversation history
and the collector schedule. Record continued service/PID health and enabled
login/keep-alive configuration. Independent final QA checks frozen config hashes,
source-mode and installed-app identity, private wire/UI readbacks and limits.
No broad source gate is needed when production source is unchanged. If an actual
pipeline defect appears, reproduce it before expanding the bounded repair.

## Acceptance

- [x] Diagnosis, scope and independent plan review established.
- [x] Credential/startup preflight and consistent data backups retained.
- [x] Authenticated live limits match fresh state and actual app display.
- [x] Durable service and independent final acceptance verified.
- [x] Owned metadata committed/pushed with clean source readback.

## Closure — shipped

Activated the existing authenticated daemon as a persistent user login service.
Independent operational QA ACCEPT verifies consistent healthy readings across
collector state, authenticated wire and actual installed Limits UI, including
zero and a later changed value. Existing conversation identities/history and
all production source, launcher, environment, credentials and desktop artifact
remain preserved. The collector retains its ten-minute interval. No provider
inference/login, mic/web startup or desktop restart/replacement occurred.
Validation and receipt hashes are in `_artifacts/validation.md` and
`_artifacts/evidence.json`. This repository closure changes process metadata only.

## Retro

Signing into providers and collecting usage are separate from delivering it to
the UI. Verify the daemon connection and real installed app before changing
parsers or guessing quotas. Bind freshness to the configured interval and treat
screen-observer failure separately from product state. Consistent backups,
existing credential proof and private operational preimages keep a service-only
repair reviewable without changing application code.
