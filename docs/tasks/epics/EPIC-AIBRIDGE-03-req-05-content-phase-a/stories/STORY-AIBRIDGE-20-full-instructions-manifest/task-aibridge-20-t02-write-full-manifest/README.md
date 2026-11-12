# Task: implement — write full ordered `instructions.manifest.json`

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P1 scaffold:** 2026-09-16T12:28:09Z  
**P3 Done:** 2026-09-16T12:32:27Z  
**Maps:** Scope #1–#2 · Target #2 · ADR-2

## Purpose

Replace in-place `src/instructions/instructions.manifest.json`: `bundle_version` + full `files[]` in REQ-05 §4.2 / TECH §6 order. Pack JSON **inside** `files[]`. Payload basename dual-use with `DOGESTONIA_PAYLOAD_SCHEMA_PATH` → `schema-packs.uus_veerenni_civic.v3.payload.schema.json`.

## Code Facts (verified exists — P1)

1. Manifest schema: `bundle_version` + `files[]` — `src/aibridge/content.py` `load_manifest`.
2. Current file is 6-file subset — FAIL completeness.
3. ADR-2: **no** loader schema change; no nested paths.

## AC/DoD

- [x] `files[]` is complete vs dir (except the manifest itself) and ordered per §4.2.
- [x] Pack JSON entries present in `files[]`.
- [x] Loader schema unchanged.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/instructions/instructions.manifest.json` (P3 — not this P1 scaffold).

## Verification commands

```bash
python3 -c "import json; d=json.load(open('doge-ai-bridge/src/instructions/instructions.manifest.json')); print(len(d['files']), d['files'][:5], '...')"
```
