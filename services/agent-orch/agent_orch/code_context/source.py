"""Bounded Git admission and descriptor-anchored source access."""
from __future__ import annotations

import fnmatch
import hashlib
import os
from pathlib import Path, PurePosixPath
import stat
import subprocess
import tempfile
import time

DIRECTORIES = frozenset((".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build",
    "release", "coverage", "__pycache__", ".cache", ".venv", "venv", ".tox", ".next",
    ".claude", ".codex", ".gemini", ".cursor", ".ssh", ".aws", ".azure", ".kube",
    ".gnupg", ".pentacle-stream-tokens"))
SUFFIXES = frozenset(".py .js .jsx .ts .tsx .mjs .cjs .json .yaml .yml .toml .md .txt .css .html .sh .go .rs .java .swift .sql .c .h .cpp .rb".split())


class Unavailable(Exception):
    """A public reason code, never raw filesystem/subprocess diagnostics."""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def excluded(path):
    import re
    parts = PurePosixPath(path).parts
    name = parts[-1].lower() if parts else ""
    return (any(p.lower() in DIRECTORIES for p in parts)
            or name == ".env" or name.startswith(".env.")
            or name in {"id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", ".netrc", ".npmrc", ".pypirc"}
            or Path(name).suffix in {".pem", ".key", ".p12", ".pfx", ".keystore"}
            or bool(re.search(r"(^|[._-])(credentials?|secrets?|tokens?)([._-]|$)", name)))


class Tree:
    def __init__(self, root, deadline, file_limit=1024 * 1024):
        self.deadline = deadline
        self.file_limit = file_limit
        candidate = Path(root).absolute()
        if candidate.is_symlink():
            raise Unavailable("symlink_root")
        self.root = candidate.resolve(strict=True)
        if self.root == Path(self.root.anchor) or self.root == Path.home().resolve():
            raise Unavailable("unsupported_root")
        self.fd = os.open(self.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        try:
            actual = self.git(["rev-parse", "--show-toplevel"]).decode().strip()
            if Path(actual).resolve() != self.root:
                raise Unavailable("worktree_root_required")
            self.rules = self.ignore_rules()
        except BaseException:
            self.close()
            raise

    def close(self):
        if self.fd is not None:
            os.close(self.fd)
            self.fd = None

    def check_time(self):
        if time.monotonic() >= self.deadline:
            raise Unavailable("deadline")

    def check_identity(self):
        current = os.stat(self.root, follow_symlinks=False)
        captured = os.fstat(self.fd)
        if not stat.S_ISDIR(current.st_mode) or (current.st_dev, current.st_ino) != (captured.st_dev, captured.st_ino):
            raise Unavailable("root_changed")

    def git(self, args, data=None):
        self.check_time()
        self.check_identity()
        env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        command = ["git", "-c", "core.fsmonitor=false", "-c", "core.hooksPath=" + os.devnull,
                   "-C", str(self.root), *args]
        with tempfile.TemporaryFile() as output, tempfile.TemporaryFile() as source:
            if data:
                source.write(data)
            source.seek(0)
            proc = subprocess.Popen(command, stdin=source, stdout=output, stderr=subprocess.DEVNULL, env=env)
            try:
                until = min(self.deadline, time.monotonic() + 2)
                while proc.poll() is None:
                    if output.tell() > 2 * 1024 * 1024 or time.monotonic() >= until:
                        raise Unavailable("git_limit")
                    time.sleep(.005)
                if proc.returncode not in (0, 1) or (proc.returncode and args[0] != "check-ignore"):
                    raise Unavailable("git_unavailable")
                if output.tell() > 2 * 1024 * 1024:
                    raise Unavailable("git_limit")
                output.seek(0)
                return output.read(2 * 1024 * 1024 + 1)
            finally:
                if proc.poll() is None:
                    proc.kill()
                proc.wait()

    def read(self, path, *, control=False):
        parts = PurePosixPath(path).parts
        if (not parts or len(path) > 1000 or "\x00" in path or "\\" in path
                or PurePosixPath(path).is_absolute() or any(p in {"..", "."} for p in parts)
                or (excluded(path) and not control)):
            raise Unavailable("excluded_path")
        fd = os.dup(self.fd)
        try:
            for part in parts[:-1]:
                child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
                os.close(fd)
                fd = child
                try:
                    os.stat(".git", dir_fd=fd, follow_symlinks=False)
                except FileNotFoundError:
                    pass
                else:
                    raise Unavailable("nested_repository")
            leaf = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=fd)
            with os.fdopen(leaf, "rb") as source:
                info = os.fstat(source.fileno())
                limit = 32768 if control else self.file_limit
                if not stat.S_ISREG(info.st_mode) or info.st_size > limit:
                    raise Unavailable("file_limit_or_nonregular")
                raw = source.read(limit + 1)
                if len(raw) > limit or b"\x00" in raw:
                    raise Unavailable("file_limit_or_binary")
                raw.decode("utf8")
                return raw
        finally:
            os.close(fd)

    def ignore_rules(self):
        try:
            raw = self.read(".pentacle-context-ignore", control=True)
        except FileNotFoundError:
            return (None, [])
        rules = [line.strip() for line in raw.decode().splitlines() if line.strip() and not line.lstrip().startswith("#")]
        if any(line.startswith("!") for line in rules):
            raise Unavailable("invalid_ignore_rules")
        return (digest(raw), rules)

    def paths(self):
        raw = self.git(["ls-files", "-z", "--cached", "--others", "--exclude-standard"])
        paths = sorted(set(raw.decode("utf8").split("\0")) - {""})
        ignored = set(self.git(["check-ignore", "--no-index", "-z", "--stdin"], raw).decode("utf8").split("\0")) if paths else set()
        result = []
        for path in paths:
            self.check_time()
            if len(path) > 1000 or path in ignored or excluded(path) or Path(path).suffix.lower() not in SUFFIXES:
                continue
            if any(fnmatch.fnmatchcase(path, rule) or (rule.endswith("/") and path.startswith(rule))
                   or ("/" not in rule and fnmatch.fnmatchcase(Path(path).name, rule)) for rule in self.rules[1]):
                continue
            result.append(path)
        return result
