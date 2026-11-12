# STORY-AIBRIDGE-04 — Dual-confirm FSM + action tokens

## Meta
- **Key:** `STORY-AIBRIDGE-04-dual-confirm-tokens`
- **Status:** Done
- **Parent REQ:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §13
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Siblings:** [03](STORY-AIBRIDGE-03-responses-tool-budgets.md) · [05](STORY-AIBRIDGE-05-gateway-outcomes.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **P3 Done:** 2026-09-12T21:40:45Z · gate PASS · pytest 70 passed, 1 skipped

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Dual-confirm, action tokens, tool intent vs permission | [03-confirm-gateway.md §1–§3](../../../architecture/runtime/03-confirm-gateway.md) |
| Wave 1 vs wave 2 (confirm without full SPA E2E in wave 1) | [03-confirm-gateway.md §6](../../../architecture/runtime/03-confirm-gateway.md); [00-overview.md §7](../../../architecture/runtime/00-overview.md) |
| Two human decisions, canonical states, tokens, verify, Edit/Cancel | REQ-01 [§13 AIB-CONF-01…04](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Callback `token` ≤64 bytes / n8n keyboard mapping | [01-channel-facade.md §3](../../../architecture/runtime/01-channel-facade.md); [`n8n-channel-workflow/README.md`](../../../ops/n8n-channel-workflow/README.md) |
| Channel `/actions` statuses | REQ-01 [§6 AIB-CH-03 / AIB-CH-05](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Principal ≠ Identity federation | [00-overview.md §10](../../../architecture/runtime/00-overview.md); REQ-02 out of scope |

## Scope
- Explicit FSM states and permitted transitions per AIB-CONF-01A.
- Interpretation confirm ≠ Send; only Send may authorize gateway (call site gated; HTTP executor in 05).
- Opaque action tokens ≤64 UTF-8 bytes; store hash; bind principal / session / revision / expiry.
- Edit invalidates prior Send tokens; Cancel cancels; ownership checks on `/v1/channel/actions`.

## Вне scope
- Actual gateway `POST /story-drafts` (05); inventing n8n workflow JSON export body.

## Verified current state
- FSM + tokens + ConfirmationGuard on disk; `/actions` fail-closed.
- Live gateway HTTP: **Absent** (story 05).

## Target / AC
- [x] Interpretation confirm produces no gateway HTTP.
- [x] Invalid / expired / foreign / consumed token → 4xx per §6 statuses; fail closed.
- [x] Callback payload contains only opaque token ≤64 UTF-8 bytes.
- [x] Content edit increments revision and invalidates prior Send tokens.
- [x] Tool intent alone never equals Send permission ([03-confirm-gateway.md §3](../../../architecture/runtime/03-confirm-gateway.md)).

## Точки в коде
- `src/aibridge/{confirm_fsm,action_tokens,confirm,channel,app}.py`

## Dependencies
- [STORY-AIBRIDGE-03](STORY-AIBRIDGE-03-responses-tool-budgets.md).
