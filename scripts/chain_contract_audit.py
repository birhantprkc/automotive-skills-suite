#!/usr/bin/env python3
"""Audit builder-to-builder xlsx handoffs: expected sheet names vs. emitted ones.

Scope (deliberately narrow, per issue #46 as descoped in WEEK-2026-W34):
  * builder -> builder reads only. A "read" is a `.py` inside a `*-builder.skill`
    that calls `openpyxl.load_workbook` on a workbook produced by a DIFFERENT
    skill. `recalc.py` is excluded everywhere: every builder ships one and it
    reloads the builder's OWN output.
  * builder -> reviewer pairs are OUT of scope. A reviewer ships alongside the
    builder it reviews, so the two move together; the failure mode that bit us
    (#43) was a builder reading another builder's drifted tab names.

Method
------
1. Reader side. For every reader script, collect the sheet names it expects:
     - `"X" in wb.sheetnames` / `"X" not in wb.sheetnames`
     - `wb["X"]` subscripts
     - module-level alias tuples/lists of tab names, e.g.
       `CSR_SHEETS = ("05_CSR_Catalog", "02_CSRs_Catalog")` — the
       preferred-name-then-legacy-fallback shape introduced by the #43 repair.
   Only strings matching the repo's tab convention (`NN_Name` / `NNb_Name`)
   count, which keeps ordinary dict subscripts out of the result.
   A reader that instead iterates `for name in wb.sheetnames` and matches by
   substring is recorded as PATTERN-SCAN: it has no fixed contract to break.

   A read is treated as a SELF-READ, and dropped, when the function or file
   name references the reading skill's own artifact (`trees_from_fsc_xlsx`
   inside `fsc-builder`). Those reload the skill's own output.

2. Upstream attribution, in priority order:
     a. enclosing function named `read_<x>` where `<x>-builder` exists
     b. reader filename `<x>_reader.py` where `<x>-builder` exists
     c. the single foreign `*-builder` named in the reading skill's SKILL.md
   (a) and (b) are treated as EXPLICIT attribution: the code itself names the
   upstream, so a miss there cannot be explained away.

3. Emitter side. For the upstream builder, collect every sheet name it can
   emit: `wb.create_sheet("X")` and `ws.title = "X"`, across all its scripts
   except `recalc.py`.

4. Verdict per expected name:
     MATCH        - upstream emits it.
     ALIAS        - upstream does not emit it, but it is a declared legacy
                    alternative in a group whose preferred name DOES match.
     FALLBACK     - same idea, expressed as an `elif`/`or` branch instead of a
                    constant. A tolerated compatibility shim, not a break.
     SELF-AMBIG   - upstream does not emit it, the READING skill emits a tab of
                    that name, AND attribution was only inferred from SKILL.md
                    prose. Ambiguous; reported, not asserted.
     BREAK        - upstream does not emit it and nothing above applies. Note
                    that a name the reading skill emits itself is still a BREAK
                    under explicit attribution — a reader hunting for its own
                    output tab inside an upstream workbook is the bug, not the
                    excuse.
     UNVERIFIABLE - upstream could not be resolved to a skill file.

Read-only. Modifies no `.skill` file.

Usage:  python scripts/chain_contract_audit.py            # writes docs/chain-contract-audit.md
        python scripts/chain_contract_audit.py --stdout   # print instead
"""

from __future__ import annotations

import ast
import difflib
import re
import sys
import zipfile
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
OUT_MD = REPO / "docs" / "chain-contract-audit.md"

# Scripts that never constitute a cross-skill read.
EXCLUDED_SCRIPTS = ("recalc.py",)
EXCLUDED_DIRS = ("/office/",)

# BREAKs that already have an issue. Key: (reader, upstream, expected tab).
# Add a row here when you open one, so a regeneration keeps the trail.
KNOWN_ISSUES: dict[tuple[str, str, str], int] = {
    ("fmeda-builder", "tsc-builder", "05_Safety_Mechanisms_From_TSC"): 53,
}

# Repo tab-name convention: two digits, optional letter suffix, underscore.
TAB_RE = re.compile(r"^\d{2}[a-z]?_[A-Za-z0-9_]+$")

LOAD_RE = re.compile(r"\bload_workbook\s*\(")
SHEETNAMES_MEMBER_RE = re.compile(r'"([^"]+)"\s*(?:not\s+)?in\s+\w+\.sheetnames')
SUBSCRIPT_RE = re.compile(r'\b\w+\[\s*"([^"]+)"\s*\]')
CREATE_SHEET_RE = re.compile(r'create_sheet\s*\(\s*"([^"]+)"')
TITLE_ASSIGN_RE = re.compile(r'\.title\s*=\s*"([^"]+)"')
DYNAMIC_SCAN_RE = re.compile(r"for\s+\w+\s+in\s+\w+\.sheetnames")
DEF_RE = re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)")


def skill_files() -> dict[str, Path]:
    return {p.name[: -len(".skill")]: p for p in sorted(SKILLS.glob("*.skill"))}


def read_members(path: Path) -> dict[str, str]:
    """Return {member-path-without-top-dir: text} for .py and SKILL.md members."""
    out: dict[str, str] = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            if not (name.endswith(".py") or name.endswith("SKILL.md")):
                continue
            rel = name.split("/", 1)[1] if "/" in name else name
            out[rel] = z.read(name).decode("utf-8", "replace")
    return out


def is_reader_script(rel: str, src: str) -> bool:
    if any(rel.endswith(x) for x in EXCLUDED_SCRIPTS):
        return False
    if any(d in "/" + rel for d in EXCLUDED_DIRS):
        return False
    return bool(LOAD_RE.search(src))


def emitted_sheets(members: dict[str, str]) -> set[str]:
    names: set[str] = set()
    for rel, src in members.items():
        if rel.endswith(".md") or rel.endswith(EXCLUDED_SCRIPTS):
            continue
        names.update(CREATE_SHEET_RE.findall(src))
        names.update(n for n in TITLE_ASSIGN_RE.findall(src) if TAB_RE.match(n))
    return names


def foreign_builders_in_md(members: dict[str, str], self_name: str, known: set[str]) -> list[str]:
    md = next((s for r, s in members.items() if r.endswith("SKILL.md")), "")
    refs = set(re.findall(r"\b([a-z0-9]+(?:-[a-z0-9]+)*-builder)\b", md))
    refs.discard(self_name)
    return sorted(r for r in refs if r in known)


def alias_groups(src: str) -> list[list[tuple[str, int]]]:
    """Module-level tuples/lists made entirely of tab-shaped strings.

    `CSR_SHEETS = ("05_CSR_Catalog", "02_CSRs_Catalog")` — preferred name first,
    legacy aliases after. Membership in such a group is an acceptance set, not
    four independent assertions.
    """
    groups: list[list[tuple[str, int]]] = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return groups
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.value, (ast.Tuple, ast.List)):
            continue
        vals = [(e.value, e.lineno) for e in node.value.elts
                if isinstance(e, ast.Constant) and isinstance(e.value, str)]
        if vals and len(vals) == len(node.value.elts) and all(TAB_RE.match(v) for v, _ in vals):
            groups.append(vals)
    return groups


def expected_names(src: str) -> list[dict]:
    """Per-line expected sheet names with enclosing function and branch keyword."""
    rows: list[dict] = []
    groups = alias_groups(src)
    group_of = {n: gi for gi, g in enumerate(groups) for n, _ in g}
    func = None

    for lineno, line in enumerate(src.splitlines(), 1):
        m = DEF_RE.match(line)
        if m:
            func = m.group(1)
        found: list[str] = []
        found += SHEETNAMES_MEMBER_RE.findall(line)
        found += [n for n in SUBSCRIPT_RE.findall(line) if TAB_RE.match(n)]
        stripped = line.strip()
        for n in dict.fromkeys(found):
            if not TAB_RE.match(n) or n in group_of:
                continue
            rows.append({"name": n, "func": func, "line": lineno,
                         "alt": stripped.startswith("elif") or " or " in stripped, "group": None})

    # Alias-group members are reported once each, at the constant's own line.
    for gi, group in enumerate(groups):
        for name, lineno in group:
            rows.append({"name": name, "func": "(module constant)", "line": lineno,
                         "alt": False, "group": gi})
    return rows


def resolve_upstream(
    func: str | None, rel: str, md_refs: list[str], known: set[str]
) -> tuple[str | None, bool]:
    """Return (upstream, explicit). `explicit` means the code named it, not prose."""
    if func and func.startswith("read_"):
        cand = func[len("read_"):].replace("_", "-") + "-builder"
        if cand in known:
            return cand, True
    stem = Path(rel).stem
    if stem.endswith("_reader"):
        cand = stem[: -len("_reader")].replace("_", "-") + "-builder"
        if cand in known:
            return cand, True
    if len(md_refs) == 1:
        return md_refs[0], False
    return None, False


def is_self_read(skill: str, func: str | None, rel: str, upstream: str | None) -> bool:
    """True when the reader reloads its own skill's output rather than an upstream."""
    token = skill[: -len("-builder")].replace("-", "_")
    up_token = upstream[: -len("-builder")].replace("-", "_") if upstream else ""
    hay = f"{Path(rel).stem}|{func or ''}"
    if up_token and up_token in hay:
        return False
    return token in hay


def main() -> int:
    files = skill_files()
    builders = {n: p for n, p in files.items() if n.endswith("-builder")}
    known = set(builders)

    members_cache = {n: read_members(p) for n, p in builders.items()}
    emitted_cache = {n: emitted_sheets(m) for n, m in members_cache.items()}

    findings: list[dict] = []
    pattern_scans: list[dict] = []
    self_reads: list[dict] = []
    reader_count = 0

    for skill in sorted(builders):
        members = members_cache[skill]
        md_refs = foreign_builders_in_md(members, skill, known)
        self_emits = emitted_cache[skill]

        for rel, src in sorted(members.items()):
            if not rel.endswith(".py") or not is_reader_script(rel, src):
                continue
            reader_count += 1
            rows = expected_names(src)

            if DYNAMIC_SCAN_RE.search(src):
                up, _ = resolve_upstream(None, rel, md_refs, known)
                pattern_scans.append({"skill": skill, "script": rel, "upstream": up})
                if not rows:
                    continue

            for row in rows:
                up, explicit = resolve_upstream(row["func"], rel, md_refs, known)
                if is_self_read(skill, row["func"], rel, up):
                    entry = {"skill": skill, "script": rel, "func": row["func"], "name": row["name"]}
                    if entry not in self_reads:
                        self_reads.append(entry)
                    continue
                if up is None:
                    verdict, note = "UNVERIFIABLE", "upstream skill could not be resolved"
                elif row["name"] in emitted_cache[up]:
                    verdict, note = "MATCH", ""
                elif row["group"] is not None:
                    verdict, note = "ALIAS", "declared legacy alias; preferred name matches"
                elif row["alt"]:
                    verdict, note = "FALLBACK", "alternative branch; sibling matches"
                elif row["name"] in self_emits and not explicit:
                    verdict, note = "SELF-AMBIG", "reading skill emits this tab; attribution inferred from prose only"
                else:
                    near = difflib.get_close_matches(row["name"], sorted(emitted_cache[up]), n=1, cutoff=0.5)
                    note = f"upstream emits no such tab"
                    if row["name"] in self_emits:
                        note += "; this is the READING skill's own output tab name"
                    if near:
                        note += f"; nearest upstream tab `{near[0]}`"
                    verdict = "BREAK"
                findings.append(
                    {
                        "skill": skill,
                        "script": rel,
                        "func": row["func"] or "-",
                        "line": row["line"],
                        "upstream": up or "?",
                        "name": row["name"],
                        "verdict": verdict,
                        "note": note,
                        "group": row["group"],
                    }
                )

    # ALIAS / FALLBACK are only honest if a sibling really did match.
    for f in findings:
        if f["verdict"] == "ALIAS":
            sibling = any(g["verdict"] == "MATCH" and g["skill"] == f["skill"]
                          and g["group"] == f["group"] for g in findings)
            if not sibling:
                f["verdict"] = "BREAK"
                f["note"] = "declared alias group, but no member matches upstream"
        elif f["verdict"] == "FALLBACK":
            sibling = any(g["verdict"] == "MATCH" and g["skill"] == f["skill"]
                          and g["func"] == f["func"] for g in findings)
            if not sibling:
                f["verdict"] = "BREAK"
                f["note"] = "alternative branch, but no sibling matches either"

    # One row per (reader, upstream, tab): a name asserted on both the
    # membership test and the subscript is one contract, not two.
    deduped: dict[tuple, dict] = {}
    for f in findings:
        key = (f["skill"], f["script"], f["upstream"], f["name"], f["verdict"])
        if key in deduped:
            deduped[key]["hits"] += 1
            deduped[key]["lines"].append(f["line"])
        else:
            f["hits"] = 1
            f["lines"] = [f["line"]]
            deduped[key] = f
    findings = list(deduped.values())
    for f in findings:
        f["loc"] = ", ".join(str(x) for x in sorted(set(f["lines"])))

    order = {"BREAK": 0, "UNVERIFIABLE": 1, "SELF-AMBIG": 2, "FALLBACK": 3, "ALIAS": 4, "MATCH": 5}
    findings.sort(key=lambda f: (order[f["verdict"]], f["skill"], f["line"]))

    counts = {k: sum(1 for f in findings if f["verdict"] == k) for k in order}
    chains = sorted({(f["skill"], f["upstream"]) for f in findings})

    lines: list[str] = []
    a = lines.append
    a("# Chain-contract audit — builder-to-builder xlsx handoffs")
    a("")
    a(f"_Generated {date.today().isoformat()} by `scripts/chain_contract_audit.py` "
      "(read-only; modifies no `.skill` file)._")
    a("")
    a("Scope is builder-to-builder reads only, per the W34 descope of "
      "[#46](https://github.com/jherrodthomas/automotive-skills-suite/issues/46). "
      "Builder-to-reviewer pairs are excluded: a reviewer ships with the builder it "
      "reviews, so the two cannot drift apart the way #43 did.")
    a("")
    a("## Summary")
    a("")
    a(f"- Builders scanned: **{len(builders)}**")
    a(f"- Cross-skill reader scripts found: **{reader_count}** "
      f"(in {len({f['skill'] for f in findings})} skills)")
    a(f"- Declared chains audited: **{len(chains)}**")
    a(f"- Sheet-name assertions checked: **{len(findings)}**")
    a("")
    a("| Verdict | Count |")
    a("|---|---|")
    for k in ["MATCH", "ALIAS", "FALLBACK", "SELF-AMBIG", "UNVERIFIABLE", "BREAK"]:
        a(f"| {k} | {counts[k]} |")
    a("")
    if counts["BREAK"]:
        a(f"**{counts['BREAK']} confirmed BREAK(s).** One issue each — see the table below. "
          "Every BREAK is hand-verified against the upstream generator before an issue is "
          "opened; the verification for each is written up in `docs/skill-polish-log/`.")
    else:
        a("**No confirmed BREAKs.** Every hard-coded tab name a builder expects from "
          "another builder is a name that builder actually emits.")
    a("")

    breaks = [f for f in findings if f["verdict"] == "BREAK"]
    if breaks:
        a("## BREAKs and their issues")
        a("")
        a("| Chain | Expected tab | Issue |")
        a("|---|---|---|")
        for f in breaks:
            num = KNOWN_ISSUES.get((f["skill"], f["upstream"], f["name"]))
            link = (f"[#{num}](https://github.com/jherrodthomas/"
                    f"automotive-skills-suite/issues/{num})") if num else "**not yet filed**"
            a(f"| `{f['skill']}` → `{f['upstream']}` | `{f['name']}` | {link} |")
        a("")

    a("## Chains audited")
    a("")
    a("| Reader | Upstream | Assertions | Worst verdict |")
    a("|---|---|---|---|")
    for reader, up in chains:
        rows = [f for f in findings if f["skill"] == reader and f["upstream"] == up]
        worst = min(rows, key=lambda r: order[r["verdict"]])["verdict"]
        a(f"| `{reader}` | `{up}` | {len(rows)} | {worst} |")
    a("")

    a("## Findings")
    a("")
    a("| Verdict | Reader | Script:line | Function | Upstream | Expected tab | Note |")
    a("|---|---|---|---|---|---|---|")
    for f in findings:
        a(f"| {f['verdict']} | `{f['skill']}` | `{f['script']}`:{f['loc']} | "
          f"`{f['func']}` | `{f['upstream']}` | `{f['name']}` | {f['note']} |")
    a("")

    if pattern_scans:
        a("## Pattern-scan readers (no fixed contract)")
        a("")
        a("These iterate `wb.sheetnames` and match by substring instead of asserting "
          "exact tab names. They cannot break on a rename, and they are the shape the "
          "other readers should converge on.")
        a("")
        a("| Reader | Script | Upstream |")
        a("|---|---|---|")
        for p in pattern_scans:
            a(f"| `{p['skill']}` | `{p['script']}` | `{p['upstream'] or '?'}` |")
        a("")

    if self_reads:
        a("## Self-reads (excluded from the audit)")
        a("")
        a("These load the reading skill's OWN output, not an upstream workbook, so they "
          "are not a cross-skill contract.")
        a("")
        a("| Skill | Script | Function | Tab |")
        a("|---|---|---|---|")
        for s in self_reads:
            a(f"| `{s['skill']}` | `{s['script']}` | `{s['func']}` | `{s['name']}` |")
        a("")

    a("## Method and limits")
    a("")
    a("Static analysis only — no workbook is generated and no generator is executed. "
      "Specifically, this audit answers *does the upstream emit a tab with this name*, "
      "not *does that tab have the columns the reader indexes into*. Column-layout "
      "drift is a real second failure mode and is NOT covered here.")
    a("")
    a("Verdict definitions: **MATCH** upstream emits it · **ALIAS** declared legacy "
      "alternative whose preferred sibling matches · **FALLBACK** the same shape "
      "expressed as an `elif`/`or` branch · **SELF-AMBIG** the reading skill emits the "
      "same tab name and attribution came only from SKILL.md prose · **UNVERIFIABLE** "
      "upstream unresolved · **BREAK** nothing upstream emits it.")

    text = "\n".join(lines) + "\n"
    if "--stdout" in sys.argv:
        print(text)
    else:
        OUT_MD.parent.mkdir(parents=True, exist_ok=True)
        OUT_MD.write_text(text, encoding="utf-8")
        print(f"{OUT_MD.relative_to(REPO)} written: {len(findings)} assertions, "
              f"{len(chains)} chains, {counts['BREAK']} BREAK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
