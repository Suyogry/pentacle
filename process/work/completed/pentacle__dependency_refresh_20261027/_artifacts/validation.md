# Dependency refresh validation — 2026-10-27

Scope: local macOS arm64 source, installed development dependencies and unsigned
rebuilt package. Base: `2afe201699d0119ac0d491559c8452a79a45592c`.
Source/docs diff SHA256 (excluding process metadata):
`42a06834f4e1017721476db905d3159624b3c53f27fe991ad2cdc05e5643e680`.
Independent plan review and final implementation/docs/runtime review: ACCEPT.

## Changes and results

- Electron floor/lock: 44.9.3, same major; actual development and packaged binary
  readback: Electron 44.9.3 / Node 24.22.0 / ABI 149 / arm64. Host Node 24.17.0 /
  ABI 137; supported Python 3.14.6 selected explicitly for daemon test probes.
- Exactly 11 package version nodes changed, all development-tagged: Electron;
  six brace-expansion nodes (1.1.21, 2.1.7, 5.0.12); undici 6.29.1 and 7.30.1;
  http-cache-semantics 4.3.0; fast-uri 3.1.9. No non-root non-dev dependency
  records changed, forced major updates, overrides or audit suppressions.
- Exact-lock `npm ci`, dependency tree check, full and omit-dev audits passed;
  both audits report zero advisories. Reviewed changed installation surface.
- Shared chat core: 396 passes and typecheck passed. Web/desktop builds and final
  `npm run build:mac` passed. Native PTY marker probes passed under both host Node
  and actual Electron. Independent focused security/IPC tests: 35 passes.
- Original full root runner exited 1: 199 files passed; one file's bundler exited
  0 but its process-inspection cleanup check took 253ms against a 250ms budget,
  before its test body ran. No assertion failed. The original process group was
  independently verified absent. The sole missing file,
  `test/assistant_chat_declutter.test.ts`, passed all four assertions and normal
  build/body/cleanup on a focused rerun with unchanged source/harness/toolchain.
  Original failure retained. Combined accepted coverage: all 200 files,
  2,464 passes, one Windows-only skip, zero unresolved failures. This is not a
  claim that the original full command exited successfully.
- Disposable rehearsal and final production Electron confirmation used the real
  main/preload/browser assets, authenticated daemon, synthetic provider, native
  PTY and tmux. Spawn/send/rendered response, terminal bytes, settings, asset
  popout/reload/dock, chat context/dock, reconnect/reload and disconnected rejection
  passed. Notification/schedule transport and explicit mic-unavailable path passed.
  Chat popout IPC remains unimplemented baseline behavior.
- Security negative controls: no renderer Node globals or generic IPC; CSP blocks
  inline/eval/Function; navigation/new windows denied; unowned same-URL,
  wrong-document and child-frame IPC rejected, registered main frame accepted.
  Cleanup verified Electron/daemon exited, owned tmux and credentials absent,
  no cleanup errors. Final screenshot inspected.
- Final package readback matched nine actual runtime/docs/browser files to source
  and built assets, main `main.js`, and executable version/hash. Package location
  relative to checkout: `dist/mac-arm64/Pentacle.app`. Embedded build SHA is the
  pre-commit base; exact file hashes and runtime readback bind the actual candidate.

## Evidence and limits

Raw receipts are outside the public repository in the maintainer's private
`dependency-refresh-20261027` receipt directory. All 46 receipt hashes were
rechecked before closure. Ledger SHA256:
`79a2793a4fd1854cee3a82f400849fc0d423a73bce15cff0e82c379cbb890da2`.
Key SHA256 receipts:

| Receipt | SHA256 |
| --- | --- |
| audit-full.json and audit-production.json | ea1aaf2c0b13798f93930b272683a759da8288ed74f14eb7c3b9b711be9c54e7 |
| qa-final.md | 8ae8d44c3b4fad224c8d1940fd080cc5b837396eb12887d70a112cd7043e606a |
| package-readback.json | 28ba314af7453e978607c760c9de715bf7d22e6bb5ab9d921daacb67bb4fa65f |
| node-aggregate.json | 5b46c11baec81e3f19875f15f211773b7dcebd0b75be7c2e0cc6fee2dc1ff1de |
| node.log (original exit 1) | 60b397e28229b10b1b61aba49deb28f7287b1291a0e846cf38372e511c8d77d4 |
| node-repair.log | 28ebdbd53083677df9d496ed84c9c0cfc8588830c68e7ec1b962b08b9b8658e5 |
| desktop-final-proof.json | 365d69ae96b3cc7780629d76c5268c7afcfcd97890d0a5f8eeb206f253615b00 |
| desktop-final-cleanup.json | deeaa168ba03945b3b96e4e3d98750f7fd079a8a7c6572dc0b61bfc455a7e733 |
| desktop-final-desktop.png | 8b9100f68025e2185f836b54ac013e2cd593760cf30babcd0dc01aba79ad969a |
| build-mac-final.log | 00df64648a7568615fe79ec4c44fe549af255054a5a52856672d17ce1ceb04f7 |

The cache advisory is disputed by its maintainer; 4.3.0 leaves the audit range,
not proof of changed semantics. Private responses are non-storable and the actual
cacheable-request consumer checks storable before writing. An initial invalid
brace probe was retained separately; corrected old/patched controls establish the
bounded stack-overflow difference. No application code was changed for a harness
or oracle failure.

Unchanged Python daemon/mic code, dependencies and interpreter reuse accepted
preceding upstream-integration unit evidence (392 daemon passes/10 capability
skips; 110 mic passes); the actual authenticated adapter ran again in desktop
checks. No physical mic, personal clipboard, live paid provider, cross-platform,
signed distribution or personal service activation was tested or performed.
Existing separate installed apps remain unchanged until replaced. Audit results
are time-bound and do not certify all application or Python security. Local
source/package delivery only; no remote push. Agent authority/approvals unchanged.

Closure metadata: generated catalogs and memory validator passed (32 documents;
five pre-existing stale-work warnings, no errors); whitespace check passed.
Final packaged executable hash and both retained audit totals rechecked.
