# Roles, coordinator, instruction assembly

**Overview:** [`00-overview.md`](./00-overview.md)  
**Locks:** Interview D3=B · D5=A · REQ **L13-1** · AC-02/03/07/08

---

## 1) Five roles (v1)

Communication setup · Interviewer · Extractor · Normalizer · Checker — versioned task configs (product §6). Bodies authored in GPT UI (REQ-48), not aibridge SSOT.

---

## 2) Coordinator (D3)

| Rule | Target |
|------|--------|
| Selection | **Policy table:** phase + gaps/flags → allowed next role; Python picks **one** role |
| Forbidden | LLM-as-router / free meta-agent (REQ Goal) |
| Model call | Via **REQ-12** interview provider port only (≠ worker `providers/`) |
| Present | `coordinator.py` **Adapt** (e.g. offer_interpretation path under L13-1) — not gateway rewrite |

Concrete phase→role rows = Open (implement/product thin).

---

## 3) Assembly (D5)

| Piece | Role |
|-------|------|
| Shared core | Common instruction material from dir |
| Per-role slice | Role-specific files from same dir/manifest family |
| Node settings | Present node/pack identity hooks |
| Session pin | Hash/pin of core+role(+node) at conversation start — no mid-flight silent swap |

Read only via `DOGESTONIA_INSTRUCTIONS_DIR` + manifest (AC-03). Model does not “hunt” pack via vague links.

---

## 4) Confirm-offer (L13-1 — REQ lock)

| Kind | Policy |
|------|--------|
| Understanding / interpretation confirm | Soft auto-offer **may** remain |
| Send confirm | **Never** automatic — ordinary model reply ≠ send permission (AC-08) |

---

## 5) AC-07 boundary

Role and core instruction text **must not** own gateway submit URL choice or SPA redirect procedure — server pipe stays REQ-11.
