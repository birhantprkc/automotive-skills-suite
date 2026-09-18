# dia-checklist-reviewer — example

**What this skill produces:** A confirmation-review checklist xlsx over an ISO 26262-8 §5 Development Interface Agreement — **33 checks** across 7 tabs, counted from the `CheckDef` entries in `scripts/check_definitions.py` on 2026-09-18: **Confirmation Review (14 `CR` checks** — IDs 1, 2, 3, 4a–4e, 5–10, generic document quality per ISO 26262-8 §10**)**, **DIA Assessment (14 `DIAA` checks** — parties, RACI, communication, reviews, deliverables, change management, tool sharing, confidentiality/IP, references, scope**)**, and **Verification Assessment (5 `VA` checks**, all external Verification Plan / governance**)**. SKILL.md's advertised 14 + 14 + 5 matches the code — no drift.

**Typical input shape:** A DIA workbook xlsx — normally `dia-builder` output, best-effort on other DIA-shaped workbooks. `scripts/dia_probe.py` reads `00_Title_Page`, `02_Parties`, `03_Item_Scope`, `04_RACI_Matrix`, `05_Communication_Protocol`, `06_Joint_Reviews`, `07_Supplier_Deliverables`, `08_Change_Management`, `09_Tool_Sharing` and `10_Confidentiality_IP`.

**Expected output:** `<name>_checklist.xlsx` with every check rated FC / LC / PC / NO / NA, or left `Pending` with an `(Auto-suggest)` draft where reviewer judgment is required. The source DIA is never modified — gaps land in the Recommended Actions column. The script prints a JSON summary with FC/LC/PC/NO/NA/PENDING counts per tab, so auto-fill yield is visible before you open the file.

**Sample I/O:**

```bash
python scripts/generate_checklist.py dia.xlsx output_checklist.xlsx
python scripts/recalc.py output_checklist.xlsx      # optional; detects formula errors
```

**Three false findings were removed on 2026-09-17 (`9170271`)** — all reader-contract mismatches, where the builder wrote valid content and the probe failed to read it, then reported a compliance defect that did not exist:

- **DIAA-8** (joint reviews) sat at `PC` on a DIA with seven fully-scheduled reviews: the probe looked for `milestone` / `participants`, the builder writes `Review Name` / `Attendees` / `Planned Date`. Aliases added.
- **DIAA-14** (item scope) sat at `PC` against 6 in-scope and 5 out-of-scope bullets: `_find_header_row` requires ≥3 populated cells, and `03_Item_Scope` is a two-column vertical layout, so no header row was ever found. A `_scan_vertical_scope()` fallback now runs only when the header parse finds nothing, leaving non-builder DIAs unaffected.
- **DIAA-4 / DIAA-5** (RACI) sat at `NO` on 10 rows: the builder writes combined assignments (`A,R`) in one cell — its own documented default — and the checks compared `v.upper() == "A"` exactly. `_raci_tokens()` now splits on `,` `/` `;` `+` and space, and the probe was tightened so `assignments` holds party columns only (`WP_ID` and `ISO Ref` were previously scanned for role letters).

On the canonical `examples/sample_dia_esc.json`, DIAA moved from `FC 6 / NO 2 / PC 2` to `FC 8 / NO 2`. **The two remaining NOs are genuine and deliberately unfixed:** the sample gives WP11 Safety Plan two Accountable parties and no Responsible, and WP12 Safety Case `A,R` for both parties. Whether joint accountability is intended is a contract-semantics call for a human, not a typo fix — either correct the sample or relax DIAA-4 to allow declared joint accountability.

All 5 `VA` checks returning `Pending` is the normal, correct result when no external Verification Plan is supplied — not a finding.

**Paired builder:** `dia-builder`, which is healthy — runs clean on its sample, emits all 12 documented tabs, frontmatter 643 chars.
