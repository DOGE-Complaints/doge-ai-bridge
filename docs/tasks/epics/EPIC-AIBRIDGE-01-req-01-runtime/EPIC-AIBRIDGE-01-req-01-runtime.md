# EPIC-AIBRIDGE-01 — REQ-01 doge-ai-bridge runtime (pilot)

> **ID:** `EPIC-AIBRIDGE-01-req-01-runtime` · **Статус:** 🟡 In Progress (01–06 🟢 Done P3; awaiting P4 on 06; 07–08 drafts)  
> **Package:** [`backlog-stories/req-01-runtime/INDEX.md`](../../backlog-stories/req-01-runtime/INDEX.md)  
> **P1 materialize:** 2026-09-12T20:30:51Z · **P3 story 01 Done:** 2026-09-12T20:35:41Z · **P1 story 02:** 2026-09-12T20:56:43Z · **P3 story 02 Done:** 2026-09-12T21:03:47Z · **P1 story 03:** 2026-09-12T21:16:48Z · **P3 story 03 Done:** 2026-09-12T21:23:18Z · **P1 story 04:** 2026-09-12T21:34:18Z · **P3 story 04 Done:** 2026-09-12T21:40:45Z · **P1 story 05:** 2026-09-12T21:50:08Z · **P3 story 05 Done:** 2026-09-12T21:54:48Z · **P1 story 06:** 2026-09-12T22:02:06Z · **P3 story 06 Done:** 2026-09-12T22:06:45Z  
> **Parent REQ:** [`REQ-01-doge-ai-bridge-runtime.md`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
> **Architecture:** [`docs/architecture/runtime/00-overview.md`](../../../architecture/runtime/00-overview.md)

## Назначение

Пилотный runtime `doge-ai-bridge` (Responses → Story Intake bridge) по пакету **req-01-runtime**: channel façade → content bundles → Responses loop → dual-confirm → gateway outcomes → ops/wave-1 proof.

**Не** изобретать epic-level AC здесь — AC живут в story-файлах (backlog / pipeline).

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 Done | STORY-AIBRIDGE-01-channel-facade-auth | [pipeline](stories/STORY-AIBRIDGE-01-channel-facade-auth/STORY-AIBRIDGE-01-channel-facade-auth.md) · [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md) |
| 🟢 Done | STORY-AIBRIDGE-02-content-bundle-registry | [pipeline](stories/STORY-AIBRIDGE-02-content-bundle-registry/STORY-AIBRIDGE-02-content-bundle-registry.md) · [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md) |
| 🟢 Done | STORY-AIBRIDGE-03-responses-tool-budgets | [pipeline](stories/STORY-AIBRIDGE-03-responses-tool-budgets/STORY-AIBRIDGE-03-responses-tool-budgets.md) · [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md) |
| 🟢 Done | STORY-AIBRIDGE-04-dual-confirm-tokens | [pipeline](stories/STORY-AIBRIDGE-04-dual-confirm-tokens/STORY-AIBRIDGE-04-dual-confirm-tokens.md) · [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md) |
| 🟢 Done | STORY-AIBRIDGE-05-gateway-outcomes | [pipeline](stories/STORY-AIBRIDGE-05-gateway-outcomes/STORY-AIBRIDGE-05-gateway-outcomes.md) · [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md) |
| 🟢 Done (P3 · next P4) | STORY-AIBRIDGE-06-ops-wave1-proof | [pipeline](stories/STORY-AIBRIDGE-06-ops-wave1-proof/STORY-AIBRIDGE-06-ops-wave1-proof.md) · [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md) |
| ⚪ Todo (backlog draft) | STORY-AIBRIDGE-07-replayable-history-postgres | [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-07-replayable-history-postgres.md) |
| ⚪ Todo (backlog draft) | STORY-AIBRIDGE-08-confirm-token-persistence | [backlog](../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-08-confirm-token-persistence.md) |

## Порядок

`01 → 02 → 03 → (07 optional) → 04 → (08 optional) → 05 → 06` (из package INDEX). Active wave: **story 06** (`pkg-000006`) — P3 Done; **next P4**.

## Non-goals этой волны

- Materialize / P3 для 07/08 without separate P1.3.
- Product runtime code в P1 (только task queue).
- Смешивание с `builder_project: gpt`.
