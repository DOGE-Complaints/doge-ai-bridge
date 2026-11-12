# STORY-AIBRIDGE-02 — Content bundle + Postgres registry + GC

## Meta
- **Key:** `STORY-AIBRIDGE-02-content-bundle-registry`
- **Status:** 🟢 Done
- **Parent Epic:** [`EPIC-AIBRIDGE-01-req-01-runtime.md`](../../EPIC-AIBRIDGE-01-req-01-runtime.md)
- **source:** `backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md`
- **decision_ref:** [`STORY-AIBRIDGE-02-content-bundle-registry.md`](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-02-content-bundle-registry.md) · [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §8, §14, §18 · [`02-content-packaging.md`](../../../../../architecture/runtime/02-content-packaging.md)
- **Parent REQ:** [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §8, §14 (`content_bundle`), §18 hashes
- **Package:** [`req-01-runtime/INDEX.md`](../../../../backlog-stories/req-01-runtime/INDEX.md)
- **Siblings:** [01](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md) · [03](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md) …
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Wire OAS (pin into bundle, not channel):** [`story-intake-actions.openapi.yaml`](../../../../../openapi/story-intake-actions.openapi.yaml)
- **Active pkg (wave):** `pkg-000002-20260912-epic-aibridge-01-story-02-content-bundle.yaml`
- **P1 materialize:** 2026-09-12T20:56:43Z
- **P3 Done:** 2026-09-12T21:03:47Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Ownership matrix, packaging & verify | [00-overview.md §4–§5](../../../../../architecture/runtime/00-overview.md) |
| Bundle contents, multi-repo CI, Postgres registry+GC, verify surfaces | [02-content-packaging.md](../../../../../architecture/runtime/02-content-packaging.md) (§1–§6) |
| Instruction bundle + manifest + Docker delivery | REQ-01 [§8 AIB-INS-01…04](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Persistence: `content_bundle`, session FK, uniqueness, retention | REQ-01 [§14 AIB-DB-01…04](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Startup validation / hashes on `/readyz` | REQ-01 [§18 AIB-OPS-01](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md); [04-ops-security.md §1](../../../../../architecture/runtime/04-ops-security.md) |
| Node scaling: one deploy = one node; no civic hardcode | [00-overview.md §10](../../../../../architecture/runtime/00-overview.md); [ARCH-RECOMMENDATIONS](../../../../../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md) |
| Absolute CI instruction/pack paths | **Unknown** — [00-overview.md §13](../../../../../architecture/runtime/00-overview.md) |

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
- Instruction/pack absolute CI paths: **Unknown** (env placeholders).
- Content loader: `src/aibridge/content.py` (local FS only).
- Registry: `src/aibridge/registry.py` (Memory + Sqlite + **Postgres**/psycopg); sessions pin in `sessions.py`.
- GC: `src/aibridge/bundle_gc.py` (library; operator trigger documented in arch §4).
- `/readyz` content verify: `src/aibridge/app.py` + `deployment.py`.
- Tests: pytest **34 passed, 1 skipped** (2026-09-12T21:13:50Z; live postgres mark skipped without DSN).
- P6 audit: G-01/G-02 CLOSED (t07/t08).

## Target / AC
- [x] Missing/mismatched artifacts → `/readyz` not ready.
- [x] Redeploy with new bundle does not delete prior hash while a session still references it.
- [x] Bundle row immutable after register; uniqueness on `bundle_hash`.
- [x] No GitHub fetch of instructions at request time.
- [x] Session resume uses pinned `content_bundle_hash`.

## Точки в коде
- `src/aibridge/content.py`, `registry.py`, `sessions.py`, `bundle_gc.py`, `deployment.py`, `app.py`, `config.py`
- Fixtures: `tests/fixtures/content/`
- Dependency: story 01 ASGI — `src/aibridge/app.py`.

## Dependencies
- [STORY-AIBRIDGE-01](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md) (ASGI + DB connectivity shell).

## Nested tasks (pkg-000002 order + P5 audit override)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-01-02-t01-content-load-hash-pin](./task-aibridge-01-02-t01-content-load-hash-pin/README.md) | Scope #1–#2; AC #4 | Done |
| t02 | [task-aibridge-01-02-t02-postgres-bundle-registry](./task-aibridge-01-02-t02-postgres-bundle-registry/README.md) | Scope #3; AC #3 | Done |
| t03 | [task-aibridge-01-02-t03-readyz-bundle-verify](./task-aibridge-01-02-t03-readyz-bundle-verify/README.md) | Scope #3; AC #1 | Done |
| t04 | [task-aibridge-01-02-t04-session-bundle-pin](./task-aibridge-01-02-t04-session-bundle-pin/README.md) | Scope #4; AC #2,#5 | Done |
| t05 | [task-aibridge-01-02-t05-bundle-gc-ci-docs](./task-aibridge-01-02-t05-bundle-gc-ci-docs/README.md) | Scope #5–#6; AC #2 | Done |
| t06 | [task-aibridge-01-02-t06-story-acceptance-verification](./task-aibridge-01-02-t06-story-acceptance-verification/README.md) | AC #1–#5 gate | Done |
| t07 | [task-aibridge-01-02-t07-audit-g01-postgres-adapter](./task-aibridge-01-02-t07-audit-g01-postgres-adapter/README.md) | P5 G-01 | Done |
| t08 | [task-aibridge-01-02-t08-audit-g02-gc-docs-t02-readme](./task-aibridge-01-02-t08-audit-g02-gc-docs-t02-readme/README.md) | P5 G-02 | Done |
