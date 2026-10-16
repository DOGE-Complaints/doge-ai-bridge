# Provider verify matrix (REQ-10)

Maps arch [`03-verify-coexistence.md`](../architecture/ai-provider-selection/03-verify-coexistence.md) surfaces → **Present** pytest files.  
No gateway board e2e as aibridge DoD. Live OpenAI SUCCESS residual = **Unknown** unless ops proves.

| Surface | AC / note | Evidence (tests) |
|---------|-----------|------------------|
| Unit — ports | AC-10-01/02/05 · defaults mock · unknown refuse | `tests/test_provider_ports_story_51.py` |
| Readyz matrix | AC-10-08/09 · allow-mock · slot-gated OpenAI | `tests/test_readyz_allow_mock_story_53.py` |
| Worker-accept smoke | AC-10-03/06 · mock+mock no live HTTP | `tests/test_mock_accept_pipe_story_52.py` |
| No silent openai | AC-10-05 · provider≠openai | `tests/test_openai_text_live_story_54.py` · `test_no_silent_openai_when_text_is_mock` |
| OpenAI text (mocked) | AC-10-04/10 · residual live SUCCESS Unknown | `tests/test_openai_text_live_story_54.py` |
| Consolidated matrix | STORY-55 entry | `tests/test_provider_verify_matrix_story_55.py` |

## Ops residual (cite only)

| Item | Status |
|------|--------|
| Live OpenAI text SUCCESS (real network/key) | Unknown — do not invent |
| Gateway REQ-58 board / Railway public | OOS aibridge · ops/gateway |
| Live image vendor | Deferred NI |

## CI command

```bash
cd doge-ai-bridge
DATABASE_URL= AIBRIDGE_ALLOW_MEMORY_STORES=true \
  .venv/bin/python -m pytest \
  tests/test_provider_verify_matrix_story_55.py \
  tests/test_provider_ports_story_51.py \
  tests/test_mock_accept_pipe_story_52.py \
  tests/test_readyz_allow_mock_story_53.py \
  tests/test_openai_text_live_story_54.py \
  -q
```
