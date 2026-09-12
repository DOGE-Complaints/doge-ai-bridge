# AI Bridge runtime — architecture overview

**Package:** `doge-ai-bridge/docs/architecture/runtime/`  
**Parent requirement:** [REQ-01 — doge-ai-bridge runtime](../../requirements/REQ-01-doge-ai-bridge-runtime.md) (v0.4.x)  
**Protocol parent:** [GPT UI REQ-47](https://github.com/DOGE-Complaints/DOGEstonia/blob/main/GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md)  
**Post-pilot (out of this package):** [REQ-02](../../requirements/REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md)  
**Pilot recommendations:** [ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md](../../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md)  
**Interview report:** [zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md](../../analysis/zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md)  
**As-of:** 2026-09-12 (ARCH-RECOMMENDATIONS applied)  
**Status:** Architecture for pilot — runtime scaffold present (`src/aibridge/`, STORY-AIBRIDGE-01)

---

## 1. Context

`doge-ai-bridge` is a **protocol channel adapter**: n8n (Telegram UI) → bridge (Responses, confirm, validation) → gateway stash → SPA continuation. It is not a Telegram bot and not a UI app ([REQ-01 §1–§2](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).

### CPO success (interview T1 = B)

Pilot success requires **both**:

1. Resident path: Telegram interview → dual-confirm → stash → SPA continuation (full E2E = wave 2).
2. Operator path: Railway deploy/redeploy with fail-closed readiness and channel Bearer rotation with overlap ([REQ-01 §7, §18](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).

---

## 2. Canonical topology

```text
Resident ↔ Telegram
         ↔ n8n (UI + routing) — public host e.g. telegram-bot.dogestonia.me
         ↔ doge-ai-bridge (private Railway hostname + $PORT)
         ↔ doge-complaints-gateway POST /story-drafts
         ↔ SPA {DOGESTONIA_DRAFT_REDIRECT_BASE_URL}/#/story/submit?draft_id=
```

| Concern | Owner |
|---------|--------|
| Telegram Bot API, keyboards, immediate `answerCallbackQuery` | n8n |
| Responses, sessions, confirm policy, gateway Bearer | `doge-ai-bridge` |
| Stash API | gateway |
| Final review | SPA |
| Versioned n8n workflow template (no secrets) | [docs/ops/n8n-channel-workflow/](../../ops/n8n-channel-workflow/README.md) |

**Contracts (do not mix):**

| File | Role |
|------|------|
| [docs/openapi/aibridge-channel-v1.openapi.yaml](../../openapi/aibridge-channel-v1.openapi.yaml) | n8n ↔ aibridge façade (`/v1/channel/*`) |
| [docs/openapi/story-intake-actions.openapi.yaml](../../openapi/story-intake-actions.openapi.yaml) | aibridge ↔ gateway wire (`postStoryDraftStash`) |

---

## 3. Runtime topology (interview T2 = A)

- **Single ASGI HTTP process** bound to Railway `$PORT`.
- Serves channel façade `/v1/channel/*`, `/healthz`, `/readyz`, and pilot `/metrics`.
- **No** separate queue/worker process in this release.
- Session serialization, locks, and **versioned content bundle registry** use **PostgreSQL** ([REQ-01 §10, §14](../../requirements/REQ-01-doge-ai-bridge-runtime.md); see [02-content-packaging.md](./02-content-packaging.md)).
- Exact Python module path / framework package name: `src/aibridge/` (`aibridge.app:app`, FastAPI) — STORY-AIBRIDGE-01 Done 2026-09-12.

---

## 4. Ownership matrix

| Artifact class | Content SSOT | How it reaches runtime |
|----------------|--------------|-------------------------|
| Instruction files + manifest | `GPT UI/instructions` (cross-repo; CI checkout) | Content stage → immutable tarball → image → register in Postgres by `bundle_hash` |
| Story Intake OpenAPI | [story-intake-actions.openapi.yaml](../../openapi/story-intake-actions.openapi.yaml) in this repo | Pin into bundle; used for tool/wire only |
| Active pack schema | Node/content tree (cross-repo CI checkout); one pack per deploy | Pin into bundle |
| Channel OpenAPI | [aibridge-channel-v1.openapi.yaml](../../openapi/aibridge-channel-v1.openapi.yaml) | Ship with service; contract-test against ASGI |
| Secrets | Railway / gitignored `.env` | Never committed |
| n8n workflow JSON | Ops artifact under `docs/ops/n8n-channel-workflow/` (export without credentials) | Import per node; not runtime code |

**Method note:** Git ownership ≠ image packaging — see [02-content-packaging.md](./02-content-packaging.md).  
CI uses **multi-repository checkout**, not fragile in-container monorepo `COPY` alone.

---

## 5. Packaging & verify

1. Operator selects content **commit SHA**(s); CI builds immutable **content tarball**.
2. Docker image = aibridge app + tarball.
3. On startup: verify hashes → **register-once** into PostgreSQL `content_bundle` by `bundle_hash` (immutable).
4. Sessions store `content_bundle_hash` FK; redeploy keeps prior bundles while sessions reference them; GC only when no active sessions + audit grace.
5. **Production verify:** `/readyz` + façade smoke (401 without Bearer).
6. Wave-1 live: n8n → `POST /v1/channel/turns` (private + channel Bearer); dry-run/interview; **no** stash.

---

## 6. Env / fail-closed pilot defaults

| Variable / concern | Pilot default (arch) |
|--------------------|----------------------|
| `AIBRIDGE_SESSION_TTL_SECONDS` | 7 days (604800); activity slides TTL |
| `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS` | 15 minutes (900) |
| LLM budgets | Required env names in [04-ops-security.md](./04-ops-security.md); **numeric values Unknown** until measured |
| Listen | `$PORT` only; no public aibridge domain |
| Channel auth | Private network + `AIBRIDGE_CHANNEL_BEARER_TOKEN` |
| Gateway Bearer | `DOGESTONIA_API_BEARER_TOKEN` — bridge only |

---

## 7. Deploy waves & residual

| Wave | Gate | Explicitly not required |
|------|------|-------------------------|
| **1 — infrastructure** | Migrations + `/readyz` + V2 smoke + live n8n→`/turns` (dry-run/interview); no stash | Full dual-confirm → gateway → SPA |
| **2 — E2E / residents** | Dual-confirm E2E; **user-reachable HTTPS SPA** base (not phone-localhost); n8n privacy settings; privacy notice | — |

`localhost` SPA base is only for controlled tests where the opening device can reach it. Telegram mobile requires a real HTTPS SPA origin for wave 2.

---

## 8. Observability & privacy boundary

- Redacted stdout logs; `/healthz` `/readyz`; private `/metrics` (incl. budget-stop reasons).
- **aibridge retention ≠ n8n retention** — see [privacy-pilot.md](../../runbooks/privacy-pilot.md).
- Channel Bearer rotation: [channel-bearer-rotation.md](../../runbooks/channel-bearer-rotation.md).
- `unknown_outcome`: [unknown-outcome-reconciliation.md](../../runbooks/unknown-outcome-reconciliation.md).

---

## 9. Seams & roles

| Seam | Pilot rule |
|------|------------|
| Content × Runtime | Content merge ≠ prod; operator picks SHA → CI → register bundle → redeploy |
| Runtime × n8n | N2 one operator; contracts N1-ready; workflow from ops template |
| Confirm × Gateway | Wave 1 dry-run; wave 2 real stash |

---

## 10. Node scaling (pilot rule — not REQ-02)

```text
one deployment = one node = one active pack
```

- Same Docker image / code for new nodes; differences only in verified bundle, env, secrets ([ARCH-RECOMMENDATIONS §4](../../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md)).
- No `uus_veerenni` / civic hardcoding in Python.
- Server-owned `deployment_id` / `node_id` on security-relevant rows; never trust client-supplied node id for auth.
- Federation / Identity / multi-tenant runtime → **REQ-02**, not this package.

---

## 11. Sibling documents

| Doc | Focus |
|-----|--------|
| [01-channel-facade.md](./01-channel-facade.md) | Channel OpenAPI, ack order, compatibility |
| [02-content-packaging.md](./02-content-packaging.md) | Bundle registry, CI, GC |
| [03-confirm-gateway.md](./03-confirm-gateway.md) | FSM, budgets pre-send, reconciliation |
| [04-ops-security.md](./04-ops-security.md) | Metrics, privacy, budgets, node release checklist |

---

## 12. Story-slice hints (no STORY keys invented)

1. Channel façade + Bearer + event dedupe + OpenAPI contract tests  
2. Content bundle registry + GC  
3. Confirm FSM + action tokens  
4. Gateway executor + dry-run + unknown_outcome  
5. Ops: readiness, metrics, budgets, n8n workflow import, wave gates  

---

## 13. Open Unknowns (pilot)

1. ~~Exact ASGI module path / framework package~~ → resolved: `src/aibridge/` FastAPI (`aibridge.app:app`).  
2. Numeric LLM budget / rate-limit defaults (set after measuring bundle + model).  
3. Absolute CI checkout paths for instruction/pack sources outside this repo.
