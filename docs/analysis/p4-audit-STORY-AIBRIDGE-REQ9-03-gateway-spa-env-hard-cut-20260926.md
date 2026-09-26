# P4 Audit — STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:49:31Z |
| **Mode** | `input_mode=backlog_story` / epic_story pipeline |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/run-reports/run-summary-20260926-1246-story-aibridge-req9-03-p3.md` |
| **$story** | `…/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md` |
| **Method** | rg Lock A (src/tests/.env.example) · Settings dual-read proof · R8 helper · runbook §2.4.1 · focused pytest; no product patches; **no** Railway invent |
| **Thinking** | `.cursor/rules/analysis.mdc` · aibridge-operator-contract §6 · workflow §P4 |
| **Locks** | **A** hard cut · **C** Railway names-only |
| **Out of scope** | Dual-read · channel→`SERVICE_API_TOKEN` · OpenAPI product invent · live Railway (04) |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (R1 R2 R4 · R8 · Lock A · checklist C)** | **PASS** |
| **Bullrun t01–t05 Done** | **Confirmed** vs code/docs/tests + gate acceptance |
| **OPEN gaps** | **0 Crit · 0 High · 0 Med · 1 Low · 2 Info** |
| **Critical / High OPEN** | **0** |
| **Live pytest (focused slice)** | **75 passed** (auth/readyz/gateway/contract/continuation) @ 2026-09-26T12:49:31Z · P3 claimed **92** focused |

---

## Bullrun touchpoints (актуализация `$bullrun`)

| ID | P3 claim | P4 fact |
|----|----------|---------|
| **STORY-REQ9-03** | P3 Done · next P4 · Lock A/C | **Confirmed** · **this P4** → next **P5** |
| **t01** | Done · Settings hard cut | **Confirmed** `config.py` aliases GATEWAY_* / SPA_BASE_URL only |
| **t02** | Done · consumers + R8 | **Confirmed** `gateway.py` · `readiness.py` · equal-bearer fail-closed |
| **t03** | Done · .env.example + checklist | **Confirmed** + runbook §2.4.1 names-only |
| **t04** | Done · tests · 92 focused | **Confirmed** no old primary names in `tests/` · this P4 **75** on core slice |
| **t05** | PASS · story gate | **Confirmed** acceptance |
| **No dual-read** | claimed | **Proved** — old env kwargs do not populate new Settings fields |
| **Railway live** | deferred 04 | **Confirmed** — no invent SUCCESS |

---

## AC matrix (pipeline / `$storyFile` · REQ-08 R1 R2 R4 R8 · Lock A/C)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| **R1** intake URL | `GATEWAY_BASE_URL` / `gateway_base_url` | **PASS** | `config.py` Field + `intake_base_url()` reads new field |
| **R2** gateway S2S | `GATEWAY_SERVICE_API_TOKEN` | **PASS** | Field + `gateway.py` `authorization_header` · readiness requires token |
| **R4** SPA base | `SPA_BASE_URL` / `spa_base_url` | **PASS** | Field + `draft_redirect_base_ok()` · ops r3-p1-08 |
| **Lock A** no dual-read | Old three names not read | **PASS** | rg clean `src/`+`tests/` (except comment); `.env.example` no primary old assigns; Settings(`DOGESTONIA_INTAKE_…`) → empty new fields |
| **R8** channel Keep ≠ gateway | Distinct + fail if equal | **PASS** | `AIBRIDGE_CHANNEL_BEARER_TOKEN` kept · `channel_gateway_bearers_equal()` · fixtures `channel_gateway_bearer_equal` |
| **Checklist C** | Railway **names** only | **PASS** | runbook §2.4.1 · story Railway table · «live → 04» |
| Nested t01–t05 | Done / PASS | **PASS** | README + acceptance 12:46:12Z |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| Manuals / arch runtime / ops | **PASS** | no old three primary names under manuals/architecture/runtime/ops |
| Pilot + web runbooks | **PASS** | `GATEWAY_*` / `SPA_BASE_URL` · removed-as-primary note |
| Remaining `DOGESTONIA_*` content paths | **Non-gap** | `DOGESTONIA_INSTRUCTIONS_*` etc. out of R1/R2/R4 |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | Parent `docs/requirements/REQ-01-doge-ai-bridge-runtime.md` still lists `DOGESTONIA_API_BEARER_TOKEN` / `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` (and related) as canonical env — product Lock A already cut to GATEWAY_*/SPA_*. | Sync REQ-01 env table / diagrams to REQ-08 names (docs SSOT); or explicit «superseded by REQ-08» pointer. |
| **G-02** | **Info** | Helper method names `intake_base_url()` / `draft_redirect_base_ok()` retain pre-cut vocabulary while reading new fields (not dual-read). | Optional rename for honesty; not required for Lock A. |
| **G-03** | **Info** | Historical `docs/analysis/aibridge-n8n-integration-context-2026-09-19.md` still cites gateway Bearer as `DOGESTONIA_API_BEARER_TOKEN`. | Refresh analysis note or mark superseded. |

### Non-gaps

| Topic | Note |
|-------|------|
| Dual-read AliasChoices for old three | Absent in `config.py` |
| Invent Railway SUCCESS / live set | Avoided · Lock C names-only |
| Renaming channel to `SERVICE_API_TOKEN` | Avoided · R8 Keep |
| Soft dual-read via getattr old names | Absent in `gateway.py` / `readiness.py` |

### Regressions

| Topic | Note |
|-------|------|
| vs P3 gate | **None** on Lock A / R8 path |
| Old env still accepted as primary | **None** — explicit Settings proof |

---

## Cited paths

- `src/aibridge/config.py` · `gateway.py` · `readiness.py`
- `.env.example`
- `docs/runbooks/aibridge-web-service-local-railway.md` §2.4.1
- `docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md`
- `docs/ops/r3-p1-08-spa-https-continuation-gate.md`
- `tests/**` (no old primary three)
- Pipeline / tasks under `…/STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut/`
- P3: `docs/tasks/run-reports/run-summary-20260926-1246-story-aibridge-req9-03-p3.md`
- REQ-01 residual: `docs/requirements/REQ-01-doge-ai-bridge-runtime.md` (G-01)

---

## Handoff

- **OPEN gaps:** 0 Crit · 0 High · 0 Med · **1 Low** · **2 Info**
- **OPEN IDs:** G-01, G-02, G-03
- **AC vs story:** **PASS**
- **next:** **P5**
