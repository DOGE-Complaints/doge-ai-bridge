# Verify, evidence, coexistence

**Overview:** [`00-overview.md`](./00-overview.md)  
**Interview D5:** split gate

---

## 1) Verify surfaces

| Gate | What | When |
|------|------|------|
| **Stub / harness** | Both adapters produce usable role/engine outcomes under fixtures (AC-AIB-12-03); fail-closed unset/unknown (AC-05); worker env cannot select interview (AC-02) | **Required** for tech accept |
| **Live per provider** | Documented + recorded live path when that provider is enabled (AC-AIB-12-04 / parent AC-10) | **Required** to claim live Pass for that provider; only with ops window |
| Without live window | AC-04 **Partial** for that provider | Do not claim Done on stub alone |

Honesty: Product Story Done ≠ Draft REQ ≠ green local smoke.

---

## 2) Peer coexistence

| Peer | Stance |
|------|--------|
| [`ai-provider-selection/`](../ai-provider-selection/00-overview.md) | Worker only; interview OOS |
| [`req15-dual-confirm-handoff/`](../req15-dual-confirm-handoff/00-overview.md) | Confirm/stash Keep; provider change ≠ Send permission |
| REQ-13 | Roles call interview port when Present |
| GPT UI REQ-48 | Instruction SSOT OOS |
| telegram / gateway | No model keys |

---

## 3) Coexistence with Present wire

| Present | Target |
|---------|--------|
| Key → Responses else recording (`app.py:414–428`) | After Adapt: provider env fail-closed first; then adapter; recording not a stand-in for missing `AIBRIDGE_INTERVIEW_PROVIDER` |

---

## 4) Open (ops)

- Live evidence window calendar per provider.  
- DeepSeek live model confirm (L12-2).
