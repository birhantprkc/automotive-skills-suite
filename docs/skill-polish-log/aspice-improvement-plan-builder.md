# Polish log — aspice-improvement-plan-builder

## 2026-07-15 (autonomous POLISH pass)

**What's good**
- Frontmatter complete (name + description, 513 chars, well under 1024).
- Clean SKILL.md: clear 6-step workflow, 11-tab output table matches generated workbook exactly.
- Scripts compile; sample JSON valid; consistent styling helpers (navy/light-blue theme shared with sibling ASPICE builders).
- Smoke test: 11 tabs generated, initiative rows populated, no exceptions.

**What to fix**
1. **Ignored `gap_analysis.xlsx` argument (HIGH, chain-break).** The CLI requires
   `<gap_analysis.xlsx>` but `generate_improvement_plan()` never opens it —
   `load_workbook` is imported and unused. Generation succeeds with a nonexistent
   path. The "02_Gaps_From_Analysis" echo tab is filled from the JSON `processes`
   key instead, so the advertised aspice-gap-analysis-builder → improvement-plan
   chain is not actually wired. Same defect class as the 2026-07-01 finding on
   aspice-gap-analysis-builder (ignored-arg).
2. **Tabs 04–09 are header-only scaffolds (MED).** `create_roadmap_tab`,
   `create_resources_tab`, `create_risks_tab`, `create_kpis_tab`,
   `create_communication_tab`, `create_pilot_tab` take no data and emit only
   title + header rows. SKILL.md Steps 3–4 instruct users to define timeline,
   resources, risks, KPIs, comms, and pilot — all of which are silently dropped.
   Sample JSON lacks those keys too, masking the gap.

**Suggested edits**
- Either implement gap-xlsx ingestion (read gap rows into 02 tab, cross-check
  initiative `gaps` IDs) or drop the argument and update SKILL.md/usage — pick one.
- Extend generator to consume `risks`, `kpis`, `roadmap`, `resources`,
  `communication`, `pilot` JSON keys; extend sample JSON to exercise them.
- Add the missing keys to examples/sample_improvement_plan_input.json.

**Severity:** high (chain-break) / medium (scaffold tabs)

**Action taken this run:** log only — both fixes exceed small-fix scope
(new parsing + data plumbing). No .skill modification.

## 2026-07-30

**Target selection:** #45 (`skill-bug`, `aspice`) — highest-priority open issue with work
remaining. Wednesday's scheduled run did not fire (last commit is Tuesday's 67c9072), so this
run picks up the Wednesday follow-up recorded in the 07-28 journal.

**What's good**
- Generator still compiles clean and emits all 11 tabs from the sample JSON; no NUL bytes.
- Paired reviewer (`aspice-improvement-plan-checklist-reviewer`) consumes only the produced
  workbook (`aspice_improvement_probe.py <xlsx>`), so the builder CLI signature was safe to
  change — same verification performed on the sibling before the 07-28 gap-analysis fix.

**Fix applied this run — finding 1 (ignored `gap_analysis.xlsx` argument, HIGH)**
Resolved as "make it honest", identical to the shim shipped for `aspice-gap-analysis-builder`
on 2026-07-28:
- `generate_improvement_plan()` signature reduced to `(input_json, output_xlsx)`.
- `__main__` accepts the legacy 3-argument form, drops the leading workbook path, and emits a
  `WARNING:` to stderr pointing at the 2-argument form. No existing call site breaks.
- Dead `load_workbook` import removed (imported, never used).
- Module docstring, SKILL.md Step 1, Step 5 usage block, and the tab-02 row reworded to state
  that gap rows are transcribed into the input JSON `processes` key, not read from a workbook.

**Smoke test**
| Case | Result |
|---|---|
| `py_compile` all scripts | OK |
| 2-arg form | exit 0, `{"status":"ok","tabs":11,"initiatives":1}` |
| legacy 3-arg form, nonexistent leading path | exit 0 + WARNING on stderr, 11 tabs |
| wrong arg count (1) | exit 1, usage on stderr |
| fresh unzip of re-zipped archive | regenerates 11 tabs |
| reviewer probe on output | unchanged (initiative_rows 1, has_owners/has_budget true, roadmap present) |
| NUL scan | clean |
| sheet-name length | max 21 chars, under Excel's 31 |

**Still open — finding 2 (scaffold tabs 04–09, MED)**
Untouched and deliberately descoped. `create_roadmap_tab`, `create_resources_tab`,
`create_risks_tab`, `create_kpis_tab`, `create_communication_tab`, `create_pilot_tab` still
take no data and emit headers only. Wiring them is a schema change across three ASPICE
builders plus their example inputs and needs the input-driven-vs-fill-in-template decision
still recorded as blocking in the 07-28 journal.

**Severity after this run:** high finding closed · medium finding (scaffold tabs) open.
