# Runbook — `unknown_outcome` reconciliation

**Service:** `doge-ai-bridge`  
**Related:** [REQ-01 §15 AIB-HTTP-05](../requirements/REQ-01-doge-ai-bridge-runtime.md) · [03-confirm-gateway.md](../architecture/runtime/03-confirm-gateway.md)  
**As-of:** 2026-09-12

Gateway has **no** confirmed server-side idempotency. After a request may have reached gateway, aibridge must **not** auto-resend the same revision.

---

## 1. When this applies

Local state is `unknown_outcome` (or equivalent) because, for example:

- timeout / disconnect after send may have completed;
- response lost or malformed after a possible accept;
- ambiguous 5xx after the request left the bridge.

Resident must **not** see a one-click “Send again” for that revision.

---

## 2. Evidence to collect (local)

From aibridge (redacted-safe operator tools / DB):

- `request_id`
- session id / deployment id
- channel principal references (hashed if exposed in tickets)
- operation id, draft revision / canonical hash
- gateway attempt id / timestamps
- any stored gateway `trace_id` or HTTP status fragment
- current FSM state and outcome class

Never paste Bearers, raw action tokens, or full narrative into tickets.

---

## 3. Gateway check

Use the **best available operator method** for the pilot node (admin UI, support query, logs) to ask: “Does a draft exist for this attempt / time window / principal?”

**Pilot limitation:** if gateway provides **no** reliable lookup by client attempt id, document that gap explicitly for the incident. Do **not** invent `stashed`.

---

## 4. Allowed transitions after check

| Finding | Allowed operator action |
|---------|-------------------------|
| Draft confirmed present with valid `draft_id` | Mark reconciled → `stashed` (or equivalent) **only with evidence**; provide continuation URL if policy allows |
| Confirmed **not** created | Mark failed/cancelled path; allow **new** revision / new interview Send — never silent retry of same frozen attempt |
| Still unknown | Leave `unknown_outcome`; escalate; resident-safe “we are checking” copy |

Forbidden:

- Automatic Send retry for the same revision
- Claiming `stashed` without evidence
- Blind second gateway POST “just in case”

---

## 5. Resident copy

- Do not claim the Story was published.
- If unknown: acknowledge delay; do not instruct spam-tapping Send.
- If stashed after reconcile: same language as normal stash (draft saved for review).

---

## 6. Who may close

Only an operator with access to aibridge attempt records **and** gateway verification channel for the node. Record who closed, when, evidence refs (ids/hashes), final state.

---

## 7. Aftercare

- Confirm UI cannot offer auto-retry for that revision.
- File follow-up if gateway lookup remains impossible (candidate for later idempotency / REQ-02 delivery work — not silent pilot scope creep).
