"""Per-request evidence worker. No project code or model is executed."""
from __future__ import annotations

from collections import defaultdict
import json
import re
import sqlite3
import sys
import time

from . import MAX_OUTPUT, SCHEMA, capabilities
from .source import Tree, Unavailable, digest
from .units import extract

STOP = set("a an the and or of to for from with on in at by as is are was were be been being can could should would have has had do does did how why what which where when this that these those it its their our your you we please find show explain code pentacle".split())


def tokens(text):
    text = text.replace('_', ' ').replace('$', ' ')
    text = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", text)
    return re.findall(r"[^\W\d]\w*", text.lower(), re.UNICODE)


def normalize(text):
    return " ".join(tokens(text))


def error(reason):
    return {"schema": SCHEMA, "status": "unavailable", "reason": reason,
            "evidence": [], "fallback": "Use normal project source search/read tools."}


def run(request):
    started = time.monotonic()
    deadline = started + request.get("seconds", 9)
    result = {"schema": SCHEMA, "status": "candidates", "scope": "git_worktree",
              "evidence": [], "limitations": [], "fallback": "Expand with read/search or use normal source tools; this is not an answer-sufficiency verdict."}
    tree = None
    try:
        tree = Tree(request["root"], deadline)
        result["root"] = str(tree.root)
        result["capabilities"] = capabilities()
        paths = tree.paths()
        sources, units = {}, []
        skipped, reasons, total = 0, set(), 0
        mode, query = request["mode"], request.get("query", "")
        terms = list(dict.fromkeys(t for t in tokens(query) if t not in STOP))[:24]
        exact = bool(re.fullmatch(r"[A-Za-z_$][\w$]*", query) and ("_" in query or re.search(r"[a-z][A-Z]", query)))
        if mode != "read" and not terms:
            return error("query_terms_required")
        target = request.get("path")
        if mode == "read":
            if target not in paths:
                return error("excluded_or_unknown_path")
            paths = [target]
        if len(paths) > 5000:
            reasons.add("file_count_limit")
            paths = paths[:5000]
        for path in paths:
            tree.check_time()
            try:
                raw = tree.read(path)
            except (OSError, UnicodeError, Unavailable):
                skipped += 1
                continue
            if total + len(raw) > 32 * 1024 * 1024:
                reasons.add("source_byte_limit")
                break
            total += len(raw)
            text = raw.decode()
            sources[path] = (raw, text)
        result["scan"] = {"files": len(sources), "source_bytes": total, "skipped": skipped,
                          "max_files": 5000, "max_source_bytes": 32 * 1024 * 1024,
                          "max_file_bytes": tree.file_limit}
        if mode == "read":
            candidates = list(sources)
        elif mode == "search" or exact:
            candidates = [p for p, (_, text) in sources.items() if query.casefold() in text.casefold()]
        else:
            candidates, backend = rank_files(sources, terms)
            result["lexical"] = backend
        if len(candidates) > 32:
            reasons.add("candidate_file_limit")
        result["candidate_files"] = len(candidates[:32])
        for path in candidates[:32]:
            tree.check_time()
            raw, text = sources[path]
            parsed, _, reason = extract(path, text) if mode != "search" else ([], {}, "literal_search")
            if reason:
                reasons.add(reason)
            if mode == "read" and request.get("start"):
                lines = text.splitlines(keepends=True)
                start, end = request["start"], request["end"]
                if start > len(lines):
                    return error("line_range_out_of_bounds")
                parsed = [{"start": start, "end": min(end, len(lines)), "symbol": "",
                           "excerpt": "".join(lines[start - 1:end]), "unit_complete": False,
                           "dependency_boundary": "Explicit line range, not a complete definition."}]
            elif mode == "read" and request.get("symbol"):
                parsed = [u for u in parsed if u["symbol"] == request["symbol"]]
                if not parsed:
                    reasons.add("symbol_not_found_or_parser_unavailable")
            elif not parsed:
                lines = text.splitlines(keepends=True)
                parsed = [{"start": i + 1, "end": min(i + 64, len(lines)), "symbol": "",
                           "excerpt": "".join(lines[i:i + 64]), "unit_complete": False,
                           "dependency_boundary": reason or "Unparsed source range."}
                          for i in range(0, len(lines), 48)]
            for unit in parsed:
                units.append({**unit, "path": path, "sha256": digest(raw)})
        if mode == "read":
            ranking = list(range(len(units)))
        else:
            if mode == "search":
                ranking = [i for i, u in enumerate(units) if query.casefold() in u["excerpt"].casefold()]
            elif exact:
                literal = re.compile(r"(?<![\w$])" + re.escape(query) + r"(?![\w$])")
                ranking = [i for i, u in enumerate(units) if u["symbol"] == query
                           or (not u["unit_complete"] and literal.search(u["excerpt"]))]
            else:
                ranking, backend = rank(units, {p: sources[p] for p in candidates[:32]}, terms)
                result["lexical"] = backend
        locator_only = False
        if mode == "query":
            named = [i for i in ranking if units[i]['symbol'] == query]
            if named:
                ranking = named
            elif not exact and len(terms) >= 3:
                # Conservative overlap routing, not a calibrated confidence
                # estimate. Weak packets return locators instead of paid noise.
                stem = lambda term: term[:-1] if len(term) > 3 and term.endswith('s') else term
                wanted = {stem(t) for t in terms}
                strong = [i for i in ranking if len(wanted & {stem(t) for t in tokens(units[i]['symbol'] + ' ' + units[i]['excerpt'])}) >= max(2, (len(wanted) + 1) // 2)]
                if strong:
                    ranking = strong
                elif ranking:
                    reasons.add('weak_match')
                    locator_only = True
                    ranking = ranking[:5]
        selected = []
        used = 0
        for index in ranking:
            tree.check_time()
            unit = dict(units[index])
            if len(selected) >= request.get("hits", 5):
                break
            if locator_only:
                unit.pop('excerpt')
                unit.pop('constant_ranges', None)
                unit['unit_complete'] = False
                selected.append(unit)
                continue
            if any(e.get("excerpt") and e["path"] == unit["path"] and e["start"] <= unit["end"] and unit["start"] <= e["end"] for e in selected):
                continue
            size = len(unit["excerpt"].encode())
            if used and used + size > 6144:
                reasons.add("soft_evidence_limit")
                continue
            constants = unit.pop("constant_ranges", [])
            support = []
            lines = sources[unit["path"]][1].splitlines(keepends=True)
            for start, end in sorted(set(tuple(r) for r in constants)):
                if start < unit["start"] or end > unit["end"]:
                    support.append({"start": start, "end": end, "excerpt": "".join(lines[start - 1:end])})
            size += sum(len(c["excerpt"].encode()) for c in support)
            if used and used + size > 6144:
                reasons.add("soft_evidence_limit")
                continue
            if used + size > 48 * 1024:
                unit.pop("excerpt")
                unit.update(unit_complete=False, reason="oversized_unit", expansion={"command": "read", "path": unit["path"], "start": unit["start"], "end": min(unit["end"], unit["start"] + 63)})
                reasons.add("hard_evidence_limit")
            else:
                unit["supporting_constants"] = support
                used += size
            selected.append(unit)
        if skipped:
            reasons.add("files_skipped")
        # Admission and bytes are revalidated after ranking; a capture is not an
        # atomic snapshot of the whole repository. Suppress changed selected files.
        eligible = set(tree.paths())
        tree.check_identity()
        same_rules = tree.ignore_rules() == tree.rules
        for unit in selected:
            try:
                valid = same_rules and unit["path"] in eligible and digest(tree.read(unit["path"])) == unit["sha256"]
            except (OSError, UnicodeError, Unavailable):
                valid = False
            if valid:
                if locator_only:
                    result.setdefault('locators', []).append({k: unit[k] for k in ('path', 'symbol', 'start', 'end', 'sha256')})
                else:
                    result["evidence"].append(unit)
            else:
                reasons.add("source_changed")
        result["status"] = "partial" if reasons else ("candidates" if result["evidence"] else "no_match")
        if not result["evidence"] and reasons:
            result["limitations"].append("No usable evidence in this capture; fall back to ordinary source search.")
        result["limitations"].extend(sorted(reasons))
        result["capture_ms"] = round((time.monotonic() - started) * 1000, 2)
        result["snapshot"] = "Captured file bytes rechecked before emission; concurrent repository changes are possible."
        return result
    except Unavailable as exc:
        return error(str(exc))
    except (OSError, UnicodeError, sqlite3.Error, ValueError, KeyError):
        return error("source_unavailable")
    finally:
        if tree:
            tree.close()


def rank_files(sources, terms):
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE VIRTUAL TABLE files USING fts5(path,body)")
        paths = sorted(sources)
        db.executemany("INSERT INTO files VALUES (?,?)", [(normalize(p), normalize(sources[p][1])) for p in paths])
        expression = " OR ".join('"' + term.replace('"', '') + '"' for term in terms)
        rows = db.execute("SELECT rowid FROM files WHERE files MATCH ? ORDER BY bm25(files,6,1) LIMIT 100", (expression,)).fetchall()
        return [paths[r[0] - 1] for r in rows], "fts5"
    except sqlite3.OperationalError:
        rows = []
        for p, value in sources.items():
            body = normalize(p + " " + value[1])
            rows.append((sum(t in body for t in terms), p))
        return [p for score, p in sorted(rows, reverse=True) if score][:100], "literal_degraded"
    finally:
        db.close()


def rank(units, sources, terms):
    """File/unit reciprocal-rank fusion; scores are not confidence probabilities."""
    db = sqlite3.connect(":memory:")
    try:
        db.execute("CREATE VIRTUAL TABLE files USING fts5(path,body)")
        db.execute("CREATE VIRTUAL TABLE units USING fts5(path,symbol,body)")
        paths = sorted(sources)
        db.executemany("INSERT INTO files VALUES (?,?)", [(normalize(p), normalize(sources[p][1])) for p in paths])
        db.executemany("INSERT INTO units VALUES (?,?,?)", [(normalize(u["path"]), normalize(u["symbol"]), normalize(u["excerpt"])) for u in units])
        expression = " OR ".join('"' + term.replace('"', '') + '"' for term in terms)
        file_rank = {paths[row[0] - 1]: i for i, row in enumerate(db.execute("SELECT rowid FROM files WHERE files MATCH ? ORDER BY bm25(files,6,1) LIMIT 100", (expression,)))}
        rows = db.execute("SELECT rowid FROM units WHERE units MATCH ? ORDER BY bm25(units,6,6,1) LIMIT 100", (expression,)).fetchall()
        scores = {row[0] - 1: 1.5 / (31 + i) + 1 / (31 + file_rank.get(units[row[0] - 1]["path"], 100)) for i, row in enumerate(rows)}
        return sorted(scores, key=lambda i: (-scores[i], units[i]["path"], units[i]["start"])), "fts5"
    except sqlite3.OperationalError:
        scored = []
        for i, u in enumerate(units):
            body = normalize(u["symbol"] + " " + u["path"] + " " + u["excerpt"])
            scored.append((sum(t in body for t in terms), i))
        return [i for score, i in sorted(scored, reverse=True) if score], "literal_degraded"
    finally:
        db.close()


def emit(value):
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode()
    if len(raw) + 1 > MAX_OUTPUT:
        raw = json.dumps(error("encoded_response_limit")).encode()
    sys.stdout.buffer.write(raw + b"\n")


if __name__ == "__main__":
    try:
        emit(run(json.loads(sys.stdin.buffer.read(16385))))
    except Exception:
        emit(error("worker_failed"))
