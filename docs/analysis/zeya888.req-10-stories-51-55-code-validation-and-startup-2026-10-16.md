# REQ-10 STORY-51…55 — code validation + aibridge startup

**Method:** [`.cursor/rules/analysis.mdc`](../../../../.cursor/rules/analysis.mdc) — claims from code path:line, REQ/STORY paths, live logs  
**Emitted:** 2026-10-16T12:27:56Z (`builder_resolve_queue.py --print-utc-now`)  
**Focus:** `doge-ai-bridge` · **builder_project:** aibridge  
**Inputs:** [`REQ-10`](../requirements/REQ-10-AI-PROVIDER-SELECTION-AND-MOCK-MODE.md) · package [`req-10-ai-provider-selection-and-mock-mode`](../tasks/backlog-stories/req-10-ai-provider-selection-and-mock-mode/INDEX.md) · arch [`ai-provider-selection/`](../architecture/ai-provider-selection/00-overview.md)

---

## 1) Verdict

| Question | Answer |
|----------|--------|
| Stories 51…55 vs code | **AC-10-01…10 Present** (see §2) |
| Why local-five / `make serve` fails | **Postgres down** on `127.0.0.1:5432` during `create_app` → process never listens (`health → 000`) |
| Missing REQ-10 env? | **No** for process crash. New provider/allow-mock vars affect **/readyz + accept after start**, not import |
| Live OpenAI text (54) | **Real HTTP adapter** in prod path; tests mock transport |

---

## 2) AC matrix (path:line)

| AC | Status | Evidence |
|----|--------|----------|
| **AC-10-01** text port | Present | `providers/registry.py:48–61` · accept `app.py:771` |
| **AC-10-02** image port independent | Present | `registry.py:69–79` · accept `app.py:819` |
| **AC-10-03** mock+mock no live vendor | Present | `providers/adapters.py` Mock* · tests `test_mock_accept_pipe_story_52.py` |
| **AC-10-04** env flip same accept API | Present | selectors `config.py:222–229` · resolve in accept `app.py:709–710,771,819` |
| **AC-10-05** unknown fail-closed | Present | `registry.py:25–37` · readiness `readiness.py:122–123` |
| **AC-10-06** mock L2 + HTTPS poster | Present | Mock adapters + Present `poster/storage.py` · story-52 tests |
| **AC-10-07** docs + mock-first REQ-58 | Present | `docs/runtime-docs/02-ai-provider-selection.md` · `03-provider-verify-matrix.md` · story-55 tests |
| **AC-10-08** mock+mock ready w/o OpenAI key | Present | `config.py` `worker_openai_presence_required` · `readiness.py:144–146` |
| **AC-10-09** refuse mock without allow | Present | `readiness.py:125–126` reason `worker_mock_not_allowed` · accept `app.py:600–607` |
| **AC-10-10** live text `{stories}` → L2 | Present | `providers/openai_text_live.py:123–161` (`ProductionResponsesClient`) |

**Modules:** `src/aibridge/providers/` — ports, ids, errors, registry, adapters, `openai_text_live.py`.  
**Image live:** deferred — `OpenAIImagePosterProvider` raises `NotImplementedError` (L10-5).

### Pytest (isolated env, 2026-10-16T12:27Z+)

With `DATABASE_URL=` + `AIBRIDGE_ALLOW_MEMORY_STORES=true` (avoid host `.env` postgres):

```
tests/test_provider_ports_story_51.py
tests/test_mock_accept_pipe_story_52.py
tests/test_readyz_allow_mock_story_53.py
tests/test_openai_text_live_story_54.py
tests/test_provider_verify_matrix_story_55.py
→ 34 passed
```

Default `pytest` from cwd that loads `.env` with dead postgres **imports `create_app` and crashes** — same root cause as serve (§3). Not an AC failure.

---

## 3) Startup failure (local-five / make serve)

### Symptom

[`scripts/shell/local-five-serve-and-health.sh`](../../../../scripts/shell/local-five-serve-and-health.sh) / terminal:

```
FAIL aibridge/health http://127.0.0.1:8080/health -> 000000 (after 60s)
```

`000` = nothing listening (crash before bind), **not** `/ready` 503.

### Root cause (log + reproduce)

[`scripts/logs/local-five/aibridge.log`](../../../../scripts/logs/local-five/aibridge.log) and live `make serve` 2026-10-16:

```
app.py:1063 create_app()
  → app.py:511 _init_stores
  → app.py:183 apply_migrations(settings.database_url)
  → db.py:31 psycopg.connect
psycopg.OperationalError: … 127.0.0.1:5432 … Connection refused
make: *** [serve] Error 1
```

Probe this session: `nc -z 127.0.0.1 5432` → **PG_DOWN**.  
`curl` `/health` → unreachable (`health=000`).

### Why `AIBRIDGE_ALLOW_MEMORY_STORES=true` did not help

Operator `.env` (read via Settings, secrets not logged): `database_url` is postgres (`db_is_pg True`) **and** `allow_memory True`.

In [`app.py:182–183`](../src/aibridge/app.py), if URL is postgres, migrations run **before** memory fallback. Except at `:189–194` catches `RuntimeError|OSError|ValueError|…` — **not** `psycopg.OperationalError`. Connection refused → process exit.

`.env.example:33` documents local throwaway: **sqlite or empty + ALLOW_MEMORY=true** — not postgres URL pointing at a dead host.

### Not REQ-10

Missing `AIBRIDGE_WORKER_*_PROVIDER` / `AIBRIDGE_ALLOW_MOCK_PROVIDERS` would, **after** a successful start and with worker enabled + mock, yield `/readyz` **503** `worker_mock_not_allowed` (`readiness.py:125–126`). That is a different failure mode from `health → 000`.

---

## 4) Env checklist (REQ-10 + start)

### New / REQ-10 (`.env.example:63–70` ≡ `config.py:222–235`)

| Variable | Default / unset | When needed |
|----------|-----------------|-------------|
| `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` | blank → `mock` | Optional; set `openai` for live text (54) |
| `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` | blank → `mock` | Leave `mock` in v1 (live image deferred) |
| `AIBRIDGE_ALLOW_MOCK_PROVIDERS` | `false` | **`true` for local mock worker** when `ENABLED=true`; **false** on public board |
| Model slots | nest | Required for fail-closed only if provider=`openai` |

Worker still needs REQ-09 vars when enabled: `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED`, `_S2S_TOKEN`, storage credential, etc.

### To get process listening again (ops — pick one)

1. **Start local Postgres** that matches `DATABASE_URL` in `.env`, then `make serve`.  
2. **Local throwaway (not for residents):** set non-postgres / empty `DATABASE_URL` + `AIBRIDGE_ALLOW_MEMORY_STORES=true` per `.env.example:33`, then `make serve`.

Do **not** expect `ALLOW_MEMORY=true` alone to fix a postgres URL to a refused port.

### After start — mock worker ready

If `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED=true` and providers are mock: set `AIBRIDGE_ALLOW_MOCK_PROVIDERS=true` or expect `worker_mock_not_allowed`. Current Settings probe: `worker_enabled False` → allow-mock gate not engaged for readyz worker path.

---

## 5) Serve retry evidence (this session)

| Check | Result |
|-------|--------|
| Postgres `:5432` | DOWN |
| `make serve` | Error 1 · `OperationalError` Connection refused (same stack as §3) |
| `GET /health` | unreachable (`000`) |
| Story pytest (isolated env) | **34 passed** |

No product-code fix in this report (out of plan scope). Optional follow-up: catch `OperationalError` in `_init_stores` or fail-soft when `ALLOW_MEMORY` — separate ask.

---

## 6) Link matrix

| Artifact | Role |
|----------|------|
| REQ-10 | Product AC |
| STORY-51…55 package INDEX | Backlog |
| `ai-provider-selection/` | Target tech |
| This report | Code validation + startup RCA |
| `scripts/logs/local-five/aibridge.log` | Crash evidence |

---

## 7) Method notes

- Inputs ≠ target tech arch ≠ new work items.  
- Name ≠ create; this report does not invent env SSOT beyond Present `.env.example` / `config.py`.  
- Startup RCA is **infrastructure / DATABASE_URL**, not missing provider selectors.
