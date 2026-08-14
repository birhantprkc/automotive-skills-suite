# sotif-analysis-checklist-reviewer — example

**What this skill produces:** A confirmation-measures checklist xlsx over an ISO 21448 (SOTIF) Analysis workbook — 7 tabs: Title, General Info, Guide, Summary (statistical roll-up + findings), **Confirmation Review (14 `cr_*` generic doc-quality checks)**, **SOTIF Analysis Assessment (14 `fsa_*` substantive checks per ISO 21448 §6)**, and **Acceptance Criterion Tracking** (measurability and coverage summary). 28 rated checks total, counted from `scripts/check_definitions.py` on 2026-08-14.

**Typical input shape:** A completed SOTIF Analysis xlsx — optimal on `sotif-analysis-builder` output (12 tabs), best-effort on others. `scripts/sotif_analysis_probe.py` is the richest probe in the reviewer set: beyond Title-page metadata it captures the item-definition reference and version, the four ODD dimensions separately (`odd_scenery_rows`, `odd_environment_rows`, `odd_dynamic_rows`, `odd_driver_state_rows`), `performance_limitations_count`, `functional_insufficiencies_count` with per-insufficiency detail, `triggering_conditions_count` **broken down by category**, `hazardous_behaviors_count`, the `scenario_quadrant_classification` histogram, and both `acceptance_criteria_count` and `acceptance_measurable`.

**Expected output:** `<name>_checklist.xlsx` with each check rated FC / LC / PC / NO / NA, or `Pending` with a `(Reviewer to verify)` draft. The source SOTIF Analysis is never modified.

**Sample I/O:**

```bash
python scripts/generate_checklist.py AEB-sotif-analysis.xlsx output_checklist.xlsx
```

Run against the builder's shipped AEB fixture, the summary reports probed counts (ODD dimensions, performance limitations, triggering conditions, scenario classes, acceptance criteria) alongside the ratings distribution. Four checks carry most of the signal:

- **ODD must span all four dimensions** — scenery, environment, dynamics, driver state. A zero in any of the four `odd_*_rows` fields drives a PC.
- **Triggering conditions must cover six categories** — environmental, sensor, road infrastructure, other road user, system state, driver state. The per-category breakdown makes a missing category visible rather than hidden inside a total.
- **Every scenario must land in a quadrant** — Known Safe / Known Unsafe / Unknown Safe / Unknown Unsafe. Unknown Unsafe scenarios are surfaced by the headline check (#14) and each needs mitigation or explicit acceptance.
- **Acceptance criteria must be quantified** — `acceptance_measurable` below `acceptance_criteria_count` means some criterion is still qualitative, which fails the check.

**Paired builder:** `sotif-analysis-builder` — probes by sheet-name keyword rather than fixed index, so the tab renames of 2026-08-11 (`386191e`, Excel's 31-character sheet-name limit) did not break this reviewer.

> **Known probe defects — open, affects the numbers above.** Two interacting bugs in `scripts/sotif_analysis_probe.py` were found on 2026-08-11 and deliberately left unfixed (they belong to the reviewer, not the builder, and fixing either alone makes the output worse). Both are documented in `docs/skill-polish-log/sotif-analysis-builder.md`:
>
> 1. **`functional_insufficiencies_count` is always 0.** The probe searches for `"insufficiency"` / `"insufficient"`; the tab is `06_Functional_Insufficiencies` and neither string is a substring of "insufficiencies". A permanent false negative — the one-word fix is to search `"insufficienc"`.
> 2. **Header row counted as data.** Generator tabs use r1 banner / r2 blank / r3 header / r4+ data, but the probe iterates from row 2 and counts any row with columns 1–2 populated, so the header is included. A 3-row limitation table probes as 4.
>
> Until both are fixed together, treat insufficiency counts and any row count from this probe as unreliable. Ratings that depend on them should be re-checked by hand.
