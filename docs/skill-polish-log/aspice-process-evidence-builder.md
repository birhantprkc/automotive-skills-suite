# Polish log — aspice-process-evidence-builder

## 2026-07-15

**What's good**
- Frontmatter valid; description 483 chars (well under 1024 limit).
- All scripts `py_compile` clean; smoke test green: sample JSON → 10-tab workbook, JSON status output correct (SWE.1, 2 BPs, 1 GP).
- Unlike its two ASPICE siblings (gap-analysis, improvement-plan), the `<input.json>` CLI argument is **genuinely consumed** — process info, BP/GP evidence, and work products are all plumbed from JSON into tabs 00–05. Negative data point for the family-wide ignored-arg sweep: this builder is NOT affected.
- All 10 sheet names ≤31 chars (Excel limit); no reviewer-probe mismatch suspected.

**What to fix**
1. **Scaffold-only tabs 06/08, hard-coded tab 07** (same defect class logged on aspice-improvement-plan-builder 2026-07-15): `create_performance_tab`, `create_improvement_tab` render headers only and take no data; `create_quantitative_tab` hard-codes 4 metric names with no values. SKILL.md Step 4 explicitly asks users for performance records, CL3+ quantitative metrics, and improvement history — all silently dropped. Sample JSON also lacks these keys, so the gap is invisible in smoke tests.
2. Sample JSON should gain `performance_records`, `quantitative_metrics`, `improvements` keys once (1) is wired.

**Suggested edits**
- Add `performance_records`/`quantitative_metrics`/`improvements` top-level JSON keys; thread them through `generate_evidence` into tabs 06–08 following the tab-03/04/05 pattern (headers + striped body rows).
- Extend `examples/sample_evidence_input.json` with 1–2 rows per new key.

**Severity:** med — workbook generates and core evidence tabs work, but a third of the promised content (Step 4) is a silent no-op, which matters for CL3+ assessments specifically.

**Fix applied this run:** none — wiring three tabs is beyond small-fix scope per polish rules; logged for a PLAN-week fix alongside the sibling scaffold-tab findings.

## 2026-08-04

**What's good**
- The 2026-07-15 finding (1) is now fixed. Tabs 06/07/08 are wired to real input data.
- Frontmatter still valid, description unchanged at 483 chars; both scripts `py_compile` clean.
- Smoke test green on the extended sample: 10 tabs, `{"bp_count":2,"gp_count":1,"wp_count":2,"performance_record_count":2,"quantitative_metric_count":4,"improvement_count":2}`.
- Back-compat regression run with the three new keys removed: still 10 tabs, tab 07 falls back to the old four-name blank template, tabs 06/08 render headers only. Old input JSON keeps working unchanged.

**Fix applied this run**
- `generate_aspice_evidence.py`: `create_performance_tab`, `create_quantitative_tab` and `create_improvement_tab` now take a data list and render striped body rows following the tab-03/04/05 pattern. New top-level JSON keys `performance_records` (`id`/`type`/`date`/`findings`/`location`), `quantitative_metrics` (`metric`/`period`/`value`/`target`/`status`) and `improvements` (`id`/`description`/`date`/`impact`) are threaded through `generate_evidence`. All three are optional.
- The hard-coded four-metric list on tab 07 is retained **only** as the empty-input fallback and is now named `DEFAULT_METRIC_TEMPLATE` with a comment saying so.
- JSON status line extended with `wp_count`, `performance_record_count`, `quantitative_metric_count`, `improvement_count` so the silent-drop class of defect is visible in future smoke tests.
- `examples/sample_evidence_input.json`: 2 performance records, 4 quantitative metrics, 2 improvements added.
- `SKILL.md` Step 4 rewritten as a content → JSON key → row fields → tab table, with the optionality and tab-07 fallback stated explicitly.

**What's left**
- Nothing outstanding on this skill. Finding (1) closed, finding (2) closed.
- Sibling scaffold-tab findings on `aspice-improvement-plan-builder` (2026-07-15) are unaffected by this run and still open.

**Severity:** was med — now resolved.
