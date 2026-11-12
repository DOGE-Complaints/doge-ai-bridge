# Task: implement — pilot TTL default 604800 + sliding on legitimate activity

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P1 scaffold:** 2026-09-13T17:43:00Z
**P3 Done:** 2026-09-13T17:49:14Z  
**Maps:** Scope #1 · R3-P1-10 TTL bullets

## Purpose

Align session/narrative/Responses-item TTL with REQ-03 §6.2: configured value; pilot default **604800** s; TTL slides only on legitimate session activity.

## Code Facts (verified exists — P1)

1. `src/aibridge/config.py` — `DEFAULT_SESSION_TTL_SECONDS = 86_400` (≠ 604800).
2. `src/aibridge/app.py` — assigns `sessions.ttl_seconds` from settings when set.
3. Arch overview documents 7d/604800: `docs/architecture/runtime/00-overview.md`.
4. Privacy runbook checklist: `docs/runbooks/privacy-pilot.md` §2.

## AC/DoD

- [x] Pilot default session TTL is **604800** (or documented env override matches REQ §6.2).
- [x] TTL slides only on legitimate activity (tests prove activity vs non-activity).
- [x] `.env.example` / Settings names stay consistent with REQ-03 §5.6 list.
- [x] `Skill declared: python-pro` present.

## Where to change

`src/aibridge/config.py`, session store TTL touch points, `.env.example`, tests under `tests/`.

## Verification commands

```bash
rg -n "DEFAULT_SESSION_TTL|604800|ttl_seconds" doge-ai-bridge/src/aibridge doge-ai-bridge/.env.example
cd doge-ai-bridge && python -m pytest tests/ -q -k 'ttl or retention or story_16' --tb=short
```

## Out of scope

Inventing channel OpenAPI delete fields; n8n execution purge scheduling (t05).
