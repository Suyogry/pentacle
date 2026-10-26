#!/usr/bin/env node
// Package the macOS app without installing it.
// Usage: node scripts/build-mac.js  (or: npm run build:mac)
'use strict';
const { execFileSync, execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

if (process.platform !== 'darwin') {
  process.stderr.write('build-mac.js: must be run on macOS\n');
  process.exit(1);
}

const root = path.join(__dirname, '..');
let appName = 'Pentacle';
try {
  appName = require(path.join(root, 'config-loader')).loadConfig(root).config.appName || 'Pentacle';
} catch {}

console.log(`Building ${appName}...`);
// Package the same isolated browser assets that npm start loads.
console.log('Bundling isolated desktop renderer...');
execSync('npm run build:desktop', { cwd: root, stdio: 'inherit' });
const buildSha = execFileSync('git', ['rev-parse', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
execFileSync('electron-builder', ['--mac', `--config.extraMetadata.pentacleBuildSha=${buildSha}`], {
  cwd: root,
  stdio: 'inherit',
});

const distApp = path.join(root, 'dist', 'mac-arm64', `${appName}.app`);
const fallbackApp = path.join(root, 'dist', 'mac', `${appName}.app`);
const src = fs.existsSync(distApp) ? distApp : fallbackApp;

if (!fs.existsSync(src)) {
  process.stderr.write(`build-mac.js: built app not found at ${src}\n`);
  process.exit(1);
}

console.log(`Packaged ${src}`);
