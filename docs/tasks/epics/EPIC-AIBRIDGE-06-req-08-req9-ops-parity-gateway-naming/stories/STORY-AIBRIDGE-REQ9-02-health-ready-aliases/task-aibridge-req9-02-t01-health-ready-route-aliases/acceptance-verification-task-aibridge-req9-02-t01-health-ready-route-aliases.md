# Acceptance — task-aibridge-req9-02-t01-health-ready-route-aliases

| Field | Value |
|-------|-------|
| **Date** | 2026-09-26T12:26:24Z |
| **Result** | **Done** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| `GET /health` registered | `src/aibridge/app.py` `@app.get("/health")` stacked with `/healthz` |
| `GET /ready` registered | `src/aibridge/app.py` `@app.get("/ready")` stacked with `/readyz` |
| z-paths kept | `/healthz` `/readyz` decorators remain |
| readiness logic unchanged | same `evaluate_readiness` / `readiness_payload` body |
