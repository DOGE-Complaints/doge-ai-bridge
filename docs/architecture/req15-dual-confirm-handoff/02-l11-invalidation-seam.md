# L11-1 — semantic invalidation seam (REQ15 delta)

**Overview:** [`00-overview.md`](./00-overview.md)  
**Product lock:** REQ-11 **L11-1** (= REQ-13 **L13-3**): target **A** + transition **C**.

---

## 1) Terms

| Term | Meaning |
|------|---------|
| **Invalidation** | Clear dependent send permission / action tokens / frozen intent for the affected revision |
| **Target A** | When app-owned semantic state is Present, a recorded **meaning change** invalidates send permission **without** requiring Telegram EDIT |
| **Transition C** | Until semantic state Present, **only** Present EDIT/revision invalidation enforces (as today) |

---

## 2) Named seam (Interview D2 = A)

```text
  [Future] REQ-13 semantic state records meaning change
                    │
                    ▼
         invalidate_send_permission()   ←── same effects as apply_edit
                    │                     (tokens, revision policy, gateway_authorized=false, …)
                    ▼
         Present ConfirmationGuard / ActionToken path
```

**Today (transition C):** the only enforce point is Present EDIT (and related revision flows), e.g. `confirm.py:407–425` `apply_edit`.

**This arch does not** invent:

- DB tables for semantic state  
- Field-level taxonomy of «what counts as meaning change»  
- New HTTP channel actions for invalidation  

Those belong to **REQ-13** Architect Studio + thin product (sensitivity under L13-3).

---

## 3) Coexistence rules

| Phase | Enforce invalidation via | Target A |
|-------|--------------------------|----------|
| REQ-13 state **Absent** | EDIT / revision only (transition C) | Documented goal; not enforceable yet |
| REQ-13 state **Present** | Semantic meaning-change **and** EDIT | Must call the **same** invalidate path as EDIT (no second permission store) |

AC-AIB-11-02 remains **Partial** until target A is enforceable with evidence; do not claim Done early.

---

## 4) Boundary vs siblings

| Sibling | Owns | This seam |
|---------|------|-----------|
| REQ-13 | Semantic fields, roles, when meaning changes | Calls into confirm invalidate |
| REQ-11 (this) | Confirm/stash/SPA Keep + seam name | Does not own state schema |
| GPT-48 | Instruction prose without model stash | Unrelated to invalidate mechanics |
