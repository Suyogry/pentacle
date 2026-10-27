# Settings viewport validation — 2026-10-27

Scope: source desktop/web CSS and setup documentation, base
`c03f51b2e4aa99e6fa696d78c45bb470627ba061`. Source/docs diff SHA256:
`ea882a1a39b8854bfa821e073da58d42b0359e3d0175f17d3b42ce5ecc1ad4c7`.

Actual native screenshot inspection confirmed tall Settings. Disposable actual
Electron 44.9.3 loaded production main/preload/generated browser assets, explicit
fixture config without daemon/provider endpoints and a separate user profile.
No live provider login, credential access or paid model call was initiated.

Before: 12/12 geometry cases failed. At 1280x800, the collapsed modal measured
979px tall, top -89.6; expanded sign-in was taller. Done/Start sign-in could not
be scrolled into view. Parent viewport overflow hid content.
After: same 12 cases pass at content sizes 1280x800, 1024x600 and minimum720x480,
both visual styles, sign-in collapsed/expanded. Dialog stays within viewport,
heading/footer remain visible and list scrolling reaches all sign-in controls.
Six further cases with a synthetic 2,000-character URL, code field, long status,
pending-reload footer and native Tab-to-Done all pass. Screenshots inspected.

Initial private harness startup error (Electron module resolution), stress
watchdog and two unfocused native-keyboard results were retained/classified as
harness failures. Corrected harness uses Electron's builtin module, removes
ELECTRON_RUN_AS_NODE, focuses the owned fixture before Tab, waits for asynchronous
focus completion and disables background throttling for animation-frame waits.
Production code was not changed for those harness errors. The comparable base
12-cell probe was rerun against unchanged old CSS before GREEN. No guards or
assertions were removed. Probe processes remaining after final run: zero.

Both desktop/web builds pass. Seven focused files: 62 tests pass, zero failures
or skips, cleanup clean (Settings version/reload/turn-duration, provider sign-in
UI/transport, desktop security, chat-first workspace). Existing full root/native,
daemon/auth evidence is reused only for unchanged JS/backend/dependencies.
This is scoped macOS CSS acceptance; no cross-platform or provider/hardware
certification, production-window reload, package replacement or remote push.

Raw receipts/screenshots stay in the maintainer's private
`layout-check-20261027` directory. Key SHA256 receipts:

| Receipt | SHA256 |
| --- | --- |
| before-v2.json | 441653891ca9834c2277c7f4f5e27af0eb5498e7af833165f7b7db6c65191564 |
| final.json | 2c2d648c63d73e20ec1b92d8c741055bbe821c354df4f94dacae4a82fdf773d9 |
| stress-initial-failure.json | 0749268559d96784e12384e66db57e1a1fe679b0bfdaf7c4fd2ac435c84d0cd7 |
| stress-diagnostic.json | f5487d3fed22229686f3429b7ff9f20e82242c52013ce62ef3fa59a24507debe |
| stress-final.json | 0c3d6bfa22a1ad6e7571292654f01580869484ff6c1fbfbb6e81ef0ebc3b4684 |
| final-1280x800.png | 0cf11417f6049c4e2d99e927a79e7de43c502e88a325f099cee6d2528a921ed3 |
| final-720x480.png | a885691a4e24d266136460c2b535dc9119481c464d207f51e3a165b5d189a045 |
| checks.json | ab1c3f0c592e04e46678a903a868cde11c8c3e55933cf2a5833df4c9183aedd0 |

Independent final QA: ACCEPT for the frozen diff; independent geometry12/12
and focused settings/provider/security21/21 passed. qa-final.md SHA256:
`9f28e892972a873c75f05f96388fe287cde04d3270e07be123e8e3b50e7a79e7`.
