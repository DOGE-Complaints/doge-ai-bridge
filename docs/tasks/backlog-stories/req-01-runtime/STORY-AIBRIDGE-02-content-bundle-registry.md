# STORY-AIBRIDGE-02 — Content bundle + Postgres registry + GC

## Meta
- **Key:** `STORY-AIBRIDGE-02-content-bundle-registry`
- **Status:** Done
- **Parent REQ:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §8, §14 (`content_bundle`), §18 hashes
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Siblings:** [01](STORY-AIBRIDGE-01-channel-facade-auth.md) · [03](STORY-AIBRIDGE-03-responses-tool-budgets.md) …
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Wire OAS (pin into bundle, not channel):** [`story-intake-actions.openapi.yaml`](../../../openapi/story-intake-actions.openapi.yaml)
- **Pipeline:** [`../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-02-content-bundle-registry/STORY-AIBRIDGE-02-content-bundle-registry.md`](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-02-content-bundle-registry/STORY-AIBRIDGE-02-content-bundle-registry.md)
- **P3 Done:** 2026-09-12T21:03:47Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Ownership matrix, packaging & verify | [00-overview.md §4–§5](../../../architecture/runtime/00-overview.md) |
| Bundle contents, multi-repo CI, Postgres registry+GC, verify surfaces | [02-content-packaging.md](../../../architecture/runtime/02-content-packaging.md) (§1–§6) |
| Instruction bundle + manifest + Docker delivery | REQ-01 [§8 AIB-INS-01…04](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Persistence: `content_bundle`, session FK, uniqueness, retention | REQ-01 [§14 AIB-DB-01…04](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Startup validation / hashes on `/readyz` | REQ-01 [§18 AIB-OPS-01](../../../requirements/REQ-01-doge-ai-bridge-runtime.md); [04-ops-security.md §1](../../../architecture/runtime/04-ops-security.md) |
| Node scaling: one deploy = one node; no civic hardcode | [00-overview.md §10](../../../architecture/runtime/00-overview.md); [ARCH-RECOMMENDATIONS](../../../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md) |
| Absolute CI instruction/pack paths | **Unknown** — [00-overview.md §13](../../../architecture/runtime/00-overview.md) |

## Scope
- Load manifest-listed instruction roots; hash; pin `DOGESTONIA_CONTENT_SOURCE_COMMIT`.
- Wire OAS path = `story-intake-actions.openapi.yaml`; pack schema path via env (one pack per deploy).
- Startup verify → **register-once** `content_bundle` by `bundle_hash` (immutable row).
- Session FK `content_bundle_hash`; resume uses pinned bundle (not “whatever is current on disk”).
- GC only if no active sessions + grace (see arch registry rules).
- CI/docs note: multi-repository checkout → tarball → image (not fragile monorepo `COPY` alone).

## Вне scope
- Responses tool generation (03); inventing instruction filenames; Railway Volume as content store; REQ-02 federation.

## Verified current state
- Wire OAS: `docs/openapi/story-intake-actions.openapi.yaml` (`postStoryDraftStash`).
- Instruction/pack absolute CI paths: **Unknown** (env).
- Modules: `src/aibridge/content.py`, `registry.py`, `sessions.py`, `bundle_gc.py`, `deployment.py`; `/readyz` in `app.py`.
- Registry offline store: Memory + Sqlite; Postgres URL adapter deferred.
- Tests: pytest **31 passed** (2026-09-12T21:03:47Z).

## Target / AC
- [x] Missing/mismatched artifacts → `/readyz` not ready.
- [x] Redeploy with new bundle does not delete prior hash while a session still references it.
- [x] Bundle row immutable after register; uniqueness on `bundle_hash`.
- [x] No GitHub fetch of instructions at request time.
- [x] Session resume uses pinned `content_bundle_hash`.

## Точки в коде
- `src/aibridge/content.py`, `registry.py`, `sessions.py`, `bundle_gc.py`, `deployment.py`, `app.py`, `config.py`

## Dependencies
- [STORY-AIBRIDGE-01](STORY-AIBRIDGE-01-channel-facade-auth.md) (ASGI + DB connectivity shell).
