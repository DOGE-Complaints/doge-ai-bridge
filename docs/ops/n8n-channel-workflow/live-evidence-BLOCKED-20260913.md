# Live evidence — BLOCKED (2026-09-13)

**Story:** STORY-AIBRIDGE-15-n8n-telegram-gate  
**Stamp:** 2026-09-13T17:31:50Z  
**Task:** t05 live evidence / recorded test

## BLOCKED facts (verified on disk this session)

| Probe | Result |
|-------|--------|
| `doge-ai-bridge/.env` | **Absent** |
| `docs/ops/n8n-channel-workflow/exports/*.json` | **Absent** (directory not present) |
| Telegram Bot token in repo | **Not found** (must not invent) |
| Channel Bearer for live n8n | **Not found** in focus tree for live call |
| Live Telegram → n8n → aibridge run | **Not executed** — credentials/workflow export missing |

## What was delivered instead (not live PASS)

1. Executable §6.1 checklist: [r3-p1-09-live-gate-checklist.md](./r3-p1-09-live-gate-checklist.md)
2. Ops contract + retry/`event_id` rules: [README.md](./README.md)
3. Simulated/contract tests (no secrets): `tests/test_story_15_n8n_gate_contract.py`

## Operator unblock

1. Provide private aibridge URL + channel Bearer in n8n (not git).
2. Import verified workflow (optional credential-stripped export = P2-04, out of this story DoD).
3. Run checklist A–C live; attach redacted screenshots/logs; clear BLOCKED.

**Claim rule:** do **not** mark Target #1 live PASS until evidence exists. Contract tests ≠ live Telegram proof.
