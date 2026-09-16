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
