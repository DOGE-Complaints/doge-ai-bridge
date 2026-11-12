# Task: implement — strict tool from wire OAS + pack projection

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md`  
**Parent story:** [`STORY-AIBRIDGE-03-responses-tool-budgets.md`](../STORY-AIBRIDGE-03-responses-tool-budgets.md)

## Purpose

Deterministic tool schema (`strict: true`) from wire OAS + pack projection; unsupported OpenAPI constructs fail startup (no silent non-strict). Server-owned fields (pack / origin / URL / auth) never model-overridable.

**Out of this task:** gateway HTTPS executor (05); inventing operationIds beyond wire OAS.

## Code Facts (verified exists)

1. Wire OAS — `docs/openapi/story-intake-actions.openapi.yaml` (`postStoryDraftStash`).
2. Content pin may include `tool_schema_hash` — `content.py` (empty hash placeholder until generator exists).
3. Pack schema path env — `DOGESTONIA_PAYLOAD_SCHEMA_PATH` in `config.py`.

## AC/DoD

- [ ] Tool schema deterministic; `strict: true` (AC #2).
- [ ] Unsupported OAS constructs fail startup / readyz (no silent non-strict).
- [ ] Model cannot override pack / origin / URL / auth (AC #4).
- [ ] `Skill declared: python-pro` present.

## Where to change

- Tool generator module under `src/aibridge/`.
- Startup / `/readyz` verify of generated tool.
- Update tool schema pin path used by content/deployment.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
```
