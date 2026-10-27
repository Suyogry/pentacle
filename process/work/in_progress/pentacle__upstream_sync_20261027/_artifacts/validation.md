# Official upstream integration validation — 2026-10-27

Personal main preimage `50e53b5cc0904e04245779389c91798fac41f720`;
origin main preimage `9feb8c310ff52fe353202d2f912db5f7a53b1693`.
Official main captured/rechecked `30a8acea51ad05951eeeb480e66015591c0ce4ac`:
50 incoming commits,100 upstream files changed. Normal merge retains both
histories. Frozen source/tests/docs diff excluding process metadata SHA256:
`c626e25f8e06a31351bb02d39d40e9687ac2e98d21d5dca020b6034809aaeea6`.
Independent plan/final QA ACCEPT; independent focused tests160pass.

## Compatibility and security

Resolved three conflicts in daemon dispatch, remote-auth documentation and RPC
admission tests. Keep mandatory operator/seat authentication on every transport;
privileged token grants/freeze require operator authority. Local-admin proof
remains limited to recovery and is not silently borrowed by ordinary CLI calls.
The incoming upstream bootstrap assumptions are adapted to this stricter policy,
including actual-socket no-effects negatives and authenticated CLI/seat positives.
No generic localhost exemption or agent approval change was introduced.

Ten preserved-file checks bind main/preload/desktop policy, provider URL fix,
Settings CSS, manifest/lock, mic client and shared operator-auth/client bytes to
the personal preimage. Electron remains44.9.3. Production dependency records and
all dependency manifests/locks are unchanged by this merge. Root exact-lock
`npm ci` passed, tree chat-core links point to isolated changed source, and both
full/omit-dev audits report0 advisories. Shared-core dev tools resolve through
the root locked install; an attempted nested npmci was correctly refused because
that subproject has no lockfile. It made no source changes.

## Final gates

- Full root Node runner:203/203 files pass/clean;2479 passed,1 Windows-only skip,
  exit0, no runner or directory cleanup errors. Supported Python3.14.6 selected
  explicitly; per-file budget120s unchanged.
- Affected daemon plus mandatory-auth/security suite:27 files,1082 passed,
  13 capability/platform skips, exit0. One existing synchronous-websocket
  context-manager deprecation warning is retained.
- Full agent-orch:7319 passed,13 skipped, exit0.
- Shared chat core:398 passed and test typecheck passed.
- Focused mic security/local-actions/wake tests:159 passed; no audio/model capture.
- Changed gate/selection/checkpoint tests:127 passed plus28 subtests.
- Desktop and web builds passed. Actual Electron44.9.3 with the real authenticated
  disposable daemon, synthetic provider, native PTY/tmux passed rehearsal and
  final confirmation: spawn/send/rendered reply, terminal bytes, settings,
  popout/reload/dock, reconnect, disconnected rejection and isolation negatives.
  Cleanup proves owned Electron/daemon exited, tmux/credentials absent, no errors.
  Final screenshot inspected; visible fixture assistant plus baseline transient
  Loading messages label after reload, not a claim of cosmetic absence.

Original failed evidence remains intact. First daemon run had14 fixture failures:
10 new oversized-event tests sent anonymous hello;4 spawn/lifecycle mocks lacked
required private-token staging. Tests now authenticate through private synthetic
operator credentials and stage synthetic worker tokens in fake transport memory;
no application guard was relaxed. An initial six error-code mismatches reflected
earlier operator denial and were reconciled to that exact stronger predicate.
The initial full CLI run had one installer discovery failure: macOS discovery
looks only at fixed3.13 paths while this host uses3.14. The existing dry-run test
now passes its running supported interpreter through the documented --python
option; installer production behavior was not changed. All final full commands
passed after these bounded fixture repairs; originals are not relabelled green.

## Receipts and limits

Raw receipts remain in the maintainer's private `upstream-sync-20261027` directory.
No personal runtime restart, real account/provider call, microphone, clipboard,
fleet activation, signed package or cross-platform certification was performed.
Source delivery/push to the personal fork is explicitly user-authorized.

| Receipt | SHA256 |
| --- | --- |
| node-summary.json | 9cdc85f95f84fd59491c73dceee09449d6f339d6ccc124dc27826ad9bf3a56e9 |
| node.log | 9987413e25f58cd2de162741225ea3d6db02ef1a76e479f06620cabaf95d724f |
| daemon.log | 473659ce7c45eb6466a6641162cd537b737b1beae4997e55b3817f3d294fdf7f |
| daemon-final.log | f65521eaf96717afb5fd50ded06d3f15d7f3c35df3e835172f184b5666df7d18 |
| cli.log | 87bdc4d8e66dbb0c4430d951e18637a3b9c4e9de034bbc8db29483f5b6c282a0 |
| cli-final.log | 35cb2137db4fce962389f863f9004b751d3021d8e759b16dd6fc198a27c4eb28 |
| chat-core.log | 546356f6ddab97ce1413d5208f383cf38c08065aefde19af12994cc425319ed1 |
| mic.log | 14ab456ee39bc8117e3552fbee4d425f1c9c0293acfb27c27e4478dea3756f56 |
| gate-selection.log | f085e994f5630e140c2cf1bbbcb91ddf9cd93e0729f157a9f5abd6cf16366aba |
| desktop-rehearsal.log | a66aa2cc12b3fc7c4a921e4160f5fb3d3d1f792922af284f305d80133e8b655e |
| desktop-final.log | 4db93966b96064e417adbce68e08d15853d259efef45ea23f5efd441007b2782 |
| final-proof.json | 2434641c49a0faac5c6d53cd52f353babc7989af8b022a61176f954ade1309c8 |
| final-cleanup.json | deeaa168ba03945b3b96e4e3d98750f7fd079a8a7c6572dc0b61bfc455a7e733 |
| final-desktop.png | 435e0dd7d7d26f0fcb0137d9458615a262f31d3e42d2dd6dc3c7d33d655c8044 |
| qa-final.md | dabe29eab86b71d7b1c0528da9dbeeb5c17759fb309f0f123fbc7601a4a08eb1 |
| audit-full.json | ea1aaf2c0b13798f93930b272683a759da8288ed74f14eb7c3b9b711be9c54e7 |
| audit-production.json | ea1aaf2c0b13798f93930b272683a759da8288ed74f14eb7c3b9b711be9c54e7 |
