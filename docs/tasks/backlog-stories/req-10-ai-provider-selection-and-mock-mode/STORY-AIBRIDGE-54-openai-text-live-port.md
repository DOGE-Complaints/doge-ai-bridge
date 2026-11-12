# STORY-AIBRIDGE-54 — OpenAI text live port

## Meta
- **Key:** `STORY-AIBRIDGE-54-openai-text-live-port`
- **Status:** P7 Done · WAVE Y · pkg-000057 · next **P8** · 2026-10-16T11:46:44Z
- **P7 Re-audit:** 2026-10-16T11:46:44Z · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-54-openai-text-live-port-20261016.md) · OPEN0 CLOSED0 WAIVED1
- **P4 Audit:** 2026-10-16T11:40:58Z · [p4](../../../analysis/p4-audit-STORY-AIBRIDGE-54-openai-text-live-port-20261016.md)
- **P5 APPLY:** 2026-10-16T11:44:26Z · [p5](../../run-reports/run-summary-20261016-1144-story-aibridge-54-p5-disposition.md) · [disposition](../../../analysis/p5-disposition-STORY-AIBRIDGE-54-openai-text-live-port-20261016.md)
- **Parent REQ:** [`REQ-10`](../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) §§2,4.4–5,5 AC-04/10 · L10-5/6
- **Tech-arch:** [`ai-provider-selection/01-provider-ports.md`](../../../architecture/ai-provider-selection/01-provider-ports.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [51](STORY-AIBRIDGE-51-provider-ports-env-registry.md) · [52](STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) · [53](STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) · [55](STORY-AIBRIDGE-55-provider-docs-verify-matrix.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-16T10:29:41Z
- **P1 materialize:** 2026-10-16T11:33:17Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_54_scaffold_20261016T113216Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-54-openai-text-live-port/STORY-AIBRIDGE-54-openai-text-live-port.md)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- `openai` text provider: live extract L2 from gateway `{stories:[…]}` corpus (or honest `corpus_insufficient`).
- Flip text mock↔openai via config/env only; same accept API (AC-10-04).
- Image stays `mock` in v1 (L10-5); do **not** implement live image.
- Failures map to existing worker `reason_class` set.
- No silent fallback to OpenAI when provider ≠ `openai`.
- Live OpenAI SUCCESS without credentials — residual OK; prove via mocked HTTP in tests.

## Out of scope
- Live image; channel Responses registry changes; Anthropic/Gemini; gateway corpus producer (REQ-58); STORY-55 docs matrix.

## Verified current state
- Live text extract Present — `providers/openai_text_live.py` · `OpenAITextBriefProvider` (injectable invoke; mocked tests).
- Channel `ProductionResponsesClient` Present — separate path (not channel registry in this story).
- Accept ports Present (STORY-52); allow-mock Present (STORY-53).
- Residual: live OpenAI SUCCESS credentials/network **Unknown**.

## Target / AC
- [x] AC-10-04: Switch text mock↔openai is config/env only; same accept API.
- [x] AC-10-10: Live text accepts `{stories:[…]}` → L2 or honest `corpus_insufficient`.

## Code points
- OpenAI text adapter behind TextBriefPort; model-id from nested slot when provider=`openai`
- Do not change accept route/auth contracts

## Dependencies
- STORY-AIBRIDGE-51, STORY-AIBRIDGE-52
