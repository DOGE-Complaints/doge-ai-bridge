# STORY-AIBRIDGE-52 — Mock providers on accept pipe

## Meta
- **Key:** `STORY-AIBRIDGE-52-mock-providers-accept-pipe`
- **Status:** P6 Done · t09 PASS · pkg-000055 · next **P7** · 2026-10-16T11:13:36Z
- **Parent REQ:** [`REQ-10`](../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) §§2,4.2–3,5 AC-03/06 · L10-3/4
- **Tech-arch:** [`ai-provider-selection/01-provider-ports.md`](../../../architecture/ai-provider-selection/01-provider-ports.md) · [`03-verify-coexistence.md`](../../../architecture/ai-provider-selection/03-verify-coexistence.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [51](STORY-AIBRIDGE-51-provider-ports-env-registry.md) · [53](STORY-AIBRIDGE-53-readyz-allow-mock-refuse.md) · [54](STORY-AIBRIDGE-54-openai-text-live-port.md) · [55](STORY-AIBRIDGE-55-provider-docs-verify-matrix.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-16T10:29:41Z
- **P1 materialize:** 2026-10-16T11:03:46Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_52_scaffold_20261016T110222Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode/stories/STORY-AIBRIDGE-52-mock-providers-accept-pipe/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md)
- **P3 Execute:** 2026-10-16T11:05:47Z · [p3](../../run-reports/run-summary-20261016-1105-story-aibridge-52-p3.md)
- **P5 APPLY:** 2026-10-16T11:11:33Z · [p5](../../run-reports/run-summary-20261016-1111-story-aibridge-52-p5-disposition.md) · `run_mode=aibridge_52_audit_20261016`
- **P6 Execute:** 2026-10-16T11:13:36Z · [p6](../../run-reports/run-summary-20261016-1113-story-aibridge-52-p6.md)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- `mock` text = Present corpus-grounded path behind TextBriefPort (`sense_brief/pipeline.py`) — L10-3.
- `mock` image = Present deterministic PNG behind ImagePosterPort (`poster/image.py`) — L10-4.
- Accept→brief→poster→bind without live vendor HTTP when both providers are `mock` (serve gated by allow-mock in 53).
- L2-valid brief + HTTPS-bindable poster URL (upload Present).
- No third parallel fake path — promote Present impl behind ports.

## Out of scope
- Live OpenAI text (54); readyz/allow-mock ownership (53); ops docs (55).
- Changing bind/accept HTTP contracts.

## Verified current state
- Accept wires `resolve_text_brief_provider` / `resolve_image_poster_provider` — `app.py` (P3).
- Mock adapters → Present pipelines — `providers/adapters.py`.
- Upload seam — `poster/pipeline.py` `poster_bytes=`.
- Injectable upload — `poster/storage.py` (REQ-10 §3).

## Target / AC
- [x] AC-10-03: mock+mock accept→brief→poster→bind without live vendor HTTP.
- [x] AC-10-06: Mock outputs L2-valid + poster HTTPS bindable.

## Code points
- `src/aibridge/app.py` — accept port wire
- `src/aibridge/providers/` · `poster/pipeline.py` `poster_bytes=`
- `tests/test_mock_accept_pipe_story_52.py`

## Dependencies
- STORY-AIBRIDGE-51
