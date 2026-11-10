# Source integration validation

Private bundle `upstream-sync-20261110`; gate manifest SHA256:
`6ecedc304040320ef11fd58f216d7f14ae582c58a95078bdf700c782ca096fdc`. Raw receipts/configuration stay private.

- Full CLI: 8,122 passed, 13 skipped.
- Core runtime/type tests and standalone typecheck: pass.
- Mic HTTP auth/origin/Host boundary: 46 passed, no capture/model calls.
- Final affected daemon controls: 491 passed.
- Broad daemon: 5,127 passed, 29 failed before bounded fixture/probe repairs;
  19 residual IDs remain after repairs and exactly reproduce on original fork
  or official upstream. These are failed gates, not a fully certified run.
- Root Node: 206 files pass; two harness failures (one timeout, one process
  inspection) both pass unchanged isolated recheck with clean owned resources.
- Desktop synthetic native-provider/PTY/auth/isolation journey: PASS; owned
  Electron/daemon/tmux/credential cleanup all proven.
- Web six-scenario chat/config/voice/gallery/dashboard smoke: PASS.
- Existing production dependency versions unchanged; production audit zero,
  full audit six moderate tooling entries, no high/critical.
- Fourteen protected fork preimage hashes unchanged; PIMR ref unchanged.
- No actual provider inference, runtime/service activation or packaged desktop
  replacement. Independent final review pending.
