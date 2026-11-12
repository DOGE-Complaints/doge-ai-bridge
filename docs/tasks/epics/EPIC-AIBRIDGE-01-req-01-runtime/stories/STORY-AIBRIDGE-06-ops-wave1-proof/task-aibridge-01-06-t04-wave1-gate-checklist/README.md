# Task: docs/test — wave-1 gate checklist

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-06-ops-wave1-proof.md`  
**P3 Done:** 2026-09-12T22:05:00Z
**Parent story:** [`STORY-AIBRIDGE-06-ops-wave1-proof.md`](../STORY-AIBRIDGE-06-ops-wave1-proof.md)

## Purpose

Document executable wave-1 checklist: `/readyz` + 401 smoke + live n8n → `/v1/channel/turns` (dry-run/interview) without stash (AC #3). Live n8n may remain manual ops proof.

**Out of this task:** Requiring live n8n in CI; inventing n8n JSON; wave-2 SPA E2E.

## Code Facts (verified exists)

1. `/readyz`, `/healthz` — `app.py`.
2. Channel 401 auth — story 01.
3. Arch wave-1 — `00-overview.md` §7; `01-channel-facade.md` §7.

## AC/DoD

- [x] Wave-1 checklist markdown on disk (executable steps).
- [x] Automated smoke for `/readyz` + 401 where practical.
- [x] Checklist notes dry-run/interview without stash.
- [x] `Skill declared: python-pro` present.

## Where to change

- Ops checklist under `docs/ops/` or runbooks.
- Optional `tests/` smoke for readyz/401.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# checklist path exists after implement
```
