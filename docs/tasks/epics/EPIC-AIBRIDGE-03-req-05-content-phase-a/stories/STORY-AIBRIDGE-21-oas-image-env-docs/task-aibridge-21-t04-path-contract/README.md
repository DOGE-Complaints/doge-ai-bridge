# Task: assert — OPENAPI_PATH story-intake; channel not in files[]

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md`  
**Parent story:** [`STORY-AIBRIDGE-21-oas-image-env-docs.md`](../STORY-AIBRIDGE-21-oas-image-env-docs.md)  
**P1 scaffold:** 2026-09-16T12:52:52Z
**P3 Done:** 2026-09-16T12:55:52Z  
**Maps:** Scope #2–#3 · TECH ADR-3 · REQ-05 §4.4

## Purpose

Assert path contract: `DOGESTONIA_OPENAPI_PATH` targets Story Intake wire (`story-intake-actions.openapi.yaml`); channel OAS may exist in `docs/openapi/` but must **not** appear in `instructions.manifest.json` `files[]`.

**Out of this task:** Dockerfile COPY (t01); inventing loader schema change; redesign channel OAS.

## Code Facts (verified exists — P1)

1. Wire OAS: `docs/openapi/story-intake-actions.openapi.yaml`.
2. Channel OAS: `docs/openapi/aibridge-channel-v1.openapi.yaml`.
3. Manifest `files[]` is instruction dump only: `src/instructions/instructions.manifest.json` (STORY-20 full dump).
4. Config name: `src/aibridge/config.py` (OPENAPI path setting).

## AC/DoD

- [x] Test or assert: documented/default OPENAPI_PATH basename = `story-intake-actions.openapi.yaml` (not channel).
- [x] Assert channel OAS filename absent from manifest `files[]`.
- [x] No product invent beyond contract test; `Skill declared: python-pro` present.

## Where to change

- `tests/` (new or extend STORY-21 contract test) · optional cite in `.env.example` (P3)

## Verification commands

```bash
python3 - <<'PY'
import json
from pathlib import Path
m = json.loads(Path('doge-ai-bridge/src/instructions/instructions.manifest.json').read_text())
assert 'aibridge-channel-v1.openapi.yaml' not in m['files']
assert 'story-intake-actions.openapi.yaml' not in m['files']
print('ok: channel+wire OAS not in instruction files[]')
PY
ls doge-ai-bridge/docs/openapi/story-intake-actions.openapi.yaml
```
