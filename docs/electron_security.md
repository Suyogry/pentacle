# Desktop isolation

The retained Electron desktop uses a sandboxed renderer with Node integration
disabled and context isolation enabled. Main, asset and chat popout windows load
browser bundles from `renderer/dist/desktop/`. Run `npm start` to build these
assets before launch; `npm run build:desktop` builds them without launching.
All desktop packaging commands build the same assets first. Direct `electron .`
requires a prior desktop build.

The main process loads private configuration and authenticates to the daemon.
A sandbox-compatible preload exposes the existing named `window.cc` methods,
public `window.HOST` metadata and a credential-redacted startup configuration.
The UI gets a mutable copy of that configuration for its existing settings.
Backend tokens, credential paths and secret-named optional adapter fields stay
in the host. Keep secrets in credential files rather than embedding them in
presentation strings, startup messages or executable command strings.

Every desktop IPC handler, including terminal and clipboard handlers, requires
a live window registered by the main process, its main frame, and its exact
expected file document. A matching URL in another window grants no authority.
Navigation, new windows and webviews are refused. A desktop content security
policy blocks inline/evaluated/remote scripts, network connections, embedded
frames, objects and form submissions. Existing inline styles, local images,
fonts and blob media remain usable. External HTTP(S) links use the named
main-process browser-opening method.

These changes preserve the daemon's existing permissions and agent autonomy.
They add no task approval prompts. The named bridge remains privileged: its
terminal and agent operations intentionally retain their existing authority.
Treat renderer injection as a security defect even with isolation enabled.

Built-in dashboards remain available. Private hosted dashboards and arbitrary
third-party adapters are not supported by the file-based desktop; use the
[authenticated web host](../server/README.md) for hosted views. This change does
not enable the public desktop's currently unimplemented chat-popout IPC action
or other external adapters. The retained chat-popout manager uses the same
window policy when invoked by an integration.

For a graphical macOS check, install tmux and lsof, install Python dependencies
as documented in the [daemon README](../services/chat-stream-v2/README.md), run
`npm run build:desktop`, then `python tools/public_desktop_smoke.py`. The smoke
uses temporary credentials, a private tmux socket and a synthetic provider. It
checks real desktop startup, settings, authenticated spawn/send and terminal
output, rendered replies, asset popout/reload/dock, chat-manager context,
reconnect, reload and disconnected rejection. It also probes CSP, Node-global
absence, unowned/wrong-document/child-frame IPC and navigation. Evidence and a
screenshot remain in the printed temporary directory; temporary credentials
and the owned daemon/tmux processes are removed. Clipboard method parity is
unit-tested without reading your clipboard; no physical mic or paid provider is
used. This is source validation on macOS, not Windows/Linux or hardware
certification. The separate terminal interaction fixture retains Node access
for source inspection and does not establish production-window isolation.
