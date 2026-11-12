# Task: tests — probe alias parity /health↔/healthz /ready↔/readyz

**Status:** Done · P3 2026-09-26T12:27:23Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md`](../STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md)  
**P1 scaffold:** 2026-09-26T12:24:30Z  
**P3 closed:** 2026-09-26T12:27:23Z  
**Maps:** REQ-08 G2 peer-parity

## Purpose

Add probe tests asserting short paths peer-parity with z-paths (status + body contract). Prefer focused new tests over rewriting entire READY-* matrix.

## AC/DoD

- [x] Tests cover `GET /health` parity with `/healthz` (status/body).
- [x] Tests cover `GET /ready` parity with `/readyz` (status/body) under comparable fixture.
- [x] Existing z-path suites remain green.
- [x] `Skill declared: python-pro` present.

## Where changed

- `tests/test_health.py` — alias parity tests (ready + not_ready)

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-req9-02-t02-probe-alias-parity-tests.md`](./acceptance-verification-task-aibridge-req9-02-t02-probe-alias-parity-tests.md)
- pytest: 7 passed (`tests/test_health.py`)
