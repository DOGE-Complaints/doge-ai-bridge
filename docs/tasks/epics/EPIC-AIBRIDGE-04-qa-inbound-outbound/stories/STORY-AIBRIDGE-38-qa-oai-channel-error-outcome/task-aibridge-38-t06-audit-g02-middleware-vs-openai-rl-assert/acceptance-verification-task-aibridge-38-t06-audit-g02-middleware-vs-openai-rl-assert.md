# Acceptance verification — task-aibridge-38-t06-audit-g02-middleware-vs-openai-rl-assert

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-18T13:56:16Z |
| **Story** | STORY-AIBRIDGE-38-qa-oai-channel-error-outcome |
| **Wave** | `run_mode=aibridge_38_audit_20260918` · P6 |
| **Gap** | G-02 |

## AC check

- [x] Suite asserts distinct OpenAI vs middleware RL messages (`OpenAI rate limited` ≠ `Rate limit exceeded`).
- [x] Existing Option A 429 channel asserts remain green.
- [x] No invent gateway / live TG.
- [x] `Skill declared: test-master` present.

## Evidence

```text
.venv/bin/python -m pytest tests/integration/test_openai_prompt_behavior.py -q
→ 22 passed
test_oai_008_*message* + test_oai_008_middleware_vs_openai_rate_limited_message_discriminator
app.py: middleware "Rate limit exceeded" · handler "OpenAI rate limited"
```
