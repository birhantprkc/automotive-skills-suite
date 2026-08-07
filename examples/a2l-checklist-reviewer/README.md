# a2l-checklist-reviewer — example

**What this skill produces:** confirmation-review checklist xlsx over an A2L calibration description workbook — 30 ASAM MCD-2 MC v1.7 checks across Summary (KPI tiles, rating pie, per-section bars), Confirmation Review (14), A2L Object Completeness (8), Memory & Address Validation (5), Conversion Method Validation (3).
**Typical input shape:** a completed A2L workbook xlsx, normally the 13-tab output of `a2l-builder`; best-effort on other A2L-shaped workbooks.
**Expected output:** `<name>_checklist.xlsx` with every check rated FC / LC / PC / NO / NA, or `Pending` where reviewer judgment is required. The source A2L workbook is never modified.
**Sample I/O:** `python scripts/generate_checklist.py a2l_workbook.xlsx output_checklist.xlsx` — a fully populated 13-tab A2L yields mostly FC with Pending rows on the subjective conversion-unit checks.
**Paired builder:** `a2l-builder`.
