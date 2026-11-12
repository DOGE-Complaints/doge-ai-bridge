# STORY-AIBRIDGE-12 — Env + `/readyz` + 500 + dry-run gate

## Meta
- **Key:** `STORY-AIBRIDGE-12-readyz-env-dryrun-gate`
- **Status:** Done (P3 · P6 audit CLOSED · next P7)
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §2 · §5.5–5.6 · P0-11
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [13](STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [14](STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)

## Scope
- Canonical `DOGESTONIA_INTAKE_BASE_URL` (mandatory HTTPS intake origin; no `API_BASE_URL` / `GATEWAY_ORIGIN` aliases).
- Settings accept TTL, max response bytes, timeouts, log level, rate limits, all LLM budget vars; `.env.example` matches.
- `/readyz`: config/DB/migration/bundle/tool/OpenAI **presence**/HTTPS origin syntax/distinct Bearers/redirect; **no** OpenAI generation; **no** gateway write; optional probes read-only/bounded/cached.
- Until R3-P1-03 (story 14): `AIBRIDGE_DRY_RUN=false` must **fail** readiness.
- Bounded JSON **500** channel envelope (REQ-03 P0-11 / AC #9).

## Вне scope
- Full schema validation implementation (14); inventing budget numeric defaults beyond «wired when set».

## Verified current state (post-P3 / P6)
- Strict `/readyz` via `src/aibridge/readiness.py` — auth, distinct Bearers, HTTPS `DOGESTONIA_INTAKE_BASE_URL` (mandatory; no API_BASE/GATEWAY_ORIGIN aliases), redirect base, OpenAI presence, store:false, dry-run gate until `AIBRIDGE_SCHEMA_VALIDATION_COMPLETE`, content/tool/migration checks; **no** OpenAI generation / **no** gateway write.
- Settings §5.6 knobs accepted and **enforced when set** (budgets → `BudgetGuard`, token/session TTL, HTTP timeouts, max response bytes, log level, rate limits → 429).
- Bounded channel JSON **500** — `Exception` handler on `/v1/channel/*`.
- Dry-run: `AIBRIDGE_DRY_RUN=false` → `/readyz` 503 (`dry_run_required`) until story 14 lifts via schema-complete flag.

## Target / AC
- [x] §5.5 and §5.6 satisfied.
- [x] Dry-run readiness gate until story 14 P1-03 complete.
- [x] Unhandled errors → bounded channel JSON 500 conforming to OpenAPI.

## Точки в коде
- `src/aibridge/app.py`, `config.py`, `readiness.py`, `budgets.py`, `rate_limit.py`, `gateway.py`, `.env.example`

## Dependencies
- [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) (migration version check)
