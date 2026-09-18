# cs-goals-builder — example

**What this skill produces:** An ISO/SAE 21434 Cybersecurity Goals workbook — **8 tabs**, counted from the `create_sheet` calls in `scripts/generate_cs_goals.py` on 2026-09-18: `00_Title_Page`, `01_Document_Control`, `02_TARA_Echo`, `03_Cybersecurity_Goals`, `04_CAL_Determination`, `05_Asset_to_CSG_Map`, `06_CS_Concept_Handoff`, `07_References`. The tab list matches SKILL.md exactly — no count drift.

**Typical input shape:** A completed TARA xlsx, normally `tara-builder` output, plus an **optional** refinement JSON. `scripts/tara_reader.py` prefers tab `11_Cybersecurity_Goals` if present and falls back to `09_Risk_Determination`, deriving a CSG per row with Risk Value ≥ 3. It also walks `05_Threat_Scenarios` and `04_Asset_Inventory` to resolve assets. The refinement JSON (schema at the top of `generate_cs_goals.py`, worked example in `examples/sample_cs_goals_input_esc.json`) carries `item`, `target_cal`, `csg_refinements` keyed on `threat_scenario_id`, and `csg_overrides` keyed on `csg_id`.

**Expected output:** `<name>.xlsx` with one row per CSG in `03_Cybersecurity_Goals` — ID, threat reference, asset, goal text in *Prevent &lt;threat&gt;* form, CAL 1–4, cybersecurity property and owner — plus the CAL rationale in `04_CAL_Determination` and placeholder CSC rows in `06_CS_Concept_Handoff`. On the ESC fixture: 15 CSGs, CAL distribution 10 / 3 / 2. The JSON is the source of truth; the xlsx is derived, so regenerate rather than hand-editing.

**Sample I/O:**

```bash
python scripts/generate_cs_goals.py tara.xlsx output_goals.xlsx                  # auto CSG text + CAL
python scripts/generate_cs_goals.py tara.xlsx refinement.json output_goals.xlsx  # with refinement
python scripts/recalc.py output_goals.xlsx
```

Note the positional argument order: with two arguments the second is the *output*; with three the middle one is the refinement JSON.

**Check the goal text before trusting the chain.** Until `a2af2f1` (2026-09-16) `tara_reader` resolved columns against snake_case names (`asset`, `cs_goal_text`) with positional fallbacks. `tara-builder` emits human-readable headers (`Cybersecurity Goal`, `Risk Value`), so no alias ever matched and both columns silently took their positional default — goal text landed in `asset` and a bare risk integer landed in `cs_goal_text`. The output looked plausible and was wrong, end to end, all the way through `cs-concept-builder` and `cs-architecture-builder`. The fix added `_HEADER_ALIASES` / `_normalize_headers()` / `_col()` so columns resolve by name, plus `_build_asset_index()` for the upstream CSG tab, which has no asset column at all. A one-line sanity check on any new TARA source: if `cs_goal_text` is numeric, the reader is misaligned again.

**Known issue (not fixed):** `Cybersecurity_Property` is hard-coded to `Confidentiality` on every CSG, though the STRIDE category in the TARA determines it unambiguously. Fixing it means threading a new field through a payload schema that three downstream skills read — queued as a follow-up, see `docs/skill-polish-log/cs-goals-builder.md`.

**Paired reviewer:** `cs-goals-checklist-reviewer`. Chain position: `tara-builder` → **`cs-goals-builder`** → `cs-concept-builder` → `cs-architecture-builder`.
