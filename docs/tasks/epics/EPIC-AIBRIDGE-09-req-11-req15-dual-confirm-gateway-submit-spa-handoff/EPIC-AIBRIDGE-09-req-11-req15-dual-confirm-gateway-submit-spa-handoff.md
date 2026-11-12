# EPIC-AIBRIDGE-09 — REQ-11 / REQ15 dual-confirm + gateway submit + SPA handoff

> **ID:** `EPIC-AIBRIDGE-09-req-11-req15-dual-confirm-gateway-submit-spa-handoff` · **Статус:** 🟡 In Progress (**STORY-58** P3 Done · next **P4**)  
> **P3 (story 58):** 2026-11-01T18:23:09Z · t08 PASS · tests 597 · AC-07 live Partial  
> **P1.3 (story 58):** 2026-11-01T18:20:43Z · active `pkg-000061` · **REUSE** epic  
> **P8 (story 57):** 2026-11-01T18:17:48Z · SHAs 1524b49/13a992f/2f89ae4  
> **P1.3 (story 57):** 2026-11-01T14:53:51Z · active `pkg-000060` · **REUSE** epic  
> **P8 (story 56):** 2026-11-01T14:51:13Z · SHAs 8a4774e/db5f5ac/22bccc3  
> **P1.3 (story 56):** 2026-11-01T14:34:14Z · active `pkg-000059` · **NEW** epic  
> **Package:** [`backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md`](../../backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/INDEX.md)  
> **Parent REQ:** [`REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md)  
> **Tech:** [`docs/architecture/req15-dual-confirm-handoff/`](../../../architecture/req15-dual-confirm-handoff/) (`00`–`03`) · Keep [`runtime/03-confirm-gateway.md`](../../../architecture/runtime/03-confirm-gateway.md)  
> **Does not modify:** EPIC-07 REQ-09 · EPIC-08 REQ-10 bodies · REQ-13 taxonomy invent

## Назначение

REQ-11 / REQ15: Keep pipe (56) · L11-1 invalidation seam (57) · stub/live evidence (58). Build order `56 → 57 → 58`.

**Не** invent epic-level AC — AC живут в story-файлах.  
**Не** invent live SUCCESS / Railway evidence в волне 58 (Partial without ops window).

## Stories

| Status | Key | Path |
|--------|-----|------|
| 🟢 P8 Done · pkg-000059 · 8a4774e/db5f5ac/22bccc3 | STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify | [pipeline](stories/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) · [backlog](../../backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) |
| 🟢 P8 Done · pkg-000060 · 1524b49/13a992f/2f89ae4 | STORY-AIBRIDGE-57-l11-invalidation-seam | [pipeline](stories/STORY-AIBRIDGE-57-l11-invalidation-seam/STORY-AIBRIDGE-57-l11-invalidation-seam.md) · [backlog](../../backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-57-l11-invalidation-seam.md) |
| 🟡 P3 Done · pkg-000061 · next P4 · AC-07 live Partial | STORY-AIBRIDGE-58-stub-live-evidence-gates | [pipeline](stories/STORY-AIBRIDGE-58-stub-live-evidence-gates/STORY-AIBRIDGE-58-stub-live-evidence-gates.md) · [backlog](../../backlog-stories/req-11-req15-dual-confirm-gateway-submit-spa-handoff/STORY-AIBRIDGE-58-stub-live-evidence-gates.md) |

## Порядок

`56 → 57 → 58`. Active wave: **STORY-58** (`pkg-000061`) — P3 Done · next **P4**.

## Non-goals этой волны (P1)

- Product runtime code в P1 (только task queue).
- Opening live ops window / inventing live SUCCESS.
- REQ-12 per-provider live body · REQ-13 taxonomy invent · gateway/SPA redesign.
