# STORY-AIBRIDGE-60 — OpenAI + DeepSeek interview adapters

## Meta
- **Key:** `STORY-AIBRIDGE-60-openai-deepseek-interview-adapters`
- **Status:** Done · Product Done · pkg-000063 · P8 2026-11-01T21:12:55Z · next **STORY-61** · [p7](../../analysis/p7-reaudit-STORY-AIBRIDGE-60-openai-deepseek-interview-adapters-20261101.md)
- **Parent REQ:** [`REQ-12`](../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) §§2–4 · AC-03 · L12-2 · L12-3 · T1 Keep/Replace
- **Tech-arch:** [`req15-interview-providers/02-adapters-openai-deepseek.md`](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [59](STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) · [61](STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-01T19:38:04Z
- **Tech subtasks:** Present (arch-bound; pre-P1.3)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- OpenAI adapter: Keep Present Responses path (`ProductionResponsesClient`) behind interview port → Keep `InterviewEngine` (budgets/tools/history).
- DeepSeek adapter: new Chat Completions + `base_url` from `AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL`; auth via `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY`; model via `AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL`; same narrow client/turn surface for Engine.
- **No** silent fallback to OpenAI when `deepseek` selected.
- Usage/error classes: config/fail-closed vs vendor/transport (literals Open — typed classes only).
- Model id: L12-2 not frozen for live Pass; orient / example `deepseek-v4-pro`.

## Out of scope
- Port/env SSOT (59); evidence gates doc/live calendar (61).
- Worker brief/poster adapters; replace InterviewEngine; grant gateway permission via adapter.
- Fine-tunes / hosted agent platforms.

## Verified current state
- OpenAI Responses / interview slot: `src/aibridge/interview_providers/openai_slot.py` → Keep `ProductionResponsesClient` (`responses_client.py:327+`); wire via `bind_interview_engine_at_wire`.
- DeepSeek interview adapter: **Present** — `src/aibridge/interview_providers/deepseek_slot.py` (`DeepSeekChatCompletionsClient` · Chat Completions + L12-3 nest). As-of-Done STORY-60 P3/P6; live Pass remains OOS **STORY-61** (G-02 WAIVED).
- Worker `providers/` Present — must stay orthogonal (≠ `interview_providers/`).
- Env names L12-3 Present in REQ + [`.env.example`](../../../../.env.example) §4b.

## Target / AC
- [x] AC-AIB-12-03: both adapters produce usable role/engine outcomes under harness (fixtures).
- [x] Keep Engine; port supplies backend only (arch D3).
- [x] No silent OpenAI when DeepSeek selected (REQ §4.3).
- [x] DeepSeek adapter reads only L12-3 nest vars (not worker env).

## Code points
- `interview.py` · `responses_client.py:327+` · `app.py` interview wire · `interview_providers/{openai_slot,deepseek_slot,errors,registry}.py`
- DeepSeek adapter: **Present** under `interview_providers/` (≠ `providers/`)

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | OpenAI adapter Keep: `ProductionResponsesClient` behind port → Engine | [`02` §1](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) | AC-AIB-12-03 openai | `responses_client.py:327+` · `app.py:418–426` | Fake Completions unification | Done |
| **t02** | DeepSeek adapter new: Chat Completions + `BASE_URL` / key / model from L12-3 | [`02` §2](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) | AC-AIB-12-03 deepseek | `deepseek_slot.py` Present · L12-3 env | Freeze model beyond L12-2 orient | Done |
| **t03** | Same narrow client/turn surface; Keep `InterviewEngine` (D3) | [`02` §2 Contract](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) · [`00` D3](../../../architecture/req15-interview-providers/00-overview.md) | D3 | `interview.py` | Replace InterviewEngine | Done |
| **t04** | No silent fallback to OpenAI when provider=`deepseek` | [`02` §2](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) · REQ §4.3 | AC-03 / §4.3 | Port resolve + DeepSeek path | Silent OpenAI fallback | Done |
| **t05** | Error classes: config/fail-closed vs vendor/transport (literals Open) | [`02` §3](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) | typed classes | Adapter error map | Fail-reason string SSOT | Done |
| **t06** | Module home ≠ `src/aibridge/providers/`; HTTP helper reuse OK without worker ids | [`02` §4](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) | AC-02 boundary | New interview package path at implement | Merge worker registry | Done |
| **t07** | Adapter must not grant gateway/Send permission (REQ-11 Keep) | [`02` §1](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) tool-intent · [`00` §5](../../../architecture/req15-interview-providers/00-overview.md) | coexistence | Confirm/tool-intent Keep | Gateway redesign | Done |
| **t08** | Story gate: both adapters usable under harness fixtures | [`00-overview`](../../../architecture/req15-interview-providers/00-overview.md) · AC-03 | Package gate for 60 | After t01–t07 | Live Pass (61) | **PASS** |

## Dependencies
- STORY-AIBRIDGE-59
- Soft: L12-2 live model confirm before claiming live Pass (61)
