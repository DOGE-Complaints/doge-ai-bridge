# Task: Lock joint inventory = E1

**Status:** Done · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t02 · joint wire · REQ-13 §3b/§7

## Purpose

Lock joint inventory = **GPT E1** into aibridge docs (REQ-13 Open close note · runtime 11). ≠ session_pin. No invent alternate.

## Code Facts (verify exists)

- GPT E1 Present in peer arch 03.
- REQ-13 inventory/hash Open until lock.
- content.py normalize_text + sha256_hex Present.

## AC/DoD

- [x] REQ-13 / runtime-11 state E1 as locked joint wire.
- [x] session_pin explicitly ≠ file inventory hash.
- [x] No invent alternate format.
- [x] Skill python-pro present.

## Where to change (P3)

- docs/requirements/REQ-13-… · docs/runtime-docs/11-…

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t02-lock-joint-inventory-e1.md`](./acceptance-verification-task-aibridge-67-t02-lock-joint-inventory-e1.md)
