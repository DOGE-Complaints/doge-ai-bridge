# REQ-07 AC-09 live evidence — BLOCKED (2026-09-24)

**Story:** STORY-AIBRIDGE-45-compat-live-telegram-verify  
**Stamp:** 2026-09-24T12:11:06Z  
**Task:** t03 (defer) · linked from t01 checklist / t04 gate  
**Pkg:** pkg-000044  
**Disposition:** `deferred_live` / **BLOCKED** — AC-09 live not executed

## BLOCKED facts (verified this session)

| Probe | Result |
|-------|--------|
| Pilot runbook | Present on disk |
| Railway project / deploy SHA (41–44 image) | **Unknown** — not probed; MCP Railway out of P3 authorized scope |
| Deployed `/readyz` 200 | **Not observed** — no invent SUCCESS |
| Live Telegram → n8n → aibridge → OpenAI turn | **Not executed** |
| `docs/ops/req-07-ac09-live-evidence-YYYYMMDD.md` (PASS template) | **Absent** (name ≠ create until live) |
| OpenAI 2xx / no `invalid_function_parameters` | **Not observed** |

## What was delivered instead (not live PASS)

1. Preflight checklist: [req-07-ac09-pilot-preflight-checklist-20260924.md](./req-07-ac09-pilot-preflight-checklist-20260924.md)
2. This BLOCKED note (honest defer)
3. Focus remains **implemented, live verification pending** (after STORY-44 merge-gate)

## Claim rule

Do **not** mark AC-09 as live PASS.  
Do **not** claim production verified / rollout complete.  
STORY-44 merge-gate remains the automated proof; live is not sole proof and was not run.

## Operator unblock

1. Deploy image containing STORY-41–44; confirm `/readyz` ready (§15).
2. Run one real Telegram → n8n → aibridge → OpenAI turn per TECH-ARCH §5.2–5.3.
3. Create redacted `docs/ops/req-07-ac09-live-evidence-YYYYMMDD.md` (fields only; no secrets).
4. Supersede this BLOCKED file; then story may claim AC-09 PASS / production verified.
