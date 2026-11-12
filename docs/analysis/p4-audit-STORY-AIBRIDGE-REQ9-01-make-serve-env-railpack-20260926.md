# P4 Audit — STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:16:55Z |
| **Mode** | `input_mode=backlog_story` / epic_story pipeline |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/run-reports/run-summary-20260926-1214-story-aibridge-req9-01-p3.md` |
| **$story** | `…/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md` |
| **Method** | Read Makefile / README / railpack / `__main__.py` + `make -n` + fail-closed probe (no `.env`) + IDS/gateway Makefile etalon; no product patches; **no** Railway invent |
| **Thinking** | `.cursor/rules/analysis.mdc` · aibridge-operator-contract §6 · workflow §P4 |
| **Scope** | Makefile serve/dev + `.env`; README make primary; railpack `${PORT:-8080}`; `aibridge.app:app` |
| **Out of scope** | Probes (02) · env/Python hard-cut (03) · Railway live verify (04) |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (G1 · G8 · G3 · G9)** | **PASS** |
| **Bullrun t01–t04 Done** | **Confirmed** vs README/acceptance + product files @ P3 stamp |
| **OPEN gaps** | **0 Crit · 0 High · 0 Med · 2 Low · 1 Info** |
| **Critical / High OPEN** | **0** |
| **Live product invent** | **None** this P4 |

---

## Bullrun touchpoints (актуализация `$bullrun`)

| ID | P3 claim | P4 fact |
|----|----------|---------|
| **STORY-REQ9-01** | P3 Done · gate PASS · next P4 | **Confirmed** product AC · **this P4** → next **P5** |
| **t01** | Done · Makefile serve/dev + .env | **Confirmed** `Makefile` · G8 pattern · fail-closed without `.env` |
| **t02** | Done · README primary make | **Confirmed** Quick start `make serve`/`dev` · thin alias |
| **t03** | Done · railpack `${PORT:-8080}` · G9 | **Confirmed** `railpack.json` · `__main__.py` unchanged G9 |
| **t04** | PASS · story gate | **Confirmed** acceptance AC matrix |
| **Changed paths** | Makefile · README · railpack | **Confirmed** on disk |
| **Backlog Verified** | emit-era «No Makefile» / `${PORT:-8000}` | **Stale** → **Low G-01** |
| **Runbook web** | (not in P3 table) | Still `${PORT:-8000}` line → **Low G-02** |

---

## AC matrix (pipeline / `$storyFile` · REQ-08 G1 G3 G8 G9)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| **G1** Makefile | `serve` / `dev` → uvicorn `aibridge.app:app` `:8080` | **PASS** | `Makefile` L6–14 · `$${PORT:-8080}` · host `127.0.0.1` (peer IDS/gateway pattern) |
| **G1** README primary | Quick start → `make serve` / `make dev` | **PASS** | `README.md` L23 · L33–35 · thin alias documented |
| **G8** `.env` required | `set -a && . ./.env && set +a` | **PASS** | Makefile both targets · cwd without `.env` → `./.env: No such file` · `make: *** [serve] Error 1` |
| **G3** railpack | `${PORT:-8080}` | **PASS** | `railpack.json` L7 |
| **G9** app string | `aibridge.app:app` | **PASS** | Makefile · railpack · `src/aibridge/__main__.py` L17 |
| Nested t01–t04 | Done / PASS | **PASS** | task README + acceptance 2026-09-26T12:14:54Z |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| Align G8 to gateway/IDS etalon | **PASS** | Same `set -a && . ./.env && set +a` + `.venv/bin/python` + `--app-dir src` |
| No probe / hard-cut / Railway invent | **PASS** | No claims in gate acceptance |
| SPA / hasUxPipeline | false | |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Low** | Backlog `$storyFile` «Verified current state» still claims no Makefile, README `PORT=8080 python -m aibridge`, railpack `${PORT:-8000}` — post-P3 files contradict. | Sync Verified (+ optional Target `[x]`) to post-P3 Makefile/README/railpack facts. |
| **G-02** | **Low** | `docs/runbooks/aibridge-web-service-local-railway.md` still documents Railpack `${PORT:-8000}` and local primary `PORT=8080 python -m aibridge` — drifts from G1/G3 after P3. | Align runbook lines to `make serve`/`dev` + `${PORT:-8080}` (docs-only). |
| **G-03** | **Info** | Backlog Target / AC checkboxes still `[ ]` while pipeline Target `[x]` and gate PASS. | Checkbox sync on backlog after Verified refresh. |

### Non-gaps

| Topic | Note |
|-------|------|
| Invent Railway SUCCESS / live deploy | Avoided · out of scope 04 |
| Probe aliases / env hard-cut | Avoided · out of scope 02/03 |
| Softening G8 (optional `.env`) | Avoided — missing `.env` fails Make |
| Changing G9 app path | Avoided — `aibridge.app:app` kept |
| `.venv/bin/python` hardcode | Peer-parity with gateway/IDS — not a story AC miss |

### Regressions

| Topic | Note |
|-------|------|
| vs P3 gate PASS | **None** on product paths |
| railpack fallback 8000 | **Gone** from `railpack.json` (still present in runbook → G-02) |

---

## Cited paths

- `Makefile`
- `README.md`
- `railpack.json`
- `src/aibridge/__main__.py`
- `docs/runbooks/aibridge-web-service-local-railway.md` (G-02)
- Pipeline / tasks under `…/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack/`
- Backlog: `…/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`
- P3: `docs/tasks/run-reports/run-summary-20260926-1214-story-aibridge-req9-01-p3.md`
- Etalon: `doge-identity-service/Makefile` · `doge-complaints-gateway/Makefile`
- TECH: `docs/architecture/req9-ops-naming/01-runtime-and-probes.md`

---

## Handoff

- **OPEN gaps:** 0 Crit · 0 High · 0 Med · **2 Low** · **1 Info**
- **OPEN IDs:** G-01, G-02, G-03
- **AC vs story:** **PASS**
- **next:** **P5** (disposition; do not implement in P4)
