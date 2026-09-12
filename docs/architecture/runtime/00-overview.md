# AI Bridge runtime — architecture overview

**Package:** `doge-ai-bridge/docs/architecture/runtime/`  
**Parent requirement:** [REQ-01 — doge-ai-bridge runtime](../../requirements/REQ-01-doge-ai-bridge-runtime.md) (v0.4.0)  
**Protocol parent:** [GPT UI REQ-47](../../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md)  
**Interview report:** [zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md](../../analysis/zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md)  
**As-of:** 2026-09-12 (tech-arch interview materialize)  
**Status:** Architecture from REQ + operator interview — **no product runtime code on disk yet**

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
| Telegram Bot API, keyboards, `answerCallbackQuery` | n8n |
| Responses, sessions, confirm policy, gateway Bearer | `doge-ai-bridge` |
| Stash API | gateway |
| Final review | SPA |

---

## 3. Runtime topology (interview T2 = A)

- **Single ASGI HTTP process** bound to Railway `$PORT`.
- Serves channel façade `/v1/channel/*`, `/healthz`, `/readyz`, and pilot `/metrics`.
- **No** separate queue/worker process in this release.
- Session serialization and locks use **PostgreSQL** ([REQ-01 §10, §14](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).
- Exact Python module path / framework package name: **Unknown** until implement (no application code yet).

---

## 4. Ownership matrix (interview T3)

| Artifact class | Git / content SSOT | How it reaches runtime |
|----------------|--------------------|-------------------------|
| Instruction files + `instructions.manifest.json` | `GPT UI/instructions` (manifest-listed roots only) | CI content stage → immutable bundle in image ([REQ-01 §8](../../requirements/REQ-01-doge-ai-bridge-runtime.md)) |
| Canonical Story Intake OpenAPI | External SSOT (GPT UI / wire path); not rewritten in bridge | COPY/pin into bundle |
| Active pack `payload.schema.json` + id/version | Node/content tree in monorepo; one pack per deploy | COPY/pin into bundle |
| Channel OpenAPI `docs/openapi/aibridge-channel-v1.openapi.yaml` | **This repo** (named in REQ; **not on disk yet** — name ≠ create) | Ship with service; contract-test against runtime |
| Secrets | Railway secrets / local gitignored `.env` | Never in image layers as committed files |
| n8n workflow JSON | Out of REQ deliverables | Ops artifact outside this package |

**Method note:** Git ownership ≠ image packaging — see [02-content-packaging.md](./02-content-packaging.md).

---

## 5. Packaging & verify (interview T4 = B + V2)

1. CI builds a **content tarball** (instructions + OAS + pack + `DOGESTONIA_CONTENT_SOURCE_COMMIT`).
2. Docker image builds from aibridge context **plus** that tarball (self-contained service image).
3. **Production verify:** `/readyz` == ready **and** façade smoke (e.g. unauthenticated channel call → 401; health OK).
4. Unit/contract/concurrency suites remain CI gates ([REQ-01 §20](../../requirements/REQ-01-doge-ai-bridge-runtime.md)); V2 does not replace them.

**Multi-bundle retention (interview T8):** pinned sessions may outlive a redeploy (session TTL 7 days). Runtime must keep **current + still-referenced** content versions (prefer over forced session kill). Physical store mechanism: **Unknown** (volume vs multi-version artifact) — principle fixed.

---

## 6. Env / fail-closed pilot defaults (interview T5)

| Variable / concern | Pilot default (arch) |
|--------------------|----------------------|
| `AIBRIDGE_SESSION_TTL_SECONDS` | 7 days (604800); activity slides TTL |
| `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS` | 15 minutes (900) |
| Listen | `$PORT` only; **no** public domain required for aibridge |
| Channel auth | Private network **+** `AIBRIDGE_CHANNEL_BEARER_TOKEN` (mode C) |
| Gateway Bearer | `DOGESTONIA_API_BEARER_TOKEN` — bridge only; ≠ channel token |

Fail-closed readiness per [REQ-01 §18](../../requirements/REQ-01-doge-ai-bridge-runtime.md).

---

## 7. Deploy waves & residual (interview T6)

| Wave | Gate | Explicitly not required |
|------|------|-------------------------|
| **1 — infrastructure** | Image + migrations + `/readyz` + V2 smoke + **live** n8n → `POST /v1/channel/turns` over Railway private networking with channel Bearer; interview or `AIBRIDGE_DRY_RUN`; **no** `POST /story-drafts` | Full Telegram dual-confirm → gateway → SPA |
| **2 — E2E** | Full resident path including stash + SPA continuation | — |

---

## 8. Observability (interview T7)

- Structured **redacted** logs to stdout.
- `/healthz`, `/readyz`.
- Prometheus-compatible `/metrics` (request counts, errors, latency, confirm states, OpenAI/gateway calls, prompt-cache telemetry) — **no** PII/narrative/secrets; **private network only** (pilot). Future external scrape → separate metrics token (not channel Bearer).
- Channel Bearer rotation: [Operator README](../../requirements/REQ-01-doge-ai-bridge-runtime.md) deliverable + [channel-bearer-rotation.md](../../runbooks/channel-bearer-rotation.md).

---

## 9. Seams & roles (interview T8)

| Seam | Pilot rule |
|------|------------|
| Content × Runtime | Content owners merge to Git; **aibridge operator** selects commit SHA → CI bundle+image → readiness/smoke → redeploy. Merge must **not** auto-change production. |
| Runtime × n8n | Pilot **N2**: one operator configures both; document boundaries so later **N1** split needs no façade contract change. |
| Confirm × Gateway | Wave 1 dry-run/interview; wave 2 real stash. |

---

## 10. Privacy (interview T9)

- Narrative + Responses items: ≤ **7 days** from last activity (sliding); early delete after stash or Cancel when not needed for continuation.
- Longer retention only for **redacted** audit metadata (timestamps, outcome class, bundle version, operationId, hashes) — no full text, no Telegram profile dump, no secrets.
- `user_id` / `chat_id` = channel principal only — **not** DOGEstonia Identity ([REQ-01 §3.2](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).
- Responses `store: false` ([REQ-01 §10](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).

---

## 11. Sibling documents

| Doc | Focus |
|-----|--------|
| [01-channel-facade.md](./01-channel-facade.md) | n8n ↔ `/v1` contract, auth, wave-1 live call |
| [02-content-packaging.md](./02-content-packaging.md) | Bundle, pin, multi-version, verify surfaces |
| [03-confirm-gateway.md](./03-confirm-gateway.md) | Dual-confirm FSM, validation, gateway, dry-run |
| [04-ops-security.md](./04-ops-security.md) | Health, metrics, secrets, privacy, wave gates |

---

## 12. Story-slice hints (no STORY keys invented)

Useful backlog slices after `req-to-backlog-stories` (operator-owned keys):

1. Channel façade + Bearer + event dedupe  
2. Content bundle loader + multi-version pin/GC  
3. Confirm FSM + action tokens  
4. Gateway executor + dry-run + outcomes  
5. Ops: readiness, metrics, rotation runbook, wave-1 n8n proof  

---

## 13. Open Unknowns

See interview report § Open Unknowns (ASGI entry path, exact monorepo paths for OAS/pack in CI, physical multi-bundle store, numeric rate-limit defaults, channel OpenAPI file not yet created).
