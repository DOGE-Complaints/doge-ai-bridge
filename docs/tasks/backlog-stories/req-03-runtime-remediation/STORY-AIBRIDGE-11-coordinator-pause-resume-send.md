# STORY-AIBRIDGE-11 — Coordinator + pause/resume + Send txn

## Meta
- **Key:** `STORY-AIBRIDGE-11-coordinator-pause-resume-send`
- **Status:** Done
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) P0-01 · §5.2 · §5.3 Send path · AC #1,#3–#6,#8
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [10](STORY-AIBRIDGE-10-responses-adapter-tools.md) · [13](STORY-AIBRIDGE-13-wave1-asgi-e2e.md)
- **Operator:** single story (unsplit) — wave1 Done requires full path including Send txn
- **Skill declared:** `fastapi-expert` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md)

## Doc pointers

| Topic | Where |
|-------|--------|
| Pause/resume across HTTP | REQ-03 [§5.2](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Commit before HTTPS / unknown_outcome | REQ-03 [§5.3](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Wave 1 dry-run | REQ-03 [§2](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Channel OAS | [`aibridge-channel-v1.openapi.yaml`](../../../openapi/aibridge-channel-v1.openapi.yaml) |

## Scope
- Wire `/v1/channel/turns` → session repo → Responses client → tool loop → confirm (no stub `Received:`).
- Pause/resume: persist pending continuation, `call_id`, frozen body, replayable items **before** `/turns` returns actions; nothing left open waiting for Telegram.
- Interpretation confirm: state change only; no gateway HTTP.
- Send: owner/chat/session/deployment/revision/hash/expiry/state checks; atomic consume + `executing` + gateway-attempt **committed before** external HTTPS; outcome in a **separate** transaction; frozen body only; ≤ one attempt per authorized revision.
- Wave-1 gateway via dry-run/fake only; on 201: `stashed`/`draft_id`/`continuation_url` as applicable; then `function_call_output` with original `call_id`; resident reply must not claim Story publish.
- Restart with `executing` → `unknown_outcome`; **no** automatic resend.

## Вне scope
- Real `POST /story-drafts` until P1 gates (14); live n8n (15); inventing OpenAPI fields.

## Verified current state
- Coordinator wired: `/turns` → InterviewEngine → confirm (no `Received:`).
- Pause/resume pending fields + Send commit-before-HTTPS + stash `function_call_output` + executing recovery.

## Target / AC
- [x] REQ-03 §4 acceptance criteria #1, #3, #4, #5, #6, #8 on fake/dry-run transports.
- [x] No PostgreSQL txn/lock held across gateway HTTPS.
- [x] Pending confirm survives separate HTTP requests and restart (with 09 store).

## Точки в коде
- `src/aibridge/channel.py`, `app.py`, `interview.py`, `confirm.py`, `gateway.py`

## Dependencies
- [09](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [10](STORY-AIBRIDGE-10-responses-adapter-tools.md)
