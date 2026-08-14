# cs-architecture-checklist-reviewer — example

**What this skill produces:** A TOMCO-style confirmation-review checklist xlsx over a CS (Cybersecurity) Architecture workbook — 7 tabs: Title, General Info, Guide, Summary (statistical roll-up + findings list), **Confirmation Review (14 `cr_*` generic doc-quality checks)**, **Functional Safety Assessment (14 `fsa_*` substantive checks** covering elements, crypto, key management, secure boot, communication and access control**)**, and **Verification Assessment (15 `va_*` checks** over verification and external artifacts**)**.

**Typical input shape:** A completed CS Architecture xlsx — optimal on `cs-architecture-builder` output, best-effort on others. `scripts/cs_arch_probe.py` reads Title-page metadata (title, doc ID, revision, author, approver, status), sets an `is_builder_format` flag from the sheet names, and counts `n_elements`, `n_crypto`, `n_key_mgmt`, `comm_channels` and `access_controls`.

**Expected output:** `<name>_checklist.xlsx` with each check rated FC / LC / PC / NO / NA, or `Pending` with a `(Reviewer to verify)` draft where judgment is required. The source CS Architecture is never modified; gaps land in Recommended Actions.

**Sample I/O:**

```bash
python scripts/generate_checklist.py cs_arch.xlsx output_checklist.xlsx
python scripts/recalc.py output_checklist.xlsx      # optional
```

The generator prints a JSON summary with FC/LC/PC/NO/NA/PENDING counts per tab, so auto-fill yield is visible immediately. Expect a high Pending count on the Verification Assessment tab — most VA checks point at a Verification Plan / Specification / Report that lives outside the workbook, so Pending is the correct rating there rather than a defect.

**Paired builder:** `cs-architecture-builder` — the `cs-concept` → `cs-architecture` reader chain was repaired 2026-08-12 (`b9c8aef`, issue #43).

> **Doc drift found 2026-08-14 (DOCS run, not yet fixed):** the reviewer's `SKILL.md` states "42 standard checklist requirements" in its frontmatter description and "14 verification checks" in both the description and the output-structure table. `scripts/check_definitions.py` actually defines **15** `va_*` checks, so the real total is **43**, not 42. Counted directly from the archive; the tab table and description are both one short. Left unfixed here deliberately — correcting frontmatter means repacking the `.skill` zip, which is a POLISH-mode change. Queued as a follow-up.
