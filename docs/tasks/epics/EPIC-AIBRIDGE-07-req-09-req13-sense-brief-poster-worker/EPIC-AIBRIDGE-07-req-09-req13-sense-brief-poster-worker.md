# EPIC-AIBRIDGE-07 — REQ-09 / REQ13 sense brief + civic poster worker

> **ID:** `EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker` · **Статус:** 🟡 In Progress (**STORY-50** P6 Done · next **P7**)  
> **Package:** [`backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md`](../../backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md)  
> **P6 (story 50):** 2026-10-14T14:53:46Z · t09 Done · next **P7**  
> **P5 (story 50):** 2026-10-14T14:50:21Z · TASKED t09 · WAIVED G-02/G-03 · `run_mode=aibridge_50_audit_20261014`  
> **P3 (story 50):** 2026-10-14T14:40:44Z · gate PASS · `pkg-000053`  
> **P1.3 (story 50):** 2026-10-14T14:33:55Z · active `pkg-000053` · REUSE epic  
> **P5 (story 49):** 2026-10-14T14:25:21Z · TASKED=0 · WAIVED G-01…G-03 · next **P7** (skip P6) · activation **none**  
> **P3 (story 49):** 2026-10-14T14:13:53Z · gate PASS · `pkg-000052`  
> **P1.3 (story 49):** 2026-10-14T14:08:54Z · prior `pkg-000052` · REUSE epic  
> **P8 (story 48):** feat/test/docs closed · prior `pkg-000051`  
> **P5 (story 48):** 2026-10-14T14:00:18Z · TASKED=0 · WAIVED G-01…G-03 · activation none  
> **P3 (story 48):** 2026-10-14T13:50:18Z · gate PASS · `pkg-000051`  
> **P1.3 (story 48):** 2026-10-14T13:41:02Z · active `pkg-000051` · REUSE epic  
> **P8 (story 47):** feat/test/docs closed · prior `pkg-000050`  
> **P6 (story 47):** 2026-10-14T13:31:42Z · t08 Done · `run_mode=aibridge_47_audit_20261014`  
> **P5 (story 47):** 2026-10-14T13:28:15Z · TASKED t08 · WAIVED G-02/G-03  
> **P3 (story 47):** 2026-10-14T13:14:47Z · gate PASS · `pkg-000050`  
> **P1.3 (story 47):** 2026-10-14T12:46:03Z · active `pkg-000050` · REUSE epic  
> **P8 (story 46):** feat/test/docs closed · prior `pkg-000049`  
> **P6 (story 46):** 2026-10-14T12:33:45Z · t08–t09 Done  
> **Parent REQ:** [`REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md)  
> **Tech:** [`docs/architecture/sense-brief-poster-worker/`](../../../architecture/sense-brief-poster-worker/) (`00`–`03`)  
> **Does not modify:** EPIC-04 QA · EPIC-05 REQ-07 · EPIC-06 REQ-08/REQ9 ops bodies

## Назначение

REQ-09 / REQ13 Wave 2: worker accept entry, dedicated S2S, Issue+version idempotency, sense brief, civic poster + aibridge-owned storage, gateway bind-in, isolation harness. Build order `46 → 47 → 48 → 49 → 50`.

**Не** invent epic-level AC — AC живут в story-файлах (backlog / pipeline).  
**Не** invent exact HTTP path / env / JSON key SSOT while story marks Open.

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 P8 Done · pkg-000049 | STORY-AIBRIDGE-46-worker-entry-s2s-idempotency | [pipeline](stories/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) · [backlog](../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) |
| 🟢 P8 Done · pkg-000050 | STORY-AIBRIDGE-47-sense-brief-prompts-policy | [pipeline](stories/STORY-AIBRIDGE-47-sense-brief-prompts-policy/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) · [backlog](../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) |
| 🟢 P8 Done · pkg-000051 | STORY-AIBRIDGE-48-poster-storage-https-url | [pipeline](stories/STORY-AIBRIDGE-48-poster-storage-https-url/STORY-AIBRIDGE-48-poster-storage-https-url.md) · [backlog](../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md) |
| 🟡 P5 Done · next P7 · pkg-000052 | STORY-AIBRIDGE-49-gateway-bind-fail-version | [pipeline](stories/STORY-AIBRIDGE-49-gateway-bind-fail-version/STORY-AIBRIDGE-49-gateway-bind-fail-version.md) · [backlog](../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-49-gateway-bind-fail-version.md) |
| 🟡 P6 Done · next P7 · pkg-000053 | STORY-AIBRIDGE-50-worker-isolation-harness | [pipeline](stories/STORY-AIBRIDGE-50-worker-isolation-harness/STORY-AIBRIDGE-50-worker-isolation-harness.md) · [backlog](../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-50-worker-isolation-harness.md) |

## Порядок

`46 → 47 → 48 → 49 → 50`. Active wave: **STORY-50** (`pkg-000053`) — P6 Done · next **P7**.

## Non-goals этой волны (P1)

- Product runtime code в P1 (только task queue).
- Invent path/env/JSON/model / harness module-name SSOT.
