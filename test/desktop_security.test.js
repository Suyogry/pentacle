'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const { EventEmitter } = require('node:events');
const { pathToFileURL } = require('node:url');
const fs = require('node:fs');
const path = require('node:path');
const { createDesktopPolicy, desktopPreferences } = require('../main/desktop_security');
const { redactConfig } = require('../main/public_config');
function fixture() {
  const policy = createDesktopPolicy(), window = new EventEmitter(), sender = new EventEmitter();
  window.webContents = sender;
  sender.mainFrame = { url: pathToFileURL('/tmp/pentacle/desktop.html').href };
  sender.getURL = () => sender.mainFrame.url;
  sender.isDestroyed = () => false;
  sender.setWindowOpenHandler = fn => { sender.open = fn; };
  policy.own(window, '/tmp/pentacle/desktop.html');
  const handlers = new Map(); let effects = 0;
  const target = policy.guard({ handle: (n, fn) => handlers.set(n, fn), on: (n, fn) => handlers.set(n, fn) });
  target.handle('invoke', () => ++effects);
  target.on('send', () => ++effects);
  target.on('bootstrap', event => { event.returnValue = { config: {} }; ++effects; });
  return { policy, window, sender, handlers, effects: () => effects,
    event: () => ({ sender, senderFrame: sender.mainFrame }) };
}
test('guard permits only a live owned exact main-frame document for every IPC mode', () => {
  const f = fixture();
  assert.equal(f.handlers.get('invoke')(f.event()), 1);
  f.handlers.get('send')(f.event());
  const bootstrap = f.event(); f.handlers.get('bootstrap')(bootstrap);
  assert.deepEqual(bootstrap.returnValue, { config: {} });
  for (const mutation of [
    f => ({ ...f.event(), sender: { ...f.sender } }), // same URL, other WebContents
    f => ({ ...f.event(), senderFrame: { url: f.sender.mainFrame.url } }),
    f => ({ ...f.event(), senderFrame: undefined }),
    f => { f.sender.mainFrame.url += '?unexpected'; return f.event(); },
    f => { f.sender.getURL = () => 'file:///other.html'; return f.event(); },
    f => { f.sender.isDestroyed = () => true; return f.event(); },
    f => { f.window.emit('closed'); return f.event(); },
  ]) {
    const invalid = fixture(), e = mutation(invalid);
    assert.throws(() => invalid.handlers.get('invoke')(e), /Untrusted/);
    invalid.handlers.get('send')(e);
    invalid.handlers.get('bootstrap')(e);
    assert.match(e.returnValue.error, /Untrusted/);
    assert.equal(invalid.effects(), 0, 'denied request must not reach any handler');
  }
});
test('guard rejects deep/cyclic/oversized arguments before delegated effects', () => {
  const f = fixture(); const cycle = {}; cycle.self = cycle;
  let deep = {}; for (let n = 0; n < 66; n++) deep = { child: deep };
  for (const value of [cycle, deep, new Uint8Array(128 * 1024 * 1024 + 1)]) {
    assert.throws(() => f.handlers.get('invoke')(f.event(), value), /IPC input/);
    f.handlers.get('send')(f.event(), value);
  }
  assert.equal(f.effects(), 0);
});
test('window policy rejects navigation, subframe navigation, webviews and new windows', () => {
  const f = fixture();
  for (const name of ['will-navigate', 'will-frame-navigate', 'will-attach-webview']) {
    let denied = false; f.sender.emit(name, { preventDefault: () => { denied = true; } }); assert.equal(denied, true);
  }
  assert.deepEqual(f.sender.open({ url: 'https://example.com' }), { action: 'deny' });
  assert.deepEqual(desktopPreferences('/preload.js'), { preload: '/preload.js', nodeIntegration: false, contextIsolation: true, sandbox: true, webviewTag: false });
});
test('public config removes nested adapter credentials and URL credentials', () => {
  const value = redactConfig({ dashboardHub: { url: 'https://user:password@example.com/?token=hidden&view=board', token: 'hidden', password: 'hidden', nested: { apiKey: 'hidden' } }, features: { chatUi: true } });
  assert.equal(JSON.stringify(value).includes('hidden'), false);
  assert.equal(value.dashboardHub.url, 'https://example.com/?view=board');
  assert.equal(value.features.chatUi, true);
});
test('config shim returns a mutable copy of the frozen bridge config', () => {
  const vm = require('node:vm'); const context = { window: { __PENTACLE_CONFIG__: Object.freeze({ features: Object.freeze({ chatUi: true }) }) }, module: { exports: {} } };
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../renderer/shims/config_loader.js'), 'utf8'), context);
  const config = context.module.exports.loadConfig().config;
  config.features.chatUi = false;
  assert.equal(config.features.chatUi, false);
  assert.equal(context.window.__PENTACLE_CONFIG__.features.chatUi, true);
});
test('sandbox preload has only named capabilities and never passes Electron event objects', () => {
  const vm = require('node:vm'); const listeners = new Map(), window = {};
  vm.runInNewContext(fs.readFileSync(path.join(__dirname, '../preload.js'), 'utf8'), {
    process: { argv: [] }, require(name) {
      assert.equal(name, 'electron');
      return { contextBridge: { exposeInMainWorld: (key, val) => { window[key] = val; } }, ipcRenderer: {
        sendSync: () => ({ HOST: {}, config: {} }), invoke() {}, send() {}, removeAllListeners() {},
        on: (channel, fn) => listeners.set(channel, fn),
      } };
    },
  });
  assert.equal(window.cc.invoke, undefined); assert.equal(window.cc.send, undefined); assert.equal(window.cc.ipcRenderer, undefined);
  let received;
  window.cc.onChatStreamFrame((...args) => { received = args; });
  const frame = { type: 'chat.event' };
  listeners.get('chat-stream:frame')({ sender: 'privileged' }, frame);
  assert.deepEqual(received, [frame]);
});
