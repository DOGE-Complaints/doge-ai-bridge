# STORY-AIBRIDGE-04 — Dual-confirm FSM + action tokens

## Meta
- **Key:** `STORY-AIBRIDGE-04-dual-confirm-tokens`
- **Status:** 🟢 Done
- **Parent Epic:** [`EPIC-AIBRIDGE-01-req-01-runtime.md`](../../EPIC-AIBRIDGE-01-req-01-runtime.md)
- **source:** `backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md`
- **decision_ref:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-04-dual-confirm-tokens.md) · [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §13 · [`03-confirm-gateway.md`](../../../../../architecture/runtime/03-confirm-gateway.md) · [`01-channel-facade.md`](../../../../../architecture/runtime/01-channel-facade.md)
- **Parent REQ:** [`REQ-01`](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §13
- **Package:** [`req-01-runtime/INDEX.md`](../../../../backlog-stories/req-01-runtime/INDEX.md)
- **Siblings:** [03](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md) · [05](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-05-gateway-outcomes.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000004-20260912-epic-aibridge-01-story-04-dual-confirm.yaml`
- **P1 materialize:** 2026-09-12T21:34:18Z
- **P3 Done:** 2026-09-12T21:40:45Z
- **Gate:** [acceptance-verification … t06](acceptance-verification-task-aibridge-01-04-t06-story-acceptance-verification.md) PASS
- **Run summary:** [run-summary-20260912-2140-story-aibridge-04-p3.md](../../../../run-reports/run-summary-20260912-2140-story-aibridge-04-p3.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Dual-confirm, action tokens, tool intent vs permission | [03-confirm-gateway.md §1–§3](../../../../../architecture/runtime/03-confirm-gateway.md) |
| Wave 1 vs wave 2 (confirm without full SPA E2E in wave 1) | [03-confirm-gateway.md §6](../../../../../architecture/runtime/03-confirm-gateway.md); [00-overview.md §7](../../../../../architecture/runtime/00-overview.md) |
| Two human decisions, canonical states, tokens, verify, Edit/Cancel | REQ-01 [§13 AIB-CONF-01…04](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Callback `token` ≤64 bytes / n8n keyboard mapping | [01-channel-facade.md §3](../../../../../architecture/runtime/01-channel-facade.md); [`n8n-channel-workflow/README.md`](../../../../../ops/n8n-channel-workflow/README.md) |
| Channel `/actions` statuses | REQ-01 [§6 AIB-CH-03 / AIB-CH-05](../../../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Principal ≠ Identity federation | [00-overview.md §10](../../../../../architecture/runtime/00-overview.md); REQ-02 out of scope |

## Scope
- Explicit FSM states and permitted transitions per AIB-CONF-01A.
- Interpretation confirm ≠ Send; only Send may authorize gateway (call site gated; HTTP executor in 05).
- Opaque action tokens ≤64 UTF-8 bytes; store hash; bind principal / session / revision / expiry.
- Edit invalidates prior Send tokens; Cancel cancels; ownership checks on `/v1/channel/actions`.

## Вне scope
- Actual gateway `POST /story-drafts` (05); inventing n8n workflow JSON export body.

## Verified current state
- Dual-confirm FSM — `src/aibridge/confirm_fsm.py` (AIB-CONF-01A).
- Action tokens hash store — `src/aibridge/action_tokens.py` (≤64 UTF-8; TTL 15m).
- ConfirmationGuard — `src/aibridge/confirm.py`; `/v1/channel/actions` fail-closed 403/404/409.
- Gateway HTTPS executor: **Absent** (story 05); Send sets `gateway_authorized` call-site only.

## Target / AC
- [x] Interpretation confirm produces no gateway HTTP.
- [x] Invalid / expired / foreign / consumed token → 4xx per §6 statuses; fail closed.
- [x] Callback payload contains only opaque token ≤64 UTF-8 bytes.
- [x] Content edit increments revision and invalidates prior Send tokens.
- [x] Tool intent alone never equals Send permission ([03-confirm-gateway.md §3](../../../../../architecture/runtime/03-confirm-gateway.md)).

## Точки в коде
- `src/aibridge/{confirm_fsm,action_tokens,confirm,channel,app}.py`

## Dependencies
- [STORY-AIBRIDGE-03](../../../../backlog-stories/req-01-runtime/STORY-AIBRIDGE-03-responses-tool-budgets.md).

## Nested tasks (pkg-000004 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-01-04-t01-confirm-fsm-states](./task-aibridge-01-04-t01-confirm-fsm-states/README.md) | Scope #1 | Done |
| t02 | [task-aibridge-01-04-t02-interpret-vs-send-gate](./task-aibridge-01-04-t02-interpret-vs-send-gate/README.md) | Scope #2; AC #1,#5 | Done |
| t03 | [task-aibridge-01-04-t03-action-token-store](./task-aibridge-01-04-t03-action-token-store/README.md) | Scope #3; AC #3 | Done |
| t04 | [task-aibridge-01-04-t04-edit-cancel-ownership](./task-aibridge-01-04-t04-edit-cancel-ownership/README.md) | Scope #4; AC #4 | Done |
| t05 | [task-aibridge-01-04-t05-actions-fail-closed-4xx](./task-aibridge-01-04-t05-actions-fail-closed-4xx/README.md) | AC #2 | Done |
| t06 | [task-aibridge-01-04-t06-story-acceptance-verification](./task-aibridge-01-04-t06-story-acceptance-verification/README.md) | AC #1–#5 gate | Done |
