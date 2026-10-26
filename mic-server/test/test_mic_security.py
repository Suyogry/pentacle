"""Real HTTP boundary checks; recording, speech and model boundaries stay fake."""
import http.client
import json
import os
from pathlib import Path
import socket
import threading
import subprocess
from types import SimpleNamespace
from http.server import ThreadingHTTPServer
from unittest.mock import Mock

import pytest
import mic_server
import mic_http

TOKEN = "synthetic-microphone-credential-" + "x" * 32


@pytest.fixture
def backend(monkeypatch):
    before = dict(mic_server.state)
    monkeypatch.setitem(mic_server.state, "transcript", ["Synthetic confidential meeting"])
    monkeypatch.setitem(mic_server.state, "partial", "")
    monkeypatch.setitem(mic_server.state, "mode", "off")
    start = Mock()
    monkeypatch.setattr(mic_server, "start_meeting", start)
    monkeypatch.setattr(mic_server, "get_service", Mock(side_effect=AssertionError("unexpected speaker access")))
    monkeypatch.setattr(mic_server, "audio_duration_s", Mock(side_effect=AssertionError("unexpected model access")))
    server = ThreadingHTTPServer(("127.0.0.1", 0), mic_server.MicHandler)
    server.mic_token = TOKEN
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server, start
    finally:
        server.shutdown()
        server.server_close()
        thread.join(2)
        mic_server.state.clear()
        mic_server.state.update(before)


def request(backend, method="GET", path="/transcript", headers=None, body=None):
    server, _ = backend
    conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=2)
    try:
        conn.request(method, path, body=body, headers=headers or {})
        response = conn.getresponse()
        return response.status, dict(response.headers), response.read()
    finally:
        conn.close()


@pytest.mark.parametrize("method,path", [("GET", "/status"), ("GET", "/transcript"),
    ("GET", "/clipboard/since/0"), ("POST", "/mode/meeting"), ("POST", "/mode/off"),
    ("POST", "/speak"), ("POST", "/transcribe?prompt_profile=fleet"),
    ("OPTIONS", "/status"), ("HEAD", "/status"), ("PUT", "/mode/meeting"), ("GET", "/unknown")])
def test_every_method_requires_authentication_before_sensitive_dispatch(backend, method, path):
    status, headers, data = request(backend, method, path, headers={"Content-Length": "1000000"})
    assert status == 401  # response must arrive without sending the promised body
    assert not any(k.lower().startswith("access-control-") for k in headers)
    assert b"Synthetic confidential" not in data
    backend[1].assert_not_called()


@pytest.mark.parametrize("authorization", ["", "Bearer wrong", TOKEN, "Basic " + TOKEN, "Bearer " + TOKEN + " extra"])
def test_wrong_credentials_are_refused(backend, authorization):
    assert request(backend, headers={"Authorization": authorization})[0] == 401


def test_authorized_read_and_control_reach_real_routes(backend):
    headers = {"Authorization": "Bearer " + TOKEN}
    status, response_headers, body = request(backend, headers=headers)
    assert status == 200
    assert json.loads(body)["lines"] == ["Synthetic confidential meeting"]
    assert response_headers["Cache-Control"] == "no-store"
    status, _, body = request(backend, "POST", "/mode/meeting", headers=headers, body=b"{}")
    assert status == 200 and json.loads(body)["ok"]
    backend[1].assert_called_once_with(stop_existing=False)


@pytest.mark.parametrize("origin", ["https://untrusted.example", "http://127.0.0.1:7780", "null", ""])
def test_even_valid_credentials_do_not_admit_browser_origins(backend, origin):
    for method in ("GET", "POST", "OPTIONS"):
        assert request(backend, method, "/mode/meeting", headers={
            "Authorization": "Bearer " + TOKEN, "Origin": origin}, body=b"{}")[0] == 403
    backend[1].assert_not_called()


@pytest.mark.parametrize("host", ["attacker.example:7780", "localhost:1", "localhost.attacker.example:7780",
    "user@localhost:7780", "localhost:7780/", "", "127.0.0.1:7780#fragment"])
def test_unexpected_host_is_refused_even_with_a_valid_token(backend, host):
    assert request(backend, headers={"Authorization": "Bearer " + TOKEN, "Host": host})[0] == 403


def raw_request(backend, fields, method="POST", path="/mode/meeting"):
    server, _ = backend
    with socket.create_connection(("127.0.0.1", server.server_port), timeout=2) as sock:
        sock.sendall((f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(fields) + "\r\n\r\n").encode())
        return sock.recv(8192).split(b"\r\n", 1)[0]


@pytest.mark.parametrize("extra,code", [(["Authorization: Bearer " + TOKEN], 401),
    (["Host: localhost:1"], 403), (["Origin: null", "Origin: https://untrusted.example"], 403),
    (["Content-Length: -1"], 400), (["Content-Length: nope"], 400),
    (["Content-Length: 1", "Content-Length: 1"], 400), (["Transfer-Encoding: chunked"], 400),
    (["Content-Length: 65537"], 413)])
def test_duplicate_headers_and_bad_framing_reject_without_reading_a_body(backend, extra, code):
    fields = [f"Host: 127.0.0.1:{backend[0].server_port}", "Authorization: Bearer " + TOKEN, *extra]
    assert f" {code} ".encode() in raw_request(backend, fields)
    backend[1].assert_not_called()


def test_large_raw_audio_rejected_before_body_or_model_access(backend):
    assert request(backend, "POST", "/transcribe?prompt_profile=fleet", headers={
        "Authorization": "Bearer " + TOKEN,
        "Content-Length": str(mic_server.MicHandler.TRANSCRIBE_MAX_BYTES + 1)})[0] == 413


@pytest.mark.parametrize("body", [b"not json", b"[]", b"null", b'"text"'])
def test_bad_json_cannot_trigger_controls(backend, body):
    assert request(backend, "POST", "/mode/meeting", headers={"Authorization": "Bearer " + TOKEN}, body=body)[0] == 400
    backend[1].assert_not_called()


def test_missing_server_credential_is_fail_closed(backend):
    del backend[0].mic_token
    assert request(backend)[0] == 503


def test_private_credential_file_and_rotation(tmp_path, monkeypatch):
    token = tmp_path / "mic.token"
    token.write_text(TOKEN)
    token.chmod(0o600)
    monkeypatch.setenv("MIC_AUTH_TOKEN_FILE", str(token))
    assert mic_http.read_token() == TOKEN
    token.write_text("replacement-random-credential-" + "z" * 32)
    assert mic_http.read_token() != TOKEN
    for mode in (0o644, 0o640, 0o400):
        token.chmod(mode)
        with pytest.raises(ValueError): mic_http.read_token()
    token.chmod(0o600)
    link = tmp_path / "link"
    link.symlink_to(token)
    monkeypatch.setenv("MIC_AUTH_TOKEN_FILE", str(link))
    with pytest.raises(ValueError): mic_http.read_token()
    monkeypatch.setenv("MIC_AUTH_TOKEN_FILE", str(tmp_path))
    with pytest.raises(ValueError): mic_http.read_token()
    monkeypatch.setenv("MIC_AUTH_TOKEN_FILE", "relative.token")
    with pytest.raises(ValueError): mic_http.read_token()


def test_missing_credential_and_routable_bind_fail_before_audio_init(monkeypatch):
    audio = Mock()
    server = Mock()
    monkeypatch.setattr(mic_server, "get_audio_buffer", audio)
    monkeypatch.setattr(mic_server, "ThreadingHTTPServer", server)
    monkeypatch.setenv("MIC_BIND_HOST", "0.0.0.0")
    with pytest.raises(ValueError, match="loopback"): mic_server.main()
    monkeypatch.setenv("MIC_BIND_HOST", "127.0.0.1")
    monkeypatch.delenv("MIC_AUTH_TOKEN_FILE", raising=False)
    with pytest.raises(ValueError, match="MIC_AUTH_TOKEN_FILE"): mic_server.main()
    audio.assert_not_called()
    server.assert_not_called()


def test_native_windows_credentials_fail_closed(monkeypatch):
    monkeypatch.setenv("MIC_AUTH_TOKEN_FILE", "/synthetic/mic.token")
    monkeypatch.setattr(mic_http, "os", SimpleNamespace(name="nt", environ=os.environ))
    with pytest.raises(ValueError, match="POSIX"): mic_http.read_token()


def test_authenticated_web_host_reaches_real_python_backend_without_exposing_token(backend, tmp_path):
    """Browser-shaped WS -> actual Node web host -> actual MicHandler HTTP."""
    token_file = tmp_path / "backend.token"
    token_file.write_text(TOKEN)
    token_file.chmod(0o600)
    profile = tmp_path / "profile.js"
    profile.write_text("module.exports=" + json.dumps({"features": {"mic": True},
        "micServerUrl": f"http://127.0.0.1:{backend[0].server_port}",
        "mic": {"tokenPath": str(token_file)}}))
    web_token = tmp_path / "web.token"
    web_token.write_text("separate-web-login-secret-" + "z" * 32)
    script = r'''
const assert=require('node:assert/strict');
const {main}=require('./server/index');
const WebSocket=require('ws');
(async()=>{
 const host=await main(['--profile',process.argv[1],'--port','0','--token-file',process.argv[2]]);
 try {
  const base='http://127.0.0.1:'+host.port;
  assert.equal((await fetch(base+'/api/config')).status,401);
  const login=await fetch(base+'/login',{method:'POST',body:new URLSearchParams({token:require('node:fs').readFileSync(process.argv[2],'utf8')}),redirect:'manual'});
  const cookie=login.headers.get('set-cookie').split(';')[0];
  const cfg=await fetch(base+'/api/config',{headers:{cookie}}).then(r=>r.text());
  assert.ok(!cfg.includes('backend.token'));assert.ok(!cfg.includes('synthetic-microphone-credential'));
  async function denied(headers,code){
   await new Promise((resolve,reject)=>{
    const ws=new WebSocket('ws://127.0.0.1:'+host.port+'/cc',{headers});
    ws.on('open',()=>{ws.close();reject(Error('unauthorized socket admitted'));});
    ws.on('unexpected-response',(_req,res)=>{res.resume();assert.equal(res.statusCode,code);resolve();});
    ws.on('error',reject);
   });
  }
  await denied({Origin:base},401);
  await denied({Cookie:cookie,Origin:'https://untrusted.example'},403);
  const ws=new WebSocket('ws://127.0.0.1:'+host.port+'/cc',{headers:{Cookie:cookie,Origin:base}});
  await new Promise((resolve,reject)=>{ws.once('open',resolve);ws.once('error',reject);});
  async function call(id,method,path,body){
   const response=new Promise(resolve=>ws.once('message',raw=>resolve(JSON.parse(raw))));
   ws.send(JSON.stringify({id,method:'mic:request',args:[method,path,...(body===undefined?[]:[body])]}));
   const got=await response;assert.equal(got.ok,true);return got.result;
  }
  assert.deepEqual((await call(1,'GET','/transcript')).lines,['Synthetic confidential meeting']);
  assert.equal((await call(2,'POST','/mode/meeting',{})).ok,true);
  await new Promise(resolve=>{ws.once('close',resolve);ws.close();});
 } finally {await host.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
'''
    result = subprocess.run(["node", "-e", script, str(profile), str(web_token)],
                            cwd=Path(__file__).resolve().parents[2], capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, result.stdout + result.stderr
    backend[1].assert_called_once_with(stop_existing=False)
