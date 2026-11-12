# Independent specification review

Verdict: **ACCEPT** for the bounded investigation and conditional repair plan.

Reviewed spec SHA256:
`55f455bcea9122f0e331606b5e140e7e8334a73c956acc97f527b88f213fdf8c`.
Repository base: `9caadf1736c3c03cc8b373a9f8f2edfd8ea6bec7`.
Reviewer: independent Codex spec-review worker, inherited available model/effort;
task class: implementation judgment because the provider's authentication behavior
and the controller's process ownership interact.

## Scope and checks

Read the spec, root AGENTS.md, QA guidelines, production provider controller and
execution-host command construction. This review did not run a provider, modify
authentication, send an external message, or evaluate an implementation candidate.

The plan has objective browser-handoff, listener, cleanup and logged-out-profile
checks, requires real-version RED before choosing a production fix, preserves URL
trust and separate authentication verification, and distinguishes a short timeout
test from the reported five-minute timeout. It correctly avoids treating passing
fixture tests as real-provider proof. No blocking specification defects found.

## Advisory implementation details

- High confidence, low severity: enforce the disposable HOME/config/secure-store
  isolation in the environment that actually reaches the CLI, including inside
  the login shell. An environment allowlist must omit inherited OAuth/API token
  variables. The production wrapper invokes a login shell, so setting only a
  parent test-process HOME is insufficient evidence of confinement. Record a
  sanitized isolation assertion and preserve the default authenticated profile.
- High confidence, low severity: identify the listener as belonging to the owned
  child, rather than proving only that some process accepts its port. Keep any
  URI containing state or PKCE data out of assertion failures and receipts.
- High confidence, low severity: provide deterministic bounded cleanup for failures
  before the test's main assertions. The controller's cleanup_failed result is
  a failure, not successful test teardown; it may require terminating the test's
  owned process and confirming listener closure without touching unrelated jobs.

These clarify the existing contract and do not require additional user approval
or broaden acceptance into paid-account authentication.

## Limits and next action

The exact-version runtime result, target binary identity and keychain-isolation
claims remain for the investigator and implementation reviewer to verify. No
judgment is made that the reported callback regression reproduces on this host.
Proceed with the isolated probe, then lock the demonstrated repair scope and
freeze its final candidate and evidence for independent implementation review.
