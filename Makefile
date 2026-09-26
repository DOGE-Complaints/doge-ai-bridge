.PHONY: serve dev

# Make start requires cwd ./.env (G8 / REQ-08 REQ9-01).
# App: aibridge.app:app (G9 Keep). Default PORT 8080.

serve:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src aibridge.app:app \
	  --host 127.0.0.1 --port $${PORT:-8080}

dev:
	set -a && . ./.env && set +a && \
	.venv/bin/python -m uvicorn --app-dir src aibridge.app:app \
	  --host 127.0.0.1 --port $${PORT:-8080} --reload --reload-dir src
