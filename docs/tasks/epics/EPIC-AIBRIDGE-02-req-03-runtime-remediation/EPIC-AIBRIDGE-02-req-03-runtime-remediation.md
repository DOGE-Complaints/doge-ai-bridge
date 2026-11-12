# EPIC-AIBRIDGE-02 — REQ-03 runtime remediation

> **ID:** `EPIC-AIBRIDGE-02-req-03-runtime-remediation` · **Статус:** 🟡 In Progress (09–17 🟢 P8 · **queue exhausted** · 18 Deferred)  
> **Package:** [`backlog-stories/req-03-runtime-remediation/INDEX.md`](../../backlog-stories/req-03-runtime-remediation/INDEX.md)  
> **P1 materialize (story 09):** 2026-09-13T15:16:41Z · **P3 story 09 Done:** 2026-09-13T15:25:46Z  
> **P1 materialize (story 10):** 2026-09-13T15:40:24Z · **P3 story 10 Done:** 2026-09-13T15:46:08Z · `pkg-000008`  
> **P1 materialize (story 11):** 2026-09-13T15:55:55Z · **P3 story 11 Done:** 2026-09-13T16:03:23Z · `pkg-000009`  
> **P1 materialize (story 12):** 2026-09-13T16:15:49Z · **P3 story 12 Done:** 2026-09-13T16:22:32Z · **P6:** 2026-09-13T16:30:46Z · `pkg-000010`  
> **P1 materialize (story 13):** 2026-09-13T16:34:47Z · **P3 story 13 Done:** 2026-09-13T16:49:42Z · **P6:** 2026-09-13T16:58:55Z · `pkg-000011`  
> **P1 materialize (story 14):** 2026-09-13T17:03:24Z · **P3 story 14 Done:** 2026-09-13T17:14:26Z · **P6:** 2026-09-13T17:23:30Z · `pkg-000012`  
> **P1 materialize (story 15):** 2026-09-13T17:28:28Z · **P3 story 15 Done:** 2026-09-13T17:34:04Z · `pkg-000013`  
> **P1 materialize (story 16):** 2026-09-13T17:43:00Z · **P8 story 16 Done:** 2026-09-13T18:18:12Z · `pkg-000014`  
> **P1 materialize (story 17):** 2026-09-13T18:20:16Z · **P8 story 17 Done:** 2026-09-13T18:30:59Z · `pkg-000015` · **queue exhausted**  
> **Parent REQ:** [`REQ-03-RUNTIME-REMEDIATION-AGREED.md`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) v0.2.1  
> **Does not modify:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md)

## Назначение

Runtime remediation wave (Postgres SSOT → Responses adapter → coordinator → gates → ops/privacy/SPA tracker) по пакету **req-03-runtime-remediation**.

**Не** invent epic-level AC — AC живут в story-файлах (backlog / pipeline).

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 Done (P8 closed) | STORY-AIBRIDGE-09-postgres-ssot-migrations | [pipeline](stories/STORY-AIBRIDGE-09-postgres-ssot-migrations/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) |
| 🟢 Done (P3 · P6 CLOSED · P8 SHAs) | STORY-AIBRIDGE-10-responses-adapter-tools | [pipeline](stories/STORY-AIBRIDGE-10-responses-adapter-tools/STORY-AIBRIDGE-10-responses-adapter-tools.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md) |
| 🟢 Done (P3 · P6 CLOSED · P8 SHAs) | STORY-AIBRIDGE-11-coordinator-pause-resume-send | [pipeline](stories/STORY-AIBRIDGE-11-coordinator-pause-resume-send/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) |
| 🟢 Done (P3 · P6 CLOSED · next P7) | STORY-AIBRIDGE-12-readyz-env-dryrun-gate | [pipeline](stories/STORY-AIBRIDGE-12-readyz-env-dryrun-gate/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) |
| 🟢 Done (P3 · P6 CLOSED · next P7) | STORY-AIBRIDGE-13-wave1-asgi-e2e | [pipeline](stories/STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) |
| 🟢 Done (P3 · P6 CLOSED · next P7) | STORY-AIBRIDGE-14-p1-ops-schema-restart | [pipeline](stories/STORY-AIBRIDGE-14-p1-ops-schema-restart/STORY-AIBRIDGE-14-p1-ops-schema-restart.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md) |
| 🟢 Done (P8 · next STORY-16) | STORY-AIBRIDGE-15-n8n-telegram-gate | [pipeline](stories/STORY-AIBRIDGE-15-n8n-telegram-gate/STORY-AIBRIDGE-15-n8n-telegram-gate.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md) |
| 🟢 Done (P3 · P6 CLOSED · P8 SHAs) | STORY-AIBRIDGE-16-privacy-retention | [pipeline](stories/STORY-AIBRIDGE-16-privacy-retention/STORY-AIBRIDGE-16-privacy-retention.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md) |
| 🟢 Done (P8 · queue exhausted) | STORY-AIBRIDGE-17-spa-https-continuation-e2e | [pipeline](stories/STORY-AIBRIDGE-17-spa-https-continuation-e2e/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) · [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) |
| ⏸ Deferred | STORY-AIBRIDGE-18-p2-replicas-observability | [backlog](../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-18-p2-replicas-observability.md) |

## Порядок

`09 → 10 → 11 ∥ 12 → 13 → 14 ∥ 15 → 16 → 17` · then Deferred `18`. Active wave: **story 17 P8 Done** · **queue exhausted** (Deferred 18 only).

## Non-goals этой волны

- Materialize / P3 для 15–17 without separate P1.3.
- Product runtime code в P1 (только task queue).
- Смешивание с `builder_project: gpt` / spa execution for 17 evidence.
