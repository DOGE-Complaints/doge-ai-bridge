# Task: docs — privacy-pilot §2–§3 ops-before-residents residual (G-03)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_16_audit_20260913`  
**Gap:** G-03 (Info) — P4 audit 2026-09-13  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-16-privacy-retention-20260913.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P5 scaffold:** 2026-09-13T17:52:16Z
**P6 Done:** 2026-09-13T17:55:59Z  
**Maps:** §6.2 n8n/early-delete/backup residuals

## Purpose

Document that privacy-pilot §2–§3 unchecked ops items (n8n retention evidence, early delete after stash, backup vs delete) are **ops-before-residents** residuals — not inventing PASS; not a code blocker for story Target AC.

## AC/DoD

- [x] privacy-pilot notes residual clearly (G-03 / before residents).
- [x] No fake checkbox PASS.
- [x] `Skill declared: python-pro` present.

## Where to change

`docs/runbooks/privacy-pilot.md`

## Verification commands

```bash
rg -n "ops-before-residents|G-03|residual" doge-ai-bridge/docs/runbooks/privacy-pilot.md
```
