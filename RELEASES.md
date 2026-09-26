# Automotive Skills Suite — Releases

Weekly snapshots of `github.com/jherrodthomas/automotive-skills-suite`. Tags are lightweight; the human clicks Publish on GitHub after reviewing this file.

---

## v2026.09.W39 — 2026-09-26

ISO week 39 (2026-09-21 → 2026-09-25). Weekly snapshot, 7 commits.

### Highlights

- **`cs-goals-builder`'s hard-coded `Cybersecurity_Property = "Confidentiality"`** (flagged as Known Issue in `[v2026.09.W38]`, opened as #62 Monday) is fixed: the property is now derived per row from the threat's STRIDE category via a new `_build_stride_index()`, with unmatched rows reporting `Not Determined` on stderr instead of silently defaulting. Verified across six scenarios including the negative case a hardcode can't fake — an Information-Disclosure-stripped input producing zero `Confidentiality` rows (#62, `4604f67`).
- **The suite-wide `_find_header_row` gate (#63) was measured down before it was fixed.** The issue's own proposed blanket `>= 2` threshold would have regressed two already-correct headers (`control-plan`, `ppap`), so the fix ships as "prefer ≥3, fall back to 2" instead, proven zero-diff across 2,616 checklist rows built from all 24 paired outputs before/after. Neither of the two symptoms the plan named turned out to move a verdict, so the issue closed HIGH → MED — but the same sweep surfaced two skills that are dead on arrival (`safety-case-builder`, `bus-load-analysis-checklist-reviewer`), left unfixed and tracked in Known issues.
- **A new column-level chain-contract audit (#64) caught what the tab-level one couldn't see, and immediately found 13 more instances.** `scripts/column_contract.py` extends the existing audit from tab-existence to column-name and data-start-row assertions, built by first watching it fail on `cs-concept-builder`'s known-bad `02_CS_Goals_Echo` edge (#65, 3 of 15 CS Goals silently dropped, every CAL echoing goal *text*) before fixing it. Run for real against the whole suite, it reports the entire TSC→software branch — `sw-arch-builder`, `sw-sr-builder`, `sw-fmea-builder` — has been running on misread or empty input for an unknown period while the tab-level audit reported every one of those edges MATCH.

### Changes this week

**plan**
- `ea692a7` auto(plan): W39 opens #62-#65, header-row HIGH resized to 24 latent 2 live

**polish**
- `4604f67` auto(polish): #62 cs-goals property derived from STRIDE, no longer constant Confidentiality
- `7796ade` auto(polish): journal and STATUS for the #62 STRIDE property fix
- `50ba884` auto(polish): #63 header gate now prefers 3 cells, falls back to 2; zero-diff proven
- `5dcce3d` auto(polish): #64 column-level chain audit, reproduces #65 and finds three more
- `6d0118f` auto(polish): #65 cs-concept reads CS Goals by header name, three dropped goals restored

**docs**
- `dcc45fb` auto(docs): W39 changelog rolled, 18 checklist-reviewer example stubs, STATUS regen

**release** _(this snapshot commit)_
- `STATUS.md` regenerated (76/76 paired, 5 fresh / 71 stale / 0 orphan)
- `RELEASES.md` appended with this W39 section
- `CHANGELOG.md` `[Unreleased]` rolled into a dated `[v2026.09.W39]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76, 2 via `docs/PAIRING_ALIASES.md`)
- Freshness: 5 🟢 · 71 🟡 · 0 🔴
- Domain spread: safety 15, quality 10, comms 8, cyber 6, v&v 5, program-mgmt 5, diagnostics 5, autosar 5, sysml 4, aspice 4, sotif 3, mbse 3, calibration 3
- Archives touched this snapshot window: 25 skill files (24 checklist-reviewer archives from #63's header-gate batch, plus `cs-goals-builder` from #62 and `cs-concept-builder` from #65 — several archives overlap both changes)

### Open issues at snapshot

**Unknown this run.** `api.github.com` returned `403` on every call this session — read, authenticated or not, against this repo or any other — with the same "not in this session's authorized repository set; use add_repo" body the sibling `robotics-skills-suite` task hit on its 2026-09-25 DOCS run. This is a session-level proxy restriction, not a repo-state fact, so no issue count is reported rather than guessing. See `docs/AUTONOMOUS_LOG.md` for today's entry and the human note below.

### Known issues carried into this tag

Six items are listed under **Known issues** in the `[v2026.09.W39]` `CHANGELOG.md` section and are not repeated here in full. The two a human should weigh first: three column-level BREAKs from #64 (`sw-arch-builder`, `sw-sr-builder`, `sw-fmea-builder`) are dynamically confirmed HIGH-severity defects not yet filed as issues; and `safety-case-builder` / `bus-load-analysis-checklist-reviewer` are both dead on arrival with mechanical, already-written fixes sitting in `docs/skill-polish-log/`.

### For the human

- **GitHub API access is blocked for this scheduled task's cloud-workspace session, and so is `git push` from that same workspace — this run's commits were made and pushed from the connected desktop instead (see journal).** This matches the `robotics-skills-suite` task's 2026-09-25 report and yesterday's automotive DOCS run exactly: read access over git-HTTPS works from the cloud workspace, but `api.github.com` and cloud-workspace `git push` both return 403 from an Anthropic-side proxy that scopes repositories per session. This is the second consecutive day this repo needed the device-side workaround; it will keep needing it until the session's authorized-repository set includes `jherrodthomas/automotive-skills-suite` for both the API and the push path.
- **Filing needed once the API is reachable:** the three #64 column-level BREAKs above, plus the four items still sitting in `docs/triage/2026-09-20.md` section 4 that W39's plan carried rather than filed.
- **Two tags may still be pushed and unpublished from before this run:** `v2026.09.W36` and `v2026.09.W38` (noted in the W39 plan). Review `RELEASES.md` and click Publish on whichever tags reached GitHub.

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.09.W38...v2026.09.W39

---

## v2026.09.W38 — 2026-09-19

ISO week 38 (2026-09-06 → 2026-09-18). Accumulating since `v2026.09.W36` (2026-09-05) — **two weeks in one tag, for the second release running**. No `v2026.09.W37` tag exists and none is backfilled: the W37 Saturday RELEASE was one of five scheduled runs that did not fire across the fortnight. 7 commits.

### Highlights

- **Four builder/reviewer pairs repaired, and every defect was the same shape: a documented input path that accepts analyst data and silently discards it.** `traceability-matrix` (input never reached 11 advertised tabs, reviewer certified the empty result), `hw-safety-reqs-builder` (`hw_sr_overrides` dropped entirely on a four-vs-three-segment HW-TSR ID drift, exit 0), `cs-goals-builder` (TARA columns resolved positionally, so every CSG shipped with the goal text in the Asset column and a risk integer as its goal text), `dia-checklist-reviewer` (three false findings from probe assumptions about layouts the builder does not emit). None raised an exception; all four had been shipping for months.
- **The verdict on tooling is harsher than the fix list.** `chain_contract_audit.py` reported 0 BREAK across all 16 chains for the entire time the `tara-builder` → `cs-goals-builder` payload was corrupt, because it asserts that a referenced *tab* exists and never that the columns line up. The week's own fixes are the argument for a column-level assertion — it is the single highest-leverage change available and would retro-catch this class suite-wide.
- **Five scheduled runs did not fire (09-09 Wed → 09-14 Mon).** W37 lost its Wed/Thu POLISH, Friday DOCS and Saturday RELEASE; W38 lost its Monday PLAN. Consequences carried into this snapshot: two W37 targets (#60 mbse wiring, #61 sheet-name confirmations) were opened, closed `completed` by the human on 09-11, and **never worked** — their defects are still in the archives. All three W38 POLISH days selected by rule (c), least-recently-touched, because there was no plan and no open issues.

### Changes this week

**triage**
- `a92088c` auto(triage): 12 issues reviewed, 5 stale commented, no low-confidence labels applied

**plan**
- `f95f4c9` auto(plan): W37 opens #59-#61, obligation hypothesis disproved, sysml batch deferred — the pre-slotting audit killed a hypothesis three previous plans had carried (the `Shall`/`Must` `REJECTED` gate is dead in 3 archives, not 76), collapsing a would-be batch target into a three-line add

**polish**
- `302660e` auto(polish): #59 traceability pair repaired, 11 tabs wired, empty workbook no longer passes
- `a8f430d` auto(polish): hw-safety-reqs overrides silently dropped on TSR ID drift, now applied and warned
- `a2af2f1` auto(polish): cs-goals-builder read TARA by header name, goal text and asset no longer swapped
- `9170271` auto(polish): dia reviewer misread joint reviews, scope and combined RACI cells

**docs**
- `54e46b3` auto(docs): W37+W38 changelog rolled, four example READMEs, five missed runs reconciled — four example READMEs written against the archives, and the first docs roll since W33 to find **no** check-count drift

**release** _(this snapshot commit)_
- `STATUS.md` regenerated (76/76 paired, 7 fresh / 69 stale / 0 orphan — `fmeda-builder` aged out of the 30-day window overnight)
- `RELEASES.md` appended with this W38 section
- `CHANGELOG.md` `[Unreleased]` rolled into a dated `[v2026.09.W38]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76, 2 via `docs/PAIRING_ALIASES.md`)
- Freshness: 7 🟢 · 69 🟡 · 0 🔴
- Domain spread: safety 15, quality 10, comms 8, cyber 6, autosar 5, diagnostics 5, program-mgmt 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, sotif 3
- Archives touched this snapshot window: 4 (`traceability-matrix-builder`, `traceability-matrix-checklist-reviewer`, `hw-safety-reqs-builder`, `cs-goals-builder`, `dia-checklist-reviewer` — 5 files across 4 pairs)

### Open issues at snapshot

**0 open.** The human closed all 15 on 2026-09-11 after six consecutive plans cited the queue. Two caveats for the reader: #60 and #61 were closed `completed` without ever being worked, and the four follow-ups raised in the `cs-goals-builder` and `dia-checklist-reviewer` polish logs were never filed because the queue tooling was not exercised this fortnight. An empty issue list here means *unfiled*, not *done*.

### Known issues carried into this tag

Six items are listed under **Known issues** in the `[v2026.09.W38]` `CHANGELOG.md` section and are not repeated here. The two structural ones worth a human's attention before the next plan: `_find_header_row` requires ≥3 populated cells, which makes every two-column tab in any builder invisible to its paired reviewer; and no regression harness runs builder output through the paired reviewer's probe, which is the exact shape of all four defects fixed this fortnight.

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.09.W36...v2026.09.W38

---

## v2026.09.W36 — 2026-09-05

ISO week 36 (2026-08-24 → 2026-09-05). Accumulating since `v2026.08.W34` (2026-08-22) — **two weeks in one tag**. The scheduled run died after 2026-08-27 and missed the W35 Friday DOCS roll and the W35 Saturday RELEASE, so no `v2026.08.W35` tag exists and none is backfilled here.

### Highlights

- **Seven reviewers that crashed on every input now run.** The single largest correctness fix in the repo's history, and it was one line repeated seven times. `sysml-block-diagram-checklist-reviewer` (W35 Thu, #56) passed a flat list where `dashboard.py:138` expected `{tab: [(check, result)]}`; the identical line sat in the other three sysml reviewers and, a week later, in all three mbse reviewers (W36 Thu, #58). Both domains went from **zero working reviewers to fully working** — sysml 0→4, mbse 0→3. Neither defect was findable by reading the archives; both surfaced only because the polish pass executed the reviewer against its own builder's output. That is now the strongest argument on the board for the proposed fifth invariant lint: *every reviewer's `generate_checklist.py` must run to completion on its builder's `{}` output.*
- **`sysml-block-diagram-builder` is the reference implementation for JSON input** (W36 Wed, #57). It takes `--input <model.json>`, the five hard-coded placeholder blocks are gone from the generator, the schema is documented in SKILL.md, and a brake-by-wire `sample_input.json` ships with it. The paired reviewer's `BDD-12` validates both connector ends instead of one. The W37 sysml batch (`activity`, `requirement`, `state-machine`) reuses these helpers. **Behaviour change** — see Known issues.
- **`autosar` closed out.** #54 stopped `autosar-bsw-config-builder` silently dropping `memory_layout` and `bus_interfaces`, which made the paired reviewer's `C005`/`C006` reachable for the first time; #55 restored the canonical 5,782-byte `recalc.py` and corrected the mis-generated `## Skills inventory` heading across the remaining five archives. Repo-wide the two mechanical invariants are now clean: `recalc.py` **152/152 at one hash**, bad heading **0/152**.
- **Two never-entered domains entered, and both were documented rather than rewritten.** `traceability-matrix` (v&v, #52) is the worst pair found to date — the builder ignores its input and emits five heading cells, and the reviewer certifies that empty workbook at 24/25 compliant because 22 of its 25 checks are a hard-coded `LC` fall-through. `mbse-system-context` (#58) reads its input and fills five tabs but leaves seven as single-cell placeholders. Both filed HIGH in the polish logs; neither repaired, because both repairs are authoring, not fixing. **Every one of the 13 domains has now had at least one polish pass.**
- **Check-count drift is now the repo's largest open honesty problem.** Four more reviewers measured this fortnight advertise 28 / 25+ / 30+ / 28+ checks and ship **15 / 6 / 8 / 6**. Added to the W33/W34 findings that is roughly **100 advertised checks that do not exist** across at least eight reviewers. Standing item 9 — author the missing checks, or downgrade the SKILL.md claims — is no longer a question about one file and now blocks honest documentation on eight.
- Inventory unchanged at 76 builder + 76 reviewer pairs, 100% paired. No skill added or removed this fortnight.

### Changes this snapshot

**feat**
- `72eefda` auto(polish): #57 sysml-block-diagram gets JSON input, placeholders out, BDD-12 symmetric

**fix**
- `84ea8b4` auto(polish): fix #54 bsw-config input drop, C005/C006 live, all mandatory FC
- `656bdfe` auto(polish): fix #55 autosar batch, recalc 152/152, bad heading 0/152
- `6e8cce6` auto(polish): fix #56 sysml probe crash, 4 reviewers repaired, domain gaps logged
- `da1082a` auto(polish): #58 mbse first pass, three crashing mbse reviewers fixed, stakeholder needs row resolved

**polish**
- `5660048` auto(polish): #52 traceability pair non-functional, reviewer passes empty workbook

**docs**
- `74d017c` auto(triage): twelve issues audited, stale rule misfires on two finished issues
- `6ed7fe5` auto(plan): W35 takes two autosar defects and opens sysml, defers v&v #52
- `30044b2` auto(plan): W36 slots deferred #52 first, opens sysml input and mbse first pass
- `357da3d` auto(monthly): KPI report for August 2026
- `b5fa14f` auto(docs): W35+W36 changelog rolled, four mbse/sysml reviewer stubs, drift logged

**release** _(this snapshot commit)_
- STATUS.md regenerated via `scripts/regen_status.py` (76/76 paired, 9 fresh / 67 stale / 0 orphan)
- RELEASES.md appended with this section
- CHANGELOG `[Unreleased]` rolled into `## [v2026.09.W36]`
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: 76
- Reviewers: 76
- Paired: 76/76 (100.0%, incl. 2 alias pairings per `docs/PAIRING_ALIASES.md`)
- Freshness: 🟢 9 touched ≤30d · 🟡 67 stale · 🔴 0 orphan
- Domain spread: safety=15, quality=10, comms=8, cyber=6, autosar=5, diagnostics=5, program-mgmt=5, v&v=5, aspice=4, sysml=4, calibration=3, mbse=3, sotif=3

_Freshness fell 10 🟢 → 9 🟢 overnight with no skill regressing, and the reason is a measurement artifact worth fixing: `regen_status.py` keys `Last Touched` on the **builder** file only. Seven reviewer archives were repaired this fortnight and not one of them moved a row. A `max(builder, reviewer)` change is one line; it is deferred because the STATUS table is a contract the Monday PLAN and Saturday RELEASE runs both read, and changing what a column means is not a Saturday job._

### Open issues at snapshot

12 open: #43, #44, #45, #46, #47, #48, #49, #50, #51, #52, #57, #58. **All twelve have met their definition of done.** No issue has been closed since #53 on 2026-08-19; the backlog has been purely decorative for three weeks and is actively corrupting the Monday PLAN priority rule, which ranks candidates by "skills referenced by open issues". A human close pass remains the single highest-leverage ten minutes available on this repo, and it is now the second consecutive tag saying so.

### Known issues shipped with this tag

- **Behaviour change:** `generate_sysml_block.py` with no `--input` emits an empty template with a stderr warning, not the old five placeholder blocks. Anything scripting the bare command should point at `examples/sysml-block-diagram-builder/sample_input.json`
- **Check-count drift, measured from `check_definitions.py` on 2026-09-04:** `sysml-block-diagram-checklist-reviewer` advertises 28 checks / 7 tabs, ships **15 / 3**; `mbse-system-context-checklist-reviewer` advertises "25+", ships **6**; `mbse-model-architecture-checklist-reviewer` advertises "30+", ships **8**; `mbse-requirements-allocation-checklist-reviewer` advertises "28+", ships **6**. Same class as `fmeda`, `autosar-bsw-config`, `cs-architecture` and `cdd`
- **`REJECTED` may be dead code suite-wide.** `dashboard.py` counts major issues as `NO and obligation == "Shall"` while the checks use `Must` / `Should`, so a `{}` workbook scoring 4 `NO` reports `CONDITIONAL APPROVAL`. Confirmed in the mbse reviewers; grep suggests the vocabulary split is wider. A repo-wide count across all 76 `dashboard.py` is queued and is one line per archive if confirmed
- **`traceability-matrix` pair is non-functional** as shipped (above). `test-case-catalog` (probes `Test Case Inventory`, builder emits `Test Cases`) and `flexray-config` (probes `Title`, builder emits `Title_Page`) each have a one-name sheet mismatch that may be a one-line fix — unconfirmed
- The 2026-09-01 chain scan found builder-to-**reviewer** breaks, which falsifies the premise on which `docs/chain-contract-audit.md` excludes those pairs. #46 should be re-scoped, not closed; that decision has been awaiting a human since 09-01

**Compare:** https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.08.W34...v2026.09.W36

---

## v2026.08.W34 — 2026-08-22

ISO week 34 (2026-08-17 → 2026-08-22). Accumulating since `v2026.08.W33` (2026-08-15).

### Highlights

- **The five-week carry finally landed, and it paid for itself inside 48 hours.** `#46` (repo-wide chain-contract audit) had been slotted last and displaced every week since W30. Monday descoped it to builder-to-builder sheet-name reads and slotted it *first*; it landed Tuesday, immediately found one silent BREAK in `fmeda-builder`'s TSC reader, and that break was fixed Wednesday. Repo chain breaks are now **zero**. The scheduling lesson — a target that loses every week is a target that is slotted wrong, not a target that is too big — is the most reusable thing in this tag.
- **First pass on `autosar`, the largest never-polished domain.** `autosar-bsw-config-builder` gained a real `examples/sample_input.json` (previously the skill's own definition-of-done was unsatisfiable — there was no sample to smoke-test from) and a working `recalc.py`. Two further defects were found and deliberately *not* fixed in the same pass; they went out as `#54` and `#55` rather than being absorbed into a refactor.
- **Check-count drift is now a repo-wide class, not four incidents.** Writing example stubs against the unpacked archives rather than the SKILL.md prose surfaced two more reviewers misstating their own check totals: `fmeda-checklist-reviewer` (claims 28, defines 36) and `autosar-bsw-config-checklist-reviewer` (claims "~30", defines 9 — off by more than 3×). With `cs-architecture` (42→43) and `cdd` that makes four confirmed. A scanner comparing every reviewer's advertised count against `len(CHECKS)` would find the rest in one pass; it is the leading PLAN candidate for W35.
- **W34 landed 3 of 4, not 4 of 4.** `#52` (`traceability-matrix-builder`, v&v) lost Thursday's slot to `#53`. That was correct triage, but v&v remains a never-polished domain and `#52` is a carried target, not a completed one. Recorded here verbatim so the tag does not round it up.
- Inventory unchanged at 76 builder + 76 reviewer pairs, 100% paired.

### Changes this week

**plan**
- `547ced0` auto(plan): W34 descopes #46 after five carries, opens autosar and v&v targets

**polish**
- `5fa7109` auto(polish): #46 chain-contract audit lands, finds silent fmeda-to-TSC break (#53)
- `ec8fc8e` auto(polish): fix #53 fmeda TSC reader, repo chain breaks now zero
- `15d4c8b` auto(polish): #51 autosar-bsw-config gains sample input, drops two silent bugs to issues

**docs**
- `dd687bd` auto(docs): W34 changelog roll, two reviewer stubs expose check-count drift, STATUS regen

**release** _(this snapshot commit)_
- STATUS.md regenerated via `scripts/regen_status.py` (76/76 paired, 10 fresh / 66 stale / 0 orphan)
- RELEASES.md appended with this section
- CHANGELOG `[Unreleased]` rolled into `## [v2026.08.W34]`
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: 76
- Reviewers: 76
- Paired: 76/76 (100.0%, incl. 2 alias pairings per `docs/PAIRING_ALIASES.md`)
- Freshness: 🟢 10 touched ≤30d · 🟡 66 stale · 🔴 0 orphan
- Domain spread: safety=15, quality=10, comms=8, cyber=6, autosar=5, diagnostics=5, program-mgmt=5, v&v=5, aspice=4, sysml=4, calibration=3, mbse=3, sotif=3

_Freshness moved 16 🟢 → 10 🟢 in a single day with no skill regressing. Six builders (`fsc`, `hara`, `pfmea`, `ppap-package`, `sw-fmea`, `tsc`) were all last touched on 2026-07-22 in one batch and crossed the 30-day line together. This is a window artifact, not a decline._

### Open issues at snapshot

12 open: #43, #44, #45, #46, #47, #48, #49, #50, #51, #52, #54, #55. **Ten of these have met their definition of done and remain open only because the autonomous run never closes issues.** Genuinely open work: `#52` (v&v polish, displaced from Thursday, takes W35's first slot), `#54` (`autosar-bsw-config` drops `memory_layout` and `bus_interfaces` silently; builder and reviewer must land in one commit) and `#55` (mis-generated template batch, 5 files remaining).

`#53` was closed by a human during the week — the first close in five weeks of a backlog that only grew. The other ten DoD-met issues are now actively distorting the Monday PLAN priority rule, which ranks by "skills referenced by open issues". A human close pass is the single highest-leverage ten minutes available on this repo.

### Known issues shipped with this tag

New this week — both need a `.skill` zip repack, i.e. POLISH-mode work:

- `fmeda-checklist-reviewer` — `SKILL.md` says "14 + 14 checks" and labels its Confirmation Review tab 14; `check_definitions.py` registers **18** `CR` entries, so the true total is **36** (18 CR + 14 FMEDAA + 4 VA), not 28
- `autosar-bsw-config-checklist-reviewer` — `SKILL.md` and the `check_definitions.py` docstring both advertise "~30 compliance checks"; the file defines **9** (`C001`–`C009`). An analyst reading "~30" reasonably assumes coverage this tool does not have, and two of the nine cannot fire against real builder output at all (`#54`)

Carried from `v2026.08.W33`, all still open, all requiring a repack: `cdd-checklist-reviewer` dangling `references/` pointers; `cs-architecture-checklist-reviewer` count 42→43 / 14→15 VA; the two interacting `sotif-analysis-checklist-reviewer` probe defects; and the 19 over-length sheet names in `docs/sheet-name-length-audit.md`.

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.08.W33...v2026.08.W34

---

## v2026.08.W33 — 2026-08-15

ISO week 33 (2026-08-10 → 2026-08-15). Accumulating since `v2026.08.W32` (2026-08-08).

### Highlights

- **The generator that writes STATUS.md is now version-controlled.** For weeks each run re-derived the pairing logic inline, so every fix to it evaporated overnight — Thursday's run duly reported `74 paired / 2 orphan`, contradicting `docs/PAIRING_ALIASES.md`. `scripts/regen_status.py` landed Friday and *parses* the alias table out of that doc rather than hard-coding it. Back to 76/76 paired, and it stays that way.
- **Three POLISH landings in three POLISH days**, second week running: `sotif-analysis-builder` (sheet names over Excel's 31-char limit — openpyxl warns and writes through, so shipped workbooks were malformed), `cs-architecture-builder` (chain reader rewritten against the tabs `cs-concept-builder` actually emits: 0/0/0 parsed before, 2/6/1 after), and `cs-concept-builder` (re-verified byte-clean).
- **A prior week's finding was retracted, not quietly dropped.** The "13 more corrupt archives" note from the NUL-byte work was a scanner false positive — zip members legitimately end in NUL via the EOCD record. An EOCD-aware rescan puts the true count at **0 corrupt archives out of 152**.
- **Domain labels corrected.** `msa-gage-rr-builder` and `spc-chart-builder` are Gage R&R and SPC — IATF 16949 quality tooling, not ISO 26262 safety. Nine builders matched no documented prefix rule and were hand-assigned each run; all nine are now pinned in the generator. This is why the domain spread below differs from W32's: it is a correction, not a migration.
- Inventory unchanged at 76 builder + 76 reviewer pairs, 100% paired.

### Changes this week

**plan**
- `fbcf48e` auto(plan): W33 carries three targets, opens cdd-builder for diagnostics, STATUS regen

**polish**
- `386191e` auto(polish): fix Excel-invalid SOTIF sheet names, restore cdd-builder sample fixture
- `b9c8aef` auto(polish): repair cs-concept to cs-architecture chain break per #43, STATUS regen
- `08cf363` auto(polish): #44 verified closed-loop, corrected scanner disproves wider archive corruption

**docs**
- `dc732bf` auto(docs): W33 changelog roll, three reviewer stubs, STATUS generator committed

**release** _(this snapshot commit)_
- STATUS.md regenerated via `scripts/regen_status.py` (76/76 paired, 15 fresh / 61 stale / 0 orphan)
- RELEASES.md appended with this section
- CHANGELOG `[Unreleased]` rolled into `## [v2026.08.W33]`
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: 76
- Reviewers: 76
- Paired: 76/76 (100.0%, incl. 2 alias pairings per `docs/PAIRING_ALIASES.md`)
- Freshness: 🟢 15 touched ≤30d · 🟡 61 stale · 🔴 0 orphan
- Domain spread: safety=15, quality=10, comms=8, cyber=6, autosar=5, diagnostics=5, program-mgmt=5, v&v=5, aspice=4, sysml=4, calibration=3, mbse=3, sotif=3

### Open issues at snapshot

8 open, all labeled `weekly-target`: #43, #44, #45, #46, #47, #48, #49, #50. **#43, #44, #45, #47 and #48 have met their definition of done and remain open only because the autonomous run never closes issues** — they are queued for a human click. Genuinely carrying into W34: #46 (repo-wide chain-contract audit, carried ×5 and never started), #49 (program-mgmt, DoD met W32 but unclosed), #50 (`cdd-builder` diagnostics polish, opened Monday, partial — sample fixture restored, reviewer-side dangling references still open).

### Known issues shipped with this tag

Four defects were found this week and deliberately left unfixed, because each needs a `.skill` zip repack (POLISH-mode work):

- `cdd-checklist-reviewer` — `SKILL.md` points at `references/methodology.md` and `references/cdd_checks.md`; neither exists in the archive
- `cs-architecture-checklist-reviewer` — advertises 42 checks / 14 verification checks; `check_definitions.py` defines 15 VA checks, so the real total is 43
- `sotif-analysis-checklist-reviewer` — insufficiency keyword probe never matches (count permanently 0) and the header row is counted as data; must be fixed together
- `docs/sheet-name-length-audit.md` — 19 over-length sheet names across 10 skills still unactioned; worst are `secure-coding-guidelines-builder` (37) and `8d-problem-solving-builder` (34 ×2)

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.08.W32...v2026.08.W33

---

## v2026.08.W32 — 2026-08-08

ISO week 32 (2026-08-03 → 2026-08-08). Accumulating since `v2026.08.W31` (2026-08-01).

### Highlights

- Three real polish landings in three POLISH days — the first week since W30 to hit that rate: `aspice-process-evidence-builder` (input keys now actually render), `a2l-builder` (comma-string `members` no longer counted as characters), and `safety-program-risk-register-builder` (docs corrected from 9 claimed tabs to the true 8).
- Two of the three closed out long-carried issues: #45 is now fully serviced (all three ASPICE thirds done) and #47's definition of done is met. Both are waiting on a human to click Close.
- First-ever pass on the **program-mgmt** domain (#49) — the domain-spread gap flagged in the W32 plan narrowed by one. `diagnostics`, `autosar`, `mbse`, `sysml` and `v&v` remain untouched since the May import.
- Inventory unchanged at 76 builder + 76 reviewer pairs, 100% paired.

### Changes this week

**plan**
- `fcc4c0b` auto(plan): W32 carries five open targets, no new issues, STATUS regen

**polish**
- `f00f1b2` auto(polish): aspice-process-evidence tabs 06/07/08 wired to real input data
- `6fab2ce` auto(polish): a2l-builder members normalization and conversion_methods schema doc fix
- `9b4660e` auto(polish): safety-program-risk-register docs made honest, dangling reference removed

**docs**
- `cd6a29e` auto(docs): W32 changelog roll, three example stubs, STATUS regen

**release** _(this snapshot commit)_
- STATUS.md regenerated (76/76 paired, 12 fresh / 64 stale / 0 orphan)
- RELEASES.md appended with this section
- CHANGELOG `[Unreleased]` rolled into `## [v2026.08.W32]`
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: 76
- Reviewers: 76
- Paired: 76/76 (100.0%, incl. 2 alias pairings per `docs/PAIRING_ALIASES.md`)
- Freshness: 🟢 12 touched ≤30d · 🟡 64 stale · 🔴 0 orphan
- Domain spread: safety=11, other=9, comms=8, cyber=6, quality=5, autosar=5, diagnostics=5, program-mgmt=5, v&v=5, aspice=4, sysml=4, calibration=3, mbse=3, sotif=3

### Open issues at snapshot

7 open, all labeled `weekly-target`: #43, #45, #46, #47, #48, #49 — plus #44. **#44, #45 and #47 have met their definition of done and are only open because the autonomous run never closes issues.** Carrying into W33: #43 (cs-concept → cs-architecture reader rewrite, carried x4), #46 (repo-wide chain-contract audit, carried x4), #48 (sotif first pass, carried x2).

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.08.W31...v2026.08.W32

---

## v2026.05.W20 — 2026-05-16

ISO week 20 (2026-05-11 → 2026-05-16). First weekly snapshot of the autonomous run cadence.

### Highlights

- Three builders moved from "shipped" to "reviewed against the polish playbook": `hara-builder`, `cs-concept-builder`, `aspice-assessment-builder`. Each now carries a dated entry in `docs/skill-polish-log/` with severity-rated findings.
- Weekly target file `docs/weekly/WEEK-2026-W20.md` opened the loop on Monday and the four GitHub issues it spawned are now mostly serviced; one (`8d-problem-solving-builder`) carries forward to W21.
- Suite still at 76 builder + 76 reviewer pairs, 100% paired (`item-definition-builder` ↔ `item-def-checklist-reviewer` and `ppap-package-builder` ↔ `ppap-checklist-reviewer` are alias pairs and now reflected correctly in STATUS).

### Changes this week

**plan**
- `16df7a5` auto(plan): W20 targets — hara, cs-concept, aspice-assessment, 8d

**polish**
- `5b6ad4e` auto(polish): regen STATUS.md and log W20 hara-builder polish findings
- `49fd9a9` auto(polish): regen STATUS.md and log W20 cs-concept-builder polish findings
- `c4fad8a` auto(polish): W20 #5 aspice-assessment-builder pass, regen STATUS.md

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (no flag changes vs. prior run)
- RELEASES.md created
- `docs/AUTONOMOUS_LOG.md` updated with RELEASE-mode entry

### Skills inventory

- Builders: 76
- Reviewers: 76
- Paired: 76/76 (100.0%)
- Domain spread: safety=12, quality=8, comms=8, program-mgmt=6, cyber=6, autosar=5, diagnostics=5, v&v=5, aspice=4, sysml=4, mbse=3, sotif=3, calibration=3, other=4

### Open issues at snapshot

- #6 W20 polish target: 8d-problem-solving-builder.skill _(carries to W21)_
- #5 W20 polish target: aspice-assessment-builder.skill _(serviced this week, awaiting close-out)_
- #4 W20 polish target: cs-concept-builder.skill _(serviced this week, awaiting close-out)_
- #3 W20 polish target: hara-builder.skill _(serviced this week, awaiting close-out)_
- #2 goodd _(needs human triage — non-conforming title, no domain signal)_

### Compare

[`3c69553...v2026.05.W20`](https://github.com/jherrodthomas/automotive-skills-suite/compare/3c69553...v2026.05.W20)

### Notes for the human

Click Publish on the v2026.05.W20 tag on GitHub once you've skimmed this section. Issue #2 (`goodd`) is the one item Sunday's TRIAGE pass should probably still escalate to you — autonomous run is intentionally not labeling or commenting it because confidence is well below 80%.

---

## v2026.05.W21 — 2026-05-23

ISO week 21 (2026-05-18 → 2026-05-23). Second weekly snapshot — W21 polish cycle closed; CHANGELOG and the first `examples/` doc stubs landed.

### Highlights

- W21 polish ran the full Tue/Wed/Thu cadence over `8d-problem-solving-builder`, `dbc-builder`, and `autosar-swc-builder`; the autosar-swc pass shipped an actual in-allowlist description fix, the other two produced severity-rated polish-log findings held for human review.
- `CHANGELOG.md` introduced and the first `examples/<skill>/README.md` stubs added — the repo now has a docs spine beyond STATUS.
- Suite steady at 76 builder + 76 reviewer pairs, 100% paired; no flag changes vs. W20.

### Changes this week

**plan**
- `3320c23` auto(plan): W21 targets — 8d carryover, dbc, autosar-swc, uds-services, classifier-freeze

**polish**
- `e8ff3b2` auto(polish): W21 #6 8d-problem-solving-builder pass, regen STATUS.md
- `76b2fff` auto(polish): W21 #7 dbc-builder pass, regen STATUS.md
- `387bbcd` auto(polish): W21 #8 autosar-swc-builder pass — description fix applied, STATUS regen

**docs**
- `1a5ca80` auto(docs): add CHANGELOG, W21 example README stubs, regen STATUS

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (no flag changes vs. prior run)
- RELEASES.md updated with the W21 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.05.W21]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76)
- Domain spread: safety 14, quality 8, comms 8, program-mgmt 6, cyber 6, autosar 5, diagnostics 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, sotif 3, other 2

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.05.W20...v2026.05.W21

### Open items for the human

- 10 issues open. Issue **#2** ("goodd", empty body) has stayed `needs-triage` across multiple runs — needs a human decision (likely close as spam/invalid).
- Issue **#11** ("packaging utility for Claude-compatible skill exports") is still unlabeled — Sunday TRIAGE should label it.
- W21 polish target **#9** (`uds-services-builder`) and tooling target **#10** (classifier freeze) were not serviced this week — both carry to W22.

---

## v2026.05.W22 — 2026-05-30

ISO week 22 (2026-05-25 → 2026-05-30). Third weekly snapshot — W22 polish cycle closed, alias map landed in the STATUS regen helper, RELEASE cadence now three weeks running.

### Highlights

- W22 polish ran the Tue/Wed/Thu cadence over `uds-services-builder`, `dfmea-builder`, and `hara-builder`; the uds-services pass shipped an in-allowlist description rewrite (DIDs, RIDs, SecurityAccess, NRC, P2/P2*/S3 timing, three session types, 0x10-0x86 service range, casual phrasings, sibling redirects) and finally cleared the W21-era classifier blind spot. The other two produced severity-rated polish-log entries held for human review.
- The reviewer-name alias map (`item-definition` ↔ `item-def`, `ppap-package` ↔ `ppap`) was promoted from inline override into the STATUS regen helper on Fri DOCS, so the 100% paired headline is now data-driven rather than hand-patched per run.
- Three new `examples/<skill>/README.md` stubs landed (uds-services, hara, dfmea) bringing the docs spine to seven seeded skills. CHANGELOG groups today's W22 work cleanly into Polish (3) and Docs (1 plan + 1 docs commit).
- Suite steady at 76 builder + 76 reviewer pairs, 100% paired; no flag changes vs. W21.

### Changes this week

**plan**
- `973c075` auto(plan): W22 targets — uds, hara, cs-concept, aspice-assessment, dfmea

**polish**
- `9850780` auto(polish): W22 #1 uds-services-builder pass, regen STATUS
- `04482aa` auto(polish): W22 #5 dfmea-builder pass, regen STATUS, journal
- `ef78172` auto(polish): W22 #2 hara-builder pass, regen STATUS, journal

**docs**
- `f9e63f9` auto(docs): W22 changelog roll-up, 3 example stubs, STATUS regen

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (no flag changes vs. prior run; 76/76 paired)
- RELEASES.md updated with the W22 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.05.W22]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76)
- Domain spread: safety 13, other 9, comms 8, cyber 6, autosar 5, diagnostics 5, quality 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, program-mgmt 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.05.W21...v2026.05.W22

### Open items for the human

- 10 issues open. The five W22-touched targets (#3 hara, #4 cs-concept, #5 aspice-assessment, #9 uds-services, #12 dfmea) now all carry W22 polish-log evidence — recommend a sweep to close the ones the human considers done.
- Issue **#10** (classifier freeze) is now 7+ runs old; this week's Fri DOCS pass got the alias map into the helper but the helper is still inline-Python in each commit. Mon W23 PLAN should allocate a tooling slot to extract `scripts/classify_skill.py`.
- Issue **#11** (skill packaging utility) and the W22 carryover targets (cs-concept, aspice-assessment, which only have W20-dated polish-log entries) are the natural W23 candidates if the human wants visible motion next week.

---

## v2026.06.W23 — 2026-06-06

ISO week 23 (2026-06-01 → 2026-06-06). Fourth weekly snapshot — first of June. Tag scheme ruling defaulted to ISO-absolute (`W23`, continuing the W20/W21/W22 series) after four unanswered flags; per-month spelling can be re-cut from the same SHA if a maintainer prefers.

### Highlights

- W23 polish cycle completed its three passes: `cs-concept-builder` (W20 findings re-confirmed), `tara-builder` (1 medium finding — Auto-rating Heuristics internal contradiction), and `fmeda-builder` (2 medium findings — Classification ladder unreachable branch; `SMvDU` non-standard acronym — plus a suspected 100× unit-convention discrepancy in the JSON example). **None of these were applied** — they are polish-log findings carried into the W24 maintainer backlog, not fixes in this snapshot.
- May 2026 monthly KPI report published (23 commits, 24 distinct skills touched, 3 weekly releases, 100% paired ratio; SOTIF flagged as the only zero-touch domain in May).
- Example-stub coverage rose from 7.9% (6/76) to 11.8% (9/76) with new stubs for cs-concept, tara, and fmeda.
- Suite steady at 76 builder + 76 reviewer pairs, 100% paired; canonical domain classifier (Tue 2026-06-02 explicit map) re-applied, spread stable at safety=15 / quality=10.

### Changes this week

**plan**
- `3af1f6b` auto(plan): W23 targets — cs-concept, aspice-assessment, classifier, fmeda, tara

**polish**
- `5b4b006` auto(polish): W23 #1 cs-concept-builder pass, regen STATUS, journal
- `22d6409` auto(polish): W23 #2 tara-builder pass, regen STATUS, journal
- `d6afa26` auto(polish): W23 #3 fmeda-builder pass, regen STATUS, journal

**docs**
- `f8e940f` auto(monthly): KPI report for May 2026
- `c21a84a` auto(docs): W23 changelog roll, 3 example stubs, STATUS regen

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (76/76 paired; canonical spread; no flag changes vs. Fri)
- RELEASES.md updated with the W23 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.06.W23]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76)
- Domain spread: safety 15, quality 10, comms 8, cyber 6, autosar 5, diagnostics 5, program-mgmt 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.05.W22...v2026.06.W23

### Open items for the human

- 12 issues open. The W20-era carryovers (#4 cs-concept, #5 aspice-assessment) have carried ready-to-apply rewrites in the polish log for 3+ weeks — recommend converting both to maintainer PRs in W24 PLAN rather than re-queuing as polish targets.
- The fmeda medium findings (Classification ladder unreachable branch; SMvDU acronym needing an ISO 26262-5 Annex B source-check; 100× `distribution_pct` unit suspicion) are the highest-leverage maintainer items from W23 — see `docs/skill-polish-log/fmeda-builder.md`.
- Issue **#10** (classifier extraction to `scripts/classify_skill.py`) is now 8 consecutive runs of hand-maintained inline Python — the explicit map grew again this week (`item-definition` → safety).
- Issue count dropped 13 → 12 between Thu and Fri without autonomous action; presumed human/spam-filter close of #17 — Sun TRIAGE will confirm.

## v2026.06.W25 — 2026-06-20

ISO week 25 (2026-06-15 → 2026-06-20). This snapshot consolidates two weeks of work: the **W24 Saturday release (2026-06-13) did not execute**, so everything committed since the last tag (`v2026.06.W23`, 2026-06-06) ships here — the W24 plan/triage/polish plus the W25 docs roll. Internal commit messages carry "W24" labels (a one-week drift between the human's week labels and ISO week numbers); the tag follows the established ISO-week-of-year convention.

### Highlights

- Three polish passes landed against `sotif-analysis-builder`, `safety-case-builder`, and `control-plan-builder`. Only `control-plan-builder` carried an embedded `.skill` fix (JSON example sample-count corrected 18 → 15 to match its 15 controlled characteristics); the other two are polish-log entries with no `.skill` edits.
- The W24 plan opened the loop on five targets (classifier extraction, sotif, safety-case, control-plan, comm-matrix); a triage pass typed #12 and confirmed the #17 delta. All issues have since been serviced or closed — the tracker is at **0 open** at snapshot.
- Suite holds at 76 builder + 76 reviewer pairs, 100% paired. No orphans, no new skills this period.

### Changes this week

**plan**
- `2623e14` auto(plan): W24 targets — classifier extract, sotif, safety-case, control-plan, comm-matrix

**polish**
- `a6df28d` auto(polish): W24 #20 sotif-analysis-builder review pass, regen STATUS, journal
- `2bd0c19` auto(polish): W24 #21 safety-case-builder review pass, regen STATUS, journal
- `54e2559` auto(polish): control-plan-builder pass, fix sample count 18->15, regen STATUS, journal

**triage**
- `d8b19ef` auto(triage): label refresh, #12 typed, #17 delta confirmed, STATUS regen

**docs**
- `6051a5d` auto(docs): backfill W24 changelog, add 2 example stubs, regen STATUS

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (76/76 paired; no flag changes vs. Fri — only the generated-on date advanced)
- RELEASES.md updated with this W25 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.06.W25]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76)
- Domain spread: safety 17, quality 10, comms 8, cyber 6, autosar 5, diagnostics 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, program-mgmt 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.06.W23...v2026.06.W25

### Open items for the human

- **Missed W24 release** — the 2026-06-13 Saturday run did not fire; W24 work is captured here rather than under its own tag. If a continuous tag history matters, a retroactive `v2026.06.W24` could be cut at `6051a5d`, but that is a manual call left to the maintainer.
- **Week-label drift** — commit messages and weekly docs use "W24" for work done in ISO week 25. Worth deciding whether to align the human labels to ISO weeks or document the offset, so future tags don't look like they skip a number (W23 → W25).
- **Issue #10** (classifier extraction to `scripts/classify_skill.py`) remains open conceptually — STATUS regen still relies on parsing the prior STATUS for the domain map rather than a committed classifier. No `feat:` work was scheduled this period.


## v2026.06.W26 — 2026-06-27

ISO week 26 (2026-06-22 → 2026-06-27). Saturday RELEASE run; W25 release fired last week, so this is a normal single-week snapshot with no backfill drift.

### Highlights

- A full W26 polish rotation landed: `5-why-builder`, `communication-matrix-builder`, and `aspice-assessment-builder` each took a review pass. Only `aspice-assessment-builder` carried an embedded `.skill` fix (capability-level rating rule corrected to ISO/IEC 33020); the other two are description/log touches.
- Week cadence is back in sync — commit labels, weekly docs, and the ISO week all read "W26" this period, closing the W23→W25 numbering drift called out in the W25 release notes.
- Suite holds at 76 builder + 76 reviewer pairs, 100% paired. No orphans and no new skills this period; the tracker is at **0 open** at snapshot.

### Changes this week

**plan**
- `e2162f8` auto(plan): W26 targets — 5-why, aspice-assessment, cs-concept, dia, comm-matrix

**polish**
- `107d490` auto(polish): 5-why-builder pass — add example stub, polish log, regen STATUS
- `9389a13` auto(polish): broaden communication-matrix-builder trigger, log, regen STATUS
- `fd66c47` auto(polish): fix aspice-assessment-builder CL rating rule to ISO/IEC 33020

**docs**
- `57dd9ba` auto(docs): W26 changelog roll, 2 example stubs, STATUS regen

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (76/76 paired; no flag changes vs. Fri — only the generated-on date advanced)
- RELEASES.md updated with this W26 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.06.W26]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76)
- Domain spread: safety 17, quality 10, comms 8, cyber 6, autosar 5, diagnostics 5, v&v 5, aspice 4, sysml 4, calibration 3, program-mgmt 3, mbse 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.06.W25...v2026.06.W26

## v2026.07.W27 — 2026-07-04

ISO week 27 (2026-06-29 → 2026-07-04). First release of July; normal single-week snapshot, cadence in sync (plan, polish ×3, monthly KPI, docs roll all landed on schedule).

### Highlights

- Full W27 polish rotation completed with three review passes: `apqp-plan-builder` (smoke-tested, clean), `item-definition-builder` (med finding: reviewer naming mismatch `item-def-checklist-reviewer` vs builder base — Option B alias-map recommended, needs human call), and `aspice-gap-analysis-builder` (med finding: assessment-xlsx argument accepted but ignored; two fix options logged, deferred as cross-file). No `.skill` edits this week — all findings logged for human decision.
- June 2026 monthly KPI report published mid-week (`docs/`), alongside the W27 weekly plan targeting odx, autosar-bsw-config, mbse-context, sysml-state, and traceability builders.
- Suite holds at 76 builder + 76 reviewer pairs, 100% paired, 0 orphans, tracker at **0 open** at snapshot.

### Changes this week

**plan**
- `8847b29` auto(plan): W27 targets — odx, autosar-bsw-config, mbse-context, sysml-state, traceability

**polish**
- `2df3374` auto(polish): apqp-plan-builder smoke-tested, polish log added, STATUS regen
- `01f38c5` auto(polish): item-definition-builder reviewed, naming-mismatch logged, STATUS regen
- `260c03f` auto(polish): aspice-gap-analysis-builder smoke-tested, ignored-arg finding logged, STATUS regen

**docs**
- `35be610` auto(monthly): KPI report for June 2026
- `19c4faa` auto(docs): W27 changelog roll, 3 example stubs, STATUS regen

**docs / release** _(this snapshot commit)_
- STATUS.md refreshed (76/76 paired, 3 fresh / 73 stale; generated-on date advanced to 2026-07-04)
- RELEASES.md updated with this W27 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.07.W27]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76)
- Domain spread: safety 17, quality 10, comms 8, cyber 6, autosar 5, diagnostics 5, v&v 5, aspice 4, sysml 4, calibration 3, program-mgmt 3, mbse 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.06.W26...v2026.07.W27

## v2026.07.W29 — 2026-07-18

ISO week 29 (2026-07-13 → 2026-07-18). **Two-week snapshot**: the W28 Sat RELEASE run (2026-07-11) never fired — no `v2026.07.W28` tag exists — so this release also carries the back-filled W28 work (see CHANGELOG note). Scheduler gap 2026-07-09 → 2026-07-14 flagged for human review.

### Highlights

- Three polish passes this week: `aspice-improvement-plan-builder` (ignored-arg chain-break logged — required `gap_analysis.xlsx` CLI arg never read), `aspice-process-evidence-builder` (clean input-consumption data point; scaffold-only tabs 06–08 logged), and `cs-architecture-builder` (smoke-tested clean, but a **high-severity silent chain-break** found upstream: cs-concept-builder's output tabs/headers don't match cs-architecture-builder's reader — a real concept workbook reads back zero CSRs). All findings logged; no `.skill` edits.
- Friday DOCS roll back-filled the missed W28 changelog entries (ppap/item-def polish, W28 plan, `docs/PAIRING_ALIASES.md` canonical alias registry) and added 4 example README stubs.
- Suite holds at 76 builder + 76 reviewer pairs, 100% paired (2 via alias registry), tracker at **0 open** at snapshot.

### Changes this week

**polish**
- `26ee19a` auto(polish): aspice-improvement-plan-builder ignored-arg chain-break logged, STATUS regen
- `696e912` auto(polish): aspice-process-evidence-builder scaffold-tab findings logged, args clean
- `8304e58` auto(polish): cs-architecture-builder verified; cs-concept chain-break found and logged

**docs**
- `78cfb27` auto(docs): W29 changelog roll with W28 back-fill, 4 example stubs, STATUS regen

**docs / release** _(this snapshot commit)_
- STATUS.md regenerated (76/76 paired, 4 fresh / 72 stale; ISO 26262 core builders dia/fmeda/fsc/hsi/item-definition reclassified `other` → `safety` per domain rules)
- RELEASES.md updated with this W29 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.07.W29]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76, 2 via docs/PAIRING_ALIASES.md)
- Domain spread: safety 15, comms 8, cyber 6, autosar 5, diagnostics 5, other 5, program-mgmt 5, quality 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.07.W27...v2026.07.W29

## v2026.07.W30 — 2026-07-25

ISO week 30 (2026-07-20 → 2026-07-25). Weekly snapshot, 5 commits.

### Highlights

- **NUL-corruption campaign**: the W30 plan flagged cs-concept-builder's generator carrying 3,361 trailing NUL bytes (#44, fixed Tue `691f614`); the same pass surfaced 13 more corrupt archives repo-wide, all cleaned in Wednesday's batch (`8a855cf`) — 9 generators compile again and prior xlsx false-positive findings were corrected.
- **a2l-builder repaired** (#47, Thu `661c4bb`): real TypeError crash in axis-points handling fixed (type-tolerant `len()` guard), frontmatter trigger strengthened, 13-tab output smoke-verified.
- Friday DOCS roll added 11 example README stubs — including the repo's first reviewer-side stubs (flagged for human confirmation). W30 targets #44 and #47 met; #43 (cs chain repair), #45 (ASPICE wiring), #46 (chain-contract audit) carry into W31.

### Changes this week

**plan**
- `a0c3d91` auto(plan): W30 targets — cs chain repair, NUL-strip, aspice bundle, audit, a2l

**polish**
- `691f614` auto(polish): cs-concept NUL-strip fixed per #44; 13 more corrupt archives found
- `8a855cf` auto(polish): batch NUL-strip 13 archives, 9 generators compile again, xlsx false-positives corrected
- `661c4bb` auto(polish): a2l-builder axis points crash fixed, trigger strengthened, 13 tabs verified

**docs**
- `f92275c` auto(docs): W30 changelog roll, 11 example stubs, STATUS regen

**docs / release** _(this snapshot commit)_
- STATUS.md regenerated (76/76 paired, 8 fresh / 68 stale; aspice-assessment-builder aged past the 30-day line)
- RELEASES.md updated with this W30 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.07.W30]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76, 2 via docs/PAIRING_ALIASES.md)
- Domain spread: safety 15, comms 8, cyber 6, other 5, quality 5, autosar 5, diagnostics 5, program-mgmt 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, sotif 3

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.07.W29...v2026.07.W30

---

## v2026.08.W31 — 2026-08-01

ISO week 31 (2026-07-27 → 2026-08-01). Weekly snapshot, 4 commits. First tag to cross a month boundary — the week opened in July and closes in August, so the tag carries the `2026.08` month prefix of its release date while retaining ISO week 31.

### Highlights

- **ASPICE ignored-arg class cleared in two of three builders** (#45): `aspice-gap-analysis-builder` (Tue `67c9072`) and `aspice-improvement-plan-builder` (Thu `299cdad`) each dropped a required-but-never-read CLI argument, with docs corrected to describe what the generator actually consumes. Both fixes are deliberately identical in shape so the ASPICE CLIs stay consistent with each other.
- **#45 cannot close yet.** The third leg, `aspice-process-evidence-builder`, has no ignored-arg defect — its input is genuinely consumed. Its only remaining finding is the scaffold-tab question (are Roadmap / Resources / Risks / KPIs / Communication / Pilot tabs input-driven or intentional fill-in templates?), which is a cross-builder schema decision first raised 2026-07-15 and still awaiting a human answer.
- **Thin week, honestly reported.** Wednesday 2026-07-29 produced no commit at all, breaking the always-commit invariant; the Friday DOCS run flagged it and the cause is still unknown. Two of the five W31 targets (#48 sotif, #49 program-mgmt — both first passes on never-polished domains) were never started, and #43 (the largest carried item) remains untouched for a second week.

### Changes this week

**plan**
- `57238bf` auto(plan): W31 targets — carry cs chain, aspice, audit; add sotif, program-mgmt

**polish**
- `67c9072` auto(polish): aspice-gap-analysis ignored assessment arg removed, docs made honest
- `299cdad` auto(polish): aspice-improvement-plan ignored gap-analysis arg removed, docs made honest

**docs**
- `e749617` auto(docs): W31 changelog roll, 2 reviewer example stubs, STATUS regen

**release** _(this snapshot commit)_
- STATUS.md regenerated (76/76 paired, 10 fresh / 66 stale / 0 orphan — unchanged from Friday apart from the header)
- RELEASES.md appended with this W31 section
- CHANGELOG.md `[Unreleased]` rolled into a dated `[v2026.08.W31]` section
- `docs/AUTONOMOUS_LOG.md` updated with the RELEASE-mode entry

### Skills inventory

- Builders: **76** · Reviewers: **76** · Paired ratio: **100.0%** (76/76, 2 via docs/PAIRING_ALIASES.md)
- Freshness: 10 🟢 · 66 🟡 · 0 🔴
- Domain spread: safety 11, other 9, comms 8, cyber 6, autosar 5, diagnostics 5, program-mgmt 5, quality 5, v&v 5, aspice 4, sysml 4, calibration 3, mbse 3, sotif 3

### Open issues at snapshot

7 open — #43, #44, #45, #46, #47, #48, #49. #44 and #47 have met their definition of done and are waiting on a human to close them (the run never closes issues autonomously).

### Compare

https://github.com/jherrodthomas/automotive-skills-suite/compare/v2026.07.W30...v2026.08.W31
