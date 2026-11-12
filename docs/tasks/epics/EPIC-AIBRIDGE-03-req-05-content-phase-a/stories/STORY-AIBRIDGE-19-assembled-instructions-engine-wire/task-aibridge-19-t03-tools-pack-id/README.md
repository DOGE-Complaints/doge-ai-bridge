# Task: implement — map `strict_tool` → `engine.tools` + `pack_id`

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P1 scaffold:** 2026-09-16T12:04:31Z  
**Maps:** Scope #3 · Target #2 · ADR-1 steps 3–4

## Purpose

When deploy has `strict_tool` (schema id/version present), set `engine.tools = [deployment.strict_tool]` and `engine.pack_id` from Settings schema_id/version (or equivalent already used in prefix telemetry).

## Code Facts (verified exists — post P3 / P6 G-02)

1. Optional `strict_tool` on `DeploymentBundleState`: `src/aibridge/deployment.py`.
2. Engine fields `tools`, `pack_id`: `src/aibridge/interview.py:42–45`.
3. Helper maps `strict_tool` → `engine.tools` and `pack_id=schema_id/schema_version`: `app.py:196–230`.
4. Prefix includes tools/pack id via `build_stable_prefix` / interview path: `request_assembly.py` · `interview.py:78–112`.

## AC/DoD

- [x] Ready deploy with `strict_tool` → interview engine tools list contains that tool dict.
- [x] `pack_id` set from schema id/version settings when applicable.
- [x] When `strict_tool` is None, do not invent a fake tool.
- [x] `Skill declared: python-pro` present.

## Where to change

Helper in `app.py` (t01) and/or small touch of settings fields already on `cfg0`.

## Verification commands

```bash
rg -n "strict_tool|pack_id|generate_strict_tool" doge-ai-bridge/src/aibridge/deployment.py doge-ai-bridge/src/aibridge/app.py doge-ai-bridge/src/aibridge/interview.py
```
