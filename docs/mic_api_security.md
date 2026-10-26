# Microphone API authentication

Every mic HTTP request requires `Authorization: Bearer …`, including status,
uploads, OPTIONS and unknown methods. All browser Origin headers are refused;
Host must name a loopback authority at the actual listener port. No CORS
permission headers are sent. Browser controls use `cc.micRequest` over the
authenticated web host, which attaches the backend token server-side.

## Setup and migration

Upgrade the backend and all callers together. Keep the mic service stopped
during migration. Generate a separate random credential without printing it:

```sh
mkdir -p "$HOME/.config/pentacle"
chmod 700 "$HOME/.config/pentacle"
python3 - <<'PY'
import os, pathlib, secrets
p = pathlib.Path.home() / '.config/pentacle/mic.token'
fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w') as f:
    f.write(secrets.token_urlsafe(32))
PY
export MIC_AUTH_TOKEN_FILE="$HOME/.config/pentacle/mic.token"
```

The file must be an absolute path to a regular, non-symlink file owned by the
current OS user with mode exactly `0600`. Contents must be 32–256 URL-safe random
characters. Missing or unsafe credentials prevent backend startup. POSIX
permissions are required: use macOS/Linux, or run the backend and web host in
WSL with a Linux-filesystem credential. Native Windows mic runtime/recovery
fails closed. WSL audio-device provisioning is separate and unverified.

Set `MIC_AUTH_TOKEN_FILE` in the actual launch environment of the mic service,
chat daemon (transcription), speech helper (`tools.voice_reply`), audio-buffer
CLI, recovery helper, and diagnostic tools (`room_mic_probe.js`,
`verify_room_mic_end.js`). An export in one terminal does not configure existing
launchd/systemd jobs. When copying a mic runtime, include `mic_http.py` alongside
its other Python files; checkout transcription/speech callers import it too.

The desktop/web host reads `mic.tokenPath` in its private profile or its own
`MIC_AUTH_TOKEN_FILE` environment. Never put the token itself in a profile. The
public browser configuration omits the token path and recovery launcher. The
host passes the configured path to its recovery helper's environment; that
helper's managed service job must independently receive the matching setting.

Keep `micServerUrl` a loopback HTTP origin, normally `http://127.0.0.1:7780`.
The backend refuses non-loopback binds before audio initialization. Clients
reject remote destinations, URL credentials/base paths and redirects, and
bypass environment proxies. Run the backend and web host on the same machine;
remote browsers reach the authenticated web host through HTTPS.

Web profiles with `features.mic: true` require `--token-file` (a separate web
login secret) or `--auth tailscale`, even on loopback. After creating the
separate web token with the same secure generation procedure, start with:

```sh
MIC_AUTH_TOKEN_FILE="$HOME/.config/pentacle/mic.token" \
PENTACLE_CONFIG="$HOME/.config/pentacle/pentacle.config.js" \
node server --port 7795 --token-file "$HOME/.config/pentacle/web.token"
```

The daemon operator credential, web login token and mic token are separate.
Do not expose the mic backend through a general reverse proxy or restore
anonymous access for compatibility.

## Checks and rotation

`python mic-server/audio_buffer_cli.py status` checks authenticated status
without recording. JSON bodies are capped at 64 KiB, raw audio at 16 MiB, and
socket reads time out after ten seconds. Rejected requests close before body
reads. Recovery treats HTTP/authentication refusals as configuration failures,
never as a reason to restart a responding service.

For rotation, stop the backend, atomically replace the private token file with
a newly generated mode-0600 token, update any separately protected copies, and
restart the backend. The backend loads its token at startup; native clients
reread it per request. Old tokens stop working after restart.

Security tests use real HTTP and the actual Node web host with synthetic
credentials and fake recording/model boundaries; no audio devices are opened:

```sh
PYTHONPATH=mic-server:. python -m pytest mic-server/test/test_mic_security.py
node --test test/mic_security.test.js test/web_mic_adapter.test.js
```
