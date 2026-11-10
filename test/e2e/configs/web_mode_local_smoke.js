'use strict';

// External-daemon web smoke profile. Use a disposable authenticated daemon
// configured via README.md#quick-start, with local host identity `local`.
// Supply its port and owner-issued private operator credential explicitly:
//
//   export PENTACLE_SMOKE_PORT=49001
//   export PENTACLE_SMOKE_TOKEN_PATH=/absolute/private/operator.token
//   node test/e2e/web_gate.js --profile test/e2e/configs/web_mode_local_smoke.js
//
// This profile does not start, stop or enroll a daemon. With no --profile,
// web_gate.js instead owns its isolated daemon and temporary credentials.

const path = require('node:path');
const rawPort = process.env.PENTACLE_SMOKE_PORT;
if (!rawPort || !/^[0-9]+$/.test(rawPort)) {
  throw new Error('PENTACLE_SMOKE_PORT must be a decimal integer in 1..65535');
}
const smokePort = Number(rawPort);
if (!Number.isSafeInteger(smokePort) || smokePort < 1 || smokePort > 65535) {
  throw new Error('PENTACLE_SMOKE_PORT must be a decimal integer in 1..65535');
}

const smokeTokenPath = process.env.PENTACLE_SMOKE_TOKEN_PATH;
if (!smokeTokenPath || !path.isAbsolute(smokeTokenPath)) {
  throw new Error('PENTACLE_SMOKE_TOKEN_PATH must name an absolute private operator credential file');
}

module.exports = {
  appName: 'Pentacle',
  features: { mic: false },
  tmux: 'tmux',
  // Keep machine glyphs visible for the gate's real-app contrast assertions.
  hosts: { local: { kind: 'local' }, local2: { kind: 'local' } },
  agents: {},
  chatStream: {
    url: `ws://127.0.0.1:${smokePort}`,
    localHost: 'local',
    hosts: ['local', 'local2'],
    // The host authenticates server-side; no credential enters the browser.
    tokenPath: smokeTokenPath,
  },
};
