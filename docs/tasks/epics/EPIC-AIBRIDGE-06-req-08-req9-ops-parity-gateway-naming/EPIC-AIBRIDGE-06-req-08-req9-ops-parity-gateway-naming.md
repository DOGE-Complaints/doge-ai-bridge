# EPIC-AIBRIDGE-06 — REQ-08 REQ9 ops parity & gateway naming

> **ID:** `EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming` · **Статус:** 🟡 In Progress (**REQ9-04** P5 Done · next **P7**)  
> **Package:** [`backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md`](../../backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md)  
> **P5 (story REQ9-04):** 2026-09-26T13:08:56Z · TASKED=0 · WAIVED G-01…G-04 · activation none · next **P7** (skip P6)  
> **P3 (story REQ9-04):** 2026-09-26T13:03:46Z · gate PASS · residual Y · `pkg-000048`  
> **P1.3 (story REQ9-04):** 2026-09-26T12:58:34Z · active `pkg-000048` · Lock C residual OK  
> **P1.3 (story REQ9-03):** 2026-09-26T12:38:37Z · `pkg-000047` (superseded as active) · Lock A hard cut  
> **P6 (story REQ9-02):** 2026-09-26T12:33:39Z · G-01/G-02 CLOSED · `pkg-000046` superseded  
> **P5 (story REQ9-02):** 2026-09-26T12:31:20Z · TASKED t05–t06  
> **P3 (story REQ9-02):** 2026-09-26T12:27:23Z · gate PASS  
> **P1.3 (story REQ9-02):** 2026-09-26T12:24:30Z · `pkg-000046`  
> **P1.3 (story REQ9-01):** 2026-09-26T12:12:53Z · `pkg-000045` (superseded)  
> **P3 (story REQ9-01):** 2026-09-26T12:14:54Z · gate PASS  
> **P5 (story REQ9-01):** 2026-09-26T12:18:29Z · TASKED t05–t06  
> **P6 (story REQ9-01):** 2026-09-26T12:20:13Z · G-01…G-03 CLOSED · next **P7** (parallel residual)  
> **Parent REQ:** [`REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md`](../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md)  
> **Tech:** [`docs/architecture/req9-ops-naming/`](../../../../../docs/architecture/req9-ops-naming/) (`01`–`04`)  
> **Does not modify:** EPIC-04 QA · EPIC-05 REQ-07 bodies

## Назначение

REQ-08 / REQ9: Make serve/dev + `.env`, probe aliases, railpack PORT 8080, hard-cut `GATEWAY_*` / `SPA_BASE_URL`. Build order `01 ∥ 02 → 03 → 04`.

**Не** invent epic-level AC — AC живут в story-файлах (backlog / pipeline).

## Stories

| Status | Key | Path |
|--------|-----|------|
| ✅ P6 Done · next P7 · pkg-000045 | STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack | [pipeline](stories/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) · [backlog](../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) |
| 🟡 P6 Done · next P7 · pkg-000046 | STORY-AIBRIDGE-REQ9-02-health-ready-aliases | [pipeline](stories/STORY-AIBRIDGE-REQ9-02-health-ready-aliases/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) · [backlog](../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) |
| ✅ P6 Done · next P7 · pkg-000047 | STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut | [pipeline](stories/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) · [backlog](../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) |
| 🟡 P5 Done · next P7 · pkg-000048 | STORY-AIBRIDGE-REQ9-04-local-railway-verify | [pipeline](stories/STORY-AIBRIDGE-REQ9-04-local-railway-verify/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md) · [backlog](../../backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md) |

## Порядок

`01 ∥ 02 → 03 → 04`. Active wave: **REQ9-04** (`pkg-000048`) — P5 Done · TASKED=0 · activation none · next **P7** (skip P6) · Lock C residual Y.

## Non-goals этой волны

- Product runtime code в P1 (только task queue).
- Makefile create before P3 (name ≠ create).
- Probe aliases / env hard-cut / live Railway invent (stories 02–04).
- Renaming channel Bearer to `SERVICE_API_TOKEN`.
