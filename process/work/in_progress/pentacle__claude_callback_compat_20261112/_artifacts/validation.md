# Validation evidence

Candidate content identity: `27e58fe8928e6ff56adb9e0d52fcf9ea558445d31cce65bed7675e3068c083d7`.
Per-file identities: [candidate.json](candidate.json). Base:
`9caadf1736c3c03cc8b373a9f8f2edfd8ea6bec7`.

## Actual version and environment

Official npm `@anthropic-ai/claude-code-darwin-arm64@2.1.318` native executable,
SHA256 `677a2ea7bf576cedd20e191d973914ed8a41796f53a63b1923381ddc4d5b5e7d`.
Real compatibility test: macOS arm64, Node v22.23.4, real node-pty and production
controller/login wrapper; only executable resolution points to an isolated
launcher of that exact binary. The launcher constructs an empty environment
with unique temporary HOME, config and secure-storage namespace. No user tokens
or credentials are copied. Normal installed CLI remains 2.1.246 and authenticated
before/after the probes. No account identity was captured.

## Results

- Baseline focused suite: 52 passed; no actual provider invoked by that suite.
- Actual pre-fix 2.1.318 RED: process starts, owned localhost listener opens,
  emitted endpoint is `https://claude.com/cai/oauth/authorize`, controller stays
  starting. Clean cancellation closes listener; disposable status false before
  and after. Sanitized [real-red.json](real-red.json) records observations.
- Added real compatibility test against old production code: FAIL at
  `Real CLI must reach awaiting_browser (old endpoint allowlist fails here)`;
  listener assertion had passed first, and cleanup confirmed. Runtime ~10.6 s.
- Unit RED: two added endpoint/controller regressions fail against old code.
- Final exact-version compatibility test: 1 passed, zero skips, runtime ~5.3 s.
  Real awaiting_browser, owned listener, cancellation and four-second timeout,
  listener closure, URL/state/challenge telemetry checks, and logged-out status
  all pass. Authentication is not claimed from browser handoff.
- Final focused controller/UI/transport/fork/desktop-security/public-IPC suite:
  63 passed, zero skips.
- `npm run prestart` and `npm run build:web`: passed.
- `git diff --check`: passed.

Raw test/build receipts stay in the private sibling reviews workspace because
native test output includes machine paths. Filename and SHA256 identify them:

| Receipt | SHA256 |
| --- | --- |
| `desktop-build.txt` | `4f2f26dc16c2bb70b3c96ff79ea12e489b4c64b01da1264698c883ba95763cb7` |
| `focused.txt` | `96d10786658ff05e1e27be6bd9304bc7cb742a4c17dbf3e74acba554105031c4` |
| `real-final.txt` | `9172ee12d7f7614dd7effc670f683717e0a254739bc7fcbbe9d9a7ef7b64deeb` |
| `real-green.txt` | `fc82ff6f54216516574b72377c77761765224221466d7adf3489da60d19ea838` |
| `unit-red.txt` | `03c1ce8c72d5b4262c1ccd65d95026427e0a6891b5e2a0f61074f798aa2e3860` |
| `web-build.txt` | `b8518f5a5aed76d1ec996c04d2abc235e2b1c32495fec814fed5f069f9090edf` |

## Boundaries and remaining work

The five-minute timeout is user-reported; production still defaults to 300000 ms.
The real test accelerates it to four seconds and does not prove five-minute
endurance. No browser authorization, account login, installed app activation,
Windows/WSL or SSH qualification was performed. Full npm test certification was
not run; these are scoped compatibility checks. The source patch remains local.
Independent final QA and the authorized Suyogry/pentacle issue are next.
