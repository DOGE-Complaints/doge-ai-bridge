# req-07-openai-strict-schema-compat — INDEX

> **Пакет:** REQ-07 — OpenAI strict-schema compatibility projection + canonical `uniqueItems`  
> **Parent REQ:** [`REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) (file stem REQ-07; H1 may still say REQ-06 — Open Unknown)  
> **Tech-arch:** [`../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md)  
> **Interview:** [`../../../analysis/zeya888.target-tech-arch-interview-REQ-07-openai-strict-schema-compat-2026-09-24.md`](../../../analysis/zeya888.target-tech-arch-interview-REQ-07-openai-strict-schema-compat-2026-09-24.md)  
> **Related seams (Implemented, not this AC):** [`../req-05-content-phase-a-flat-launch/INDEX.md`](../req-05-content-phase-a-flat-launch/INDEX.md) STORY-19…22  
> **Emitted:** 2026-09-24T10:28:49Z · materialize from REQ→backlog plan (operator «запиши»)  
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)  
> **P1.3 note (2026-09-24T10:55:45Z):** story 41 pipeline materialized · **NEW EPIC-05** · active `pkg-000040`  
> **P3 note (2026-09-24T11:17:36Z):** STORY-42 Gate 2 uniqueItems Done · gate PASS · next **P4** · [p3](../../run-reports/run-summary-20260924-1117-story-aibridge-42-p3.md)  
> **P3 note (2026-09-24T11:52:39Z):** STORY-44 merge-gate Done · gate PASS · next **P4** · **implemented, live verification pending** · [p3](../../run-reports/run-summary-20260924-1152-story-aibridge-44-p3.md)  
> **P1.3 note (2026-09-24T12:07:46Z):** STORY-45 pipeline materialized · active `pkg-000044` · next **P2** · **no invent live TG SUCCESS**  
> **P3 note (2026-09-24T12:11:06Z):** STORY-45 P3 Done · gate PASS (`deferred_live` / BLOCKED AC-09) · [p3](../../run-reports/run-summary-20260924-1211-story-aibridge-45-p3.md) · [BLOCKED](../../ops/req-07-ac09-live-evidence-BLOCKED-20260924.md)  
> **P5 note (2026-09-24T12:17:21Z):** STORY-45 P5 Done · WAIVED G-01…G-03 · TASKED=0 · next **P7** (skip P6) · [p5](../../run-reports/run-summary-20260924-1217-story-aibridge-45-p5-disposition.md)  
> **Two-stage DoD:** merge gate = stories 41–44 → status **implemented, live verification pending**; production verified only after **45** AC-09 **live PASS** (still pending)

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| P8 Done · pkg-000040 | STORY-AIBRIDGE-41-openai-schema-projection | [OpenAI schema compatibility projection](STORY-AIBRIDGE-41-openai-schema-projection.md) · [pipeline](../../epics/EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat/stories/STORY-AIBRIDGE-41-openai-schema-projection/STORY-AIBRIDGE-41-openai-schema-projection.md) | — |
| P8 Done · pkg-000041 | STORY-AIBRIDGE-42-canonical-uniqueitems-validation | [Canonical uniqueItems validation (Gate 2)](STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [pipeline](../../epics/EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat/stories/STORY-AIBRIDGE-42-canonical-uniqueitems-validation/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) | — |
| P8 Done · pkg-000042 | STORY-AIBRIDGE-43-validation-context-bind-readyz | [Minimal ValidationContext bind + readiness](STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [pipeline](../../epics/EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat/stories/STORY-AIBRIDGE-43-validation-context-bind-readyz/STORY-AIBRIDGE-43-validation-context-bind-readyz.md) | 41, 42 |
| P6 Done · pkg-000043 superseded | STORY-AIBRIDGE-44-compat-merge-gate-proof | [Compat merge-gate proof (automated)](STORY-AIBRIDGE-44-compat-merge-gate-proof.md) · [pipeline](../../epics/EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat/stories/STORY-AIBRIDGE-44-compat-merge-gate-proof/STORY-AIBRIDGE-44-compat-merge-gate-proof.md) | 41, 42, 43 |
| P5 Done · deferred_live · next P7 · TASKED=0 · pkg-000044 | STORY-AIBRIDGE-45-compat-live-telegram-verify | [Live Telegram deployment verification (AC-09)](STORY-AIBRIDGE-45-compat-live-telegram-verify.md) · [pipeline](../../epics/EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat/stories/STORY-AIBRIDGE-45-compat-live-telegram-verify/STORY-AIBRIDGE-45-compat-live-telegram-verify.md) · [BLOCKED](../../ops/req-07-ac09-live-evidence-BLOCKED-20260924.md) | 44 |

## Build order

`41 ∥ 42 → 43 → 44 → 45`

## Out of package

- REQ-04 full confirm hardening (beyond minimal VC bind in 43)
- REQ-06 Phase B packaging
- Hand-edited dual node schemas / deleting `uniqueItems` from pack JSON
- NEW epic/pkg activation (P1.3 per story later)
