# Task: implement — Prometheus `/metrics` private (no narrative)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md`  
**P3 Done:** 2026-09-12T22:05:00Z
**Parent story:** [`STORY-AIBRIDGE-06-ops-wave1-proof.md`](../STORY-AIBRIDGE-06-ops-wave1-proof.md)

## Purpose

Prometheus-compatible `/metrics` on private interface; no PII / narrative / secrets; include budget-stop reasons (AC #1 / Scope #1).

**Out of this task:** APM SaaS; inventing n8n workflow JSON.

## Code Facts (verified exists)

1. Arch metrics rules — `docs/architecture/runtime/04-ops-security.md` §3.
2. Budget breach redacted reason hook — `budgets.py` comment (story 06).
3. No `/metrics` route under `src/aibridge/app.py` yet.

## AC/DoD

- [x] `/metrics` returns Prometheus text without channel Bearer (private-only assumption for pilot).
- [x] Series exclude narrative/PII/secrets; budget-stop reasons present when applicable.
- [x] Unit tests assert no narrative samples.
- [x] `Skill declared: python-pro` present.

## Where to change

- New metrics module under `src/aibridge/`; `app.py` route; budget → metric hooks.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
```
