# Task: fixtures — generate VAL-002…018 matrix envelopes

**Status:** Done  
**P3 closed:** 2026-09-17T14:32:38Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-24-qa-json-schema-boundary.md`  
**Parent story:** [`STORY-AIBRIDGE-24-qa-json-schema-boundary.md`](../STORY-AIBRIDGE-24-qa-json-schema-boundary.md)  
**P1 scaffold:** 2026-09-17T14:26:09Z  
**Maps:** VAL-002…018 · envelope schema_version=1.0 · cluster `channel`

## Purpose

Generate VAL-002…018 envelopes (valid/invalid `/turns` + `/actions` bodies, Content-Length / Content-Type cases) into package `fixtures/` first, then **copy** each to `tests/fixtures/channel/`. Do not delete or move package originals. Mark VAL-014 / VAL-018 as characterization in notes.

**Out of this task:** implement pytest suites (t03); invent product trim/Content-Type policy; Railway invent.

## Code Facts (verified exists — post P3)

1. 17 `val-*.json` envelopes in package `fixtures/` + hash_eq copies under `tests/fixtures/channel/`.
2. Characterization notes on `val-whitespace-message` (VAL-014) and `val-missing-content-type` (VAL-018).
3. Package originals retained (promote=copy only).

## AC/DoD

- [x] Package `fixtures/` contains VAL-002…018 envelopes (schema_version=1.0 · matrix_ids · story_keys).
- [x] Matching **copies** exist under `tests/fixtures/channel/` (hash_eq).
- [x] Package originals remain; no move/delete.
- [x] Characterization VAL-014 / VAL-018 noted in envelope `notes`.
- [x] `Skill declared: test-master` present.

## Where to change

- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` — **Done**
- `tests/fixtures/channel/` — **Done**

## Verification commands

```bash
ls doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/val-*.json | wc -l
ls doge-ai-bridge/tests/fixtures/channel/val-*.json | wc -l
```
