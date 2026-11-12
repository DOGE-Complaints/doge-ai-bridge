# Railway Railpack: Build image FAILED — no start command (2026-09-13)

**Scope:** `doge-ai-bridge` deploy on Railway  
**Symptom source:** operator screenshot — Railpack v0.39.0, step **Build > Build image** failed (~10s); Diagnosis failed  
**As-of:** 2026-09-13  
**Status:** Fix applied in repo (`railpack.json` + `requirements.txt`); live redeploy = operator verify

---

## 1. Symptom (facts from available log)

- Deployment status: **FAILED**
- Failed step: **Build image** (Initialization OK)
- Railpack message class: auto-start detection for Python — FastHTML / FastAPI / Flask / Django / else root `main.py` or `app.py`
- Prepare process cut off while planning (`railpack-… prepare /app --plan-out …`)
- Automatic Railway diagnosis: **failed** (no extra root cause from UI)

This matches the gateway failure class documented as «No start command detected» — not a mysterious runtime crash after boot.

---

## 2. Hypotheses (prioritized)

| Id | Hypothesis | Verdict |
|----|------------|---------|
| **H1** | Railpack cannot auto-detect start because ASGI app lives under `src/aibridge/app.py`, not root `app.py`/`main.py` | **Confirmed** — layout + missing `railpack.json` before fix |
| **H2** | Missing explicit `deploy.startCommand` in repo (or Custom Start Command in Railway UI) | **Confirmed** — Glob/ Grep: no `railpack.json` in aibridge before this change |
| **H3** | Wrong Root Directory (not `doge-ai-bridge`) | Possible residual — operator checks Railway service settings |
| **H4** | App env / `/readyz` fail-closed after container starts | **Out of scope** for this build failure (container never built) |

---

## 3. Evidence (code / docs)

| Fact | Path |
|------|------|
| FastAPI `app` module | `src/aibridge/app.py` (`app = create_app()`) |
| Local entrypoint | `src/aibridge/__main__.py` → `python -m aibridge` |
| No Dockerfile invented | aibridge root (pre-fix) |
| Gateway precedent | `doge-complaints-gateway/railpack.json` |
| Gateway write-up | `doge-complaints-gateway/docs/runtime-docs/manuals/server-env-quickstart.md` §4.7–§4.8 |

Gateway §4.7: Railpack looks for root `app.py`/`main.py`; FastAPI under `src/` needs explicit startCommand.  
Gateway §4.8: use `python -m uvicorn` (not bare `uvicorn` on PATH); pin Python 3.11; optional root `requirements.txt` for stable install.

---

## 4. Applied fix (mirror gateway — no Dockerfile)

1. **`railpack.json`** (repo root):

```json
{
  "$schema": "https://schema.railpack.com",
  "packages": { "python": "3.11" },
  "deploy": {
    "startCommand": "python -m uvicorn --app-dir src aibridge.app:app --host 0.0.0.0 --port ${PORT:-8000}"
  }
}
```

Justification:

- Same pattern as gateway (proven on Railway).
- `python -m uvicorn` avoids `uvicorn: command not found`.
- `--app-dir src` imports `aibridge.app:app`.
- `0.0.0.0` + Railway-owned `PORT`.

2. **`requirements.txt`** — runtime deps aligned with `pyproject.toml` (fastapi, uvicorn[standard], pydantic, pydantic-settings, psycopg[binary], pyyaml, httpx).

3. **README** — one-liner pointing at `railpack.json`.

---

## 5. Residual risks (after build succeeds)

1. Railway **Root Directory** must be the `doge-ai-bridge` repo root (where `pyproject.toml` / `railpack.json` live).
2. Process may start but `/readyz` still fail-closed without required env (channel Bearer ≠ gateway Bearer, content bundle paths, DB, etc.) — separate ops checklist; not this prepare failure.
3. This analysis file is **local operator zone** (`docs/analysis/`) — per commit methodology **not** committed; deploy artifacts are.

---

## 6. Operator verify

1. Push includes `railpack.json` + `requirements.txt` (+ README).
2. Redeploy on Railway.
3. Expect Build image to pass prepare; then check Deploy logs for uvicorn bind on `$PORT`.
4. Smoke: `GET /healthz` (liveness) vs `GET /readyz` (may still need env).
