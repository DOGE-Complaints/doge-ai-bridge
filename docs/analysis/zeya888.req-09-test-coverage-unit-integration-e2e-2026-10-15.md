# REQ-09 — test coverage: unit / integration / e2e

| Field | Value |
|-------|--------|
| **UTC** | 2026-10-15T10:13:28Z |
| **Method** | [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc) |
| **Suite command** | `cd doge-ai-bridge && .venv/bin/python -m pytest tests/test_worker_accept_story_46.py tests/test_sense_brief_story_47.py tests/test_poster_storage_story_48.py tests/test_sense_bind_story_49.py tests/test_worker_isolation_harness_story_50.py -q` |
| **Result** | **48 passed**, 2 warnings (Starlette TestClient deprecation) |
| **Arch verify lock** | DP8 — contract + isolation harness; live vendor smoke = optional ops ([`03-storage-bind-verify.md`](../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)) |
| **Code validation** | [`zeya888.req-09-stories-46-50-code-validation-2026-10-15.md`](./zeya888.req-09-stories-46-50-code-validation-2026-10-15.md) |

---

## 1) Executive verdict

| Layer | Status | Evidence |
|-------|--------|----------|
| **Unit** | **Present / adequate** for models, payloads, ports, prompts, version helpers | Direct asserts in story test modules |
| **Integration (ASGI + mocks)** | **Present / adequate** for accept auth, fail-closed, brief→poster→bind dry-run | FastAPI `TestClient` against `create_app` |
| **Isolation harness (AC package gate)** | **Present / PASS** | STORY-50 maps AC-09-01…06 |
| **E2E / live** (real LLM + bucket + gateway receiver) | **Absent by design** (DP8) | No CI secrets; ops residual |

**Merge-gate recommendation:** keep isolation + story suites as Done gate. Do **not** require live OpenAI/bucket/Railway for package merge.

---

## 2) Inventory by file

### `tests/test_worker_accept_story_46.py` (STORY-46)

| Test | Layer | Maps |
|------|-------|------|
| `test_accept_path_is_not_channel_prefix` | unit | AC-09-01 / T02 |
| `test_channel_bearer_rejected_on_worker_accept` | integration | AC-09-01 / T03 |
| `test_missing_auth_rejected` | integration | T03 |
| `test_valid_worker_s2s_admits_accept` | integration | T03 |
| `test_same_version_idempotent_no_second_create` | integration | AC-09-06 / T05 |
| `test_new_generation_version_allows_new_work` | integration | T05 |
| `test_enabled_missing_s2s_fail_closed_accept` | integration | T01 |
| `test_enabled_missing_s2s_fail_closed_readyz` | integration | T01 |
| `test_worker_disabled_returns_503` | integration | T01 |
| `test_gateway_token_not_worker_s2s` | unit/integration | T03 trust |
| `test_channel_eq_worker_s2s_still_rejected` | integration | T03 |

### `tests/test_sense_brief_story_47.py` (STORY-47)

| Test | Layer | Maps |
|------|-------|------|
| `test_t01_golden_l2_model_satisfies_ac` | unit | AC-09-02 / T01 |
| `test_t02_dedicated_prompts_not_interview_ssot` | unit | AC-09-05 / T02 |
| `test_t03_text_brief_slot_fail_closed_accept` | integration | T03 |
| `test_t03_text_brief_slot_fail_closed_readyz` | integration | T03 |
| `test_t04_corpus_insufficient_no_fake_brief` | unit | AC-09-04/05 / T04–T05 |
| `test_t04_refuse_invented_civic_facts` | unit | AC-09-05 / T04 |
| `test_t04_accept_returns_brief_without_interview_engine` | integration | T04 |
| `test_t05_accept_surfaces_corpus_insufficient_class` | integration | T05 |
| `test_t06_pii_safe_logging_no_corpus_body` | unit | REQ §4.6 |

Fixtures: `tests/fixtures/sense_brief_golden_l2.json`, `sense_brief_insufficient.json`.

### `tests/test_poster_storage_story_48.py` (STORY-48)

| Test | Layer | Maps |
|------|-------|------|
| `test_t01_image_poster_slot_fail_closed_accept` | integration | T01 |
| `test_t01_image_poster_slot_fail_closed_readyz` | integration | T01 |
| `test_t02_poster_bytes_from_brief_not_interview` | unit | T02 |
| `test_t02_image_slot_unset_raises_class` | unit | T01/T04 |
| `test_t03_storage_creds_fail_closed_readyz` | integration | T03 |
| `test_t03_missing_creds_upload_fail_class` | unit | T03/T04 |
| `test_t04_mock_upload_yields_https_url` | unit | AC-09-03 / T04 |
| `test_t05_mockable_upload_port_injectable` | unit | T05 |
| `test_t06_accept_returns_poster_https_url` | integration | AC-09-03 |
| `test_t06_default_uploader_uses_aibridge_creds_only` | unit | T03 |

### `tests/test_sense_bind_story_49.py` (STORY-49)

| Test | Layer | Maps |
|------|-------|------|
| `test_t01_bind_uses_gateway_service_auth_not_channel_or_worker` | unit | T01 |
| `test_t01_refuse_when_gateway_equals_channel` | unit | T01 |
| `test_t02_success_payload_has_apply_url_version` | unit | T02 / AC-09-03 payload |
| `test_t03_fail_payload_no_fake_brief` | unit | AC-09-04 / T03 |
| `test_t04_regenerate_versions_distinguishable` | unit | AC-09-06 / T04 |
| `test_t05_pii_safe_bind_logging` | unit | T05 |
| `test_t06_mock_gateway_reject_maps_bind_rejected` | unit/integration | T06 |
| `test_t06_accept_bind_ready_dry_run` | integration | T01–T02 |
| `test_t06_accept_fail_bind_on_corpus_insufficient` | integration | AC-09-04 |
| `test_t06_two_versions_distinguishable_on_accept` | integration | AC-09-06 |
| `test_client_from_settings_wires_tokens` | unit | T01 |

### `tests/test_worker_isolation_harness_story_50.py` + `tests/harness/sense_brief_isolation.py`

| Test | Layer | Maps |
|------|-------|------|
| `test_t01_harness_runs_without_live_vendor_secrets` | isolation | T01 / DP8 |
| `test_ac_09_01_channel_bearer_rejected_on_accept` | isolation | AC-09-01 |
| `test_ac_09_02_logical_l2_brief_shape` | isolation | AC-09-02 |
| `test_ac_09_03_upload_mock_returns_https_url` | isolation | AC-09-03 |
| `test_ac_09_04_fail_bind_reason_class_no_fake_brief` | isolation | AC-09-04 |
| `test_ac_09_05_prompt_isolation_and_invent_refusal` | isolation | AC-09-05 |
| `test_ac_09_06_idempotent_same_version_and_bump_distinguishable` | isolation | AC-09-06 |

---

## 3) Coverage vs AC-09 checklist

| AC | Unit | Integration | Isolation harness | Live E2E |
|----|------|-------------|-------------------|----------|
| AC-09-01 | yes (path constants) | yes (Bearer reject/admit) | yes | no (N/A) |
| AC-09-02 | yes (model/golden) | yes (accept returns brief) | yes | no |
| AC-09-03 | yes (mock HTTPS) | yes (accept poster_url) | yes | no (live bucket Absent) |
| AC-09-04 | yes (fail payload) | yes (fail bind dry-run) | yes | no (live gateway Absent) |
| AC-09-05 | yes (prompts/invent) | yes | yes | no |
| AC-09-06 | yes (version helpers) | yes (idempotent + bump) | yes | no |

---

## 4) Gaps vs broader testing standards

| Standard expectation | This package | Assessment |
|----------------------|--------------|------------|
| Unit tests for pure logic | Present | **OK** |
| Integration tests for HTTP surface | Present (TestClient) | **OK** |
| Contract / OpenAPI schema tests | **Absent** at validation time (OpenAPI worker added in same docs wave) | Follow-up: optional schemathesis/openapi check later |
| Multi-process / shared idempotency | **Absent** (in-memory store) | Residual — call out for ops scale |
| E2E live LLM + image + bucket + gateway bind | **Absent** | **Intentional** DP8; ops residual |
| Chaos / load | Absent | OOS for Wave-2 MVP |
| SPA E2E | Absent | OOS (sibling 23; no SPA↔aibridge) |

---

## 5) Recommendations

1. **CI merge gate:** run the five story modules + harness (or package marker) — already green (48).  
2. **Do not** block Done on live OpenAI/bucket/Railway for this package.  
3. After gateway bind receiver lands: add **cross-service contract test** (or recorded HTTP) in gateway or joint suite — outside REQ-09 aibridge scope.  
4. When production storage is chosen: one **ops smoke** checklist (optional), not CI hard gate.  
5. Optionally add OpenAPI request/response shape tests once [`aibridge-worker-sense-brief-v1.openapi.yaml`](../openapi/aibridge-worker-sense-brief-v1.openapi.yaml) is linked.

---

## 6) Related

- Code validation: [`zeya888.req-09-stories-46-50-code-validation-2026-10-15.md`](./zeya888.req-09-stories-46-50-code-validation-2026-10-15.md)  
- Gateway handoff: [`handoff-gateway-req13-sense-brief-worker-2026-10-15.md`](./handoff-gateway-req13-sense-brief-worker-2026-10-15.md)  
