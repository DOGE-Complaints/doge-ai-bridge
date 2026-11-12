# STORY-AIBRIDGE-51 — Provider ports + env registry

## Meta
- **Key:** `STORY-AIBRIDGE-51-provider-ports-env-registry`
- **Status:** P6 Done · t09 PASS · pkg-000054 · next **P7** · 2026-10-16T10:58:46Z
- **Parent Epic:** [`EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md`](../../EPIC-AIBRIDGE-08-req-10-ai-provider-selection-and-mock-mode.md)
- **source:** `backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md`
- **decision_ref:** [`STORY-AIBRIDGE-51-….md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/STORY-AIBRIDGE-51-provider-ports-env-registry.md) · [`REQ-10`](../../../../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · [`01-provider-ports.md`](../../../../architecture/ai-provider-selection/01-provider-ports.md) · [`02-readyz-env-fail-closed.md`](../../../../architecture/ai-provider-selection/02-readyz-env-fail-closed.md)
- **Package:** [`req-10-ai-provider-selection-and-mock-mode/INDEX.md`](../../../../backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000054-20261016-epic-aibridge-08-story-51-provider-ports-env-registry.yaml`
- **P1 materialize:** 2026-10-16T10:46:25Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_51_scaffold_20261016T104516Z.plan.md)
- **P3 Execute:** 2026-10-16T10:49:56Z · [p3](../../../../run-reports/run-summary-20261016-1049-story-aibridge-51-p3.md)
- **P4 Audit:** 2026-10-16T10:53:17Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-51-provider-ports-env-registry-20261016.md)
- **P5 APPLY:** 2026-10-16T10:56:55Z · [p5](../../../../run-reports/run-summary-20261016-1056-story-aibridge-51-p5-disposition.md) · [disposition](../../../../analysis/p5-disposition-STORY-AIBRIDGE-51-provider-ports-env-registry-20261016.md)
- **P6 Execute:** 2026-10-16T10:58:46Z · [p6](../../../../run-reports/run-summary-20261016-1058-story-aibridge-51-p6.md) · t09 Done
- **Gate:** [t08](./task-aibridge-51-t08-story-gate-checklist/README.md) · **PASS**
- **Depends:** soft STORY-46…50 (REQ-09 Present)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Ports / registry | [`01-provider-ports.md`](../../../../architecture/ai-provider-selection/01-provider-ports.md) |
| Env nest | [`02-readyz-env-fail-closed.md`](../../../../architecture/ai-provider-selection/02-readyz-env-fail-closed.md) |
| Implement | `src/aibridge/providers/` · `config.py` selectors |

## Scope
- Worker-only selectable providers for text-brief and image-poster (independent).
- Env selectors ∈ {`mock`,`openai`}; unset → `mock`; model nest only if provider=`openai`.
- Unknown provider → fail-closed; no silent OpenAI fallback.

## Вне scope
- Mock accept wire (52); readyz/allow-mock (53); live OpenAI text (54); docs/verify (55).

## Context
Multi-provider registry — **Present** (P3): `src/aibridge/providers/`.

## Target / AC
- [x] AC-10-01: Text slot resolves via selectable provider port.
- [x] AC-10-02: Image slot resolves independently.
- [x] AC-10-05: Unknown/incomplete provider config fail-closed; no silent OpenAI fallback.
- [x] Unset provider defaults to `mock`; model nest per arch.
- [x] Nested tasks Done at execute

**Implement names (P3):** `src/aibridge/providers/` · env `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `…_IMAGE_POSTER_PROVIDER` · reason `worker_provider_unknown`.

## Nested tasks (pkg-000054)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-51-t01-config-provider-selector-env](./task-aibridge-51-t01-config-provider-selector-env/README.md) | env · arch 02 | **Done** |
| t02 | [task-aibridge-51-t02-registry-ports-module-skeleton](./task-aibridge-51-t02-registry-ports-module-skeleton/README.md) | ports · arch 01 | **Done** |
| t03 | [task-aibridge-51-t03-ac-10-01-text-slot-port-resolve](./task-aibridge-51-t03-ac-10-01-text-slot-port-resolve/README.md) | AC-10-01 | **Done** |
| t04 | [task-aibridge-51-t04-ac-10-02-image-slot-independent-resolve](./task-aibridge-51-t04-ac-10-02-image-slot-independent-resolve/README.md) | AC-10-02 | **Done** |
| t05 | [task-aibridge-51-t05-model-nest-openai-only](./task-aibridge-51-t05-model-nest-openai-only/README.md) | nest | **Done** |
| t06 | [task-aibridge-51-t06-ac-10-05-unknown-fail-closed-no-silent-openai](./task-aibridge-51-t06-ac-10-05-unknown-fail-closed-no-silent-openai/README.md) | AC-10-05 | **Done** |
| t07 | [task-aibridge-51-t07-registry-defaults-fail-closed-tests](./task-aibridge-51-t07-registry-defaults-fail-closed-tests/README.md) | tests | **Done** |
| t08 | [task-aibridge-51-t08-story-gate-checklist](./task-aibridge-51-t08-story-gate-checklist/README.md) | gate | **PASS** |
| t09 | [task-aibridge-51-t09-audit-g01-env-example-provider-selectors](./task-aibridge-51-t09-audit-g01-env-example-provider-selectors/README.md) | P4 G-01 | **Done** |
