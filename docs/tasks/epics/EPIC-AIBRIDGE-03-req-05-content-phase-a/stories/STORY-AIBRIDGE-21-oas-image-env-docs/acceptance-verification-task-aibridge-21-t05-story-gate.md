# Acceptance verification — task-aibridge-21-t05-story-gate

| Field | Value |
|-------|-------|
| **Result** | **PASS** |
| **Date** | 2026-09-16T12:55:52Z |
| **Story** | STORY-AIBRIDGE-21-oas-image-env-docs |
| **Pkg** | pkg-000018 |
| **ADR** | ADR-3 |

## AC check

- [x] REQ-05 §4.4: `COPY docs/openapi ./docs/openapi` in Dockerfile; both YAML present under `docs/openapi/`; OPENAPI_PATH = Story Intake wire.
- [x] REQ-05 §4.3: Phase A pins in `.env.example` + `aibridge-web-service-local-railway.md` (local + `/app`; SCHEMA_ID/VERSION uus_veerenni_civic/v3).
- [x] Channel OAS not in instruction `files[]` (`tests/test_story_21_oas_path_contract.py` — 3 passed).

## Evidence

```text
Dockerfile: COPY docs/openapi ./docs/openapi
.env.example: DOGESTONIA_OPENAPI_PATH=docs/openapi/story-intake-actions.openapi.yaml
              DOGESTONIA_SCHEMA_ID=uus_veerenni_civic / VERSION=v3
runbook §1.1b Phase A pins (local + /app)
pytest tests/test_story_21_oas_path_contract.py --noconftest → 3 passed
```
