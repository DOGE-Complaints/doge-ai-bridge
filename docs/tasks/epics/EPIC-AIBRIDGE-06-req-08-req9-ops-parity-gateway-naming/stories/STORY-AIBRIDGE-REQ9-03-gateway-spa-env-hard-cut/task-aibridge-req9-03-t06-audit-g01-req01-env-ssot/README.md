# Task: docs — audit G-01 REQ-01 env SSOT sync

**Status:** Done · P6 2026-09-26T12:53:50Z · G-01 **CLOSED**  
**Skill declared:** code-documenter  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut-20260926.md` · G-01  
**Parent story:** [`STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md`](../STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md)  
**P5 scaffold:** 2026-09-26T12:52:08Z  
**P6 closed:** 2026-09-26T12:53:50Z  
**Maps:** REQ-01 env table ↔ REQ-08 R1/R2/R4 names

## Purpose

Sync parent `docs/requirements/REQ-01-doge-ai-bridge-runtime.md` env table / diagrams for the three hard-cut pairs to `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL`, **or** add an explicit «superseded by REQ-08 / STORY-REQ9-03» pointer. Docs-only — no product Lock A reopen.

## AC/DoD

- [x] REQ-01 documents target names for R1/R2/R4 **or** superseded pointer to REQ-08 / STORY-REQ9-03.
- [x] No Lock A product code / dual-read / channel→`SERVICE_API_TOKEN` / live Railway invent.
- [x] Do not rename helpers (G-02 WAIVED) or refresh `docs/analysis/**` historical (G-03 WAIVED).
- [x] `Skill declared: code-documenter` present.
- [x] pkg pointer stays pkg-000047.

## Where changed

- `docs/requirements/REQ-01-doge-ai-bridge-runtime.md` (§2 · §15 · §16 · §17 · Related · History v0.4.2)

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-03-t06-audit-g01-req01-env-ssot.md`](./acceptance-verification-task-aibridge-req9-03-t06-audit-g01-req01-env-ssot.md)
