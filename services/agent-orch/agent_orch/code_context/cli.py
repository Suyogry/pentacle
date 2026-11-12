"""Small standalone entrypoint; importing it needs no orchestration runtime."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile

from . import MAX_OUTPUT, capabilities


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        from .engine import emit, error
        emit(error("invalid_arguments"))
        raise SystemExit(2)


def main(argv=None):
    parser = SafeParser(description="Optional read-only code evidence. Native source tools remain available.")
    sub = parser.add_subparsers(dest="mode", required=True)
    status = sub.add_parser("status", help="Report capability without scanning source")
    status.add_argument("--json", action="store_true", help="JSON is always used")
    for mode in ("query", "read", "search"):
        command = sub.add_parser(mode)
        command.add_argument("--root", default=None, help="Exact Git worktree root; default current worktree")
        command.add_argument("--hits", type=int, default=5)
        if mode == "read":
            command.add_argument("--path", required=True)
            group = command.add_mutually_exclusive_group(required=True)
            group.add_argument("--symbol")
            group.add_argument("--start", type=int)
            command.add_argument("--end", type=int)
        else:
            command.add_argument("--query", required=True)
    args = vars(parser.parse_args(argv))
    from .engine import emit, error
    if args["mode"] == "status":
        result = capabilities()
        emit(result)
        return 0 if result["status"] == "ready" else 2
    if not capabilities()["status"] == "ready":
        emit(error("platform_unavailable"))
        return 2
    if (not 1 <= args["hits"] <= 12 or any(len(str(args.get(k) or "")) > limit for k, limit in (("query", 4096), ("symbol", 200), ("path", 1000), ("root", 4096)))
            or args.get("start") is not None and (args["start"] < 1 or args.get("end") is None or not args["start"] <= args["end"] <= args["start"] + 999)):
        emit(error("invalid_request"))
        return 2
    if args.get("end") is not None and args.get("start") is None:
        emit(error("invalid_range"))
        return 2
    if args["root"] is None:
        # Resolve only the current worktree, never walk the workspace for roots.
        try:
            p = subprocess.run(["git", "-c", "core.fsmonitor=false", "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True, timeout=2, check=True)
            args["root"] = p.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            emit(error("unsupported_root"))
            return 2
    encoded = json.dumps(args).encode()
    if len(encoded) > 16384:
        emit(error("invalid_request"))
        return 2
    # A separate owned process group puts a real deadline around native parsers
    # and Git subprocesses. Stdout is spooled, never buffered without a bound.
    with tempfile.TemporaryFile() as output:
        proc = subprocess.Popen([sys.executable, "-I", "-m", "agent_orch.code_context.engine"], stdin=subprocess.PIPE,
                                stdout=output, stderr=subprocess.DEVNULL, start_new_session=True)
        try:
            proc.communicate(encoded, timeout=10)
            output.seek(0)
            raw = output.read(MAX_OUTPUT + 1)
            if proc.returncode or len(raw) > MAX_OUTPUT:
                result = error("worker_failed")
            else:
                result = json.loads(raw)
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
            result = error("deadline")
        except (ValueError, OSError):
            result = error("worker_failed")
        finally:
            if proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
    emit(result)
    return 2 if result["status"] == "unavailable" else 0


if __name__ == "__main__":
    raise SystemExit(main())
