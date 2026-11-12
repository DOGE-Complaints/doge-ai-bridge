# Task: docs — GC operator note + refresh t02 README (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_02_audit_20260912`  
**Gap:** G-02 (Info) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-02-content-bundle-registry-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)  
**P5 scaffold:** 2026-09-12T21:09:54Z  
**P6 Done:** 2026-09-12T21:13:50Z

## Purpose

(a) Document operator GC trigger/schedule: `gc_unreferenced_bundles` is library+unit only (no `app.py` lifecycle call) — when/how ops may invoke it.  
(b) Refresh `task-aibridge-01-02-t02-…/README.md` Code Facts / DoD checkboxes to match disk (Memory+Sqlite Done; Postgres → t07 Done).

**Out of this task:** Implementing GC cron in ASGI; inventing absolute CI paths.

## Code Facts (verified exists — post P6)

1. GC library — `src/aibridge/bundle_gc.py`; tests `tests/test_bundle_gc.py`.
2. No `gc_unreferenced` call in `src/aibridge/app.py`.
3. Operator note — `docs/architecture/runtime/02-content-packaging.md` §4 «Operator GC trigger (pilot)».
4. t02 README refreshed to Memory/Sqlite + Postgres t07.

## AC/DoD

- [x] Ops/arch note documents GC trigger or schedule (library vs runtime); no invented absolute paths.
- [x] t02 README Code Facts + DoD synced.
- [x] Acceptance-verification; gate Date live.
- [x] `Skill declared: python-pro` present.

## Where to change

- `task-aibridge-01-02-t02-postgres-bundle-registry/README.md`
- `docs/architecture/runtime/02-content-packaging.md`

## Verification commands (P6)

```bash
rg -n 'Operator GC|gc_unreferenced|grace' doge-ai-bridge/docs/architecture/runtime/02-content-packaging.md
```
