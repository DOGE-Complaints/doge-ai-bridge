# Task: implement — continuation URL + stash copy hygiene

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md`  
**P3 Done:** 2026-09-12T21:54:48Z
**Parent story:** [`STORY-AIBRIDGE-05-gateway-outcomes.md`](../STORY-AIBRIDGE-05-gateway-outcomes.md)

## Purpose

Build `continuation_url` from `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` **only** when outcome is `stashed`; stash reply/UX copy must never claim Story published (AC #5, #6 / REQ-01 §16).

**Out of this task:** full mobile SPA E2E (06); inventing redirect hosts.

## Code Facts (verified exists)

1. Channel envelope fields — `schemas.py` `draft_id`, `continuation_url`.
2. REQ-01 §16 URL shape: `{DOGESTONIA_DRAFT_REDIRECT_BASE_URL}/#/story/submit?draft_id=…`.
3. Current channel success sets `continuation_url=None` — `channel.py`.

## AC/DoD

- [x] `continuation_url` present only for `outcome=stashed` (uses redirect base + encoded draft_id).
- [x] Non-stashed outcomes omit continuation URL / draft_id as required.
- [x] Reply/copy never claims Story published on stash.
- [x] `Skill declared: python-pro` present.

## Where to change

- URL builder; channel/confirm success envelope; reply text.
- Settings for `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` if missing.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
# stashed → URL; other outcomes → no continuation; copy assertions
```
