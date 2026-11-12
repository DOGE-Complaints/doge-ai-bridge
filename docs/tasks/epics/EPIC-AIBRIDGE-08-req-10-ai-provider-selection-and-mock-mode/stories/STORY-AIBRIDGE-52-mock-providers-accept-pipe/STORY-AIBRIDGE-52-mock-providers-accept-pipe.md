# STORY-AIBRIDGE-52 — Mock providers on accept pipe

## Meta
- **Key:** `STORY-AIBRIDGE-52-mock-providers-accept-pipe`
- **Status:** P6 Done · t09 PASS · pkg-000055 · next **P7** · 2026-10-16T11:13:36Z
- **Parent Epic:** [`EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md`](../../EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md)
- **source:** `backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md`
- **decision_ref:** [`STORY-AIBRIDGE-52-….md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-52-mock-providers-accept-pipe.md) · [`REQ-10`](../../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [`01-provider-ports.md`](../../../../architecture/ai-provider-selection/01-provider-ports.md) · [`03-verify-coexistence.md`](../../../../architecture/ai-provider-selection/03-verify-coexistence.md)
- **Package:** [`req-10-ai-provider-selection-and-mock-mode/INDEX.md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000055-20261016-epic-aibridge-08-story-52-mock-providers-accept-pipe.yaml`
- **P1 materialize:** 2026-10-16T11:03:46Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_52_scaffold_20261016T110222Z.plan.md)
- **P3 Execute:** 2026-10-16T11:05:47Z · [p3](../../../../run-reports/run-summary-20261016-1105-story-aibridge-52-p3.md)
- **P4 Audit:** 2026-10-16T11:09:18Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-52-mock-providers-accept-pipe-20261016.md)
- **P5 APPLY:** 2026-10-16T11:11:33Z · [p5](../../../../run-reports/run-summary-20261016-1111-story-aibridge-52-p5-disposition.md) · [disposition](../../../../analysis/p5-disposition-STORY-AIBRIDGE-52-mock-providers-accept-pipe-20261016.md)
- **P6 Execute:** 2026-10-16T11:13:36Z · [p6](../../../../run-reports/run-summary-20261016-1113-story-aibridge-52-p6.md) · t09 Done
- **Gate:** [t08](./task-aibridge-52-t08-story-gate-checklist/README.md) · **PASS**
- **Depends:** STORY-51 Present (`src/aibridge/providers/`)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Ports / mock backends | [`01-provider-ports.md`](../../../../architecture/ai-provider-selection/01-provider-ports.md) |
| Accept smoke verify | [`03-verify-coexistence.md`](../../../../architecture/ai-provider-selection/03-verify-coexistence.md) |
| Implement | `src/aibridge/app.py` accept · `providers/` · `poster/pipeline.py` |

## Scope
- Wire mock text/image ports into accept orchestration (Present adapters).
- Accept→brief→poster→bind without live vendor HTTP when both =`mock`.
- L2-valid brief + HTTPS-bindable poster URL.
- No third parallel fake path.

## Вне scope
- Readyz/allow-mock (53); live OpenAI text (54); docs/verify matrix (55).
- Changing bind/accept HTTP contracts.

## Target / AC
- [x] AC-10-03: mock+mock accept→brief→poster→bind without live vendor HTTP.
- [x] AC-10-06: Mock outputs L2-valid + poster HTTPS bindable.
- [x] Nested tasks Done at execute

**Implement names (P3):** accept uses `resolve_text_brief_provider` / `resolve_image_poster_provider`; upload seam `poster_bytes=` on `upload_poster_https`.

## Nested tasks (pkg-000055)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-52-t01-wire-text-brief-port-into-accept](./task-aibridge-52-t01-wire-text-brief-port-into-accept/README.md) | wire text | **Done** |
| t02 | [task-aibridge-52-t02-wire-image-poster-port-into-accept](./task-aibridge-52-t02-wire-image-poster-port-into-accept/README.md) | wire image | **Done** |
| t03 | [task-aibridge-52-t03-no-third-fake-path-present-adapters](./task-aibridge-52-t03-no-third-fake-path-present-adapters/README.md) | L10-3/4 | **Done** |
| t04 | [task-aibridge-52-t04-ac-10-03-mock-mock-no-live-vendor-http](./task-aibridge-52-t04-ac-10-03-mock-mock-no-live-vendor-http/README.md) | AC-10-03 | **Done** |
| t05 | [task-aibridge-52-t05-ac-10-06-l2-valid-https-bindable-poster](./task-aibridge-52-t05-ac-10-06-l2-valid-https-bindable-poster/README.md) | AC-10-06 | **Done** |
| t06 | [task-aibridge-52-t06-accept-pipe-production-entry-tests](./task-aibridge-52-t06-accept-pipe-production-entry-tests/README.md) | arch 03 | **Done** |
| t07 | [task-aibridge-52-t07-http-contracts-channel-unchanged](./task-aibridge-52-t07-http-contracts-channel-unchanged/README.md) | guards | **Done** |
| t08 | [task-aibridge-52-t08-story-gate-checklist](./task-aibridge-52-t08-story-gate-checklist/README.md) | gate | **PASS** |
| t09 | [task-aibridge-52-t09-audit-g03-openai-image-adapter-message](./task-aibridge-52-t09-audit-g03-openai-image-adapter-message/README.md) | P4 G-03 | **Done** |
