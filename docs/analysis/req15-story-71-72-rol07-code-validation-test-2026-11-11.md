# REQ15 STORY-71 / 72 / ROL-07 — code validation + how to test (2026-11-11)

**Role:** code-backed validation + operator retest expectations · not invent live TG SUCCESS.  
**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc)  
**Stories:** [`STORY-AIBRIDGE-71`](../../doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-71-awaiting-interpretation-actions-always.md) · [`STORY-AIBRIDGE-72`](../../doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-72-send-after-draft-confirm-and-validation.md) · [`STORY-GPT-ROL-07`](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-07-citizen-surface-no-role-theater.md)  
**North star / gap:** [`req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md`](./req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md) · [`req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md`](./req15-tg-interviewer-citizen-conversation-gap-2026-11-10.md)  
**Wave:** [`wave-20261110-req15-71-72.md`](../../doge-ai-bridge/docs/tasks/run-reports/operator-waves/wave-20261110-req15-71-72.md) (H-01 live smoke **WAIVE**)

**Honesty:** Product/Code Done + pytest green ≠ live channel SUCCESS until operator retest with fresh telegram (no REUSE).

---

## 1. Verdict (code / instructions)

| AC | Claim | Verified |
|----|-------|----------|
| AC-71-01/02 | Remint Confirm+Edit when `awaiting_interpretation_confirm` ∧ empty actions, **without** Send-claim markers | **Present** — [`coordinator._ensure_control_surface`](../../doge-ai-bridge/src/aibridge/coordinator.py) step **0** before marker gate |
| AC-71-03/04 | No invent Send/stash on that remint | **Present** — remint calls `offer_interpretation_confirm` only |
| AC-72-01 | No Send before draft confirm | **Present** — FC before confirm blocked; consume alone no Send |
| AC-72-02 | After Confirm → validate path → Send on success | **Present** — `post_confirm_engine` in [`confirm.py`](../../doge-ai-bridge/src/aibridge/confirm.py) · chain in [`channel.py`](../../doge-ai-bridge/src/aibridge/channel.py) |
| AC-72-03 | Free-text «отправляй» ≠ stash | **Present** — harness + Keep REQ-11 |
| AC-72-04 | Stash only via Send confirm | **Present** — harness |
| AC-ROL-07-01…04 | Citizen surface covenant + fences + stash bans | **Present** in [`instructions-roles/`](../../GPT-UI/instructions-roles/) · **live model compliance Open** |
| Live TG | H-01 | **WAIVE / Open** — retest below |

---

## 2. What changed (thin)

| Layer | Behavior |
|-------|----------|
| **71** | `_ensure_control_surface`: if state=`awaiting_interpretation_confirm` and `actions` empty → always `offer_interpretation_confirm` **before** `needs_control_surface` |
| **72** | After `CONFIRM_INTERPRETATION` consume → server-owned engine turn → `build_turn_from_engine`; FC OK → `offer_send_confirm`; no-FC/fail → CONTINUE/Edit, never Send/gateway |
| **ROL-07** | `core.md` **Citizen surface covenant**; interviewer bans operable HANDOFF/roles; fences on extractor/checker/normalizer/communication_setup |

---

## 3. Automated tests (aibridge)

```bash
cd doge-ai-bridge
.venv/bin/pytest \
  tests/test_story_71_awaiting_interpretation_actions_always.py \
  tests/test_story_72_send_after_draft_confirm_and_validation.py \
  -q
```

**Evidence 2026-11-11 (this validation):** **9 passed** in 0.03s.

| File | Cases (expect PASS) |
|------|---------------------|
| `test_story_71_…` | plain reply no markers remints Confirm/Edit · ok=false path remints |
| `test_story_72_…` | confirm→Send after validate · no-FC→CONTINUE · no engine→CONTINUE · consume alone no gateway · FC before confirm blocked · freetext send ≠ stash · stash only via Send |

Optional regression:

```bash
.venv/bin/pytest tests/test_story_68_channel_seam_send_actions.py tests/test_story_70_send_claim_requires_actions.py -q
```

---

## 4. ROL-07 static check

```bash
rg -n 'Citizen surface covenant|Citizen fence|HANDOFF|следующий процесс' GPT-UI/instructions-roles/
```

**Expect Present:** covenant in `core.md`; fences on role files; interviewer «Do not» operable extractor/checker/HANDOFF.  
**Do not expect:** deterministic live prose — model may still leak jargon; treat as live Partial if Observed.

Custom GPT / pack must be **re-exported / uploaded** with these instruction files for live TG to pick ROL-07 up (instruction Apply ≠ automatic remote GPT).

---

## 5. Live TG retest (operator) — expectations

### Prep

1. Kill telegram on `:8090` (no REUSE) · restart **aibridge** then **telegram**.  
2. Prove boot: `aibridge.log` → `ops_runtime use_pg_runtime=…` · `telegram.log` → fresh `production_entry_started` + later `reply_prefix=`.

### Path A — AC-71 (Confirm/Edit appear)

1. Restore or reach draft so FSM is `awaiting_interpretation_confirm` (e.g. «восстанови контекст» / draft ready).  
2. **Expect logs:** `ops_channel_turn … state=awaiting_interpretation_confirm … actions_count≥2` (Confirm+Edit; Cancel may make 3).  
3. **Expect TG:** `ops_outbound_sent … has_actions=True` + visible Confirm/Edit keyboard.  
4. **Fail if:** `actions_count=0` / `has_actions=False` (pre-71 bug).

### Path B — AC-72 (after Confirm)

1. Press Confirm («Looks right» / confirm_interpretation).  
2. **Expect either:**
   - Send confirm actions (`CONFIRM_SEND` / «Send to DOGEstonia») when validate+FC succeed, **or**
   - CONTINUE/Edit (no Send) if engine returns no FC / validate fail.  
3. **Fail if:** empty actions + prose «передал чекеру/HANDOFF» with no CTA.  
4. Free-text «отправляй» **must not** stash (refuse / no gateway).

### Path C — ROL-07 (prose)

1. Do **not** coach «передай экстрактору».  
2. **Expect:** calm draft talk; may name in-chat buttons if Present.  
3. **Fail (Partial):** operable extractor/checker/HANDOFF / «следующий процесс» as user steps.

### Log join

| Field | Where |
|-------|--------|
| `ops_channel_turn event_id= session_id= state= fc_count= actions_count= send_claim= needs_control=` | `aibridge.log` |
| `ops_outbound_sent has_actions= reply_prefix=` · `ops_turn_ok event_id=` | `telegram.log` |

Paste matching lines for Confirm turn + post-Confirm turn into chat for evidence.

---

## 6. Expected vs not expected (summary)

| Expect | Do not expect |
|--------|----------------|
| Confirm/Edit whenever stuck in awaiting interpret | Buttons only if bot says «Send» |
| Send **after** Confirm + successful validate/FC | Send on free-text «отправляй» |
| CONTINUE/Edit if post-confirm has no FC | Fake «pipeline done» without CTAs |
| Pytest 71/72 green | Live SUCCESS without fresh TG + smoke |
| Instruction covenant Present | Perfect model obedience every turn |

---

## Related

- Aibridge INDEX: [`../../doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md`](../../doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/INDEX.md)  
- GPT roles INDEX: [`../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/INDEX.md`](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/INDEX.md)  
- REUSE orphan: [`../../scripts/docs/analysis/local-five-telegram-reuse-orphan-2026-11-10.md`](../../scripts/docs/analysis/local-five-telegram-reuse-orphan-2026-11-10.md)  
- Operator training (pipe + buttons) 2026-11-11: [`req15-operator-pipe-and-buttons-training-2026-11-11.md`](./req15-operator-pipe-and-buttons-training-2026-11-11.md)  
- Live buttons Present log note: [`req15-tg-interview-2026-11-11-buttons-present-log-note.md`](./req15-tg-interview-2026-11-11-buttons-present-log-note.md)  
- Transcript 2026-11-11: [`tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-11-pille-buttons-present.md`](./tg-interview-transcripts/req15-tg-interview-dialogue-2026-11-11-pille-buttons-present.md)  
- North star: [`req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md`](./req15-tg-interviewer-citizen-conversation-north-star-2026-11-10.md)  
