# Task: implement — ASGI health skeleton (`$PORT`, `/healthz`, `/readyz`)

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-01-runtime/STORY-AIBRIDGE-01-channel-facade-auth.md`  
**Parent story:** [`STORY-AIBRIDGE-01-channel-facade-auth.md`](../STORY-AIBRIDGE-01-channel-facade-auth.md)

## Purpose

Python project + single ASGI app bound to Railway `$PORT`; `GET /healthz`, `GET /readyz` (minimal: process up + channel auth config present). Exact module path chosen at implement (currently **Unknown** per `00-overview.md` §3/§13).

**Out of this task:** channel routes (t03); Bearer middleware (t02); event dedupe (t04).

## Code Facts (verified exists)

1. No product `*.py` under `doge-ai-bridge/` (docs + LICENSE only) — Phase 0 / P1 apply.
2. Topology: single ASGI on `$PORT`, no worker — `doge-ai-bridge/docs/architecture/runtime/00-overview.md` §3.
3. Module path / framework package: **Unknown** — `00-overview.md` §13.
4. Health/readiness requirements — REQ-01 §18; `docs/architecture/runtime/04-ops-security.md` §1.

## AC/DoD

- [x] `GET /healthz` returns success when process is up.
- [x] `GET /readyz` reflects channel auth config presence (shell for equal-token fail in t02 / AC #5).
- [x] App binds to Railway `$PORT`.
- [x] README includes `Skill declared: python-pro` (story AC #6).

## Where to change

- New product tree under `doge-ai-bridge/` (ASGI app package + entrypoint — path chosen at P3).
- Packaging as needed for Railway deploy (no invent of secrets).

## Verification commands

```bash
cd doge-ai-bridge && python3 -V
# After implement: import/ASGI smoke; rg healthz|readyz on new files
```
