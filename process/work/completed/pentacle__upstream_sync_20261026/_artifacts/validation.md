# Local upstream pull validation

Local preimage: `9feb8c310ff52fe353202d2f912db5f7a53b1693`. Official main: `42698e64dcb33e2e6329fc9faf8c6a689226f7cd` (19 incoming commits; ref rechecked at closure). Merge: `a79150ed1ffe6405651a3b403a85f43987c481a9`. Final source/test candidate: `a4118a47b42a621bd7f45fa26513902eb5afa9f7`. Diff excluding lifecycle metadata SHA256: `10a0b416fc75c0a38976a6a32e317be2d7b1bde190ffa4a57f616018edd7751c`.

Independent plan and final QA: ACCEPT. Final reviewer independently ran 46 daemon/summary, 6 desktop-security and 10 corrected-Python household tests; checked merge ancestry, 13 preserved security/build files, incoming server delta, authentication fixture repair, docs and actual smoke evidence. No production fix was needed.

| Receipt | SHA256 | Result |
| --- | --- | --- |
| daemon-final.log | `f7e5ae44d3330256be6d85d53cf595419a12b4d16b11a44fa1b72fb1eeedf540` | 392 passed; 10 capability/platform skips |
| mic.log | `6450b952249b6b871510ff7fddcfd5b7732d49decd16779f0594645afa32f5cf` | 110 passed; no hardware |
| chat-core.log | `7acea60aec4e4c0ba71310dde4cca9b8bd52439f6eb2ffcafc4d39ef9133701d` | 396 passed and test typecheck |
| build-desktop.log | `fe6a7a8e7cbbd6434e90c6a0b9a3a388ff1473fc2f30449ec774cf5c3eef3a4a` | PASS |
| build-web.log | `4816a3c379f6766d39fb6b494cffd31e856f48547c1db80a999ae6ddbd7f96ff` | PASS |
| desktop.log | `978b37b93dacb6ff3f3de55df8b6eaf319b33764a7478f94ceea90d8ed73f61a` | Actual production Electron synthetic-provider/native-PTY task, security negatives, popouts/reload/reconnect and cleanup PASS |
| node.log | `e83718b068aa9dce6462fd9f20239059bc06e59ab1cef13f49ab5fc791bd7783` | Original full run: 199 files passed; one file failed from system Python 3.9; exit 1 retained |
| node-python.log | `d7127a48891b6d5ba457952c79bad137d52147f97ecd670767ceb8d82db7b4b9` | Sole failed file rerun with PENTACLE_PYTHON set to Python 3.14.6 venv: 10 passed; exit 0 |
| node-aggregate.json | `1fab889b2aed842e4f491c0edb398922a78656239b7fb90da923ad0601032a75` | All 200 files covered; 2464 passed, 1 Windows-only skip; 0 unresolved failures |
| qa-final.md | `ca0e455e076bcdce2a77f4717370e67d1ad197b67d633f86e0aab47f62a82633` | Independent final QA ACCEPT |

The original full Node invocation is not relabeled green. Its sole failing file imported a newly reachable Python type expression under the unsupported macOS system Python 3.9. The unchanged file passed all 10 tests with the documented Python 3.11+ prerequisite; all other 199 files retain their original passing evidence. Aggregate counts avoid double-counting repeated tests. No test assertion was removed or muted.

The new upstream summary-wire tests first timed out at authentication_required because they sent an anonymous hello. The test-only follow-up provisions a private synthetic credential, attaches its registry to the disposable daemon and uses its real public nonce on every connection/restart. All summary/inventory/restart assertions remain; mandatory auth regressions pass.

Raw logs, exact configuration hash, screenshot/proof/cleanup, source patch and private ledger remain outside public source. Final private ledger SHA256: `43851ecce5636cbbef09eb9e9901e8f0aae757803dd64db44d7403759fa9393b`. Actual smoke cleanup proves Electron/daemon exited, isolated tmux absent and temporary credentials absent; every Node file cleanup is clean.

This is a local source pull with explicit no-push scope. No personal service, mic hardware, clipboard capture, real paid provider, fleet deployment or cross-platform certification was exercised. Desktop/web artifacts were rebuilt; the old uninstalled packaged app was not promoted. Dependency manifests/lockfiles and security admission modules are unchanged; incoming server.py delta is only the additive progeny-close refusal.
