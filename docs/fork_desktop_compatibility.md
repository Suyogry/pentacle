# Desktop compatibility in this fork

Official Pentacle removed its Electron shell in November 2026. This fork keeps
the desktop entry point, isolated preload, native clipboard/popout adapters,
build commands and smoke harness because existing installations use them.
Pentacle Web remains the recommended client and receives upstream UI features.

Desktop continues to use the shared renderer and `main/cc_handlers.js`, including
provider sign-in, account catalog, terminal and authenticated daemon contracts.
Its renderer has Node integration off, context isolation and sandbox on, a
restricted IPC bridge, a content security policy and guarded navigation.
Credentials stay in private host configuration; do not put them in the renderer.
Microphone requests still require authentication and host/origin admission.

Install dependencies with `npm ci`. Use `npm run build:desktop` and `npm start`
for a development launch, or `npm run build:mac` for a macOS package. These are
fork compatibility commands, not official upstream release instructions.
Build and serve the web client with `npm run build:web` and `node server`.
The separate design-gallery page is primarily a served-web feature.

Pulling source does not upgrade an already-running packaged desktop app or
restart the daemon. A source-mode daemon may read changed source metadata, so
source integration is not proof of a coordinated runtime deployment. Preserve
private profiles, credentials, active work and service configuration during an
upgrade; use the normal authenticated runtime release procedure when explicitly
activating backend changes. See [desktop configuration](desktop_config.md) and
[daemon authentication](daemon_authentication.md).

The upstream merge does not include the separate PIMR feature branch. Its
reviewed source stays isolated until deliberately merged and configured.
