# STORY-AIBRIDGE-35-qa-gates-layers-dod — QA — Test layers, gates, fixtures, characterization DoD

## Meta
- **Key:** `STORY-AIBRIDGE-35-qa-gates-layers-dod`
- **Status:** Todo (statement only — no implementation in this wave)
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §9 Layers A–F · §12–14 fixtures/spies · §15 Gates · §16 CHAR · §18 DoD
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Implementing tests, fixtures, or code changes in this story wave.
- Nested pipeline tasks / epic folders (name ≠ create until explicit P1).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent.

## Context

Program-level statement: which automation layers exist (unit→live smoke), pass/fail gates 1–5, required fakes/spies, and characterization items that must not be silently guessed. Does not implement suites — only binds acceptance program to stories 23–34.

## Use cases / matrix IDs (must transfer from guide)

### Test layers (guide §9)

### Layer A — pure unit tests

No network or real database. Cover parsing, state transitions, token verification, three validation gates, gateway status mapping, response parsing, redaction, and URL generation.

### Layer B — application contract tests

Run FastAPI/ASGI in-process with fake OpenAI and gateway transports. Cover HTTP status, exact envelopes, middleware ordering, body limits, authentication, rate limiting, and dedupe.

### Layer C — PostgreSQL integration tests

Run migrations against disposable PostgreSQL. Cover durable dedupe, session/history/token persistence, locks, gateway attempt uniqueness, restart recovery, TTL cleanup, and migration readiness.

### Layer D — container/deployment tests

Build the real image with a pinned content bundle. Verify start command, `$PORT`, `/healthz`, `/readyz`, `/metrics`, environment fail-closed rules, and no accidental public dependencies.

### Layer E — n8n contract tests

Use recorded Telegram updates and a test aibridge. Verify field expressions, fixed event IDs across retries, immediate callback acknowledgement, headers, routing, and response-to-keyboard mapping.

### Layer F — live pilot smoke

Use a dedicated Telegram test bot/chat and non-production test user. First run with `AIBRIDGE_DRY_RUN=true`; then separately run an authorized staging gateway stash. Do not make destructive or production Story submissions.

---

### Pass/fail gates (guide §15)

### Gate 1 — channel contract

- all AUTH, VAL, and core N8N mapping tests pass;
- generated responses conform to `aibridge-channel-v1.openapi.yaml`;
- no secret appears in body/log/metrics.

### Gate 2 — interview safety

- `store=false` and one prompt channel proven;
- dedupe/concurrency tests prove one OpenAI call per event;
- no tool call can bypass interpretation confirmation or three validation gates.

### Gate 3 — consequential-action safety

- token ownership/TTL/revision/state/deployment/hash tests pass;
- only Send confirmation reaches gateway;
- one gateway attempt per revision;
- unknown outcome never auto-retries.

### Gate 4 — durable runtime

- migrations applied and `/readyz` passes;
- restart tests preserve state, dedupe, token status, history, and gateway attempts;
- retention and bundle pinning behavior verified.

### Gate 5 — live channel

- real Telegram → n8n → private aibridge → response works in dry-run;
- callback is acknowledged immediately;
- one staging stash returns an SPA continuation URL;
- resident-facing text never claims the draft is published.

---

### Characterization (guide §16) — CHAR-*

- **CHAR-001:** What starts a fresh story after `cancelled`?
- **CHAR-002:** What starts a fresh story after `stashed`?
- **CHAR-003:** Should whitespace-only messages be rejected after trimming?
- **CHAR-004:** Should Telegram media captions enter the text-only façade?
- **CHAR-005:** How should n8n notify a resident when aibridge is unavailable after callback acknowledgement?
- **CHAR-006:** Should OpenAI 429/5xx remain a channel 500, or later gain a distinct retryable channel outcome?
- **CHAR-007:** Should unusual known gateway statuses such as 409 be a specific outcome rather than `unknown_outcome`?
- **CHAR-008:** Does the n8n workflow use Send Message or Edit Message for each response state, and how does it prevent duplicate outbound Telegram messages after its own retry?

### Gate IDs

- **Gate-1:** channel contract — See guide §15 pass criteria
- **Gate-2:** interview safety — See guide §15 pass criteria
- **Gate-3:** consequential-action safety — See guide §15 pass criteria
- **Gate-4:** durable runtime — See guide §15 pass criteria
- **Gate-5:** live channel — See guide §15 pass criteria

### Definition of done (guide §18)

for the IDE testing task

The QA automation is complete when:

- every matrix row is implemented, explicitly deferred with a reason, or converted into a named characterization test;
- tests use current OpenAPI files as contract sources;
- the test suite proves idempotency by side-effect counts, not only response equality;
- tests exercise real PostgreSQL migrations and restart recovery;
- OpenAI and gateway negative cases are deterministic through injected transports;
- live tests are isolated, secret-safe, and disabled by default unless explicit environment flags are set;
- CI artifacts contain no resident PII, raw Bearers, raw action tokens, or production drafts;
- the final report separates code failures, environment failures, n8n mapping failures, and unresolved product decisions.
## Acceptance criteria (statement)

- [ ] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [ ] Characterization IDs (if any) are marked characterization — not silent product invent.
- [ ] No nested implementation tasks created by this wave.
- [ ] Future automation must treat guide **must** as automated asserts; **characterization** as capture-first.
