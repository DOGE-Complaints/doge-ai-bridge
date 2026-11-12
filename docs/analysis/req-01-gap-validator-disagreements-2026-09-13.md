# REQ-01 gap — disagreements with external validator (2026-09-13)

**Audience:** сторонний валидатор / operator handoff  
**Parent gap report:** [`req-01-runtime-code-gap-2026-09-13.md`](./req-01-runtime-code-gap-2026-09-13.md)  
**Agreed remediation SSOT (не правка REQ-01):** [`../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md`](../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) **v0.2.1** (Ready for implementation)

---

## Status

| Topic | Outcome |
|-------|---------|
| D1 (409 on consumed token vs replay) | **Принят валидатором в пользу IDE-аудита** (2026-09-13) |
| Clarification «replayed callback» | Живёт в **REQ-03 §2** — **не** в теле REQ-01 (оператор: не менять реализованный REQ) |
| Остальной P0/P1/P2 список | Согласован → **REQ-03** |

---

## D1 — итог (закрыт)

1. Same `(channel, event_id)` = **transport replay** → stored bounded response; no gateway/OpenAI repeat.  
2. New `event_id` + consumed `action_token` = **409**; no gateway repeat.  
3. Finding validator §11 (обязательный token-hash UX replay) — **снять с P1-gap**; только optional UX.  
4. Отдельный **P0** сохраняется: event dedupe + stored response в **PostgreSQL** (REQ-03 R3-P0-06).

---

## Hand-back

- Remediation list: REQ-03  
- Gap evidence: `req-01-runtime-code-gap-2026-09-13.md`  
- REQ-01 body: **не менять** этим треком.
