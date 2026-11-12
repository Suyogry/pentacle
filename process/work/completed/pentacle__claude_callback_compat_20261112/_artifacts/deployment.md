# Local desktop activation — 2026-11-12

User authorized deployment after source QA. Independent release-plan and
artifact QA ACCEPT. Applied a scoped hotfix to the registered macOS app while
it was closed; complete preimage and rollback retained privately. No daemon
restart, native dependency change or CLI upgrade was required.

Installed baseline: `ac9cec6894228265589c0969cb31e2fadc7e41ea`.
Hotfix archive SHA256:
`f2d981118406939c1e63e2438a61e7d50911b2b06c8cee5f369266a37bce7ae8`.
Header/plist integrity:
`1812462459e3cbfef9e116904dffaa4d6dc0400ee8ef3d8da097763fca7bc827`.
The old build SHA remains the baseline label; the archive hash identifies this
hotfix. Do not treat that old label as the deployed content identity.

A no-op desktop rebuild matched all original generated outputs byte-for-byte
using the installed source, original build aliases and toolchain. Compared
10777 archive entries and 8838 file contents; only provider_relogin.js, Claude
browser-guidance source, generated desktop bundle/map, and provider sign-in
documentation changed. All archive links/unpack/executable metadata matched.
The existing 344-entry physical native tree was retained and verified identical
in bytes, types, modes and links after installation.

First packaged rehearsal failed before native process creation because the
archive writer dropped execute bits from the generated rehearsal native copy.
This was a harness precondition failure; no product acceptance or app installation
occurred from it. Restored the exact original native tree and verified its full
physical metadata. The next rehearsal and post-install real-CLI test each passed
1/1 with zero skips on the app's Electron44.9.3/Node24.22.0 runtime, loading its
actual archive controller and packaged node-pty. Exact Claude2.1.318 identity is
unchanged from source evidence. Disposable status, callback listener ownership,
awaiting_browser, cancellation and accelerated timeout cleanup all pass.

The registered app launched successfully; its live executable mapping and loaded
archive document were verified. Settings shows the new callback guidance. During
UI inspection the user started a real sign-in attempt; the live app then displayed
Waiting for you to complete sign-in with the new accepted endpoint. The agent did
not open the authorization URL, submit a code, cancel that attempt or modify the
real provider login. The attempt was left open for the user. Account authorization
is separate from this completed deployment. Five-minute endurance remains untested.

Raw private deployment receipts, identified without publishing machine paths:

| Receipt | SHA256 |
| --- | --- |
| `preimage.json` | `ce1312d5e9ff6fadc0a272ac16264bf85692472c849b5c2fd140732af5756b55` |
| `noop-manifest.json` | `8b354724b2dfb0057f4c6d2c03c99fcdb1e17fefed7491dc0294c29fde770db2` |
| `candidate-manifest.json` | `779bfe618f1439099128b6d9b91742a0cc566f2b23a42fc5a56349ec46cfb517` |
| `candidate-renderer.diff` | `6be21fd2a045b582e1a8cdf332bf7d5e86928d273ef96229acda24658b2ed897` |
| `unpacked-mode-verification.json` | `1f40e33453c5f4385b3aebe0981bcf27ed7df76476bb41c92b76f19abd58c517` |
| `compat-candidate-failed.txt` | `d93958363996006f819581125fdf5405d7d2305584c9f60b3168cfd57668859e` |
| `staging-failure.json` | `5932eb33948883df7551a934a58cea2e2a54bd4e10be63397fa58fc8a6834e6b` |
| `compat-candidate.txt` | `21cbc073422a78224008a3df117814987f1141856e119576c033070ece135286` |
| `compat-installed.txt` | `7f764eac95420b7eb9c31eca9dd526ff2552a32808f0a5e8237d1857c0d64f42` |
| `installed.json` | `5202baecbd315fba95577bfae86cc1be989f73435fe2bd6d39dc83871c4cda8a` |
| `activation.json` | `73b76a6d1219cb7b54afed25089d24c65df801db2089f38c59ce1fd67e202edd` |
| `release-plan-qa.md` | `db2f5f1785ba80d6e6ca771a8e3bb3bf90a93596a61ccbee08aa31ace2541de8` |
| `release-artifact-qa.md` | `3681192490ed61f6199a9048c6d7469803ccad8c8ab13260a2567b339597ff88` |
