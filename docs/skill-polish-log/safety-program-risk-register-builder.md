# Polish log — safety-program-risk-register-builder

## 2026-08-06 (autonomous POLISH pass, first pass on this skill)

Selected per priority rule (3) least-recently-touched builder (last touched 2026-05-02,
bulk-import wave) and because it is the open target of issue #49 — the last un-worked
W31 weekly target. `program-mgmt` had never received a polish pass before today.

### What's good

- Chain contract with `safety-program-risk-register-checklist-reviewer` is **intact**.
  The reviewer's `risk_probe.py` looks for exactly `Risk Catalog`, `Mitigation Plan`,
  `Contingency Plan`, `Escalation Log`, `Risk Trend` — all five are emitted under those
  exact names. No chain break here; #46's audit can mark this pair clean.
- Generator runs clean end-to-end on a 2-risk sample: 8 sheets, no exceptions,
  `py_compile` OK, no NUL padding (the May-01/02 fault family did not touch this file).
- Risk Score is a real formula (`=D{row}*E{row}`), not a baked constant, so an analyst
  editing likelihood/impact gets live recalculation. That's the right call.
- Scope framing in the doc is genuinely useful — it draws the line between *program*
  risk (delivery/assurance) and *functional hazard* (HARA territory) up front, which
  is the distinction users most often get wrong on this artifact.

### What to fix

| # | Finding | Severity | Status |
|---|---|---|---|
| 1 | SKILL.md advertised **9 tabs** including a `02 Risk Register Header`; generator emits **8** and has no such tab. Tab numbering downstream was off-by-one for tabs 03-08. | med | **fixed** |
| 2 | "Files in this skill" listed `references/methodology.md`, `references/risk_categories.md`, and `examples/sample_risk_register.json`. **None of the three ship in the archive.** | med | **fixed** |
| 3 | References tab wrote a live cell pointing at `references/risk_categories.md` — a dangling pointer to a file that does not exist, landing in the delivered workbook. | med | **fixed** |
| 4 | Step 4 told the presenter to call out "the **Risk Register** tab"; the tab is named `Risk Catalog`. | low | **fixed** |
| 5 | `Risk Trend` and `Escalation Log` are **empty scaffolds** — headers plus one placeholder string. Doc promised trend and escalation content. Same scaffold-tab family as the ASPICE bundle (#45). | med | documented, not built |
| 6 | Mitigation Plan → Status is **hardcoded `"In Progress"`** for every row. Per-risk `status` from input feeds only the Risk Catalog. | med | documented, not built |
| 7 | Contingency Plan → Trigger Criteria is auto-templated `"If <id> exceeds score threshold"` — same string for every risk, no threshold value. | low | documented, not built |
| 8 | Dead imports/constants: `datetime`, `Any`, `get_column_letter`, `Table`, `TableStyleInfo`, `LIGHT_BLUE`, `WARN_YELLOW`, `GREEN_OK`, `RED_BAD`, `GREY`. `RISK_CATEGORIES` was defined and unused — now consumed by the References fix. | low | partially resolved |

### Applied this pass

- SKILL.md: output table corrected to the true 8 tabs with true names and renumbered
  00-07; added an explicit **Known limitations** block naming findings 5/6/7 so the
  skill stops promising content it does not generate.
- SKILL.md: file listing reduced to what actually ships; added a line telling the user
  the Step 2 JSON block *is* the input template (there is no `examples/` file to point at).
- SKILL.md: Step 4 presentation bullets corrected — `Risk Catalog` name, and the two
  scaffold tabs now instruct the presenter to flag them as needing manual population.
- `generate_risk_register.py`: References tab no longer emits a dangling file pointer.
  It now inlines the permitted category values (from the previously-dead
  `RISK_CATEGORIES` constant) plus the scoring convention band definitions.

Verified post-repack: `py_compile` OK, archive `testzip` clean, generator reproduces
8 sheets with correct names, References tab renders the inlined values.

### Deliberately descoped

Findings 5, 6, and 7 all require **schema changes** — historical score entries for
trend, a `mitigation_status` field, a per-risk `escalation` block, and a numeric
threshold for contingency triggers. Changing the input schema means the reviewer's
checks RR-C15/C16 (contingency plan + trigger criteria) need re-verification against
the new shape, and that is a two-skill change, not a one-file edit. Not a same-day job.
Captured as a follow-up rather than half-done.

**Severity of remaining open items: medium.** Nothing here ships broken — the workbook
generates and the chain holds. The risk was that the documentation *oversold* the
artifact, so an analyst would present a "Risk Trend" tab that is empty. That gap is
now stated in the skill itself.
