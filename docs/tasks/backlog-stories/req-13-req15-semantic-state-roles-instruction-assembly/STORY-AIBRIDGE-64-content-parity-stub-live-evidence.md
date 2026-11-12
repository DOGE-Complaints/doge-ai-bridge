# STORY-AIBRIDGE-64 — Content volume/parity + stub/live evidence

## Meta
- **Key:** `STORY-AIBRIDGE-64-content-parity-stub-live-evidence`
- **Status:** **Done** · **Product Done** · pkg-000067 · P8 · AC-05 live **Explicit Partial** residual · queue exhausted · 2026-11-02 · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-64-content-parity-stub-live-evidence/STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) · [runtime 11](../../../runtime-docs/11-content-volume-parity-stub-live-evidence.md) · [package INDEX](INDEX.md)
- **Parent REQ:** [`REQ-13`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) AC-04/05/06 · L13-2 · arch D4/D6
- **Tech-arch:** [`req15-semantic-state-roles/03-content-volume-parity-verify.md`](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [62](STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [63](STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-02T08:32:08Z
- **Operator Q1:** Product Done for this story = **gate/docs + stub** scope; AC-05 live/parity = **Explicit Partial** until GPT-48 export Pass + ops window (etalon STORY-61).
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Document prod Railway volume path (ops may upload manually v1) — L13-2; baked `src/instructions/` = fixture/dev.
- Incomplete/mismatched content → readiness fail-closed (AC-06) — harness with broken fixture.
- Stub evidence matrix mapping 62/63 → AC-01/02/03/07/08 (+ AC-06 stub).
- Consume parity (AC-05): gate/docs Present; live Pass only with GPT-48 export + ops window; else Explicit Partial.
- Honesty in package INDEX: stub ≠ live/parity Done.

## Out of scope
- Authoring GPT-48 bodies; opening live window / mandatory export this wave; invent inventory hash SSOT format (joint Open).

## Verified current state
- Content fail-closed patterns Present (`content.py` / readiness content gates — cite at implement).
- GPT UI sync script: **not found** (T1).
- Arch D6 split gate locked.

## Target / AC
- [x] AC-AIB-13-04: prod volume path documented.
- [x] AC-AIB-13-06: incomplete/mismatch → fail-closed (fixture).
- [x] AC-AIB-13-05 stub/docs: parity gate described; live = **Explicit Partial** without GPT-48 export+window (Q1).
- [x] Package INDEX honesty note.

## Code points
- readiness/content gates · thin runtime-docs note (path at implement) · tests 62/63 cite

## Dependencies
- Soft: 63 · peer GPT UI REQ-48 for live AC-05 Pass
