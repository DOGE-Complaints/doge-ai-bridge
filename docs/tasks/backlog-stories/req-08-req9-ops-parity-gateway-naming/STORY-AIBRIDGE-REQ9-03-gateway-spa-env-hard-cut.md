# STORY-AIBRIDGE-REQ9-03 — GATEWAY_* + SPA_BASE_URL hard cut (R1 R2 R4 R8)

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut`
- **Status:** P6 Done · G-01 CLOSED · pkg-000047 · next **P7** · Lock **A** · 2026-09-26T12:53:50Z
- **Parent REQ:** [`REQ-08`](../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §2–§5 R1 R2 R4 R8
- **Tech-arch:** [`02-env-auth-url-naming.md`](../../../../../docs/architecture/req9-ops-naming/02-env-auth-url-naming.md) · [`03-coexistence-and-migration.md`](../../../../../docs/architecture/req9-ops-naming/03-coexistence-and-migration.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [01](STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) · [02](STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) · [04](STORY-AIBRIDGE-REQ9-04-local-railway-verify.md); gateway `STORY-GW-REQ9-01`; spa `STORY-SPA-REQ9-01`
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md) · soft `code-documenter` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/code-documenter/SKILL.md)
- **Operator lock:** **A** — full hard cut env **and** Python `Settings` fields/helpers; **no** dual-read
- **Operator lock (Railway):** **C** — this story documents **target Railway var names** checklist; live set/verify → [04](STORY-AIBRIDGE-REQ9-04-local-railway-verify.md)
- **Emitted:** 2026-09-26T12:02:45Z
- **P3 close:** 2026-09-26T12:46:12Z · [p3](../../run-reports/run-summary-20260926-1246-story-aibridge-req9-03-p3.md)
- **P6 close:** 2026-09-26T12:53:50Z · G-01 CLOSED · [p6](../../run-reports/run-summary-20260926-1253-story-aibridge-req9-03-p6.md)

## Scope
Hard cut (no dual-read of old names):

| From (remove) | To (primary) |
|---------------|--------------|
| `DOGESTONIA_INTAKE_BASE_URL` / `dogestonia_intake_base_url` (+ helpers) | `GATEWAY_BASE_URL` / `gateway_base_url` |
| `DOGESTONIA_API_BEARER_TOKEN` / `dogestonia_api_bearer_token` | `GATEWAY_SERVICE_API_TOKEN` / `gateway_service_api_token` (= gateway `SERVICE_API_TOKEN`) |
| `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` / draft-redirect fields | `SPA_BASE_URL` / `spa_base_url` |

- Update `.env.example`, runbooks, manuals, QA fixtures/tests.
- Keep `AIBRIDGE_CHANNEL_BEARER_TOKEN` distinct from gateway S2S (R8); readiness still fails if equal.
- Document Railway **target var names** (and pairing note) in ops checklist inside this story or linked runbook — **do not** require live Railway access for Done of 03.

## Out of scope
- Dual-read of removed env/Python names
- Renaming channel to `SERVICE_API_TOKEN`
- Product channel OpenAPI; invent waitlist
- Live Railway set/verify proof (→ 04)

## Verified current state
- Hard cut Done (P3): `config.py` aliases `GATEWAY_BASE_URL` / `GATEWAY_SERVICE_API_TOKEN` / `SPA_BASE_URL`; fields `gateway_base_url` / `gateway_service_api_token` / `spa_base_url`.
- Consumers: `readiness.py` · `gateway.py` (no dual-read getattr to removed names).
- `.env.example` + runbooks/manuals/checklist updated; Railway names §2.4.1 (live → 04).

## Railway target var names (checklist — Lock C)

| Var | Peer note |
|-----|-----------|
| `GATEWAY_BASE_URL` | HTTPS intake/gateway origin |
| `GATEWAY_SERVICE_API_TOKEN` | = gateway `SERVICE_API_TOKEN` value; ≠ channel Bearer (R8) |
| `SPA_BASE_URL` | SPA continuation base |
| `AIBRIDGE_CHANNEL_BEARER_TOKEN` | Keep — channel only |

Ops copy: [`aibridge-web-service-local-railway.md`](../../../runbooks/aibridge-web-service-local-railway.md) §2.4.1. Live set/verify → [04](STORY-AIBRIDGE-REQ9-04-local-railway-verify.md).

## Target / AC
- [x] R1 R2 R4 hard cut in config + template + docs + tests (env **and** Python)
- [x] R8 channel Keep and ≠ `GATEWAY_SERVICE_API_TOKEN`
- [x] No dual-read of removed names
- [x] Railway **names checklist** present (proof deferred to 04)

## Code points
- `src/aibridge/config.py`, `gateway.py`, `readiness.py`, `.env.example`, docs/runbooks/manuals, `tests/**`

## Dependencies
- Requires **01** and **02**
