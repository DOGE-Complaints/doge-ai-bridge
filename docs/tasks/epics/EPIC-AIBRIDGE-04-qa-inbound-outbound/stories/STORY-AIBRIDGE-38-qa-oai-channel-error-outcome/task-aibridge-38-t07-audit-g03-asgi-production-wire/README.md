# Task: test — ASGI ProductionResponsesClient wire for 429/503 (G-03)

**Status:** Done  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_38_audit_20260918`  
**Gap:** G-03 (Low) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-38-qa-oai-channel-error-outcome-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md`](../STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md)  
**P5 scaffold:** 2026-09-18T13:53:25Z  
**Maps:** OAI-008 · OAI-009 · CHAR-006 · gaps §38

## Purpose

Add ASGI `/v1/channel/turns` path with `ProductionResponsesClient` + scripted HTTP 429/503 through `create_app` (full wire), proving transport map → handler → channel envelope. Prefer wire assert over documenting intentional split. Suite only.

**Out of this task:** guide §10.5 (t05); middleware RL discriminator (t06); invent OAS/gateway; invent live TG.

## AC/DoD

- [x] At least one ASGI test wires ProductionResponsesClient + scripted 429 and/or 503 → Option A channel envelope.
- [x] Existing transport-only and `_RaiseClient` paths remain green (or consolidated honestly).
- [x] No invent gateway / live TG / OAS fields.
- [x] `Skill declared: test-master` present.

## Where to change

- `tests/integration/test_openai_prompt_behavior.py` — **P6**
- optional: `create_app` test wiring helpers — **P6**
