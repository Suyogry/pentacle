'use strict';

// Backend credentials belong to the host, including optional adapter fields.
// Keep this projection shared by desktop bootstrap, get-config and the web UI.
function redactConfig(value) {
  if (Array.isArray(value)) return value.map(redactConfig);
  if (!value || typeof value !== 'object') return value;
  const out = {};
  for (const [key, child] of Object.entries(value)) {
    if (/token|password|secret|credential|api.?key|authorization|private.?key/i.test(key)) continue;
    if (typeof child === 'string' && /url$/i.test(key)) {
      try {
        const url = new URL(child);
        url.username = ''; url.password = '';
        for (const name of [...url.searchParams.keys()]) {
          if (/token|password|secret|credential|key|authorization/i.test(name)) url.searchParams.delete(name);
        }
        out[key] = (url.href !== new URL(child).href) ? url.href : child;
        continue;
      } catch (_) { /* Non-URL presentation strings retain their existing form. */ }
    }
    out[key] = redactConfig(child);
  }
  return out;
}

module.exports = { redactConfig };
