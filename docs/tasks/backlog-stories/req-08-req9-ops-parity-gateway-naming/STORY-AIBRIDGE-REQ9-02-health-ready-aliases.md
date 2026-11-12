# STORY-AIBRIDGE-REQ9-02 — GET /health and /ready aliases

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-02-health-ready-aliases`
- **Status:** ✅ P6 Done · G-01/G-02 CLOSED · next **P7** · `run_mode=aibridge_req9_02_audit_20260926` · 2026-09-26T12:33:39Z
- **Parent REQ:** [`REQ-08`](../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §4 · G2
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md) (aliases OK over `/healthz` `/readyz`)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [01](STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) · [03](STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) · [04](STORY-AIBRIDGE-REQ9-04-local-railway-verify.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-09-26T12:02:45Z
- **P3 close:** 2026-09-26T12:27:23Z

## Scope
- Expose `GET /health` and `GET /ready` with same semantics as existing `/healthz` / `/readyz` (aliases OK; keep both paths unless implement documents otherwise).
- Update docs/runbooks that cite only `z` paths to list short paths as REQ9-primary.

## Out of scope
- Changing readiness evaluation logic; Makefile (01); env renames (03).

## Verified current state
- Routes: `/health` + `/healthz`, `/ready` + `/readyz` stacked in `src/aibridge/app.py` (P3).
- Parity tests: `tests/test_health.py` (7 passed).
- Runbooks: REQ9-primary short paths in web + pilot runbooks.

## Target / AC
- [x] G2: `GET /health` and `GET /ready` peer-parity probe semantics

## Code points
- `src/aibridge/app.py`; probe tests; runbooks citing `/healthz`/`/readyz`

## Dependencies
- None (∥ 01)
