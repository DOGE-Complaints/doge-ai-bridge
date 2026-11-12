# Task: docs — R3-P1-08 HTTPS SPA continuation gate checklist SSOT

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../STORY-AIBRIDGE-17-spa-https-continuation-e2e.md)  
**P1 scaffold:** 2026-09-13T18:20:16Z
**P3 Done:** 2026-09-13T18:23:58Z  
**Maps:** Scope #1 · R3-P1-08

## Purpose

Publish an executable **aibridge gate/tracker** checklist for REQ-03 R3-P1-08 (real-device HTTPS SPA continuation E2E / wave-2 residents) so the package has a single ops SSOT — without implementing SPA UI inside aibridge.

## Code Facts (verified exists — P1)

1. REQ-03 §6 row R3-P1-08: `docs/requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md`.
2. aibridge builds continuation URL: `src/aibridge/gateway.py` `build_continuation_url` → `{base}/#/story/submit?draft_id=…`.
3. SPA base env: `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` in `src/aibridge/config.py` / `.env.example`.
4. `docs/ops/wave1-gate-checklist.md` exists but is **not** the R3-P1-08 SPA HTTPS gate.

## AC/DoD

- [x] Executable R3-P1-08 tracker checklist on disk under `docs/ops/` (new file or clearly titled section).
- [x] Checklist states aibridge = gate/tracker; SPA profile owns device E2E evidence.
- [x] Checklist references continuation URL shape + redirect base env; does **not** invent spa product routes/components.
- [x] `Skill declared: test-master` present.

## Where to change

`docs/ops/` (e.g. `r3-p1-08-spa-https-continuation-gate.md`); optional cross-link from `wave1-gate-checklist.md` without replacing it.

## Verification commands

```bash
test -f doge-ai-bridge/docs/ops/wave1-gate-checklist.md
rg -n "R3-P1-08|continuation_url|DOGESTONIA_DRAFT_REDIRECT" doge-ai-bridge/docs/ops --glob '*.md' || true
rg -n "def build_continuation_url" doge-ai-bridge/src/aibridge/gateway.py
```
