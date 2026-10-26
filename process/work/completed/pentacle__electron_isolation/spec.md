---
id: spec_electron_isolation
title: Isolate Electron renderers while preserving desktop workflows
type: spec
status: completed
canonical: false
created_at: '2026-10-26'
updated_at: '2026-10-26'
source_path: work/completed/pentacle__electron_isolation/spec.md
machine: local
owner: maintainer
tags: [security, electron]
summary: Sandbox the desktop display and preserve its existing privileged API and agent autonomy.
related: [work_electron_isolation]
---

# Isolate Electron renderers while preserving desktop workflows

## Goal, ownership and authority

The lead implements directly and ships to the personal fork. Bounded investigation and independent spec/final QA support the lead. User authorized the proposed in-place Electron hardening with existing UI workflows and end-to-end agent authority preserved, without new task approval prompts. Build and exercise a separate disposable desktop runtime before replacement. No personal service activation, installation of a running app, provider login, paid model call, microphone capture or fleet rollout. Provisioning existing locked Electron binary and tmux test prerequisites is within reversible verification scope.

## Tracking

- Intended and actual checkout: pentacle repository in the authorized workspace; private absolute path retained in session evidence.
- Intended and actual origin: https://github.com/Suyogry/pentacle.git
- Intended and actual branch/base: main / origin/main, 13e5af951bfe78040e0cc81923e19d25b98a9560. Read back toplevel, remote, branch and merge-base before editing.
- Freeze source/tests/docs candidate content identity and evidence digests for final QA; keep raw local receipts outside the public tree.

## Current behavior and diagnosis

The main window and popout constructors enable Node integration and disable context isolation; the main window explicitly disables sandboxing. Preload imports Node/local modules and assigns window.cc/HOST directly. The app uses CommonJS imports and reads configuration synchronously at module evaluation. Existing web bundling already produces a browser-safe app. Native IPC accepts any sender/frame. Main navigation is blocked, but popout policies and frame/window ownership are inconsistent. Loaded source pages have no CSP. Initial investigation found no working injection exploit.

## Target contract

1. Every production app window uses nodeIntegration=false, contextIsolation=true, sandbox=true, and browser-built local renderer assets. Main-world Node globals/module loading are unavailable. Apply consistent navigation, new-window and webview admission to main, chat popout and asset popout constructors. Retire the insecure source-page load path.
2. Preserve every existing window.cc method/event and synchronous chat-popout context, HOST metadata and initial config timing. Use contextBridge with named operations only, never generic IPC exposure. The sandbox-compatible preload imports only electron; main supplies a narrow, sender-verified bootstrap payload. Clone bridged public configuration in the renderer before settings mutations. Backend credentials stay in main.
3. Every native IPC handle/on, including delegated asset/schedule/notification/terminal/relogin, clipboard, reload, external URLs and bootstrap, requires a registered live app WebContents, its actual main frame, and the exact permitted committed document. Unowned windows, child frames and wrong/navigated documents cannot invoke privileged handlers. Refusals never perform effects. Keep web transport and server-side per-operation authorization unchanged. Bound IPC payload shapes/sizes where the bridge otherwise permits arbitrary unsafe data; preserve existing operation validators and semantics.
4. Built desktop HTML uses CSP forbidding inline/eval/remote scripts and objects/base injection; allow existing local bundles, styles and image/blob/media use needed by current UI. Preserve built-in rendering and safe content escaping. Optional private web-adapters/hosted views already unsupported in file-loaded desktop remain explicitly unsupported; do not silently add privileged network exceptions. Web build retains its current transport and output contract.
5. Reuse the existing browser bundle pipeline; preserve classic global script order, CSS, fonts and icons. Generate desktop main/popout pages and browser-safe bundles under renderer/dist/desktop; include all prerequisites in npm start and every packaging build command. Fix build/fixture consumers of retired paths. Keep renderer-facing APIs stable; no new agent approvals or changes to daemon/provider tool/filesystem authority.

## Validation plan

Capture RED using the real original Electron window or exact isolated copy: injected main-world probe can see Node/require or unsafe actual preferences. Then exercise the generated production main/preload/renderer in real Electron using a disposable configuration and synthetic credentials, plus existing isolated daemon/provider/tmux adapters. Positive checks: first screen and public config; mutable settings; authenticated spawn, terminal attach, send, actual synthetic assistant output; reconnect/disconnected rejection; assets/popout/dock/reload; clipboard transport; schedule/notification/mic bridge method parity. No audio or model initialization. Restore any owned temporary clipboard changes; no deliberate focus/input capture against personal apps.

Negative controls: main-world require/process/Buffer absent, bridge exposes no generic IPC; inline/eval script blocked by CSP; unregistered window loading same URL denied; wrong document and child frame IPC denied before effects; disallowed navigation/window/webview refused; no backend secret in renderer config. Use real-frame probes where possible, unit control of actual guard inputs for otherwise inaccessible Electron frame APIs. Keep accepted evidence bounded and label representative transport tests versus actual hardware/provider workflows.

Run full Node unit/renderer suite, desktop and web builds, relevant packaging command checks, existing terminal logic regressions, and a real production desktop smoke with deterministic provider plus real tmux. Capture an observed UI screenshot. Existing full daemon auth evidence can be reused if daemon code/dependencies are unchanged. Full cross-platform or physical mic/provider certification is outside this Mac source shipment; report exact unavailable cells rather than infer success. Independent spec review precedes production edits; independent final code/tests/docs review uses frozen candidate. Do not replace a personal installation until these gates pass.

## Acceptance

- [x] All production desktop window types use isolated sandboxed browser renderers.
- [x] Existing desktop bridge methods/config/startup and core task workflows remain usable.
- [x] Untrusted IPC senders/frames/documents and injected script paths fail closed.
- [x] Agent authority and approval policy remain unchanged.
- [x] Tests, real desktop smoke, screenshot, build/docs, independent QA and push complete.

## Closure

Shipped source commit `d4068baba0613f259193b64e853174375ef2bee9` to the personal fork's main; remote ref readback matches. All acceptance criteria are satisfied within the explicit macOS source-shipment scope. Personal services remain stopped and the built package is uninstalled. See [_artifacts/validation.md](_artifacts/validation.md) for the accepted evidence and platform/hardware bounds.

Retrospective: Reusing the browser build preserved the UI while removing renderer Node access. Testing the actual sandboxed artifact exposed immutable-bridge config and harness assumptions that source-only checks miss. Keep test prerequisites complete and use a realistic per-file deadline for the existing Git integration suite.
