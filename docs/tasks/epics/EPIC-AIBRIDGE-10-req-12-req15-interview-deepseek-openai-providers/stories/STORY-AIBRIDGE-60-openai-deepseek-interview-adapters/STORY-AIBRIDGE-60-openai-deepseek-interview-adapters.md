# STORY-AIBRIDGE-60 — OpenAI + DeepSeek interview adapters

## Meta
- **Key:** `STORY-AIBRIDGE-60-openai-deepseek-interview-adapters`
- **Status:** Done · Product Done · pkg-000063 · P8 2026-11-01T21:12:55Z · next **STORY-61**
- **Parent Epic:** [`EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers.md`](../../EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers.md)
- **source:** `backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md`
- **decision_ref:** [`STORY-AIBRIDGE-60-….md`](../../../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md) · [`REQ-12`](../../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) · [`02-adapters-openai-deepseek.md`](../../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md)
- **Package:** [`req-12-req15-interview-deepseek-openai-providers/INDEX.md`](../../../../backlog-stories/req-12-req15-interview-deepseek-openai-providers/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000063-20261101-epic-aibridge-10-story-60-openai-deepseek-interview-adapters.yaml`
- **P1 materialize:** 2026-11-01T20:51:31Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_60_scaffold_20261101T204955Z.plan.md)
- **Depends:** STORY-AIBRIDGE-59 Done
- **OOS:** STORY-59 port/env · STORY-61 evidence · replace InterviewEngine

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Adapters OpenAI/DeepSeek | [`02-adapters-openai-deepseek.md`](../../../../architecture/req15-interview-providers/02-adapters-openai-deepseek.md) |
| Port/env (peer Done) | [`01-interview-port-env-fail-closed.md`](../../../../architecture/req15-interview-providers/01-interview-port-env-fail-closed.md) |
| Env template | [`.env.example`](../../../../../.env.example) §4b |

## Scope
- OpenAI adapter: Keep `ProductionResponsesClient` behind interview port → Keep `InterviewEngine`.
- DeepSeek adapter: Chat Completions + L12-3 nest; same narrow client/turn surface.
- **No** silent OpenAI when `deepseek` selected.
- Module home ≠ `providers/`.

## Вне scope
- Port/env SSOT (59); evidence/live calendar (61).
- Worker adapters; replace InterviewEngine; grant Send via adapter.

## Target / AC
- [x] AC-AIB-12-03: both adapters usable under harness fixtures.
- [x] Keep Engine; port supplies backend only (D3).
- [x] No silent OpenAI when DeepSeek selected.
- [x] DeepSeek reads only L12-3 nest vars.

## Nested tasks (pkg-000063)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-60-t01-openai-adapter-keep-responses-port](./task-aibridge-60-t01-openai-adapter-keep-responses-port/README.md) | AC-03 openai | Done |
| t02 | [task-aibridge-60-t02-deepseek-adapter-chat-completions-l12-3](./task-aibridge-60-t02-deepseek-adapter-chat-completions-l12-3/README.md) | AC-03 deepseek | Done |
| t03 | [task-aibridge-60-t03-narrow-client-turn-surface-keep-engine](./task-aibridge-60-t03-narrow-client-turn-surface-keep-engine/README.md) | D3 | Done |
| t04 | [task-aibridge-60-t04-no-silent-openai-when-deepseek](./task-aibridge-60-t04-no-silent-openai-when-deepseek/README.md) | §4.3 | Done |
| t05 | [task-aibridge-60-t05-error-classes-config-vs-vendor-transport](./task-aibridge-60-t05-error-classes-config-vs-vendor-transport/README.md) | typed errors | Done |
| t06 | [task-aibridge-60-t06-module-home-ne-worker-providers](./task-aibridge-60-t06-module-home-ne-worker-providers/README.md) | ≠ providers/ | Done |
| t07 | [task-aibridge-60-t07-adapter-no-gateway-send-permission](./task-aibridge-60-t07-adapter-no-gateway-send-permission/README.md) | REQ-11 Keep | Done |
| t08 | [task-aibridge-60-t08-story-gate-checklist](./task-aibridge-60-t08-story-gate-checklist/README.md) | gate | **PASS** |
| t09 | [task-aibridge-60-t09-audit-g01-backlog-verified-state-sync](./task-aibridge-60-t09-audit-g01-backlog-verified-state-sync/README.md) | P5 G-01 | Done |
