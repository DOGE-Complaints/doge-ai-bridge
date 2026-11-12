# qa-inbound-outbound-data-flow — INDEX

> **Пакет:** QA automated coverage — inbound/outbound data flow
> **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) (2026-09-17)
> **Channel OAS:** `docs/openapi/aibridge-channel-v1.openapi.yaml` · **Gateway OAS:** `docs/openapi/story-intake-actions.openapi.yaml`
> **Traceability:** [`TRACEABILITY-MATRIX.md`](./TRACEABILITY-MATRIX.md) · **Coverage check:** [`MATRIX-COVERAGE-VERIFICATION.md`](./MATRIX-COVERAGE-VERIFICATION.md)
> **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) (harness + sim-data envelope + cluster prompts)
> **Tech arch gaps 36–40:** [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) (qualification gap closure · execute order · named acceptance paths)
> **Context init:** [`CONTEXT-INIT-PROMPT.md`](./CONTEXT-INIT-PROMPT.md) (cold-start dialog + attach checklist; civic node `uus_veerenni_civic` v3)
> **Test qualification SSOT:** [`TEST-QUALIFICATION-20260918-post36-40.md`](./TEST-QUALIFICATION-20260918-post36-40.md) (post Done 36–40) · prior [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md)
> **Generated envelopes (originals):** [`fixtures/`](./fixtures/) — seed batch; **promote = copy** to `tests/fixtures/{cluster}/` on story execute (do not move/delete originals)  
> **DoD — hash_eq integrity-only (QUAL-002 · STORY-40 · 2026-09-18T14:28:02Z):** `*_hash_eq*` / promote SHA256 checks prove package↔tests copy integrity only — **never** sole evidence for matrix Expected behavior (behavioral asserts required separately).  
> **Emitted:** 2026-09-17 · nested tasks named in stories 23–35  
> **Qual gap wave (2026-09-18):** stories **36–40 Scaffolded** (постановка only · no P1 materialize · no pytest/product)  
> **P1.3 note (2026-09-17T13:59:06Z):** story 23 pipeline materialized · EPIC-04 · active `pkg-000020` — next **P2**  
> **P3 note (2026-09-17T14:02:23Z):** STORY-23 Implemented · AUTH contract 15 passed · gate PASS · next **P4**  
> **P6 note (2026-09-17T14:18:28Z):** G-01/G-05 closed · contract 16 passed · next **P7**  
> **P1.3 note (2026-09-17T14:26:09Z):** story 24 pipeline materialized · EPIC-04 reuse · active `pkg-000021` — next **P2**  
> **P3 note (2026-09-17T14:32:38Z):** STORY-24 Implemented · VAL contract 20 passed · gate PASS · next **P4**  
> **P1.3 note (2026-09-17T17:39:14Z):** story 25 pipeline materialized · EPIC-04 reuse · active `pkg-000022` — next **P2**  
> **P3 note (2026-09-17T17:44:23Z):** STORY-25 Implemented · n8n suite 19 passed · gate PASS · next **P4**  
> **P1.3 note (2026-09-17T18:12:10Z):** story 26 pipeline materialized · EPIC-04 reuse · active `pkg-000023` — next **P2**  
> **P3 note (2026-09-17T18:21:34Z):** STORY-26 Implemented · IDEM suite 13 passed · gate PASS · next **P4**  
> **P1.3 note (2026-09-17T18:39:38Z):** story 27 pipeline materialized · EPIC-04 reuse · active `pkg-000024` — next **P2**  
> **P3 note (2026-09-17T18:46:05Z):** STORY-27 Implemented · OAI suite 18 passed · gate PASS · next **P4**  
> **P1.3 note (2026-09-17T19:00:38Z):** story 28 pipeline materialized · EPIC-04 reuse · active `pkg-000025` — next **P2**  
> **P3 note (2026-09-17T19:07:11Z):** STORY-28 Implemented · TOOL unit 17 passed · gate PASS · next **P4**  
> **P5 note (2026-09-17T19:13:12Z):** STORY-28 disposition · G-01/G-02 TASKED (t05/t06) · G-03/04/05 WAIVED · `run_mode=aibridge_28_audit_20260917` — next **P6**  
> **P6 note (2026-09-17T19:15:26Z):** STORY-28 G-01/G-02 CLOSED · TOOL unit 18 passed · next **P7**  
> **P1.3 note (2026-09-17T19:21:48Z):** story 29 pipeline materialized · EPIC-04 reuse · active `pkg-000026` — next **P2**  
> **P3 note (2026-09-17T19:30:03Z):** STORY-29 Implemented · ACT suite 26 passed · gate PASS · next **P4**  
> **P5 note (2026-09-17T19:35:13Z):** G-01/G-02 TASKED (t05/t06) · G-03/04/05 WAIVED · `run_mode=aibridge_29_audit_20260917` · next **P6**  
> **P6 note (2026-09-17T19:38:16Z):** STORY-29 G-01/G-02 CLOSED · ACT suite 29 passed · next **P7**  
> **P1.3 note (2026-09-17T19:45:47Z):** story 30 pipeline materialized · EPIC-04 reuse · active `pkg-000027` — next **P2**  
> **P3 note (2026-09-17T19:51:28Z):** STORY-30 Implemented · GW suite 22 passed · gate PASS · next **P4**  
> **P5 note (2026-09-17T19:56:48Z):** G-01/G-02 TASKED (t05/t06) · G-03…G-06 WAIVED · `run_mode=aibridge_30_audit_20260917` · next **P6**  
> **P6 note (2026-09-17T19:59:20Z):** STORY-30 G-01/G-02 CLOSED · GW suite 23 passed · next **P7**  
> **P1.3 note (2026-09-17T20:05:23Z):** story 31 pipeline materialized · EPIC-04 reuse · active `pkg-000028` — next **P2**  
> **P3 note (2026-09-17T20:12:21Z):** STORY-31 Implemented · LIFE suite 13 passed · gate PASS · next **P4**  
> **P5 note (2026-09-17T20:17:44Z):** G-01/G-02 TASKED (t05/t06) · G-03/04/05 WAIVED · `run_mode=aibridge_31_audit_20260917` · next **P6**  
> **P6 note (2026-09-17T20:19:43Z):** STORY-31 G-01/G-02 CLOSED · LIFE suite 17 passed · next **P7**  
> **P1.3 note (2026-09-17T20:27:34Z):** story 32 pipeline materialized · EPIC-04 reuse · active `pkg-000029` — next **P2**  
> **P3 note (2026-09-17T20:33:31Z):** STORY-32 Implemented · SEC suite 11 passed · gate PASS · next **P4**  
> **P5 note (2026-09-17T20:38:37Z):** G-01/G-02 TASKED (t05/t06) · G-03/04/05 WAIVED · `run_mode=aibridge_32_audit_20260917` — next **P6**  
> **P6 note (2026-09-17T20:42:29Z):** STORY-32 G-01/G-02 CLOSED · SEC suite 12 passed · next **P7**  
> **P1.3 note (2026-09-17T20:50:14Z):** story 33 pipeline materialized · EPIC-04 reuse · active `pkg-000030` — next **P2**  
> **P1.3 note (2026-09-17T21:14:24Z):** story 34 pipeline materialized · EPIC-04 reuse · active `pkg-000033` — P3 Done · next **P4**  
> **P1.3 note (2026-09-17T21:40:06Z):** story 35 pipeline materialized · EPIC-04 reuse · active `pkg-000034` — next **P2**  
> **P3 note (2026-09-17T21:45:30Z):** STORY-35 t01–t04 Done · fixture-index 224 rows · checklist 20 passed · next **P4**  
> **P5 note (2026-09-17T21:51:00Z):** STORY-35 TASKED G-01/G-02/G-03 → t05–t07 scaffold · `run_mode=aibridge_35_audit_20260917` · next **P6**  
> **P1.3 note (2026-09-18T12:27:40Z):** story 36 pipeline materialized · EPIC-04 reuse · active `pkg-000035` — next **P2**  
> **P3 note (2026-09-18T12:32:14Z):** STORY-36 t01–t04 Done · N8N-WF-001 deferred pin · Layer E adapter-contract · out-of-CI checklist · next **P4**  
> **P5 note (2026-09-18T12:40:26Z):** STORY-36 TASKED G-02/G-03/G-04 → t05–t07 scaffold · `run_mode=aibridge_36_audit_20260918` · next **P6**  
> **P6 note (2026-09-18T12:42:35Z):** STORY-36 G-02/G-03/G-04 CLOSED · pin honesty 6 passed · next **P7**  
> **P1.3 note (2026-09-18T12:50:58Z):** story 37 pipeline materialized · EPIC-04 reuse · active `pkg-000036` — next **P2**  
> **P3 note (2026-09-18T14:28:02Z):** STORY-40 Done · QUAL-001/002 covered · QUAL-003 WAIVE · VAL 21 passed · next **P4**  
> **P1.3 note (2026-09-18T14:25:26Z):** story 40 pipeline materialized · EPIC-04 reuse · active `pkg-000039` — next **P2**  
> **P3 note (2026-09-18T14:06:43Z):** STORY-39 Done · CHAR-008 deferred (export absent) · honesty suite · next **P4**  
> **P1.3 note (2026-09-18T14:03:38Z):** story 39 pipeline materialized · EPIC-04 reuse · active `pkg-000038` — next **P2**  
> **P1.3 note (2026-09-18T13:40:25Z):** story 38 pipeline materialized · EPIC-04 reuse · active `pkg-000037` — next **P2**  
> **P3 note (2026-09-18T13:43:00Z):** STORY-38 Done · CHAR-006 Option A · OAI suite 19 passed · next **P4**  
> **P3 note (2026-09-18T12:53:26Z):** STORY-37 t01–t04 Done · Gate-5 evidence **deferred** (no pilot) · checklist G1–G4 · next **P4**  
> **Layer E honesty:** `tests/n8n/` = **adapter-contract** (fixture + Python helpers; not live workflow e2e). Runtime pin / out-of-CI smoke → STORY-36 / N8N-WF-001. N8N-001…018 remain fixture-covered under STORY-25.  
> **Does not modify:** REQ-01/03/05 bodies

## Stories

| Status | Key | Title | Matrix |
|--------|-----|-------|--------|
| Implemented | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | [QA — Authentication and operational boundaries](STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-23-qa-auth-ops-boundaries/STORY-AIBRIDGE-23-qa-auth-ops-boundaries.md) | 12 IDs |
| Implemented | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | [QA — JSON and schema boundary](STORY-AIBRIDGE-24-qa-json-schema-boundary.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-24-qa-json-schema-boundary/STORY-AIBRIDGE-24-qa-json-schema-boundary.md) | 18 IDs |
| Implemented | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | [QA — n8n and Telegram mapping](STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping/STORY-AIBRIDGE-25-qa-n8n-telegram-mapping.md) | 18 IDs |
| Implemented | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | [QA — Idempotency and concurrency](STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-26-qa-idempotency-concurrency/STORY-AIBRIDGE-26-qa-idempotency-concurrency.md) | 10 IDs |
| Implemented | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | [QA — OpenAI and prompt behavior](STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-27-qa-openai-prompt-behavior/STORY-AIBRIDGE-27-qa-openai-prompt-behavior.md) | 16 IDs |
| Implemented | `STORY-AIBRIDGE-28-qa-tool-call-validation` | [QA — Tool-call validation](STORY-AIBRIDGE-28-qa-tool-call-validation.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-28-qa-tool-call-validation/STORY-AIBRIDGE-28-qa-tool-call-validation.md) | 14 IDs |
| Implemented | `STORY-AIBRIDGE-29-qa-action-token-fsm` | [QA — Action token and dual-confirm FSM](STORY-AIBRIDGE-29-qa-action-token-fsm.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-29-qa-action-token-fsm/STORY-AIBRIDGE-29-qa-action-token-fsm.md) | 18 IDs |
| Implemented | `STORY-AIBRIDGE-30-qa-gateway-continuation` | [QA — Gateway and SPA continuation](STORY-AIBRIDGE-30-qa-gateway-continuation.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-30-qa-gateway-continuation/STORY-AIBRIDGE-30-qa-gateway-continuation.md) | 20 IDs |
| Implemented | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | [QA — Restart, lifecycle, and retention](STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention/STORY-AIBRIDGE-31-qa-restart-lifecycle-retention.md) | 12 IDs |
| Implemented | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | [QA — Privacy, logs, and observability](STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-32-qa-privacy-logs-observability/STORY-AIBRIDGE-32-qa-privacy-logs-observability.md) | 10 IDs |
| Scaffolded | `STORY-AIBRIDGE-33-qa-readiness-configuration` | [QA — Readiness and configuration](STORY-AIBRIDGE-33-qa-readiness-configuration.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-33-qa-readiness-configuration/STORY-AIBRIDGE-33-qa-readiness-configuration.md) | 15 IDs |
| Implemented | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | [QA — Product-journey scenarios (UC-01…10)](STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-34-qa-product-journey-scenarios/STORY-AIBRIDGE-34-qa-product-journey-scenarios.md) | 10 IDs |
| Done (P3 · next P4) | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | [QA — Test layers, gates, fixtures, characterization DoD](STORY-AIBRIDGE-35-qa-gates-layers-dod.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-35-qa-gates-layers-dod/STORY-AIBRIDGE-35-qa-gates-layers-dod.md) | 13 IDs |
| Done (P3 · next P4) | `STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty` | [QA — n8n workflow pin + Layer E honesty](STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty/STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty.md) | N8N-WF-001 (+ N8N honesty) |
| Done (P3 · next P4) | `STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence` | [QA — Gate-5 live pilot evidence pack](STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence/STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md) | Gate-5 |
| Done (P3 · next P4) | `STORY-AIBRIDGE-38-qa-oai-channel-error-outcome` | [QA — OAI 429/5xx channel outcome](STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome/STORY-AIBRIDGE-38-qa-oai-channel-error-outcome.md) | CHAR-006 · OAI-008/009 |
| Done (P3 · next P4) | `STORY-AIBRIDGE-39-qa-char008-send-edit-capture` | [QA — CHAR-008 Send/Edit + dedupe capture](STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-39-qa-char008-send-edit-capture/STORY-AIBRIDGE-39-qa-char008-send-edit-capture.md) | CHAR-008 |
| Done (P3 · next P4 · pkg-000039) | `STORY-AIBRIDGE-40-qa-suite-assert-hygiene` | [QA — Suite assert hygiene](STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) · [pipeline](../../epics/EPIC-AIBRIDGE-04-qa-inbound-outbound/stories/STORY-AIBRIDGE-40-qa-suite-assert-hygiene/STORY-AIBRIDGE-40-qa-suite-assert-hygiene.md) | QUAL-001…003 |

## Build order (automation)

`23 → 24 → 25 ∥ 26 → 27 → 28 → 29 → 30 → 31 ∥ 32 → 33 → 34 → 35 → 36 → 37 → 38 → 39 → 40`

## Fixture promote map (seed batch → tests/fixtures)

| Package `fixtures/` file | Target after promote | Stories |
|--------------------------|----------------------|---------|
| `message-private-ru-pothole.json` | `tests/fixtures/telegram/message-private-ru-pothole.json` | 25 |
| `text-only-ru-clarify.json` | `tests/fixtures/openai/text-only-ru-clarify.json` | 27 |
| `stashed-201.json` | `tests/fixtures/gateway/stashed-201.json` | 30 |
| `turns-valid-private.json` | `tests/fixtures/channel/turns-valid-private.json` | 23, 24 |
| `ready-missing-channel-bearer.json` | `tests/fixtures/settings/ready-missing-channel-bearer.json` | 33 |
| `callback-ack-before-actions.json` | `tests/fixtures/n8n/callback-ack-before-actions.json` | 25 |
| `idem-same-event-once-openai.json` | `tests/fixtures/spies/idem-same-event-once-openai.json` | 26 |
| `fixture-index.json` | `tests/fixtures/meta/fixture-index.json` | 35 |
| `meta/n8n-wf-001-pin-pointer.json` | `tests/fixtures/meta/n8n-wf-001-pin-pointer.json` | 36 |
| `meta/gate5-evidence-index.json` | `tests/fixtures/meta/gate5-evidence-index.json` | 37 |
| `n8n/char-008-send-edit-capture.json` | `tests/fixtures/n8n/char-008-send-edit-capture.json` | 39 |

**Verified:** clusters promoted per story execute waves; STORY-36 pin deferred; STORY-37 Gate-5 evidence deferred (no pilot); STORY-39 CHAR-008 capture deferred (export absent).

## Out of package

- Materializing `task-*` / epic folders before explicit P1 (incl. stories 36–40)
- Implementing pytest suites before story execute waves
- REQ-06 / ADMIN / mockups
