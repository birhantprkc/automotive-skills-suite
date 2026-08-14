# cdd-checklist-reviewer — example

**What this skill produces:** A confirmation-review checklist xlsx over a CDD (CANdela Diagnostic Description) workbook — **28 checks** across 7 tabs, counted from `scripts/check_definitions.py` on 2026-08-14: Title, General Info, Guide, Summary (KPI tiles, rating pie, compliance bars, findings table), **Confirmation Review (10 `cr_*` checks)**, **CDD Assessment (12 `ca_*` checks,** ISO 14229-1 + Vector CANdela conventions**)**, and **Variant Assessment (6 `va_*` checks** covering variant coding and inheritance**)**.

**Typical input shape:** A completed CDD authoring workbook xlsx — normally the output of `cdd-builder`, best-effort on other CDD-shaped workbooks. `scripts/cdd_probe.py` reads the Title page (title, project, doc ID, revision, author, approver, status), the Document Control tab (revision-history row count), and then counts `sessions`, `services`, `diids`, `riids`, `security_levels` and `variants`, plus the DTC cross-reference string and a table-of-contents flag.

**Expected output:** `<name>_checklist.xlsx` with every check rated FC / LC / PC / NO / NA, or left `Pending` with an `(Auto-suggest)` draft finding where reviewer judgment is required. The source CDD is never modified — gaps land in the Recommended Actions column.

**Sample I/O:**

```bash
python scripts/generate_checklist.py cdd_workbook.xlsx output_checklist.xlsx
python scripts/recalc.py output_checklist.xlsx      # optional
```

The generator prints a JSON summary carrying `status`, `checks_run` and `output`. A fully populated CDD yields mostly FC; the security-pairing check (request-seed / send-key level symmetry) and the DTC cross-reference completeness check are the two that most often come back PC on real workbooks, because both depend on content the probe can count but not semantically validate.

**Paired builder:** `cdd-builder`.

> **Doc drift found 2026-08-14 (DOCS run, not yet fixed):** the reviewer's `SKILL.md` tells the user to "read `references/methodology.md` and `references/cdd_checks.md` on first use" and lists both under "Files in this skill" — **neither file exists in the archive.** `cdd-checklist-reviewer.skill` contains 8 entries, all `SKILL.md` + `scripts/`, with no `references/` directory at all. This is the same dangling-reference class fixed in `safety-program-risk-register-builder` (`9b4660e`). Left unfixed here deliberately: repacking a `.skill` zip is a POLISH-mode change, not a Friday docs change. Queued as a follow-up.
