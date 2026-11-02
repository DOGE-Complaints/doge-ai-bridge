# Semantic state store + invalidation seam

**Overview:** [`00-overview.md`](./00-overview.md)  
**Locks:** Interview D1=B · D2=B · REQ **L13-3** (Target A + Transition C) · peer [`../req15-dual-confirm-handoff/02-l11-invalidation-seam.md`](../req15-dual-confirm-handoff/02-l11-invalidation-seam.md)

---

## 1) Store (logical)

| Item | Target |
|------|--------|
| Home | **Separate** app semantic store on Postgres (same DB SSOT family as sessions) |
| Not | HistoryStore / chat dump / `last_confirmed_state` string map as SSOT |
| Contents (logical classes) | phase · facts↔utterance grounds · hypotheses · gaps · corrections |
| Confirmed vs draft | Facts/corrections that count as **confirmed** are distinct from draft hypotheses/gaps |

DDL / table shape = **Open** (REQ §7) — name ≠ create here.

---

## 2) Meaning change → invalidate (D2)

| Triggers invalidation (v1) | Does **not** auto-invalidate |
|----------------------------|------------------------------|
| Confirmed facts change | Draft hypotheses / gaps alone |
| Corrections | Pure reads |
| Phase change **when** it changes role/rights policy | — |

**Effect:** call Present `invalidate_send_permission` (same clearance family as `apply_edit`) — `confirm.py:407+`.

**Target A:** meaning change invalidates send permission **without** requiring Telegram EDIT.  
**Transition C:** until semantic store Present, only EDIT/revision invalidation enforces (`confirm.py:441–445`).

---

## 3) Trust

| Must | Must not |
|------|----------|
| App validates/persists state; model proposes | Model alone grant send permission |
| Grounds cite utterances from history | Replace history with opaque blob only |
| Invalidation clears dependent tokens/intent | Invent new HTTP invalidate action in this arch |
