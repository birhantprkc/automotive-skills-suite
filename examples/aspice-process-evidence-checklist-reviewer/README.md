# aspice-process-evidence-checklist-reviewer — example

**What this skill produces:** confirmation-measures checklist xlsx over an ASPICE Process Evidence Package — 14 substantive checks across 5 tabs covering process documentation, evidence inventory, work products, performance records, and document quality.
**Typical input shape:** a Process Evidence Package xlsx, normally the output of `aspice-process-evidence-builder`; best-effort on other evidence-package workbooks.
**Expected output:** `<name>_checklist.xlsx` with each check auto-filled FC / LC / PC / NO / NA where machine-verifiable, and `Pending` with a drafted finding where reviewer judgment is required. The source Package is never modified.
**Sample I/O:** `python scripts/generate_checklist.py process_evidence.xlsx output_checklist.xlsx` — a Package with tabs 06/07/08 populated from real input (post-`f00f1b2`) clears the performance-record and improvement-evidence checks that previously came back PC.
**Paired builder:** `aspice-process-evidence-builder`.
