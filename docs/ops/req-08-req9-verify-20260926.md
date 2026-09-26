# REQ-08 / REQ9 — verify note (aibridge) · 20260926

| Field | Value |
|-------|-------|
| **UTC** | `2026-09-26T13:03:46Z` |
| **Nested SHA** | `ab8d9f3` |
| **Story** | STORY-AIBRIDGE-REQ9-04 · pkg-000048 · Lock **C** |
| **Skill** | test-master · soft code-documenter |

**Secrets:** none recorded below (no tokens / bearer values).

---

## Local (t01) — PASS

| Check | Result |
|-------|--------|
| Start | `make serve` target → uvicorn `aibridge.app:app` · `127.0.0.1:${PORT:-8080}` (process up) |
| `GET /health` | **200** · `{"status":"ok"}` |
| `GET /ready` | **200** · `{"status":"ready"}` |
| Template names | `.env.example` + Settings: `GATEWAY_BASE_URL` · `GATEWAY_SERVICE_API_TOKEN` · `SPA_BASE_URL` present |
| Runtime config | Settings attrs set (local `.env`); values not copied here |

---

## Railway (t02) — vars PASS · remote `/health` residual Y

| Field | Fact |
|-------|------|
| Project | `DOGEstonia` · `bd6b5707-fe1f-4a9d-a43c-b5f7582b9d6d` |
| Environment | `tallinn-demo` · `297a80a7-9fc9-4049-98a8-1b0d12799fac` |
| Service | `doge-ai-bridge` · `2ef34661-d247-476e-8ab1-bbcc3f70a997` |
| Public host | `aibridge.dogestonia.me` |

### Target vars (set + verify)

| Name | Present | Equals legacy | Notes |
|------|---------|---------------|-------|
| `GATEWAY_BASE_URL` | Y | = `DOGESTONIA_INTAKE_BASE_URL` | set via Railway MCP · `skipDeploys` |
| `GATEWAY_SERVICE_API_TOKEN` | Y | = `DOGESTONIA_API_BEARER_TOKEN` | set via Railway MCP · `skipDeploys` |
| `SPA_BASE_URL` | Y | = `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` | set via Railway MCP · `skipDeploys` |
| `AIBRIDGE_CHANNEL_BEARER_TOKEN` | Y | ≠ gateway token | Keep / R8 |

### Remote smoke

| Endpoint | HTTP | Body (minimal) | Verdict |
|----------|------|----------------|---------|
| `GET https://aibridge.dogestonia.me/healthz` | **200** | `{"status":"ok"}` | PASS (live image) |
| `GET https://aibridge.dogestonia.me/readyz` | **200** | `{"status":"ready"}` | PASS (live image) |
| `GET https://aibridge.dogestonia.me/health` | **404** | `{"detail":"Not Found"}` | **FAIL** — residual |
| `GET https://aibridge.dogestonia.me/ready` | **404** | `{"detail":"Not Found"}` | **FAIL** — residual |

**Do not invent SUCCESS** for remote `/health`/`/ready` on current deploy.

---

## Residual Y (explicit)

1. **Live deploy** still serves `/healthz`/`/readyz` only; `/health`/`/ready` 404 until redeploy picks up REQ9-02 aliases (vars set with **skipDeploys** — no redeploy this P3).
2. **Legacy** `DOGESTONIA_INTAKE_BASE_URL` / `DOGESTONIA_API_BEARER_TOKEN` / `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` still present alongside target names (Railway coexistence; product hard-cut is code-side from 03).

---

## G9 clause

Local verify **PASS**. Railway target **names+values** verified **PASS**. Remote canonical `/health`/`/ready` **residual Y** (linked above) — not claimed PASS.

Evidence links: t01 local · t02 Railway/residual · t04 topology sync.
