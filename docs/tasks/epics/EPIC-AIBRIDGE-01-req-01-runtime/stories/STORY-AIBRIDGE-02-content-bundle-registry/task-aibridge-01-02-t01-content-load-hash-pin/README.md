# Task: implement — content load, hash, and source-commit pin

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)

## Purpose

Load manifest-listed instruction roots from **local** staged paths; compute hashes; pin `DOGESTONIA_CONTENT_SOURCE_COMMIT`; resolve wire OAS (`story-intake-actions.openapi.yaml`) + pack schema path via env (one pack per deploy). No invent of instruction filenames beyond manifest.

**Out of this task:** Postgres register (t02); session FK (t04); Responses tools (03); GitHub fetch at request time.

## Code Facts (verified exists)

1. Wire OAS on disk: `doge-ai-bridge/docs/openapi/story-intake-actions.openapi.yaml`.
2. ASGI app exists: `src/aibridge/app.py` (story 01).
3. No content loader / Postgres in `src/` yet (`rg` postgres/sqlalchemy = 0).
4. Absolute CI instruction/pack paths: **Unknown** — `00-overview.md` §13; use env placeholders, do not invent.

## AC/DoD

- [ ] Local-only load of manifest-listed roots; hashes computed.
- [ ] `DOGESTONIA_CONTENT_SOURCE_COMMIT` pinned.
- [ ] Wire OAS + pack schema env paths resolved (one pack per deploy).
- [ ] No GitHub fetch of instructions at request time (AC #4).
- [ ] `Skill declared: python-pro` present.

## Where to change

- New modules under `src/aibridge/` (content/bundle loader — path chosen at P3).
- `src/aibridge/config.py` env fields.

## Verification commands

```bash
# After implement: unit tests on hash/pin; rg -i 'github|fetch' on loader must not show request-time fetch
cd doge-ai-bridge && .venv/bin/pytest -q
```
