# Task: gate — story acceptance verification (STORY-AIBRIDGE-17)

**Status:** Done  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`  
**Parent story:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../STORY-AIBRIDGE-17-spa-https-continuation-e2e.md)  
**P1 scaffold:** 2026-09-13T18:20:16Z
**P3 Done:** 2026-09-13T18:23:58Z  
**Maps:** Target AC gate

## Purpose

Close the story only when Target AC #1–#2 are evidenced (linked spa pack **or** explicit BLOCKED residual + dashboard wave-2 blocked language). Produce story-level acceptance gate per template.

## Code Facts (verified exists — P1)

1. Gate template: `docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md`.
2. Parent Target AC are two checkboxes on the pipeline/backlog story.
3. pkg paths: `pkg-000015-20260913-epic-aibridge-02-story-17-spa-https-continuation-e2e.yaml`.

## AC/DoD

- [x] Story acceptance gate file filled with live Date after `--verify` + evidence check in the execution session.
- [x] AC #1 and #2 each PASS or documented BLOCKED residual (no invented spa PASS).
- [x] `Skill declared: test-master` present.

## Where to change

`acceptance-verification-task-aibridge-02-17-t05-story-acceptance-verification.md` (sibling of pipeline story); pipeline Target checkboxes.

## Verification commands

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
# evidence / BLOCKED paths from t04; dashboard language from t03
```
