"""Optional, read-only project evidence. No daemon or provider imports."""

SCHEMA = "pentacle.code-context.v1"
MAX_OUTPUT = 384 * 1024


def capabilities():
    import importlib.util
    import os
    import sqlite3
    parsers = {"python": True}
    for language, module in (("javascript", "tree_sitter_javascript"), ("typescript", "tree_sitter_typescript")):
        parsers[language] = bool(importlib.util.find_spec("tree_sitter") and importlib.util.find_spec(module))
    try:
        db = sqlite3.connect(":memory:")
        db.execute("CREATE VIRTUAL TABLE probe USING fts5(text)")
        db.close()
        lexical = "fts5"
    except sqlite3.Error:
        lexical = "literal"
    available = os.name == "posix" and hasattr(os, "O_NOFOLLOW") and os.open in os.supports_dir_fd
    return {"schema": SCHEMA, "status": "ready" if available else "unavailable",
            "read_only": True, "parsers_installed": parsers, "lexical": lexical,
            "limitations": ["Parser installation is not a proof of compatibility; extraction failures are explicit.",
                            "Git worktrees and POSIX no-follow file access required."]}
