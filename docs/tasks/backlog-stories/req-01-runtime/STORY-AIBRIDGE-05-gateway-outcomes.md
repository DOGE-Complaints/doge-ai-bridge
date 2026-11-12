# STORY-AIBRIDGE-05 — Gateway executor, dry-run, outcomes

## Meta
- **Key:** `STORY-AIBRIDGE-05-gateway-outcomes`
- **Status:** Done (P3 2026-09-12T21:54:48Z)
- **Parent REQ:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §15–§16; AIB-HTTP-05
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Siblings:** [04](STORY-AIBRIDGE-04-dual-confirm-tokens.md) · [06](STORY-AIBRIDGE-06-ops-wave1-proof.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Wire contract:** [`story-intake-actions.openapi.yaml`](../../../openapi/story-intake-actions.openapi.yaml)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Gateway execution, `unknown_outcome` rules | [03-confirm-gateway.md §5](../../../architecture/runtime/03-confirm-gateway.md) |
| Constrained HTTPS, gateway Bearer, 201 verify, outcome map, idempotency | REQ-01 [§15 AIB-HTTP-01…05](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Continuation URL (SPA base env) | REQ-01 [§16](../../../requirements/REQ-01-doge-ai-bridge-runtime.md); [00-overview.md §2 topology](../../../architecture/runtime/00-overview.md) |
| Dry-run / wave-1 without stash | [03-confirm-gateway.md §6](../../../architecture/runtime/03-confirm-gateway.md); [00-overview.md §7](../../../architecture/runtime/00-overview.md) |
| Operator reconciliation | [`unknown-outcome-reconciliation.md`](../../../runbooks/unknown-outcome-reconciliation.md) |
| Secrets: channel Bearer ≠ gateway Bearer | [04-ops-security.md §4](../../../architecture/runtime/04-ops-security.md); REQ-01 [§7 / §15](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Stash ≠ Story published | REQ-01 [§1–§2 / acceptance](../../../requirements/REQ-01-doge-ai-bridge-runtime.md); [ARCH-RECOMMENDATIONS](../../../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md) |

## Scope
- Constrained HTTPS to configured gateway origin; TLS verify; no redirects; gateway Bearer only in executor.
- Success only verified **201** + `draft_id` + `trace_id` per wire OAS.
- Outcome mapping incl. `unknown_outcome`, `contract_mismatch`, `blocked_by_confirmation`.
- `AIBRIDGE_DRY_RUN` skips real stash (local validation path only).
- No automatic retry same revision after ambiguous delivery; continuation URL only if `stashed`.
- Link operator path to unknown-outcome runbook.

## Вне scope
- Gateway idempotency extension beyond REQ; inventing gateway lookup API; full wave-2 mobile SPA E2E (06 / later).

## Verified current state
- Runbook on disk: `docs/runbooks/unknown-outcome-reconciliation.md`.
- Wire OAS on disk; `GatewayExecutor` + recorded transport — `src/aibridge/gateway.py` (P3).

## Target / AC
- [x] Channel Bearer never used as gateway Bearer.
- [x] Dry-run: Send path validates locally without `POST /story-drafts`.
- [x] Malformed 201 → not `stashed`.
- [x] `unknown_outcome` blocks auto Send retry for same revision.
- [x] Stash copy / UX never claims Story published.
- [x] Continuation URL uses `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` only when outcome is `stashed`.

## Точки в коде
- `src/aibridge/{gateway,confirm,confirm_fsm,channel,config}.py` · `tests/test_gateway_outcomes.py`

## Dependencies
- [STORY-AIBRIDGE-04](STORY-AIBRIDGE-04-dual-confirm-tokens.md).
