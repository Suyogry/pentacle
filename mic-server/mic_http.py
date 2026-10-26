"""Private, loopback-only microphone transport shared by native Python callers."""
import ipaddress
import os
from pathlib import Path
import re
import stat
import urllib.parse
import urllib.request


TOKEN_PATTERN = re.compile(r"[A-Za-z0-9_-]{32,256}", re.ASCII)


def read_token():
    """Read an explicit owner-only credential; no anonymous or inline fallback."""
    filename = os.environ.get("MIC_AUTH_TOKEN_FILE", "")
    if os.name != "posix":
        raise ValueError("Microphone credentials require POSIX file permissions; use WSL on Windows")
    if not filename or not Path(filename).is_absolute():
        raise ValueError("MIC_AUTH_TOKEN_FILE must name an absolute private token file")
    try:
        fd = os.open(filename, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        with os.fdopen(fd, "rb") as handle:
            info = os.fstat(handle.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid() or stat.S_IMODE(info.st_mode) != 0o600:
                raise ValueError("Microphone token must be an owned regular mode-0600 file")
            raw = handle.read(4097)
        token = raw.decode("ascii").strip()
        if len(raw) > 4096 or TOKEN_PATTERN.fullmatch(token) is None:
            raise ValueError("Microphone token must contain 32–256 URL-safe random characters")
        return token
    except (OSError, UnicodeError) as exc:
        raise ValueError("Cannot read the private microphone credential") from exc


def is_loopback(host):
    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def local_url(value):
    """Pin destinations before attaching credentials. Hostnames are not resolved."""
    try:
        url = urllib.parse.urlsplit(value)
        if (url.scheme != "http" or not is_loopback(url.hostname or "") or url.username
                or url.password or url.query or url.fragment or url.path not in ("", "/")
                or "\\" in value or any(c.isspace() for c in value)):
            raise ValueError("invalid endpoint")
        if not 1 <= (url.port or 80) <= 65535:
            raise ValueError("invalid port")
        return value.rstrip("/")
    except (ValueError, TypeError) as exc:
        raise ValueError("Microphone endpoint must be a loopback HTTP origin") from exc


def auth_headers():
    return {"Authorization": "Bearer " + read_token()}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def open_request(request, *, timeout):
    # Neither environment proxies nor redirects may receive the credential.
    return urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect()).open(request, timeout=timeout)


def make_request(base, path, *, data=None, headers=None, method=None):
    base = local_url(base)
    if not isinstance(path, str) or not path.startswith("/") or path.startswith("//") or "\\" in path:
        raise ValueError("Invalid microphone request path")
    return urllib.request.Request(base + path, data=data, method=method,
                                  headers={**(headers or {}), **auth_headers()})
