# STORY-AIBRIDGE-14 — P1 ops + full schema + restart tests

## Meta
- **Key:** `STORY-AIBRIDGE-14-p1-ops-schema-restart`
- **Status:** 🟢 Done (P3 · P6 audit CLOSED · next P7)
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6 P1-01–04 · P1-06–07 (P1-05 superseded by P0-13)
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [12](STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) · [13](STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [16](STORY-AIBRIDGE-16-privacy-retention.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)  
  Dockerfile slice: `devops-engineer` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md)

## Scope
- Graceful shutdown (AIB-OPS-03 / R3-P1-01).
- Channel **429** / rate limits + finite budget defaults; budgets enforced on `/turns` (R3-P1-02).
- **Full schema validation** (enum etc.); blocks real gateway readiness (R3-P1-03) — lifts dry-run-only gate from story 12 / REQ-03 §2.
- Restart recovery + DB race/restart tests: Send / pending-confirm / `unknown_outcome` (R3-P1-04; AC #7–#8).
- Gateway response-size limit / remaining §17 timeout knobs (R3-P1-06).
- Dockerfile for reproducible deploy / node clone (R3-P1-07).

## Вне scope
- Dual instructions (done in 10 / P0-13); n8n live gate (15); privacy (16); SPA E2E (17); P2 (18).

## Verified current state
- Dockerfile: present at repo root (P3).
- Full schema validation (enum/const/bounds) + dry-run readiness lift via `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE`.
- Finite rate/budget defaults; graceful shutdown lifespan; restart/race tests (in-memory + disposable-PG P6).
- Gateway connect timeout from Settings wired to httpx (P6 G-02).
- `schema_validation_complete()` is real enum/const probe (P6 G-03).

## Target / AC
- [x] R3-P1-01,02,03,04,06,07 closed with tests/evidence.
- [x] `AIBRIDGE_DRY_RUN=false` may pass readiness only after full schema validation is proven.
- [x] Restart/race tests cover AC #7–#8.

## Dependencies
- [13](STORY-AIBRIDGE-13-wave1-asgi-e2e.md)
