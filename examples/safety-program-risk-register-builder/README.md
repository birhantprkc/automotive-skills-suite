# safety-program-risk-register-builder — example

**What this skill produces:** 8-tab safety program risk register workbook (Title Page, Document Control, Risk Catalog, Mitigation Plan, Contingency Plan, Risk Trend, Escalation Log, References) covering ISO 26262-2 Clause 7 program-management risks — resource gaps, tool qualification gaps, supplier delays, late requirements changes, compliance risks.
**Typical input shape:** JSON with `project` (`name`, `doc_id`, `target_asil`), `reporting_period` (`start`, `end`), and `risks[]` (`id`, `category`, `description`, `owner`, `likelihood` 1-5, `impact` 1-5, `mitigation`, `contingency`, `status`).
**Expected output:** `<name>.xlsx` with one Risk Catalog row per input risk and a formula-driven score (`=likelihood*impact`); Risk Trend and Escalation Log ship as header-only scaffolds.
**Sample I/O:** `python scripts/generate_risk_register.py input.json output.xlsx && python scripts/recalc.py output.xlsx` — a 1-risk input yields all 8 tabs, 1 catalog row, 1 mitigation row, 1 contingency row.
**Paired reviewer:** `safety-program-risk-register-checklist-reviewer` — its probe expects exactly the 5 data-bearing sheets emitted here.
