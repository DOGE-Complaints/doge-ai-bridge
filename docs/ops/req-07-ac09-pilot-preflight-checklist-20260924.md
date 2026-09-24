# REQ-07 AC-09 — pilot preflight checklist (2026-09-24)

**Story:** STORY-AIBRIDGE-45-compat-live-telegram-verify  
**Task:** t01  
**Stamp:** 2026-09-24T12:11:06Z  
**Pkg:** pkg-000044  
**Skill:** test-master (evidence discipline)

## Preflight probes (facts only)

| # | Check | Result |
|---|-------|--------|
| 1 | Pilot runbook on disk | **Present** — `docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md` |
| 2 | Deployed image SHA includes STORY-41–44 | **Unknown** — Railway deploy not probed this session (MCP list-projects out of P3 authorized scope; no invent SUCCESS) |
| 3 | Deployed `/readyz` ready (§15.1) | **Not probed** — no authorized Railway/public URL probe; local `127.0.0.1:8080/readyz` unreachable |
| 4 | AC-09 live evidence file | **Absent** — `docs/ops/req-07-ac09-live-evidence-YYYYMMDD.md` not created (name ≠ create until live) |
| 5 | Telegram → n8n → aibridge → OpenAI live turn | **Not executed** this session |

## Disposition

**No pilot env confirmed for AC-09 live.** Hand off to **t03** defer / BLOCKED path.  
Do **not** claim Railway SUCCESS, `/readyz` 200, or Telegram PASS.

## Pointers

- Runbook: [`../runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md`](../runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md)
- BLOCKED note (t03): [`req-07-ac09-live-evidence-BLOCKED-20260924.md`](./req-07-ac09-live-evidence-BLOCKED-20260924.md)
