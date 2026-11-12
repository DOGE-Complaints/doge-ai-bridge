# STORY-AIBRIDGE-09 — Postgres SSOT + migrations + concurrency

## Meta
- **Key:** `STORY-AIBRIDGE-09-postgres-ssot-migrations`
- **Status:** 🟢 Done (P3 gate PASS · awaiting P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md`
- **decision_ref:** [`STORY-AIBRIDGE-09-postgres-ssot-migrations.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §5 P0-05–08 · §5.3–5.4
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §5 P0-05–08 · §5.3–5.4
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [10](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md) · [11](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) · [12](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)
- **Supersedes:** [07](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-07-replayable-history-postgres.md) · [08](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-08-confirm-token-persistence.md)
- **Skill declared:** `postgres-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/postgres-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000007-20260913-epic-aibridge-02-story-09-postgres-ssot.yaml`
- **P3 Done:** 2026-09-13T15:25:46Z
**P1 materialize:** 2026-09-13T15:16:41Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| PG transactions / commit-before-HTTPS | REQ-03 [§5.3](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Concurrency vs replicas | REQ-03 [§5.4](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Transport replay terms | REQ-03 [§3](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) · AC #2 |
| Privacy tombstone (consume forever) | REQ-03 [§6.2](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) (full purge in 16) |

## Scope
- Versioned migrations as sole production schema mechanism (no boot-only `CREATE TABLE IF NOT EXISTS`).
- Unique `(channel, event_id)`, action token hash, `(session_id, call_id)`; at most one gateway attempt per authorized revision.
- Database-backed one active turn per session.
- Event dedupe + **stored HTTP status and response body** in PostgreSQL (replay after restart / instances).
- SessionStore / confirm / token / history repos on the runtime path (no silent memory fallback in production).
- Postgres row factory; disposable Postgres CI; transactional concurrency races (two concurrent messages/callbacks same session).

## Вне scope
- Live OpenAI HTTP client (10); ASGI coordinator wire (11); n8n; SPA; multi-replica load (18); optional token-hash UX.

## Verified current state (post-P3)
- Migrations + `pg_runtime` stores + disposable PG tests.
- pytest **109 passed, 1 skipped**.

## Verified current state (P1)
- In-process dedupe — `src/aibridge/dedupe.py` (`EventDedupeStore`).
- `ConfirmationGuard._sessions` in-process — `src/aibridge/confirm.py`.
- Boot `CREATE TABLE IF NOT EXISTS` — `src/aibridge/sessions.py`, `src/aibridge/registry.py`.
- History / tokens — `history.py`, `action_tokens.py` on disk.
- REQ-01 drafts 07/08 — **Superseded by this story**.

## Target / AC
- [x] Versioned migrations applied; boot schema-only path not production-acceptable.
- [x] Constraints above enforced; failed txn does not advance history/FSM.
- [x] Transport replay after restart returns previously stored HTTP status + body (REQ-03 AC #2).
- [x] Disposable Postgres integration + concurrency race tests pass (constraints win).
- [x] Production path has no silent memory fallback for dedupe/session/confirm/tokens/history.

## Точки в коде
- `src/aibridge/dedupe.py`, `sessions.py`, `registry.py`, `confirm.py`, `action_tokens.py`, `history.py`

## Dependencies
- Done STORY-AIBRIDGE-01…06. Blocks 10–13.

## Nested tasks (pkg-000007 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-09-t01-versioned-migrations-ssot](./task-aibridge-02-09-t01-versioned-migrations-ssot/README.md) | Scope #1; AC #1 | Done |
| t02 | [task-aibridge-02-09-t02-uniqueness-gateway-constraints](./task-aibridge-02-09-t02-uniqueness-gateway-constraints/README.md) | Scope #2; AC #2 | Done |
| t03 | [task-aibridge-02-09-t03-db-one-active-turn](./task-aibridge-02-09-t03-db-one-active-turn/README.md) | Scope #3; AC #2/#4 | Done |
| t04 | [task-aibridge-02-09-t04-transport-replay-store](./task-aibridge-02-09-t04-transport-replay-store/README.md) | Scope #4; AC #3 | Done |
| t05 | [task-aibridge-02-09-t05-prod-repos-no-memory-fallback](./task-aibridge-02-09-t05-prod-repos-no-memory-fallback/README.md) | Scope #5; AC #5 | Done |
| t06 | [task-aibridge-02-09-t06-pg-ci-concurrency-races](./task-aibridge-02-09-t06-pg-ci-concurrency-races/README.md) | Scope #6; AC #4 | Done |
| t07 | [task-aibridge-02-09-t07-story-acceptance-verification](./task-aibridge-02-09-t07-story-acceptance-verification/README.md) | AC #1–#5 gate | Done |
