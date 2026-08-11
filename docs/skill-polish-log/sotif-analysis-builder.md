# Polish log — sotif-analysis-builder

## 2026-06-09 (W24 POLISH, first pass)

**Tracking issue:** #20 (W24 polish target, label `sotif`)
**Mode:** POLISH · **Severity:** low (no blocking issues found)
**In-place fix applied:** none required (see rationale)

### What's good
- **Frontmatter is valid and complete.** Required fields `name` and `description`
  both present; `description` is 619 chars, comfortably under the 1024-char ceiling.
  The description correctly frames SOTIF as distinct from ISO 26262 random-HW faults,
  which is the single most important triggering distinction for this skill.
- **Body is coherent and self-consistent.** The "Output structure (12 tabs)" header
  matches the table exactly (rows 00–11 = 12 tabs). The tab inventory in the body
  lines up with the tab list implied by the description.
- **Schema/example/generator are aligned.** Example input
  `examples/sample_sotif_input_aeb.json` has top-level keys
  `[system, functions, odd_definition, performance_limitations,
  functional_insufficiencies, triggering_conditions, hazardous_behaviors,
  scenarios, acceptance_criteria]` and every one is consumed by
  `scripts/generate_sotif_analysis.py` via a matching `data.get(...)`. No orphan
  fields, no fields the generator reads that the example omits.
- **Scripts are syntactically sound.** `generate_sotif_analysis.py` and `recalc.py`
  both parse without error. No `TODO`/`FIXME`/`placeholder`/`lorem` markers anywhere
  in the archive.
- **Correct cross-reference.** "When to use" routes random-HW-failure hazards to
  hara-builder, reinforcing the SOTIF-vs-FuSa boundary.

### What to fix
- Nothing blocking. The skill is in good health.

### Suggested (non-blocking) edits for a future pass
- **Quadrant terminology consistency (cosmetic):** the body uses both the standard
  ISO 21448 4-quadrant labels and the prose "Known/Unknown × Safe/Unsafe". These
  agree, but a one-line legend near tab 09 would remove any ambiguity for new users.
- **Acceptance-criterion singular/plural:** prose refers to "Acceptance criterion"
  (tab 10) while the input key is `acceptance_criteria` (plural). The generator
  already keys on the plural, so this is purely descriptive — worth a one-word
  harmonization only if the file is opened for another reason.
- **Reference freshness:** `references/iso21448_clauses.md` cites the §6 concept /
  §5 scenario taxonomy structure; confirm against the current ISO 21448:2022 clause
  numbering on a future content pass (low priority — structure is unchanged).

### Rationale for no in-place change
Per POLISH discipline, edits are limited to small, obvious, unambiguous fixes
(typo, over-length description, missing required frontmatter). None of those
conditions are present here. The suggestions above are content-judgement calls,
not mechanical fixes, so they are logged for a future deliberate pass rather than
applied blind. A small honest commit beats a wrong one.

### Net assessment
Healthy skill. The 🟡 staleness flag in STATUS.md is **date-based, not
quality-based** — the file simply hasn't been edited since 2026-05-01. This review
satisfies the standing SOTIF-coverage mandate (SOTIF was the only zero-touch domain
in the May KPI); the domain has now had a documented quality pass.

---

## 2026-08-11 (POLISH pass 2) — severity: **medium**, changes applied

Slot assigned by `WEEK-2026-W33.md`: Tuesday -> #48 (stub tail). The stub was written,
but running the generator first turned up a real defect, so this pass is not docs-only.

### What's good
- Generator runs clean on the shipped AEB fixture and reports an honest summary
  (`functions: 2, performance_limitations: 3, functional_insufficiencies: 3, tabs: 12`).
- The paired reviewer probes by **sheet-name keyword**, not by fixed index, so tab renames
  are non-breaking as long as the distinguishing keyword survives. Verified before editing.
- No other skill in the repo reads this builder's tab names (grepped all 152 archives), so
  the blast radius of a rename is exactly one skill.

### What was fixed
Three emitted sheet names exceeded **Excel's hard 31-character limit**, and openpyxl was
warning on every run (`Title is more than 31 characters. Some applications may not be able
to read the file`). openpyxl does not truncate — it writes the over-length name through, so
the shipped workbook was technically malformed:

| Tab | Before | Len | After | Len |
|-----|--------|-----|-------|-----|
| 03 | `03_Functional_Performance_Specification` | 39 | `03_Functional_Perf_Spec` | 23 |
| 07 | `07_Triggering_Conditions_Catalog` | 32 | `07_Triggering_Conditions` | 24 |
| 09 | `09_Scenario_Quadrant_Classification` | 35 | `09_Scenario_Quadrants` | 21 |

`SKILL.md`'s "Output structure (12 tabs)" table was updated to match. Regenerated and
verified: 12 tabs, zero over-limit names, no warning.

**Second-order fix, free of charge.** The reviewer's `_find_sheet_by_keywords(["performance"])`
returns the *first* matching sheet. Tab 03 previously contained "Performance" and sorts before
tab 05, so the probe was silently reading **tab 03 (function names) as the performance-limitation
table** — `functions_with_performance` came back as `[{'function': 'Function ID', 'limitation':
'Function Name'}, ...]`. Dropping "Performance" from tab 03's name makes tab 05 the unique match.
Confirmed against both the old and new workbook.

### Found, NOT fixed (deliberate descope)
Two defects in `sotif-analysis-checklist-reviewer/scripts/sotif_analysis_probe.py`. They
interact, so fixing one alone makes the output *worse*, and they belong to the reviewer, not
this builder:

1. **Insufficiency keyword never matches.** The probe searches `["insufficiency",
   "insufficient"]`; the tab is `06_Functional_Insufficiencies`. Neither string is a substring
   of "insufficiencies", so `functional_insufficiencies_count` is **always 0** — a permanent
   false negative. One-word fix: search for `"insufficienc"`.
2. **Header row counted as data.** Every generator tab uses r1 banner / r2 blank / r3 header /
   r4+ data, but the probe iterates from `row 2` and counts any row with cols 1-2 populated —
   so the header lands in the count. The 3-row limitation table probes as **4**.

Fixing (1) without (2) flips the insufficiency check from a false FAIL to a PASS carrying an
inflated count — an inflated number inside an audit artifact is worse than an obvious zero.
They ship together or not at all, and (2) plausibly affects other reviewer probes sharing this
banner/blank/header layout, which needs a look before editing. Captured as a follow-up.

### Repo-wide finding
The over-length sheet name is **not** local to this skill. A read-only scan of all 152 archives
found **19 over-limit names across 10 skills** — see `docs/sheet-name-length-audit.md`, written
this run. Worst offender is `triggering-conditions-builder` with six, topping out at 44
characters. No issue was opened: POLISH mode is not authorized to create issues, so Monday's
PLAN run should pick this up.

### Net assessment
Downgraded from "healthy, docs-only" (the 2026-06-09 pass) to **had a shipping defect**. The
earlier pass reviewed the file and did not run it — that is the lesson worth carrying: for a
builder skill, *execute the generator* before declaring it clean. #48's stub-tail DoD is now
met, plus a fix the plan did not anticipate.
