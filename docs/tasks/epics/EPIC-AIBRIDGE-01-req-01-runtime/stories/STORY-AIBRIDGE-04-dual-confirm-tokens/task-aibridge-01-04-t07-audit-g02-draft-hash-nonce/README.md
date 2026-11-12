# Task: implement — bind draft-hash + nonce on action tokens (G-02)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_04_audit_20260912`  
**Gap:** G-02 (Info) — P4 audit 2026-09-12  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-04-dual-confirm-tokens-20260912.md`  
**Parent story:** [`STORY-AIBRIDGE-04-dual-confirm-tokens.md`](../STORY-AIBRIDGE-04-dual-confirm-tokens.md)  
**P5 scaffold:** 2026-09-12T21:45:18Z  
**P6 Done:** 2026-09-12T21:47:12Z

## Purpose

Extend `TokenRecord` bind domain with **draft_hash** and **nonce** (REQ-01 Send binding language). Story AC #1–#5 already PASS; this closes the Info residual without gateway HTTP (05).

**Out of this task:** Persist tokens across process (G-01 → STORY-AIBRIDGE-08); live gateway executor.

## Code Facts (verified exists — post P6)

1. `TokenRecord.draft_hash` / `nonce` — `action_tokens.py`.
2. `issue()` mints unique nonce; optional `draft_hash`.
3. `ConfirmSession.draft_hash` + `set_frozen_tool_intent(..., draft_hash=)` — `confirm.py`.
4. Tests — `tests/test_action_tokens.py`, `tests/test_interpret_vs_send.py`.

## AC/DoD

- [x] `TokenRecord` stores `draft_hash` (optional/str) and unique `nonce` per issue.
- [x] Issue path mints nonce; Send (and other) tokens can carry session `draft_hash`.
- [x] `bind_snapshot` exposes hash + nonce; never raw token.
- [x] Tests cover bind fields.
- [x] `Skill declared: python-pro` present.

## Where to change

- `src/aibridge/action_tokens.py`, `confirm.py` (session draft_hash + mint)
- `tests/test_action_tokens.py` (and/or small confirm bind test)

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/pytest -q tests/test_action_tokens.py tests/test_interpret_vs_send.py
```
