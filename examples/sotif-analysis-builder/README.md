# sotif-analysis-builder — Example

**What this skill produces:** An ISO 21448 (SOTIF) analysis xlsx — exactly 12 tabs, verified against the generator on 2026-08-11: `00_Title_Page`, `01_Document_Control`, `02_Item_Definition_Reference`, `03_Functional_Perf_Spec`, `04_ODD_Definition`, `05_Performance_Limitations`, `06_Functional_Insufficiencies`, `07_Triggering_Conditions`, `08_Hazardous_Behavior_Catalog`, `09_Scenario_Quadrants`, `10_Acceptance_Criterion`, `11_References`. The analysis covers hazards arising from performance limitations of the intended functionality — the gap between specification and reality — as distinct from random hardware faults (ISO 26262).

**Typical input shape:** A single JSON file (schema documented in `scripts/generate_sotif_analysis.py`; worked example shipped as `examples/sample_sotif_input_aeb.json`) with: `system` metadata (name, abbr, project, doc_id, revision, date, author); `functions[]` each with id / name / description / `kinetic_authority`; `odd_definition` split into `scenery`, `environment`, dynamic elements and driver state; `performance_limitations[]` keyed to function IDs; `functional_insufficiencies[]`; triggering conditions; scenarios for quadrant classification; and `acceptance_criteria[]` carrying the quantified residual-risk target.

**Expected output:** `<system>-sotif-analysis.xlsx`. Tab 05 enumerates sensor/latency/algorithm limits per function, tab 06 the resulting insufficiencies, tab 07 the triggering conditions that expose them, tab 08 the (function x insufficiency x triggering condition) -> hazardous vehicle behavior rows, tab 09 the Known Safe / Known Unsafe / Unknown Safe / Unknown Unsafe quadrant assignment per scenario, and tab 10 the quantified acceptance criterion per safety goal.

**Sample I/O:** Running the shipped AEB fixture —

```bash
python scripts/generate_sotif_analysis.py examples/sample_sotif_input_aeb.json AEB-sotif-analysis.xlsx
python scripts/recalc.py AEB-sotif-analysis.xlsx
```

returns the generator summary
`{"system": "Autonomous Emergency Braking", "functions": 2, "performance_limitations": 3, "functional_insufficiencies": 3, "scenarios": 2, "acceptance_criteria": 2, "tabs": 12}`
— e.g. limitation `L01` (camera cannot reliably detect stationary vehicles beyond 100 m) and insufficiency `I01` (motorcycles undetected in lateral fields due to small profile) flow through to the hazardous-behavior and quadrant tabs.

**Paired reviewer:** `sotif-analysis-checklist-reviewer` — probes this workbook by sheet-name keyword (not fixed index), so renaming a tab is safe as long as its keyword survives.

> **Note (2026-08-11):** tabs 03, 07 and 09 were shortened this run — they previously ran 39 / 32 / 35 characters against Excel's 31-character sheet-name limit. Workbooks generated before this date carry the older, over-length names.
