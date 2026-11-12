# Task: implement — readyz strict tool generation check (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_12_audit_20260913`  
**Gap:** G-02 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-12-readyz-env-dryrun-gate-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md`](../STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)  
**P5 scaffold:** 2026-09-13T16:26:12Z
**P6 Done:** 2026-09-13T16:30:46Z  
**Maps:** REQ-03 §5.5 tool generation + strict schema

## Purpose

When content + `DOGESTONIA_SCHEMA_ID`/`VERSION` + wire/pack paths are configured, `/readyz` must verify `generate_strict_tool` (or boot `deployment.strict_tool`), not only optional tool-schema file presence.

## AC/DoD

- [x] Readiness fails with clear reason when strict tool generation would fail under configured schema ids.
- [x] No OpenAI generation / no gateway write on readiness path.
- [x] Test covers fail + pass paths.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/readiness.py`, `tests/test_story_12_readyz_env.py` (or dedicated)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/ -k "readyz and (strict or tool_gen)" --maxfail=5
```
