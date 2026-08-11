# Sheet-name length audit — Excel's 31-character limit

_Generated 2026-08-11 by automotive-skills-daily-standup (POLISH mode). Read-only scan; no
`.skill` file was modified by the audit itself._

## Why this matters

Excel enforces a **hard 31-character limit** on worksheet names. `openpyxl` does not truncate
an over-length title — it emits

```
UserWarning: Title is more than 31 characters. Some applications may not be able to read the file
```

and writes the name through anyway. The resulting `.xlsx` is out of spec: Excel typically
reports the file as needing repair and renames the offending sheets on open. Any downstream
reviewer skill that looks a sheet up by exact name then misses it.

## Method

All 152 `.skill` archives were extracted to a scratch directory and every `*.py` scanned for
`create_sheet("...")` literals. Names longer than 31 characters are listed below. Dynamically
constructed names (f-strings, variables) are **not** covered by this scan — the real count may
be higher.

## Findings — 19 names across 10 skills

| Skill | Sheet name | Length | Over by |
|-------|-----------|--------|---------|
| `5-why-builder` | `06_Verification_of_Effectiveness` | 32 | 1 |
| `8d-problem-solving-builder` | `07_D6_Implement_Corrective_Actions` | 34 | 3 |
| `8d-problem-solving-builder` | `06_D5_Permanent_Corrective_Actions` | 34 | 3 |
| `incident-response-plan-builder` | `06_Coordinated_Disclosure_Policy` | 32 | 1 |
| `odx-builder` | `Communication Parameters (ODX-C)` | 32 | 1 |
| `secure-coding-guidelines-builder` | `08_Authentication_Authorization_Rules` | 37 | 6 |
| `secure-coding-guidelines-checklist-reviewer` | `Secure Coding Guidelines Assessment` | 35 | 4 |
| `sotif-analysis-builder` | `03_Functional_Performance_Specification` | 39 | 8 |
| `sotif-analysis-builder` | `09_Scenario_Quadrant_Classification` | 35 | 4 |
| `sotif-analysis-builder` | `07_Triggering_Conditions_Catalog` | 32 | 1 |
| `sotif-validation-strategy-builder` | `02_Acceptance_Criterion_Reference` | 33 | 2 |
| `sotif-validation-strategy-builder` | `09_Acceptance_Criterion_Tracking` | 32 | 1 |
| `sw-sr-builder` | `06_Verification_Methods_per_ASIL` | 32 | 1 |
| `triggering-conditions-builder` | `05_Road_Infrastructure_Triggering_Conditions` | 44 | 13 |
| `triggering-conditions-builder` | `06_Other_Road_User_Triggering_Conditions` | 40 | 9 |
| `triggering-conditions-builder` | `03_Environmental_Triggering_Conditions` | 38 | 7 |
| `triggering-conditions-builder` | `08_Driver_State_Triggering_Conditions` | 37 | 6 |
| `triggering-conditions-builder` | `07_System_State_Triggering_Conditions` | 37 | 6 |
| `triggering-conditions-builder` | `09_Combined_Triggering_Conditions` | 33 | 2 |

## Status

`sotif-analysis-builder` (3 names) was **fixed on 2026-08-11** as part of that skill's polish
pass and is listed above only for the record — re-run this audit to confirm it drops out.
The remaining **9 skills / 16 names** are open.

## Renaming is not automatically safe

Before shortening a name, check how the paired reviewer resolves it:

- **Keyword probes** (e.g. `sotif-analysis-checklist-reviewer._find_sheet_by_keywords`) survive
  a rename as long as the distinguishing keyword stays in the name — but note they return the
  **first** match, so shortening one tab can silently re-bind a keyword to a different tab.
  This was an active bug in the SOTIF pair, fixed the same run.
- **Exact-name lookups** (`wb["09_..."]`) break immediately and need the reviewer updated in the
  same commit.
- **Builder-to-builder handoffs** matter too: `triggering-conditions-builder` — the worst
  offender here, six names topping out at 44 characters — sits upstream of the SOTIF chain.

## Suggested sequencing

One skill (plus its paired reviewer) per POLISH day, worst-first: `triggering-conditions-builder`
(6), then `secure-coding-guidelines-builder` + its reviewer (2, and the reviewer's own 35-char
name), then `8d-problem-solving-builder` (2), `sotif-validation-strategy-builder` (2), and the
five single-name skills last. Roughly three POLISH weeks.
