'use strict';
const { app, BrowserWindow } = require('electron');
const fs = require('node:fs');
const path = require('node:path');
const root = process.env.PENTACLE_SMOKE_ROOT;
if (!root || !/^\d+$/.test(process.env.PENTACLE_SMOKE_PID || '')) throw new Error('Run tools/public_desktop_smoke.py');
process.env.PENTACLE_CONFIG = path.join(root, 'pentacle.config.js');
app.setPath('userData', path.join(root, 'electron-profile'));
require('../main.js');
const { verifyDesktopIsolation, preferences, until } = require('./desktop_isolation_probe.cjs');
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
const timeout = setTimeout(() => { console.error('Smoke timed out'); app.exit(1); }, 90000);
app.whenReady().then(async () => {
  try {
    let win;
    for (let i = 0; i < 150; i++) {
      win = BrowserWindow.getAllWindows()[0];
      if (win && !win.webContents.isLoading() && await win.webContents.executeJavaScript('!!window.PentacleChatStore')) break;
      await wait(100);
    }
    win.webContents.on('console-message', event => console.log('RENDERER:', event.message));
    const execute = code => win.webContents.executeJavaScript(`(async()=>{try{return await (${code})}catch(e){return {smokeError:e.stack||String(e)}}})()`).then(result=>{if(result?.smokeError)throw new Error(result.smokeError);return result;});
    for (let i = 0; i < 100; i++) {
      if ((await execute('window.cc.getChatStreamState()')).connected) break;
      await wait(100);
    }
    let terminalOutput = '';
    const send = win.webContents.send.bind(win.webContents);
    win.webContents.send = (channel, ...args) => { if (channel === 'pty:data') terminalOutput += String(args[1] || ''); return send(channel, ...args); };
    const isolation = await verifyDesktopIsolation(win, root);
    const spawned = await execute("window.PentacleHarnessActions.spawnThrowaway({hostId:'local',provider:'claude',model:'claude-opus-4-8',effort:'high'})");
    if (!spawned?.sessionName) throw new Error('The UI did not return a real session');
    await until(() => terminalOutput.includes('READY'), 'real native terminal output');
    await execute(`document.querySelector('[data-slot="${spawned.slot}"][data-mode="chat"]').click()`);
    let ready = false;
    for (let i = 0; i < 200; i++) {
      const state = await execute('window.cc.getChatStreamState()');
      ready = state.sessions.some((session) => session.stream_id === spawned.streamId && session.bootstrap_state === 'ready');
      if (ready) break;
      await wait(100);
    }
    if (!ready) throw new Error('Spawn never reached ready inventory');
    const marker = 'public-smoke-' + Date.now();
    const sent = await execute(`window.cc.chatSend('local',${JSON.stringify(spawned.sessionName)},${JSON.stringify(marker)})`);
    if (!sent.ok) throw new Error('Send was rejected: ' + sent.error);
    let rendered = false;
    for (let i = 0; i < 200; i++) {
      rendered = (await execute('document.body.innerText')).includes('Public fixture assistant: ' + marker);
      if (rendered) break;
      await wait(100);
    }
    if (!rendered) throw new Error('Actual assistant transcript is missing from the DOM');
    await until(() => terminalOutput.includes(marker), 'terminal response');
    const workflows = await require('./desktop_workflow_probe.cjs').verifyPopouts(win, spawned);
    await execute(`window.focusStreamId(${JSON.stringify(spawned.streamId)})`);
    await execute(`document.querySelector('[data-slot="${spawned.slot}"][data-mode="chat"]').click()`);
    await until(async () => (await execute('document.body.innerText')).includes('Public fixture assistant: ' + marker), 'restored chat');
    fs.writeFileSync(path.join(root, 'desktop.png'), (await win.webContents.capturePage()).toPNG());
    process.kill(Number(process.env.PENTACLE_SMOKE_PID), 'SIGTERM');
    for (let i = 0; i < 100; i++) {
      if (!(await execute('window.cc.getChatStreamState()')).connected) break;
      await wait(100);
    }
    const failed = await execute(`window.cc.chatSend('local',${JSON.stringify(spawned.sessionName)},'must not be fabricated')`);
    if (failed.ok !== false || !failed.error) throw new Error('Disconnected send must fail explicitly');
    fs.writeFileSync(path.join(root, 'proof.json'), JSON.stringify({ isolation, workflows, terminalOutputVerified: true, spawned, marker, assistantRendered: rendered, disconnectedRejected: true }, null, 2));
    console.log('PUBLIC_DESKTOP_SMOKE_PASS');
    clearTimeout(timeout); app.exit(0);
  } catch (error) {
    console.error(error); clearTimeout(timeout); app.exit(1);
  }
});
