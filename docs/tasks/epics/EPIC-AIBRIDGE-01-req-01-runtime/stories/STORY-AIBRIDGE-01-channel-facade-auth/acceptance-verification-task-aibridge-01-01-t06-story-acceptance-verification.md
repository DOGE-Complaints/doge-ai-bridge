# Story acceptance gate — STORY-AIBRIDGE-01-channel-facade-auth

- **Story:** Channel façade + Bearer + event dedupe
- **Package:** `pkg-000001-20260912-epic-aibridge-01-story-01-channel-facade.yaml`
- **Result:** PASS
- **Date:** 2026-09-12T20:35:41Z (story AC gate)
- **P6 residual note:** G-01/G-02 closed 2026-09-12T20:43:28Z — see t07/t08 acceptance; pytest **22 passed**

## AC checklist (verbatim from backlog / pipeline story)

| AC | Status | Evidence |
|----|--------|----------|
| Unauthenticated `/v1/channel/*` → 401. | PASS | `tests/test_auth.py`; `src/aibridge/app.py` channel middleware |
| Valid Bearer + turn request → 200 envelope fields per channel OAS (no `callback_ack_text`). | PASS | `tests/test_channel.py`; `src/aibridge/schemas.py` ChannelSuccessResponse |
| Duplicate `event_id` → same stored response; no second side-effect path. | PASS | `tests/test_dedupe.py`; `src/aibridge/dedupe.py` get_or_create |
| Contract tests: request/response vs committed channel OAS. | PASS | `tests/test_contract_oas.py` vs `docs/openapi/aibridge-channel-v1.openapi.yaml` |
| Equal channel/gateway Bearer when both configured → readiness fail (REQ-01 §7 / §18). | PASS | `tests/test_auth.py::test_equal_channel_gateway_bearer_readyz_fail`; `src/aibridge/app.py` readyz |
| Task README after P1.3 includes `Skill declared: python-pro`. | PASS | all `task-aibridge-01-01-t0*/README.md` |

## Commands (live verification 2026-09-12)

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
cd doge-ai-bridge && .venv/bin/pytest -q
# → 21 passed
```

SSOT дат: [`guides/builder-artifact-dates.md`](../../../../../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md)
