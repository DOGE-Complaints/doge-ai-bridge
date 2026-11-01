# Adapters — OpenAI (Keep) + DeepSeek (Replace)

**Overview:** [`00-overview.md`](./00-overview.md)  
**AC:** AC-AIB-12-03 · T1 Keep/Replace

---

## 1) OpenAI adapter (Keep)

| Item | Target |
|------|--------|
| Transport | Present OpenAI **Responses** API |
| Client | `ProductionResponsesClient` (`responses_client.py:327+`) |
| Wire today | `app.py:418–426` when `OPENAI_API_KEY` Present |
| Role vs Engine | Adapter/backend behind InterviewProviderPort → Keep `InterviewEngine` |

No forced fake unification with Chat Completions. Tool-intent loop remains internal transition (REQ-11 arch D4) — adapter must not grant gateway permission.

---

## 2) DeepSeek adapter (Replace / new)

| Item | Target |
|------|--------|
| Transport | Chat Completions + `base_url` where vendor docs confirm (REQ-12 §2) |
| Model id | **Not frozen** in arch (L12-2); brief orient `deepseek-v4-pro` until live confirm |
| Contract | Implement the **same narrow client/turn surface** consumed by `InterviewEngine` (Interview D3) — hide Completions quirks inside adapter |
| Presence today | **Absent** in `src/` (T1) |
| Env nest (L12-3) | `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` · `…_BASE_URL` · `…_MODEL` |

Do **not** silently fall back to OpenAI if DeepSeek selected (REQ §4.3).

---

## 3) Error / usage classification (logical)

| Class | Intent |
|-------|--------|
| Config / fail-closed | Unknown provider; incomplete nest when deepseek/openai selected |
| Vendor / transport | HTTP/timeouts/auth from adapter — mapped to Engine-safe errors |
| Budget / confirm | Remain Engine / REQ-11 concerns — not provider-owned |

Exact fail-reason **string catalog** = Open (implement + thin product).

---

## 4) Module home (docs intent; name ≠ create)

Logical home for interview adapters/registry is **separate** from worker `src/aibridge/providers/` (AC-02). Concrete package path under `src/aibridge/` = implement/P1.3 choice; must not merge worker registry.

HTTP client reuse (e.g. shared transport helpers) allowed **without** sharing worker provider ids.
