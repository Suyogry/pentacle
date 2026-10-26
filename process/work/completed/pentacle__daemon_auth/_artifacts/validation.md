# Source validation receipts

Candidate source/tests/docs diff SHA256: `5ab7c099594622d0b0be0bb2ab3ced2d35664c641e8ae6af2d8ae010ec89bb33` against `9d1d1f48edcde8cb763a43a4960bf501b697de0a`. Process metadata excluded. Raw receipts remain in the private temporary workspace; only hashes are distributed.

| Check | Raw receipt basename | SHA256 |
| --- | --- | --- |
| RED native localhost read | pentacle-daemon-auth-red.log | `f88b7c7eb128a8105810545c7c3a288eee8d9092f79de939a9f83a76bebc2e0d` |
| Daemon auth/launch/schedule/recovery combined; 615 passed | pentacle-daemon-auth-final-combined.log | `db3f816b6e54542791e8bdd5c5cd0ac9ab07a72b1ed1b1124a7896239bc528e4` |
| Maintenance probes and connection diagnostics; 125 passed | pentacle-daemon-auth-tools-final2.log | `940caa6529d89295730c5939c785c481e01045d7710d6a24a3e2c39c522562ab` |
| New actual-socket repair regressions; 19 passed | pentacle-daemon-auth-security-repair.log | `2144f7019c31e31876d19f74b069ea36a2ce9d79ef2160a1ec8494a59d6d1e1f` |
| Full CLI before bounded repair; 7257 passed, 13 skipped, 1 deselected | pentacle-cli-auth-final-verbose.log | `8f95867bdab11a57acbcaeac4cf75c0334455644ea6a0be70da08c82b4de019f` |
| CLI repair regressions; 6223 passed | pentacle-cli-auth-repair-final.log | `c0d1375e824c40a3e05e9f99d05b6f185073b24f05bb85e600e9684c9a03a757` |
| Node; 2455 tests, 2452 pass, 3 skip, 0 fail | pentacle-daemon-auth-node.log | `e6fbb9c6f4d0608ce2a1aa7f81aab179f8f5eb4539182c39a77636e287bce441` |
| Web build passed | pentacle-daemon-auth-web-build.log | `60ab1ca97a7f75dc11a945497dd8b5a137595c84308abf8b75f19db7ea322468` |
| CLI installer explicit Python no-install dry run passed | pentacle-daemon-auth-cli-install.log | `830982e549e4fd85168d0ede2fad025b30e69dfdc19a2e5d6f601e797a0707e6` |

Spec QA: ACCEPT. First final review: server/scoped egress/private files/docs accepted, CLI caller/lineage and special operator fallback rejected. Bounded repairs removed fallback, separated relationship metadata from caller identity, and added real-socket controls. Final repair QA ACCEPT on the frozen repaired candidate; independent actual-socket repair checks: 19 passed in 0.63s.

The broad full CLI result predates only the bounded CLI identity repair; the 6223-test repair selection reruns all affected wire builders, wsclient, loader, command-translation and census surfaces. Unchanged installer/parser/other CLI evidence is reused. Daemon 615 and tools 125 cover the prior source; four added repair regression cases bring the new actual-socket suite from 15 to 19. Server implementation is unchanged from those runs.

Unavailable: tmux/native provider workflow certification; smoke autouse isolation fails before its test subject because tmux is absent; multi-bind macOS alias unprovisioned. No full certification claimed. Installer auto-discovery of a Python 3.13 executable is an unrelated environment prerequisite (one test deselected); explicit supported Python override verified without installing. Paid-provider, device and fleet runs were outside source shipment scope.

The owned services were stopped throughout. Private launch files use a separate full operator credential for the orchestrator, with valid offline challenge/proof and owner-only files; no secret material is tracked.

Shipped source `6b68a998bd9cee0cb8939fefdedcee9b97bb327c`; remote main readback matches. Source diff identity read back after commit still matches the accepted candidate above. Work tree clean before this closure metadata update.
