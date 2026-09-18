# hw-safety-reqs-builder — example

**What this skill produces:** An ISO 26262-5 §6 Hardware Safety Requirements workbook — **10 tabs**, counted from the `create_sheet` calls in `scripts/generate_hw_safety_reqs.py` on 2026-09-18: `00_Title_Page`, `01_Document_Control`, `02_HW_TSRs_From_TSC`, `03_HW_Safety_Requirements`, `04_Failure_Mode_Mapping`, `05_HSI_Reference`, `06_Verification_Methods`, `07_Test_Strategy`, `08_Independence_Considerations`, `09_References`. All 10 carry data on a real run — verified 2026-09-15 by executing the full upstream chain, not by reading the source.

**Typical input shape:** Two arguments. (1) A TSC workbook xlsx, normally `tsc-builder` output; `scripts/tsc_reader.py` reads `05_TSR_Catalog` (filtering `HW-TSR` from `SW-TSR`), `00_Title_Page` for document control, and `03_System_Architecture` for allocated hardware nodes. (2) A project metadata JSON matching `examples/sample_hw_sr_input_esc.json` — `project.*`, `linked_tsc`, and the optional `hw_sr_overrides` list keyed on `parent_hw_tsr`.

**Expected output:** `<name>.xlsx` with one or more HW-SRs derived per HW-TSR by template, each carrying a failure-mode set, a target DC%, an allocated hardware element and a verification method. ASIL is **inherited from the parent TSR**, not defaulted — a decomposed `B(D)` survives both hops from the FSC. Unrefined fields land as `<TBD: ...>` placeholders for the analyst.

**Sample I/O:**

```bash
python scripts/generate_hw_safety_reqs.py TSC.xlsx sample_hw_sr_input_esc.json HWSR.xlsx
python scripts/recalc.py HWSR.xlsx          # optional; evaluates formulas via LibreOffice
```

The 2026-09-15 polish pass built the input from the shipped ESC fixtures rather than a hand-made stub, which is the honest way to exercise this skill:

```
hara-builder  sample_input_esc.json          -> HARA.xlsx  (900 rows, 25 safety goals)
fsc-builder   HARA.xlsx + block_diagram.json -> FSC.xlsx   (375 FSRs, 25 fault trees)
tsc-builder   FSC.xlsx + architecture.json   -> TSC.xlsx   (750 TSRs, of which 375 HW-TSR)
hw-safety-reqs-builder TSC.xlsx + input.json -> HWSR.xlsx  (10 tabs, 825 HW-SRs)
```

**Read the stderr, not just the exit code.** As of `a8f430d` (2026-09-15) the generator reports override outcomes: the JSON summary carries `overrides_supplied`, `overrides_applied` and `overrides_unmatched`, and any override whose `parent_hw_tsr` matches no TSR in the TSC raises a `WARNING` on stderr naming the unmatched key. Before that fix the mismatch was silent — the shipped example keyed its two overrides on a stale three-segment ID (`TSR-001-01`) while `tsc-builder` emits four segments (`TSR-001-01-01`), so both overrides were discarded, the run still exited 0, and the generic template text shipped as though refinement had been applied. If you supply overrides, confirm `overrides_applied` equals `overrides_supplied` before trusting the workbook.

**Paired reviewer:** `hw-safety-reqs-checklist-reviewer`. Unlike the mbse / sysml / traceability pairs repaired earlier this quarter, this reviewer does **not** certify an empty workbook — the 2026-09-15 empty-input regression scored 0 FC and 12 NO across both substantive tabs, and HWSRA-4 (allocated element specified, no `<TBD>`) and HWSRA-10 (test strategy coverage) move with the content rather than resting on a hard-coded pass.
