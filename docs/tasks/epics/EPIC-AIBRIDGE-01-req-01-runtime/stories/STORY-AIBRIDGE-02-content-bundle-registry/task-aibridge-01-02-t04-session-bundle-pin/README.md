# Task: implement — session content_bundle_hash pin and resume

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)

## Purpose

Session stores FK `content_bundle_hash`; resume loads **pinned** bundle, not “current on disk”. Minimal session persistence sufficient for pin/resume proof (full interview FSM = later stories).

**Out of this task:** dual-confirm FSM (04); gateway stash (05).

## Code Facts (verified exists)

1. Session pin rules — `02-content-packaging.md` §4 rules 4–5; REQ-01 §14.
2. No session model in `src/` yet.
3. Depends on t02 `content_bundle` rows.

## AC/DoD

- [ ] Session resume uses pinned `content_bundle_hash` (AC #5).
- [ ] Redeploy with new bundle does not delete prior hash while a session still references it (AC #2 — retention).
- [ ] `Skill declared: python-pro` present.

## Where to change

- Session model + load path under `src/aibridge/`.

## Verification commands

```bash
# Create session on hash A, register hash B, resume still loads A
cd doge-ai-bridge && .venv/bin/pytest -q
```
