# STORY-AIBRIDGE-45 — Live Telegram deployment verification (AC-09)

## Meta
- **Key:** `STORY-AIBRIDGE-45-compat-live-telegram-verify`
- **Status:** ✅ P5 Done · G-01…G-03 **WAIVED** · TASKED=0 · next **P7** (skip P6) · pkg-000044 · 2026-09-24T12:17:21Z · **implemented, live verification pending** · **no invent live Telegram SUCCESS**
- **Parent Epic:** [`EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md`](../../EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md)
- **source:** `backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-45-compat-live-telegram-verify.md`
- **decision_ref:** [`STORY-AIBRIDGE-45-….md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-45-compat-live-telegram-verify.md) · [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §11.5 · AC-09 · §15 · [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §5.2–5.3
- **Package:** [`req-07-openai-strict-schema-compat/INDEX.md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/INDEX.md)
- **Skill declared:** `test-master` (evidence discipline)
- **Active pkg (wave):** `pkg-000044-20260924-epic-aibridge-05-story-45-compat-live-telegram-verify.yaml`
- **P1 materialize:** 2026-09-24T12:07:46Z
- **P3 close:** 2026-09-24T12:11:06Z · [run-summary](../../../../run-reports/run-summary-20260924-1211-story-aibridge-45-p3.md)
- **P4 audit:** 2026-09-24T12:14:42Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-45-compat-live-telegram-verify-20260924.md)
- **P5 disposition:** 2026-09-24T12:17:21Z · [p5](../../../../run-reports/run-summary-20260924-1217-story-aibridge-45-p5-disposition.md)
- **Gate:** [t04](./task-aibridge-45-t04-story-gate/README.md) **PASS** (deferred_live)
- **Depends:** STORY-44 Implemented; deployed image with 41–44

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-07 AC-09 / §15 | [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §11.5 · AC-09 · §15 |
| Live verify | [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §5.2–5.3 |
| Pilot runbook | [`AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md`](../../../../runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md) |
| Preflight checklist | [`req-07-ac09-pilot-preflight-checklist-20260924.md`](../../../../ops/req-07-ac09-pilot-preflight-checklist-20260924.md) |
| AC-09 evidence | **BLOCKED** [`req-07-ac09-live-evidence-BLOCKED-20260924.md`](../../../../ops/req-07-ac09-live-evidence-BLOCKED-20260924.md) · PASS template **absent** |

## Scope
- After Railway deploy of image containing 41–44: one real Telegram → n8n → aibridge → **real** OpenAI turn; no `invalid_function_parameters`; meaningful interview reply; no gateway stash before existing dual-confirm.
- Write redacted live evidence under template path:  
  `docs/ops/req-07-ac09-live-evidence-YYYYMMDD.md`  
  Fields: UTC time, deployment/version or commit SHA, scenario id, pass/fail, correlation/request ID. **No** user narrative, Bearer, API keys, or full tool/args.
- Only after PASS: focus **production verified / rollout complete**. Until then keep **implemented, live verification pending** (after 44).
- **Defer path** if no pilot env: honest BLOCKED/deferred — **do not invent** Telegram / Railway / OpenAI SUCCESS.

## Вне scope
- Using live as the only proof; n8n workflow redesign; creating the evidence file before the live run (name ≠ create); product invent beyond 41–44 image.

## Context
P3: no pilot env confirmed — AC-09 live **deferred_live / BLOCKED**. Merge-gate STORY-44 remains automated proof.

## Target / AC
- [x] AC-09 satisfied **or** documented defer without invent PASS → **BLOCKED** note linked.
- [x] Deployed `/readyz` ready before the live turn (§15) — **N/A** (live not run); preflight documented Unknown/Not probed.
- [x] Nested tasks Done at execute (defer disposition recorded).

## Nested tasks (pkg-000044)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-45-t01-pilot-preflight-readyz-checklist](./task-aibridge-45-t01-pilot-preflight-readyz-checklist/README.md) | §15 /readyz + deploy checklist | **Done** |
| t02 | [task-aibridge-45-t02-live-turn-and-redacted-evidence](./task-aibridge-45-t02-live-turn-and-redacted-evidence/README.md) | AC-09 + evidence (name≠create) | **Done** · deferred_live |
| t03 | [task-aibridge-45-t03-defer-blocked-without-pilot-env](./task-aibridge-45-t03-defer-blocked-without-pilot-env/README.md) | defer if no pilot | **Done** · BLOCKED |
| t04 | [task-aibridge-45-t04-story-gate](./task-aibridge-45-t04-story-gate/README.md) | story AC gate | **PASS** (deferred_live) |
