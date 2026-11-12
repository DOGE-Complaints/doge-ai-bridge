# Task: docs/tests — tombstone, audit retention, n8n retention checklist

**Status:** Done  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-16-privacy-retention.md`  
**Parent story:** [`STORY-AIBRIDGE-16-privacy-retention.md`](../STORY-AIBRIDGE-16-privacy-retention.md)  
**P1 scaffold:** 2026-09-13T17:43:00Z
**P3 Done:** 2026-09-13T17:49:14Z  
**Maps:** Scope #5–#6 · privacy-pilot §3

## Purpose

Document and/or test: minimized non-PII replay tombstone may be retained for security/audit window; redacted audit metadata may use separate retention; n8n execution retention is verified separately before residents (checklist evidence, not inventing n8n JSON).

## Code Facts (verified exists — P1)

1. `docs/runbooks/privacy-pilot.md` §2–§3 — aibridge + n8n checklists (unchecked).
2. REQ-03 §6.2 allows tombstone + separate audit retention + separate n8n verification.
3. Live n8n retention proof is ops (sibling story 15 residual) — do not invent Bot secrets.

## AC/DoD

- [x] Tombstone / audit-retention policy reflected in runbook or code comments + test where applicable.
- [x] n8n retention checklist items in `privacy-pilot.md` §3 cross-linked or evidenced (ops checkboxes; no fake PASS).
- [x] Does not invent live Telegram credentials.
- [x] `Skill declared: python-pro` present.

## Where to change

`docs/runbooks/privacy-pilot.md`; optional ops note under `docs/ops/`; tests for tombstone behavior if code lands in t02/t03.

## Verification commands

```bash
rg -n "tombstone|audit|n8n|retention" doge-ai-bridge/docs/runbooks/privacy-pilot.md
test -f doge-ai-bridge/docs/runbooks/privacy-pilot.md
```

## Out of scope

Mandatory credential-stripped n8n export (REQ-03 §8 / P2-04).
