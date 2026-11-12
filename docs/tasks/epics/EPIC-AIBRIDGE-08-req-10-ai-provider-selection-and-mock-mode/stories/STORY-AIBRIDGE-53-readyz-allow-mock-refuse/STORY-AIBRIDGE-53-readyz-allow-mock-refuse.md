# STORY-AIBRIDGE-53 — Readyz + allow-mock refuse

## Meta
- **Key:** `STORY-AIBRIDGE-53-readyz-allow-mock-refuse`
- **Status:** P5 APPLY · TASKED=0 · pkg-000056 · next **P7** · 2026-10-16T11:28:42Z
- **Parent Epic:** [`EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md`](../../EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md)
- **source:** `backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md`
- **decision_ref:** [`STORY-AIBRIDGE-53-….md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) · [`REQ-10`](../../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [`02-readyz-env-fail-closed.md`](../../../../architecture/ai-provider-selection/02-readyz-env-fail-closed.md)
- **Package:** [`req-10-ai-provider-selection-and-mock-mode/INDEX.md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000056-20261016-epic-aibridge-08-story-53-readyz-allow-mock-refuse.yaml`
- **P1 materialize:** 2026-10-16T11:18:56Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_53_scaffold_20261016T111732Z.plan.md)
- **P3 Execute:** 2026-10-16T11:23:50Z · [p3](../../../../run-reports/run-summary-20261016-1123-story-aibridge-53-p3.md) · tests **559 passed**
- **P4 Audit:** 2026-10-16T11:26:35Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-53-readyz-allow-mock-refuse-20261016.md)
- **P5 APPLY:** 2026-10-16T11:28:42Z · [p5](../../../../run-reports/run-summary-20261016-1128-story-aibridge-53-p5-disposition.md) · [disposition](../../../../analysis/p5-disposition-STORY-AIBRIDGE-53-readyz-allow-mock-refuse-20261016.md) · activation **none**
- **Gate:** [t08](./task-aibridge-53-t08-story-gate-checklist/README.md) · **PASS**
- **Depends:** STORY-51 Present; soft STORY-52

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Env / allow-mock / slot-gated OpenAI | [`02-readyz-env-fail-closed.md`](../../../../architecture/ai-provider-selection/02-readyz-env-fail-closed.md) |
| Selectors Present | `src/aibridge/config.py` · `providers/` (51) |
| Readyz | `src/aibridge/readiness.py` |

## Scope
- Env `AIBRIDGE_ALLOW_MOCK_PROVIDERS`; without it → refuse mock at **/readyz** and **worker accept**.
- Slot-gated OpenAI: both worker providers `mock` → `/ready` does not require `OPENAI_API_KEY` for the worker gate.
- Exact readiness reason / accept fail-class: **`worker_mock_not_allowed`** (P3).

## Вне scope
- Channel registry; live OpenAI text (54); docs/verify matrix (55).

## Target / AC
- [x] AC-10-08: mock+mock → `/ready` without `OPENAI_API_KEY` (worker gate).
- [x] AC-10-09: Production/public refuses mock unless explicit override (readyz + accept).
- [x] Nested tasks Done at execute

**Implement names (P3):** `AIBRIDGE_ALLOW_MOCK_PROVIDERS` · `worker_mock_not_allowed` · `worker_openai_presence_required`.

## Nested tasks (pkg-000056)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-53-t01-config-allow-mock-providers-env](./task-aibridge-53-t01-config-allow-mock-providers-env/README.md) | env | Done |
| t02 | [task-aibridge-53-t02-slot-gated-openai-presence-worker](./task-aibridge-53-t02-slot-gated-openai-presence-worker/README.md) | L10-7 | Done |
| t03 | [task-aibridge-53-t03-ac-10-08-readyz-mock-mock-without-openai-key](./task-aibridge-53-t03-ac-10-08-readyz-mock-mock-without-openai-key/README.md) | AC-10-08 | Done |
| t04 | [task-aibridge-53-t04-ac-10-09-readyz-refuse-mock-without-allow](./task-aibridge-53-t04-ac-10-09-readyz-refuse-mock-without-allow/README.md) | AC-10-09 readyz | Done |
| t05 | [task-aibridge-53-t05-ac-10-09-accept-refuse-mock-without-allow](./task-aibridge-53-t05-ac-10-09-accept-refuse-mock-without-allow/README.md) | AC-10-09 accept | Done |
| t06 | [task-aibridge-53-t06-explicit-mock-without-allow-reason-string](./task-aibridge-53-t06-explicit-mock-without-allow-reason-string/README.md) | reason string | Done |
| t07 | [task-aibridge-53-t07-readyz-accept-allow-mock-tests](./task-aibridge-53-t07-readyz-accept-allow-mock-tests/README.md) | tests | Done |
| t08 | [task-aibridge-53-t08-story-gate-checklist](./task-aibridge-53-t08-story-gate-checklist/README.md) | gate | PASS |
