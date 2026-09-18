# traceability-matrix-checklist-reviewer — example

**What this skill produces:** A confirmation-measures checklist xlsx over a traceability matrix workbook — **25 checks** (`TM001`–`TM025`, counted from `scripts/check_definitions.py` on 2026-09-18) against ISO 26262, ISO/SAE 21434 and IEEE 1012, written into **5 tabs**: `Title`, `Checklist`, `Findings`, `Dashboard`, `Signoff`. Coverage is bidirectional: trace completeness, orphan identification, coverage analysis, gap identification, validation-rule compliance.

**Typical input shape:** A traceability matrix xlsx — normally `traceability-matrix-builder` output, best-effort on others. `scripts/trace_probe.py` reads `Title`, `Trace Source Catalog`, `Traceability Matrix`, `Coverage Analysis`, and the three orphan tabs (`Orphan Requirement`, `Orphan Stakeholder Need`, `Orphan Test Case`). As of `302660e` the probe locates coverage metrics and orphan rows **by label rather than by a fixed row window**, so a matrix whose tabs grew or shifted still parses.

**Expected output:** `<name>_checklist.xlsx` rating each check, with the `Findings` tab carrying check ID, measure and evidence for every non-pass. The source matrix is never modified.

**Sample I/O:**

```bash
python scripts/generate_checklist.py matrix.xlsx output_checklist.xlsx
python scripts/recalc.py output_checklist.xlsx      # optional
```

**What the numbers should look like.** On `examples/traceability-matrix-builder/sample_input.json` built through the repaired builder, the reviewer scores **0 FC / 20 LC / 5 NO**; an empty workbook scores **0 FC / 7 NO / 5 NA**. Before the 2026-09-08 repair (#59) those were `2 FC / 22 LC / 1 PC` and *identical for an empty workbook* — the reviewer certified nothing as almost-compliant. If a run ever returns the same spread for a populated and an empty matrix again, that regression is back. `TM005`/`TM006`/`TM007` were corrected and `TM008`/`TM009` implemented in the same change; **12 checks that cannot be machine-verified are explicitly labelled `AUTO-SUGGEST DRAFT`** rather than silently passing, which is what the old hard-coded `LC` fall-through did.

**Known issue (not fixed here):** this archive ships three `scripts/__pycache__/*.pyc` files. Harmless at runtime but contaminating — repacking a `.skill` zip is POLISH-mode work, so it is recorded rather than corrected. Worth a suite-wide `__pycache__` scan.

**Paired builder:** `traceability-matrix-builder`, rewritten in the same commit so its input reaches all 11 advertised tabs and coverage/orphans are derived rather than hard-coded.
