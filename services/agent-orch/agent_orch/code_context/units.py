"""Extract verbatim syntax units. Project source is parsed, never imported."""
from __future__ import annotations

import ast
from pathlib import Path
import re


def leading(lines, start):
    while start > 1 and (not lines[start - 2].strip() or lines[start - 2].lstrip().startswith(("#", "//"))):
        start -= 1
    return start


def extract(path, text):
    lines = text.splitlines(keepends=True)
    units, constants = [], {}
    suffix = Path(path).suffix.lower()
    try:
        if suffix == ".py":
            tree = ast.parse(text)
            for node in tree.body:
                if isinstance(node, (ast.Assign, ast.AnnAssign)):
                    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                    for target in targets:
                        if isinstance(target, ast.Name) and target.id.isupper():
                            constants[target.id] = (node.lineno, node.end_lineno)
            def bindings(node):
                return ({n.id for n in ast.walk(node) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store)}
                        | {n.arg for n in ast.walk(node) if isinstance(n, ast.arg)}
                        | {n.asname or n.name.split('.')[0] for n in ast.walk(node) if isinstance(n, ast.alias)})
            def visit(node, parents=(), shadowed=frozenset()):
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        start = min([child.lineno] + [d.lineno for d in child.decorator_list])
                        refs = {n.id for n in ast.walk(child) if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load)}
                        refs -= bindings(child) | shadowed
                        units.append((child.name, leading(lines, start), child.end_lineno, parents, refs))
                    extra = (child.name,) if isinstance(child, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) else ()
                    inherited = shadowed | bindings(child) if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) else shadowed
                    visit(child, parents + extra, inherited)
            visit(tree)
        elif suffix in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx"}:
            from tree_sitter import Language, Parser
            if suffix in {".ts", ".tsx"}:
                import tree_sitter_typescript as grammar
                language = grammar.language_tsx() if suffix == ".tsx" else grammar.language_typescript()
            else:
                import tree_sitter_javascript as grammar
                language = grammar.language()
            raw = text.encode()
            tree = Parser(Language(language)).parse(raw)
            if tree.root_node.has_error:
                raise ValueError("parse_error")
            def value(node):
                return raw[node.start_byte:node.end_byte].decode() if node else ""
            def descendants(node):
                yield node
                for child in node.named_children:
                    yield from descendants(child)
            function_types = {"function_declaration", "generator_function_declaration", "method_definition", "arrow_function", "function_expression"}
            def bindings(node):
                bound = set()
                for child in descendants(node):
                    target = child.child_by_field_name("name") if child.type == "variable_declarator" else None
                    if target:
                        bound.update(value(n) for n in descendants(target) if n.type == "identifier")
                    if child.type in function_types:
                        params = child.child_by_field_name("parameters") or child.child_by_field_name("parameter")
                        if params:
                            bound.update(value(n) for n in descendants(params) if n.type == "identifier")
                return bound
            def visit(node, parents=(), shadowed=frozenset()):
                if node.type == "variable_declarator":
                    name_node = node.child_by_field_name("name")
                    name = value(name_node)
                    if name_node and name_node.type == "identifier" and name.isupper() and value(node.parent).startswith("const ") and node.parent.parent.type in {"program", "export_statement"}:
                        constants[name] = (node.parent.start_point.row + 1, node.parent.end_point.row + 1)
                if node.type in function_types:
                    name = value(node.child_by_field_name("name"))
                    if not name and node.parent.type in {"variable_declarator", "pair"}:
                        name = value(node.parent.child_by_field_name("name") or node.parent.child_by_field_name("key"))
                    if name:
                        boundary = node.parent if node.parent.type == "export_statement" else node
                        if node.parent.type == "variable_declarator":
                            boundary = node.parent.parent
                            if boundary.parent.type == "export_statement":
                                boundary = boundary.parent
                        refs = {value(n) for n in descendants(node) if n.type == "identifier" and value(n).isupper()}
                        refs -= bindings(node) | shadowed
                        units.append((name[:200], leading(lines, boundary.start_point.row + 1),
                                      boundary.end_point.row + 1, parents, refs))
                name_node = node.child_by_field_name("name")
                extra = (value(name_node)[:200],) if name_node and node.type in {"class_declaration", "function_declaration", "method_definition"} else ()
                inherited = shadowed | bindings(node) if node.type in function_types else shadowed
                for child in node.named_children:
                    visit(child, parents + extra, inherited)
            visit(tree.root_node)
        else:
            return [], {}, "unsupported_language"
    except ImportError:
        return [], {}, "parser_missing"
    except (ValueError, SyntaxError, TypeError, AttributeError, RecursionError):
        return [], {}, "parse_unavailable"
    result = []
    for name, start, end, parents, refs in units:
        result.append({"symbol": name, "start": start, "end": end,
                       "excerpt": "".join(lines[start - 1:end]), "unit_complete": True,
                       "enclosing": list(parents[-4:]),
                       "constant_ranges": [constants[k] for k in sorted(refs & constants.keys())],
                       "dependency_boundary": "Same-file constants only; imports, closures and dynamic dependencies need source verification."})
    return result, constants, None
