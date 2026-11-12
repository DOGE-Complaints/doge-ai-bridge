# STORY-AIBRIDGE-07 — Replayable history in Postgres (bundle-pinned)

## Meta
- **Key:** `STORY-AIBRIDGE-07-replayable-history-postgres`
- **Status:** Superseded — work continues in [`STORY-AIBRIDGE-09-postgres-ssot-migrations`](../req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) (operator 2026-09-13; REQ-03)
- **Parent REQ:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §10 AIB-RSP (local replayable history)
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Origin:** P4 residual **G-01** on [STORY-AIBRIDGE-03](STORY-AIBRIDGE-03-responses-tool-budgets.md) — WAIVED `out-of-DoD` / `follow_up=new_story` (P5 2026-09-12T21:27:29Z)
- **Audit:** [`p4-audit-STORY-AIBRIDGE-03-responses-tool-budgets-20260912.md`](../../../analysis/p4-audit-STORY-AIBRIDGE-03-responses-tool-budgets-20260912.md)
- **Siblings:** [03](STORY-AIBRIDGE-03-responses-tool-budgets.md) · [02](STORY-AIBRIDGE-02-content-bundle-registry.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Responses history / store:false | REQ-01 [§10](../../../requirements/REQ-01-doge-ai-bridge-runtime.md); story 03 |
| Bundle-pinned sessions | [02-content-packaging.md](../../../architecture/runtime/02-content-packaging.md); story 02 `sessions.py` |
| In-process HistoryStore (current) | `src/aibridge/history.py` |

## Scope
- Persist replayable Responses items keyed by `session_id` (+ pinned `content_bundle_hash`) in Postgres/Sqlite session store (same adapters as story 02).
- Resume history across process restart / multi-instance-safe for pilot.
- Keep `store: false` on OpenAI; local store only.

## Вне scope
- Dual-confirm / gateway Send (04/05); inventing OpenAI `store:true`; full `/metrics` (06).

## Verified current state
- `HistoryStore` is in-process only (`history.py`).
- Session pin + Postgres/Sqlite adapters exist from story 02 / P6.

## Target / AC
- [ ] History survives process restart for a pinned session (Sqlite or Postgres).
- [ ] Items keyed by session + content_bundle_hash; resume uses pin.
- [ ] Unit/integration tests (mocked or `@pytest.mark.postgres` skip-friendly).
- [ ] No gateway side effect from history I/O failures (fail closed / resident-safe).

## Точки в коде
- `src/aibridge/history.py`, `sessions.py`, `interview.py`, `registry.py` (as needed)

## Dependencies
- [STORY-AIBRIDGE-03](STORY-AIBRIDGE-03-responses-tool-budgets.md) · [STORY-AIBRIDGE-02](STORY-AIBRIDGE-02-content-bundle-registry.md)

## Suggested order
After **03** Done; may run before or after **04** (operator choose at P1.3) — does not block dual-confirm AC.
