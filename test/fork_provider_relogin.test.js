'use strict';
// This fork retains its corrected Settings sign-in flow. Reconcile upstream's
// removal-only assertions with that supported consumer and keep its unknown
// method negative control plus same-origin admission.
const test = require('node:test');
const assert = require('node:assert/strict');
const { buildCc } = require('../renderer/web_cc');
const { createCcHandlers, createCollector } = require('../main/cc_handlers');
const { createWsBridge } = require('../server/ws_bridge');

test('web sign-in capabilities remain available to the retained Settings UI', () => {
  const transport = { call: async () => ({}), fire() {}, on() {}, onReconnect() {} };
  const cc = buildCc(transport, { clipboard: {}, config: {} });
  assert.deepEqual(Object.keys(cc).filter(key => /relogin/i.test(key)).sort(),
    ['onReloginState', 'reloginCancel', 'reloginCode', 'reloginHosts', 'reloginStart'].sort());
});

test('retained sign-in handlers require origin admission and refuse unknown methods', async t => {
  const collector = createCollector();
  const stop = createCcHandlers({ CONFIG: { chatStream: { localHost: 'fixture' } }, chatStreamClient: {} }).register(collector);
  const bridge = createWsBridge({ table: collector.table });
  const replies = [];
  const socket = { send: raw => replies.push(JSON.parse(raw)) };
  t.after(async () => { bridge.closeAll(); await stop(); });
  bridge.addSocket(socket);
  await bridge.handleMessage(socket, JSON.stringify({ id: 1, method: 'provider-relogin:hosts', args: [] }));
  assert.equal(replies.pop().error.code, 'relogin_origin_refused');
  bridge.removeSocket(socket);
  bridge.addSocket(socket, { reloginAllowed: true });
  await bridge.handleMessage(socket, JSON.stringify({ id: 2, method: 'provider-relogin:hosts', args: [] }));
  const admitted = replies.pop();
  assert.equal(admitted.ok, true);
  assert.equal(admitted.result.ok, true);
  assert.ok(Array.isArray(admitted.result.hosts));
  await bridge.handleMessage(socket, JSON.stringify({ id: 3, method: 'provider-relogin:unrecognized', args: [] }));
  assert.equal(replies.pop().error.code, 'unknown_method');
});
