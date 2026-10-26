'use strict';
const vm = require('node:vm');
const assert = require('node:assert/strict');

// Test the real preload with Electron's sandbox-only require contract.
function run(source, context, options) {
  const originalRequire = context.require;
  context.require = name => {
    assert.equal(name, 'electron', 'sandboxed preload must not load Node or local modules');
    const electron = originalRequire(name);
    return { ...electron,
      contextBridge: { exposeInMainWorld: (name, value) => { context.window[name] = value; } },
      ipcRenderer: { ...electron.ipcRenderer, sendSync(channel) {
        assert.equal(channel, 'desktop:bootstrap');
        return { config: { features: {}, hostname: 'fixture' }, HOST: { hostname: 'fixture' } };
      } },
    };
  };
  return vm.runInNewContext(source, context, options);
}
module.exports = { run };
