# AC-AIB-11-07 — stub + live evidence gates (STORY-58 / REQ-11)

Thin runtime note. Arch SSOT: [`../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md`](../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md). Keep pipe: [`04-confirm-gateway-keep-pipe.md`](./04-confirm-gateway-keep-pipe.md).

**Honesty:** stub harness ≠ AC-AIB-11-07 **Done**. Live Pass only with ops evidence window + recorded path. This wave: live = **Explicit Partial**. Do **not** invent Railway / live SUCCESS.

---

## 1) Stub evidence matrix (required · tech accept)

Runnable harness (Present): `tests/test_story_56_keep_pipe_confirm_stash_spa.py` · soft seam: `tests/test_story_57_l11_invalidation_seam.py`.

| AC | Meaning | Stub harness (pytest) | Status |
|----|---------|----------------------|--------|
| **AC-AIB-11-01** | Interpretation ≠ send / no gateway auth on interpret | `test_t01_interpretation_confirm_never_authorizes_gateway` · `test_t01_send_offer_distinct_from_interpretation` | Present |
| **AC-AIB-11-03** | Gateway URL + Bearer from config only | `test_t04_submit_url_and_bearer_from_config_only` · `test_t04_fail_closed_without_gateway_token` | Present |
| **AC-AIB-11-04** | User-visible success only after factual stash | `test_t05_user_visible_success_only_after_factual_stash` · `test_t05_clear_failure_no_continuation` · `test_t05_unknown_outcome_blocks_blind_resend` | Present |
| **AC-AIB-11-05** | Continuation `#/story/submit?draft_id=` only when stashed | `test_t06_continuation_present_shape_only_when_stashed` · `test_t06_no_continuation_without_stash` | Present |
| **AC-AIB-11-06** | Bridge owns stash; channel has no gateway client | `test_t07_channel_module_has_no_gateway_stash_client` · `test_t07_runtime_note_present` | Present |
| Soft **AC-AIB-11-02** (57) | Transition C EDIT invalidate; target A Partial | `test_t03_transition_c_edit_invalidates_send_permission` · `test_t05_doc_target_a_partial_vs_done` | Present (soft) |

Command (from `doge-ai-bridge/`):

```bash
.venv/bin/python -m pytest tests/test_story_56_keep_pipe_confirm_stash_spa.py tests/test_story_57_l11_invalidation_seam.py -q
```

No claim of live Telegram E2E from this matrix.

---

## 2) Live Pass runbook / checklist (Q2)

### Path (when ops window open)

`Telegram → doge-ai-bridge channel → gateway stash → SPA open`  
(≥1 recorded path required to claim **live Pass / AC-AIB-11-07 Done**.)

### Checklist (ops)

| Step | Fact to record | Blocker if missing |
|------|----------------|--------------------|
| 1 | Ops evidence window calendar/env **open** | Without window → stay **Partial** |
| 2 | Telegram transport delivers to bridge (cite telegram REQ-01) | Transport failure → **BLOCKED** / residual |
| 3 | Bridge dual-confirm + factual stash (Keep pipe) | Fail closed → not live Pass |
| 4 | Gateway `/story-drafts` (or Present stash) returns draft id | Cite gateway 59 — no invent API |
| 5 | SPA opens `#/story/submit?draft_id=` (cite spa 25) | Continuity fail → not live Pass |
| 6 | Evidence artifact path + UTC recorded in analysis/run-report | Absent record → cannot claim Done |

### Wave status (STORY-58 / this implement)

| Field | Value |
|-------|-------|
| Ops evidence window | **Not open** (operator Q2 — mandatory live not required) |
| Live E2E evidence | **Unknown** / not claimed Done |
| AC-AIB-11-07 live side | **Explicit Partial** |
| Invented Railway / live SUCCESS | **Forbidden · Absent** |

---

## 3) Peer verify-first cites (no invent APIs)

| Peer | Cite | Stance |
|------|------|--------|
| gateway 59 | [`../../../doge-complaints-gateway/docs/requirements/59-req15-story-draft-stash-channel-parity-verify.md`](../../../doge-complaints-gateway/docs/requirements/59-req15-story-draft-stash-channel-parity-verify.md) | Present `/story-drafts`; no new draft API |
| spa 25 | [`../../../spa-app/docs/requirements/25-req15-story-submit-handoff-continuity-verify.md`](../../../spa-app/docs/requirements/25-req15-story-submit-handoff-continuity-verify.md) | Present hash `#/story/submit?draft_id=` |
| telegram REQ-01 | [`../../../doge-telegram/docs/requirements/REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md`](../../../doge-telegram/docs/requirements/REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md) | Transport only; never model keys / never stashes |
| REQ-12 | [`../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md`](../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) | Per-provider live matrix OOS beyond pointer |

---

## 4) Out of this note

Keep-pipe rewrite (56) · L11-1 seam invent (57) · opening ops window · REQ-13 taxonomy · gateway/SPA redesign.
