# Polish log — `_find_header_row` batch (24 reviewers, issue #63)

## 2026-09-23 (W39 target 2 / issue #63) — autonomous POLISH pass

**Scope:** `_find_header_row()` in the probe module of 24 checklist reviewers (apqp-plan, aspice-assessment,
aspice-gap-analysis, aspice-improvement-plan, aspice-process-evidence, control-plan, cs-concept, cs-goals,
dfmea, dia, fmeda, hara, hsi, hw-architecture, hw-safety-reqs, pfmea, ppap, safety-case, safety-plan, sw-arch,
sw-fmea, sw-hsis, sw-sr, tara). `fmeda-builder/scripts/tsc_reader.py` also defines a `_find_header_row` but with
different logic and no `>= 3` literal; out of scope and untouched.
**Severity:** MED (was filed HIGH; see "What the measurement said")

### What the measurement said — the issue's fix would have shipped two regressions

The definition of done in #63 was "lower the gate to `>= 2` in all 24". Before touching anything I built every
paired builder's output from its own sample input (full chains: hara → fsc → tsc → fmeda / hsi → sw-hsis /
hw-arch / hw-sr / sw-arch / sw-fmea / sw-sr; tara → cs-goals → cs-concept; item-definition + chain → safety-case;
11 standalone builders; ppap-package) and diffed, per worksheet, which row each reviewer's function selects
under `>= 3` versus a blanket `>= 2`:

| Change in selected header row | Sheets |
|---|---|
| 0 → found (tab previously unlocated) | 48 |
| **found → a different, earlier row** | **2** |

The two moved rows are exactly the risk the plan named:

- `control-plan` `02_Header_Block`: real header row 11 → row 3 (`Control Plan Number:` / `CP-ESC-2026-001`)
- `ppap` `02_PSW_Part_Submission_Warrant`: real header row 17 → row 5 (`Part Name` / `ESC … Module`)

A 2-cell key/value row above a real header pre-empts it. So the blanket change fails its own regression guard
and was **not** applied.

### Fix applied — prefer a 3-cell header, fall back to 2

Same loop, same short-text/no-formula test, one change in selection policy: a row with ≥3 cells returns
immediately (identical to before); the first qualifying 2-cell row is remembered and returned only if the scan
finds no ≥3-cell row. By construction this cannot move a header that was found before — it can only locate one
that was not. Two textual variants existed (nested-if and a one-line `return r, {…}` in the two aspice
improvement/evidence probes); both were rewritten by one script that asserts exactly one `>= 3`, one return and
one `return 0, {}` per function before editing. The `hara` docstring was updated to say so.

### Verification (run from the repacked archives, not the working copy)

1. **Header differential, all 24 × every sheet of the paired builder output:** 48 gained, **0 moved**.
2. **Full reviewer regression sweep:** every one of the 24 `generate_checklist.py` run before and after over its
   builder's output, every populated row of every checklist tab compared (timestamps masked): **2,616 rows,
   0 differ.** A single `sw-fmea` row differed on an earlier pass — `ASIL D/QM` vs `ASIL QM/D` in a finding
   string — and was shown to flip between three identical *unpatched* runs, i.e. pre-existing set-iteration
   nondeterminism, unrelated.
3. **Synthetic acceptance workbook** (two-column-only tab / 2-cell key:value row above a 3-col header / title-only
   tab): old = `(0, 3, 0)` in all 24, new = `(3, 3, 0)` in all 24. A blanket `>= 2` would return `2` for the
   middle case.
4. **Archive integrity:** each of the 24 archives differs from HEAD in exactly one member (the probe), with an
   identical member list; all other entries copied byte-for-byte; `testzip()` clean; no `__pycache__` introduced.

### What the measurement also said — neither "live symptom" was live

The plan and the issue named two present-day symptoms, `cs-concept` `09_References` (`Reference`/`Source`) and
`sw-fmea` `04_SW_Failure_Mode_Library` (`SWC Type`/`Failure Mode`), and the DoD asked for their bound checks to
move from NO/NA to a real verdict. **No check is bound to either tab through this function**, which is why the
sweep shows zero verdict change:

- `cs_concept_probe.py` never reads `09_References` at all.
- `sw_fmea_probe.py` does read `04_SW_Failure_Mode_Library`, now locates its header, but resolves the ID column
  with `["fm id", "mode id", "id"]` — the tab has no ID column, so zero rows are collected either way — and
  `failure_modes_library` feeds only an informational count in the run summary, not any check.
- A third genuine two-column header, `cs-goals` `07_References` (`Reference`/`Description`), was missed by the
  planning scan; it is also not read by any check.

So #63 is fixed as **latent hardening with a zero-diff proof**, not as a repair of an observed false pass.
Severity downgraded HIGH → MED accordingly. The static scan that sized this (literal `>= 3` + two-item header
assignments) was right about the literal and wrong about consumption; a producer-side scan cannot see whether
a consumer reads the tab.

### Noticed, not touched

- Most of the 48 "gained" headers are not headers: title pages and reference tabs where the first key:value row
  is now treated as a header map. Harmless today (no check reads those maps — proven by the sweep) but it means
  the 2-cell fallback is a weak signal; a reviewer that starts reading a title page by header must not trust it.
- `sw-fmea` probe ID-column candidates don't match the builder's library schema (LOW).
- `sw-fmea` reviewer residual-risk finding text is nondeterministic (`D/QM` vs `QM/D`) — sort the set (LOW).

### Found during the sweep — two skills that cannot run at all (HIGH, separate skills, not fixed here)

Building the safety-case input exposed a truncated file; a follow-up `ast.parse` over all 849 `.py` files in
all 152 archives plus a pyflakes undefined-name pass found exactly two dead skills, both shipped broken in their
initial commits:

- **`safety-case-builder`** — `scripts/multi_xlsx_reader.py` ends mid-token at line 161 (`retu`), so
  `read_all_artifacts()` raises `NameError` on every run. The 2026-06-17 polish pass rated this skill
  "exemplary" without executing it. Verified fix (scratch copy, full 15-tab build succeeded):
  `return {"hara": hara_data, "fsc": fsc_data, "tsc": tsc_data, "fmeda": fmeda_data}` — matches every
  `artifacts.get(...)` at the call sites. Separately, `examples/sample_safety_case_input_esc.json` hardcodes
  absolute `/sessions/vigilant-ecstatic-maxwell/...` paths that exist on no machine.
- **`bus-load-analysis-checklist-reviewer`** — `scripts/check_definitions.py` ends mid-dict at line 191
  (`"18_no_formula_errors": ch`), a `SyntaxError` on import. All 28 `check_NN_*` functions are defined; only the
  `CHECKS` mapping for 18–28 is missing, so the repair is mechanical.
