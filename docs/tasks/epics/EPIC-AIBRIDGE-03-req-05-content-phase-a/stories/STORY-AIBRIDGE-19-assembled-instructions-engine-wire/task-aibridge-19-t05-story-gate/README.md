# Task: gate — story acceptance (§4.1 AC + XOR prefix)

**Status:** Done  
**Skill declared:** python-pro  
**Composition note:** fastapi-expert  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`  
**Parent story:** [`STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md`](../STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md)  
**P1 scaffold:** 2026-09-16T12:04:31Z  
**Maps:** Target #1–#2 · XOR

## Purpose

Close STORY-19 only when REQ-05 §4.1 holds: `prompt_channel=prefix`, assembled text in stable prefix, XOR (no API `instructions=`), and strict tool on interview path when schema id/version yield `strict_tool`. Produce story acceptance gate per template after live verify.

## Code Facts (verified exists — P1)

1. XOR assert: `interview.py:111–112` (`"instructions" not in request.payload` when prefix).
2. Gate template: `docs/methodology/Zeya888-builder-queue/templates/story-acceptance-gate-template.md`.
3. Pkg: `pkg-000016-20260916-epic-aibridge-03-story-19-assembled-instructions-engine-wire.yaml`.

## AC/DoD

- [x] Target #1–#2 evidenced (tests and/or recorded ASGI/request payload proof).
- [x] Story acceptance gate file filled with live Date after `--verify` in execution session.
- [x] `Skill declared: python-pro` present.

## Where to change

`acceptance-verification-task-aibridge-19-t05-story-gate.md` (sibling of pipeline story); tests under `tests/` in P3 (not P1).

## Verification commands

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify --check-dates
# P3: pytest proving prefix XOR + non-empty instructions when content_configured
```
