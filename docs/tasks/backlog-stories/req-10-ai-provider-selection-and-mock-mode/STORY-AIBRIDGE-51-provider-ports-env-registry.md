# STORY-AIBRIDGE-51 — Provider ports + env registry

## Meta
- **Key:** `STORY-AIBRIDGE-51-provider-ports-env-registry`
- **Status:** P6 Done · t09 PASS · pkg-000054 · next **P7** · 2026-10-16T10:58:46Z  
- **P1 materialize:** 2026-10-16T10:46:25Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_51_scaffold_20261016T104516Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-51-provider-ports-env-registry/STORY-AIBRIDGE-51-provider-ports-env-registry.md)
- **P3 Execute:** 2026-10-16T10:49:56Z · [p3](../../run-reports/run-summary-20261016-1049-story-aibridge-51-p3.md)
- **P5 APPLY:** 2026-10-16T10:56:55Z · [p5](../../run-reports/run-summary-20261016-1056-story-aibridge-51-p5-disposition.md) · `run_mode=aibridge_51_audit_20261016`
- **P6 Execute:** 2026-10-16T10:58:46Z · [p6](../../run-reports/run-summary-20261016-1058-story-aibridge-51-p6.md)
- **Parent REQ:** [`REQ-10`](../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) §§2,4.1–2,5 AC-01/02/05 · L10-1/2
- **Tech-arch:** [`ai-provider-selection/01-provider-ports.md`](../../../architecture/ai-provider-selection/01-provider-ports.md) · [`02-readyz-env-fail-closed.md`](../../../architecture/ai-provider-selection/02-readyz-env-fail-closed.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [52](STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) · [53](STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) · [54](STORY-AIBRIDGE-54-openai-text-live-port.md) · [55](STORY-AIBRIDGE-55-provider-docs-verify-matrix.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-16T10:29:41Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Worker-only selectable providers for text-brief and image-poster (independent).
- Env: `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` ∈ {`mock`,`openai`}; unset → `mock` (arch `02-…`).
- Nest: model-id slots (`AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` / `…_IMAGE_POSTER_MODEL`) required for fail-closed **only if** that slot’s provider = `openai`.
- Unknown provider id → fail-closed; **no silent OpenAI fallback**.
- Channel/interview registry unchanged (L10-1).

## Out of scope
- Mock pipeline wire-through (52); readyz/allow-mock enforce (53); live OpenAI text invoke (54); docs/verify suite (55).
- Anthropic/Gemini; live image vendor; gateway contract changes.

## Verified current state
- Model slots Present + provider selectors Present (P3).
- Model fail-closed nested: only when that slot’s provider = `openai`.
- Multi-provider registry — **Present**: `src/aibridge/providers/`.
- Channel OpenAI separate — unchanged (L10-1).

## Target / AC
- [x] AC-10-01: Text slot resolves via selectable provider port.
- [x] AC-10-02: Image slot resolves independently.
- [x] AC-10-05: Unknown/incomplete provider config fail-closed; no silent OpenAI fallback.
- [x] Unset provider defaults to `mock` (arch); model nest per arch.

## Code points
- `src/aibridge/config.py` — `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `…_IMAGE_POSTER_PROVIDER`
- `src/aibridge/providers/` — registry + ports (implement choice)
- Do not alter channel Responses wiring in this story

## Dependencies
- Soft: REQ-09 worker Present (STORY-46…50). Soft: tech-arch `ai-provider-selection/` Present.
