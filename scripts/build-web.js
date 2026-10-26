#!/usr/bin/env node
'use strict';

// Shared browser build for the web host and isolated Electron desktop.
//   node scripts/build-web.js [--desktop] [--minify]
// Both pages derive from the same markup and classic-script ordering.

const fs = require('fs');
const path = require('path');
const esbuild = require('esbuild');

const ROOT = path.join(__dirname, '..');
const RENDERER = path.join(ROOT, 'renderer');
const OUT = path.join(RENDERER, 'dist', 'web');

// Stylesheets index.html pulls from outside renderer/ are copied in beside the
// bundle; the rest are copied from renderer/ under the same relative name.
const EXTERNAL_CSS = {
  '../node_modules/@xterm/xterm/css/xterm.css': 'xterm.css',
};

// Scripts that stay <script src> tags instead of entering the bundle. They are
// already browser-ready IIFEs/UMDs that publish window globals, and a bundler's
// CommonJS wrapper is exactly what breaks them: a UMD sees `module.exports` and
// assigns there instead of to `window`, so `window.TriforceDashboards` and
// `window.PentacleChatCore` would silently never appear. Keeping them external
// also keeps them byte-identical to what Electron loads.
const EXTERNAL_SCRIPTS = {
  'confirm_dialog.js': 'confirm_dialog.js',
  'dashboards/registry.js': 'dashboards-registry.js',
  'dashboards/demo.js': 'dashboards-demo.js',
  'dashboards/catalog_loader.js': 'dashboards-catalog-loader.js',
  'dashboards/report_board.js': 'dashboards-report-board.js',
  'dist/chat_core.bundle.js': 'chat_core.bundle.js',
  'dist/cosmic_tokens.bundle.js': 'cosmic_tokens.bundle.js',
  'dist/cosmic_components.bundle.js': 'cosmic_components.bundle.js',
};

// The bundle takes this tag's place in the document, so everything it contains
// runs exactly where app.js ran.
const BUNDLE_ANCHOR = 'app.js';

// `../config-loader` reads the config off disk in the Electron preload; in a
// browser the host injects the computed config, so it maps to the shim. esbuild
// cannot infer that from the filesystem, hence the resolve hook.
function rendererResolvePlugin() {
  return {
    name: 'pentacle-renderer-resolve',
    setup(build) {
      build.onResolve({ filter: /[\/]dashboards[\/](catalog_loader|report_board)$/ }, args => ({ path: args.path.endsWith('catalog_loader') ? 'DashboardCatalogLoader' : 'DashboardReportBoard', namespace: 'dashboard-global' }));
      build.onLoad({ filter: /.*/, namespace: 'dashboard-global' }, args => ({ contents: `module.exports = window.${args.path};`, loader: 'js' }));
      build.onResolve({ filter: /(^|\/)config-loader$/ }, () => ({
        path: path.join(RENDERER, 'shims', 'config_loader.js'),
      }));
    },
  };
}

function readIndexHtml() {
  return fs.readFileSync(path.join(RENDERER, 'index.html'), 'utf8');
}

/** Every `<script src="…">` in index.html, in document order. */
function scriptSources(html) {
  return [...html.matchAll(/<script\s+src="([^"]+)"\s*>\s*<\/script>/g)].map((m) => m[1]);
}

/** Every `<link rel="stylesheet" href="…">` in index.html, in document order. */
function styleSources(html) {
  return [...html.matchAll(/<link\s+rel="stylesheet"\s+href="([^"]+)"\s*>/g)].map((m) => m[1]);
}

function buildHtml(html) {
  let out = html;
  for (const src of scriptSources(html)) {
    const tag = new RegExp(`[ \\t]*<script\\s+src="${src.replace(/[.*+?^${}()|[\\]\\\\]/g, '\\\\$&')}"\\s*></script>\\n?`);
    if (EXTERNAL_SCRIPTS[src]) out = out.replace(`src="${src}"`, `src="${EXTERNAL_SCRIPTS[src]}"`);
    else if (src === BUNDLE_ANCHOR) out = out.replace(tag, '  <script src="bundle.js"></script>\n');
    else out = out.replace(tag, '');
  }
  for (const [href, local] of Object.entries(EXTERNAL_CSS)) {
    out = out.split(`href="${href}"`).join(`href="${local}"`);
  }
  return out.replace('</head>', '  <!--PENTACLE_CONFIG-->\n</head>');
}

function buildAssetPopoutHtml(html) {
  return html.replace('<script src="asset_popout.js"></script>', '<script src="asset-popout.bundle.js"></script>')
    .replace('</head>', '  <!--PENTACLE_CONFIG-->\n</head>');
}

function copyExternalScripts(out = OUT) {
  for (const [src, local] of Object.entries(EXTERNAL_SCRIPTS)) {
    fs.copyFileSync(path.resolve(RENDERER, src), path.join(out, local));
  }
}

// Icons referenced from <link rel="icon"> / apple-touch-icon are copied next to the page.
function copyIcons(html, out = OUT) {
  const refs = [];
  for (const m of html.matchAll(/<link[^>]+rel="(?:icon|apple-touch-icon|manifest)"[^>]+href="([^"]+)"/g)) refs.push(m[1]);
  // A web app manifest lists its own icons; ship those too so the page is installable.
  for (const ref of refs.filter((r) => r.endsWith('.webmanifest'))) {
    const manifest = JSON.parse(fs.readFileSync(path.resolve(RENDERER, ref), 'utf8'));
    for (const icon of manifest.icons || []) refs.push(icon.src);
  }
  for (const m of refs.map((r) => [null, r])) {
    const from = path.resolve(RENDERER, m[1]);
    const to = path.join(out, m[1]);
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.copyFileSync(from, to);
  }
}

function copyStyles(html, out = OUT) {
  for (const href of styleSources(html)) {
    const local = EXTERNAL_CSS[href] || href;
    const from = path.resolve(RENDERER, href);
    const to = path.join(out, local);
    fs.mkdirSync(path.dirname(to), { recursive: true });
    fs.copyFileSync(from, to);
  }
}

const PREREQ_BUNDLES = [
  ['renderer/src/chat_core_entry.ts', 'renderer/dist/chat_core.bundle.js'],
  ['renderer/src/cosmic_tokens_entry.ts', 'renderer/dist/cosmic_tokens.bundle.js'],
  ['renderer/src/cosmic_components_entry.ts', 'renderer/dist/cosmic_components.bundle.js'],
];

// index.html loads these as plain <script src> tags, so the web bundle can only
// inline them once they exist. Same invocation as the npm build:* scripts.
async function buildPrereqBundles() {
  for (const [entry, outfile] of PREREQ_BUNDLES) {
    await esbuild.build({
      entryPoints: [path.join(ROOT, entry)],
      bundle: true,
      format: 'iife',
      target: 'chrome134',
      outfile: path.join(ROOT, outfile),
      logLevel: 'warning',
    });
  }
}

const DESKTOP_CSP = "default-src 'none'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; font-src 'self' data:; media-src 'self' blob:; connect-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'";

function desktopHtml(html) {
  return html.replace('<!--PENTACLE_CONFIG-->', '').replace('<head>', `<head>\n  <meta http-equiv="Content-Security-Policy" content="${DESKTOP_CSP}">`);
}

async function build({ minify = false, desktop = false } = {}) {
  const out = desktop ? path.join(RENDERER, 'dist', 'desktop') : OUT;
  await buildPrereqBundles();
  fs.rmSync(out, { recursive: true, force: true });
  fs.mkdirSync(out, { recursive: true });

  await esbuild.build({
    entryPoints: [path.join(RENDERER, desktop ? 'app.js' : 'web_entry.js')],
    bundle: true,
    format: 'iife',
    target: 'chrome134',
    platform: 'browser',
    outfile: path.join(out, 'bundle.js'),
    sourcemap: true,
    minify,
    // The renderer's only Node dependencies. Everything else it requires is
    // already browser-safe (xterm, the renderer modules, main/mic-url).
    alias: {
      path: path.join(RENDERER, 'shims', 'path.js'),
    },
    plugins: [rendererResolvePlugin()],
    define: {
      // app.js does `path.join(__dirname, '..')` purely to locate the config
      // root; the shimmed loader ignores the argument.
      __dirname: '"/"',
      __filename: '"/web_entry.js"',
    },
    loader: { '.png': 'dataurl', '.svg': 'dataurl', '.woff': 'dataurl', '.woff2': 'dataurl', '.ttf': 'dataurl' },
    logLevel: 'info',
  });

  await esbuild.build({
    entryPoints: [path.join(RENDERER, desktop ? 'asset_popout.js' : 'asset_popout_web_entry.js')],
    bundle: true,
    format: 'iife',
    target: 'chrome134',
    platform: 'browser',
    outfile: path.join(out, 'asset-popout.bundle.js'),
    sourcemap: true,
    minify,
    logLevel: 'info',
  });

  const html = readIndexHtml();
  const transform = desktop ? desktopHtml : value => value;
  fs.writeFileSync(path.join(out, desktop ? 'desktop.html' : 'web.html'), transform(buildHtml(html)));
  fs.writeFileSync(path.join(out, 'asset-popout.html'), transform(buildAssetPopoutHtml(
    fs.readFileSync(path.join(RENDERER, 'asset_popout.html'), 'utf8'))));
  copyExternalScripts(out);
  copyStyles(html, out);
  copyIcons(html, out);

  // Fonts and images referenced from the copied stylesheets by relative URL.
  for (const dir of ['fonts', 'assets', 'img']) {
    const from = path.join(RENDERER, dir);
    if (fs.existsSync(from)) fs.cpSync(from, path.join(out, dir), { recursive: true });
  }

  console.log(`[build:${desktop ? 'desktop' : 'web'}] wrote ${path.relative(ROOT, out)}`);
}

module.exports = { DESKTOP_CSP, desktopHtml, build, buildHtml, buildAssetPopoutHtml, scriptSources, styleSources, EXTERNAL_CSS, EXTERNAL_SCRIPTS, BUNDLE_ANCHOR, OUT, RENDERER, PREREQ_BUNDLES };

if (require.main === module) {
  build({ minify: process.argv.includes('--minify'), desktop: process.argv.includes('--desktop') }).catch((e) => {
    console.error(e && e.stack ? e.stack : e);
    process.exit(1);
  });
}
