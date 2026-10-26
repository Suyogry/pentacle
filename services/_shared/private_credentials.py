"""Bounded owner-only credential file reads; never include secrets in errors."""
import os
from pathlib import Path
import stat


def read_private_token(path: Path) -> str:
    descriptor = -1
    try:
        if not hasattr(os, "O_NOFOLLOW") or not Path(path).is_absolute():
            raise ValueError()
        descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
        info = os.fstat(descriptor)
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != os.getuid()
                or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 8192):
            raise ValueError()
        raw = os.read(descriptor, 8193)
        value = raw.decode("utf-8").strip()
        if not value or len(raw) > 8192 or "\n" in value or "\r" in value or "\0" in value:
            raise ValueError()
        return value
    except (OSError, ValueError, UnicodeError):
        raise PermissionError("private credential file unavailable or unsafe") from None
    finally:
        if descriptor >= 0:
            os.close(descriptor)
