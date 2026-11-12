# Task: evidence — live proof or recorded integration test

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md`  
**Parent story:** [`STORY-AIBRIDGE-15-n8n-telegram-gate.md`](../STORY-AIBRIDGE-15-n8n-telegram-gate.md)  
**P1 scaffold:** 2026-09-13T17:28:28Z
**P3 Done:** 2026-09-13T17:34:04Z  
**Maps:** Target #1 · R3-P1-09

## Purpose

Produce story Target #1 evidence: runbook + screenshots/logs **or** a recorded integration test showing live routing matches §6.1 (no secrets in git).

## Code Facts (verified exists — P1)

1. Wave-1 manual n8n proof steps exist but are incomplete vs §6.1: `docs/ops/wave1-gate-checklist.md`.
2. n8n README smoke §5 is operator-facing, not a filled evidence pack.
3. Credential-stripped JSON export is **out of scope** (P2-04) — evidence must not invent a fake export body.

## AC/DoD

- [x] Evidence artifact(s) on disk (ops notes path / recorded test) cover §6.1 checklist completion for Target #1.
- [x] Evidence includes retry/`event_id` invariance or points to t04 proof.
- [x] No secrets committed.
- [x] `Skill declared: python-pro` present.

**P3 note:** Live Telegram/n8n screenshots **BLOCKED** — no `.env` / workflow export / Bot token on disk. Recorded contract tests + BLOCKED fact file delivered instead of inventing live PASS.

## Where to change

`docs/ops/` evidence pointers; optional `tests/` recorded integration; operator notes outside secrets.

## Verification commands

```bash
rg -n "R3-P1-09|§6.1|live n8n|evidence" doge-ai-bridge/docs/ops --glob '*.md'
# live: follow checklist; record proof without committing tokens
```
