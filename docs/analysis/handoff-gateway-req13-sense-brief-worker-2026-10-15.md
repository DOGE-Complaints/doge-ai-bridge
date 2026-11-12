# Handoff → gateway — REQ13 sense brief + civic poster worker (aibridge as-built)

| Field | Value |
|-------|--------|
| **UTC** | 2026-10-15T10:13:28Z |
| **From** | `doge-ai-bridge` REQ-09 / STORY-AIBRIDGE-46…50 |
| **To** | `doge-complaints-gateway` sibling REQ-57 / arch `issue-sense-brief-poster` |
| **Method** | [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) — claims from code path:line |
| **Purpose** | Contract for gateway to **nudge** aibridge and **receive bind-in** results |

---

## 1) Одной фразой

aibridge **Present**: отдельный worker accept (`POST /v1/worker/sense-brief/accept`, worker S2S) строит sense brief + civic poster, грузит HTTPS URL (aibridge-owned creds), и **клиентом** шлёт success/fail на `POST {GATEWAY_BASE_URL}/v1/issue-sense-brief/bind` с `GATEWAY_SERVICE_API_TOKEN`. Board SSOT остаётся на **gateway**. SPA не зовёт aibridge.

---

## 2) Roles

| Side | Owns | Must not |
|------|------|----------|
| **Gateway** | Issue pending/ready/failed; thin nudge; bind-in apply; public status/version/URL; regenerate bump | Run LLM/image; hold storage write keys (MVP) |
| **aibridge** | Accept + S2S; brief; poster; upload; outbound bind client | Own public board status; accept channel Bearer |

Gateway Wave-1 locks (interview): DP1–6 in [`issue-sense-brief-poster/00-overview.md`](../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md).

---

## 3) Nudge contract (gateway → aibridge)

| Item | As-built value |
|------|----------------|
| Method/path | `POST /v1/worker/sense-brief/accept` |
| Prefix | `/v1/worker/` (≠ `/v1/channel/`) |
| Auth header | `Authorization: Bearer <AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN>` |
| Reject | Channel Bearer, missing auth, citizen |
| Enable | Worker must have `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=true` + slots/creds or **503 fail-closed** |

### Request body

```json
{
  "issue_id": "<gateway Issue id>",
  "generation_version": "<string; bump on regenerate>",
  "corpus": { }
}
```

- `issue_id`, `generation_version` — **required** (minLength 1).  
- `corpus` — optional; Stories text/metadata for brief (insufficient → fail class `corpus_insufficient`).  
- Cite: `src/aibridge/worker_accept.py:25–32`.

### Idempotency

Same `(issue_id, generation_version)` → **200** with `idempotent: true` and prior outcome (no second LLM/image spend). In-process store on aibridge (not multi-replica). Cite: `WorkerIdempotencyStore` `worker_accept.py:48–69`.

### Success response (shape)

Includes `status`, `issue_id`, `generation_version`, `idempotent`, `pipeline` (e.g. `bind_ready`); may include `brief`, `poster_url`, `bind_outcome`. Cite: `accept_response_body` `worker_accept.py:103–119`.

OpenAPI: [`../openapi/aibridge-worker-sense-brief-v1.openapi.yaml`](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml).

---

## 4) Bind-in contract (aibridge → gateway)

aibridge **calls** (gateway must **serve**):

| Item | As-built value |
|------|----------------|
| URL | `{GATEWAY_BASE_URL}/v1/issue-sense-brief/bind` |
| Method | `POST` |
| Auth | `Authorization: Bearer <GATEWAY_SERVICE_API_TOKEN>` |
| Must not | Channel Bearer / worker S2S as bind auth |

Cite: `sense_bind/client.py:32`, `:59–88`.

### Success body

```json
{
  "issue_id": "...",
  "generation_version": "...",
  "outcome": "success",
  "poster_url": "https://...",
  "apply": {
    "title": "...",
    "summary": { "et": "...", "ru": "...", "en": "..." }
  }
}
```

Cite: `sense_bind/payload.py:31–40`. Gateway applies title/summary; sets ready + URL + version (per DP1/DP4).

### Failure body

```json
{
  "issue_id": "...",
  "generation_version": "...",
  "outcome": "failure",
  "reason_class": "corpus_insufficient"
}
```

**Never** includes `brief` / `apply`. Cite: `sense_bind/payload.py:55–64`.

### `reason_class` values (aibridge wire)

| Class | Meaning |
|-------|---------|
| `accept_unauthorized` | Usually pre-bind |
| `corpus_insufficient` | Honest brief impossible |
| `brief_generation_failed` | Text slot/policy abort |
| `image_generation_failed` | Image slot |
| `storage_upload_failed` | Upload/URL |
| `bind_rejected` | Gateway non-2xx / reject |
| `internal_error` | Unexpected |

Cite: `sense_bind/errors.py:8–17`.

---

## 5) What gateway still needs (sibling work)

| Item | Status |
|------|--------|
| Wave-1 DP1–6 product locks | Locked in gateway arch interview |
| HTTP bind **receiver** at `/v1/issue-sense-brief/bind` | **Implement** (aibridge client already posts here) |
| Thin nudge client to aibridge accept URL + worker S2S | **Implement** |
| Public Issue wire keys (status/version/URL) | Residual Open on gateway |
| Sweep/cron re-nudge | Per gateway DP2 |
| Manual regenerate (service token) → version bump | Per gateway DP6 |

Do **not** invent SPA↔aibridge calls. Do **not** require gateway storage write keys for MVP.

---

## 6) Env checklist

### aibridge

| Variable | Role |
|----------|------|
| `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` | Enable worker |
| `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` | Accept auth (share with gateway nudge) |
| `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` | LLM slot |
| `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` | Image slot |
| `AIBRIDGE_WORKER_STORAGE_UPLOAD_CREDENTIAL` | Upload cred |
| `GATEWAY_BASE_URL` | HTTPS origin for bind |
| `GATEWAY_SERVICE_API_TOKEN` | Bind auth |

### gateway (expected)

| Variable | Role |
|----------|------|
| Worker nudge base URL | aibridge origin + accept path |
| Worker S2S token | Same secret as aibridge worker S2S |
| Service token for bind-in receive | Align with `GATEWAY_SERVICE_API_TOKEN` peer model |

Exact gateway env **names** — gateway package Open until frozen.

---

## 7) Verify pointers

| Proof | Location |
|-------|----------|
| Code validation | [`zeya888.req-09-stories-46-50-code-validation-2026-10-15.md`](./zeya888.req-09-stories-46-50-code-validation-2026-10-15.md) |
| Test matrix | [`zeya888.req-09-test-coverage-unit-integration-e2e-2026-10-15.md`](./zeya888.req-09-test-coverage-unit-integration-e2e-2026-10-15.md) |
| Isolation suite | `doge-ai-bridge/tests/test_worker_isolation_harness_story_50.py` — **48** story tests passed 2026-10-15 |
| Live E2E | Optional ops (DP8) — not aibridge merge gate |

---

## 8) Links

| Artifact | Path |
|----------|------|
| REQ-09 | [`../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| aibridge arch | [`../architecture/sense-brief-poster-worker/00-overview.md`](../architecture/sense-brief-poster-worker/00-overview.md) |
| gateway arch | [`../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md`](../../../doge-complaints-gateway/docs/architecture/issue-sense-brief-poster/00-overview.md) |
| gateway REQ-57 | [`../../../doge-complaints-gateway/docs/requirements/57-req13-issue-sense-brief-poster-projection.md`](../../../doge-complaints-gateway/docs/requirements/57-req13-issue-sense-brief-poster-projection.md) |
| Worker OpenAPI | [`../openapi/aibridge-worker-sense-brief-v1.openapi.yaml`](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml) |
| Runtime API | [`../runtime-docs/01-api.md`](../runtime-docs/01-api.md) |
| Code entry | `src/aibridge/app.py` (`worker_sense_brief_accept`) · `sense_bind/client.py` |
