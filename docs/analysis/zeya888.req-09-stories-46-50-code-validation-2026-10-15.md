# REQ-09 stories 46–50 — code validation vs as-built

| Field | Value |
|-------|--------|
| **UTC** | 2026-10-15T10:13:28Z (`builder_resolve_queue.py --print-utc-now`) |
| **Method** | [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) |
| **Parent REQ** | [`../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Package** | [`../tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md`](../tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md) |
| **Arch** | [`../architecture/sense-brief-poster-worker/00-overview.md`](../architecture/sense-brief-poster-worker/00-overview.md) |
| **Pytest** | `.venv/bin/python -m pytest` story suite → **48 passed** (2026-10-15) |

**Scope:** validate AC-09 / story Scope against **code** (path:line). Not P7/P8 process close.

**Package process note (INDEX):** 46–48 P8 Done; 49 P5 Done · next P7; 50 P6 Done · next P7.

---

## Verdict (summary)

| Story | Code AC | Notes |
|-------|---------|-------|
| STORY-46 | **PASS** | Separate entry, S2S, idempotency Present |
| STORY-47 | **PASS** | L2 model, dedicated prompts, no-invent, text slot |
| STORY-48 | **PASS** | Poster + credential-gated HTTPS upload (mock mint OK for CI) |
| STORY-49 | **PASS** (aibridge client) | Bind client + payloads Present; gateway **receiver** is sibling OOS |
| STORY-50 | **PASS** | Isolation harness maps AC-09-01…06 |

**Package code verdict:** REQ-09 worker path is **Present** and AC-covered under isolation tests. Residual: live vendor/bucket/gateway E2E (DP8 ops); multi-replica idempotency; gateway bind receiver + public wire (sibling 57).

---

## AC matrix (code cites)

| AC | Criterion | Evidence | Result |
|----|-----------|----------|--------|
| AC-09-01 | Worker ≠ channel entry | `WORKER_PATH_PREFIX` / `WORKER_ACCEPT_PATH` — `worker_accept.py:21–22`; `CHANNEL_PATH_PREFIX` — `app.py:57`; route `@app.post(WORKER_ACCEPT_PATH)` — `app.py:684–685` | **PASS** |
| AC-09-01 auth | Channel Bearer rejected | `is_worker_s2s_authorized` rejects channel tokens — `auth.py:45–58`; middleware — `app.py:566–626` | **PASS** |
| AC-09-02 | Brief title≤80 + summary et/ru/en | `SenseBrief` / `satisfies_l2` — `sense_brief/model.py:21–50` | **PASS** |
| AC-09-03 | Public HTTPS poster URL | `CredentialGatedUploader` requires `https://` — `poster/storage.py:44–71`; accept stores `poster_url` — `app.py:781–832` | **PASS** |
| AC-09-04 | Explicit fail to gateway, no fake brief | `build_fail_bind_payload` + guard — `sense_bind/payload.py:43–71`; accept `_fail_bind` — `app.py:738–766` | **PASS** |
| AC-09-05 | EN prompts; no invented facts | Dedicated `sense_brief/prompts.py`; pipeline refuse invent — `sense_brief/pipeline.py` (tests `test_t04_refuse_invented_civic_facts`) | **PASS** |
| AC-09-06 | Regenerated version/URL distinguishable | `regenerate_assets_distinguishable` — `sense_bind/version.py:24–34`; idempotency same version — `WorkerIdempotencyStore.accept` — `worker_accept.py:54–69` | **PASS** |

---

## Per-story validation

### STORY-46 — entry / S2S / idempotency

| Check | Cite | Result |
|-------|------|--------|
| Separate path | `worker_accept.py:21–22` vs `app.py:57` | PASS |
| Enable + S2S env | `config.py:197–204`, fail-closed `297–301` | PASS |
| Middleware ≠ channel | `app.py:566–626` | PASS |
| Accept body | `issue_id`, `generation_version`, optional `corpus` — `worker_accept.py:25–32` | PASS |
| Idempotency | `WorkerIdempotencyStore` in-process — `worker_accept.py:48–69`; wired `app.py:723–728` | PASS |

**Gap:** idempotency store is **in-process** (not shared across replicas). Documented residual — not AC fail for MVP isolation.

### STORY-47 — brief / prompts / policy

| Check | Cite | Result |
|-------|------|--------|
| L2 keys | `sense_brief/model.py:1–33` | PASS |
| text-brief slot | `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` — `config.py:206–209`; fail-closed `303–307` | PASS |
| Pipeline + classes | `generate_sense_brief` — `sense_brief/pipeline.py:102+`; `BriefFailureClass` — `sense_brief/errors.py:8–12` | PASS |

### STORY-48 — poster / storage

| Check | Cite | Result |
|-------|------|--------|
| image-poster slot | `config.py:212–215`, fail-closed `317–321` | PASS |
| Storage cred gate | `config.py:216–219`, `323–327`; `CredentialGatedUploader` — `poster/storage.py:44–71` | PASS |
| Mockable port | `PosterUploadPort` / `MockHttpsUploader` — `poster/port.py`, `storage.py:19–41` | PASS |

**Gap:** default uploader mints `https://aibridge-poster.test/objects/…` (`storage.py:16–17`) — CI/fixture path, **not** production CDN SSOT. Live bucket provider remains residual Open.

### STORY-49 — bind / fail / version

| Check | Cite | Result |
|-------|------|--------|
| Bind path (client) | `BIND_PATH = "/v1/issue-sense-brief/bind"` — `sense_bind/client.py:32` | PASS (aibridge implement) |
| Service-auth only | `authorization_header` + domain assert — `sense_bind/client.py:59–88` | PASS |
| Success payload | `issue_id`, `generation_version`, `outcome`, `poster_url`, `apply` — `payload.py:31–40` | PASS |
| Fail payload | `reason_class`, no brief/apply — `payload.py:55–64` | PASS |
| DP9 classes | `BindFailureClass` — `sense_bind/errors.py:8–17` | PASS |

**Gap:** gateway **HTTP receiver** for bind path is **out of this package** (sibling 57). aibridge client may POST to a not-yet-Present gateway route in live deploy until Wave-1 implement lands.

### STORY-50 — isolation harness

| Check | Cite | Result |
|-------|------|--------|
| Harness | `tests/harness/sense_brief_isolation.py` | PASS |
| AC tests | `tests/test_worker_isolation_harness_story_50.py` — `test_ac_09_01`…`test_ac_09_06` | PASS |
| No live vendor required | DP8; suite green without OpenAI/bucket secrets | PASS |

---

## Gaps / residuals (honest)

1. **Multi-replica idempotency** — in-memory store only.  
2. **Live storage/CDN** — mock HTTPS mint for default/CI; real provider Open.  
3. **Live LLM/image models** — env slots Present; concrete model IDs ops residual.  
4. **Gateway bind receiver + public wire** — sibling 57; aibridge client path chosen unilaterally until joint freeze.  
5. **Process:** stories 49/50 not P8 Done on package INDEX (next P7) — code still AC-green under isolation.

---

## Related

- Test report: [`zeya888.req-09-test-coverage-unit-integration-e2e-2026-10-15.md`](./zeya888.req-09-test-coverage-unit-integration-e2e-2026-10-15.md)  
- Gateway handoff: [`handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](./handoff-gateway-req13-sense-brief-worker-2026-10-15.md)  
