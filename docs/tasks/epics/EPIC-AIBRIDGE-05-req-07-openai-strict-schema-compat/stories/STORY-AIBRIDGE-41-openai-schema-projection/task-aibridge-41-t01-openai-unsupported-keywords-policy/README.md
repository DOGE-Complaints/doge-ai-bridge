# Task: implement — OpenAI unsupported schema keywords policy + strip helper

**Status:** Done · P3 2026-09-24T11:00:27Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md`  
**Parent story:** [`STORY-AIBRIDGE-41-openai-schema-projection.md`](../STORY-AIBRIDGE-41-openai-schema-projection.md)  
**P1 scaffold:** 2026-09-24T10:55:45Z  
**Maps:** AIB-COMPAT-02/10/11 · TECH-ARCH §2.1

## Purpose

Add code-level policy constant (e.g. `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS = frozenset({"uniqueItems"})`) and recursive helper that removes **JSON Schema keyword** keys listed in the policy from a deep-copied schema tree (not data fields merely named `uniqueItems`).

**Out of this task:** wire into `generate_strict_tool` (t02); tests (t03); Gate 2 uniqueItems enforcement (STORY-42).

## AC/DoD

- [x] Policy constant exists and is the sole allow-list for strip targets.
- [x] Recursive strip covers nested schema shapes (`properties` / `items` / `anyOf` / … as required by AIB-COMPAT-02).
- [x] Does not delete domain data fields solely by name.
- [x] `Skill declared: python-pro` present.

## Where to change (execute — not P1)

- `src/aibridge/tool_gen.py` (or adjacent module) — **P3**
