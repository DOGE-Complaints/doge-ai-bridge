# Zeya888 — REQ → tech-arch interview report

**Slug:** REQ-01-doge-ai-bridge-runtime  
**utc_date:** 2026-09-12 (from `builder_resolve_queue.py --print-utc-now` → `utc_now: 2026-09-12T19:05:06Z`)  
**builder_project:** `aibridge`  
**focus_folder:** `doge-ai-bridge`  
**Requirement:** [REQ-01-doge-ai-bridge-runtime.md](../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Architecture root:** [architecture/runtime/00-overview.md](../architecture/runtime/00-overview.md)

---

## Inputs

- `@.cursor/rules/analysis.mdc`
- `docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md`
- REQ-01 v0.4.0 (Ready for implementation)
- Operator interactive answers in Architect Studio chat (2026-09-12)
- Path override on materialize: `docs/architecture/runtime/` (not `aibridge-runtime/`)

---

## Verbatim decision log

| # | Question theme | Operator answer (verbatim / compact) | Recommendation | Outcome |
|---|----------------|--------------------------------------|----------------|---------|
| T1 | CPO success | **B** — resident path + Railway redeploy/rotate with Bearer overlap | Prefer B | **accepted** |
| T2 | Runtime | **A** — single ASGI on `$PORT`, no worker v1 | Prefer A | **accepted** |
| T3 | Ownership | **A1 B1 C1 D1** — instructions/OAS/pack from monorepo via CI COPY; channel OpenAPI in aibridge | Prefer matrix | **accepted** |
| T4 | Packaging + verify | **B + V2** — CI tarball then Docker; `/readyz` + façade smoke | Prefer B+V2 | **accepted** |
| T5 | TTL / bind | **S1 T1 L1** — session 7d; action token 15m; `$PORT` only | Prefer | **accepted** |
| T6 | Deploy gate | **B** + clarification: wave 1 needs live n8n→`/v1/channel/turns` private+Bearer, interview/dry-run, no stash; full E2E next gate | Prefer clarified B | **accepted** |
| T7 | Obs + runbook | **B + R2** — logs, health, private `/metrics` with listed families; README + `docs/runbooks/channel-bearer-rotation.md` with overlap sequence; no SaaS | Prefer | **accepted** |
| T8 | Seams | **B + N2** — content merge ≠ prod; operator picks SHA; multi-bundle retention preferred; one pilot operator for aibridge+n8n; document N1-ready roles | Prefer + multi-bundle | **accepted** |
| T9 | Privacy + metrics auth | **P1 + M1** — narrative ≤7d sliding; early purge after stash/Cancel; redacted audit longer; `/metrics` private only; future M3 separate token; principal ≠ Identity | Prefer | **accepted** |

---

## Open Unknowns

1. Exact ASGI module path / framework package (no product code yet).
2. Absolute monorepo paths for Story Intake OpenAPI + pack tree in CI tarball.
3. Physical multi-bundle storage mechanism.
4. Railway private scrape details for `/metrics` without token.
5. `docs/openapi/aibridge-channel-v1.openapi.yaml` not created (name ≠ create until implement).
6. Numeric defaults for rate limits / some byte caps beyond interview TTLs.
7. Fallback controlled session-kill if GC of old bundles is deferred.

---

## Link matrix

| Artifact | Path |
|----------|------|
| REQ | `doge-ai-bridge/docs/requirements/REQ-01-doge-ai-bridge-runtime.md` |
| Arch root | `doge-ai-bridge/docs/architecture/runtime/00-overview.md` |
| Arch siblings | `01-channel-facade.md`, `02-content-packaging.md`, `03-confirm-gateway.md`, `04-ops-security.md` |
| This report | `doge-ai-bridge/docs/analysis/zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md` |
| Runbook | `doge-ai-bridge/docs/runbooks/channel-bearer-rotation.md` |

---

## Method note

**Git ownership ≠ image packaging.** Content SSOT in the monorepo must be explicitly staged into an immutable bundle/image; pinned sessions require retaining still-referenced bundle versions across redeploys (session TTL 7 days).
