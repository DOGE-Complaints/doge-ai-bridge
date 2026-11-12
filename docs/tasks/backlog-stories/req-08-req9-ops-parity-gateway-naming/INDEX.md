# req-08-req9-ops-parity-gateway-naming — INDEX

> **Пакет:** REQ-08 — REQ9 ops parity & gateway naming (hard cut)  
> **Parent REQ:** [`REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md`](../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md)  
> **Parent product:** [`REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md`](../../../../../docs/requirements%20backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md)  
> **Tech-arch:** [`docs/architecture/req9-ops-naming/`](../../../../../docs/architecture/req9-ops-naming/) (`01`–`04`)  
> **Siblings:** gateway [`53-req9-ops-parity-env-naming`](../../../../../doge-complaints-gateway/docs/requirements/53-req9-ops-parity-env-naming.md) · spa [`18-req9-vite-identity-base-url`](../../../../../spa-app/docs/requirements/18-req9-vite-identity-base-url.md) · identity `22` · threads `02`  
> **P5 note (2026-09-26T13:08:56Z):** STORY-REQ9-04 P5 Done · TASKED=0 · WAIVED G-01…G-04 · activation none · next **P7** (skip P6) · [p5](../../run-reports/run-summary-20260926-1308-story-aibridge-req9-04-p5-disposition.md)  
> **P3 note (2026-09-26T13:03:46Z):** STORY-REQ9-04 P3 Done · gate PASS · residual Y · next **P4** · [p3](../../run-reports/run-summary-20260926-1303-story-aibridge-req9-04-p3.md) · [ops](../../../ops/req-08-req9-verify-20260926.md)  
> **P1.3 note (2026-09-26T12:58:34Z):** STORY-REQ9-04 pipeline materialized · **REUSE EPIC-06** · active `pkg-000048` · Lock C residual OK · next **P2**  
> **P1.3 note (2026-09-26T12:38:37Z):** STORY-REQ9-03 pipeline materialized · **REUSE EPIC-06** · active `pkg-000047` · Lock A hard cut · next **P2**  
> **P3 note (2026-09-26T12:46:12Z):** STORY-REQ9-03 P3 Done · gate PASS · next **P4** · [p3](../../run-reports/run-summary-20260926-1246-story-aibridge-req9-03-p3.md)  
> **P5 note (2026-09-26T12:52:08Z):** STORY-REQ9-03 P5 Scaffolded · TASKED t06 · WAIVED G-02/G-03 · next **P6** · [p5](../../run-reports/run-summary-20260926-1252-story-aibridge-req9-03-p5-disposition.md)  
> **P6 note (2026-09-26T12:53:50Z):** STORY-REQ9-03 P6 Done · G-01 CLOSED · next **P7** · [p6](../../run-reports/run-summary-20260926-1253-story-aibridge-req9-03-p6.md)  
> **P6 note (2026-09-26T12:33:39Z):** STORY-REQ9-02 P6 Done · G-01/G-02 CLOSED · next **P7** · [p6](../../run-reports/run-summary-20260926-1233-story-aibridge-req9-02-p6.md)  
> **P5 note (2026-09-26T12:31:20Z):** STORY-REQ9-02 P5 Scaffolded · TASKED t05–t06 · G-03 WAIVED · next **P6** · [p5](../../run-reports/run-summary-20260926-1231-story-aibridge-req9-02-p5-disposition.md)  
> **P3 note (2026-09-26T12:27:23Z):** STORY-REQ9-02 P3 Done · gate PASS · next **P4** · [p3](../../run-reports/run-summary-20260926-1227-story-aibridge-req9-02-p3.md)  
> **P1.3 note (2026-09-26T12:24:30Z):** STORY-REQ9-02 pipeline materialized · **REUSE EPIC-06** · `pkg-000046` · next **P2**  
> **P6 note (2026-09-26T12:20:13Z):** STORY-REQ9-01 P6 Done · G-01…G-03 CLOSED · next **P7** · [p6](../../run-reports/run-summary-20260926-1220-story-aibridge-req9-01-p6.md)  
> **P3 note (2026-09-26T12:14:54Z):** STORY-REQ9-01 P3 Done · gate PASS · [p3](../../run-reports/run-summary-20260926-1214-story-aibridge-req9-01-p3.md)  
> **P1.3 note (2026-09-26T12:12:53Z):** STORY-REQ9-01 pipeline materialized · **NEW EPIC-06** · `pkg-000045` · Makefile name≠create until P3  
> **Emitted:** 2026-09-26T12:02:45Z · materialize from REQ→backlog (operator «запиши»)
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)  
> **Operator locks:** hard cut env+Python (**A**); keys `STORY-AIBRIDGE-REQ9-*` (**A**); Railway names checklist in 03 / verify+residual in 04 (**C**)

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| P6 Done · next P7 · pkg-000045 | STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack | [Makefile serve/dev + .env + railpack 8080](STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) · [pipeline](../../epics/EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming/stories/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) | — |
| P6 Done · next P7 · pkg-000046 | STORY-AIBRIDGE-REQ9-02-health-ready-aliases | [GET /health and /ready aliases](STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) · [pipeline](../../epics/EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming/stories/STORY-AIBRIDGE-REQ9-02-health-ready-aliases/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) | — |
| P6 Done · next P7 · pkg-000047 | STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut | [GATEWAY_* + SPA_BASE_URL hard cut](STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) · [pipeline](../../epics/EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming/stories/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) | 01, 02 |
| P5 Done · next P7 · pkg-000048 | STORY-AIBRIDGE-REQ9-04-local-railway-verify | [Local + Railway verify (or residual)](STORY-AIBRIDGE-REQ9-04-local-railway-verify.md) · [pipeline](../../epics/EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming/stories/STORY-AIBRIDGE-REQ9-04-local-railway-verify/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md) | 01, 02, 03 |

## Build order

`01 ∥ 02 → 03 → 04`

## Out of package

- Renaming channel to `SERVICE_API_TOKEN`
- Product channel OpenAPI changes
- Dual-read of old `DOGESTONIA_INTAKE_*` / `DOGESTONIA_API_BEARER_TOKEN` / `DOGESTONIA_DRAFT_REDIRECT_*`
- Invent waitlist / nginx
- P1.3/pkg activation (later per story)
