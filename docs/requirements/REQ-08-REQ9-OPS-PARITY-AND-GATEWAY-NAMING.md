# REQ-08: REQ9 — ops parity & gateway naming (hard cut)

**Index key:** REQ-08  
**Service / repo:** `doge-ai-bridge`  
Parent: docs/requirements backlog/REQ9-DOGEstonia-Microservices-Ops-Parity-Target.md §3, §5–§8.4, §10 (G1–G3, G6/R1–R2, R4, R8, G9)  
Parent-id: dogestonia-microservices-ops-parity-target  
Siblings:  
- doge-complaints-gateway/docs/requirements/53-req9-ops-parity-env-naming.md (contract: `GATEWAY_BASE_URL` host; `GATEWAY_SERVICE_API_TOKEN` = gateway `SERVICE_API_TOKEN`; `SPA_BASE_URL`)  
- spa-app/docs/requirements/18-req9-vite-identity-base-url.md (contract: `SPA_BASE_URL` value = public spa origin; no service token in spa)  
Status: Draft — awaiting PA.2  
Tech-arch: docs/architecture/req9-ops-naming/ (esp. 01, 02, 03, 04)  
**Version:** 0.1.0 · 2026-09-25  

**Related — Backlog:** [`../tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md`](../tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/INDEX.md) (STORY-AIBRIDGE-REQ9-01…04)  
**Related — Tech-arch:** [`../../../docs/architecture/req9-ops-naming/00-overview.md`](../../../docs/architecture/req9-ops-naming/00-overview.md)

---

## 1) Goal

Close aibridge as REQ9 ops+naming outlier: Make `serve`/`dev`, probes `/health`+`/ready`, railpack PORT 8080, hard-cut renames to `GATEWAY_*` and `SPA_BASE_URL`; keep channel Bearer distinct.

## 2) Scope / Out of scope

**In:** Makefile; probe aliases; `railpack.json`; config/template/docs renames R1 R2 R4; Railway var names+values per tech-arch 03 (generate/set allowed; operator rotates later); required `.env` on Make (G8).

**Out:** renaming channel to `SERVICE_API_TOKEN`; product channel OpenAPI changes; invent waitlist; alias dual-read of old `DOGESTONIA_INTAKE_*` / `DOGESTONIA_API_BEARER_TOKEN`.

## 3) Verified current state

- No Makefile; `PORT=8080 python -m aibridge`; `/healthz` `/readyz`; railpack `${PORT:-8000}`; `DOGESTONIA_INTAKE_BASE_URL` + `DOGESTONIA_API_BEARER_TOKEN` — REQ9 + integrity gap + naming analysis

## 4) Target behavior

- `make serve`/`dev` → uvicorn `aibridge.app:app` `:8080` with required `.env`  
- `GET /health` and `/ready` (aliases OK)  
- railpack `${PORT:-8080}`  
- `GATEWAY_BASE_URL`, `GATEWAY_SERVICE_API_TOKEN`, `SPA_BASE_URL` primary  
- `AIBRIDGE_CHANNEL_BEARER_TOKEN` ≠ gateway S2S token

## 5) Acceptance criteria

- [ ] G1 Makefile + README primary start  
- [ ] G2 `/health` `/ready`  
- [ ] G3 railpack fallback 8080  
- [ ] R1 R2 R4 hard cut in config+template+docs  
- [ ] R8 channel Keep and distinct  
- [ ] G9 `aibridge.app:app`  
- [ ] Local + Railway verify per tech-arch 04 (or residual recorded)

## 6) Open questions

- Railway project/service id — Unknown until implement  
- Exact remote smoke beyond `/health` — TBD at implement

## 7) Dependencies

Parent §8.4 §10; tech-arch; sibling gateway `53-…` for token pairing.
