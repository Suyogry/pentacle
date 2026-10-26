'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');
const { micAuthHeaders, localMicUrl } = require('../main/mic_auth');
const { createMicRequest } = require('../main/mic_request');
const { createCcHandlers } = require('../main/cc_handlers');
const { main } = require('../server/index');

function credential(t) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'mic-security-'));
  const filename = path.join(dir, 'mic.token');
  const token = 'synthetic-private-microphone-token-' + 'x'.repeat(32);
  fs.writeFileSync(filename, token, { mode: 0o600 });
  t.after(() => fs.rmSync(dir, { recursive: true, force: true }));
  return { dir, filename, token, config: { features: { mic: true }, mic: { tokenPath: filename } } };
}

test('credential files must be private, regular and valid; replacements are reread', t => {
  const { dir, filename, token, config } = credential(t);
  assert.equal(micAuthHeaders(config).Authorization, 'Bearer ' + token);
  fs.writeFileSync(filename, 'z'.repeat(43));
  assert.equal(micAuthHeaders(config).Authorization, 'Bearer ' + 'z'.repeat(43));
  fs.chmodSync(filename, 0o644);
  assert.throws(() => micAuthHeaders(config), /mode-0600/);
  fs.chmodSync(filename, 0o600);
  const link = path.join(dir, 'link'); fs.symlinkSync(filename, link);
  assert.throws(() => micAuthHeaders({ mic: { tokenPath: link } }), /mode-0600/);
  assert.throws(() => micAuthHeaders({ mic: { tokenPath: dir } }), /mode-0600/);
  fs.writeFileSync(filename, 'too-short');
  assert.throws(() => micAuthHeaders(config), /mode-0600/);
});

test('remote or ambiguous destinations are rejected before sending credentials', async t => {
  const { config } = credential(t);
  let calls = 0;
  for (const value of ['https://127.0.0.1:7780', 'http://attacker.example:7780', 'http://127.0.0.1.attacker.example',
    'http://user@127.0.0.1:7780', 'http://127.0.0.1:7780/path', 'http://127.0.0.1:7780?query', 'http://127.0.0.1:7780#fragment']) {
    assert.throws(() => localMicUrl(value));
    assert.equal(await createMicRequest({ ...config, micServerUrl: value }, () => { calls++; })('GET', '/status'), null);
  }
  assert.equal(calls, 0);
});

test('mic credentials and launcher never enter public configuration', t => {
  const { config, filename, token } = credential(t);
  config.mic.token = token;
  config.mic.startCommand = { file: '/private/helper', args: [] };
  const data = JSON.stringify(createCcHandlers({ CONFIG: config, chatStreamClient: {} }).publicConfig());
  for (const secret of [token, filename, '/private/helper', 'tokenPath']) assert.ok(!data.includes(secret));
});

test('a web host with mic enabled refuses unauthenticated operation before allocating transports', async t => {
  const { dir, config } = credential(t);
  const profile = path.join(dir, 'profile.js');
  fs.writeFileSync(profile, 'module.exports=' + JSON.stringify(config));
  await assert.rejects(main(['--profile', profile, '--port', '0']), /require web authentication/);
});

test('redirects cannot forward the mic credential to another endpoint', async t => {
  const { config } = credential(t);
  let leaked = 0;
  const target = http.createServer((_req, res) => { leaked++; res.end('{}'); });
  await new Promise(resolve => target.listen(0, '127.0.0.1', resolve));
  const source = http.createServer((_req, res) => {
    res.writeHead(302, { location: `http://127.0.0.1:${target.address().port}/status` }).end();
  });
  await new Promise(resolve => source.listen(0, '127.0.0.1', resolve));
  try {
    assert.equal(await createMicRequest({ ...config, micServerUrl: `http://127.0.0.1:${source.address().port}` })('GET', '/status'), null);
    assert.equal(leaked, 0);
  } finally {
    await Promise.all([new Promise(resolve => target.close(resolve)), new Promise(resolve => source.close(resolve))]);
  }
});

test('renderer mic entrypoints have no direct HTTP fallback', () => {
  const app = fs.readFileSync(path.join(__dirname, '../renderer/app.js'), 'utf8');
  const meeting = fs.readFileSync(path.join(__dirname, '../renderer/meeting.html'), 'utf8');
  assert.doesNotMatch(app, /fetch\(MIC_API|const MIC_API|resolveMicUrl/);
  assert.doesNotMatch(meeting, /fetch\(|7780/);
  assert.match(meeting, /cc\.micRequest/);
});
