---
id: spec_mic_api_auth
title: Authenticate the microphone API and proxy browser clients
type: spec
status: completed
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
completed_at: '2026-10-26'
source_path: work/completed/pentacle__mic_api_auth/spec.md
machine: local
owner: maintainer
tags: [security, microphone]
summary: Require private credentials and reject browser-origin access to the microphone backend.
related: [work_mic_api_auth]
---

# Authenticate the microphone API and proxy browser clients

## Ownership and goal

The implementation lead owns the Python/Node transport boundary, all shipped callers, tests and docs. An independent reviewer checks the spec before implementation and the final candidate. Deliver source and commit to the user's fork; installing or activating a microphone runtime is outside scope.

## Tracking

- Intended and actual checkout: repository root `pentacle` in the authorized workspace (absolute path retained only in private session evidence).
- Intended and actual authoritative origin: https://github.com/Suyogry/pentacle.git
- Intended and actual branch/base: main / origin/main, 2bcab76dea486813839d0faf98a6296b7b128a26.
- Review candidate: source/tests/docs diff SHA256 `7bb0eae07ddcff43db31aa7d04b3ceae435bf27339e58b16b403ca48c77acad6` against base above; process bookkeeping excluded. Evidence digests recorded in `_artifacts/validation.md`.

## Current behavior and reproduction

MicHandler serves transcripts and recording controls without authentication, accepts arbitrary Host/Origin, and enables wildcard CORS. Isolated original-handler reproduction returned HTTP 200 with synthetic transcript content for Origin https://untrusted.example and reached meeting control without credentials. The renderer contains direct-fetch fallbacks. Backend probes, transcription and speech helpers also lack authentication. The web host currently allows unauthenticated loopback use.

## Target behavior and constraints

1. Every mic HTTP method, including status, raw audio, OPTIONS, HEAD and unknown methods, must pass a centralized check before body reads, sensitive state, imports/model access or dispatch. Require one Authorization Bearer credential on loopback too; reject duplicates, missing/invalid credentials and unexpected Host. All browser Origin headers (including null, duplicate and local origins) are refused; browsers use the web proxy, never the mic backend. Remove CORS permission headers. Validate literal loopback Host with the actual listener port. Keep the backend loopback-only and refuse non-loopback bind before audio/model initialization.
2. Load a random URL-safe token (at least 32 characters) from explicit MIC_AUTH_TOKEN_FILE, private regular file, not a symlink, owned by the current OS user with POSIX 0600 permissions. Fail closed at startup on missing/unsafe credentials; never auto-generate or expose a secret. Rotation is an explicit file replacement + server restart; clients reread the file.
3. Node main-side transport reads mic.tokenPath or MIC_AUTH_TOKEN_FILE, never inline/browser credentials; strips private mic settings from public config. Send the token server-side for allowlisted operations and health probes. Backend URL is literal loopback HTTP, no userinfo/query/fragment/base path. Disable proxy/redirect forwarding for native clients to prevent secret leakage.
4. Browser mic access remains through mic:request over the web host's authenticated token/Tailscale session and exact Origin admission. Enabling microphone features on a web host without web authentication is a startup error. Remove renderer direct-fetch fallbacks and route the legacy meeting view via the existing bridge.
5. Update daemon transcription, speech helper, buffer CLI, recovery probes and shipped diagnostic tools. Authentication failures are configuration failures, never a reason to restart a responding service. Share a small Python stdlib transport helper; no new runtime dependencies.
6. Bound JSON bodies (64 KiB), raw audio (existing 16 MiB cap) and socket read times before untrusted allocation; errors have fixed messages, no tokens. Preserve existing authorized mic behavior and caller error contracts where practical. Explicit migration is required for previously open/remote mic endpoints.

## Validation plan (locked after independent review)

- Capture original RED from synthetic handler reproduction (done).
- Real loopback HTTP tests with hardware/model/process boundaries faked: authorized transcript GET and mode POST reach real handlers; no/malformed/wrong/duplicate auth, hostile/duplicate Host and Origin, OPTIONS/HEAD/unknown verbs, JSON/simple cross-site requests, raw oversized audio, fail-closed startup and bad credential files. Assert rejected calls do not read bodies or touch model/recording boundaries; wildcard CORS is absent.
- Node tests: web bridge carries successful requests, missing/bad web auth or cross-origin upgrade is rejected, backend credential stays server-side, probes carry auth, invalid destination/redirect cannot leak it, no browser fetch fallback.
- Python caller tests: real backend auth on speech/transcription/CLI/probe path, missing token fails closed, redirects rejected, recovery 401/403 never restarts.
- Run full portable mic suite, Node unit/renderer suite and web build; targeted daemon transcription suite. Full daemon certification needs tmux/lsof/zsh and its macOS loopback alias; record unavailable prerequisites explicitly rather than claim certification. No audio devices, model downloads, paid providers, runtime activation or tests against existing personal services.
- Freeze diff/content identity and test evidence for independent final code/tests/docs review before commit/push.

## Acceptance criteria

- [x] Unauthenticated or browser-origin requests cannot disclose mic state or invoke controls, including localhost.
- [x] Correctly authenticated host-side callers preserve recording/transcript/transcription/speech workflows.
- [x] UI never receives backend secrets or calls the backend directly; web auth required with mic enabled.
- [x] Startup, credentials, URL handling, redirects, input sizes and recovery fail safely.
- [x] Migration/setup documentation covers every required credential consumer and local-only transport.
- [x] Independent spec/final review and scoped verification complete, commit pushed to origin/main, clean tree.

## Non-goals

Agent permission policy, Electron isolation, dependency upgrades, device/model provisioning, fleet deployment and live recording/playback.

## Checkpoint and closure

Shipped source: `7986a3b3a9f2e288711398f99f50acc90484ec49` was pushed to
origin/main and verified against the remote ref. Runtime installation and
activation were outside the user's request and were not performed. The source
working tree was clean after shipment; this closure record is a documentation
follow-up. Acceptance is scoped to the tests and limitations in the evidence.

## Retro

- Authentication must cover status/probes and every HTTP method before dispatch, not just recording routes.
- Migrating all native callers and the web host together avoids an anonymous compatibility bypass.
- Recovery must distinguish a refused authenticated service from a dead process.
- Real HTTP plus the actual Node host verified the browser-to-backend boundary without opening devices.
