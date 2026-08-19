# fmeda-builder polish log

_Polish target for W23 (issue [#15](https://github.com/jherrodthomas/automotive-skills-suite/issues/15)). Reviewer: autonomous daily-standup task._

---

## 2026-06-04 — first POLISH pass

**Mode:** POLISH (Thursday — third POLISH day of W23)
**File reviewed:** `skills/fmeda-builder.skill` (ZIP archive; SKILL.md is 9,673 bytes / ~155 lines; 10 files total in archive).
**DoD recap (from `docs/weekly/WEEK-2026-W23.md`):**
confirm the description's "13-tab workbook" claim matches the actual generator tab list,
spot-check the SPFM / LFM / PMHF target numbers against ISO 26262-5 Table 6,
and audit the "Key formulas" section in SKILL.md for internal consistency.

### DoD verdict

| DoD check | Result |
|---|---|
| 13-tab claim matches generator schema | **PASS** (cross-check vs. Output structure table; rows 00–12 enumerated) |
| SPFM / LFM / PMHF target numbers vs. ISO 26262-5 Table 6 | **PASS** (90/97/99 for SPFM B/C/D, 60/80/90 for LFM B/C/D, 100/100/10 FIT for PMHF B/C/D — all match standard) |
| "Key formulas" section internal consistency | **FAIL** — Classification ladder has a logically unreachable branch (see finding #1) |

### What's good

- **Description is well-shaped.** 720 / 1024 chars, names every formal trigger phrase
  a user would type ("FMEDA", "SPFM", "LFM", "PMHF", "ISO 26262-5", "diagnostic
  coverage", "safety mechanisms"), and closes with the suite-standard "Always use this
  skill instead of producing a freeform FMEDA in chat." line. No version-number gap of
  the kind that bit `aspice-assessment-builder` (#5) and `cs-concept-builder` (#4) —
  there's only one ISO 26262 revision relevant here (2018).
- **Frontmatter is clean.** Both required keys present (`name`, `description`); YAML
  parses without complaint; no drift fields.
- **ASIL targets are right.** Intro paragraph and PMHF pitfall section agree, and both
  match ISO 26262-5:2018 Table 6 (SPFM ≥90/97/99% for ASIL B/C/D; LFM ≥60/80/90% for
  B/C/D; PMHF ≤100/100/10 FIT for B/C/D). This is the math users would most plausibly
  mis-remember, so getting it locked in two places is a real strength.
- **13-tab list is exact.** The Output Structure table (00 Title Page → 12 References)
  enumerates 13 rows and the Step 4 review checklist references tabs `03` through `11`
  by name — every reference resolves to a tab in the table. No drift between the
  description's "13-tab" claim and the body.
- **Workflow ordering is correct.** Step 1 (BOM JSON) → Step 2 (read references, with
  the right three files named in the right order) → Step 3 (run generator + recalc)
  → Step 4 (analyst review, tab-by-tab). The Step 2 instruction to read the bundled
  references is the pattern `aspice-assessment-builder` is *missing* and `fmeda-builder`
  gets right.
- **Pre-requisites are explicit.** "A TSC workbook (produced by tsc-builder)" and
  "A HW BOM JSON" — names the upstream skill by ID, not by hand-wave. Makes the chain
  dependency auditable.
- **Common pitfalls section is mentor-quality content.** Items #1 (FIT sourcing),
  #2 (DC% evidence), #3 (residual fault accounting), and #4 (PMHF units) are exactly
  the four mistakes a junior FuSa engineer makes in their first FMEDA. This is not
  filler — it's the right content for an audit-grade builder.

### What to fix

1. **MEDIUM — Classification ladder in "Key formulas" has an unreachable branch.**
   The current text reads (paraphrased):

   ```
   If not safety-related → S
   If allocated mechanism with DC% and DC% = 100 → S
   Else if allocated mechanism → check DC%:
       If DC% < 100 → RF
       If no mechanism or DC% = 0 → SPF
       If allocated mechanism but covers multiple points → MPF_D or MPF_L
   ```

   The inner "If no mechanism or DC% = 0 → SPF" branch sits inside an "Else if
   allocated mechanism" block — so the "no mechanism" disjunct is logically
   unreachable from that position. Two fixes are possible: (a) flatten the ladder so
   "no mechanism → SPF" is a sibling branch of "allocated mechanism with DC% = 100 →
   S", or (b) restate as a decision table. Either way, the current nesting cannot
   be evaluated as written. Severity: **medium** (math content; a careful analyst
   reading the formula spec literally will get the wrong classification for an
   unmechanized failure mode).

2. **MEDIUM — "SMvDU (Safe Fault Metric)" acronym in pitfall #5 is not a standard
   ISO 26262 term.** The Common Pitfalls section closes with:
   > "This is why LFM has separate targets — it's about SMvDU (Safe Fault Metric)
   > paired with the architecture's diagnostic coverage of two-point faults."

   Neither ISO 26262-5:2018 nor the standard FuSa vocabulary (Annex B) defines
   "SMvDU". The closest standard terms are λ_S (safe fault rate), MPF_DP (multipoint
   fault, detectable/perceivable), and λ_S,LF (safe latent fault contribution). The
   parenthetical "(Safe Fault Metric)" suggests the author meant either the Safe
   Fault contribution to LFM, or possibly conflated MPF_L (latent multipoint) with
   a Safe-Fault-style ratio. Severity: **medium** (a reader will Google "SMvDU"
   and find nothing). Fix requires a real source check, not a typo correction.

3. **LOW — SPFM and LFM intro phrasings invert the metric direction.** Intro reads:
   > "**SPFM** ... Coverage of *undetected* failure modes. Target: 90% (ASIL B), ..."
   > "**LFM** ... Coverage of *latent* (undetected two-point) failures. Target: 60% ..."

   By ISO 26262-5 definition, SPFM = 1 − Σ(λ_SPF + λ_RF) / Σ(λ_safety_related) and
   LFM = 1 − Σ(λ_MPF,L) / (Σ(λ_safety) − Σ(λ_SPF + λ_RF)). Both metrics measure the
   fraction of safety-related faults that ARE handled (safe or detected), not the
   fraction undetected. The intro's "Coverage of *undetected*" is the inverse of
   what the formula actually computes — a target of 99% SPFM means 99% of single-
   point and residual fault rate is COVERED, not undetected. Severity: **low**
   (the targets themselves are right and Step 4 later describes metrics correctly,
   but the one-line definitions at the top of SKILL.md will mislead a reader
   skimming the intro).

4. **LOW — `failure_mode_overrides` JSON example uses `distribution_pct: 0.3`.**
   In the BOM JSON example the override row says `"distribution_pct": 0.3` but the
   "Key formulas" section says `λ = FIT × (distribution % / 100)`. So a
   distribution of 0.3 in the JSON would mean 0.3% of failures — almost certainly
   not the author's intent (a stuck-at fault is typically 30–40% of an MCU's
   failure mode budget, not 0.3%). Either the JSON example should read `30` or the
   formula should read `× distribution_pct` (without the `/100`). Severity: **low**
   (the example is documentary, not run-tested, but an analyst cloning the example
   will produce an under-estimate by 100×). Fix needs a maintainer eyeball to
   confirm the intended unit convention before flipping either side.

5. **LOW (obs) — Step 4 instruction "_When done, save + re-run `recalc.py`_" lacks
   the same explicit error-checking the rest of the workflow does.** Other suite
   skills (e.g. `tsc-builder`) name `#REF!` and `#DIV/0!` as the specific tokens to
   grep for; this skill says "confirm all formulas evaluate and no #REF/#DIV/0
   errors remain." The phrasing is close but the `!` punctuation is dropped, which
   matters for a CTRL-F. Severity: **low (obs)**.

### Suggested edits (NOT applied this run)

The autonomous-edit allowlist for the daily-standup task is narrow — typo /
over-length description / missing-required-frontmatter-field. **None of the five
findings match that list:**

- #1 (Classification ladder) needs a structural rewrite of a multi-line spec
  block, not a surgical edit. Requires a 5–10-line replacement with re-checked
  precedence; better to do this with a human eyeball.
- #2 (SMvDU acronym) needs source research to identify the right replacement term,
  not a substitution. Could be deletion, could be a re-naming to λ_S,LF — either
  way it's a content decision.
- #3 (SPFM/LFM intro inversion) is a two-sentence rewrite touching the
  most-skimmed part of the SKILL.md. Worth doing carefully.
- #4 (distribution_pct unit) requires deciding which side (JSON or formula) is the
  source of truth, then changing the other to match — and possibly re-checking
  the generator script against whichever side is kept. Not a surgical edit.
- #5 is a `!`-punctuation tidy. Borderline allowlist material but I'm declining
  on the conservative reading.

**No code edits committed today.** Issue #15 stays open with this log linked from
the journal entry.

Proposed minimal rewrite of the SPFM / LFM intro lines (for human review):

```
- **SPFM** (Single-Point Failure Metric): Fraction of safety-related fault rate
  that is *not* uncovered single-point or residual. Target: ≥90% (ASIL B),
  ≥97% (C), ≥99% (D).
- **LFM** (Latent Fault Metric): Fraction of remaining safety-related fault rate
  (after SPFM) that is *not* uncovered latent multipoint. Target: ≥60% (B),
  ≥80% (C), ≥90% (D).
- **PMHF** (Probabilistic Metric for Hardware Failures): Raw uncovered failure
  rate (λ_SPF + λ_RF), in FIT. Target: ≤100 FIT (B/C), ≤10 FIT (D).
```

Proposed flattened Classification ladder:

```
If not safety-related                                  → S
Else if allocated mechanism AND DC% = 100              → S (safe due to detection)
Else if allocated mechanism AND covers multipoint:
    If second-fault detection in place                 → MPF_D
    Else                                               → MPF_L
Else if allocated mechanism AND DC% < 100              → RF
Else (no mechanism OR DC% = 0)                         → SPF
```

### Other observations (not fixes, just notes for future passes)

- The skill bundles three references (`methodology.md`, `failure_mode_libraries.md`,
  `metrics_targets.md`) totaling ~23.6 KB — substantial mentor content. Step 2 of
  the workflow correctly tells Claude to read them. This is the right pattern; it
  is what `aspice-assessment-builder` is missing.
- Generator script is 20.5 KB. Did not deep-audit script content this pass; the
  STATUS regen + this log filled the slot. Worth a script-level pass on a future
  POLISH day, particularly to confirm that the actual classification logic in
  `generate_fmeda.py` matches whichever flattened ladder we land on for finding #1.
- No `.placeholder` cruft in this archive (unlike `aspice-assessment-builder`).
  Archive is clean.
- The `examples/sample_fmeda_bom_esc.json` example is a real ESC (Electronic
  Stability Control) BOM, not a toy. Likely valuable as a public reference
  artefact for the eventual `examples/fmeda-builder/README.md` stub.

### Severity roll-up

| Finding | Severity | Action |
|---|---|---|
| Classification ladder has unreachable "no mechanism" branch | medium | flattened ladder drafted; await human review |
| "SMvDU (Safe Fault Metric)" non-standard acronym in pitfall #5 | medium | flagged; needs source research before substitution |
| SPFM/LFM intro lines invert metric direction ("Coverage of *undetected*") | low | three-line rewrite drafted; await human review |
| `failure_mode_overrides.distribution_pct: 0.3` likely 100× off | low | flagged; needs maintainer call on unit convention |
| `#REF/#DIV/0` lacks `!` punctuation in Step 4 close | low (obs) | flagged; suite-wide style item |

**No code edits committed in this run.** Two medium-severity findings (logic bug
in Classification ladder + non-standard acronym) plus three low-severity items.
This is the **first** fmeda-builder polish pass — earlier passes targeted
description-quality and trigger-list shape, but this run uncovered actual math /
content issues. Recommend the Classification ladder fix gets prioritized in a
maintainer touch-up rather than carried as another polish-log appendix; the logic
bug is reachable and would produce a wrong rating for an unmechanized failure
mode if read literally.

## 2026-08-18 — chain-contract audit finding (issue #46 pass)

**Severity: high.** Not a cosmetic rename. Found by `scripts/chain_contract_audit.py`,
then hand-verified by execution. No `.skill` file was modified this run — #46's
definition of done is read-only, and the repair belongs on a POLISH day of its own.

### What's good

- `read_tsc()` is defensive in the right places: it locates the header row by
  content rather than assuming a fixed offset, tolerates missing columns, and
  parses `"99%"`, `99`, and `None` into a float without throwing.
- The FMEDA metric tabs (SPFM / LFM / PMHF) are formula-driven off the editable
  DC% column, so an analyst who fills the worksheet by hand still gets correct
  arithmetic. The break below degrades the *import*, not the *math*.

### What to fix

`fmeda-builder/scripts/tsc_reader.py` cannot read a workbook produced by
`tsc-builder`. Two independent defects, both in `read_tsc()`:

**1. Wrong tab name (line 21).** The reader asks for `05_Safety_Mechanisms_From_TSC`
and returns `{}` if it is absent. `tsc-builder` emits no such tab — its mechanism
tab is `04_Safety_Mechanism_Catalog`. `05_Safety_Mechanisms_From_TSC` is
**fmeda-builder's own output tab** (`generate_fmeda.py:239`); the reader is
hunting for its own echo tab inside the upstream workbook.

Corroboration: every other reader of a TSC workbook in this repo —
`hw-architecture-builder`, `sw-arch-builder`, `safety-case-builder` — reads
`04_Safety_Mechanism_Catalog`. `fmeda-builder` is the lone outlier.

**2. Column-1-only header scan (lines ~30-36).** The header probe reads
`ws.cell(r, 1)` for rows 1-10 and looks for `"Mechanism ID"`. In
`tsc-builder`'s catalog the row-4 header is:

```
FSR_ID | Allocated ASIL | Branch | Linked Node | Mechanism ID | Mechanism Name | Default DC% | Detection Time (target) | Selection
```

`Mechanism ID` sits in **column 5**. So even after the tab is renamed correctly,
the header row is never found and the function still returns `{}`.

### Evidence (executed, not inferred)

Ran `read_tsc()` against three synthetic workbooks built to `tsc-builder`'s
emitted shape:

| Input | Result |
|---|---|
| A. Real tab name `04_Safety_Mechanism_Catalog`, real 9-column header | `{}` |
| B. Tab renamed to `05_Safety_Mechanisms_From_TSC`, real 9-column header | `{}` |
| C. Tab renamed **and** headers moved to column 1 | 2 mechanisms parsed correctly |

B is the important row: it isolates defect 2 and proves a one-line rename is an
incomplete fix. C is the control — it confirms the parse logic itself is sound
once it can find the header.

### Blast radius

`mechanisms` is consumed only by `build_tsc_mechanisms()` (`generate_fmeda.py:470`).
`build_fmeda_worksheet()` accepts the dict but never reads it — column 9
"Allocated Mechanism" is written empty and DC% defaults to 50 for the analyst to
edit. So:

- **Not affected:** SPFM / LFM / PMHF arithmetic. Nothing is silently miscomputed.
- **Affected:** tab `05_Safety_Mechanisms_From_TSC` ships header-only on every run,
  no matter what TSC is passed. SKILL.md line 70 claims the skill "Reads chosen
  mechanisms + baseline DC% from the TSC" and line 81 tells the analyst to use
  that tab to "verify that every failure mode you enumerated in FMEDA is covered
  by at least one mechanism". That cross-check has never been possible.
- The failure is **silent**: no exception, no warning, an empty tab that looks
  like a TSC with no mechanisms rather than a failed read. Identical shape to #43.

### Suggested edits (deferred — do not apply in an audit pass)

1. Accept a tuple of names, preferred first, exactly as the #43 repair did in
   `cs-architecture-builder/scripts/cs_concept_reader.py`:
   `MECH_SHEETS = ("04_Safety_Mechanism_Catalog", "05_Safety_Mechanisms_From_TSC")`.
2. Widen the header probe to scan all columns of rows 1-10, not column 1 only.
3. Return a `(mechanisms, warnings)` pair, or log to stderr, so a zero-row import
   is visible instead of silent.
4. Drop the unused `mechanisms` parameter from `build_fmeda_worksheet()`, or wire
   it into the "Allocated Mechanism" column as the signature implies it should be.
5. Add the tab contract as a module docstring, the way `cs_concept_reader.py`
   documents its own.

Tracked as its own issue. Items 1-2 are the fix; 3-5 are the reason it went
unnoticed for as long as it did.

---

## 2026-08-19 — #53 fix pass (chain break repaired)

**Mode:** POLISH (Wednesday, W34)
**Issue:** [#53](https://github.com/jherrodthomas/automotive-skills-suite/issues/53) — `skill-bug`, `chain-break`, `safety`
**File changed:** `skills/fmeda-builder.skill` → `fmeda-builder/scripts/tsc_reader.py` (rewritten, 88 → 197 lines)
**Severity:** medium — no metric was ever miscomputed; an advertised import silently produced nothing.

### Target selection

Yesterday's follow-up slotted Wednesday for #51 (`autosar-bsw-config-builder`). Overridden:
the standing POLISH priority order puts "open issue labeled `skill-bug`" first, #53 carries
both `skill-bug` and `chain-break`, and yesterday's own notes also asked for it "on a POLISH
day". It was found yesterday, is bounded, and already had a written DoD — fixing it while the
context is warm beats letting it age. #51 moves to Thursday.

### Verification chain — real, not synthetic

Yesterday's evidence used synthetic workbooks built to tsc-builder's shape. DoD item 5 required
a real one, so the full upstream chain was executed from the shipped sample inputs:

| Step | Command | Result |
|---|---|---|
| HARA | `generate_hara.py sample_input_esc.json` | 25 safety goals, 468 significant rows |
| FSC | `generate_fsc.py hara.xlsx sample_block_diagram_esc.json` | 375 FSRs, 375 ASIL allocations, 25 fault trees |
| TSC | `generate_tsc.py fsc.xlsx sample_architecture_esc.json` | 13 tabs, 375 chosen mechanisms, 750 TSRs |

`04_Safety_Mechanism_Catalog` came out exactly as the issue predicted: title row 1, analyst
note row 2, header row 4, `Mechanism ID` in column 5.

### Before / after against that real TSC

| | mechanisms parsed | distinct nodes | exception | warning |
|---|---|---|---|---|
| Before | **0** | 0 | none | none |
| After | **39** | 15 | none | none (clean read) |

Full `generate_fmeda.py` run against the real TSC: 13 tabs, 30 FMEDA rows, 8 HW elements.
`05_Safety_Mechanisms_From_TSC` went from header-only to 39 populated rows.
`07_SPFM` / `08_LFM` / `09_PMHF` / `06_FMEDA_Worksheet` shapes unchanged — no regression.

### DoD

| # | Requirement | Status |
|---|---|---|
| 1 | Preferred-then-legacy tab tuple | **DONE** — `MECHANISM_SHEETS = ("04_Safety_Mechanism_Catalog", "05_Safety_Mechanisms_From_TSC")`, same shape as the post-#43 `cs_concept_reader.py` |
| 2 | Header probe scans all columns of rows 1-10 | **DONE** — `_find_header_row()` sweeps rows 1-10 × cols 1-20 |
| 3 | Zero-row import surfaced, not silent | **DONE** — stderr warning on missing tab, header-not-found, zero rows parsed, and legacy-tab use |
| 4 | `chain_contract_audit.py` reads MATCH | **DONE** — `fmeda-builder → tsc-builder` now MATCH + ALIAS; repo-wide **0 BREAK** (was 1) |
| 5 | Verified against real tsc-builder output | **DONE** — see chain table above |

Negative cases exercised: workbook with no catalog tab → `{}` + warning; catalog tab with a
header but no data rows → `{}` + warning; legacy-named tab with the old column-1 layout →
parses, with a warning naming the legacy tab.

### Two defects found while fixing, beyond the issue's scope

**A. DC% ranges parsed to 0.0.** Not in the issue. The catalog carries qualitative text —
`60-80%`, `>=99%`, `90-99%`, `99%+` — and the old `float(dc_str.replace("%",""))` raised on
every one of them, falling back to 0.0. Fixing tabs 1-2 alone would have shipped a "working"
import where all 39 mechanisms read DC = 0 — visibly worse than the empty tab it replaced.
Now: ranges collapse to their midpoint (`60-80%` → 70.0), bounded forms take the bound
(`>=99%` and `99%+` → 99.0), and the original text is preserved in a new `dc_raw` key.
3 of 39 still read 0.0 — all genuinely `n/a` in the catalog. That is honest, not a parse failure.

**B. Alternative-candidate rows lost their node.** tsc-builder writes FSR_ID / ASIL / Branch /
Linked Node only on the first `[primary]` row; `[alternative]` rows leave them blank. Without a
forward-fill every alternative keys to `(None, mech_id)` and collides across FSRs. The reader now
carries the last seen Linked Node forward. This is what produced 15 distinct nodes instead of 1.

### Left alone, deliberately

- `build_fmeda_worksheet()` still takes a `mechanisms` param it never reads — real smell, explicitly
  out of scope per the issue. Still unfiled.
- `dc_raw` is populated but nothing consumes it. The echo tab keeps writing the numeric `dc` into its
  numeric "Default DC%" column. Showing the analyst `60-80%` instead of `70` is arguably more honest
  and is a one-line change to `build_tsc_mechanisms()` — but it changes a column's type, so it is a
  separate decision, not a drive-by.
- SKILL.md needed **no** edit. Line 70 ("Reads chosen mechanisms + baseline DC% from the TSC") and
  line 81 (the coverage cross-check) were aspirational before this pass and are now simply true.

### Suggested next

- Extend `chain_contract_audit.py` to column contracts. Defect 2 of #53 and defect A above are both
  column-layout failures that a tab-name scanner cannot see. This is the second run in a row where
  the real bug was one level below what the scanner checks.
