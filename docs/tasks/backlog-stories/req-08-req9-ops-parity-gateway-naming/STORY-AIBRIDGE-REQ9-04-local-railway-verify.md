# STORY-AIBRIDGE-REQ9-04 — Local + Railway verify (or residual)

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-04-local-railway-verify`
- **Status:** P5 Done · TASKED=0 · WAIVED G-01…G-04 · activation none · next **P7** (skip P6) · Lock **C** residual Y · 2026-09-26T13:08:56Z
- **Parent REQ:** [`REQ-08`](../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §5 · §6
- **Tech-arch:** [`04-verify-and-topology-sync.md`](../../../../../docs/architecture/req9-ops-naming/04-verify-and-topology-sync.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [01](STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md) · [02](STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) · [03](STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md) · soft `code-documenter`
- **Operator lock (Railway):** **C** — execute set/verify of vars named in 03; or record residual if project/service id Unknown — **no invent SUCCESS**
- **Emitted:** 2026-09-26T12:02:45Z
- **P1 materialize:** 2026-09-26T12:58:34Z · [p1 draft](../../../../../.cursor/plans/p1_aibridge_req9_04_scaffold_20260926T125740Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming/stories/STORY-AIBRIDGE-REQ9-04-local-railway-verify/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md)

## Scope
- Local: `make serve`/`dev` on 8080; curl `/health` + `/ready`; config/template show `GATEWAY_BASE_URL`, `GATEWAY_SERVICE_API_TOKEN`, `SPA_BASE_URL`.
- Railway: apply/verify var names+values per tech-arch 03/04 (generate/set allowed; operator rotates later) **or** explicit residual if service id Unknown (REQ §6).
- Evidence note (no secrets): UTC time, SHA/deploy, pass/fail, probe results. Suggested path pattern: `docs/ops/req-08-req9-verify-YYYYMMDD.md` (create at verify time — name ≠ create now).

## Out of scope
- Inventing Railway project/service id; expanding smoke beyond `/health`/`/ready` unless implement chooses (REQ §6 TBD).
- Re-doing hard-cut code from 03.

## Verified current state
- Railway: project `DOGEstonia` · service `doge-ai-bridge` · env `tallinn-demo` (MCP+CLI 2026-09-26).
- Target vars set+verified; remote `/health`/`/ready` **404** residual (live `/healthz`/`/readyz` 200).
- Evidence: [`docs/ops/req-08-req9-verify-20260926.md`](../../../ops/req-08-req9-verify-20260926.md).

## Target / AC
- [x] Local verify per tech-arch 04
- [x] Railway verify **or** residual explicitly recorded
- [x] REQ-08 §5 G9 local+Railway verify clause satisfied or residual linked

## Dependencies
- Requires **01**, **02**, **03** Done/Implemented
