# STORY-AIBRIDGE-62 — Semantic state store + invalidation

## Meta
- **Key:** `STORY-AIBRIDGE-62-semantic-state-store-invalidation`
- **Status:** **Done** · **Product Done** · pkg-000065 · P8 `e94eed4`/`19eb95b`/`c68aeca` · next **STORY-63** · REQ T1 Present · G-02 WAIVED ASGI residual
- **Parent Epic:** [`EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md`](../../EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md)
- **source:** `backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md`
- **decision_ref:** [`STORY-AIBRIDGE-62-….md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) · [`01-semantic-state-store-invalidation.md`](../../../../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md)
- **Package:** [`req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000065-20261102-epic-aibridge-11-story-62-semantic-state-store-invalidation.yaml`
- **P1 materialize:** 2026-11-02T08:41:40Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_62_scaffold_20261102T083726Z.plan.md)
- **Depends:** soft REQ-11 invalidate seam Present · tech-arch `01` Present
- **OOS:** STORY-63 roles · STORY-64 parity · invent hash/DDL SSOT · GPT-48

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Store + invalidation | [`01-semantic-state-store-invalidation.md`](../../../../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md) |
| Arch overview | [`00-overview.md`](../../../../architecture/req15-semantic-state-roles/00-overview.md) |
| Peer L11 seam | [`confirm.py:407+`](../../../../../src/aibridge/confirm.py) · REQ-11 arch |

## Scope
- Separate Postgres semantic store (≠ HistoryStore / ≠ `last_confirmed_state` as SSOT): phase, facts↔grounds, hypotheses, gaps, corrections (logical classes; DDL Open at implement).
- Persist across turns; harness without GPT UI.
- Meaning change (arch D2): confirmed facts / corrections / (phase if rights) → `invalidate_send_permission` (L13-3 Target A).
- Until store wired end-to-end: Transition C EDIT path remains Present enforce.

## Вне scope
- Role registry/assembly (63); volume/parity docs (64); GPT-48; gateway redesign; invent hash format.

## Verified current state (P3)
- Semantic store Present: `src/aibridge/semantic_state/` · Memory + Postgres (`semantic_state` table · migration `0002`).
- Invalidation: Target A via `SemanticStateService` → `invalidate_send_permission`; Transition C `apply_edit` Present.
- History Keep — utterance log orthogonal (not semantic SSOT).
- Runtime: [`docs/runtime-docs/09-semantic-state-store-invalidation.md`](../../../../runtime-docs/09-semantic-state-store-invalidation.md).
- Tests: `tests/test_story_62_semantic_state_store_invalidation.py`.

## Target / AC
- [x] AC-AIB-13-01: semantic fields persist across turns (fixture/harness).
- [x] L13-3 Target A: confirmed-meaning write → invalidate send without Telegram EDIT.
- [x] History remains utterance log; store separate.
- [x] Transition C EDIT enforce Present until store wired.

## Nested tasks (pkg-000065)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-62-t01-semantic-store-boundary-not-history](./task-aibridge-62-t01-semantic-store-boundary-not-history/README.md) | store ≠ History / ≠ last_confirmed_state | Done |
| t02 | [task-aibridge-62-t02-postgres-semantic-persist-logical-classes](./task-aibridge-62-t02-postgres-semantic-persist-logical-classes/README.md) | Postgres · logical classes · Open DDL | Done |
| t03 | [task-aibridge-62-t03-ac01-multi-turn-harness-no-gpt-ui](./task-aibridge-62-t03-ac01-multi-turn-harness-no-gpt-ui/README.md) | AC-AIB-13-01 | Done |
| t04 | [task-aibridge-62-t04-l13-3-target-a-meaning-invalidate](./task-aibridge-62-t04-l13-3-target-a-meaning-invalidate/README.md) | L13-3 Target A · D2 | Done |
| t05 | [task-aibridge-62-t05-transition-c-edit-enforce-until-wired](./task-aibridge-62-t05-transition-c-edit-enforce-until-wired/README.md) | Transition C | Done |
| t06 | [task-aibridge-62-t06-history-utterance-log-orthogonality](./task-aibridge-62-t06-history-utterance-log-orthogonality/README.md) | History utterance log | Done |
| t08 | [task-aibridge-62-t08-story-gate-checklist](./task-aibridge-62-t08-story-gate-checklist/README.md) | package gate | **PASS** |
| t09 | [task-aibridge-62-t09-audit-g01-req13-t1-verified-state-sync](./task-aibridge-62-t09-audit-g01-req13-t1-verified-state-sync/README.md) | P4 G-01 · REQ T1 hygiene | Done |

## Code points
- `src/aibridge/semantic_state/` · `confirm.py:407–445` · `migrations/0002_semantic_state.sql`
