# Provider sign-in

Desktop and web share **Settings → Provider sign-in**. Select the execution host,
choose **Re-login Claude** or **Re-login Codex**, read the warning, confirm the
host is available, then select **Start sign-in**. Opening Settings does not
inspect or change provider authentication.

Starting can clear or replace that host's current login. Cancelling or failing
can leave it signed out. Cancellation stops the attempt; it does not restore
credentials. Do not start while another client is signing in to the same host.

The temporary URL is displayed in the dialog. Nothing opens automatically.
Use **Open on this device** only when this is the intended browser device.
For Codex, use a browser on the selected execution host: for a WSL target, use
its Windows browser. A browser on another machine cannot reach the target's
localhost callback. This flow does not create callback tunnels or substitute
device authentication. Claude also opens a localhost callback listener. Use a
browser on the execution host for that callback, or enter the one-time code if
the provider offers one. Enter codes in the dialog's password field, never in a chat.

Keep the dialog open until it reports **Sign-in verified**. That outcome requires
a successful login process and a separate CLI authentication check on the same
host. Opening a browser alone is not success. The overall attempt is bounded to
five minutes, with up to fifteen seconds for verification.

Claude CLI output may place its URL after “If the browser didn't open, visit:”.
Pentacle recognizes that complete line as well as a standalone URL, including
the visible URL text of terminal hyperlinks. Hidden terminal metadata is ignored;
the same provider URL checks still apply.
Claude Code 2.1.318 uses `https://claude.com/cai/oauth/authorize`. Pentacle accepts
that exact origin/path pair alongside the previously supported endpoints;
arbitrary paths on those domains remain refused.

Cancel, closing Settings, reloading, disconnecting, or quitting stops the owned
attempt. **Could not confirm the provider stopped** means cleanup is uncertain;
the same application server refuses further attempts for that host. Check the
target process through your normal host administration before starting again.
Do not restart the application merely to bypass that uncertainty.

## Configuration and privacy

Host selection uses the same local, `localWsl`, `remote`, `hosts`, and `peers`
configuration as terminal attachment. A listed host without a configured
transport is unavailable. Both provider CLIs must be on the target's login-shell
PATH; Windows local execution needs the existing WSL configuration. SSH uses the
existing configured destination and SSH authentication. No credentials are
copied between machines, and this flow does not install or upgrade a CLI.

The implementation uses direct temporary PTYs, not chat sessions or tmux
history. It retains authorization URLs and codes only in memory and forwards
them only to the requesting client/provider. It clears them at terminal state
or connection loss. Raw provider output, account identifiers and arbitrary
exceptions are never emitted as application telemetry. Telemetry contains only
the provider, host, state, fixed reason, subsystem and feature reference.

Codex login and verification use `RUST_LOG=off`; Claude uses
`--debug-file /dev/null`. These apply inside the target shell, with inherited
debug selectors removed and nonessential reporting disabled for the child.
The provider still owns its credential store. Provider changes require renewed
qualification of parsing, diagnostic logging and target-process cleanup.

Web sign-in channels require the page's Origin to match the web host, including
on loopback. Missing, null and foreign origins are refused. Routable web hosts
also retain their existing token-cookie authentication. Proxies must preserve
the correct scheme and host; do not disable the origin check to work around a
proxy mismatch. Disconnected auth requests are never queued or replayed.

## Validation and current limits

The default focused suite uses synthetic providers, temporary tokens/profiles and DOM
fixtures; its native PTY check replaces the provider executable with a harmless
fixture before spawning. It never invokes a real provider login or status check.

```
node --test test/provider_relogin.test.js test/provider_relogin_ui.test.js test/provider_relogin_transport.test.js
```

An opt-in compatibility test runs an actual Claude binary under native PTY with
a disposable home, config and secure-storage namespace. It requires POSIX,
`node-pty`, `lsof`, and an explicitly selected CLI with an exact expected version:

```sh
CLAUDE_COMPAT_BIN=/absolute/path/to/claude CLAUDE_COMPAT_VERSION=2.1.318 \
  node --test test/compat/claude_relogin.test.js
```

This test never installs or upgrades a CLI. It checks the real browser handoff,
owned localhost listener, cancellation, accelerated timeout cleanup, telemetry
privacy and logged-out status before and after. It does not open a browser,
submit authorization codes or sign in an account. The timeout case uses four
seconds; the production deadline remains five minutes. The real 2.1.318 test
fails against the previous endpoint allowlist even though the fixture suite passes.
No authorization URLs or codes are written as test evidence.

The full source gate is `npm run prestart && npm test && npm run build:web`.
Use an isolated tmux namespace and temporary test state for terminal tests.
Source/mock results do not qualify a deployed client, a real account, Windows/WSL
browser delivery, or remote target cleanup. Those require an explicitly available
machine and authorized provider journey. This candidate has not yet received
that live qualification or runtime activation.

Governance ruling: the temporary login-child owner is necessary to keep a
user-initiated auth process alive and cancel it with observable cleanup. It reuses
node-pty, the terminal host transport and the shared IPC/web handler table, under
the provider re-login feature commission. It owns only the children it starts;
there is no daemon reaper, new service, database or `PENTACLE_*` setting.
