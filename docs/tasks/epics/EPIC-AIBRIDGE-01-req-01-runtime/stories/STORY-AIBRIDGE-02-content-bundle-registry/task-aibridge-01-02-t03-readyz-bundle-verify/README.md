# Task: implement — /readyz current-deployment bundle verify

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)

## Purpose

`/readyz` fails when artifacts missing/mismatched vs expected hashes / current deployment bundle (REQ-01 §18). Preserve story-01 channel auth readiness invariants.

**Out of this task:** Responses loop (03); inventing CI absolute paths.

## Code Facts (verified exists)

1. Story-01 `/readyz` shell — `src/aibridge/app.py` (channel auth + equal-Bearer fail).
2. Health/ready requirements — REQ-01 §18; `04-ops-security.md` §1.
3. Bundle verify surfaces — `02-content-packaging.md`.

## AC/DoD

- [ ] Missing/mismatched artifacts → `/readyz` not ready (AC #1).
- [ ] Healthy pin → ready (with story-01 channel auth checks preserved).
- [ ] `Skill declared: python-pro` present.

## Where to change

- `src/aibridge/app.py` readyz + content verify glue from t01/t02.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k readyz
```
