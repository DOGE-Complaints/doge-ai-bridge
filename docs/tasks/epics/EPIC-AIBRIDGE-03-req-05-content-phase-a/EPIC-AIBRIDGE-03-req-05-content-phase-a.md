# EPIC-AIBRIDGE-03 — REQ-05 Content Phase A (flat launch)

> **ID:** `EPIC-AIBRIDGE-03-req-05-content-phase-a` · **Статус:** 🟡 In Progress (**19–21** P8 Done · **22** P6 · next **P7**)  
> **Package:** [`backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md`](../../backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md)  
> **P6 closed (story 22 t06):** 2026-09-16T13:49:48Z · next **P7**  
> **Parent REQ:** [`REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0  
> **Tech:** [`TECHNICAL-ARCHITECTURE.md`](../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md)  
> **Does not modify:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) body

## Назначение

Content Phase A: full flat dump + stable-prefix wiring (stories 19–22). Build order `19 ∥ 20 ∥ 21 → 22`.

**Не** invent epic-level AC — AC живут в story-файлах (backlog / pipeline).

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 Done (P8) | STORY-AIBRIDGE-19-assembled-instructions-engine-wire | [pipeline](stories/STORY-AIBRIDGE-19-assembled-instructions-engine-wire/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [backlog](../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) |
| 🟢 Done (P8) | STORY-AIBRIDGE-20-full-instructions-manifest | [pipeline](stories/STORY-AIBRIDGE-20-full-instructions-manifest/STORY-AIBRIDGE-20-full-instructions-manifest.md) · [backlog](../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md) |
| 🟢 Done (P8) | STORY-AIBRIDGE-21-oas-image-env-docs | [pipeline](stories/STORY-AIBRIDGE-21-oas-image-env-docs/STORY-AIBRIDGE-21-oas-image-env-docs.md) · [backlog](../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md) |
| 🟢 Implemented (P6 · next P7) | STORY-AIBRIDGE-22-content-phase-a-proof | [pipeline](stories/STORY-AIBRIDGE-22-content-phase-a-proof/STORY-AIBRIDGE-22-content-phase-a-proof.md) · [backlog](../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md) |

## Порядок

`19 ∥ 20 ∥ 21 → 22`. Active wave: **story 22** (`pkg-000019`) — P6 · next **P7**.

## Non-goals этой волны

- Product runtime code в P1 (только task queue).
- REQ-06 profiles / multi-repo; invent spa stories.
