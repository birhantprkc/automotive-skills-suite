# Polish log — cs-goals-builder

## 2026-09-16 — first pass (POLISH, W38 Wednesday slot, no open issue)

**Severity: HIGH — fixed this run.** `cs-goals-builder` could not read the TARA workbook its own
upstream (`tara-builder`) produces. Every generated Cybersecurity Goal shipped with a bare
integer as its goal text and the goal text sitting in the `Asset` column. The chain
`tara-builder → cs-goals-builder → cs-concept-builder → cs-architecture-builder` was carrying
corrupted payload end to end.

This is the first `cyber` skill polished since `cs-concept-builder`, and it is the producer that
`cs-concept-builder` reads — so the previously-polished downstream was consuming garbage.

### What's good

- Archive intact, all `.py` files compile, no `__pycache__` contamination (pre-existing).
- Frontmatter well-formed: `name` and `description` present, correctly named, 552 chars —
  inside the 1,024 limit.
- `recalc.py` matches the repo-wide single hash.
- All 8 emitted sheet names are Excel-legal and match the 8 tabs SKILL.md advertises — no
  tab-count drift, which is the failure mode seen in #52/#54.
- SKILL.md is genuinely good: accurate workflow, honest "Common pitfalls", correct statement
  that the JSON is the source of truth and the xlsx is derived.
- The generator itself is sound. Given correct reader output it produces a fully populated
  8-tab workbook (15 CSGs, CAL distribution 10/3/2) with no further changes.
- `references/cal_assignment.md` and `methodology.md` are substantive, not placeholders.

### What was fixed

**1. Header aliasing — the headline break. (HIGH, fixed)**

`tara_reader._read_csg_tab` resolved columns against snake_case names
(`threat_scenario_id`, `asset`, `cs_goal_text`) with *positional* fallbacks `2, 3, 4`.
`tara-builder` actually emits human-readable headers:

| col | tara-builder emits | reader wanted | result |
|---|---|---|---|
| 1 | `CSG ID` | `csg_id` | matched |
| 2 | `Derived From Scenario` | `threat_scenario_id` | fell back to col 2 — correct by luck |
| 3 | `Cybersecurity Goal` | `asset` | **fell back to col 3 — goal text landed in `asset`** |
| 4 | `Risk Value` | `cs_goal_text` | **fell back to col 4 — risk number landed in goal text** |

No alias ever matched for `asset` or `cs_goal_text`, so both silently took the positional
default and produced plausible-looking, wrong output. Verified before the fix:

```
"asset": "Prevent Malicious firmware injection via JTAG debug port",
"cs_goal_text": "5",
```

Added `_HEADER_ALIASES` + `_normalize_headers()` + `_col()`. Columns now resolve by name across
both readers; positional fallback only applies where no alias matches, and `None` (rather than a
guessed column) is used where guessing would fabricate data.

**2. No asset column in the upstream CSG tab. (HIGH, fixed)**

`tara-builder`'s `11_Cybersecurity_Goals` has no asset column at all, so aliasing alone would
have yielded `"Unknown"` for all 15 rows. Added `_build_asset_index()`, which walks
`05_Threat_Scenarios` (scenario → asset ID) and `04_Asset_Inventory` (asset ID → asset name) to
resolve the real name. `CSG-001` now correctly reports `ESC Firmware Image` rather than
`Unknown` or the goal text.

**3. Silent risk-value downgrade. (MED, fixed)**

`int(risk_val) if isinstance(risk_val, int) else 3` mapped any float (`4.0`), numeric string
(`"4"`), or blank to **3** — silently downgrading a CAL 4 goal to CAL 2 with no warning. This is
the same "silently dropped" shape as the 2026-09-15 `hw-safety-reqs` fix. Replaced with
`_coerce_risk()`, which accepts int/float/numeric-string and warns to stderr before defaulting.

**4. Crash on non-string headers. (MED, fixed)**

`_read_csg_tab` called `header_val.lower()` directly — an `AttributeError` on any numeric or
date header cell. `_read_risk_determination_tab` already guarded with `str()`; the two are now
consistent via `_normalize_headers()`.

**5. Silent no-op on unrecognised TARA. (LOW, fixed)**

A TARA with neither `11_Cybersecurity_Goals` nor `09_Risk_Determination` produced an empty
workbook with no diagnostic. Now warns to stderr.

### Verification

- `tara-builder` sample ESC input → TARA xlsx → `cs-goals-builder` → 15 CSGs, all with real goal
  text, real asset names, correct risk values. Assertion `no goal-text cell is numeric` passes.
- Downstream `cs-concept-builder` consumes the repaired workbook: 12 CS Goals, 6 nodes, 192 CSRs,
  and `02_CS_Goals_Echo` now carries real goal text instead of `"5"`.
- `scripts/chain_contract_audit.py`: 48 assertions, 16 chains, 0 BREAK. The two new
  `_build_asset_index` reads of `04_Asset_Inventory` and `05_Threat_Scenarios` register as MATCH.

### Not fixed — follow-ups

**A. `Cybersecurity_Property` is hardcoded to `Confidentiality` for every CSG. (HIGH)**

Observed on all 15 rows, including Tampering, Spoofing and DoS scenarios where the correct
properties are Integrity, Authenticity and Availability. The STRIDE→property mapping is standard
and unambiguous, but applying it means threading `STRIDE Category` from `05_Threat_Scenarios`
through the reader payload schema into the generator — a wider change than this slot allows, and
one that touches a schema three downstream skills read. Descoped deliberately; this is the top
candidate for the next `cyber` polish.

**B. `02_CS_Goals_Echo` column shift in `cs-concept-builder`. (MED)**

While verifying the downstream chain: that tab's header row reads `CSG ID | Threat | Asset | CAL
| TARA IDs` but the data row places goal text under `CAL` and the CAL value under `TARA IDs` —
headers are one column short of the data. Belongs to `cs-concept-builder`, polished 2026-09-08;
not touched today.

**C. `_suggest_cal()` ignores safety impact.** SKILL.md documents the heuristic as
"Risk Value 5 + Severe Safety Impact → CAL 4", but the implementation keys on risk value alone.
Either wire the impact rating in or correct SKILL.md. Doc/impl drift, low risk.

**D. Chain audit is name-level only.** `chain_contract_audit.py` asserts that a referenced *tab*
exists; it reported 0 BREAK on this chain the entire time the column mapping was wrong. A
column-level assertion (reader's expected headers vs producer's emitted headers) would have
caught this on day one and would likely catch the same shape in other reader pairs.

---

## 2026-09-22 — second pass (POLISH, W39 Tuesday slot, issue #62)

**Severity: HIGH — fixed this run.** `Cybersecurity_Property` was written as the constant
`Confidentiality` on every derived goal. This was finding **A** of the 2026-09-16 pass, filed
as #62 during W39 planning and slotted as this week's Tuesday target.

### The defect

`generate_cs_goals.py` wrote `csg.get("property", "Confidentiality")` into
`03_Cybersecurity_Goals` col 6 and `06_CS_Concept_Handoff` col 5. Nothing ever set
`property` — `tara_reader.py` never read a STRIDE category at all — so the `.get()` default
was the value in every case except the two rows carrying an explicit `csg_overrides.property`
in the refinement JSON. Measured on the ESC sample: **13 of 15 goals mislabelled
Confidentiality**, including all five Tampering, both Spoofing, both DoS, the Repudiation and
the Elevation-of-Privilege rows.

The reason the property was never read is structural, not an oversight in the reader's field
list: `tara-builder` does **not** carry a property or STRIDE column on
`11_Cybersecurity_Goals` (its headers are `CSG ID | Derived From Scenario | Cybersecurity Goal
| Risk Value | CAL`). STRIDE lives one tab away on `05_Threat_Scenarios`, keyed by scenario ID.
Deriving the property therefore requires a second index off a second tab — which is why the
original author reached for a default instead.

### What was fixed

**1. STRIDE → property derivation. (HIGH, fixed)** Added `_STRIDE_TO_PROPERTY`,
`_stride_to_property()` and `_build_stride_index()` to `tara_reader.py`. The index is built
alongside the existing `_build_asset_index()` — same tab, same key — and threaded through both
read paths (`_read_csg_tab` and the `09_Risk_Determination` fallback), so goals now carry a
`property` key. Mapping: Spoofing→Authentication, Tampering→Integrity,
Repudiation→Non-repudiation, Information Disclosure→Confidentiality, DoS→Availability,
Elevation of Privilege→Authorization. The STRIDE column is resolved **by header name** with a
positional fallback to col 3 — the same discipline the 09-16 pass established for the goal
columns, and for the same reason.

**2. The default is no longer a property. (fixed alongside)** Both generator call sites now
emit `Not Determined` rather than `Confidentiality` when nothing derived one. A goal labelled
with a property the TARA never claimed is worse than one visibly marked undetermined: the
former is invisible to a reader, the latter is a question. The reader warns on stderr when
`05_Threat_Scenarios` is missing entirely, and when a STRIDE cell is present but unrecognised;
an *empty* STRIDE cell is silent, because absent is not the same as malformed.

**3. Mapping table stated in SKILL.md.** New "Cybersecurity property derivation" section giving
the six-row table plus the precedence order (override → STRIDE → `Not Determined`), so the
reviewer has a documented contract to check against rather than inferring it from code. This
was an explicit clause of #62's definition of done.

`csg_overrides.property` still wins over derivation — `_apply_csg_overrides()` runs after the
read, unchanged. On the ESC sample CSG-003 stays `Integrity` by override even though TS03 is a
Spoofing scenario, which is correct: explicit analyst intent beats a heuristic.

### Verification

Built `tara-builder` → `cs-goals-builder` for real rather than reasoning about it.

| Check | Before | After |
|---|---|---|
| Distinct properties, ESC sample (15 goals) | 2 (13 Confidentiality, 2 override) | **6** |
| `Confidentiality` rows, input with all Information Disclosure scenarios removed | 11 of 11 | **0** |
| Cells differing between the two workbooks | — | **18** — all in `03` col 6 and `06` col 5 |
| `09_Risk_Determination` fallback path | n/a | derives correctly (6 properties) |
| TARA with `05_Threat_Scenarios` deleted | n/a | 15× `Not Determined` + warning |
| Unrecognised STRIDE value (`'Cromulence'`) | n/a | `Not Determined` + named warning |

Both assertions #62 named as its definition of done pass: ≥3 distinct values on the sample, and
**zero** Confidentiality rows on an input containing no Information Disclosure threat. Every
figure above was re-derived from the repacked `.skill` archive, not from the working copy.

`cs-goals-checklist-reviewer` over the fixed output: CR 8 FC / 1 PC / 2 NO / 3 PENDING;
CSGA 5 FC / 1 LC / 2 PC / 1 NO / 1 NA / 2 PENDING; VA 6 PENDING.

### Findings raised, not fixed

**A. The reviewer's property-coverage check cannot pass, and could not see this fix. (MED — new,
needs a decision.)** `csga_07_property_coverage` requires `{"C","I","A","Auth","Authz","NR"}`
but `cs_goals_probe.py` adds the cell value verbatim to `properties_covered`. Run over the
before and after workbooks it returns the **identical** string both times —
`NO — Property coverage incomplete. Missing: A, Auth, Authz, C, I, NR` — for a workbook with one
property and for one with all six. It is a constant, not a check. Two defensible fixes exist and
they are not equivalent: normalise full names to abbreviations in the probe, or restate the
check in full names. The abbreviations are what both SKILL.md files document (`cs-goals-builder`
line 79, the check description itself); the full names are what every builder has always
emitted. That is a convention call, so I made neither — this is the "small and shipped beats big
and broken" line. Worth noting it is also the first live candidate for the unused
`reviewer-finding` label flagged in the 09-20 triage.

**B. #62's stated downstream impact is wrong, and the issue should be corrected on close.**
The issue says the wrong property is inherited by `cs-concept-builder`, "which fans one CSR per
goal *per security property*". It does fan per property — but it enumerates all six from its own
`NODE_TYPE_PROPERTIES` table and **never reads `Cybersecurity_Property` from the CS Goals
workbook at all** (no occurrence of the string in any file of the archive). So the corruption
was confined to the CS Goals workbook and whoever read it; it did not propagate down the chain.
The fix is still right and the severity still HIGH — a mislabelled goal is an audit finding on
its own — but the chain-contamination framing came from the 09-16 log and was never checked.

**C. Carried, unchanged from the 09-16 pass:** `_suggest_cal()` still keys on risk value alone
while SKILL.md documents "Risk Value 5 + Severe Safety Impact" (LOW, doc/impl drift).
