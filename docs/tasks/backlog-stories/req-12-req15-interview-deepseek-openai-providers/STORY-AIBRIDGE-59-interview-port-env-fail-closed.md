# STORY-AIBRIDGE-59 — Interview port + env fail-closed

## Meta
- **Key:** `STORY-AIBRIDGE-59-interview-port-env-fail-closed`
- **Status:** **Done** · Product Done · pkg-000062 · P8 2026-11-01T20:47:36Z · G-01 WAIVED · next **STORY-60** · [pipeline](../../epics/EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers/stories/STORY-AIBRIDGE-59-interview-port-env-fail-closed/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md)
- **Parent REQ:** [`REQ-12`](../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) §§2,4.1–3,5 AC-01/02/05 · L12-1 · L12-3
- **Tech-arch:** [`req15-interview-providers/01-interview-port-env-fail-closed.md`](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [60](STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) · [61](STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-01T19:38:04Z
- **Tech subtasks:** Present (arch-bound; pre-P1.3)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Env `AIBRIDGE_INTERVIEW_PROVIDER` ∈ {`deepseek`,`openai`} — **required**; unset/unknown/empty → fail-closed (arch D2).
- Nest SSOT (L12-3): when `deepseek` → require `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` · `AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL` · `AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL`; when `openai` → Keep `OPENAI_API_KEY` + `OPENAI_MODEL`.
- Shared interview provider port/registry for channel wire today and future REQ-13 roles (logical; package ≠ worker `providers/`).
- Prove `AIBRIDGE_WORKER_*_PROVIDER` cannot select interview (AC-02).
- Transition: deploy sets `openai` explicitly — no silent OpenAI when unset; recording ≠ substitute for missing provider.
- v1: provider bound at wire/start only (arch D4) — document; no in-session flip API.

## Out of scope
- DeepSeek/OpenAI adapter bodies (60); stub/live evidence matrix (61).
- Worker REQ-10 registry changes; GPT-48; telegram; gateway stash; mid-session flip implement.

## Verified current state (P3)
- Wire: `bind_interview_engine_at_wire` · port `src/aibridge/interview_providers/` ≠ `providers/`.
- Settings L12-1/L12-3 Present · `/readyz` reasons `interview_provider_*` · runtime-docs/07.
- DeepSeek adapter HTTP: Deferred OOS-60 · suite **608 passed**.

## Target / AC
- [x] AC-AIB-12-01: config selects `deepseek` \| `openai` for interview only.
- [x] AC-AIB-12-02: worker REQ-10 env cannot act as interview switch.
- [x] AC-AIB-12-05: unknown/incomplete provider config (incl. incomplete DeepSeek nest) → fail-closed.
- [x] Wire/start binding only (D4) documented in harness/docs note.
- [x] Settings load L12-1 + L12-3 names from env (match `.env.example` §4b).

## Code points
- `src/aibridge/app.py:414–428` · `interview.py` · `config.py` (add interview settings; cite worker env for orthogonality)
- New interview port/registry home under `src/aibridge/` — path chosen at implement; **must not** merge into `providers/`

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Settings: load `AIBRIDGE_INTERVIEW_PROVIDER` ∈ {`deepseek`,`openai`}; required | [`01` §1](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) L12-1 | AC-AIB-12-01 | `config.py` · [`.env.example`](../../../../.env.example) §4b | Adapter bodies (60) | Done |
| **t02** | Nest L12-3: deepseek → three `AIBRIDGE_INTERVIEW_DEEPSEEK_*`; openai → Keep `OPENAI_API_KEY`+`OPENAI_MODEL` | [`01` §1](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) · [`01` §3](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) | AC-AIB-12-05 nest | `config.py` · Present `OPENAI_*` | Invent alternate env names | Done |
| **t03** | Fail-closed unset/unknown/empty; recording ≠ typed OK provider | [`01` §1](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) D2 · [`03` §3](../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md) | AC-AIB-12-05 | `app.py` wire · `interview_providers/` | Fail-reason string SSOT | Done |
| **t04** | Orthogonality: `AIBRIDGE_WORKER_*_PROVIDER` cannot select interview | [`01` Forbidden](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) · AC-02 | AC-AIB-12-02 | `config.py` · `providers/` cite | Worker REQ-10 registry changes | Done |
| **t05** | Logical InterviewProviderPort + registry (map id→backend slot); home ≠ `providers/` | [`01` §2](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) · [`02` §4](../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) | AC-01 support | `src/aibridge/interview_providers/` | Merge into `providers/` · adapter bodies (60) | Done |
| **t06** | Wire/start bind only (D4); `app.py` Adapt: fail-closed **before** Responses/recording | [`01` D4](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) · [`00` §5](../../../architecture/req15-interview-providers/00-overview.md) | D4 | `app.py` · `bind_interview_engine_at_wire` | Mid-session flip API | Done |
| **t07** | Trust: channel Bearer / telegram must not carry model keys | [`01` §4](../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) · [`00` §3](../../../architecture/req15-interview-providers/00-overview.md) | ownership | `auth.py` · runtime-docs/07 | telegram transport implement | Done |
| **t08** | Story gate: AC-01/02/05 stub-ready; OOS adapters/evidence | [`00-overview`](../../../architecture/req15-interview-providers/00-overview.md) | Package gate for 59 | After t01–t07 | 60/61 scopes | **PASS** |

## Dependencies
- Soft: tech-arch `req15-interview-providers/` Present · L12-3 locked
