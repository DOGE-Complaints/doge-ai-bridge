# STORY-AIBRIDGE-16 — Privacy retention enforcement

## Meta
- **Key:** `STORY-AIBRIDGE-16-privacy-retention`
- **Status:** 🟢 Done (P8 · next STORY-17)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md`
- **decision_ref:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6.2 R3-P1-10 · [`privacy-pilot.md`](../../../../../runbooks/privacy-pilot.md)
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6.2 R3-P1-10
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [14](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Operator decision:** session-delete = **ops-only**, authenticated, authorized, fail-closed, audit-logged. **HTTP path Unknown** — do **not** invent channel OpenAPI fields.
- **Active pkg (wave):** `pkg-000014-20260913-epic-aibridge-02-story-16-privacy-retention.yaml`
- **P1 materialize:** 2026-09-13T17:43:00Z
- **P3 Done:** 2026-09-13T17:49:14Z
- **P6 Done:** 2026-09-13T17:55:59Z · `run_mode=aibridge_16_audit_20260913` · G-01/G-02/G-03 CLOSED
- **P8 Done:** 2026-09-13T18:18:12Z · feat `d2c27b7` · test `3e55b9c` · docs `bb471a4` · **no push**

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| R3-P1-10 privacy retention | REQ-03 [§6.2](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Privacy pilot runbook | [`privacy-pilot.md`](../../../../../runbooks/privacy-pilot.md) |
| Arch TTL note (604800) | [`00-overview.md`](../../../../../architecture/runtime/00-overview.md) |
| Settings TTL knobs | `src/aibridge/config.py` |
| Ops delete (no OAS invent) | `src/aibridge/ops_session_delete.py` · `privacy_retention.py` |
| Channel OpenAPI SSOT | [`aibridge-channel-v1.openapi.yaml`](../../../../../openapi/aibridge-channel-v1.openapi.yaml) |

## Scope
- Session/narrative/Responses-item TTL = configured; pilot default **604800** s; slides only on legitimate activity.
- Expired narrative deleted or irreversibly minimized; expired action tokens purged per audit policy.
- Operator session-delete mechanism (ops-only) tested; covers history, pending intents, action tokens.
- Deletion/expiry must **never** make an already consumed action token usable.
- Minimized non-PII replay tombstone may be retained for security/audit window.
- Redacted audit metadata may follow separate retention; n8n execution retention verified separately before residents.

## Вне scope
- Changing channel OpenAPI for delete (forbidden without operator decision).
- Inventing delete URL/method before path is agreed.

## Verified current state (post-P3 · post-P6 audit)
- `DEFAULT_SESSION_TTL_SECONDS = 604800`; `.env.example` aligned; `SessionActivityClock` slides on `get_or_create_session`.
- `minimize_narrative` → privacy tombstone; `purge_expired_pending_tokens` keeps CONSUMED unusable.
- Ops delete: `AIBRIDGE_OPS_BEARER_TOKEN` + `python -m aibridge.ops_session_delete` — fail-closed; requires Postgres `DATABASE_URL` after authz; **no** channel OAS path.
- G-01: `expire_idle` + durable confirm `updated_at` TTL wired on ASGI/guard.
- G-02: ops CLI uses PG history/engine (not empty `HistoryStore`).
- G-03: `privacy-pilot.md` residual ops-before-residents notes.
- Tests: `tests/test_story_16_privacy_retention.py` · `tests/test_story_16_audit_gaps.py` · pytest **181 passed / 39 skipped**.

## Target / AC
- [x] §6.2 bullets proven with tests and/or ops evidence.
- [x] Consumed token remains non-usable after delete/expiry (tombstone OK).
- [x] Delete surface documented as ops-only once path is decided — fail-closed until then.

## Точки в коде
- `src/aibridge/privacy_retention.py`, `ops_session_delete.py`, `config.py`, `sessions.py`, `confirm.py`, `app.py`
- `docs/runbooks/privacy-pilot.md`
- `tests/test_story_16_privacy_retention.py`

## Dependencies
- [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [14](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md)

## Nested tasks (pkg-000014 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-16-t01-ttl-default-sliding-activity](./task-aibridge-02-16-t01-ttl-default-sliding-activity/README.md) | Scope #1 | Done |
| t02 | [task-aibridge-02-16-t02-expired-narrative-minimize](./task-aibridge-02-16-t02-expired-narrative-minimize/README.md) | Scope #2 narrative | Done |
| t03 | [task-aibridge-02-16-t03-token-purge-consumed-invariant](./task-aibridge-02-16-t03-token-purge-consumed-invariant/README.md) | Scope #2 tokens · #4 · Target #2 | Done |
| t04 | [task-aibridge-02-16-t04-ops-session-delete-failclosed](./task-aibridge-02-16-t04-ops-session-delete-failclosed/README.md) | Scope #3 · Target #3 | Done |
| t05 | [task-aibridge-02-16-t05-tombstone-audit-n8n-retention](./task-aibridge-02-16-t05-tombstone-audit-n8n-retention/README.md) | Scope #5–#6 | Done |
| t06 | [task-aibridge-02-16-t06-story-acceptance-verification](./task-aibridge-02-16-t06-story-acceptance-verification/README.md) | Target AC gate | Done |
| t07 | [task-aibridge-02-16-t07-audit-g01-wire-expire-idle](./task-aibridge-02-16-t07-audit-g01-wire-expire-idle/README.md) | P5 G-01 | Done |
| t08 | [task-aibridge-02-16-t08-audit-g02-ops-cli-pg-wire](./task-aibridge-02-16-t08-audit-g02-ops-cli-pg-wire/README.md) | P5 G-02 | Done |
| t09 | [task-aibridge-02-16-t09-audit-g03-privacy-pilot-residual](./task-aibridge-02-16-t09-audit-g03-privacy-pilot-residual/README.md) | P5 G-03 | Done |
