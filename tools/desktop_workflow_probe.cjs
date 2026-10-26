'use strict';
const { BrowserWindow } = require('electron');
const assert = require('node:assert/strict');
const path = require('node:path');
const { until, preferences } = require('./desktop_isolation_probe.cjs');
const client = require('../main/chat_stream_client');
async function verifyPopouts(window, spawned) {
  const execute = code => window.webContents.executeJavaScript(code);
  const published = await client.sendCommand({ type: 'asset.publish', asset_id: 'isolation-smoke', stream_id: spawned.streamId,
    title: 'Isolation fixture asset', content_type: 'report', body: JSON.stringify({schema_version:1,title:'Safe asset',sections:[{id:'s1',title:'Desktop isolation fixture.',status:'reference',blocks:[]}]}) }, 'asset');
  assert.ok(published.asset, JSON.stringify(published));
  const args = { stream_id: spawned.streamId, asset_id: published.asset.asset_id, asset: published.asset };
  const opened = await execute(`window.cc.assetPopOut(${JSON.stringify(args)})`);
  assert.equal(opened.ok, true);
  const child = BrowserWindow.fromId(opened.windowId);
  try {
    await until(async () => !child.webContents.isLoading() && (await child.webContents.executeJavaScript('document.body.innerText')).includes('Desktop isolation fixture.'), 'asset popout render');
    preferences(child);
    assert.equal(await child.webContents.executeJavaScript('typeof require'), 'undefined');
    const finished = new Promise(resolve => child.webContents.once('did-finish-load', resolve));
    await child.webContents.executeJavaScript('window.cc.reloadApp()'); await finished;
    await until(async () => (await child.webContents.executeJavaScript('document.body.innerText')).includes('Desktop isolation fixture.'), 'asset reload/init');
    await child.webContents.executeJavaScript("document.getElementById('asset-popout-dock').click()");
    await until(() => child.isDestroyed(), 'asset dock');
  } finally { if (!child.isDestroyed()) child.destroy(); }
  // The public main does not implement chatPopOut. Exercise the retained
  // manager directly without claiming this unsupported UI action is enabled.
  const manager = require('../main/chat_popout_windows').createChatPopoutManager({ BrowserWindow,
    appRoot: path.resolve(__dirname, '..'), getMainWindow: () => window });
  try {
    const result = manager.open({ stream_id: spawned.streamId, host: spawned.hostId, session_name: spawned.sessionName });
    const chat = BrowserWindow.fromId(result.windowId);
    await until(async () => !chat.webContents.isLoading() && await chat.webContents.executeJavaScript('!!window.PentacleChatStore'), 'chat manager bootstrap');
    preferences(chat);
    assert.equal((await chat.webContents.executeJavaScript('window.cc.chatPopoutContext()')).stream_id, spawned.streamId);
    assert.equal((await chat.webContents.executeJavaScript('window.cc.getConfig()')).chatStream.tokenPath, undefined);
    assert.equal(await chat.webContents.executeJavaScript('typeof require'), 'undefined');
    assert.equal(manager.dock({ stream_id: spawned.streamId }).ok, true);
    await until(() => chat.isDestroyed(), 'chat manager dock');
  } finally { manager.closeAll(); }
  const list = await execute('window.cc.notificationList()'); assert.equal(list.ok, true);
  const schedule = await execute("window.cc.scheduleGet('isolation-smoke-missing')"); assert.equal(typeof schedule.ok, 'boolean');
  const mic = await execute("window.cc.micRequest('GET','/status')"); assert.equal(mic.ok, false);
  client.forceReconnect('isolation smoke');
  await until(() => client.connected && client._ws?.readyState === 1, 'authenticated reconnect');
  assert.equal((await execute('window.cc.getChatStreamState()')).connected, true);
  const loaded = new Promise(resolve => window.webContents.once('did-finish-load', resolve));
  await execute('window.cc.reloadApp()'); await loaded;
  await until(async () => await execute('!!window.PentacleChatStore && !!window.HOST && !!window.cc'), 'main reload');
  return { assetRendered: true, assetReloaded: true, assetDocked: true, chatManagerContext: true, chatManagerDocked: true,
    notificationTransport: true, scheduleTransport: true, micUnavailableExplicit: true, reconnected: true, mainReloaded: true };
}
module.exports = { verifyPopouts };
