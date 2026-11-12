# Task: implement — wire generate_strict_tool OpenAI projection

**Status:** Done · P3 2026-09-24T11:00:27Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md`  
**Parent story:** [`STORY-AIBRIDGE-41-openai-schema-projection.md`](../STORY-AIBRIDGE-41-openai-schema-projection.md)  
**P1 scaffold:** 2026-09-24T10:55:45Z  
**Maps:** AC-01…03/05/07 · AIB-COMPAT-01/03/06/09 · fail-closed `tool_gen_failed:*`

## Purpose

Wire `generate_strict_tool`: deep-copy → project via t01 helper → post-assert forbidden keywords absent; keep `strict: true` and name `postStoryDraftStash`; store once in `DeploymentBundleState.strict_tool`. Fail closed on projection error or remaining forbidden keyword. Optional redacted init event (REQ §10) — **must not** block readiness if logging fails. **No** disk writes to pack JSON / Story Intake OAS.

**Out of this task:** policy helper alone (t01); tests (t03); STORY-42/43/45 invent.

## AC/DoD

- [x] OpenAI-facing tool has no `uniqueItems`; `strict: true`; name `postStoryDraftStash`.
- [x] Input Python pack object unchanged; no pack/OAS disk rewrite.
- [x] Fail-closed `tool_gen_failed:*` (or existing convention) on projection/assert failure.
- [x] Optional init log non-blocking for readiness.
- [x] `Skill declared: python-pro` present.

## Where to change (execute — not P1)

- `src/aibridge/tool_gen.py` · `deployment.py` · `readiness.py` as needed — **P3**
