# STORY-AIBRIDGE-01 — Channel façade + Bearer + event dedupe

## Meta
- **Key:** `STORY-AIBRIDGE-01-channel-facade-auth`
- **Status:** Done
- **Parent REQ:** [`REQ-01-doge-ai-bridge-runtime.md`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) §6–§7, §18 (health partial)
- **Package:** [`req-01-runtime/INDEX.md`](INDEX.md)
- **Pipeline:** [`epics/.../STORY-AIBRIDGE-01-channel-facade-auth.md`](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-01-channel-facade-auth/STORY-AIBRIDGE-01-channel-facade-auth.md)
- **Siblings:** [02](STORY-AIBRIDGE-02-content-bundle-registry.md) … [06](STORY-AIBRIDGE-06-ops-wave1-proof.md)
- **Skill declared:** `python-pro` — [`.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md`](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Channel contract:** [`aibridge-channel-v1.openapi.yaml`](../../../openapi/aibridge-channel-v1.openapi.yaml)
- **P3 Done:** 2026-09-12T20:35:41Z · module `src/aibridge/`

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Topology, single ASGI `$PORT`, no worker | [00-overview.md §2–§3](../../../architecture/runtime/00-overview.md) |
| Channel role, auth mode C, ack order, n8n mapping, wave-1 façade proof | [01-channel-facade.md](../../../architecture/runtime/01-channel-facade.md) (§1–§7) |
| Façade protocol, statuses, response envelope | REQ-01 [§6 AIB-CH-01…06](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Channel Bearer + private network | REQ-01 [§7 AIB-AUTH-01…02](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) |
| Health endpoints (minimal shell) | REQ-01 [§18 AIB-OPS-02](../../../requirements/REQ-01-doge-ai-bridge-runtime.md); [04-ops-security.md §1](../../../architecture/runtime/04-ops-security.md) |
| n8n ops contract (no invented JSON) | [`docs/ops/n8n-channel-workflow/README.md`](../../../ops/n8n-channel-workflow/README.md) |
| Bearer rotation overlap | [`channel-bearer-rotation.md`](../../../runbooks/channel-bearer-rotation.md) |
| Do not mix with Story Intake wire OAS | [00-overview.md §2 contracts table](../../../architecture/runtime/00-overview.md); wire = [`story-intake-actions.openapi.yaml`](../../../openapi/story-intake-actions.openapi.yaml) (story 05) |

## Scope
- ASGI app skeleton bound to Railway `$PORT`; `GET /healthz`, `GET /readyz` (minimal: process up + channel auth config present).
- `POST /v1/channel/turns` and `POST /v1/channel/actions` per channel OpenAPI (**no** `callback_ack_text`).
- Channel Bearer (`AIBRIDGE_CHANNEL_BEARER_TOKEN` + previous-token overlap per runbook); constant-time compare; 401 generic body.
- Telegram IDs as decimal strings; reject unknown fields; size bounds; no CORS.
- Event dedupe by `(channel, event_id)` returning stored response (no second side-effect path).
- Document operator ack order: immediate Telegram `answerCallbackQuery` in n8n → then `/v1/channel/actions` → Send/Edit UI.

## Вне scope
- OpenAI Responses / tool loop (03); gateway HTTPS (05); dual-confirm business FSM beyond accepting `action_token` shape (04); content bundle registry (02); full `/metrics` series (06).

## Verified current state
- Channel OAS on disk: `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml`.
- Runtime Python/ASGI module path: `doge-ai-bridge/src/aibridge/app.py` (`aibridge.app:app`).
- Arch façade: `docs/architecture/runtime/01-channel-facade.md`.

## Target / AC
- [x] Unauthenticated `/v1/channel/*` → 401.
- [x] Valid Bearer + turn request → 200 envelope fields per channel OAS (no `callback_ack_text`).
- [x] Duplicate `event_id` → same stored response; no second side-effect path.
- [x] Contract tests: request/response vs committed channel OAS.
- [x] Equal channel/gateway Bearer when both configured → readiness fail (REQ-01 §7 / §18).
- [x] Task README after P1.3 includes `Skill declared: python-pro`.

## Точки в коде
- `src/aibridge/app.py`, `auth.py`, `schemas.py`, `channel.py`, `dedupe.py`
- Gate: `acceptance-verification-task-aibridge-01-01-t06-story-acceptance-verification.md` PASS 2026-09-12T20:35:41Z

## Dependencies
- None (first in package order).
