'use strict';
// Host-side only. Never bundle this module or its credential into the renderer.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const http = require('node:http');

function micTokenPath(config, env = process.env) {
  const filename = config?.mic?.tokenPath || env.MIC_AUTH_TOKEN_FILE;
  const expanded = typeof filename === 'string' && filename.startsWith('~/')
    ? path.join(os.homedir(), filename.slice(2)) : filename;
  if (typeof expanded !== 'string' || !path.isAbsolute(expanded)) throw Error('Microphone credential is not configured.');
  return expanded;
}

function micAuthHeaders(config) {
  const filename = micTokenPath(config);
  if (process.platform === 'win32') throw Error('Microphone credentials require POSIX file permissions; use WSL.');
  let fd;
  try {
    fd = fs.openSync(filename, fs.constants.O_RDONLY | fs.constants.O_NOFOLLOW | fs.constants.O_NONBLOCK);
    const info = fs.fstatSync(fd);
    if (!info.isFile() || info.uid !== process.getuid() || (info.mode & 0o7777) !== 0o600 || info.size > 4096)
      throw Error('invalid credential file');
    const buffer = Buffer.alloc(4097);
    const token = buffer.subarray(0, fs.readSync(fd, buffer, 0, buffer.length, 0)).toString('utf8').trim();
    if (!/^[A-Za-z0-9_-]{32,256}$/.test(token)) throw Error('invalid credential');
    return { Authorization: `Bearer ${token}` };
  } catch {
    throw Error('Microphone credential must be an owned regular mode-0600 file containing a random token.');
  } finally {
    if (fd !== undefined) fs.closeSync(fd);
  }
}

function localMicUrl(value) {
  let url;
  try { url = new URL(value); } catch { throw Error('Microphone endpoint must be a loopback HTTP origin.'); }
  const hostname = url.hostname.replace(/^\[|\]$/g, '');
  if (url.protocol !== 'http:' || !(hostname === 'localhost' || hostname === '::1' || /^127(\.\d{1,3}){3}$/.test(hostname))
    || url.username || url.password || url.pathname !== '/' || url.search || url.hash || /[\\\s]/.test(value))
    throw Error('Microphone endpoint must be a loopback HTTP origin.');
  return url.origin;
}

function fetchMic(url, options = {}) {
  // Use a direct core HTTP connection. Global fetch dispatchers and environment
  // proxy settings must never receive this local service's bearer credential.
  return new Promise((resolve, reject) => {
    const request = http.request(url, { method: options.method || 'GET', headers: options.headers,
      signal: options.signal, agent: false }, response => {
      const chunks = [];
      let size = 0;
      response.on('data', chunk => {
        size += chunk.length;
        if (size > 16 * 1024 * 1024) response.destroy(Error('Microphone response is too large.'));
        else chunks.push(chunk);
      });
      response.on('error', reject);
      response.on('end', () => {
        const body = Buffer.concat(chunks);
        const status = response.statusCode;
        resolve({ status, ok: status >= 200 && status < 300,
          json: async () => JSON.parse(body.toString('utf8')) });
      });
    });
    request.on('error', reject);
    request.end(options.body);
  });
}

module.exports = { micAuthHeaders, micTokenPath, localMicUrl, fetchMic };
