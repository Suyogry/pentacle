'use strict';
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const { EventEmitter } = require('node:events');
const { pathToFileURL } = require('node:url');
const { createRequire } = require('node:module');
const root = path.resolve(__dirname, '../..');
const realRequire = createRequire(path.join(root, 'main.js'));
function loadMain(client = {}, config = {}) {
  const handlers = new Map(), instances = [];
  class Window extends EventEmitter {
    constructor(options) { super(); this.options = options; instances.push(this); this.webContents = new EventEmitter();
      Object.assign(this.webContents, { mainFrame: { url: '' }, isDestroyed: () => false,
        getURL: () => this.webContents.mainFrame.url, setWindowOpenHandler() {}, send() {}, reload() {} }); }
    isDestroyed() { return false; }
    loadFile(file) { this.webContents.mainFrame.url = pathToFileURL(file).href; return Promise.resolve(); }
    show() {}
    static getAllWindows() { return instances; }
  }
  const electron = { app: { setName() {}, on() {}, whenReady: () => ({ then: fn => fn() }) }, BrowserWindow: Window,
    ipcMain: { handle: (n, f) => handlers.set(n, f), on: (n, f) => handlers.set(n, f) }, shell: {}, clipboard: {} };
  vm.runInNewContext(fs.readFileSync(path.join(root, 'main.js'), 'utf8'), {
    require(name) {
      if (name === 'electron') return electron;
      if (name === './main/chat_stream_client') return { init() {}, ...client };
      if (name === './config-loader') return { loadConfig: () => ({ config }) };
      return realRequire(name);
    }, __dirname: root, process: { ...process, env: {} }, console, Buffer, URL,
  });
  const window = instances[0];
  const event = { sender: window.webContents, senderFrame: window.webContents.mainFrame };
  return { handlers, window, event, invoke: (name, ...args) => handlers.get(name)(event, ...args) };
}
module.exports = { loadMain };
