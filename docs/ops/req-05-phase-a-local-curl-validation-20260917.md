# REQ-05 Phase A — local curl validation (2026-09-17)

**Scope:** local operator process + Postgres via `.env` · **not** memory stores · **not** Railway  
**Plan:** local CURL Phase A + report  
**analysis.mdc:** only observed facts below

## Who started

- **Operator** started: `PORT=8080 python -m aibridge` (cwd `doge-ai-bridge`, `.venv`)
- **Agent** did not start/stop the process; after DB URL fix, agent only curled and wrote this report

## Env pins used (secrets redacted)

| Key | Value (observed) |
|-----|------------------|
| `DATABASE_URL` | `postgresql://postgres:***@localhost:5432/postgres` |
| `AIBRIDGE_ALLOW_MEMORY_STORES` | `false` |
| `DOGESTONIA_CONTENT_SOURCE_COMMIT` | `821a4d83e29b6453d1c7d86efc2a0dc438e04e39` |
| `DOGESTONIA_INSTRUCTIONS_DIR` | `src/instructions` |
| `DOGESTONIA_INSTRUCTIONS_MANIFEST` | `src/instructions/instructions.manifest.json` |
| `DOGESTONIA_OPENAPI_PATH` | `docs/openapi/story-intake-actions.openapi.yaml` |
| `DOGESTONIA_PAYLOAD_SCHEMA_PATH` | `src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json` |
| `DOGESTONIA_SCHEMA_ID` / `VERSION` | `uus_veerenni_civic` / `v3` |
| `AIBRIDGE_DRY_RUN` | `false` |

**Note:** earlier FAIL was `FATAL: database "aibridge"` / then `"public"` — `/public` is a **schema**, not a database. Correct dbname = `postgres` (tables already in schema `public`).

## Curl results (observed 2026-09-17)

Base: `http://127.0.0.1:8080`

| Endpoint | HTTP | Body | Verdict vs smoke |
|----------|------|------|------------------|
| `GET /healthz` | **200** | `{"status":"ok"}` | PASS (smoke §2) |
| `GET /readyz` | **200** | `{"status":"ready"}` | PASS (smoke §3 — no `content_bundle_not_ready`; full ready) |

## Fail-closed control

**Skipped** (operator single start; no second run with broken OAS / empty commit).

## Phase A content proof — local verdict

**PASS**

- Process up with complete Phase A pins
- `/healthz` 200
- `/readyz` 200 `ready` → content bundle / OAS / manifest / wiring not blocking

## Related

- Checklist marks: [`req-05-phase-a-smoke.md`](./req-05-phase-a-smoke.md) (local only; no Railway SUCCESS claim)
- Runbook: [`../runbooks/aibridge-web-service-local-railway.md`](../runbooks/aibridge-web-service-local-railway.md) §1.1b / §1.4
