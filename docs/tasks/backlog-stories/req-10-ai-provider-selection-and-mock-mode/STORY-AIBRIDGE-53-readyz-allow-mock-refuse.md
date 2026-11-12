# STORY-AIBRIDGE-53 — Readyz + allow-mock refuse

## Meta
- **Key:** `STORY-AIBRIDGE-53-readyz-allow-mock-refuse`
- **Status:** P5 APPLY · TASKED=0 · pkg-000056 · next **P7** · 2026-10-16T11:28:42Z
- **Parent REQ:** [`REQ-10`](../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) §§2,4.6,5 AC-08/09 · L10-7/8
- **Tech-arch:** [`ai-provider-selection/02-readyz-env-fail-closed.md`](../../../architecture/ai-provider-selection/02-readyz-env-fail-closed.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [51](STORY-AIBRIDGE-51-provider-ports-env-registry.md) · [52](STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) · [54](STORY-AIBRIDGE-54-openai-text-live-port.md) · [55](STORY-AIBRIDGE-55-provider-docs-verify-matrix.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-16T10:29:41Z
- **P1 materialize:** 2026-10-16T11:18:56Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_53_scaffold_20261016T111732Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-53-readyz-allow-mock-refuse/STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md)
- **P3 Execute:** 2026-10-16T11:23:50Z · [p3](../../run-reports/run-summary-20261016-1123-story-aibridge-53-p3.md)
- **P5 APPLY:** 2026-10-16T11:28:42Z · [p5](../../run-reports/run-summary-20261016-1128-story-aibridge-53-p5-disposition.md) · activation **none**
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Env `AIBRIDGE_ALLOW_MOCK_PROVIDERS`; without it → refuse mock at **/readyz** and **worker accept**.
- Slot-gated OpenAI: both worker providers `mock` → `/ready` does not require `OPENAI_API_KEY` for the worker gate.
- Reason/fail-class: `worker_mock_not_allowed`.

## Out of scope
- Channel registry refactor; defaulting Railway public board to mock; live text (54).

## Verified current state
- Provider selectors + nest — **Present** (STORY-51).
- Allow-mock + slot-gated presence + refuse — **Present** (this story P3).
- Accept ports — Present (STORY-52).

## Target / AC
- [x] AC-10-08: mock+mock → `/ready` without `OPENAI_API_KEY` (worker gate).
- [x] AC-10-09: Production/public refuses mock unless explicit override (readyz + accept).

## Code points
- `src/aibridge/readiness.py` · `config.py` · `app.py` worker middleware · `tests/test_readyz_allow_mock_story_53.py`

## Dependencies
- STORY-AIBRIDGE-51
