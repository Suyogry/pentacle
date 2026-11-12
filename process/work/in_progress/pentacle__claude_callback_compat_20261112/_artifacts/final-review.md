# Independent final QA

Verdict: **ACCEPT** for the bounded local source repair and real-CLI compatibility
test. No blocking findings or advisory code defects found.

Candidate content identity:
`27e58fe8928e6ff56adb9e0d52fcf9ea558445d31cce65bed7675e3068c083d7`.
Base: `9caadf1736c3c03cc8b373a9f8f2edfd8ea6bec7`.
Evidence index reviewed: `validation.md`, SHA256
`bf745776a6d9eb45dff9f19df034f5d672358dfde57d993343e94daf95d663e4`.
All six files independently match the hashes in `candidate.json`, including
the final compatibility-harness assertions.

Reviewer: independent Codex final-review worker, inherited available model and
effort. Task class: implementation judgment, selected for authentication parser
trust boundaries, real child-process ownership, isolation and cleanup review.

## Reviewed behavior

Read the accepted spec, repository instructions, QA guidelines, full provider
controller, six candidate files and retained RED evidence. Cold-read the complete
provider sign-in documentation and exercised its opt-in test command with the
exact binary rather than a fixture executable.

The production change adds only the demonstrated Claude 2.1.318 origin/path
pair. Existing endpoint pairs remain equivalent to their previous behavior.
HTTPS, complete-line parsing, OSC metadata rejection, userinfo/fragment refusal,
and nonempty state/client/challenge validation remain intact. New negative
controls cover wrong endpoint combinations, lookalike domains, HTTP, missing
parameters, userinfo, fragments, and Codex separation. Chunked visible OSC8
output must reach its final newline before the browser event is emitted.

The real test keeps production login flags, shell wrapper, native PTY and exit
receipts. Its launcher invokes the selected actual Claude binary with an empty,
constructed environment and unique home/config/secure-store namespace. It
asserts that production suppresses automatic browser navigation, checks listener
ownership through process descendants, observes callback listener closure after
both cancellation and timeout, and checks logged-out status before and after.
Authorization material is retained only transiently and absent from telemetry.
Failure paths invoke controller cleanup and reject unconfirmed cleanup.

## Independent checks

- Focused controller/UI/transport/fork/desktop-security/public-IPC tests:
  **63 passed**, zero failures, zero skips.
- Exact real Claude Code **2.1.318** compatibility test: **1 passed**, zero
  failures, zero skips. macOS arm64, Node v22.23.4, binary SHA256
  `677a2ea7bf576cedd20e191d973914ed8a41796f53a63b1923381ddc4d5b5e7d`.
  The real provider reaches `awaiting_browser`; both owned-listener cleanup
  journeys and still-logged-out isolation assertions pass.
- Candidate manifest independently recomputed before and after review: matches.

Independent raw receipts remain outside the public source tree. Their names and
SHA256 values are:

| Receipt | SHA256 |
| --- | --- |
| `pentacle-callback-qa-focused.txt` | `5906a834f45e757cce7a0ab16560c17f4d2a15873146205b0e866ea99b031aed` |
| `pentacle-callback-qa-real.txt` | `9ba77f6cc1128df3b60ae2b8d6efe252a9f4c6f4e67dbfc89e1726e49826a4bc` |

## Limits and disposition

This accepts the source repair and local compatibility evidence, not a deployed
release or a completed account sign-in. The five-minute timeout remains
user-reported; the real automated test uses four seconds and documents that
bound. No browser authorization, credential exchange, Windows/WSL, SSH, installed
app activation, or full repository test certification was exercised here.
Desktop/web build results are retained lead evidence and were not rerun by this
reviewer. Filing the requested issue and any subsequent source disposition or
activation remain with the lead. No further runtime test is required for this
bounded verdict.
