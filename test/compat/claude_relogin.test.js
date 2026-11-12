'use strict';

// Explicit opt-in: this launches the REAL provider with a disposable profile.
// No account login, browser navigation, callback code or token exchange occurs.
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const net = require('node:net');
const { createHash } = require('node:crypto');
const { spawnSync } = require('node:child_process');
const { EventEmitter } = require('node:events');
const { registerProviderRelogin } = require('../../main/provider_relogin');
const { quote } = require('../../main/execution_host');

const binary = process.env.CLAUDE_COMPAT_BIN;
const expectedVersion = process.env.CLAUDE_COMPAT_VERSION;

test('real Claude callback handoff, cancellation and timeout preserve logged-out isolation', {
  skip: !binary && 'Set CLAUDE_COMPAT_BIN and CLAUDE_COMPAT_VERSION to opt in',
  timeout: 45000,
}, async t => {
  assert.ok(['darwin', 'linux'].includes(process.platform), 'Requires POSIX native PTY and lsof');
  assert.ok(path.isAbsolute(binary), 'CLAUDE_COMPAT_BIN must be absolute');
  assert.match(expectedVersion || '', /^\d+\.\d+\.\d+$/, 'An exact expected CLI version is required');
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'claude-relogin-compat-'));
  const config = path.join(home, '.claude');
  fs.mkdirSync(config, { mode: 0o700 });
  // Do not inherit tokens, providers, proxies, debug selectors or Keychain names.
  // Both config selectors are unique: macOS derives its Keychain service from
  // this directory. Never use a user's normal HOME/config for this test.
  const env = {
    HOME: home, USER: 'pentacle_compat', LOGNAME: 'pentacle_compat',
    PATH: '/usr/bin:/bin:/usr/sbin:/sbin',
    CLAUDE_CONFIG_DIR: config, CLAUDE_SECURESTORAGE_CONFIG_DIR: config,
    DISABLE_TELEMETRY: '1', DISABLE_ERROR_REPORTING: '1',
    CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC: '1', TERM: 'dumb', NO_COLOR: '1',
    BROWSER: '/bin/echo',
  };
  const run = args => spawnSync(binary, args, { env, cwd: home, encoding: 'utf8', timeout: 10000 });
  const status = () => {
    const result = run(['--debug-file', '/dev/null', 'auth', 'status', '--json']);
    assert.equal(result.error, undefined, 'Real auth status must execute');
    let loggedIn;
    try { loggedIn = JSON.parse(result.stdout).loggedIn; } catch { assert.fail('Real auth status must return JSON'); }
    assert.equal(loggedIn, false, 'Disposable profile must remain logged out');
    assert.equal(result.status, 1, 'Logged-out status must fail');
  };
  t.after(() => fs.rmSync(home, { recursive: true, force: true }));
  const version = run(['--version']);
  assert.equal(version.status, 0, 'Real CLI must launch');
  assert.ok(version.stdout.trim() === `${expectedVersion} (Claude Code)`, 'CLI version must match exactly');
  t.diagnostic(`Claude ${expectedVersion}; ${process.platform}/${process.arch}; Node ${process.version}; SHA256 ${createHash('sha256').update(fs.readFileSync(binary)).digest('hex')}`);
  status();

  // Keep the production login flags and shell/PTY/exit-receipt machinery. Only
  // resolve the provider executable to an env-isolated launcher of the real CLI.
  const launcher = path.join(home, 'claude-real');
  fs.writeFileSync(launcher, '#!/bin/sh\nexec /usr/bin/env -i '
    + Object.entries(env).map(([k, v]) => `${k}=${quote(v)}`).join(' ')
    + ` ${quote(binary)} "$@"\n`, { mode: 0o700 });
  const native = require('node-pty');
  const lsof = process.platform === 'darwin' ? '/usr/sbin/lsof' : 'lsof';
  const ownedListeners = pid => {
    const result = spawnSync('ps', ['-A', '-o', 'pid=,ppid='], { encoding: 'utf8' });
    assert.equal(result.status, 0, 'Must enumerate owned descendants');
    const rows = result.stdout.trim().split('\n').map(line => line.trim().split(/\s+/).map(Number));
    const owned = new Set([pid]);
    for (let changed = true; changed;) {
      changed = false;
      for (const [child, parent] of rows) if (owned.has(parent) && !owned.has(child)) { owned.add(child); changed = true; }
    }
    const ports = [];
    for (const child of owned) {
      const sockets = spawnSync(lsof, ['-nP', '-a', '-p', String(child), '-iTCP', '-sTCP:LISTEN', '-Fn'], { encoding: 'utf8' });
      assert.equal(sockets.error, undefined, 'lsof is required for listener ownership proof');
      assert.ok([0, 1].includes(sockets.status), 'lsof must execute successfully');
      for (const line of sockets.stdout.split('\n')) {
        const match = line.match(/^n127\.0\.0\.1:(\d+)$/);
        if (match) ports.push(Number(match[1]));
      }
    }
    return ports;
  };
  const closed = port => new Promise(resolve => {
    const socket = net.connect({ host: '127.0.0.1', port });
    socket.setTimeout(1000);
    socket.once('connect', () => { socket.destroy(); resolve(false); });
    socket.once('error', error => { socket.destroy(); resolve(error.code === 'ECONNREFUSED'); });
    socket.once('timeout', () => { socket.destroy(); resolve(false); });
  });

  for (const mode of ['cancel', 'timeout']) {
    let proc;
    let resolveBrowser;
    const browser = new Promise(resolve => { resolveBrowser = resolve; });
    let resolveTerminal;
    const terminal = new Promise(resolve => { resolveTerminal = resolve; });
    const events = [], logs = [];
    const sender = new EventEmitter();
    sender.id = mode;
    sender.isDestroyed = () => false;
    sender.send = (_channel, event) => {
      events.push(event);
      if (event.state === 'awaiting_browser') resolveBrowser(event);
      if (['failed', 'succeeded', 'cancelled', 'timed_out', 'cleanup_failed'].includes(event.state)) resolveTerminal(event);
    };
    const table = {};
    const pty = { spawn(file, args, options) {
      assert.equal(file, '/bin/bash');
      assert.equal(args.at(-1).split("'claude'").length, 2, 'Replace only the provider executable');
      assert.ok(args.at(-1).includes('BROWSER=' + quote('/bin/echo')), 'Production flow must suppress automatic browser navigation');
      proc = native.spawn(file, [...args.slice(0, -1), args.at(-1).replace("'claude'", quote(launcher))], { ...options, env, cwd: home });
      return proc;
    } };
    // The timeout case accelerates the five-minute production deadline. It
    // proves the cleanup path, not five minutes of wall-clock endurance.
    const stop = registerProviderRelogin({ handle: (key, fn) => { table[key] = fn; } },
      { chatStream: { localHost: 'compat' } }, { pty, env, cwd: home, log: v => logs.push(v),
        ...(mode === 'timeout' ? { timeoutMs: 4000 } : {}), cleanupMs: 3000 });
    try {
      assert.equal(table['provider-relogin:start']({ sender }, {
        id: `real_compat_${mode}_123`, provider: 'claude', host: 'local', available: true,
      }).ok, true);
      let timer;
      const event = await Promise.race([browser, new Promise(resolve => { timer = setTimeout(() => resolve(null), 10000); })]);
      clearTimeout(timer);
      const ports = ownedListeners(proc.pid);
      assert.ok(ports.length > 0, 'Real Claude must open an owned localhost listener');
      assert.ok(event, 'Real CLI must reach awaiting_browser (old endpoint allowlist fails here)');
      const url = new URL(event.url);
      assert.ok(url.protocol === 'https:' && url.searchParams.has('state') && url.searchParams.has('client_id')
        && url.searchParams.has('code_challenge'), 'Real handoff must include a complete OAuth URL');
      for (const value of [event.url, url.searchParams.get('state'), url.searchParams.get('code_challenge')]) {
        assert.ok(value && !JSON.stringify(logs).includes(value), 'Authorization material must not reach telemetry');
      }
      assert.ok(!events.some(value => value.state === 'succeeded'), 'Browser handoff alone must not succeed');
      if (mode === 'cancel') await table['provider-relogin:cancel']({ sender }, `real_compat_${mode}_123`);
      const end = await terminal;
      assert.equal(end.state, mode === 'cancel' ? 'cancelled' : 'timed_out');
      assert.equal(end.reason, mode === 'cancel' ? 'operator_cancel' : 'login_timeout');
      assert.ok(!Object.hasOwn(end, 'url'), 'Terminal event must clear its URL');
      for (const port of ports) assert.ok(await closed(port), 'Owned callback listener must close');
      status();
    } finally {
      const cleanup = await stop();
      // Keep transient auth output only in memory, including on assertion failure.
      events.length = 0;
      logs.length = 0;
      assert.ok(cleanup.every(result => result.ok), 'Controller must confirm cleanup even after a failed assertion');
    }
  }
});
