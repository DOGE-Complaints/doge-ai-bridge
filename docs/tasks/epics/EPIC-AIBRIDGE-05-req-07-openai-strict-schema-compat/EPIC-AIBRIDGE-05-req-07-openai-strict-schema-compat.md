# EPIC-AIBRIDGE-05 — REQ-07 OpenAI strict-schema compatibility

> **ID:** `EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat` · **Статус:** 🟡 In Progress (**45** P5 Done · next **P7** · TASKED=0 · deferred_live)  
> **Package:** [`backlog-stories/req-07-openai-strict-schema-compat/INDEX.md`](../../backlog-stories/req-07-openai-strict-schema-compat/INDEX.md)  
> **P1.3 (story 41):** 2026-09-24T10:55:45Z · pkg-000040 (superseded)  
> **P8 (story 41):** projection Done  
> **P1.3 (story 42):** 2026-09-24T11:13:54Z · pkg-000041 (superseded)  
> **P8 (story 42):** uniqueItems Done  
> **P1.3 (story 43):** 2026-09-24T11:30:36Z · pkg-000042 (superseded)  
> **P8 (story 43):** VC bind Done  
> **P1.3 (story 44):** 2026-09-24T11:49:26Z · pkg-000043 (superseded)  
> **P3 (story 44):** 2026-09-24T11:52:39Z · gate PASS · **implemented, live verification pending**  
> **P1.3 (story 45):** 2026-09-24T12:07:46Z · active `pkg-000044`  
> **P3 (story 45):** 2026-09-24T12:11:06Z · gate PASS (`deferred_live`) · **no invent live TG**  
> **P5 (story 45):** 2026-09-24T12:17:21Z · WAIVED G-01…G-03 · TASKED=0 · next **P7** (skip P6)  
> **Parent REQ:** [`REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md)  
> **Tech:** [`TECH-ARCH-REQ-07-openai-strict-schema-compat.md`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md)  
> **Does not modify:** REQ-01/03/05 bodies · EPIC-04 QA package

## Назначение

REQ-07: OpenAI compatibility projection + canonical `uniqueItems` + minimal ValidationContext bind (stories 41–45). Build order `41 ∥ 42 → 43 → 44 → 45`.

**Не** invent epic-level AC — AC живут в story-файлах (backlog / pipeline).

## Stories

| Status | Key | Path |
|--------|-----|------|
| ✅ P8 Done · pkg-000040 | STORY-AIBRIDGE-41-openai-schema-projection | [pipeline](stories/STORY-AIBRIDGE-41-openai-schema-projection/STORY-AIBRIDGE-41-openai-schema-projection.md) · [backlog](../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md) |
| ✅ P8 Done · pkg-000041 | STORY-AIBRIDGE-42-canonical-uniqueitems-validation | [pipeline](stories/STORY-AIBRIDGE-42-canonical-uniqueitems-validation/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [backlog](../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) |
| ✅ P8 Done · pkg-000042 | STORY-AIBRIDGE-43-validation-context-bind-readyz | [pipeline](stories/STORY-AIBRIDGE-43-validation-context-bind-readyz/STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [backlog](../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-43-validation-context-bind-readyz.md) |
| ✅ P6 Done · pkg-000043 superseded | STORY-AIBRIDGE-44-compat-merge-gate-proof | [pipeline](stories/STORY-AIBRIDGE-44-compat-merge-gate-proof/STORY-AIBRIDGE-44-compat-merge-gate-proof.md) · [backlog](../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md) |
| ✅ P5 Done · next P7 · TASKED=0 · deferred_live · pkg-000044 | STORY-AIBRIDGE-45-compat-live-telegram-verify | [pipeline](stories/STORY-AIBRIDGE-45-compat-live-telegram-verify/STORY-AIBRIDGE-45-compat-live-telegram-verify.md) · [backlog](../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-45-compat-live-telegram-verify.md) |

## Порядок

`41 ∥ 42 → 43 → 44 → 45`. Active wave: **story 45** (`pkg-000044`) — P5 Done · next **P7** (skip P6) · AC-09 **deferred_live / BLOCKED** · focus **implemented, live verification pending**.

## Non-goals этой волны

- Product runtime code в P1 (только task queue).
- Rewrite pack JSON on disk; live Telegram invent; REQ-04 full hardening beyond minimal VC bind.
