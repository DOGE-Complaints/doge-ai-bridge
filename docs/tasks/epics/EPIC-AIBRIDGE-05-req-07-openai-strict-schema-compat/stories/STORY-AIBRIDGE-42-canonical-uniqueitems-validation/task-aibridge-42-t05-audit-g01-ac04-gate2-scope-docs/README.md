# Task: docs — soften AC-04 freeze/Send to Gate 2 unit scope (G-01)

**Status:** Done · P6 2026-09-24T11:25:01Z  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_42_audit_20260924`  
**Gap:** G-01 (Low) — P4 audit 2026-09-24 → **CLOSED**  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-42-canonical-uniqueitems-validation-20260924.md`  
**Parent story:** [`STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`](../STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md)  
**P5 scaffold:** 2026-09-24T11:22:57Z  
**P6 closed:** 2026-09-24T11:25:01Z  
**Maps:** G-01 · AC-04 docs honesty · STORY-43 footnote

## Purpose

Soften backlog + pipeline AC-04 wording that claims «no freeze / Send / gateway write» so it accurately reflects **unit Gate 2** evidence (`validate_gate2_pack_payload`). Add footnote that ValidationContext / FC bind path is owned by **STORY-43** (do not invent `app.py` VC bind here).

**Out of this task:** negative uniqueItems prove (t06); product VC bind; live TG; pack JSON rewrite.

## AC/DoD

- [x] Backlog + pipeline AC-04 wording = Gate 2 unit scope (not invent freeze/Send/gateway proof).
- [x] Footnote: STORY-43 owns VC/FC bind path.
- [x] No invent `app.py` VC bind / live TG / Railway.
- [x] `Skill declared: python-pro` present.

## Where changed

- `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`
- `doge-ai-bridge/docs/tasks/epics/EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat/stories/STORY-AIBRIDGE-42-canonical-uniqueitems-validation/STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md`
