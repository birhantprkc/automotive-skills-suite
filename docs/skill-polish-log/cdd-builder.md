# cdd-builder — polish log

## 2026-08-11 (POLISH pass 1) — severity: **medium**, changes applied

First pass on this skill. Slot assigned by `WEEK-2026-W33.md` (Tuesday companion target,
issue #50 — diagnostics, the longest-neglected domain).

### DoD from #50, item by item
- **Frontmatter validated** — `name: cdd-builder`, description 413 chars (well under the
  1024 limit), both required keys present, no extras. Clean.
- **Generator smoke-tested** — no fixture shipped, so one was constructed from the schema
  docstring and run end to end. Produces 12 tabs, all sheet names <= Excel's 31-character
  limit (worst is `Communication Configuration` at 27). Exit status success.
- **Pairing confirmed** — `cdd-checklist-reviewer` present; its `cdd_probe.py` resolves all
  nine content tabs. Pairing is real, not nominal.
- **Polish log** — this file.
- **Example README** — `examples/cdd-builder/README.md`, written from the verified run.

### What's good
Tab set matches the SKILL.md "Output structure" table exactly, 0-11, no drift. Sheet names
are comfortably inside the length limit — one of the few builders that is (see
`docs/sheet-name-length-audit.md`). The DTC tab correctly models itself as a *cross-reference*
to `dtc-catalog-builder` output rather than duplicating DTC content, which keeps the
diagnostics chain single-sourced.

### What was fixed
**The SKILL.md file tree described four files that do not exist.** The archive contained only
`SKILL.md` + `scripts/`, but the tree diagram promised `references/methodology.md`,
`references/cdd_conventions.md`, `references/iso_services.md` and `examples/sample_input.json`
— and Step 2 told the user to "see `examples/sample_input.json` for a worked example."
Following the documented workflow hit a missing file immediately.

Fixed both ways round, preferring the honest version of each:
1. **`examples/sample_input.json` now ships** — the smoke-test fixture (a Body Control Module
   with 3 services, 2 DIDs, 1 RID, 1 security level, 1 variant) was added to the archive rather
   than deleting the reference, because Step 2's promise is a good one and the fixture is
   verified to run. The documented workflow is now executable as written.
2. **The three `references/` entries were removed from the tree** — writing three reference
   documents is content authoring, not a polish fix, and no workflow step actually reads them.
   Better an accurate tree than an aspirational one.

Re-zipped and verified from a clean extraction: `python scripts/generate_cdd.py
examples/sample_input.json out.xlsx` succeeds straight out of the archive.

### Found, NOT fixed (deliberate descope)
- **`diids` / `riids` schema keys (double-i).** The input schema uses `diids` and `riids`;
  every piece of prose, and the tab names themselves, use the conventional `DID` / `RID`.
  It reads like a typo that set. Renaming the keys breaks every input file anyone has already
  written against this skill, for a purely cosmetic gain — not a polish-day call. Documented
  in the example README instead so the next author is not caught by it.
- **Tab-naming convention drift.** This builder uses bare spaced names (`DID Catalog`) while
  most of the suite uses the `NN_Underscore_Form` (`05_DID_Catalog`). Harmonizing would be
  nicer, but `cdd_probe.py` looks tabs up by **exact string** — `wb["DID Catalog"]` — so a
  rename silently zeroes out every reviewer check unless builder and reviewer move together.
  Worth doing as a deliberate paired change; not worth doing casually.
- **No `references/` content.** The skill carries no reference material at all, unlike its
  domain siblings. `ISO 14229-1` service semantics and CANdela authoring conventions would be
  the obvious two. Real work, flagged for a future content pass.

### Net assessment
Sound generator, documentation that had drifted ahead of the archive. The fix restores the
documented workflow rather than trimming it back. Diagnostics now has a documented pass —
first since W27.
