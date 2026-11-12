# STORY-AIBRIDGE-32 — QA — Privacy, logs, and observability

## Meta
- **Key:** `STORY-AIBRIDGE-32-qa-privacy-logs-observability`
- **Status:** 🟢 Implemented (P6 closed · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-04-qa-inbound-outbound.md`](../../EPIC-AIBRIDGE-04-qa-inbound-outbound.md)
- **source:** `backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`
- **decision_ref:** [`STORY-AIBRIDGE-32-qa-privacy-logs-observability.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) · [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) §2 trust · §10.10 SEC-* · §14 spies · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) ADR-Q1/Q2
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 · ADR-Q1/Q2
- **Skill declared:** `python-pro` · `test-master`
- **Active pkg (wave):** `pkg-000029-20260917-epic-aibridge-04-story-32-qa-privacy-logs-observability.yaml` (**immutable** under `run_mode=aibridge_32_audit_20260917`)
- **P1 materialize:** 2026-09-17T20:27:34Z
- **P3 closed:** 2026-09-17T20:33:31Z
- **P4 audited:** 2026-09-17T20:35:51Z
- **P5 disposition:** 2026-09-17T20:38:37Z · G-01/G-02 TASKED · G-03…G-05 WAIVED
- **P6 closed:** 2026-09-17T20:42:29Z · G-01/G-02 CLOSED
- **Gate:** [t04](./task-aibridge-32-t04-story-gate/README.md) · [acceptance PASS](./task-aibridge-32-t04-story-gate/acceptance-verification-task-aibridge-32-t04-story-gate.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Guide §2 / §10.10 SEC-* / §14 spies | [`AIBRIDGE-QA-…-GUIDE.md`](../../../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| ADR-Q1/Q2 fixtures | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Traceability SEC-001…010 | [`TRACEABILITY-MATRIX.md`](../../../../backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md) |
| Seed originals | reuse spies/channel/openai/gateway; generate SEC-* on P3 t01 into package [`fixtures/`](../../../../backlog-stories/qa-inbound-outbound-data-flow/fixtures/) |
| Harness | spy bag §14 · Recording* captures without printing secrets |

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Deleting or moving package `fixtures/` originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.

## Context

No PII/narrative/secrets in audit/metrics. Token hashes only in DB. Channel vs Gateway Bearer separation in captures. Prompt injection must not expose system prompt or enable arbitrary tools/URLs.

## Use cases / matrix IDs (must transfer from guide)

| ID | Scenario | Expected |
|----|----------|----------|
| SEC-001 | Narrative contains email/phone/personal name | Full narrative absent from structured audit logs and metrics. |
| SEC-002 | Error raised with secret in exception text | Secret redacted from response/logs. |
| SEC-003 | Channel request audited | Log only bounded IDs/statuses/lengths; not raw Bearer or full narrative. |
| SEC-004 | `/metrics` scrape | Contains counts/latencies/cache telemetry only; no IDs, text, token, draft body, or URL secrets. |
| SEC-005 | Error envelope | Stable bounded schema and generated `request_id`. |
| SEC-006 | PostgreSQL token inspection | Only token hash stored. |
| SEC-007 | OpenAI request capture | `store=false`; no gateway/channel secrets. |
| SEC-008 | Gateway request capture | Gateway Bearer only; no Channel Bearer. |
| SEC-009 | n8n workflow export | No credentials or secrets committed. |
| SEC-010 | Prompt injection asks model to call arbitrary URL/tool | Only allowlisted generated function is available; gateway origin/path remain server-owned. |

## Verified current state
- SEC-* spy envelopes in package `fixtures/` — **absent**; generate on P3 t01 (reuse prior cluster seeds).
- TRACEABILITY-MATRIX SEC-001…010 → this story key (`covered`).
- Layer `tests/integration/` exists; SEC matrix suite **absent** — create on P3 t03.
- Product: audit/metrics/redact/Recording* — assert-only in P3; no product invent in P1.

## Target / AC
- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] Guide **must** → automated asserts; **characterization** → capture-first.
- [ ] On story Done: required envelopes under `tests/fixtures/{cluster}/` as **copies**; originals remain in package `fixtures/`.

## Техническое решение

- **Approach (ADR-Q1/Q2):** generate SEC-* into package `fixtures/` (`schema_version=1.0`), promote=copy → `tests/fixtures/{spies,channel,openai,gateway}/`; tests in `tests/integration/`; spy bag §14; Recording* without printing secrets; no live Telegram.
- **Skill:** python-pro · test-master

## Nested tasks (pkg-000029 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-32-t01-generate-sec-spy-fixtures](./task-aibridge-32-t01-generate-sec-spy-fixtures/README.md) | Generate SEC-* spy envelopes | Done |
| t02 | [task-aibridge-32-t02-promote-fixtures](./task-aibridge-32-t02-promote-fixtures/README.md) | Promote copies | Done |
| t03 | [task-aibridge-32-t03-implement-privacy-obs-tests](./task-aibridge-32-t03-implement-privacy-obs-tests/README.md) | Privacy/obs suite | Done |
| t04 | [task-aibridge-32-t04-story-gate](./task-aibridge-32-t04-story-gate/README.md) | Gate all SEC-* | Done |
| t05 | [task-aibridge-32-t05-audit-g01-sec006-pg-hash-only](./task-aibridge-32-t05-audit-g01-sec006-pg-hash-only/README.md) | G-01 SEC-006 PG hash | Done |
| t06 | [task-aibridge-32-t06-audit-g02-sec010-tool-gen](./task-aibridge-32-t06-audit-g02-sec010-tool-gen/README.md) | G-02 SEC-010 tool_gen | Done |
