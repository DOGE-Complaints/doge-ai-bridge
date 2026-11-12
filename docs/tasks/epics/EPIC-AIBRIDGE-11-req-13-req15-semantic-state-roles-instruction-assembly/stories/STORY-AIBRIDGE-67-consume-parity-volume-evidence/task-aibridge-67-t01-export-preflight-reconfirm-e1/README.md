# Task: Export preflight: reconfirm GPT E1

**Status:** Done · P3 2026-11-05T12:02:38Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`](../STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)  
**P1 scaffold:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md) · pkg-000070  
**Maps:** t01 · export preflight · GPT E1

## Purpose

Reconfirm GPT `instructions-roles/` vs E1 evidence; block Pass claim on stale path/hash.

## Code Facts (verify exists)

- Export tree Present under GPT UI.
- Evidence artifact may be stale until reconfirm.
- E1 = roles-schema root children + SHA-256 after normalize_text.

## AC/DoD

- [x] Export tree/path/hash reconfirmed or Explicit Block on Pass claim.
- [x] Stale evidence not cited as Export Pass.
- [x] No invent bodies / alternate hash.
- [x] Skill python-pro present.

## Where to change (P3)

- Peer evidence cite · docs only (no GPT authoring rewrite)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story67 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-67-t01-export-preflight-reconfirm-e1.md`](./acceptance-verification-task-aibridge-67-t01-export-preflight-reconfirm-e1.md)
