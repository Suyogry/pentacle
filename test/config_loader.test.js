const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('node:path');

const { candidateConfigPaths, machineKey, withThemeDefaults } = require('../config-loader');
const { configWarnings, loadConfig } = require('../config-loader');

test('warnings identify omitted multi-host presentation maps individually', () => {
  const config = { chatStream: { hosts: ['local', 'workstation'] } };
  assert.equal(configWarnings(config).length, 1);
  assert.match(configWarnings(config)[0].message, /hostNames.*hostColors/);
  assert.match(configWarnings({ ...config, hostNames: {} })[0].message, /hostColors/);
  assert.deepEqual(configWarnings({ ...config, hostNames: {}, hostColors: {} }), []);
  assert.deepEqual(configWarnings({ chatStream: { hosts: ['local'] } }), []);
});

test('warnings flag enabled mic without an explicit endpoint', () => {
  assert.match(configWarnings({ features: { mic: true } })[0].message, /mic/);
  assert.equal(configWarnings({ features: { mic: true }, mic: {} }).length, 1);
  assert.deepEqual(configWarnings({ features: { mic: false } }), []);
  assert.deepEqual(configWarnings({ features: { mic: true }, micServerUrl: 'http://localhost:7780' }), []);
  assert.deepEqual(configWarnings({ features: { mic: true }, mic: { useStreamHost: true }, chatStream: { url: 'ws://localhost:7791' } }), []);
});

test('unknown top-level keys warn without exposing their values', () => {
  const warnings = configWarnings({ hostColros: { secret: 'do not log me' } });
  assert.match(warnings[0].message, /hostColros/);
  assert.doesNotMatch(warnings[0].message, /do not log me/);
});

test('loadConfig returns warnings and writes them to stderr', (t) => {
  const fs = require('node:fs');
  const os = require('node:os');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'desktop-config-test-'));
  const file = path.join(dir, 'config.js');
  fs.writeFileSync(file, 'module.exports = { hostColros: {} };');
  const seen = [];
  t.mock.method(console, 'warn', message => seen.push(message));
  t.after(() => { fs.unlinkSync(file); fs.rmdirSync(dir); });
  const loaded = loadConfig(dir, { PENTACLE_CONFIG: file });
  assert.equal(loaded.warnings.length, 1);
  assert.match(seen[0], /hostColros/);
});

// Regression guard (public_e2e_harness): a config missing dark/terminal crashed
// the app at launch (main.js `backgroundColor: CONFIG.dark.bg` → "Cannot read
// properties of undefined (reading 'bg')", no usable window). The packaged app
// is the trap (its resolved config can differ from dev). Pentacle is dark-only;
// there is no light theme block.
test('withThemeDefaults backfills missing theme blocks (no .bg crash possible)', () => {
  const c = withThemeDefaults({ features: { chatUi: true } }, process.cwd() + '/');
  assert.ok(c.dark && typeof c.dark.bg === 'string', 'dark.bg present');
  assert.ok(c.terminal && typeof c.terminal === 'object', 'terminal block present');
  assert.equal(c.light, undefined, 'no light theme is backfilled (dark-only)');
});

test('withThemeDefaults leaves a config that already has all theme blocks unchanged', () => {
  const orig = { dark: { bg: '#111' }, terminal: { background: '#111' }, features: {} };
  const c = withThemeDefaults(orig, process.cwd() + '/');
  assert.equal(c.dark.bg, '#111');
  assert.equal(c.terminal.background, '#111');
});

test('withThemeDefaults fills the absent terminal block (partial config)', () => {
  const c = withThemeDefaults({ dark: { bg: '#abc' } }, process.cwd() + '/');
  assert.equal(c.dark.bg, '#abc', 'present dark kept');
  assert.ok(c.terminal && typeof c.terminal === 'object', 'absent terminal filled');
});

test('machineKey normalizes a public hostname deterministically', () => {
  assert.equal(machineKey('example.local'), 'example-local');
  assert.equal(machineKey('Example Local'), 'example-local');
});

test('config candidates prefer explicit, local, user, then bundled configuration', (t) => {
  const home = path.resolve('/private-home');
  t.mock.method(require('node:os'), 'homedir', () => home);
  const paths = candidateConfigPaths('/repo/public-desktop', {}, 'example.local');
  const base = path.resolve('/repo/public-desktop');
  const privateConfig = path.join(path.parse(base).root, 'private', 'config.js');
  assert.deepEqual(candidateConfigPaths(base, { PENTACLE_CONFIG: privateConfig }), [privateConfig]);

  assert.equal(paths[0], path.join(base, 'pentacle.config.js'));
  assert.equal(paths[1], path.join(home, '.config', 'pentacle', 'pentacle.config.js'));
  assert.equal(paths[2], path.join(base, 'pentacle.config.example.js'));
});

test('normal launches load the private user profile without a shell environment', (t) => {
  const fs = require('node:fs');
  const os = require('node:os');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pentacle-user-config-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const root = path.join(dir, 'app');
  const home = path.join(dir, 'home');
  const user = path.join(home, '.config', 'pentacle', 'pentacle.config.js');
  fs.mkdirSync(root, { recursive: true });
  fs.mkdirSync(path.dirname(user), { recursive: true });
  t.mock.method(os, 'homedir', () => home);
  const example = path.join(root, 'pentacle.config.example.js');
  const local = path.join(root, 'pentacle.config.js');
  fs.writeFileSync(example, 'module.exports = { features: { usage: false } };');
  assert.equal(loadConfig(root, {}).path, example, 'absent user config retains example fallback');
  fs.writeFileSync(user, 'module.exports = { features: { usage: true, mic: false } };');
  const loaded = loadConfig(root, {});
  assert.equal(loaded.path, user);
  assert.equal(loaded.config.features.usage, true, 'main process subscribes to quota updates');
  assert.equal(loaded.config.features.mic, false);
  fs.writeFileSync(local, 'module.exports = { features: { usage: false } };');
  assert.equal(loadConfig(root, {}).path, local, 'existing local overlays retain precedence');
  assert.equal(loadConfig(root, { PENTACLE_CONFIG: user }).path, user, 'explicit path is authoritative');
  assert.throws(() => loadConfig(root, { PENTACLE_CONFIG: path.join(dir, 'missing.js') }), /No Pentacle config found/);
});

test('a broken user profile fails visibly instead of silently using the example', (t) => {
  const fs = require('node:fs');
  const os = require('node:os');
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'pentacle-broken-user-config-'));
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  const user = path.join(dir, '.config', 'pentacle', 'pentacle.config.js');
  fs.mkdirSync(path.dirname(user), { recursive: true });
  fs.writeFileSync(user, 'throw new Error("broken private profile");');
  fs.writeFileSync(path.join(dir, 'pentacle.config.example.js'), 'module.exports = {};');
  t.mock.method(os, 'homedir', () => dir);
  assert.throws(() => loadConfig(dir, {}), /broken private profile/);
});

test('dashboards visibility and modeler settings are supported without exposing their values', () => {
  assert.deepEqual(configWarnings({ dashboards: { hidden: ['synthetic-retired'], showRetired: true,
    modeler3d: { url: 'http://127.0.0.1:9031/synthetic-viewer' } } }), []);
});
