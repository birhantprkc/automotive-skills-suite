#!/usr/bin/env python3
"""Regenerate STATUS.md from the skills/ directory.

Pairing rule, in priority order, for every `<base>-builder.skill`:
  1. `<base>-checklist-reviewer.skill`
  2. `<base>-reviewer.skill`
  3. an explicit alias row in docs/PAIRING_ALIASES.md

The alias table is PARSED, not hard-coded. docs/PAIRING_ALIASES.md is the single
source of truth and states that any STATUS regeneration MUST honor it; an
inline/ad-hoc regeneration dropped those two pairings on 2026-08-13 and reported
two false orphans. Parsing the table is what stops that recurring — add an alias
row there and this script picks it up with no code change.

Usage:  python scripts/regen_status.py           # writes STATUS.md at repo root
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import date, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
ALIASES_MD = REPO / "docs" / "PAIRING_ALIASES.md"
STATUS_MD = REPO / "STATUS.md"

STALE_DAYS = 30

# Domain inference: ordered (regex, domain). First match wins, so more specific
# prefixes must precede broader ones (e.g. safety-program-* before safety-*).
DOMAIN_RULES: list[tuple[str, str]] = [
    (r"^(safety-program-|safety-gate-|wp-|change-impact-|lessons-learned)", "program-mgmt"),
    (r"^(verification-|validation-|test-|traceability-|vv-)", "v&v"),
    (r"^(hara|fsc|tsc|hw-|sw-|safety-)", "safety"),
    (r"^(tara|cs-|incident-|secure-coding)", "cyber"),
    (r"^(sotif-|triggering-)", "sotif"),
    (r"^(apqp|dfmea|pfmea|ppap|control-plan)", "quality"),
    (r"^aspice-", "aspice"),
    (r"^(dbc|ldf|flexray|automotive-ethernet|communication-matrix|bus-load|gateway|arxml)", "comms"),
    (r"^(uds|dtc|cdd|odx|dem)", "diagnostics"),
    (r"^autosar-", "autosar"),
    (r"^(a2l|dcm|calibration-)", "calibration"),
    (r"^mbse-", "mbse"),
    (r"^sysml-", "sysml"),
    # --- Supplemental: builders whose names match none of the prefix rules above.
    # These nine were previously assigned by hand on each ad-hoc regeneration.
    # Pinning them here keeps the label stable run-to-run.
    # `msa-gage-rr` and `spc-chart` were carrying "safety" before 2026-08-14;
    # Gage R&R and SPC are IATF 16949 quality tools, so both are corrected to
    # "quality" here. The other seven preserve their previous labels.
    (r"^(5-why|8d-problem-solving|fishbone|msa-gage-rr|spc-chart)", "quality"),
    (r"^(dia|fmeda|hsi|item-definition)", "safety"),
]


def infer_domain(base: str) -> str:
    for pattern, domain in DOMAIN_RULES:
        if re.match(pattern, base):
            return domain
    return "uncategorized"


def load_aliases() -> dict[str, str]:
    """Parse the builder -> reviewer alias table out of docs/PAIRING_ALIASES.md.

    Reads markdown table rows whose first two cells are backticked .skill
    filenames. Header/separator rows and prose are ignored.
    """
    aliases: dict[str, str] = {}
    if not ALIASES_MD.exists():
        return aliases
    row_re = re.compile(
        r"^\|\s*`([A-Za-z0-9._-]+\.skill)`\s*\|\s*`([A-Za-z0-9._-]+\.skill)`\s*\|"
    )
    for line in ALIASES_MD.read_text(encoding="utf-8").splitlines():
        m = row_re.match(line.strip())
        if m:
            aliases[m.group(1)] = m.group(2)
    return aliases


def last_touched(relpath: str) -> str:
    out = subprocess.run(
        ["git", "log", "-1", "--format=%ad", "--date=short", "--", relpath],
        cwd=REPO, capture_output=True, text=True,
    ).stdout.strip()
    return out or "—"


def main() -> int:
    if not SKILLS.is_dir():
        print(f"ERROR: {SKILLS} not found", file=sys.stderr)
        return 1

    present = {p.name for p in SKILLS.glob("*.skill")}
    aliases = load_aliases()
    builders = sorted(n for n in present if n.endswith("-builder.skill"))
    reviewers = sorted(n for n in present if "reviewer" in n)

    today = date.today()
    rows = []
    orphan = stale = fresh = 0
    alias_used: list[tuple[str, str]] = []

    for b in builders:
        base = b[: -len("-builder.skill")]
        reviewer = None
        for cand in (f"{base}-checklist-reviewer.skill", f"{base}-reviewer.skill"):
            if cand in present:
                reviewer = cand
                break
        if reviewer is None and b in aliases and aliases[b] in present:
            reviewer = aliases[b]
            alias_used.append((b, reviewer))

        touched = last_touched(f"skills/{b}")
        if reviewer is None:
            flag, orphan = "🔴", orphan + 1
        else:
            try:
                age = (today - datetime.strptime(touched, "%Y-%m-%d").date()).days
            except ValueError:
                age = 10**6
            if age > STALE_DAYS:
                flag, stale = "🟡", stale + 1
            else:
                flag, fresh = "🟢", fresh + 1

        rows.append(
            f"| {b} | {infer_domain(base)} | {reviewer or '— none —'} | {touched} | {flag} |"
        )

    paired = len(builders) - orphan
    pct = round(100 * paired / len(builders)) if builders else 0

    lines = [
        "# Skill Suite Status",
        "",
        f"_Regenerated {today.isoformat()} by autonomous daily run "
        f"(`scripts/regen_status.py`)._",
        "",
        "| Builder | Domain | Paired Reviewer | Last Touched | Flag |",
        "|---|---|---|---|---|",
        *rows,
        "",
        "## Summary",
        "",
        f"- Builders: {len(builders)} · Reviewers: {len(reviewers)} · "
        f"Total skill files: {len(present)}",
        f"- Paired builders: {paired}/{len(builders)} ({pct}%)",
        f"- 🔴 Orphan builders (no reviewer): {orphan}",
        f"- 🟡 Paired but stale ({STALE_DAYS}+ days untouched): {stale}",
        f"- 🟢 Paired and fresh (≤{STALE_DAYS} days): {fresh}",
    ]
    if alias_used:
        lines += [
            "",
            f"_{len(alias_used)} builder(s) paired via `docs/PAIRING_ALIASES.md` "
            "rather than filename convention: "
            + ", ".join(f"`{b}` → `{r}`" for b, r in alias_used)
            + "._",
        ]

    STATUS_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(
        f"STATUS.md written: {len(builders)} builders, {paired} paired "
        f"({len(alias_used)} via alias), {orphan} orphan, {stale} stale, {fresh} fresh"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
