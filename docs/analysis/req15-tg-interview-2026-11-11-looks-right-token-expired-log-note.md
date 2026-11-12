# REQ15 — log note 2026-11-11 (Looks right → 409 Token expired)

**Role:** thin evidence note · not Product Done · not code fix.  
**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc)  
**Logs:** `scripts/logs/local-five/{aibridge,telegram}.log`  
**Prior:** [`req15-tg-interview-2026-11-11-buttons-present-log-note.md`](./req15-tg-interview-2026-11-11-buttons-present-log-note.md) · [`req15-operator-pipe-and-buttons-training-2026-11-11.md`](./req15-operator-pipe-and-buttons-training-2026-11-11.md)

---

## Verdict

| Check | Result |
|-------|--------|
| Looks right reached aibridge | **Yes** — `POST /v1/channel/actions` |
| Token consume | **Fail** — HTTP **409** `Token expired` · `retryable=false` |
| FSM advance / STORY-72 | **Absent** — no `ops_action_ok` · still `awaiting_interpretation_confirm` |
| DeepSeek on these presses | **Not called** — fail at token verify before `post_confirm_engine` |

---

## Event table

| Approx time (UTC+2) | event_id | Signal |
|---------------------|----------|--------|
| ~12:39 | `87952420` | restore remint · `actions_count=3` · tokens issued (TTL 900s → ~12:54) |
| ~13:15 | `87952421` | Looks right → **409 Token expired** · `channel_action ok=False` |
| ~13:16 | `87952422` | text «что дальше?» → remint Confirm set |
| ~13:22 | `87952423` | text «иди дальше» → remint · tokens expire ~**13:37** |
| ~14:07 | `87952424` | Looks right #1 → **409** (mint age ~45 min) · retry storm |
| ~14:11 | `87952425` | Looks right #2 → **409** · same · ack `query is too old` |

Telegram: `ops_bridge_action_failed … status=409` · body `conflict` / `Token expired`.  
Aibridge: `audit event=channel_action … ok=False` at matching times.

---

## Root cause

- Config: `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS=900` (15 min).  
- Code: `action_tokens.verify_for_consume` → `TokenConflictError("Token expired")`.  
- Remint (`offer_interpretation_confirm`) puts **fresh** tokens on the **new** outbound message; older messages keep old callback tokens until TTL. Labels look identical (Looks right / Edit / Cancel).  
- Presses at 14:07 / 14:11 used tokens past TTL (and/or an older message’s keyboard).

**Distortion:** «кнопки есть / Looks right ничего» ≠ mint broken. = **expired (or stale-message) token**.

---

## Latency split (Observed)

| Layer | What | Evidence |
|-------|------|----------|
| **A. Text turns** | Interview provider = DeepSeek (`deepseek-v4-pro`) | Gap `audit channel_turn` → `ops_channel_turn` today ~7–10 s; no `latency_ms` field in ops logs |
| **B. Callback storm** | After 409, poller `return False` without advance/`mark_seen` | Many 409 retries then `answerCallbackQuery` too-old for minutes (14:07–14:12) despite bridge `retryable:false` |

Тишина после Looks right сегодня = **B + expired**, не «DeepSeek думает на Confirm».

---

## Operator recovery (now)

1. Написать любой короткий текст в чат → сервер remint’ит **новое** сообщение с кнопками.  
2. В течение **15 минут** нажать **Looks right** на **самом свежем** сообщении (не на 12:39 / 13:22).  
3. Не ждать ответа модели на кнопку: успех = новое сообщение с Send/Continue (или явный отказ), плюс в логе `ops_action_ok` / смена state.

---

## Future gaps (not this wave)

- Longer action-token TTL for pilot UX.  
- Citizen/ops notice when 409 expired («кнопки устарели — напишите что угодно»).  
- Telegram: non-retryable 409 → advance + mark_seen + user-facing notice; stop callback storm.  
- Optional: ops `latency_ms` on interview provider turns.

---

## Related

- Buttons Present (morning): [`req15-tg-interview-2026-11-11-buttons-present-log-note.md`](./req15-tg-interview-2026-11-11-buttons-present-log-note.md)  
- Operator training: [`req15-operator-pipe-and-buttons-training-2026-11-11.md`](./req15-operator-pipe-and-buttons-training-2026-11-11.md)  
- Validate 71/72/ROL-07: [`req15-story-71-72-rol07-code-validation-test-2026-11-11.md`](./req15-story-71-72-rol07-code-validation-test-2026-11-11.md)  
