# STORY-AIBRIDGE-54 — OpenAI text live port

## Meta
- **Key:** `STORY-AIBRIDGE-54-openai-text-live-port`
- **Status:** P8 Done · pkg-000057 · SHAs e5cde7a/489a428/e187871 · 2026-10-16T11:48:21Z
- **P7 Re-audit:** 2026-10-16T11:46:44Z · [p7](../../../../analysis/p7-reaudit-STORY-AIBRIDGE-54-openai-text-live-port-20261016.md) · OPEN0 CLOSED0 WAIVED1
- **P8 Commits:** e5cde7a feat · 489a428 test · e187871 docs · push=NO
- **Parent Epic:** [`EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md`](../../EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md)
- **source:** `backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-54-openai-text-live-port.md`
- **decision_ref:** [`STORY-AIBRIDGE-54-….md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-54-openai-text-live-port.md) · [`REQ-10`](../../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [`01-provider-ports.md`](../../../../architecture/ai-provider-selection/01-provider-ports.md)
- **Package:** [`req-10-ai-provider-selection-and-mock-mode/INDEX.md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000057-20261016-epic-aibridge-08-story-54-openai-text-live-port.yaml`
- **P1 materialize:** 2026-10-16T11:33:17Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_54_scaffold_20261016T113216Z.plan.md)
- **P3 Execute:** 2026-10-16T11:37:56Z · [p3](../../../../run-reports/run-summary-20261016-1137-story-aibridge-54-p3.md) · tests **568 passed**
- **P4 Audit:** 2026-10-16T11:40:58Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-54-openai-text-live-port-20261016.md)
- **P5 APPLY:** 2026-10-16T11:44:26Z · TASKED=0 · WAIVED G-01 · [p5](../../../../run-reports/run-summary-20261016-1144-story-aibridge-54-p5-disposition.md) · [disposition](../../../../analysis/p5-disposition-STORY-AIBRIDGE-54-openai-text-live-port-20261016.md)
- **Gate:** [t08](./task-aibridge-54-t08-story-gate-checklist/README.md) · **PASS**
- **Depends:** STORY-51 Present; STORY-52 Present; soft STORY-53

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Ports / openai text | [`01-provider-ports.md`](../../../../architecture/ai-provider-selection/01-provider-ports.md) |
| Selectors + accept wire | `providers/` (51) · accept resolve (52) |
| Allow-mock (soft) | STORY-53 Present |

## Scope
- `openai` text provider: live extract L2 from gateway `{stories:[…]}` (or honest `corpus_insufficient`).
- Flip text mock↔openai via config/env only; same accept API (AC-10-04).
- Image stays `mock` in v1 — **no** live image.
- Failures map to existing worker `reason_class` set.
- Live OpenAI SUCCESS without credentials — residual OK; tests use mocked HTTP.

## Вне scope
- Live image; channel Responses registry; Anthropic/Gemini; gateway corpus producer; STORY-55 docs matrix.

## Target / AC
- [x] AC-10-04: Switch text mock↔openai is config/env only; same accept API.
- [x] AC-10-10: Live text accepts `{stories:[…]}` → L2 or honest `corpus_insufficient`.
- [x] Nested tasks Done at execute

**Implement (P3):** `src/aibridge/providers/openai_text_live.py` · `OpenAITextBriefProvider` injectable invoke/transport · residual live SUCCESS Unknown.

## Nested tasks (pkg-000057)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-54-t01-openai-text-brief-live-adapter](./task-aibridge-54-t01-openai-text-brief-live-adapter/README.md) | ports | Done |
| t02 | [task-aibridge-54-t02-ac-10-04-env-flip-same-accept-api](./task-aibridge-54-t02-ac-10-04-env-flip-same-accept-api/README.md) | AC-10-04 | Done |
| t03 | [task-aibridge-54-t03-ac-10-10-stories-corpus-to-l2](./task-aibridge-54-t03-ac-10-10-stories-corpus-to-l2/README.md) | AC-10-10 | Done |
| t04 | [task-aibridge-54-t04-honest-corpus-insufficient](./task-aibridge-54-t04-honest-corpus-insufficient/README.md) | AC-10-10 | Done |
| t05 | [task-aibridge-54-t05-no-silent-openai-image-stays-mock](./task-aibridge-54-t05-no-silent-openai-image-stays-mock/README.md) | L10-5/6 | Done |
| t06 | [task-aibridge-54-t06-map-failures-to-worker-reason-class](./task-aibridge-54-t06-map-failures-to-worker-reason-class/README.md) | REQ-10 §4 | Done |
| t07 | [task-aibridge-54-t07-live-text-port-tests](./task-aibridge-54-t07-live-text-port-tests/README.md) | tests | Done |
| t08 | [task-aibridge-54-t08-story-gate-checklist](./task-aibridge-54-t08-story-gate-checklist/README.md) | gate | PASS |
