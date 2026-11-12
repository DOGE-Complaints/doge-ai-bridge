# Task: implement — expired narrative delete or irreversible minimize

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P1 scaffold:** 2026-09-13T17:43:00Z
**P3 Done:** 2026-09-13T17:49:14Z  
**Maps:** Scope #2 (narrative) · R3-P1-10

## Purpose

When session/narrative/Responses-item TTL expires, narrative is deleted or irreversibly minimized so resident text is not recoverable from aibridge storage.

## Code Facts (verified exists — P1)

1. Privacy runbook: early delete after stashed/cancelled; TTL ≤7d — `docs/runbooks/privacy-pilot.md`.
2. Postgres session/history surfaces exist under `src/aibridge/pg_runtime.py` (story 09).
3. `bundle_gc.py` GCs unreferenced content bundles — **not** narrative retention.
4. Concrete expiry job / minimize path for narrative: **Unknown** at P1 (implement in P3).

## AC/DoD

- [x] Expired narrative is deleted or irreversibly minimized (test with unique phrase).
- [x] Early-delete path after stashed/cancelled covered or explicitly deferred with evidence pointer.
- [x] Does not invent OpenAI store:true or channel OAS fields.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/` session/history/retention modules; migrations if needed; tests.

## Verification commands

```bash
rg -n "minimize|expire|retention|delete.*session|narrative" doge-ai-bridge/src/aibridge --glob '*.py' | head -40
cd doge-ai-bridge && python -m pytest tests/ -q -k 'narrative or retention or story_16' --tb=short
```

## Out of scope

Ops HTTP delete surface (t04); action-token purge (t03).
