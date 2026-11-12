# Task: implement — bundle GC + multi-repo CI packaging docs

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md`  
**Parent story:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../STORY-AIBRIDGE-02-content-bundle-registry.md)

## Purpose

GC deletes a bundle only if no active sessions reference it **and** audit/recovery grace has elapsed (arch rules). Docs/CI note: multi-repo checkout → tarball → image (not fragile monorepo `COPY` alone). Absolute CI paths remain **Unknown** until pinned — document as Unknown/env; do not invent.

**Out of this task:** Railway Volume as content store; REQ-02 federation.

## Code Facts (verified exists)

1. GC rules — `02-content-packaging.md` §4 rule 6 / §5–§6.
2. CI shape — `02-content-packaging.md` §3.
3. Absolute paths Unknown — `00-overview.md` §13.

## AC/DoD

- [ ] GC skips hashes still referenced by active sessions (AC #2).
- [ ] Grace honored before delete.
- [ ] CI packaging note present (multi-repo → tarball → image).
- [ ] `Skill declared: python-pro` present.

## Where to change

- GC function under `src/aibridge/`.
- Prefer sync existing `docs/architecture/runtime/02-content-packaging.md` (or ops note) — no invented absolute paths.

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q
rg -n 'multi-repo|tarball|GC|grace' doge-ai-bridge/docs/architecture/runtime/02-content-packaging.md
```
