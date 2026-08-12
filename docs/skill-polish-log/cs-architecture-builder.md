# cs-architecture-builder — polish log

## 2026-08-12 (autonomous POLISH, addresses #43)

**Selection:** open issue #43 (`chain-break`, `cyber`) — "Repair cs-concept →
cs-architecture chain break (reader rewrite)". Also the least-recently-touched
builder in the suite: untouched since the 2026-05-01 bulk import.

**What's good:** the generator itself is sound. All 12 tabs build, `recalc.py`
and the `office/soffice.py` helper are intact, the ESC sample input exercises
7 CS elements, and the control catalog / methodology references are substantive.
Nothing in the downstream code needed changing — the defect was entirely in the
input adapter.

**What was wrong — the chain break, confirmed by execution:**

`scripts/cs_concept_reader.py` looked for three tabs that cs-concept-builder has
*never* emitted:

| Reader expected | cs-concept-builder actually emits |
|---|---|
| `02_CSRs_Catalog` | `05_CSR_Catalog` |
| `03_CAL_Allocations` | `06_CAL_Allocation` |
| `04_Threat_Mapping` | (no such tab — goals live in `02_CS_Goals_Echo`) |

Every lookup was guarded by `if <name> in wb.sheetnames`, so all three missed
silently and the reader returned empty lists with no error. The title page was
additionally read from columns A/B while the generator writes labels in B and
values in C, so `item` came back empty too.

Measured against a CS Concept workbook built from cs-concept-builder's own tab
builders:

- **before:** `csrs=0  cal_allocations=0  threat_mapping=0  item={}`
- **after:** `csrs=2  cal_allocations=6  threat_mapping=1  item=8 fields`

Net effect of the bug: the CS Architecture built, reported success, and shipped
with an empty `02_CS_Concept_Echo` and an allocation matrix with zero CSR rows.
Failure was silent in both directions — worse than a crash.

**Fix applied:**

1. Rewrote `cs_concept_reader.py` against the real contract, with the correct
   column offsets for each tab (header row 2, data from row 3).
2. Threat context now derives from `02_CS_Goals_Echo` (CSG ID, threat, asset,
   CAL, driving TARA IDs) with `linked_csrs` back-filled by matching each CSR's
   `parent_csg` — recovering the linkage the phantom `04_Threat_Mapping` tab was
   supposed to provide.
3. Legacy tab names kept as ordered fallbacks so any hand-built workbook on the
   old layout still loads.
4. A missing CSR catalog now raises `ValueError` naming both tabs it looked for,
   instead of silently producing a blank architecture.
5. Preserved every downstream key (`tara_level`, `target_node`, `title`,
   `description`, `allocated_nodes`) so `generate_cs_architecture.py` needed no
   changes; added the honest names (`cal`, `branch`, `requirement_text`,
   `target_asset`, `node_id`, `verification_method`) alongside.
6. Honest-label fixes: echo tab headers `Title`/`TARA Level`/`Description` →
   `Branch`/`CAL`/`Requirement Text` (the column carries CAL, not a TARA level),
   and SKILL.md Step 1 + the tab table now name the tabs actually read.

**Verification:** built a CS Concept via cs-concept-builder's own tab builders,
ran the old reader (0/0/0) and the new one (2/6/1) against it, then ran
`generate_cs_architecture.py` end to end — 12 tabs, echo populated, allocation
matrix carrying both CSR rows, 14 CSR×element cells. `py_compile` clean; archive
repacked with original member order and timestamps, `testzip()` clean.

**Severity:** was **high** (flagship cyber chain produced silently empty output
for 3.5 months) → **resolved**.

**Follow-ups:**
- #43 is ready to close pending human confirmation — not closed autonomously.
- The same silent `if <tab> in wb.sheetnames` guard pattern is the likely root
  cause family behind #46's chain-contract audit. Recommend #46 grep every
  `*_reader.py` in the suite for guarded lookups and assert the emitter side.
- cs-architecture-builder has no paired reviewer file — it is one of the two 🔴
  entries in STATUS.md. Candidate for a future `new-skill` target.
