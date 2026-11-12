# STORY-AIBRIDGE-15 — Live n8n / Telegram integration gate

## Meta
- **Key:** `STORY-AIBRIDGE-15-n8n-telegram-gate`
- **Status:** 🟢 Done (P8 · G-01/G-02 WAIVED · next STORY-16)
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6.1 R3-P1-09
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [13](STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [11](STORY-AIBRIDGE-11-coordinator-pause-resume-send.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)

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

## Verified current state
- §6.1 checklist SSOT + n8n ops README (`event_id` retry rule).
- Contract/recorded tests in `tests/test_story_15_n8n_gate_contract.py`.
- Live Telegram screenshots **BLOCKED** (no credentials on disk) — see `docs/ops/n8n-channel-workflow/live-evidence-BLOCKED-20260913.md`.

## Target / AC
- [x] §6.1 checklist evidenced (runbook + screenshots/logs or recorded integration test).
- [x] Retry of same Telegram update does not mint a new `event_id`.

## Dependencies
- [13](STORY-AIBRIDGE-13-wave1-asgi-e2e.md) (aibridge contract stable)
