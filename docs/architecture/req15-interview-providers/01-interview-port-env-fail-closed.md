# Interview port, env, fail-closed

**Overview:** [`00-overview.md`](./00-overview.md)  
**Product locks:** REQ-12 **L12-1**, AC-AIB-12-01 / 02 / 05

---

## 1) Env SSOT (interview only)

| Variable | Values | Rule |
|----------|--------|------|
| `AIBRIDGE_INTERVIEW_PROVIDER` | `deepseek` \| `openai` | **Required** (Interview D2 · L12-1) |
| `AIBRIDGE_INTERVIEW_DEEPSEEK_API_KEY` | secret | **Required** when provider=`deepseek` (L12-3) |
| `AIBRIDGE_INTERVIEW_DEEPSEEK_BASE_URL` | HTTPS base | **Required** when provider=`deepseek`; example default `https://api.deepseek.com` |
| `AIBRIDGE_INTERVIEW_DEEPSEEK_MODEL` | model id string | **Required** when provider=`deepseek`; live id confirm L12-2; orient `deepseek-v4-pro` |
| `OPENAI_API_KEY` / `OPENAI_MODEL` | Present | **Required** when provider=`openai` (Keep) |

| Forbidden | Why |
|-----------|-----|
| Using `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` / `…_IMAGE_POSTER_PROVIDER` as interview switch | AC-AIB-12-02 · worker arch L10-1 |
| Unset / unknown / empty → silent OpenAI | §4.3 · AC-05 · Interview D2 |
| Unset → recording engine as “OK interview” | Present `app.py:427–428` is **not** typed provider fail |

**Fail-closed (D2):** missing/unknown provider id → refuse interview wire / readiness-class failure (exact string Open for implement). Transition deploys set `openai` **explicitly**. Incomplete DeepSeek nest when provider=`deepseek` → same class fail-closed.

Template: [`.env.example`](../../../.env.example) §4b.

---

## 2) Shared port (logical)

| Component | Role |
|-----------|------|
| Interview provider registry | Map env id → adapter |
| InterviewProviderPort | Resolve backend for Keep `InterviewEngine` |
| Callers | Channel wire today; future REQ-13 roles — **same port** |

**Interview D3:** Port **supplies** client/turn backend; does **not** replace `InterviewEngine` in v1.

**Interview D4:** Provider id bound at process wire/start; **no** in-session flip API in v1.

---

## 3) Nest rules (L12-3)

When `AIBRIDGE_INTERVIEW_PROVIDER=deepseek`, the three `AIBRIDGE_INTERVIEW_DEEPSEEK_*` slots above are **required**.

When provider = `openai`, Present `OPENAI_API_KEY` + `OPENAI_MODEL` Keep (cite `config.py` / `app.py`).

---

## 4) Trust

| Domain | Must not |
|--------|----------|
| Channel Bearer | Carry model vendor keys |
| Telegram service | Hold interview provider secrets |
| Worker registry | Select interview backend |
