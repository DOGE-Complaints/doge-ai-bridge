# Task: fixtures — generate AUTH-002…012 envelopes + promote copies

**Status:** Done  
**P3 closed:** 2026-09-17T14:02:23Z  

**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`  
**Parent story:** [`STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md`](../STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md)  
**P1 scaffold:** 2026-09-17T13:59:06Z  
**Maps:** AUTH-002…012 · clusters channel/settings/spies · ADR-Q2 envelope

## Purpose

Generate remaining AUTH-002…012 envelopes into package `fixtures/` (TECH §8 prompts / envelope v1.0), then **copy** into `tests/fixtures/{channel,settings,spies}/`. Never delete/move package originals.

**Out of this task:** seed promote (t01); contract tests (t03); invent product auth behavior.

## Code Facts (verified exists — P1)

1. Envelope schema: TECH ADR-Q2 · §6.2 (`schema_version`, `cluster`, `fixture_id`, `matrix_ids`, …).
2. Clusters for story 23: `channel`, `settings`, `spies`.
3. Generation prompts: TECH §8 (channel/settings/spies).

## AC/DoD

- [x] Package `fixtures/` holds envelopes covering AUTH-002…012 (as needed by matrix).
- [x] Matching **copies** under `tests/fixtures/{channel,settings,spies}/`.
- [x] Originals not moved/deleted.
- [x] `Skill declared: test-master` present.

## Where to change

- `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/` (generate) — **P3**
- `tests/fixtures/{channel,settings,spies}/` (copies) — **P3**

## Verification commands

```bash
ls doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/fixtures/
ls doge-ai-bridge/tests/fixtures/channel/ doge-ai-bridge/tests/fixtures/settings/ doge-ai-bridge/tests/fixtures/spies/ 2>/dev/null || true
```
