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
```

Entrypoint: `python -m aibridge` (binds `PORT` / Railway `$PORT`).

## Quick start

```bash
cd doge-ai-bridge
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export AIBRIDGE_CHANNEL_BEARER_TOKEN='dev-channel-token'
export DOGESTONIA_API_BEARER_TOKEN='dev-gateway-token-different'
pytest -q
PORT=8080 python -m aibridge
```

## Story 01 scope

Channel façade + Bearer + event dedupe + `/healthz`/`/readyz`. No OpenAI Responses (03), no gateway HTTPS (05).
