'use strict';

const { pathToFileURL } = require('node:url');

// One registry covers the main window and both popout managers. A matching URL
// alone never grants access: the main process must have created this window.
function createDesktopPolicy() {
  const documents = new Map();
  function trusted(sender, frame = sender?.mainFrame) {
    const expected = documents.get(sender);
    return !!expected && !sender.isDestroyed() && frame === sender.mainFrame
      && frame.url === expected && sender.getURL() === expected;
  }
  function own(window, file) {
    const sender = window.webContents;
    documents.set(sender, pathToFileURL(file).href);
    window.once('closed', () => documents.delete(sender));
    sender.setWindowOpenHandler(() => ({ action: 'deny' }));
    for (const event of ['will-navigate', 'will-frame-navigate', 'will-attach-webview']) {
      sender.on(event, (e) => e.preventDefault());
    }
  }
  function admit(event, args) {
    if (!event.senderFrame || !trusted(event.sender, event.senderFrame)) throw new Error('Untrusted desktop IPC sender');
    // Bound structured-clone input before any native/delegated handler runs.
    // This accommodates the existing blob/image paths without permitting
    // arbitrary deep or unbounded object graphs.
    let bytes = 0, nodes = 0;
    const seen = new Set();
    function visit(value, depth) {
      if (++nodes > 1000000 || depth > 64) throw new Error('Desktop IPC input too complex');
      if (typeof value === 'string') bytes += Buffer.byteLength(value);
      else if (value && typeof value === 'object') {
        if (seen.has(value)) throw new Error('Cyclic desktop IPC input');
        seen.add(value);
        if (ArrayBuffer.isView(value) || value instanceof ArrayBuffer) bytes += value.byteLength;
        else for (const [key, child] of Object.entries(value)) { bytes += Buffer.byteLength(key); visit(child, depth + 1); }
        seen.delete(value);
      }
      if (bytes > 128 * 1024 * 1024) throw new Error('Desktop IPC input too large');
    }
    visit(args, 0);
  }
  function guard(ipcMain) {
    return {
      handle(channel, handler) {
        ipcMain.handle(channel, (event, ...args) => { admit(event, args); return handler(event, ...args); });
      },
      on(channel, handler) {
        ipcMain.on(channel, (event, ...args) => {
          try { admit(event, args); } catch (_) {
            // sendSync bootstrap must always receive a response, even on deny.
            event.returnValue = { error: 'Untrusted desktop IPC request' };
            return;
          }
          return handler(event, ...args);
        });
      },
    };
  }
  return { own, trusted, guard };
}

function desktopPreferences(preload) {
  return { preload, nodeIntegration: false, contextIsolation: true, sandbox: true, webviewTag: false };
}

const desktopPolicy = createDesktopPolicy();
module.exports = { createDesktopPolicy, desktopPolicy, desktopPreferences };
