# STORY-AIBRIDGE-11 — Coordinator + pause/resume + Send txn

## Meta
- **Key:** `STORY-AIBRIDGE-11-coordinator-pause-resume-send`
- **Status:** 🟢 Done (P3 gate PASS · awaiting P4)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`
- **decision_ref:** [`STORY-AIBRIDGE-11-coordinator-pause-resume-send.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) P0-01 · §5.2 · §5.3 · AC #1,#3–#6,#8
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) P0-01 · §5.2 · §5.3 Send path · AC #1,#3–#6,#8
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [10](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md) · [13](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md)
- **Operator:** single story (unsplit) — wave1 Done requires full path including Send txn
- **Skill declared:** `fastapi-expert` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md)
- **Active pkg (wave):** `pkg-000009-20260913-epic-aibridge-02-story-11-coordinator-pause-resume-send.yaml`
- **P1 materialize:** 2026-09-13T15:55:55Z
- **P3 Done:** 2026-09-13T16:03:23Z

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Pause/resume across HTTP | REQ-03 [§5.2](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Commit before HTTPS / unknown_outcome | REQ-03 [§5.3](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Wave 1 dry-run | REQ-03 [§2](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| Channel OAS | [`aibridge-channel-v1.openapi.yaml`](../../../../../openapi/aibridge-channel-v1.openapi.yaml) |

## Scope
- Wire `/v1/channel/turns` → session repo → Responses client → tool loop → confirm (no stub `Received:`).
- Pause/resume: persist pending continuation, `call_id`, frozen body, replayable items **before** `/turns` returns actions; nothing left open waiting for Telegram.
- Interpretation confirm: state change only; no gateway HTTP.
- Send: owner/chat/session/deployment/revision/hash/expiry/state checks; atomic consume + `executing` + gateway-attempt **committed before** external HTTPS; outcome in a **separate** transaction; frozen body only; ≤ one attempt per authorized revision.
- Wave-1 gateway via dry-run/fake only; on 201: `stashed`/`draft_id`/`continuation_url` as applicable; then `function_call_output` with original `call_id`; resident reply must not claim Story publish.
- Restart with `executing` → `unknown_outcome`; **no** automatic resend.

## Вне scope
- Real `POST /story-drafts` until P1 gates (14); live n8n (15); inventing OpenAPI fields.

## Verified current state (post-P3)
- `process_turn_async` + `coordinator.build_turn_from_engine` replace stub `Received:`.
- Pending `call_id` / frozen body / replay items persisted before Send actions.
- Interpretation confirm is state-only; Send uses frozen body; stash → `function_call_output`; boot recovers `executing` → `unknown_outcome`.
- pytest **122 passed, 14 skipped**.

## Verified current state (P1)
- Stub turn reply — `src/aibridge/channel.py` (`Received:`).
- `InterviewEngine` exists but is not the ASGI turn product path (stub side-effect).

## Target / AC
- [x] REQ-03 §4 acceptance criteria #1, #3, #4, #5, #6, #8 on fake/dry-run transports.
- [x] No PostgreSQL txn/lock held across gateway HTTPS.
- [x] Pending confirm survives separate HTTP requests and restart (with 09 store).

## Точки в коде
- `src/aibridge/channel.py`, `app.py`, `interview.py`, `confirm.py`, `gateway.py`, `coordinator.py`

## Dependencies
- [STORY-AIBRIDGE-09](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [STORY-AIBRIDGE-10](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-10-responses-adapter-tools.md)

## Nested tasks (pkg-000009 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-11-t01-wire-turns-coordinator](./task-aibridge-02-11-t01-wire-turns-coordinator/README.md) | Scope #1; AC #1 | Done |
| t02 | [task-aibridge-02-11-t02-pause-resume-persist](./task-aibridge-02-11-t02-pause-resume-persist/README.md) | Scope #2; pending + #3 | Done |
| t03 | [task-aibridge-02-11-t03-interpretation-confirm](./task-aibridge-02-11-t03-interpretation-confirm/README.md) | Scope #3; AC #4 | Done |
| t04 | [task-aibridge-02-11-t04-send-commit-before-https](./task-aibridge-02-11-t04-send-commit-before-https/README.md) | Scope #4; AC #5 + txn | Done |
| t05 | [task-aibridge-02-11-t05-wave1-stash-call-id](./task-aibridge-02-11-t05-wave1-stash-call-id/README.md) | Scope #5; AC #6 | Done |
| t06 | [task-aibridge-02-11-t06-executing-unknown-outcome](./task-aibridge-02-11-t06-executing-unknown-outcome/README.md) | Scope #6; AC #8 | Done |
| t07 | [task-aibridge-02-11-t07-story-acceptance-verification](./task-aibridge-02-11-t07-story-acceptance-verification/README.md) | Target AC gate | Done |
| t08 | [task-aibridge-02-11-t08-audit-g01-three-gates](./task-aibridge-02-11-t08-audit-g01-three-gates/README.md) | P4 G-01 | Done |
| t09 | [task-aibridge-02-11-t09-audit-g02-lock-before-https](./task-aibridge-02-11-t09-audit-g02-lock-before-https/README.md) | P4 G-02 | Done |
| t10 | [task-aibridge-02-11-t10-audit-g03-dedupe-pending-pg](./task-aibridge-02-11-t10-audit-g03-dedupe-pending-pg/README.md) | P4 G-03 | Done |
