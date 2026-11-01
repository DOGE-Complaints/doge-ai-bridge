# Keep pipe — components & trust boundaries

**Overview:** [`00-overview.md`](./00-overview.md)  
**Keep detail SSOT:** [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md)

---

## 1) Components (Keep)

| Component | Responsibility | As-is |
|-----------|----------------|-------|
| Channel façade | `/v1/channel/turns` · `/actions` | `app.py` channel routes · `channel.py` |
| ConfirmationGuard + FSM | Interpretation confirm ≠ Send confirm | `confirm_fsm.py` · `confirm.py` |
| Action tokens | Opaque callback tokens; hash at rest; revision bind | `action_tokens.py` |
| GatewayExecutor | Config HTTPS `POST /story-drafts`; service Bearer | `gateway.py` `execute_stash` |
| Continuation builder | `{SPA}/#/story/submit?draft_id=` | `gateway.py:118` `build_continuation_url` |
| Transport peer | Deliver link/errors only | doge-telegram REQ-01 (OOS implement here) |

---

## 2) Trust boundaries

| Domain | Token / secret | Must not |
|--------|----------------|----------|
| Channel | Channel Bearer | Act as gateway submit |
| Gateway S2S | Service API token in executor | Appear in browser / telegram service / model output |
| User session | Action tokens (raw once) | Authorize stash without Send consume |
| Model / tool-intent | Frozen intent after validation | Choose submit URL or hold Bearer |

**Interview D4:** Responses **tool loop may remain internal** as transition; tool-intent ≠ permission (`runtime/03` §3). Pure role chat cutover is sibling REQ-13/48 — not a hard cut in this package.

---

## 3) Confirm storage (Interview D3)

**Reuse Present:** ActionToken store + session `revision` / `draft_hash` / EDIT invalidation.  
Do **not** invent a parallel confirm schema in this arch. Revisit only if REQ-13 proves a versioning gap.

EDIT path (transition C enforce today): `confirm.py:441–445` `apply_edit` → `confirm.py:407–439` `invalidate_send_permission` — bumps revision, invalidates tokens, clears gateway authorization and continuation fields.

---

## 4) Outcome contract (unchanged)

1. Understanding confirm never authorizes HTTPS stash.  
2. Send confirm consume is the only path that may call `execute_stash`.  
3. User-visible success only after factual gateway success (AC-AIB-11-04).  
4. `unknown_outcome` — no blind resend for same revision (`runtime/03` §5–6).  
5. Continuation URL only with stashed outcome; copy must not claim Story published.

---

## 5) Out of scope here

Gateway schema redesign · SPA UX redesign · provider ports · instruction markdown · sense-brief worker.
