# Task: test — assert checklist G3 SPA stash wording (G-03)

**Status:** Done · 2026-09-18T13:03:40Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Wave:** `run_mode=aibridge_37_audit_20260918`  
**Gap:** G-03 (Low) — P4 audit 2026-09-18  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence-20260918.md`  
**Parent story:** [`STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md`](../STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md)  
**P5 scaffold:** 2026-09-18T13:01:18Z  
**P6 closed:** 2026-09-18T13:03:40Z  
**Maps:** Gate-5 · guide §15 G3 · r3-p1-09 checklist · honesty suite

## Purpose

Extend `tests/test_gate5_evidence_honesty.py` (`test_gate5_checklist_and_uc_crosslinks` or sibling) so guide §15 / checklist **G3** (staging stash → SPA continuation URL) is asserted alongside G1/G2/G4 string checks. Suite/docs only.

**Out of this task:** QUAL map (t05); honesty count docs (t07); check off live G1–G4; invent live TG/Railway; product code.

## AC/DoD

- [x] Honesty suite asserts G3 wording present in checklist (and/or guide §15 pointer).
- [x] Existing G1/G2/G4 asserts remain green; default CI still no live TG.
- [x] No invent live Telegram / Railway SUCCESS / evidence bodies.
- [x] `Skill declared: test-master` present.

## Where to change

- `doge-ai-bridge/tests/test_gate5_evidence_honesty.py` — **P6 Done**
- optional read: `docs/ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md` §Gate-5 — **P6**
