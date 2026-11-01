# Confirm + gateway Keep pipe (REQ-11 / STORY-56)

Thin runtime note — **Keep**, not a rewrite. Detail SSOT:

- Arch boundaries: [`../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md`](../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md)
- Confirm/gateway Keep: [`../architecture/runtime/03-confirm-gateway.md`](../architecture/runtime/03-confirm-gateway.md)

## What the pipe does (Present)

| Stage | Code | Must |
|-------|------|------|
| Interpretation confirm | `confirm.py` `offer_interpretation_confirm` / consume | Never authorize gateway HTTPS (**AC-AIB-11-01**) |
| Send confirm | `offer_send_confirm` / `CONFIRM_SEND` consume | Only path that may call stash |
| Action tokens | `action_tokens.py` + session `revision` / `draft_hash` | Reuse store — no parallel confirm schema |
| Tool-intent freeze | `set_frozen_tool_intent` | Intent ≠ stash permission |
| Gateway submit | `gateway.py` `GatewayExecutor.execute_stash` | URL + Bearer from config only (**AC-AIB-11-03**) |
| Success / failure | factual `STASHED` vs clear errors / `unknown_outcome` | User-visible success only after stash (**AC-AIB-11-04**); no blind resend |
| Continuation | `build_continuation_url` → `{SPA}/#/story/submit?draft_id=` | Only when stashed; copy ≠ Story published (**AC-AIB-11-05**) |
| Channel boundary | `channel.py` routes actions; executor owns Bearer | Bridge owns stash (**AC-AIB-11-06**) |

## Verify harness

`tests/test_story_56_keep_pipe_confirm_stash_spa.py` (+ Present `tests/test_gateway_outcomes.py`, `tests/integration/test_gateway_continuation.py`).

## Out of this note

L11-1 seam (STORY-57) · stub/live evidence gates (STORY-58) · FSM/gateway API redesign.
