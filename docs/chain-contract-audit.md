# Chain-contract audit — builder-to-builder xlsx handoffs

_Generated 2026-09-24 by `scripts/chain_contract_audit.py` (read-only; modifies no `.skill` file)._

Scope is builder-to-builder reads only, per the W34 descope of [#46](https://github.com/jherrodthomas/automotive-skills-suite/issues/46). Builder-to-reviewer pairs are excluded: a reviewer ships with the builder it reviews, so the two cannot drift apart the way #43 did.

## Summary

- Builders scanned: **76**
- Cross-skill reader scripts found: **15** (in 13 skills)
- Declared chains audited: **16**
- Sheet-name assertions checked: **48**

| Verdict | Count |
|---|---|
| MATCH | 43 |
| ALIAS | 4 |
| FALLBACK | 1 |
| SELF-AMBIG | 0 |
| UNVERIFIABLE | 0 |
| BREAK | 0 |

### Column level ([#64](https://github.com/jherrodthomas/automotive-skills-suite/issues/64))

- Column/row assertions checked: **193** across 16 chains

| Verdict | Count |
|---|---|
| COL-MATCH | 130 |
| NAME-MATCH | 10 |
| ROW-OK | 23 |
| COL-WEAK | 14 |
| UNVERIFIABLE | 0 |
| NAME-MISS | 0 |
| COL-OOR | 0 |
| COL-SHIFT | 14 |
| ROW-SKIP | 1 |
| SCAN-MISS | 1 |
| PARSE-ERROR | 0 |

**16 column-level BREAK(s)** (`COL-OOR`, `COL-SHIFT`, `NAME-MISS`, `PARSE-ERROR`, `ROW-SKIP`, `SCAN-MISS`) — see *Column-level contracts* below.

### Tab level

**No confirmed BREAKs.** Every hard-coded tab name a builder expects from another builder is a name that builder actually emits.

## Chains audited

| Reader | Upstream | Assertions | Worst verdict |
|---|---|---|---|
| `cs-architecture-builder` | `cs-concept-builder` | 7 | ALIAS |
| `cs-concept-builder` | `cs-goals-builder` | 1 | MATCH |
| `cs-goals-builder` | `tara-builder` | 4 | MATCH |
| `fmeda-builder` | `tsc-builder` | 2 | ALIAS |
| `fsc-builder` | `hara-builder` | 2 | MATCH |
| `hsi-builder` | `tsc-builder` | 1 | MATCH |
| `hw-architecture-builder` | `tsc-builder` | 5 | MATCH |
| `hw-safety-reqs-builder` | `tsc-builder` | 3 | MATCH |
| `safety-case-builder` | `fmeda-builder` | 3 | MATCH |
| `safety-case-builder` | `fsc-builder` | 2 | MATCH |
| `safety-case-builder` | `hara-builder` | 2 | FALLBACK |
| `safety-case-builder` | `tsc-builder` | 2 | MATCH |
| `sw-arch-builder` | `tsc-builder` | 5 | MATCH |
| `sw-fmea-builder` | `tsc-builder` | 1 | MATCH |
| `sw-sr-builder` | `tsc-builder` | 4 | MATCH |
| `tsc-builder` | `fsc-builder` | 4 | MATCH |

## Findings

| Verdict | Reader | Script:line | Function | Upstream | Expected tab | Note |
|---|---|---|---|---|---|---|
| FALLBACK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:24 | `read_hara` | `hara-builder` | `05_Safety_Goals` | alternative branch; sibling matches |
| ALIAS | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:23 | `(module constant)` | `cs-concept-builder` | `02_CSRs_Catalog` | declared legacy alias; preferred name matches |
| ALIAS | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:24 | `(module constant)` | `cs-concept-builder` | `03_CAL_Allocations` | declared legacy alias; preferred name matches |
| ALIAS | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:25 | `(module constant)` | `cs-concept-builder` | `04_Threat_Mapping` | declared legacy alias; preferred name matches |
| ALIAS | `fmeda-builder` | `scripts/tsc_reader.py`:29 | `(module constant)` | `tsc-builder` | `05_Safety_Mechanisms_From_TSC` | declared legacy alias; preferred name matches |
| MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:23 | `(module constant)` | `cs-concept-builder` | `05_CSR_Catalog` |  |
| MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:24 | `(module constant)` | `cs-concept-builder` | `06_CAL_Allocation` |  |
| MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:25 | `(module constant)` | `cs-concept-builder` | `02_CS_Goals_Echo` |  |
| MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:26 | `(module constant)` | `cs-concept-builder` | `00_Title_Page` |  |
| MATCH | `cs-concept-builder` | `scripts/cs_goals_reader.py`:16, 17 | `read_cs_goals` | `cs-goals-builder` | `00_Title_Page` |  |
| MATCH | `cs-goals-builder` | `scripts/tara_reader.py`:51, 54 | `read_tara_xlsx` | `tara-builder` | `11_Cybersecurity_Goals` |  |
| MATCH | `cs-goals-builder` | `scripts/tara_reader.py`:59, 62 | `read_tara_xlsx` | `tara-builder` | `09_Risk_Determination` |  |
| MATCH | `cs-goals-builder` | `scripts/tara_reader.py`:155, 163, 259, 260 | `_build_stride_index` | `tara-builder` | `05_Threat_Scenarios` |  |
| MATCH | `cs-goals-builder` | `scripts/tara_reader.py`:251, 252 | `_build_asset_index` | `tara-builder` | `04_Asset_Inventory` |  |
| MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:29 | `(module constant)` | `tsc-builder` | `04_Safety_Mechanism_Catalog` |  |
| MATCH | `fsc-builder` | `scripts/generate_fsc.py`:203, 204 | `read_hara` | `hara-builder` | `00_Title_Page` |  |
| MATCH | `fsc-builder` | `scripts/generate_fsc.py`:218, 220 | `read_hara` | `hara-builder` | `13_Safety_Goals` |  |
| MATCH | `hsi-builder` | `scripts/tsc_reader.py`:28, 32 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` |  |
| MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:27, 28 | `read_tsc` | `tsc-builder` | `00_Title_Page` |  |
| MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:40, 41 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` |  |
| MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:59, 60 | `read_tsc` | `tsc-builder` | `03_System_Architecture` |  |
| MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:111, 112 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` |  |
| MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:128, 129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` |  |
| MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:26, 44 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` |  |
| MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:31, 32 | `read_tsc` | `tsc-builder` | `00_Title_Page` |  |
| MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:69, 70, 90, 91 | `read_tsc` | `tsc-builder` | `03_System_Architecture` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:22 | `read_hara` | `hara-builder` | `13_Safety_Goals` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:50, 51 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:65, 66 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:90, 91 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:106, 107 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:131, 132 | `read_fmeda` | `fmeda-builder` | `07_SPFM_Calculation` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:140 | `read_fmeda` | `fmeda-builder` | `08_LFM_Calculation` |  |
| MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:141 | `read_fmeda` | `fmeda-builder` | `09_PMHF_Calculation` |  |
| MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:28, 29 | `read_tsc` | `tsc-builder` | `00_Title_Page` |  |
| MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:41, 42 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` |  |
| MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:58, 59 | `read_tsc` | `tsc-builder` | `03_System_Architecture` |  |
| MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:104, 105 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` |  |
| MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:123, 124 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` |  |
| MATCH | `sw-fmea-builder` | `scripts/tsc_reader.py`:34, 35 | `read_tsc` | `tsc-builder` | `00_Title_Page` |  |
| MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:26, 44 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` |  |
| MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:31, 32 | `read_tsc` | `tsc-builder` | `00_Title_Page` |  |
| MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:69, 70 | `read_tsc` | `tsc-builder` | `03_System_Architecture` |  |
| MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:97, 98 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` |  |
| MATCH | `tsc-builder` | `scripts/generate_tsc.py`:209, 227 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` |  |
| MATCH | `tsc-builder` | `scripts/generate_tsc.py`:214, 215 | `read_fsc` | `fsc-builder` | `00_Title_Page` |  |
| MATCH | `tsc-builder` | `scripts/generate_tsc.py`:248, 249 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` |  |
| MATCH | `tsc-builder` | `scripts/generate_tsc.py`:267, 268 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` |  |

## Column-level contracts

For every reader function attributed to an upstream, each positional read (`ws.cell(r, N)`, `row[i]`) is checked against the header the upstream emits at that position, each by-name header lookup against the upstream's header text, and each data loop's first row against the upstream's header row. Presence and naming only — no values are inspected.

### Column-level BREAKs and their issues

| Chain | Tab | Verdict | Assertion | Issue |
|---|---|---|---|---|
| `sw-fmea-builder` → `tsc-builder` | `(scan: partition | sw_partition | sw_tsr | software_tsr)` | SCAN-MISS | pattern scan finds a tab | **not yet filed** |
| `cs-concept-builder` → `cs-goals-builder` | `03_Cybersecurity_Goals` | ROW-SKIP | data from row 5 | [#65](https://github.com/jherrodthomas/automotive-skills-suite/issues/65) |
| `cs-concept-builder` → `cs-goals-builder` | `03_Cybersecurity_Goals` | COL-SHIFT | col 4 as `cal` | [#65](https://github.com/jherrodthomas/automotive-skills-suite/issues/65) |
| `cs-concept-builder` → `cs-goals-builder` | `03_Cybersecurity_Goals` | COL-SHIFT | col 6 as `csg_text` | [#65](https://github.com/jherrodthomas/automotive-skills-suite/issues/65) |
| `sw-arch-builder` → `tsc-builder` | `03_System_Architecture` | COL-SHIFT | col 5 as `asil` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `03_System_Architecture` | COL-SHIFT | col 6 as `notes` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `05_TSR_Catalog` | COL-SHIFT | col 3 as `fsr_ref` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `05_TSR_Catalog` | COL-SHIFT | col 5 as `asil` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `05_TSR_Catalog` | COL-SHIFT | col 6 as `mechanism_ref` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `04_Safety_Mechanism_Catalog` | COL-SHIFT | col 2 as `name` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `04_Safety_Mechanism_Catalog` | COL-SHIFT | col 4 as `dc` | **not yet filed** |
| `sw-arch-builder` → `tsc-builder` | `04_Safety_Mechanism_Catalog` | COL-SHIFT | col 5 as `detection_time` | **not yet filed** |
| `sw-fmea-builder` → `sw-arch-builder` | `02_TSC_Architecture_Echo` | COL-SHIFT | col 4 as `partition_id` | **not yet filed** |
| `sw-sr-builder` → `tsc-builder` | `06_HSI_Specification` | COL-SHIFT | col 3 as `direction` | **not yet filed** |
| `sw-sr-builder` → `tsc-builder` | `06_HSI_Specification` | COL-SHIFT | col 7 as `update_rate` | **not yet filed** |
| `sw-sr-builder` → `tsc-builder` | `06_HSI_Specification` | COL-SHIFT | col 8 as `integrity` | **not yet filed** |

| Verdict | Reader | Script:line | Function | Upstream | Tab | Assertion | Note |
|---|---|---|---|---|---|---|---|
| SCAN-MISS | `sw-fmea-builder` | `scripts/tsc_reader.py`:51 | `read_tsc` | `tsc-builder` | `(scan: partition | sw_partition | sw_tsr | software_tsr)` | pattern scan finds a tab | no tab the upstream emits matches these substrings; every read under it is dead |
| ROW-SKIP | `cs-concept-builder` | `scripts/cs_goals_reader.py`:43 | `read_cs_goals` | `cs-goals-builder` | `03_Cybersecurity_Goals` | data from row 5 | upstream header is row 1; the first 3 data row(s) are never read |
| COL-SHIFT | `cs-concept-builder` | `scripts/cs_goals_reader.py`:43 | `read_cs_goals` | `cs-goals-builder` | `03_Cybersecurity_Goals` | col 4 as `cal` | upstream col 4 is `CS_Goal_Text`; `CAL` is at col 5 |
| COL-SHIFT | `cs-concept-builder` | `scripts/cs_goals_reader.py`:43 | `read_cs_goals` | `cs-goals-builder` | `03_Cybersecurity_Goals` | col 6 as `csg_text` | upstream col 6 is `Cybersecurity_Property`; `CSG_ID` is at col 1 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:93 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 5 as `asil` | upstream col 5 is `RTOS / OS`; `ASIL (developed-to)` is at col 6 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:93 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 6 as `notes` | upstream col 6 is `ASIL (developed-to)`; `Notes` is at col 7 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:112 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 3 as `fsr_ref` | upstream col 3 is `Allocated ASIL`; `TSR_ID` is at col 1 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:112 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 5 as `asil` | upstream col 5 is `Mechanism`; `Allocated ASIL` is at col 3 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:112 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 6 as `mechanism_ref` | upstream col 6 is `Linked Node`; `Mechanism` is at col 5 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 2 as `name` | upstream col 2 is `Allocated ASIL`; `Mechanism Name` is at col 6 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 4 as `dc` | upstream col 4 is `Linked Node`; `Default DC%` is at col 7 |
| COL-SHIFT | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 5 as `detection_time` | upstream col 5 is `Mechanism ID`; `Detection Time (target)` is at col 8 |
| COL-SHIFT | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | col 4 as `partition_id` | upstream col 4 is `Allocated Nodes`; `Partition ID` is at col 1 |
| COL-SHIFT | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 3 as `direction` | upstream col 3 is `Linked FSR / TSR`; `Direction` is at col 2 |
| COL-SHIFT | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 7 as `update_rate` | upstream col 7 is `Integrity Protection`; `Update Rate` is at col 6 |
| COL-SHIFT | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 8 as `integrity` | upstream col 8 is `Failure Reaction`; `Integrity Protection` is at col 7 |
| COL-WEAK | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:138 | `read_cs_concept` | `cs-concept-builder` | `02_CS_Goals_Echo` | col 2 as `attack_type` | upstream col 2 is `Threat`; no header names this key |
| COL-WEAK | `cs-concept-builder` | `scripts/cs_goals_reader.py`:43 | `read_cs_goals` | `cs-goals-builder` | `03_Cybersecurity_Goals` | col 5 as `driving_tara_ids` | upstream col 5 is `CAL`; no header names this key |
| COL-WEAK | `hw-architecture-builder` | `scripts/tsc_reader.py`:118 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 7 as `text` | upstream col 7 is `Technical Safety Requirement`; no header names this key |
| COL-WEAK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 7 as `text` | upstream col 7 is `Technical Safety Requirement`; no header names this key |
| COL-WEAK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:137 | `read_fmeda` | `fmeda-builder` | `07_SPFM_Calculation` | col 2 as `pmhf` | upstream col 2 is `Σ(λ_SPF + λ_RF)`; no header names this key |
| COL-WEAK | `sw-arch-builder` | `scripts/tsc_reader.py`:93 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `type` | upstream col 3 is `Hosted On (HW Comp ID)`; no header names this key |
| COL-WEAK | `sw-arch-builder` | `scripts/tsc_reader.py`:112 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 4 as `text` | upstream col 4 is `Type`; no header names this key |
| COL-WEAK | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 6 as `implementation` | upstream col 6 is `Mechanism Name`; no header names this key |
| COL-WEAK | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 7 as `notes` | upstream col 7 is `Default DC%`; no header names this key |
| COL-WEAK | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | col 6 as `language` | upstream col 6 is `Notes`; no header names this key |
| COL-WEAK | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 2 as `name` | upstream col 2 is `Direction`; no header names this key |
| COL-WEAK | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 4 as `source` | upstream col 4 is `Mechanism`; no header names this key |
| COL-WEAK | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 6 as `range` | upstream col 6 is `Update Rate`; no header names this key |
| COL-WEAK | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 5 as `be_code` | upstream col 5 is `Linked Basic Event`; no header names this key |
| ROW-OK | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | data from row 3 | upstream header is row 2 |
| ROW-OK | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:119 | `read_cs_concept` | `cs-concept-builder` | `06_CAL_Allocation` | data from row 3 | upstream header is row 2 |
| ROW-OK | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:138 | `read_cs_concept` | `cs-concept-builder` | `02_CS_Goals_Echo` | data from row 3 | upstream header is row 2 |
| ROW-OK | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | data from row 5 | upstream header is row 4 |
| ROW-OK | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | data from row 5 | upstream header is row 4 |
| ROW-OK | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | data from row 5 | upstream header is row 4 |
| ROW-OK | `hw-architecture-builder` | `scripts/tsc_reader.py`:118 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `hw-architecture-builder` | `scripts/tsc_reader.py`:138 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | data from row 5 | upstream header is row 4 |
| ROW-OK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:56 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | data from row 5 | upstream header is row 4 |
| ROW-OK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:112 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:137 | `read_fmeda` | `fmeda-builder` | `07_SPFM_Calculation` | data from row 4 | upstream header is row 3 |
| ROW-OK | `sw-arch-builder` | `scripts/tsc_reader.py`:47 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | data from row 5 | upstream header is row 4 |
| ROW-OK | `sw-arch-builder` | `scripts/tsc_reader.py`:112 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | data from row 2 | upstream header is row 2 |
| ROW-OK | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | data from row 5 | upstream header is row 4 |
| ROW-OK | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | data from row 5 | upstream header is row 4 |
| ROW-OK | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | data from row 5 | upstream header is row 4 |
| ROW-OK | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | data from row 5 | upstream header is row 4 |
| ROW-OK | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | data from row 5 | upstream header is row 4 |
| NAME-MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:141 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | header containing "mechanism id" | upstream `Mechanism ID` |
| NAME-MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:143 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | header containing "mechanism name" | upstream `Mechanism Name` |
| NAME-MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:145 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | header containing "default dc" | upstream `Default DC%` |
| NAME-MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:145 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | header containing "dc%" | upstream `Default DC%` |
| NAME-MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:147 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | header containing "node" | upstream `Linked Node` |
| NAME-MATCH | `fmeda-builder` | `scripts/tsc_reader.py`:147 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | header containing "linked" | upstream `Linked Node` |
| NAME-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:66 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | header containing "hw component" | upstream `HW Component ID` |
| NAME-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:68 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | header containing "sw partition" | upstream `SW Partition ID` |
| NAME-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:66 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | header containing "hw component" | upstream `HW Component ID` |
| NAME-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:68 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | header containing "sw partition" | upstream `SW Partition ID` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | col 1 as `csr_id` | upstream `CSR ID` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | col 2 as `parent_csg` | upstream `Parent CSG` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | col 3 as `cal`/`tara_level` | upstream `CAL` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | col 4 as `branch`/`title` | upstream `Branch` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | col 6 as `description`/`requirement_text` | upstream `Requirement Text` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:97 | `read_cs_concept` | `cs-concept-builder` | `05_CSR_Catalog` | col 7 as `verification_method` | upstream `Verification Method` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:119 | `read_cs_concept` | `cs-concept-builder` | `06_CAL_Allocation` | col 1 as `node_id` | upstream `Node ID` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:119 | `read_cs_concept` | `cs-concept-builder` | `06_CAL_Allocation` | col 2 as `node_name` | upstream `Node Name` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:119 | `read_cs_concept` | `cs-concept-builder` | `06_CAL_Allocation` | col 3 as `node_type` | upstream `Type` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:119 | `read_cs_concept` | `cs-concept-builder` | `06_CAL_Allocation` | col 4 as `cal` | upstream `Inherited CAL` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:119 | `read_cs_concept` | `cs-concept-builder` | `06_CAL_Allocation` | col 5 as `csr_count` | upstream `CSR Count` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:138 | `read_cs_concept` | `cs-concept-builder` | `02_CS_Goals_Echo` | col 3 as `target_asset`/`target_node` | upstream `Asset` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:138 | `read_cs_concept` | `cs-concept-builder` | `02_CS_Goals_Echo` | col 4 as `severity`/`cal` | upstream `CAL` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:138 | `read_cs_concept` | `cs-concept-builder` | `02_CS_Goals_Echo` | col 5 as `driving_tara_ids` | upstream `TARA IDs` |
| COL-MATCH | `cs-architecture-builder` | `scripts/cs_concept_reader.py`:138 | `read_cs_concept` | `cs-concept-builder` | `02_CS_Goals_Echo` | col 6 as `goal_text` | upstream `CS Goal Text` |
| COL-MATCH | `cs-concept-builder` | `scripts/cs_goals_reader.py`:43 | `read_cs_goals` | `cs-goals-builder` | `03_Cybersecurity_Goals` | col 2 as `threat` | upstream `Threat_Scenario_Ref` |
| COL-MATCH | `cs-concept-builder` | `scripts/cs_goals_reader.py`:43 | `read_cs_goals` | `cs-goals-builder` | `03_Cybersecurity_Goals` | col 3 as `asset` | upstream `Asset` |
| COL-MATCH | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | col 2 as `function` | upstream `Function` |
| COL-MATCH | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | col 3 as `hazard` | upstream `Hazard` |
| COL-MATCH | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | col 4 as `asil` | upstream `Worst-case ASIL` |
| COL-MATCH | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | col 5 as `driving_hara_ids` | upstream `Driving HARA IDs` |
| COL-MATCH | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | col 6 as `sg_text` | upstream `Safety Goal` |
| COL-MATCH | `fsc-builder` | `scripts/generate_fsc.py`:225 | `read_hara` | `hara-builder` | `13_Safety_Goals` | col 7 as `safe_state` | upstream `Safe State` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 2 as `direction` | upstream `Direction` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 3 as `linked_fsr` | upstream `Linked FSR / TSR` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 4 as `mechanism` | upstream `Mechanism` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 5 as `encoding` | upstream `Encoding` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 6 as `update_rate` | upstream `Update Rate` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 7 as `integrity_protection` | upstream `Integrity Protection` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 8 as `failure_reaction` | upstream `Failure Reaction` |
| COL-MATCH | `hsi-builder` | `scripts/tsc_reader.py`:37 | `read_hsi_signals` | `tsc-builder` | `06_HSI_Specification` | col 9 as `allocated_asil` | upstream `Allocated ASIL` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 2 as `sg_id` | upstream `SG_ID` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 3 as `asil` | upstream `ASIL (inherited)` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 4 as `branch` | upstream `Branch` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 5 as `node_ref` | upstream `Linked Node` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 6 as `fsr_text` | upstream `Functional Safety Requirement` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:46 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 7 as `ftti_ms` | upstream `FTTI (ms)` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:80 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:80 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `part` | upstream `Part / Vendor` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:80 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 5 as `power_domain` | upstream `Power Domain` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:80 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 6 as `clock_domain` | upstream `Clock Domain` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:80 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 7 as `notes` | upstream `Notes` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:99 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:99 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `hosted_on` | upstream `Hosted On (HW Comp ID)` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:99 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 5 as `rtos` | upstream `RTOS / OS` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:99 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 6 as `asil` | upstream `ASIL (developed-to)` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:99 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 7 as `notes` | upstream `Notes` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:118 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 2 as `fsr_id` | upstream `FSR_ID` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:118 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 3 as `asil` | upstream `Allocated ASIL` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:118 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 5 as `mechanism` | upstream `Mechanism` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:138 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 7 as `dc` | upstream `Default DC%` |
| COL-MATCH | `hw-architecture-builder` | `scripts/tsc_reader.py`:138 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 8 as `detection_time` | upstream `Detection Time (target)` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `part` | upstream `Part / Vendor` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 4 as `allocated_nodes` | upstream `Allocated Nodes` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 5 as `power_domain` | upstream `Power Domain` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 6 as `clock_domain` | upstream `Clock Domain` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 7 as `notes` | upstream `Notes` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:106 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:106 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `hosted_on` | upstream `Hosted On (HW Comp ID)` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:106 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 4 as `allocated_nodes` | upstream `Allocated Nodes` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:106 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 5 as `rtos` | upstream `RTOS / OS` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:106 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 6 as `asil` | upstream `ASIL (developed-to)` |
| COL-MATCH | `hw-safety-reqs-builder` | `scripts/tsc_reader.py`:106 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 7 as `notes` | upstream `Notes` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:56 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 2 as `sg_id` | upstream `SG_ID` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:56 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 3 as `asil_inherited` | upstream `ASIL (inherited)` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:56 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 4 as `branch` | upstream `Branch` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:56 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 7 as `fsr_text` | upstream `Functional Safety Requirement` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:56 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 8 as `ftti_ms` | upstream `FTTI (ms)` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 2 as `node_id` | upstream `Node ID` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 3 as `node_name` | upstream `Node Name` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 4 as `branch` | upstream `Branch` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 5 as `inherited_asil` | upstream `Inherited ASIL` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 7 as `decomposition` | upstream `Selected Decomposition` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:71 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 8 as `resulting_asil` | upstream `Resulting Per-Node ASIL` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 2 as `fsr_id` | upstream `FSR_ID` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 3 as `asil` | upstream `Allocated ASIL` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 4 as `type` | upstream `Type` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 5 as `mechanism` | upstream `Mechanism` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:96 | `read_tsc` | `tsc-builder` | `05_TSR_Catalog` | col 6 as `node` | upstream `Linked Node` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:112 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 1 as `fsr_id` | upstream `FSR_ID` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:112 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 6 as `mechanism_name` | upstream `Mechanism Name` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:112 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 7 as `default_dc` | upstream `Default DC%` |
| COL-MATCH | `safety-case-builder` | `scripts/multi_xlsx_reader.py`:137 | `read_fmeda` | `fmeda-builder` | `07_SPFM_Calculation` | col 4 as `spfm`/`lfm` | upstream `SPFM` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:47 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 2 as `sg_id` | upstream `SG_ID` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:47 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 3 as `asil` | upstream `ASIL (inherited)` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:47 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 6 as `fsr_text` | upstream `Functional Safety Requirement` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:47 | `read_tsc` | `tsc-builder` | `02_FSRs_From_FSC` | col 7 as `ftti_ms` | upstream `FTTI (ms)` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `part` | upstream `Part / Vendor` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:78 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 7 as `notes` | upstream `Notes` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:93 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `sw-arch-builder` | `scripts/tsc_reader.py`:129 | `read_tsc` | `tsc-builder` | `04_Safety_Mechanism_Catalog` | col 3 as `branch` | upstream `Branch` |
| COL-MATCH | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | col 1 as `id` | upstream `Partition ID` |
| COL-MATCH | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | col 3 as `type` | upstream `Type` |
| COL-MATCH | `sw-fmea-builder` | `scripts/tsc_reader.py`:113 | `read_sw_arch` | `sw-arch-builder` | `02_TSC_Architecture_Echo` | col 5 as `asil` | upstream `ASIL` |
| COL-MATCH | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | col 2 as `sample_rate_hz` | upstream `Sample Rate (Hz)` |
| COL-MATCH | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | col 3 as `max_age_ms` | upstream `Max Age (ms)` |
| COL-MATCH | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | col 4 as `latency_hw_to_sw_ms` | upstream `Latency HW->SW (ms)` |
| COL-MATCH | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | col 5 as `latency_sw_to_hw_ms` | upstream `Latency SW->HW (ms)` |
| COL-MATCH | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | col 6 as `detection_time_ms` | upstream `Detection Time (ms)` |
| COL-MATCH | `sw-hsis-builder` | `scripts/hsi_reader.py`:114 | `read_hsi_timing` | `hsi-builder` | `04_Timing_Specification` | col 7 as `settling_time_ms` | upstream `Settling Time (ms)` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:85 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:85 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 3 as `hosted_on` | upstream `Hosted On (HW Comp ID)` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:85 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 4 as `allocated_nodes` | upstream `Allocated Nodes` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:85 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 5 as `rtos` | upstream `RTOS / OS` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:85 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 6 as `asil` | upstream `ASIL (developed-to)` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:85 | `read_tsc` | `tsc-builder` | `03_System_Architecture` | col 7 as `notes` | upstream `Notes` |
| COL-MATCH | `sw-sr-builder` | `scripts/tsc_reader.py`:103 | `read_tsc` | `tsc-builder` | `06_HSI_Specification` | col 5 as `encoding` | upstream `Encoding` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 2 as `sg_id` | upstream `SG_ID` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 3 as `asil_inherited` | upstream `ASIL (inherited)` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 4 as `branch` | upstream `Branch` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 7 as `fsr_text` | upstream `Functional Safety Requirement` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:234 | `read_fsc` | `fsc-builder` | `05_FSR_Catalog` | col 8 as `ftti_ms` | upstream `FTTI (ms)` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 2 as `node_id` | upstream `Node ID` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 3 as `node_name` | upstream `Node Name` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 4 as `branch` | upstream `Branch` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 5 as `inherited_asil` | upstream `Inherited ASIL` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 7 as `decomposition` | upstream `Selected Decomposition` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 8 as `resulting_asil` | upstream `Resulting Per-Node ASIL` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:254 | `read_fsc` | `fsc-builder` | `06_ASIL_Allocation` | col 9 as `independence_evidence` | upstream `Independence Evidence (analyst)` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 2 as `name` | upstream `Name` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 3 as `type` | upstream `Type` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 4 as `branch` | upstream `FTA Branch` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 5 as `asil_relevant` | upstream `ASIL-relevant` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 6 as `inputs` | upstream `Inputs (IDs)` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 7 as `outputs` | upstream `Outputs (IDs)` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 8 as `redundancy_group` | upstream `Redundancy Group` |
| COL-MATCH | `tsc-builder` | `scripts/generate_tsc.py`:273 | `read_fsc` | `fsc-builder` | `03_System_Block_Diagram` | col 9 as `shared_resources` | upstream `Shared Resources` |

## Pattern-scan readers (no fixed contract)

These iterate `wb.sheetnames` and match by substring instead of asserting exact tab names. They cannot break on a rename, and they are the shape the other readers should converge on.

| Reader | Script | Upstream |
|---|---|---|
| `cs-concept-builder` | `scripts/cs_goals_reader.py` | `cs-goals-builder` |
| `sw-fmea-builder` | `scripts/tsc_reader.py` | `tsc-builder` |
| `sw-hsis-builder` | `scripts/hsi_reader.py` | `hsi-builder` |

## Self-reads (excluded from the audit)

These load the reading skill's OWN output, not an upstream workbook, so they are not a cross-skill contract.

| Skill | Script | Function | Tab |
|---|---|---|---|
| `fsc-builder` | `scripts/fault_tree_renderer.py` | `trees_from_fsc_xlsx` | `04_FTA_Combined` |
| `fsc-builder` | `scripts/fault_tree_renderer.py` | `trees_from_fsc_xlsx` | `02_SGs_From_HARA` |

## Method and limits

Static analysis only — no workbook is generated and no generator is executed. The tab layer answers *does the upstream emit a tab with this name*. The column layer (#64, `scripts/column_contract.py`) answers *does that tab carry, at the position and under the name the reader uses, the column it thinks it is reading*, and *does the reader's data loop start on the upstream's first data row*.

Column-layer limits: emitter headers are resolved only from `style_header_row(...)` and `enumerate(headers)` + `ws.cell(ROW, i)` shapes; tabs built any other way are UNVERIFIABLE, never guessed. Reader columns are recognised only when a single cell read is the value of a dict-literal key. Naming uses token overlap with a small abbreviation map (`csg`, `fsr`, `dc`, ...); **COL-WEAK** means no header in the tab names the key and is reported for a human, not asserted. A pattern-scan reader (`for s in wb.sheetnames`) is resolved to the first upstream tab, in name order, that matches its substrings.

Column verdicts: **COL-MATCH** header at the read position names the key · **COL-SHIFT** it does not, but another header in the tab does (BREAK) · **COL-OOR** read past the last header (BREAK) · **ROW-SKIP** data loop starts more than one row below the header, so leading data rows are never read (BREAK) · **NAME-MISS** a by-name lookup matches no header (BREAK) · **SCAN-MISS** a `wb.sheetnames` substring scan matches no upstream tab, so every read under it is dead (BREAK) · **PARSE-ERROR** the reader does not parse (BREAK).

Verdict definitions: **MATCH** upstream emits it · **ALIAS** declared legacy alternative whose preferred sibling matches · **FALLBACK** the same shape expressed as an `elif`/`or` branch · **SELF-AMBIG** the reading skill emits the same tab name and attribution came only from SKILL.md prose · **UNVERIFIABLE** upstream unresolved · **BREAK** nothing upstream emits it.
