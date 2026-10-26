# Electron isolation validation

Base: `13e5af951bfe78040e0cc81923e19d25b98a9560` on the personal fork's main.
Frozen source/tests/docs staged diff SHA256:
`3217b0658bda71accc414287b257117e3b396d4d2d0de23dd4d7f0272cd1ed0a`.
Process lifecycle metadata is outside this content identity.

Independent spec review: ACCEPT, original spec SHA256
`246d777b87a26d7917bc1cbac1c0cf79ee80ca0d9caad2622816ec52937bec4d`.
Independent final review: ACCEPT on the frozen candidate. Reviewer independently
ran 73 focused checks, read the docs, verified package/source hashes and inspected
actual desktop proof, screenshot and cleanup. Review receipt SHA256:
`1f66d89756ab40f631e858e262f813465e09da35a1737772ea207dc78c1ce880`.
Final full Node gate PASS: 200 files, 2,462 tests, 2,461 passed, one Windows-only
process-ancestry skip, zero failed; runner exit 0 and every file cleanup clean.
Command: `npm test -- --file-timeout-ms 120000 --summary-path <private-summary>`.
The push-hook integration completed in 57.538s. Full raw log SHA256
`c14eeb6a0d8b3828421bb1d650bf9fafb6176a565442385e1dc00a08cf6919e7`;
structured summary SHA256
`4a6326d8618081635c66d43c11f8a2e2eb64d39e2cf13f9a6383a65627a15dac`.

Raw receipts stay in a private local validation directory outside the public
repository. The private ledger identifies exact paths, configuration hash,
Node/Python/Electron/tmux versions, candidate patch and receipt hashes.
Final private ledger SHA256:
`7d74610986d1bedb9250f2fc4072f9910d13659b98f9e339fd7d00d127554890`.

| Receipt | SHA256 | Result |
| --- | --- | --- |
| Original Electron RED | `801c288189b23676116a9f6e780b5bc59243dda0021852dfeaae579b2e0ac3f8` | require/process/Buffer accessible; isolation and sandbox disabled |
| Final production desktop proof | `9725e142f91a16623da70d747136ccc279cd2b024787c99d5e0c26b7b7ed66b6` | Positive task workflows and isolation negatives pass |
| Final owned-resource cleanup | `deeaa168ba03945b3b96e4e3d98750f7fd079a8a7c6572dc0b61bfc455a7e733` | Electron/daemon exited; isolated tmux absent; credentials removed; no errors |
| Observed desktop screenshot | `08bb39fe50ad4463ae93eca636ac28965b40faa623a009417098c37012a27b66` | Real generated UI shows actual fixture assistant reply; visually inspected |
| Packaged runtime readback | `dc8578e3d7b1c1d07dbc6866db1ee1c869e53345db8f47a068eb2b6679c2377a` | Main/preload/window policy and both generated desktop pages/bundles match source |
| macOS package build | `bad699bf3cdecc4ffe008219c7fee5638bb0e21e58b9338d114ff04e2bf5a651` | macOS arm64 package built, unsigned, uninstalled |
| Final web build | `babfd8158500abf8a4abdc35e52286b51cad0b44b935e348c6793e93823b0631` | Browser build passed with existing web transport |

Real desktop coverage: exact production main/preload/browser assets, public
config, mutable Settings, authenticated v2 operator connection, real tmux/native
PTY output, synthetic provider spawn/send/reply rendering, asset publish/get/
popout/reload/dock, retained chat manager context/dock, authenticated reconnect,
main reload, explicit disconnected rejection, notification/schedule transport,
and unavailable mic response without hardware initialization. Clipboard bridge
parity uses unit fixtures; personal clipboard contents were not read or changed.

Negative controls: Node globals absent; no generic bridge IPC; inline/eval/
Function denied; unowned same-URL window receives no production bridge; real IPC
from same-URL strangers, registered wrong document and child frame rejected;
registered main frame succeeds; unexpected navigation and new windows denied.
Unit controls also cover webview/frame-navigation refusal, closed/destroyed
ownership, bounded/cyclic/deep input and event-object stripping. Child-frame
transport fixture enables subframe preload only in its isolated diagnostic
window; production preferences remain sandboxed and refuse frame navigation.

Preserved baseline: daemon/auth source and lockfile unchanged. Reuse accepted
daemon-auth evidence in the preceding completed work item; no fresh daemon-wide
or paid-provider certification is claimed. macOS source validation and packaging
only; Windows/Linux, physical audio, paid providers, hosted third-party adapters
and personal installation activation are outside this shipment.

Rehearsal failures were classified and retained privately: obsolete test global/
selector assumptions after bundling; invalid markdown fixture against the daemon's
report-only asset schema; asynchronous window-close oracle; missing cpu-features
buildcheck prerequisite after script-disabled npm install; and cleanup attempting
to signal an already-exited Electron group (macOS EPERM). Bounded harness/
prerequisite repairs preserved production authority. Final cleanup passed and
leftover temporary seat credentials from preceding owned attempts were removed.

The first final full Node run passed 199 files but its existing pre-push
integration file reached the 60-second file deadline (baseline run: 56.6s).
No assertion failure occurred. Final suite rerun uses the supported
`--file-timeout-ms 120000` option with all tests and assertions intact; source
candidate unchanged. The complete timeout receipt is retained privately.

Post-exit process inspection found zero processes referencing the seven retained
smoke directories. Receipt SHA256:
`c098aed64cb7ac248bd60b087cd9ad90a26d6eb33c18e0f7903f9cf0c4a50079`.
Process metadata validates with zero errors and five pre-existing stale-work
warnings; no new warning remains for this work item.

Shipped source commit: `d4068baba0613f259193b64e853174375ef2bee9`. Personal fork main ref independently
read back at that exact commit after push. The source/tests/docs patch content
identity is unchanged from independent QA; lifecycle closure metadata follows
in a separate commit. No personal runtime installation or activation occurred.
