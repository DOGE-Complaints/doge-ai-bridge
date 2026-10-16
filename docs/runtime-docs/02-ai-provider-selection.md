# AI provider selection + mock mode (worker)

Человекочитаемая ops-дока по **фактическому коду** (REQ-10 / STORY-51…55).  
Architecture SSOT: [`../architecture/ai-provider-selection/`](../architecture/ai-provider-selection/).

| Field | Value |
|-------|--------|
| **AC** | AC-10-07 (provider list + mock-first order with gateway REQ-58) |
| **Code** | `src/aibridge/providers/` · `src/aibridge/readiness.py` · worker accept middleware |
| **Residual** | Live OpenAI vendor SUCCESS against real credentials/network — **Unknown** unless ops proves; CI uses mocked invoke (STORY-54) |

---

## 1) Provider list (worker slots)

Worker sense-brief has **two independent** slots (not channel InterviewEngine — L10-1).

| Slot | Env | Allowed ids | Present behavior |
|------|-----|-------------|------------------|
| Text brief | `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` | `mock` \| `openai` | `mock` → Present corpus-grounded brief; `openai` → `providers/openai_text_live.py` from gateway `{stories:[…]}` |
| Image poster | `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` | `mock` \| `openai` | `mock` → deterministic PNG; `openai` → deferred NI (live image OOS v1) |

Defaults: both slots **`mock`**.

Nested model envs (required for readiness/accept when slot=`openai`):

| Env | When |
|-----|------|
| `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` | text provider = `openai` |
| `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` | image provider = `openai` |

Allow-mock (AC-10-09):

| Env | Role |
|-----|------|
| `AIBRIDGE_ALLOW_MOCK_PROVIDERS` | Truthy → allow worker slots `mock` at `/readyz` and accept; falsy → refuse with `worker_mock_not_allowed` |

Shared OpenAI key (worker gate when any worker slot=`openai`):

| Env | Role |
|-----|------|
| `OPENAI_API_KEY` | Required for worker readiness when a slot is `openai`; **not** required for worker gate when both slots are `mock` and allow-mock is on (AC-10-08) |

Accept route/auth unchanged: `POST /v1/worker/sense-brief/accept` + worker S2S token ([`01-api.md`](./01-api.md)).

---

## 2) Mock-first ops order (with gateway REQ-58)

Gateway sibling: [`58-req13-existing-issues-sense-brief-backfill-via-regenerate`](../../../doge-complaints-gateway/docs/requirements/58-req13-existing-issues-sense-brief-backfill-via-regenerate.md) (regenerate / backfill; mock-first dry run). **This focus does not invent gateway paths.**

Recommended order:

1. **Local / CI — mock first**  
   - `AIBRIDGE_ALLOW_MOCK_PROVIDERS=true`  
   - both worker providers `mock`  
   - `/readyz` ready without `OPENAI_API_KEY` (worker gate)  
   - one accept smoke: mock+mock → brief → poster → bind (no live vendor HTTP)
2. **Flip text to openai (optional)**  
   - set `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER=openai` + nested text model + `OPENAI_API_KEY`  
   - keep image `mock` in v1  
   - corpus shape `{stories:[…]}` or honest `corpus_insufficient`  
   - do **not** claim live vendor SUCCESS without credentials/network evidence
3. **Public / production**  
   - `AIBRIDGE_ALLOW_MOCK_PROVIDERS=false` (or unset)  
   - set openai slots as needed; mock without allow → refuse  
4. **Gateway REQ-58 backfill**  
   - after mock dry-run, ops may run regenerate/backfill per REQ-58  
   - live Issue proof = ops residual (not aibridge DoD)

---

## 3) Fail-closed notes

- Unknown provider id → fail-closed (no silent OpenAI fallback) — AC-10-05.  
- Mock without allow → `worker_mock_not_allowed` at readyz + accept — AC-10-09.  
- OpenAI text without stories → `corpus_insufficient` — AC-10-10.  
- Channel OpenAI registry unchanged (L10-1).

---

## 4) Verify matrix pointer

Harness entry + AC → test map: [`03-provider-verify-matrix.md`](./03-provider-verify-matrix.md).
