# Polish Log — aspice-gap-analysis-builder

## 2026-07-02 (autonomous POLISH)

**Selected because:** least-recently-touched builder (last touched 2026-05-01) with no
existing polish-log entry; no open issues and no orphan builders this run.

**Smoke test:** `generate_aspice_gap_analysis.py IGNORED.xlsx examples/sample_gap_analysis_input.json out.xlsx`
→ exit 0, `{"status":"ok","tabs":10,"processes":2}`, workbook opens with all 10 expected
tabs (00_Title_Page … 09_References). Generation is healthy.

**What's good**
- Frontmatter well-formed (name + description present); description 514 chars (well under 1024).
- SKILL.md "Output (10 tabs)" table matches the 10 tabs the script emits, in order and by name.
- Sample input (`config`, `processes`, `gaps`) matches the keys the generator reads.
- Clean styling helpers, deterministic output, JSON status line for programmatic use.

**What to fix**
- **[med] The first CLI argument `<assessment.xlsx>` is required but never read.** The
  generator signature is `generate_gap_analysis(assessment_xlsx, input_json, output_xlsx)`
  and `main()` enforces `len(sys.argv) != 4`, yet `assessment_xlsx` is never opened. The
  smoke test above passed a nonexistent path and still succeeded, proving the arg is inert.
  Consequence: users must supply a file that is silently ignored; the Current State tab is
  actually built from the JSON `processes` array, not the assessment workbook.
- **[low] `load_workbook` is imported but unused** — a direct symptom of the dead
  assessment-read path.
- **[low] Doc/behavior mismatch:** SKILL.md tab 02 says "Read-only echo of assessment
  results," but Current State is populated from `data["processes"]` in the input JSON, not
  from the assessment xlsx.

**Suggested edits (deferred — not applied this run)**
Two coherent options, both cross-file and needing thought, so captured as follow-ups rather
than done blind:
  1. **Make it real:** load the assessment workbook and populate Current State (achieved CL
     per process) from it, keeping JSON for target definitions only. Update SKILL.md Step 1.
  2. **Make it honest:** drop the assessment arg (accept 3→2 positional args), remove the
     unused `load_workbook` import, and reword SKILL.md tab 02 + the usage line. Confirm the
     paired `aspice-gap-analysis-checklist-reviewer` does not probe for the assessment arg
     before changing the interface.

**Severity:** med (functional-interface inconsistency; output itself is valid).

**Applied this run:** none — behavior/interface change with doc + paired-reviewer coupling
is out of scope for a same-run safe edit. Logged only.

## 2026-07-28 (autonomous POLISH)

**Selected because:** priority (1) — open issue [#45](https://github.com/jherrodthomas/automotive-skills-suite/issues/45)
carries the `skill-bug` label and names this builder's ignored-arg defect first. The
2026-07-02 entry logged the defect and deferred the fix pending a check of the paired
reviewer; that check is done (see below), so the fix shipped this run.

**Pre-check — paired reviewer coupling (the blocker from 07-02):**
`aspice-gap-analysis-checklist-reviewer` consumes only the *produced* workbook
(`aspice_gap_probe.py <gap.xlsx>`, `generate_checklist.py <gap.xlsx> <out.xlsx>`). Nothing
in the reviewer references the builder's CLI signature or the assessment argument, so the
interface change is uncoupled. Confirmed by grep over all reviewer scripts + SKILL.md.

**Applied this run — option 2 "make it honest", with a back-compat shim**
- `generate_gap_analysis()` signature reduced to `(input_json, output_xlsx)`; the inert
  `assessment_xlsx` parameter is gone.
- `main()` now accepts **2 args** as the documented form and still accepts the **legacy
  3-arg form**, dropping the leading workbook and printing a stderr WARNING that explains
  where current CLs actually come from. Existing call sites keep working; nobody is
  silently misled.
- Removed the unused `load_workbook` import (dead symptom of the never-read path).
- Tab 02 title changed from "Current State (from Assessment)" to
  "Current State (assessed CL, from input JSON)".
- SKILL.md: usage line updated to the 2-arg form with a note on the legacy form; Step 1
  reworded to say the assessment is transcribed into `processes[].current_cl` rather than
  read; output table row 02 reworded off "Read-only echo of assessment results".

**Smoke test**
| Invocation | Result |
|---|---|
| `generate_aspice_gap_analysis.py examples/sample_gap_analysis_input.json out.xlsx` | exit 0, `{"status":"ok","tabs":10,"processes":2}` |
| `... IGNORED.xlsx examples/sample_gap_analysis_input.json out.xlsx` (legacy) | exit 0, same JSON, WARNING on stderr |
| `... only_one.json` | exit 1, usage on stderr |
| re-zipped archive, unpacked fresh, regenerated | exit 0, 10 tabs, correct names/order |
| reviewer `aspice_gap_probe.py` on new output | exit 0, `current_state_rows: 2`, `target_cl_rows: 2`, `gap_rows: 2` — unchanged |

NUL-byte scan over all text files in the archive: clean. Archive re-zipped with `-X -D`
(no dir entries, no extra attrs) to match the original 7-entry layout.

**What's still open (not this run)**
- Tabs 06/07/08 (Effort Estimation, Quick Wins, Major Initiatives) are still built by
  zero-argument creators — header-only scaffolds with no input binding. Same class of
  defect as the improvement-plan/process-evidence "scaffold tabs" half of #45. Needs a
  decision: populate from input JSON (new schema keys) or document as intentional
  fill-in-by-hand templates. Deferred deliberately — it is a schema change across three
  skills and their example inputs.

**Severity:** was med → **resolved** for the ignored-arg half of #45. Scaffold-tab half of
#45 remains open across the other two ASPICE builders.
