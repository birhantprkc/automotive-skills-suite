# Polish log — dia-builder / dia-checklist-reviewer

## 2026-09-17 — first pass (POLISH)

**Selected because:** zero open issues and zero orphan builders, so selection fell to
least-recently-touched. `dia-builder.skill` was last touched 2026-05-01 and had no
polish log entry.

**Severity: high** (three false findings on the pair's own canonical sample)

### What's good

- `generate_dia.py` runs clean on `examples/sample_dia_esc.json` and emits all 12
  documented tabs, matching the SKILL.md output table exactly. No drift between the
  documented tab list and the generated one.
- Frontmatter is well-formed; description is 643 chars, comfortably inside the 1024 limit.
- The auto-RACI default table in SKILL.md matches what the script actually emits.
- `dia_probe.py` correctly detects builder format and reads parties, RACI rows,
  communication channels and supplier deliverables.

### What was broken (fixed this run, reviewer side only)

All three were reader-contract mismatches: the builder writes valid content, the
reviewer failed to read it and reported a compliance defect that did not exist.

1. **Joint reviews never read — DIAA-8 always PC.**
   `dia_probe.py` looked for columns `milestone` / `participants`; `generate_dia.py`
   writes `Review Name` / `Attendees` / `Planned Date`. The milestone column was never
   found, so every row was skipped and `n_joint_reviews` was 0 on a workbook with 7
   fully-scheduled reviews. DIAA-8 reported "No joint reviews defined."
   *Fix:* added `review name` / `review` and `attendees` / `planned date` aliases.

2. **Item scope never read — DIAA-14 always PC.**
   `_find_header_row` requires >=3 populated cells in a row. `03_Item_Scope` is a
   two-column vertical layout (`In Scope` heading, then bullet rows, then
   `Out of Scope`), so no header row was ever found and both scope lists stayed empty.
   DIAA-14 reported "0 in-scope, 0 out-of-scope" against 6 in-scope and 5 out-of-scope
   bullets.
   *Fix:* added `_scan_vertical_scope()` fallback that scans column 1 for section
   markers and strips bullet glyphs. Only runs when the header-based parse finds nothing,
   so non-builder DIAs are unaffected.

3. **Combined RACI cells misread — DIAA-4 and DIAA-5 always NO.**
   The builder writes combined assignments (`A,R`) in one cell, as its own documented
   default mapping requires. The checks compared `v.upper() == "A"` exactly, so `A,R`
   counted as neither Accountable nor Responsible. All 10 such rows were flagged.
   *Fix:* added `_raci_tokens()` in `check_definitions.py` to split on `,/;+` and space.
   Also tightened the probe so `assignments` holds party columns only — `WP_ID` and
   `ISO Ref` were previously being scanned for role letters.

**Result on the canonical sample:** DIAA went from `FC 6 / NO 2 / PC 2` to
`FC 8 / NO 2`. The two remaining NOs are real (see below).

### What to fix next (not done this run)

- **`examples/sample_dia_esc.json` has a genuine RACI defect** (medium). With the
  reviewer now reading correctly, WP11 Safety Plan carries `A` for both Phoenix and
  ChassisCorp and no `R` at all; WP12 Safety Case carries `A,R` for both parties.
  Dual-Accountable violates the rule DIAA-4 enforces. This is arguably an intentional
  joint-ownership statement, so it is a contract-semantics decision, not a typo —
  left alone deliberately. Either correct the sample to single-A, or relax DIAA-4 to
  permit declared joint accountability. Needs a human call.
- **`_find_header_row`'s >=3-cell rule is a latent trap** (low). Any two-column tab in
  any builder in this suite is invisible to its reviewer for the same reason. Worth a
  suite-wide sweep rather than a per-skill patch.
- No automated regression test exists for the pair; these three bugs survived since
  2026-05-01 because nothing runs builder-output through reviewer-probe.
