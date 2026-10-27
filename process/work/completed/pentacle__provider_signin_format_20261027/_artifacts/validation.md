# Provider sign-in format validation — 2026-10-27

Base `a4fa51dab27378a2e99bac6372b9b8c03b973c2b`; frozen source/tests/docs diff
SHA256 `68671295d8d558e7fd0e45b973578c37f9150214580a96a7443362a0f841c15f`.

Actual user desktop showed Starting sign-in with an owned Claude child running.
Read-only installed CLI2.1.246 help/version and bundled source confirmed its
complete URL line has the exact prefix "If the browser didn't open, visit: "
and OSC8 hyperlink formatting. Existing parser required URL at line start.
The user's stuck attempt was cancelled through its own UI; clean cancellation
and absence of its owned child/wrapper were verified. No auth store was edited.
The [upstream issue](https://github.com/anthropics/claude-code/issues/75099)
corroborates terminal hyperlinks; installed source identifies the exact prefix.

Three new selected tests failed before the change (exact prefix and two split
OSC8 terminators). Final controller regressions preserve complete-line/query
handling and refuse wrong domains/schemes/paths, missing challenge, userinfo,
fragments, arbitrary prefixes, prefixed Codex output, hidden metadata and
misleading visible labels. Existing bare URL, both providers, verification,
cancellation, timeout, ownership, origin and privacy checks remain passing.
Five focused files:59 tests pass, zero failures/skips, cleanup clean. Desktop
and web builds pass. No dependency, auth-policy or timeout change.

Disposable actual production main/preload/browser plus real native PTY uses an
exact replacement of the provider executable with a synthetic fixture before
spawn. It never invokes the real provider or accesses its auth store. Complete
fixture URL appears in the visible UI; dummy code completes only after a separate
verification process; a second attempt cancels cleanly. All three owned native
children exited and screenshot inspected. The first screenshot was captured
before composition and retained separately; final capture awaits paint and
asserts URL field within the visible scroll region. Test oracles were not relaxed.

Raw receipts live outside public source in private `signin-format-20261027`.
Key SHA256 receipts:

| Receipt | SHA256 |
| --- | --- |
| baseline.json | 372f7c9708acb41cd280231b42b7e2c612abd6fb1773b7b1484fc0a5c515cc37 |
| red.log | e7878ec2aabc1d678cfbd8338cf7ee2664d42ebed2a934ba358e547ddc53d32d |
| focused.log | 070a9c481cfbe2f3a81b21c365278494302de0917cb1f1d15e4bfa0d658e2f5c |
| build-desktop.log | c3d53adb26f44bc0185b66f28cd26c19c7ee4bbdef8ec245fad5a7a6b82c01e0 |
| build-web.log | f4db3bc5c6f6110db71ed405609a2183741c2563a162e18d69ca07d7a44247bf |
| desktop-proof.json | 77a1ddd1e84d47330b8a1c0d1b5684e7ac764e18d1647d6b87af29e0ce6c9149 |
| desktop-proof.log | 179160ee3c18f432938e25910e029e93b4d1c544918c18d325644a584d64d9e1 |
| awaiting-browser.png | e93fa15af6bb111603e276521a2b27f29e916d3281749704ceea1e7d4ac12344 |

Acceptance is scoped macOS source behavior with a synthetic provider. No real
account sign-in, paid provider usage, cross-platform certification, package
replacement or remote push is claimed. Prior unchanged dependency/backend/layout
acceptance is reused only within its original bounds.

Independent plan and final QA ACCEPT. Independent38/38 controller/security
tests passed, including native fixture. qa-final.md SHA256:
`52689cf64fdfa7969425b4398e33eab538d7b9718033007d8daa11b5baa45d39`.

Source-mode activation: original stuck attempt remains cancelled before restart.
Preimage, launched process/content identity and post-restart readiness readback
are retained privately. Restart alone does not complete provider authentication.
