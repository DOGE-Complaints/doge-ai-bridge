# Semantic state store + L13-3 invalidation (STORY-62 / REQ-13)

Thin runtime note. Arch SSOT: [`../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md`](../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md). Peer seam: [`05-l11-invalidation-seam.md`](./05-l11-invalidation-seam.md).

**Honesty:** store ≠ `HistoryStore` / ≠ `interview.last_confirmed_state` SSOT. No invent hash-format SSOT (opaque uuid record ids). OOS roles (63) / parity (64).

---

## 1) Module home

| Piece | Path |
|-------|------|
| Package | `src/aibridge/semantic_state/` |
| Memory harness | `MemorySemanticStateStore` |
| Postgres | `PostgresSemanticStateStore` · table `semantic_state` (migration `0002_semantic_state`) |
| Writes + Target A | `SemanticStateService` → `ConfirmationGuard.invalidate_send_permission` |

Logical classes: phase · confirmed facts↔grounds · hypotheses · gaps · corrections.

**AC-AIB-13-01:** fields persist across turns (harness: `MemorySemanticStateStore` / Postgres `semantic_state`).

---

## 2) Meaning → invalidate (Target A)

| Write | Invalidates send? |
|-------|-------------------|
| Confirmed fact upsert | **yes** (`reason=confirmed_fact`) |
| Correction add | **yes** (`reason=correction`) |
| Phase when `changes_role_rights=True` | **yes** (`reason=phase_rights_change`) |
| Hypothesis / gap alone | **no** |

Effect: call Present `invalidate_send_permission` **without** Telegram EDIT / FSM EDIT.

---

## 3) Transition C

Until product wires store end-to-end in channel path, `apply_edit` → invalidate remains Present (`confirm.py:441–445`). Target A path does not remove Transition C.

---

## 4) History orthogonality

`conversation_history` remains utterance log. Semantic grounds may cite utterance refs; store must not replace history with an opaque blob only.

---

## OOS

- STORY-63 roles/assembly · STORY-64 volume/parity · GPT-48 · invent hash format · new HTTP invalidate action
