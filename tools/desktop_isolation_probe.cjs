'use strict';
// Called only by the disposable public desktop smoke, never by the product.
const { BrowserWindow, ipcMain } = require('electron');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { desktopPolicy, desktopPreferences } = require('../main/desktop_security');
const delay = ms => new Promise(r => setTimeout(r, ms));
async function until(check, label) {
  for (let n = 0; n < 100; n++) { if (await check()) return; await delay(50); }
  throw new Error('Isolation probe timed out: ' + label);
}
function preferences(window) {
  const p = window.webContents.getLastWebPreferences();
  assert.equal(p.nodeIntegration, false); assert.equal(p.contextIsolation, true); assert.equal(p.sandbox, true);
}
async function verifyDesktopIsolation(window, root) {
  const execute = code => window.webContents.executeJavaScript(code);
  preferences(window);
  const globals = await execute('({require:typeof require,process:typeof process,Buffer:typeof Buffer,ipc:typeof window.cc.invoke,send:typeof window.cc.send,frozen:Object.isFrozen(window.__PENTACLE_CONFIG__),host:!!window.HOST.hostname})');
  assert.deepEqual(globals, { require: 'undefined', process: 'undefined', Buffer: 'undefined', ipc: 'undefined', send: 'undefined', frozen: true, host: true });
  const config = await execute('window.cc.getConfig()');
  assert.equal(config.chatStream.tokenPath, undefined);
  assert.equal(config.mic?.token, undefined);
  assert.equal(JSON.stringify(config).includes('fixture-adapter-secret'), false);
  // This is a real settings handler mutating the UI's private configuration copy.
  assert.equal(await execute(`(()=>{document.querySelector('#settings-default-view-row [data-value="terminal"]').click();return document.querySelector('#settings-default-view-row [data-value="terminal"]').getAttribute('aria-pressed')})()`), 'true');
  await execute(`document.querySelector('#settings-default-view-row [data-value="chat"]').click()`);
  const csp = await execute(`new Promise(resolve=>{
    window.__unsafeInline=false;window.__unsafeEval=false;window.__unsafeFunction=false;
    const script=document.createElement('script');script.textContent='window.__unsafeInline=true';document.body.append(script);
    try{eval('window.__unsafeEval=true')}catch(_){}
    try{new Function('window.__unsafeFunction=true')()}catch(_){}
    setTimeout(()=>resolve({inline:window.__unsafeInline,eval:window.__unsafeEval,fn:window.__unsafeFunction}),100);
  })`);
  assert.deepEqual(csp, { inline: false, eval: false, fn: false });
  let opened = 0;
  const onCreated = () => { opened++; };
  window.webContents.on('did-create-window', onCreated);
  await execute(`window.open('https://example.invalid/')`);
  await delay(100); window.webContents.removeListener('did-create-window', onCreated);
  assert.equal(opened, 0);
  const original = window.webContents.getURL();
  await execute(`location.href='https://example.invalid/'`);
  await delay(100); assert.equal(window.webContents.getURL(), original);

  // An unowned window gets no production bridge even at the exact same URL.
  const unowned = new BrowserWindow({ show: false, webPreferences: desktopPreferences(path.resolve(__dirname, '../preload.js')) });
  try {
    await unowned.loadURL(original);
    assert.equal(await unowned.webContents.executeJavaScript('typeof window.cc'), 'undefined');
  } finally { unowned.destroy(); }

  // Real IPC from same-URL strangers, a registered wrong document and a child
  // frame. Diagnostic preload exists only in this private test directory.
  const preload = path.join(root, 'ipc-probe.cjs');
  const page = path.join(root, 'ipc-probe.html');
  fs.writeFileSync(preload, `const {ipcRenderer}=require('electron');\n(async()=>{let accepted=false,error='';try{await ipcRenderer.invoke('get-config');accepted=true}catch(e){error=String(e)}ipcRenderer.send('isolation-test:receipt',{main:process.isMainFrame,accepted,error,url:location.href,bootstrap:ipcRenderer.sendSync('desktop:bootstrap')?.error||null})})()`);
  fs.writeFileSync(page, '<!doctype html><title>IPC transport probe</title><iframe src="ipc-child.html"></iframe>');
  fs.writeFileSync(path.join(root, 'ipc-child.html'), '<!doctype html><title>Child</title>');
  const receipts = [];
  const listener = (event, receipt) => receipts.push({ sender: event.sender, ...receipt });
  ipcMain.on('isolation-test:receipt', listener);
  const probes = [];
  try {
    const stranger = new BrowserWindow({ show: false, webPreferences: desktopPreferences(preload) }); probes.push(stranger);
    await stranger.loadURL(original);
    await until(() => receipts.some(r => r.sender === stranger.webContents), 'same URL stranger');
    assert.equal(receipts.find(r => r.sender === stranger.webContents).accepted, false);
    const wrong = new BrowserWindow({ show: false, webPreferences: desktopPreferences(preload) }); probes.push(wrong);
    desktopPolicy.own(wrong, path.resolve(__dirname, '../renderer/dist/desktop/desktop.html'));
    await wrong.loadFile(page);
    await until(() => receipts.some(r => r.sender === wrong.webContents), 'wrong document');
    assert.equal(receipts.find(r => r.sender === wrong.webContents).accepted, false);
    const framed = new BrowserWindow({ show: false, webPreferences: { ...desktopPreferences(preload), nodeIntegrationInSubFrames: true } }); probes.push(framed);
    desktopPolicy.own(framed, page);
    // Transport fixture allows a child to load; production windows deny this.
    framed.webContents.removeAllListeners('will-frame-navigate');
    await framed.loadFile(page);
    await until(() => receipts.some(r => r.sender === framed.webContents && !r.main), 'child frame');
    assert.equal(receipts.find(r => r.sender === framed.webContents && r.main).accepted, true);
    assert.equal(receipts.find(r => r.sender === framed.webContents && !r.main).accepted, false);
    for (const r of receipts.filter(r => !r.accepted)) assert.match(r.error, /Untrusted desktop IPC sender/);
  } finally {
    for (const probe of probes) if (!probe.isDestroyed()) probe.destroy();
    ipcMain.removeListener('isolation-test:receipt', listener);
  }
  return { globals, csp, unexpectedNavigationBlocked: true, newWindowBlocked: true, unownedBridgeDenied: true,
    ipc: receipts.map(({ main, accepted, error }) => ({ main, accepted, error })) };
}
module.exports = { verifyDesktopIsolation, preferences, until };
