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
- Sequenced browser-to-host-to-tmux typing, resize and detach: PASS.
- Existing production dependency versions unchanged; production audit zero,
  full audit six moderate tooling entries, no high/critical.
- Fourteen protected fork preimage hashes unchanged; PIMR ref unchanged.
- No actual provider inference, runtime/service activation or packaged desktop
  replacement. Independent final source/security and repaired docs/profile review: ACCEPT.

Accepted source candidate: `a86a8524918ee0deedadf38d3ff573270fb61ac7`.
Initial independent review rejected only stale anonymous web setup; source and
security were accepted. Bounded repair supplied explicit external-profile
credentials and corrected docs. Independent real isolated profile/host/daemon
success, missing-credential rejection and cleanup passed.

Private review receipts SHA256:
- `final-qa.md`: `8538a1d913b91259a32931af9206ead70b06d86a4fa861d349a8010760629cde`
- `final-qa-repair.md`: `c7582c19cb5f1376ecf8944018a0ea7b84eccbc5a4d6d7806918b57377abb367`

Local main fast-forward and normal fork push succeeded. Main desktop/web builds
passed; actual daemon authenticated hello/catalog readbacks passed with the same
PID. Protected files, private launch/config hashes and PIMR ref match preimages.
Runtime/source-mode caveats from the spec apply. Closure edits are metadata only.

Private closure manifest SHA256:
`a96f5dc1c370f71906bd5705c3f6065bada51c78033a9ceed35574673876e8a3`.
