# STORY-AIBRIDGE-13 — Wave-1 ASGI E2E (fake/dry-run + Postgres)

## Meta
- **Key:** `STORY-AIBRIDGE-13-wave1-asgi-e2e`
- **Status:** Done (P3 · P6 audit CLOSED · next P7)
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §2 · P0-12 · §4 AC (wave 1)
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Pipeline:** [`../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md`](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md)
- **Siblings:** [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md)–[12](STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md)
- **Active pkg:** `pkg-000011-20260913-epic-aibridge-02-story-13-wave1-asgi-e2e.yaml`
- **P1 materialize:** 2026-09-13T16:34:47Z
- **P3 Done:** 2026-09-13T16:49:42Z
- **P6 Done:** 2026-09-13T16:58:55Z

## Scope
- Automated ASGI E2E with fake OpenAI + fake/dry-run gateway transports + real disposable Postgres.
- Prove REQ-03 §4 AC #1–#9 for wave 1 (no real `POST /story-drafts`).
- Transport replay returns stored HTTP status + body; every success/replay/non-2xx conforms to `docs/openapi/aibridge-channel-v1.openapi.yaml`.

## Вне scope
- Live Telegram/n8n (15); real gateway (after 14); SPA device E2E (17).

## Verified current state (post-P3 / P6)
- E2E suite green: `tests/test_story_13_wave1_asgi_e2e.py` + `tests/story13_e2e_helpers.py` + `tests/test_story_13_audit_gaps.py`.
- PG dedupe `try_begin`/`complete` on ASGI path; OpenAPI 401/409/500 samples; Send fail-closed wrong-owner/double-consume on PG.
- Remaining §4 #5 facets (expired token, mutated frozen body, etc.) remain covered by STORY-11 unit tests.

## Target / AC
- [x] E2E suite green without `"Received:"` replies.
- [x] AC #1–#9 demonstrated on fake/dry-run + Postgres (including restart replay where in-scope).
- [x] Zero real gateway stash in wave-1 proof.

## Dependencies
- [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [10](STORY-AIBRIDGE-10-responses-adapter-tools.md) · [11](STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) · [12](STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md)
