# Task: gate — story acceptance (REQ-05 §4.2)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P1 scaffold:** 2026-09-16T12:28:09Z  
**P3 Done:** 2026-09-16T12:32:27Z  
**Maps:** Target #1–#3 · R5-A-02

## Purpose

Close STORY-20 only when REQ-05 §4.2 holds: completeness, layer order, pack JSON in `files[]`, load succeeds. Produce story acceptance gate per template after live verify.

## Code Facts (verified exists — P1)

1. Gate template: `docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md`.
2. Pkg: `pkg-000017-20260916-epic-aibridge-03-story-20-full-instructions-manifest.yaml`.

## AC/DoD

- [x] Target #1–#3 evidenced (tests and/or recorded load proof).
- [x] Story acceptance gate file filled with live Date after `--verify` in execution session.
- [x] `Skill declared: python-pro` present.

## Where to change

`acceptance-verification-task-aibridge-20-t05-story-gate.md` (sibling of pipeline story); tests under `tests/` in P3 (not P1).

## Verification commands

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
```
