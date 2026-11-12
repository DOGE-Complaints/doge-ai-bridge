# STORY-AIBRIDGE-62 — Semantic state store + invalidation

## Meta
- **Key:** `STORY-AIBRIDGE-62-semantic-state-store-invalidation`
- **Status:** **Done** · **Product Done** · pkg-000065 · P8 SHAs `e94eed4`/`19eb95b`/`c68aeca` · next **STORY-63** · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-62-semantic-state-store-invalidation/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [p7 reaudit](../../../analysis/p7-reaudit-STORY-AIBRIDGE-62-semantic-state-store-invalidation-20261102.md)
- **Parent REQ:** [`REQ-13`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) §§2,4.1,5 AC-01 · L13-3
- **Tech-arch:** [`req15-semantic-state-roles/01-semantic-state-store-invalidation.md`](../../../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [63](STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) · [64](STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-02T08:32:08Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Separate Postgres semantic store (≠ HistoryStore / ≠ `last_confirmed_state` as SSOT): phase, facts↔grounds, hypotheses, gaps, corrections (logical classes; DDL at implement — not invent SSOT beyond Open).
- Persist across turns; harness without GPT UI.
- Meaning change (arch D2): confirmed facts / corrections / (phase if rights) → `invalidate_send_permission` (L13-3 Target A).
- Until store wired end-to-end: Transition C EDIT path remains Present enforce.

## Out of scope
- Role registry/assembly (63); volume/parity docs (64); GPT-48 authoring; gateway redesign; invent hash format.

## Verified current state
- Semantic store Present: `src/aibridge/semantic_state/` · Postgres table `semantic_state` (migration `0002`).
- Target A: confirmed/correction/(phase+rights) → `invalidate_send_permission` without EDIT.
- Transition C: `apply_edit` Present.
- History Keep — utterance log; not semantic SSOT.

## Target / AC
- [x] AC-AIB-13-01: semantic fields persist across turns (fixture/harness).
- [x] L13-3 Target A: confirmed-meaning write → invalidate send without Telegram EDIT.
- [x] History remains utterance log; store separate.

## Code points
- `src/aibridge/semantic_state/` · `confirm.py:407–445` · `migrations/0002_semantic_state.sql` · runtime `09`

## Dependencies
- Soft: REQ-11 arch seam Present · tech-arch `01` Present
