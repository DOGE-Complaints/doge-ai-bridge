# STORY-AIBRIDGE-15 — Live n8n / Telegram integration gate

## Meta
- **Key:** `STORY-AIBRIDGE-15-n8n-telegram-gate`
- **Status:** 🟢 Done (P8 · G-01/G-02 WAIVED · next STORY-16)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md`
- **decision_ref:** [`STORY-AIBRIDGE-15-n8n-telegram-gate.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-15-n8n-telegram-gate.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6.1 R3-P1-09
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6.1 R3-P1-09
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [13](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [11](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Active pkg (wave):** `pkg-000013-20260913-epic-aibridge-02-story-15-n8n-telegram-gate.yaml`
- **P1 materialize:** 2026-09-13T17:28:28Z
- **P3 Done:** 2026-09-13T17:34:04Z
- **P5 APPLY:** 2026-09-13T17:38:54Z · G-01/G-02 WAIVED · activation none · [p5 draft](../../../../../../../../.cursor/plans/p5_aibridge15_gap_20260913T173854Z.plan.md)
- **P8:** 2026-09-13T17:42:08Z · feat `edbb8cd` · test `d4fab69` · docs `bcf58bb`/`c6076c9`

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| R3-P1-09 live gate | REQ-03 [§6.1](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) |
| §6.1 checklist SSOT | [`r3-p1-09-live-gate-checklist.md`](../../../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) |
| n8n ops contract | [`docs/ops/n8n-channel-workflow/README.md`](../../../../../ops/n8n-channel-workflow/README.md) |
| Live evidence BLOCKED | [`live-evidence-BLOCKED-20260913.md`](../../../../../ops/n8n-channel-workflow/live-evidence-BLOCKED-20260913.md) |
| Channel OpenAPI SSOT | [`docs/openapi/aibridge-channel-v1.openapi.yaml`](../../../../../openapi/aibridge-channel-v1.openapi.yaml) |
| Wave-1 ASGI baseline | [STORY-13](../STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) |

## Scope
Evidence/checklist that live routing matches REQ-03 §6.1:
- Telegram message → n8n → `/v1/channel/turns`;
- every `actions[]` as inline buttons; `callback_data` = token only;
- `answerCallbackQuery` then `/v1/channel/actions`; render via Send/Edit Message;
- secrets in n8n: Bot token + channel Bearer only; **no** OpenAI / gateway Bearers; **no** `/story-drafts`;
- `channel` always `telegram`;
- `event_id` deterministic from Telegram update/callback id; **unchanged** across n8n HTTP retries;
- `from.id` / `chat.id` mapped to channel principal fields;
- stable `session_id` for active interview;
- `/actions` callback user/chat match token binding.

## Вне scope
- Mandatory credential-stripped n8n JSON export as product deliverable (P2-04 / REQ-03 §8).
- Inventing channel OpenAPI fields.

## Verified current state (post-P3)
- Executable §6.1 checklist SSOT on disk.
- n8n README documents ack order, secrets names, `event_id` = `String(update.update_id)`, retry invariance.
- Contract/recorded tests: `tests/test_story_15_n8n_gate_contract.py` (mapping, OAS telegram enum, dedupe retry, session stability, wrong-owner 403).
- Live Telegram/n8n screenshots: **BLOCKED** — no Bot token / `.env` / workflow export on disk (fact file present). No live PASS claimed.

## Target / AC
- [x] §6.1 checklist evidenced (runbook + screenshots/logs or recorded integration test).
- [x] Retry of same Telegram update does not mint a new `event_id`.

## Точки в коде / ops
- `docs/ops/n8n-channel-workflow/README.md`
- `docs/ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md`
- `docs/ops/n8n-channel-workflow/live-evidence-BLOCKED-20260913.md`
- `docs/ops/wave1-gate-checklist.md` (cross-link only)
- `docs/openapi/aibridge-channel-v1.openapi.yaml`
- `tests/test_story_15_n8n_gate_contract.py`

## Dependencies
- [13](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-13-wave1-asgi-e2e.md)

## Nested tasks (pkg-000013 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-15-t01-r3-p1-09-checklist-ssot](./task-aibridge-02-15-t01-r3-p1-09-checklist-ssot/README.md) | Scope #1–#9 · Target #1 | Done |
| t02 | [task-aibridge-02-15-t02-turns-buttons-callback-order](./task-aibridge-02-15-t02-turns-buttons-callback-order/README.md) | Scope #1–#3 | Done |
| t03 | [task-aibridge-02-15-t03-secrets-no-story-drafts](./task-aibridge-02-15-t03-secrets-no-story-drafts/README.md) | Scope #4 | Done |
| t04 | [task-aibridge-02-15-t04-event-id-retry-principal-session](./task-aibridge-02-15-t04-event-id-retry-principal-session/README.md) | Scope #5–#9 · Target #2 | Done |
| t05 | [task-aibridge-02-15-t05-live-evidence-or-recorded-test](./task-aibridge-02-15-t05-live-evidence-or-recorded-test/README.md) | Target #1 evidence | Done |
| t06 | [task-aibridge-02-15-t06-story-acceptance-verification](./task-aibridge-02-15-t06-story-acceptance-verification/README.md) | Target AC gate | Done |
