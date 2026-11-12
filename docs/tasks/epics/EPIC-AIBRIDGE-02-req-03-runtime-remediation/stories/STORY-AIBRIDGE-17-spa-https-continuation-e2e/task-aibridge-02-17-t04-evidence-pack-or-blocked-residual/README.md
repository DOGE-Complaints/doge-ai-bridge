# Task: evidence — link spa pack or record BLOCKED residual

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../STORY-AIBRIDGE-17-spa-https-continuation-e2e.md)  
**P1 scaffold:** 2026-09-13T18:20:16Z
**P3 Done:** 2026-09-13T18:23:58Z  
**Maps:** Scope #2 · Target #1

## Purpose

Satisfy Target #1 by **linking** a spa-owned evidence pack (story Done / run-summary / checklist) proving continuation URL works on a real-device HTTPS SPA path — **or** recording a BLOCKED residual fact file when spa evidence is absent. **Do not invent** spa product code, fake screenshots, or a live PASS.

## Code Facts (verified exists — P1)

1. Precedent: STORY-15 used `live-evidence-BLOCKED-*.md` when credentials/evidence missing — no invented PASS.
2. SPA owner story key remains **Unknown** until resolved (t02).
3. aibridge unit/E2E dry-run may assert `continuation_url` shape (`tests/test_story_13_wave1_asgi_e2e.py`) — that is **not** R3-P1-08 real-device SPA proof.

## AC/DoD

- [x] Either: pipeline/ops links to spa evidence paths that exist on disk; **or** BLOCKED residual artifact documents missing spa evidence without claiming PASS.
- [x] Evidence (if present) addresses HTTPS device continuation URL path (pilot policy).
- [x] No secrets committed; no spa UI implementation in aibridge.
- [x] `Skill declared: test-master` present.

## Where to change

`docs/ops/` evidence pointer or BLOCKED fact file; pipeline story Target/Verified links.

## Verification commands

```bash
rg -n "R3-P1-08|BLOCKED|evidence|STORY-SPA|continuation" doge-ai-bridge/docs/ops --glob '*.md'
# if spa pack linked: test -f <path-from-pipeline>
```
