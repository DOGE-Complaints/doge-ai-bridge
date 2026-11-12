# STORY-AIBRIDGE-59 — Interview port + env fail-closed

## Meta
- **Key:** `STORY-AIBRIDGE-59-interview-port-env-fail-closed`
- **Status:** **Done** · Product Done · pkg-000062 · P8 2026-11-01T20:47:36Z · G-01 WAIVED · next **STORY-60**
- **Parent Epic:** [`EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers.md`](../../EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers.md)
- **source:** `backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md`
- **decision_ref:** [`STORY-AIBRIDGE-59-interview-port-env-fail-closed.md`](../../../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) · [`REQ-12`](../../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) · [`01-interview-port-env-fail-closed.md`](../../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md)
- **Package:** [`req-12-req15-interview-deepseek-openai-providers/INDEX.md`](../../../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000062-20261101-epic-aibridge-10-story-59-interview-port-env-fail-closed.yaml`
- **P1 materialize:** 2026-11-01T20:23:26Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_59_scaffold_20261101T202103Z.plan.md)
- **Depends:** soft tech-arch `req15-interview-providers/` Present · L12-3 locked
- **OOS:** STORY-60 adapters · STORY-61 evidence

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Port / env fail-closed | [`01-interview-port-env-fail-closed.md`](../../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) |
| Arch overview | [`00-overview.md`](../../../../architecture/req15-interview-providers/00-overview.md) |
| Env template | [`.env.example`](../../../../../.env.example) §4b |

## Scope
- Env `AIBRIDGE_INTERVIEW_PROVIDER` ∈ {`deepseek`,`openai`} — **required**; unset/unknown/empty → fail-closed (arch D2).
- Nest SSOT (L12-3): when `deepseek` → require `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` · `AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL` · `AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL`; when `openai` → Keep `OPENAI_API_KEY` + `OPENAI_MODEL`.
- Shared interview provider port/registry for channel wire today and future REQ-13 roles (logical; package ≠ worker `providers/`).
- Prove `AIBRIDGE_WORKER_*_PROVIDER` cannot select interview (AC-02).
- Transition: deploy sets `openai` explicitly — no silent OpenAI when unset; recording ≠ substitute for missing provider.
- v1: provider bound at wire/start only (arch D4) — document; no in-session flip API.

## Вне scope
- DeepSeek/OpenAI adapter bodies (60); stub/live evidence matrix (61).
- Worker REQ-10 registry changes; GPT-48; telegram; gateway stash; mid-session flip implement.

## Verified current state (P3)
- Interview wire: `app.py` → `bind_interview_engine_at_wire` (fail-closed; no recording substitute).
- Port home: `src/aibridge/interview_providers/` (**≠** `providers/`).
- Settings: `AIBRIDGE_INTERVIEW_PROVIDER` + L12-3 nests in `config.py`; `.env.example` §4b Present.
- DeepSeek HTTP adapter body: **Deferred** (OOS STORY-60) · openai Keep `ProductionResponsesClient`.
- Worker selectors Present orthogonal (`providers/` · AC-02).
- Runtime note: [`docs/runtime-docs/07-interview-provider-port-env.md`](../../../../runtime-docs/07-interview-provider-port-env.md).
- Tests: `tests/test_story_59_interview_port_env_fail_closed.py` · suite **608 passed**.

## Target / AC
- [x] AC-AIB-12-01: config selects `deepseek` \| `openai` for interview only.
- [x] AC-AIB-12-02: worker REQ-10 env cannot act as interview switch.
- [x] AC-AIB-12-05: unknown/incomplete provider config (incl. incomplete DeepSeek nest) → fail-closed.
- [x] Wire/start binding only (D4) documented in harness/docs note.
- [x] Settings load L12-1 + L12-3 names from env (match `.env.example` §4b).

## Nested tasks (pkg-000062)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-59-t01-settings-interview-provider-required](./task-aibridge-59-t01-settings-interview-provider-required/README.md) | AC-AIB-12-01 | Done |
| t02 | [task-aibridge-59-t02-nest-l12-3-deepseek-openai-keys](./task-aibridge-59-t02-nest-l12-3-deepseek-openai-keys/README.md) | AC-AIB-12-05 nest | Done |
| t03 | [task-aibridge-59-t03-fail-closed-unset-unknown-empty](./task-aibridge-59-t03-fail-closed-unset-unknown-empty/README.md) | AC-AIB-12-05 D2 | Done |
| t04 | [task-aibridge-59-t04-worker-env-cannot-select-interview](./task-aibridge-59-t04-worker-env-cannot-select-interview/README.md) | AC-AIB-12-02 | Done |
| t05 | [task-aibridge-59-t05-interview-provider-port-registry-home](./task-aibridge-59-t05-interview-provider-port-registry-home/README.md) | AC-01 support | Done |
| t06 | [task-aibridge-59-t06-wire-start-bind-fail-closed-before-engine](./task-aibridge-59-t06-wire-start-bind-fail-closed-before-engine/README.md) | D4 | Done |
| t07 | [task-aibridge-59-t07-trust-channel-bearer-no-model-keys](./task-aibridge-59-t07-trust-channel-bearer-no-model-keys/README.md) | ownership | Done |
| t08 | [task-aibridge-59-t08-story-gate-checklist](./task-aibridge-59-t08-story-gate-checklist/README.md) | gate | **PASS** |
| t09 | [task-aibridge-59-t09-audit-g02-t08-status-pass-align](./task-aibridge-59-t09-audit-g02-t08-status-pass-align/README.md) | P4 G-02 | Done · P6 |

## P5/P6 disposition

| Gap | Disposition | Note |
|-----|-------------|------|
| G-01 | **WAIVED** out-of-DoD / info-nonblocking | DeepSeek adapter → STORY-60 |
| G-02 | **CLOSED** (was TASKED) | t09 Done · t08 Status **PASS** |

**activation:** `run_mode=aibridge_59_audit_20261101` · TASKED=**0** · **next:** **P7**
