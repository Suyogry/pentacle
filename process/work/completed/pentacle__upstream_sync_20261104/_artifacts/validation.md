# Official upstream integration validation — 2026-11-04

Personal main preimage: `183838435a949425c94095a0df18590db79a36bb`.
Official main: `318c8f17f9471e5ee4b6f5c1c3ac70592a5179cf`, rechecked before
promotion. Incoming official delta: 301 commits across 368 files. Normal merge
`2100eb0c9e38c2fcabc01b7b3e4634646883e8b0` preserves both histories.
Final source candidate: `8df132e1ade2b4995cde4c22011333b82239b39b`.

## Preserved behavior

The fork retains mandatory daemon operator/seat authentication; native loopback
alone conveys no command authority. Mic requests retain credentials, Host and
Origin validation and the authenticated UI proxy. Electron isolation/CSP and
Settings scrolling remain. Dependency manifests and lockfiles are unchanged.
The corrected fork provider sign-in workflow remains supported even though
upstream removed its broken version. No orchestrator permission prompts or
reductions in authenticated operator authority were introduced.

New account pin recovery uses the existing narrow native local-admin transport,
without granting ordinary account, inventory or spawning authority. Screen lease
RPCs load operator proof only for an operator identity. Seat close requests carry
mandatory seat proof directly; retired seats can replay their own completed
close, with existing token-hash/target/generation checks. Native tests reject a
retired seat targeting another live seat and prove exactly one termination.

## Accepted evidence and recovery bounds

- Root Node: all assertions in 210 files passed. Two cleanup-inspection timeouts
  under load were recovered by rerunning exactly those unchanged files with the
  same bounded runner; both passed with clean resource inspection.
- Shared core: 410 tests passed; test and source TypeScript checks passed.
- Affected daemon unit manifest: 116 files, 3,476 tests and 835 subtests passed,
  10 skips. A frozen-source native close/restart and mandatory-auth recovery
  selection passed 62 tests after the final CLI-only correction.
- Full CLI run: 8,035 passed, 32 failed, 13 skipped. Every failure was a previous
  seat-close wire-parity expectation requiring hello. The final targeted recovery
  passed 6,833 tests, covering every failed cell, all credential matrix/loader/
  census tests, close and screen workflows, and a new implicit-seat proof test.
  The original full result remains recorded as failed; unchanged coverage is
  reused only within its actual input bounds.
- Gate environment checks: 76 passed; aggregation checks: 7 passed. Focused mic
  HTTP/security checks: 60 passed. No microphone capture occurred.
- Desktop/web builds passed. Actual production Electron, isolated authenticated
  daemon, synthetic provider and native PTY/tmux passed rehearsal and final UI
  smoke: rendered chat reply, terminal, popout/dock, settings, notifications,
  schedules, reconnect/reload and disconnected-send refusal. Isolation negatives
  passed. Cleanup confirmed owned Electron/daemon exited and tmux/credentials
  absent, with no errors. Application/daemon inputs to this evidence are
  unchanged by subsequent CLI-only and fixture repairs.

Initial failed daemon evidence is retained. The original file selector included
two live soak files by mistake; the corrected unit manifest excludes the soak
directory as the official unit gate does. Newly imported upstream fixtures were
adapted to mandatory authentication and private launch-token staging. Negative
anonymous and forged-context checks remain denied; production guards were not
weakened. Release-selection tests use separately installed Python 3.13/Node 22
prerequisites; the overall local test tuple is macOS arm64/Python 3.14/Node 24.

## Audit and scope

Production npm audit: zero known advisories. Full audit retains one moderate
minimatch advisory propagated through six existing build-tool packages; none is
introduced by this merge. No high or critical findings. No forced dependency
upgrades or lock changes were made.

No personal application/service restart, real paid-provider inference,
microphone capture, fleet deployment or full soak/default-CI certification is
claimed. Raw logs and screenshots remain in the maintainer's private
`upstream-sync-20261104` evidence bundle. The public digest inventory records
receipt names and SHA256 values without personal paths or credentials.

## Independent review and source disposition

Independent final QA: ACCEPT on the frozen source candidate above; 93 focused
tests passed independently. All 23 original evidence digests and critical-file
preservation checks were verified. Source was fast-forwarded and pushed normally
to personal main. This closure changes process metadata only; the accepted source
identity remains unchanged.

Desktop and web assets were also rebuilt successfully in the promoted laptop
checkout for the next launch. Final catalog generation and full/source-only
metadata validation passed; five pre-existing stale-work warnings remain.
