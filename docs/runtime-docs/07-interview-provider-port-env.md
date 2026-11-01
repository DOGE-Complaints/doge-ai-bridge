# Interview provider port + env fail-closed (STORY-59 / adapters STORY-60 / REQ-12)

| Field | Value |
|-------|--------|
| **Story** | STORY-AIBRIDGE-59 · STORY-AIBRIDGE-60 |
| **AC** | AC-AIB-12-01 · AC-AIB-12-02 · AC-AIB-12-03 · AC-AIB-12-05 |
| **Arch** | [`req15-interview-providers/01-…`](../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) · [`02-adapters…`](../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) |
| **Code** | `src/aibridge/interview_providers/` · `config.py` · `app.py` wire · `readiness.py` |

## Selector (L12-1)

| Env | Rule |
|-----|------|
| `AIBRIDGE_INTERVIEW_PROVIDER` | **Required** ∈ {`deepseek`,`openai`} |
| unset / empty / unknown | **fail-closed** — no silent OpenAI; recording ≠ typed OK provider |

## Nest (L12-3)

| Provider | Required nest |
|----------|---------------|
| `openai` | `OPENAI_API_KEY` + `OPENAI_MODEL` (Keep §4) |
| `deepseek` | `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` · `_BASE_URL` · `_MODEL` |

## Orthogonality (AC-02)

`AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` **cannot** select interview. Worker registry stays under `src/aibridge/providers/`. Interview port home: `src/aibridge/interview_providers/` (**≠** `providers/`).

## Wire / start bind (D4)

Provider id is resolved **once** at `create_app` wire via `bind_interview_engine_at_wire` — **before** any Responses/recording fallback. No in-session flip API in v1.

| Id | Bind result |
|----|-------------|
| `openai` | Keep `ProductionResponsesClient` behind interview port |
| `deepseek` | `DeepSeekChatCompletionsClient` — Chat Completions + L12-3 nest (no silent OpenAI) |

## Trust

Channel Bearer / telegram must **not** carry model vendor keys. Auth path: `auth.is_channel_authorized` ↔ channel tokens only.

## /readyz reasons

| reason | When |
|--------|------|
| `interview_provider_missing` | unset/empty |
| `interview_provider_unknown` | not deepseek\|openai |
| `interview_provider_incomplete` | nest incomplete |

## OOS

- Stub/live evidence matrix → STORY-61
- Live Pass / model freeze beyond L12-2 orient
