# Task: fixtures — Gate-5 evidence pack or explicit defer

**Status:** Done · 2026-09-18T12:53:26Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md`  
**Parent story:** [`STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md`](../STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md)  
**P1 scaffold:** 2026-09-18T12:50:58Z  
**Maps:** Gate-5 · Layer F · ADR-Q1 promote=copy · gaps §37 T03

## Purpose

Collect redacted pilot evidence **or** (if no pilot env) explicit defer with reason in package `fixtures/meta/gate5-evidence-index.json` (status=deferred · capture-first). Promote=copy → `tests/fixtures/meta/`. Optional ops `live-evidence-*.md` paths indexed — **do not invent** live PASS / Railway SUCCESS / evidence bodies without operator pilot.

**Out of this task:** UC docs (t01); checklist map (t02); flipping Gate-5 off deferred without accepted pack (t04); product invent.

## AC/DoD

- [x] Package `gate5-evidence-index.json` present with accepted paths **or** explicit defer_reason.
- [x] Matching **copy** under `tests/fixtures/meta/` when index present; hash_eq vs package.
- [x] No invent live Telegram PASS / Railway SUCCESS / fake evidence bodies.
- [x] `Skill declared: test-master` present.

## Where to change

- package `fixtures/meta/gate5-evidence-index.json` + `tests/fixtures/meta/` promote=copy — **P3**
- optional ops `live-evidence-*.md` — operator / **P3**
