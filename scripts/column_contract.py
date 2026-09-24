"""Column-level layer for chain_contract_audit.py (issue #64).

The tab-level audit answers "does the upstream emit a tab with this name". Every
chain defect found in W37-W39 passed that check and was a *column* defect. This
module adds the second question: does the tab the reader opens carry, at the
positions and under the names the reader uses, the columns it thinks it is
reading?

Scope, per #64: column PRESENCE and NAMING only. No value-level validation.

Emitter side (static, per upstream builder)
-------------------------------------------
For every function that calls `create_sheet("NN_Tab")`, the header row is taken
from the first of these in the same function:
  * `style_header_row(ws, <row>, <list literal | name bound to list literal>)`
  * `for i, h in enumerate(<headers>, <start>): ws.cell(<row>, i ...)`
Tabs whose header cannot be resolved statically are left out; any reader
assertion against them is reported UNVERIFIABLE, never guessed.

Reader side (static, per reader function attributed to an upstream)
-------------------------------------------------------------------
Within one function, statements are walked in source order while tracking which
tab each worksheet variable is bound to (`ws = wb["X"]`, `ws = _pick(wb, GROUP)`
with the group's preferred name, or a `for s in wb.sheetnames` substring scan
resolved against the upstream's emitted tabs). Then:
  * POSITIONAL reads - a dict literal value built from `ws.cell(r, N)`,
    `ws.cell(row=r, column=N)`, `_cell(row, i)` or `row[i]` over
    `iter_rows(values_only=True)` (0-based, converted). The dict key is the
    reader's name for the column.
  * DATA START ROW - `range(K, ...)` or `iter_rows(min_row=K)` driving the loop
    that holds those reads.
  * NAME lookups - `"literal" in h` / `h == "literal"` tests inside a function
    bound to a tab: the reader is locating a column by header text.

Verdicts
--------
  COL-MATCH   header at the read position names the reader's key
  COL-SHIFT   header at that position does NOT name the key, but another
              header in the same tab does                              -> BREAK
  COL-OOR     read position is past the last emitted header            -> BREAK
  COL-WEAK    no header in the tab names the key (naming drift or a
              legacy key); reported, not asserted
  ROW-SKIP    data loop starts more than one row below the header, so
              the first data rows are silently never read              -> BREAK
  NAME-MATCH  a by-name lookup finds its text in some header
  NAME-MISS   a by-name lookup matches no header in the tab            -> BREAK
  SCAN-MISS   a `for s in wb.sheetnames` substring scan matches no tab
              the upstream emits, so every read under it is dead       -> BREAK
  UNVERIFIABLE emitter header for that tab could not be resolved
"""

from __future__ import annotations

import ast
import re

TAB_RE = re.compile(r"^\d{2}[a-z]?_[A-Za-z0-9_]+$")

# Tokens too generic to establish that a header names a key on their own.
WEAK_TOKENS = {"id", "ids", "text", "name", "value", "type", "raw", "the", "of",
               "no", "ref", "list", "count"}
# Repo abbreviations -> the words they stand for in header text.
ABBREV = {
    "csg": {"csg", "cs", "goal"},
    "csr": {"csr", "cs", "requirement"},
    "sg": {"sg", "safety", "goal"},
    "fsr": {"fsr", "functional", "requirement"},
    "tsr": {"tsr", "technical", "requirement"},
    "dc": {"dc", "diagnostic", "coverage"},
    "sm": {"sm", "safety", "mechanism"},
    "asil": {"asil"},
    "cal": {"cal"},
    "desc": {"desc", "description"},
    "req": {"req", "requirement"},
}


def _tokens(s: str) -> set[str]:
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", str(s))
    return {t for t in re.split(r"[^a-z0-9]+", s.lower()) if t}


def _expand(tokens: set[str]) -> set[str]:
    out: set[str] = set()
    for t in tokens:
        out |= ABBREV.get(t, {t})
    return out


def names(key: str, header: str) -> bool:
    """True when `header` plausibly names the reader's `key`."""
    k = _expand(_tokens(key))
    h = _expand(_tokens(header))
    if h and h <= k:            # "Type" names `node_type`
        return True
    strong = k - WEAK_TOKENS
    if strong:
        return bool(strong & (h - WEAK_TOKENS))
    return bool(k & h)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def _int(node, consts: dict[str, int]) -> int | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, int):
        return node.value
    if isinstance(node, ast.Name) and node.id in consts:
        return consts[node.id]
    return None


def _str_list(node) -> list[str] | None:
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts and all(
            isinstance(e, ast.Constant) and isinstance(e.value, str) for e in node.elts):
        return [e.value for e in node.elts]
    return None


def _module_consts(tree: ast.Module) -> tuple[dict[str, int], dict[str, list[str]]]:
    ints: dict[str, int] = {}
    groups: dict[str, list[str]] = {}
    for n in tree.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
            name = n.targets[0].id
            if isinstance(n.value, ast.Constant) and isinstance(n.value.value, int):
                ints[name] = n.value.value
            lst = _str_list(n.value)
            if lst and all(TAB_RE.match(x) for x in lst):
                groups[name] = lst
    return ints, groups


def _funcs(tree: ast.Module):
    for n in ast.walk(tree):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield n


def _call_name(call: ast.Call) -> str:
    f = call.func
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


# --------------------------------------------------------------------------
# emitter side
# --------------------------------------------------------------------------

def emitted_headers(members: dict[str, str]) -> dict[str, dict]:
    """{tab: {"row": header_row, "headers": [...], "where": "file:line"}}"""
    out: dict[str, dict] = {}
    for rel, src in members.items():
        if not rel.endswith(".py") or rel.endswith("recalc.py") or "/office/" in "/" + rel:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        ints, _ = _module_consts(tree)
        for fn in _funcs(tree):
            tab = None
            local_lists: dict[str, list[str]] = {}
            found = None
            for node in ast.walk(fn):
                if isinstance(node, ast.Call) and _call_name(node) == "create_sheet" and node.args:
                    a0 = node.args[0]
                    if isinstance(a0, ast.Constant) and isinstance(a0.value, str) and tab is None:
                        tab = a0.value
                if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    lst = _str_list(node.value)
                    if lst:
                        local_lists[node.targets[0].id] = lst
            if not tab:
                continue
            sections: list[tuple] = []
            for node in ast.walk(fn):
                if isinstance(node, ast.Call) and _call_name(node) == "style_header_row" and len(node.args) >= 3:
                    row = _int(node.args[1], ints)
                    hdrs = _str_list(node.args[2])
                    if hdrs is None and isinstance(node.args[2], ast.Name):
                        hdrs = local_lists.get(node.args[2].id)
                    if hdrs:
                        # row may be computed (a second table lower in the tab): keep it, row unknown
                        sections.append((row, hdrs, node.lineno))
                        if row and not found:
                            found = (row, hdrs, node.lineno)
                # for i, h in enumerate(headers, 1): ws.cell(ROW, i)
                if isinstance(node, ast.For) and isinstance(node.iter, ast.Call) \
                        and _call_name(node.iter) == "enumerate" and node.iter.args:
                    src_list = node.iter.args[0]
                    hdrs = _str_list(src_list)
                    if hdrs is None and isinstance(src_list, ast.Name):
                        hdrs = local_lists.get(src_list.id)
                    if not hdrs:
                        continue
                    for inner in ast.walk(node):
                        if isinstance(inner, ast.Call) and _call_name(inner) == "cell":
                            r = inner.args[0] if inner.args else next(
                                (k.value for k in inner.keywords if k.arg == "row"), None)
                            row = _int(r, ints) if r is not None else None
                            if row:
                                found = (row, hdrs, node.lineno)
                                break
            if found and not sections:
                sections.append(found)
            if found and tab not in out:
                sections.sort(key=lambda x: x[2])
                out[tab] = {"row": found[0], "headers": found[1], "where": f"{rel}:{found[2]}",
                            "sections": [{"row": r, "headers": h} for r, h, _ in sections]}
    return out


# --------------------------------------------------------------------------
# reader side
# --------------------------------------------------------------------------

class _ReaderWalk(ast.NodeVisitor):
    """Collect positional reads, data-start rows and name lookups in one function."""

    def __init__(self, ints, groups, upstream_tabs: list[str]):
        self.ints = ints
        self.groups = groups
        self.upstream_tabs = upstream_tabs
        self.ws_tab: dict[str, str] = {}      # worksheet var -> tab
        self.row_var: dict[str, tuple] = {}   # loop var -> (tab, start_row, kind)
        self.reads: list[dict] = []
        self.starts: list[dict] = []
        self.lookups: list[dict] = []
        self.current_tab: str | None = None
        self._scan_subs: list[str] = []
        self.scan_misses: list[dict] = []

    # -- tab binding ------------------------------------------------------
    def _tab_of_expr(self, e) -> str | None:
        if isinstance(e, ast.Subscript) and isinstance(e.slice, ast.Constant) \
                and isinstance(e.slice.value, str) and TAB_RE.match(e.slice.value):
            return e.slice.value
        if isinstance(e, ast.Subscript) and isinstance(e.slice, ast.Name) and e.slice.id == "__scan__":
            return None
        if isinstance(e, ast.Call) and e.args:
            for a in e.args:
                if isinstance(a, ast.Name) and a.id in self.groups:
                    return self.groups[a.id][0]
        return None

    def visit_Assign(self, node):
        tab = self._tab_of_expr(node.value)
        # ws = wb[goal_tab] after a sheetnames substring scan
        if tab is None and isinstance(node.value, ast.Subscript) and isinstance(node.value.slice, ast.Name) \
                and self._scan_subs:
            tab = self._resolve_scan()
            if tab is None:
                # the substring scan matches no tab the upstream emits: nothing is ever read
                tab = "(scan: " + " | ".join(dict.fromkeys(self._scan_subs)) + ")"
                if not any(m["tab"] == tab for m in self.scan_misses):
                    self.scan_misses.append({"tab": tab, "line": node.lineno})
        if tab:
            for t in node.targets:
                if isinstance(t, ast.Name):
                    self.ws_tab[t.id] = tab
                elif isinstance(t, ast.Tuple) and t.elts and isinstance(t.elts[0], ast.Name):
                    self.ws_tab[t.elts[0].id] = tab
            self.current_tab = tab
        self.generic_visit(node)

    scan_misses: list

    def _resolve_scan(self) -> str | None:
        for tab in self.upstream_tabs:
            if any(s in tab.lower() for s in self._scan_subs):
                return tab
        return None

    # -- loops ------------------------------------------------------------
    def visit_For(self, node):
        it = node.iter
        # for sheet_name in wb.sheetnames: if "goal" in sheet_name.lower() ...
        if isinstance(it, ast.Attribute) and it.attr == "sheetnames":
            self._scan_subs = []
            for c in ast.walk(node):
                if isinstance(c, ast.Compare) and isinstance(c.left, ast.Constant) \
                        and isinstance(c.left.value, str) and any(isinstance(o, ast.In) for o in c.ops):
                    self._scan_subs.append(c.left.value.lower())
        # for i, row in enumerate(ws.iter_rows(...)) -> treat as `for row in ws.iter_rows(...)`
        if isinstance(it, ast.Call) and _call_name(it) == "enumerate" and it.args \
                and isinstance(node.target, ast.Tuple) and len(node.target.elts) == 2:
            it = it.args[0]
            tgt_node = node.target.elts[1]
        else:
            tgt_node = node.target
        # any name this loop rebinds stops meaning whatever row it meant before
        for n in ast.walk(node.target):
            if isinstance(n, ast.Name):
                self.row_var.pop(n.id, None)
        tgt = tgt_node.id if isinstance(tgt_node, ast.Name) else None
        if tgt and isinstance(it, ast.Call):
            name = _call_name(it)
            if name == "range" and it.args:
                start = _int(it.args[0], self.ints)
                ws = None
                if len(it.args) > 1:
                    for sub in ast.walk(it.args[1]):
                        if isinstance(sub, ast.Attribute) and sub.attr == "max_row" \
                                and isinstance(sub.value, ast.Name):
                            ws = sub.value.id
                tab = self.ws_tab.get(ws) if ws else None
                if tab:
                    # start may be computed (`hdr_row + 1`): keep the loop identity, skip the row check
                    self.row_var[tgt] = (tab, start, "cell", node.lineno)
                else:
                    self.row_var.pop(tgt, None)
            elif name == "iter_rows" and isinstance(it.func, ast.Attribute) \
                    and isinstance(it.func.value, ast.Name):
                tab = self.ws_tab.get(it.func.value.id)
                start = next((_int(k.value, self.ints) for k in it.keywords if k.arg == "min_row"), None)
                values_only = any(k.arg == "values_only" and isinstance(k.value, ast.Constant)
                                  and k.value.value for k in it.keywords)
                if tab and values_only:
                    self.row_var[tgt] = (tab, start, "tuple", node.lineno)
                else:
                    self.row_var.pop(tgt, None)
        self.generic_visit(node)

    # -- positional reads inside dict literals ---------------------------
    def _col_of(self, e) -> tuple[str, int] | None:
        """Return (tab, 1-based column) if expression `e` reads one cell."""
        for sub in ast.walk(e):
            if isinstance(sub, ast.Call) and _call_name(sub) == "cell" \
                    and isinstance(sub.func, ast.Attribute) and isinstance(sub.func.value, ast.Name):
                tab = self.ws_tab.get(sub.func.value.id)
                col = sub.args[1] if len(sub.args) > 1 else next(
                    (k.value for k in sub.keywords if k.arg == "column"), None)
                row = sub.args[0] if sub.args else next(
                    (k.value for k in sub.keywords if k.arg == "row"), None)
                c = _int(col, self.ints) if col is not None else None
                if tab and c and isinstance(row, ast.Name) and row.id in self.row_var:
                    return tab, c
            if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and len(sub.args) >= 2 \
                    and isinstance(sub.args[0], ast.Name) and sub.args[0].id in self.row_var:
                info = self.row_var[sub.args[0].id]
                i = _int(sub.args[1], self.ints)
                if info[2] == "tuple" and i is not None:
                    return info[0], i + 1
            if isinstance(sub, ast.Subscript) and isinstance(sub.value, ast.Name) \
                    and sub.value.id in self.row_var:
                info = self.row_var[sub.value.id]
                i = _int(sub.slice, self.ints)
                if info[2] == "tuple" and i is not None:
                    return info[0], i + 1
        return None

    def visit_Dict(self, node):
        for k, v in zip(node.keys, node.values):
            if not (isinstance(k, ast.Constant) and isinstance(k.value, str)) or v is None:
                continue
            hit = self._col_of(v)
            if hit:
                tab, col = hit
                loopvar = next((s.id for s in ast.walk(v) if isinstance(s, ast.Name) and s.id in self.row_var), None)
                start = self.row_var[loopvar][1] if loopvar else None
                loop = self.row_var[loopvar][3] if loopvar else None
                self.reads.append({"tab": tab, "col": col, "key": k.value, "line": node.lineno,
                                   "start": start, "loop": loop})
        self.generic_visit(node)

    # -- by-name header lookups ------------------------------------------
    def visit_Compare(self, node):
        if self.current_tab and isinstance(node.left, ast.Constant) and isinstance(node.left.value, str) \
                and len(node.ops) == 1 and isinstance(node.ops[0], (ast.In, ast.Eq)) \
                and isinstance(node.comparators[0], ast.Name):
            lit = node.left.value.strip()
            if len(lit) >= 3 and re.search(r"[a-z]", lit, re.I) and not TAB_RE.match(lit) \
                    and lit.lower() not in self._scan_subs:
                self.lookups.append({"tab": self.current_tab, "text": lit, "line": node.lineno})
        self.generic_visit(node)


def reader_contracts(src: str, func_filter, upstream_tabs: list[str]) -> list[dict]:
    """Walk every function accepted by `func_filter(name)`; return raw contract rows."""
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return [{"kind": "PARSE-ERROR", "func": "-", "line": e.lineno or 0, "detail": str(e.msg)}]
    ints, groups = _module_consts(tree)
    rows: list[dict] = []
    for fn in _funcs(tree):
        if not func_filter(fn.name):
            continue
        w = _ReaderWalk(ints, groups, upstream_tabs)
        for stmt in fn.body:
            w.visit(stmt)
        for r in w.reads:
            rows.append({"kind": "POS", "func": fn.name, **r})
        for lk in w.lookups:
            rows.append({"kind": "NAME", "func": fn.name, **lk})
        for sm in w.scan_misses:
            rows.append({"kind": "SCAN", "func": fn.name, **sm})
    return rows


def judge(rows: list[dict], emitted: dict[str, dict]) -> list[dict]:
    """Turn raw reader rows into verdicts against the upstream's emitted headers."""
    out: list[dict] = []
    # POSITIONAL: group keys by (func, tab, col) - several legacy keys may alias one column
    pos: dict[tuple, dict] = {}
    for r in rows:
        if r["kind"] == "SCAN":
            out.append({"func": r["func"], "tab": r["tab"], "line": r["line"], "verdict": "SCAN-MISS",
                        "assertion": "pattern scan finds a tab",
                        "note": "no tab the upstream emits matches these substrings; every read under it is dead"})
            continue
        if r["kind"] != "POS" or r["tab"].startswith("(scan:"):
            continue
        k = (r["func"], r["tab"], r["loop"], r["col"])
        g = pos.setdefault(k, {"keys": [], "lines": [], "start": r["start"]})
        if r["key"] not in g["keys"]:
            g["keys"].append(r["key"])
        g["lines"].append(r["line"])

    # A tab can hold several tables (tsc 03_System_Architecture: HW then SW). Each
    # read loop is judged against the section whose headers it matches best.
    section_of: dict[tuple, dict] = {}
    for (func, tab, loop, _c) in pos:
        if (func, tab, loop) in section_of or tab not in emitted:
            continue
        cols = {c: g["keys"] for (f2, t2, l2, c), g in pos.items() if (f2, t2, l2) == (func, tab, loop)}
        def _score(sec, cols=cols):
            here = sum(1 for c, ks in cols.items()
                       if c <= len(sec["headers"]) and any(names(k, sec["headers"][c - 1]) for k in ks))
            anywhere = sum(1 for ks in cols.values() if any(names(k, h) for k in ks for h in sec["headers"]))
            return (here, anywhere)
        best = max(emitted[tab].get("sections") or [emitted[tab]], key=_score)
        section_of[(func, tab, loop)] = best

    starts: dict[tuple, dict] = {}
    for (func, tab, loop, col), g in sorted(pos.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2] or 0, kv[0][3])):
        em = emitted.get(tab)
        base = {"func": func, "tab": tab, "line": min(g["lines"])}
        if em is None:
            out.append({**base, "verdict": "UNVERIFIABLE", "assertion": f"col {col} as `{'`/`'.join(g['keys'])}`",
                        "note": "upstream header row for this tab not statically resolvable"})
            continue
        sec = section_of[(func, tab, loop)]
        hdrs = sec["headers"]
        keys = g["keys"]
        desc = f"col {col} as `{'`/`'.join(keys)}`"
        if col > len(hdrs):
            out.append({**base, "verdict": "COL-OOR", "assertion": desc,
                        "note": f"upstream emits only {len(hdrs)} headers"})
        else:
            here = hdrs[col - 1]
            if any(names(k, here) for k in keys):
                out.append({**base, "verdict": "COL-MATCH", "assertion": desc, "note": f"upstream `{here}`"})
            else:
                elsewhere = [(j + 1, h) for j, h in enumerate(hdrs) if j != col - 1 and any(names(k, h) for k in keys)]
                if elsewhere:
                    j, h = elsewhere[0]
                    out.append({**base, "verdict": "COL-SHIFT", "assertion": desc,
                                "note": f"upstream col {col} is `{here}`; `{h}` is at col {j}"})
                else:
                    out.append({**base, "verdict": "COL-WEAK", "assertion": desc,
                                "note": f"upstream col {col} is `{here}`; no header names this key"})
        if g["start"] is not None and sec.get("row"):
            starts.setdefault((func, tab, loop), {"start": g["start"], "line": min(g["lines"]), "row": sec["row"]})

    for (func, tab, _loop), s in sorted(starts.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2] or 0)):
        hdr_row, first = s["row"], s["start"]
        desc = f"data from row {first}"
        if first > hdr_row + 1:
            n = first - hdr_row - 1
            out.append({"func": func, "tab": tab, "line": s["line"], "verdict": "ROW-SKIP", "assertion": desc,
                        "note": f"upstream header is row {hdr_row}; the first {n} data row(s) are never read"})
        else:
            out.append({"func": func, "tab": tab, "line": s["line"], "verdict": "ROW-OK", "assertion": desc,
                        "note": f"upstream header is row {hdr_row}"})

    for r in rows:
        if r["kind"] == "NAME":
            em = emitted.get(r["tab"])
            base = {"func": r["func"], "tab": r["tab"], "line": r["line"], "assertion": f"header containing \"{r['text']}\""}
            if em is None:
                out.append({**base, "verdict": "UNVERIFIABLE", "note": "upstream header row not resolvable"})
                continue
            all_h = [h for sec in (em.get("sections") or [em]) for h in sec["headers"]]
            hit = next((h for h in all_h if r["text"].lower() in h.lower()), None)
            if hit:
                out.append({**base, "verdict": "NAME-MATCH", "note": f"upstream `{hit}`"})
            else:
                out.append({**base, "verdict": "NAME-MISS", "note": "no upstream header contains this text"})
        elif r["kind"] == "PARSE-ERROR":
            out.append({"func": "-", "tab": "-", "line": r["line"], "verdict": "PARSE-ERROR",
                        "assertion": "reader parses", "note": r["detail"]})
    return out


COL_BREAKS = {"COL-SHIFT", "COL-OOR", "ROW-SKIP", "NAME-MISS", "PARSE-ERROR", "SCAN-MISS"}
COL_ORDER = ["PARSE-ERROR", "SCAN-MISS", "ROW-SKIP", "COL-SHIFT", "COL-OOR", "NAME-MISS", "UNVERIFIABLE",
             "COL-WEAK", "ROW-OK", "NAME-MATCH", "COL-MATCH"]
