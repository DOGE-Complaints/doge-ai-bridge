# Task: fixtures — pin n8n workflow export (N8N-WF-001)

**Status:** Done · 2026-09-18T12:32:14Z  
**Skill declared:** test-master  
**Secondary skill:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`  
**Parent story:** [`STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md`](../STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md)  
**P1 scaffold:** 2026-09-18T12:27:40Z  
**Maps:** N8N-WF-001 · ADR-Q1 promote=copy · gaps §36 T02

## Purpose

Operator places credential-stripped export at `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json` (**do not invent body**). Package pointer `fixtures/meta/n8n-wf-001-pin-pointer.json` records sha256 + relative_path + verified_at (+ channel_openapi_version as applicable). Promote=copy → `tests/fixtures/meta/`. If export absent: explicit defer with reason (capture-first).

**Out of this task:** Layer E relabel (t01); out-of-CI smoke (t03); invent export JSON; Railway SUCCESS; live TG.

## AC/DoD

- [x] Pin pointer envelope `schema_version=1.0` in package `fixtures/` (or explicit defer documented).
- [x] Matching **copy** under `tests/fixtures/meta/` when pin present; hash_eq vs package original.
- [x] No invent of export body / secrets.
- [x] `Skill declared: test-master` present.

## Where to change

- `docs/ops/n8n-channel-workflow/exports/` — operator (P3)
- package `fixtures/meta/n8n-wf-001-pin-pointer.json` + `tests/fixtures/meta/` promote=copy — **P3**
