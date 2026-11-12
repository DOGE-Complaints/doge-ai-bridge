# Task: docs — sync backlog Verified current state module path (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_01_audit_20260912`  
**Gap:** G-02 (Info) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-01-channel-facade-auth-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)  
**P5 scaffold:** 2026-09-12T20:41:08Z  
**P6 Done:** 2026-09-12T20:43:28Z

## Purpose

Sync backlog `$storyFile` §Verified current state: replace runtime module path **Unknown** with `src/aibridge/app.py` (`aibridge.app:app`) to match pipeline story + product layout.

**Out of this task:** product `src/` edits; inventing new AC; rewriting architecture package wholesale.

## Code Facts (verified exists — post P6)

1. Backlog §Verified current state → `src/aibridge/app.py` (`aibridge.app:app`) — `backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md`.
2. Pipeline + product module unchanged this task (docs-only).

## AC/DoD

- [x] Backlog §Verified current state module line matches pipeline (`src/aibridge/app.py` / `aibridge.app:app`).
- [x] No product source changes under `doge-ai-bridge/src/` for this task (G-01 changed `app.py` in prior gap-task only).
- [x] Story product AC / 🟢 Done status unchanged.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md` only

## Verification commands (P6)

```bash
rg -n 'Unknown|src/aibridge' doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md
```
