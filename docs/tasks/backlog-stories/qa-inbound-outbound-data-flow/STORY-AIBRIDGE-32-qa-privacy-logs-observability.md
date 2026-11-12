# STORY-AIBRIDGE-32-qa-privacy-logs-observability — QA — Privacy, logs, and observability

## Meta
- **Key:** `STORY-AIBRIDGE-32-qa-privacy-logs-observability`
- **Status:** Implemented (P3 closed · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §2 trust · §10.10 SEC-* · §14 spies
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
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

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** reuse spies/channel/openai/gateway seeds; generate SEC-* spy snapshots  
> **Clusters:** `spies`, `channel`, `openai`, `gateway` · **Layer:** `tests/integration/` · **Harness:** spy bag §14; Recording* call captures without printing secrets

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-32-t01-generate-sec-spy-fixtures` | Done | Generate SEC-* spies envelopes into package `fixtures/` |
| **T02** | `task-aibridge-32-t02-promote-fixtures` | Done | Copy to `tests/fixtures/spies/` (+ related clusters); originals stay |
| **T03** | `task-aibridge-32-t03-implement-privacy-obs-tests` | Done | Assert redaction; metrics scrub; token hash-only |
| **T04** | `task-aibridge-32-t04-story-gate` | Done | All SEC-*; CI artifacts secret-free; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
