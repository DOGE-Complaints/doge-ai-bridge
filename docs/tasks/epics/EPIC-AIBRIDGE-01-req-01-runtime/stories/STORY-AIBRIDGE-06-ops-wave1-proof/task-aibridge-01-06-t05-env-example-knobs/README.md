# Task: docs — `.env.example` knobs (names only)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md`  
**P3 Done:** 2026-09-12T22:05:00Z
**Parent story:** [`STORY-AIBRIDGE-06-ops-wave1-proof.md`](../STORY-AIBRIDGE-06-ops-wave1-proof.md)

## Purpose

`.env.example` lists required knobs from REQ-01 §17 / budget policy **names only** — no secret values (AC #5).

**Out of this task:** Inventing numeric budget defaults; committing real secrets.

## Code Facts (verified exists)

1. `.env.example` partially populated (stories 01–05).
2. `config.py` Settings aliases.
3. Arch budget knobs — `04-ops-security.md` §2.

## AC/DoD

- [x] Required §17 / budget / gateway / dry-run / redirect names listed.
- [x] No secret literals in `.env.example`.
- [x] Test or checklist verifies names present.
- [x] `Skill declared: python-pro` present.

## Where to change

- `.env.example`; align comments with `config.py` as needed.

## Verification commands

```bash
rg -n '^[A-Z0-9_]+=' doge-ai-bridge/.env.example
cd doge-ai-bridge && .venv/bin/pytest -q
```
