# STORY-AIBRIDGE-08 — Confirm FSM + action-token persistence

## Meta
- **Key:** `STORY-AIBRIDGE-08-confirm-token-persistence`
- **Status:** Superseded — work continues in [`STORY-AIBRIDGE-09-postgres-ssot-migrations`](../req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) (operator 2026-09-13; REQ-03)
- **Parent REQ:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §13 dual-confirm / AIB-CONF
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Origin:** P4 residual **G-01** on [STORY-AIBRIDGE-04](STORY-AIBRIDGE-04-dual-confirm-tokens.md) — WAIVED `out-of-DoD` / `follow_up=new_story` (P5 2026-09-12T21:45:18Z)
- **Audit:** [`p4-audit-STORY-AIBRIDGE-04-dual-confirm-tokens-20260912.md`](../../../analysis/p4-audit-STORY-AIBRIDGE-04-dual-confirm-tokens-20260912.md)
- **Siblings:** [04](STORY-AIBRIDGE-04-dual-confirm-tokens.md) · [02](STORY-AIBRIDGE-02-content-bundle-registry.md) · [07](STORY-AIBRIDGE-07-replayable-history-postgres.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Dual-confirm FSM + tokens | REQ-01 [§13](../../../requirements/REQ-01-doge-ai-bridge-runtime.md); [03-confirm-gateway.md](../../../architecture/runtime/03-confirm-gateway.md) |
| In-process store (current) | `src/aibridge/action_tokens.py`, `confirm.py` |
| Session adapters | story 02 `sessions.py` / Postgres+Sqlite |

## Scope
- Persist action-token **hashes** (never raw) + confirm session/revision/FSM state across process restart.
- Multi-instance-safe for pilot (shared store with story-02 adapters where practical).
- Resume pending confirm after reopen; invalidate/TTL semantics preserved.

## Вне scope
- Live gateway HTTP (05); inventing new AC for story 04; SPA E2E; history Postgres (07).

## Verified current state
- `ActionTokenStore` and `ConfirmationGuard._sessions` are in-process only (story 04 AC PASS).
- Comment in `action_tokens.py`: «Postgres persistence later».

## Target / AC
- [ ] Token hashes + session/revision/state survive process restart (Sqlite or Postgres).
- [ ] Multi-instance consumers share the same pending token/session view.
- [ ] Unit/integration tests (reopen / skip-friendly Postgres).
- [ ] Fail closed on store errors (no silent Send authorize).

## Точки в коде
- `src/aibridge/action_tokens.py`, `confirm.py`, `sessions.py` (as needed)

## Depends
- Prefer after or alongside [STORY-AIBRIDGE-07](STORY-AIBRIDGE-07-replayable-history-postgres.md) adapter patterns; blocks multi-instance pilot hardening before scale-out.
