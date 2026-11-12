# STORY-AIBRIDGE-13 — Wave-1 ASGI E2E (fake/dry-run + Postgres)

## Meta
- **Key:** `STORY-AIBRIDGE-13-wave1-asgi-e2e`
- **Status:** 🟢 Done (P3 · P6 audit CLOSED · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`
- **decision_ref:** [`STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §2 · P0-12 · §4 AC (wave 1)
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §2 · P0-12 · §4 AC (wave 1)
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md)–[12](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) · [14](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md)
- **Active pkg (wave):** `pkg-000011-20260913-epic-aibridge-02-story-13-wave1-asgi-e2e.yaml`
- **P1 materialize:** 2026-09-13T16:34:47Z
- **P3 Done:** 2026-09-13T16:49:42Z
- **P6 Done:** 2026-09-13T16:58:55Z · `run_mode=aibridge_13_audit_20260913`

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Wave 1 AC | REQ-03 [§4](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) AC #1–#9 |
| P0-12 ASGI E2E | REQ-03 [§5](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) R3-P0-12 |
| Channel OpenAPI SSOT | [`docs/openapi/aibridge-channel-v1.openapi.yaml`](../../../../../openapi/aibridge-channel-v1.openapi.yaml) |
| Disposable PG | [`scripts/start-disposable-pg.sh`](../../../../../../scripts/start-disposable-pg.sh) |

## Scope
- Automated ASGI E2E with fake OpenAI + fake/dry-run gateway transports + real disposable Postgres.
- Prove REQ-03 §4 AC #1–#9 for wave 1 (no real `POST /story-drafts`).
- Transport replay returns stored HTTP status + body; every success/replay/non-2xx conforms to `docs/openapi/aibridge-channel-v1.openapi.yaml`.

## Вне scope
- Live Telegram/n8n (15); real gateway (after 14); SPA device E2E (17).

## Verified current state (post-P3 / P6)
- E2E suite: `tests/test_story_13_wave1_asgi_e2e.py` + harness `tests/story13_e2e_helpers.py` — fake OpenAI, fake/dry-run gateway, disposable Postgres.
- REQ-03 §4 AC #1–#9 covered for wave 1; zero real Dogestonia stash.
- **P6 G-01:** `PostgresEventDedupeStore.try_begin`/`complete`/`abort`/`wait_for_result` — ASGI claim-before-engine; concurrent same `event_id` → one Responses call (`tests/test_story_13_audit_gaps.py`).
- **P6 G-02:** OpenAPI error samples 401/409/500 against `ChannelErrorBody`.
- **P6 G-03:** ASGI+PG fail-closed Send (wrong owner 403, double consume 409); remaining §4 #5 facets stay story-11 unit coverage.

## Target / AC
- [x] E2E suite green without `"Received:"` replies.
- [x] AC #1–#9 demonstrated on fake/dry-run + Postgres (including restart replay where in-scope).
- [x] Zero real gateway stash in wave-1 proof.

## Точки в коде
- `tests/story13_e2e_helpers.py`, `tests/test_story_13_wave1_asgi_e2e.py`
- `src/aibridge/pg_runtime.py` (attempt-store commit)
- `scripts/start-disposable-pg.sh`, `docs/openapi/aibridge-channel-v1.openapi.yaml`

## Dependencies
- [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [10](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md) · [11](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) · [12](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)

## Nested tasks (pkg-000011 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-13-t01-asgi-e2e-harness-pg-fakes](./task-aibridge-02-13-t01-asgi-e2e-harness-pg-fakes/README.md) | Scope #1 harness | Done |
| t02 | [task-aibridge-02-13-t02-e2e-turns-replay-ac12](./task-aibridge-02-13-t02-e2e-turns-replay-ac12/README.md) | AC #1–#2; Target #1 | Done |
| t03 | [task-aibridge-02-13-t03-e2e-fc-interpretation-ac34](./task-aibridge-02-13-t03-e2e-fc-interpretation-ac34/README.md) | AC #3–#4 | Done |
| t04 | [task-aibridge-02-13-t04-e2e-send-dryrun-ac56](./task-aibridge-02-13-t04-e2e-send-dryrun-ac56/README.md) | AC #5–#6; Target #3 | Done |
| t05 | [task-aibridge-02-13-t05-e2e-restart-openapi-ac789](./task-aibridge-02-13-t05-e2e-restart-openapi-ac789/README.md) | AC #7–#9; Scope #3 | Done |
| t06 | [task-aibridge-02-13-t06-story-acceptance-verification](./task-aibridge-02-13-t06-story-acceptance-verification/README.md) | Target AC gate | Done |
| t07 | [task-aibridge-02-13-t07-audit-g01-pg-dedupe-try-begin](./task-aibridge-02-13-t07-audit-g01-pg-dedupe-try-begin/README.md) | P5 G-01 | Done |
| t08 | [task-aibridge-02-13-t08-audit-g02-openapi-non2xx-matrix](./task-aibridge-02-13-t08-audit-g02-openapi-non2xx-matrix/README.md) | P5 G-02 | Done |
| t09 | [task-aibridge-02-13-t09-audit-g03-send-failclosed-e2e](./task-aibridge-02-13-t09-audit-g03-send-failclosed-e2e/README.md) | P5 G-03 | Done |
