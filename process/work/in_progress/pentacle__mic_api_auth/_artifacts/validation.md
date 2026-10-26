# Microphone authentication validation

Base: `2bcab76dea486813839d0faf98a6296b7b128a26`.
Frozen source/tests/docs diff (process metadata excluded): SHA256
`7bb0eae07ddcff43db31aa7d04b3ceae435bf27339e58b16b403ca48c77acad6`.

## Results

- Original RED: isolated original handler returned synthetic transcript content with a foreign Origin and no token; unauthenticated meeting POST reached the control boundary.
- `npm run prestart` and `npm run build:web`: pass.
- `npm test`: exit 0; 199 passing file verdicts, 2455 tests. Initial native-PTY failure was an installed dependency's missing executable bit after `npm ci --ignore-scripts`; the reviewed `scripts/prepare-native.js` restored it. The focused PTY recheck and final full suite pass.
- `PYTHONPATH=mic-server:. .venv/bin/python -m pytest mic-server/test -q --tb=short -k 'not real_wav_duration_including_silence'`: 451 passed, 1 deselected. Original unfiltered suite confirmed the existing duration test fails only because ffprobe is unavailable. No oracle or production behavior was changed to bypass that prerequisite.
- Targeted native caller/recovery/transcription/speech suite: 50 passed, 17 subtests passed.
- Process source and generated-catalog validators: pass (existing stale-work warnings only after this record closes).
- `git diff --check`: pass.

## Independent review

Spec QA ACCEPT on original spec digest
`216260051156cd8f74c59d66560e296c4f4953f1306d631ffeaf4bb0ff50adb8`.
Final QA ACCEPT on the frozen source diff above. Reviewer independently reran
46 real HTTP/security tests, including browser-shaped WebSocket admission via
the actual Node web host to the actual Python backend; recording/model boundaries
were synthetic. Reviewer also reran 34 Node credential/transport/recovery tests.
No blocking auth, Host/Origin, body, leakage, caller or migration-doc defect found.

## Receipt digests

Raw logs stay outside the public source tree because they contain local paths.

| Receipt | SHA256 |
| --- | --- |
| Final npm suite | ff0b60c51c72eee569180e90d1f8993f620c81e0f0328aca21f328c979ac68c6 |
| Final portable mic suite | 8f931a30601c86e8d8d309c675d5c6cc817d448fcb57a5e4812fa41d9eba676c |
| Native caller suite | 20b80cbd8ce1e2d258d8c0615af4dd3596eb82d1530b79ce43b60a4fb4c3458e |
| Independent HTTP/security review | da227926ae38676731cef4fc1abe9c948f5527fa7928744f316237ff59cd9a37 |
| Independent Node subset | 217459f7b47465ab24aa5564f8a73d55a3aa11a21f2e1e959a9436d2883ce036 |

## Scope and limitations

This is source-only acceptance on macOS with Node 24 and an isolated Python
3.14 environment. Runtime dependency manifests and lockfile are unchanged.
No mic/model downloads, audio capture/playback, installed service changes or
real-browser E2E were performed. Full daemon certification needs unavailable
tmux (and the documented macOS loopback alias); the excluded existing audio
probe needs ffprobe. Native Windows fails closed; WSL audio provisioning is not
validated. The service remains unactivated. Owner: implementation lead; any
future runtime deployment must provision credentials and perform its own owned
acceptance window.
