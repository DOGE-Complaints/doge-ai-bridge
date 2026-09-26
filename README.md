# doge-ai-bridge

Python ASGI runtime: n8n Telegram channel façade → (later) OpenAI Responses → gateway Story Intake.

**Builder profile:** `aibridge` · **Requirement:** [REQ-01](docs/requirements/REQ-01-doge-ai-bridge-runtime.md)

## Module path

```text
src/aibridge/app.py          # FastAPI ASGI app (create_app / app)
src/aibridge/config.py       # env settings
src/aibridge/auth.py         # channel Bearer (constant-time)
src/aibridge/schemas.py      # channel OAS models
src/aibridge/channel.py      # turns/actions stub processor
src/aibridge/dedupe.py       # (channel, event_id) store
src/aibridge/content.py      # local manifest load + hashes (no GitHub fetch)
src/aibridge/registry.py     # content_bundle register-once (memory/sqlite)
src/aibridge/sessions.py     # session content_bundle_hash pin
src/aibridge/bundle_gc.py    # GC after grace when unreferenced
src/aibridge/deployment.py   # startup verify + register
```

Primary start: `make serve` / `make dev` (loads required `./.env` — G8). Thin alias: `python -m aibridge` (binds `PORT` / Railway `$PORT`, app `aibridge.app:app`).

## Quick start

```bash
cd doge-ai-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
# Ensure ./.env exists (required by Make serve/dev)
pytest -q
make serve
# or: make dev
# thin alias (no Make .env load): PORT=8080 python -m aibridge
```

**Runbook (web only, local + Railway):** [`docs/runbooks/aibridge-web-service-local-railway.md`](docs/runbooks/aibridge-web-service-local-railway.md). Full pilot (n8n/Telegram): [`docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md`](docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md).

**QA inbound/outbound (stories 23–35):** [`docs/qa/inbound-outbound/TEST-MANUAL.md`](docs/qa/inbound-outbound/TEST-MANUAL.md) · matrices [`TRACEABILITY-MATRIX.md`](docs/qa/inbound-outbound/TRACEABILITY-MATRIX.md).

**Railway (Railpack):** start command is pinned in [`railpack.json`](railpack.json) (`python -m uvicorn --app-dir src aibridge.app:app …`). Root `requirements.txt` mirrors runtime deps from `pyproject.toml`. See local analysis note `docs/analysis/railway-railpack-start-command-failure-2026-09-13.md` if present.

## Stories 01–02 scope

- **01:** Channel façade + Bearer + event dedupe + `/healthz`/`/readyz`.
- **02:** Local content load/hash/pin, register-once registry, session pin, `/readyz` bundle verify, GC + CI packaging note.

No OpenAI Responses (03), no gateway HTTPS (05). Absolute CI instruction/pack paths remain **Unknown** until pinned in env.
