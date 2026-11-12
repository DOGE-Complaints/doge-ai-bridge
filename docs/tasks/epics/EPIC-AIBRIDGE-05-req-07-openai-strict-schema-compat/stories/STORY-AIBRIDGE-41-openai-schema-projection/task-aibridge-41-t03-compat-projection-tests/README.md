# Task: test — compat projection AC / T-COMPAT proofs

**Status:** Done · P3 2026-09-24T11:00:27Z  

**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md`  
**Parent story:** [`STORY-AIBRIDGE-41-openai-schema-projection.md`](../STORY-AIBRIDGE-41-openai-schema-projection.md)  
**P1 scaffold:** 2026-09-24T10:55:45Z  
**Maps:** AC-01/02/03/05/07 · T-COMPAT-02/03 · REQ §11.1

## Purpose

Extend `tests/test_tool_gen.py` and/or dedicated module: prove disk pack + Story Intake OAS unchanged; OpenAI tool has no `uniqueItems` anywhere; `strict: true` + name; input Python object unchanged; deterministic serialization. No live Telegram / Railway invent.

**Out of this task:** product wire (t01/t02); story gate (t04); Gate 2 uniqueItems tests (STORY-42).

## AC/DoD

- [x] AC-01/02/03/05/07 · T-COMPAT-01…05/07/08 · **T-COMPAT-06** (P6 t06) covered in `tests/test_openai_schema_projection.py`
- [x] No invent live TG / OpenAI network SUCCESS.
- [x] Suite green under filter (P6: **14 passed**).
- [x] `Skill declared: python-pro` present.

## Where to change (execute — not P1)

- `tests/test_tool_gen.py` and/or new test module — **P3**
