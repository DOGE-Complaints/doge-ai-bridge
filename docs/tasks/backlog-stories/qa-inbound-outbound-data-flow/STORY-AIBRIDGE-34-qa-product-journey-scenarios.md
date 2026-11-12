# STORY-AIBRIDGE-34-qa-product-journey-scenarios — QA — Product-journey scenarios (UC-01…10)

## Meta
- **Key:** `STORY-AIBRIDGE-34-qa-product-journey-scenarios`
- **Status:** Done (P3 · pkg-000033 · next P4)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** to `tests/fixtures/{cluster}/`
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §11 Product-journey scenarios
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-17 · from QA data-flow guide (operator package ask)

## Scope
Automated **test/QA acceptance statements** covering the matrix IDs listed below. Preserve ownership table from guide §1 (Telegram / n8n thin adapter / aibridge / OpenAI / gateway / SPA / PostgreSQL).

## Вне scope
- Materializing `task-*` / epic folders before explicit P1 (this story only **names** tasks).
- Deleting or moving package [`fixtures/`](./fixtures/) originals (promote = **copy** only).
- Moving product logic into n8n; inventing channel OAS paths; Railway SUCCESS invent; live Telegram in default CI.
- Claiming UC-01…10 greens as **Gate-5** live channel proof (owned by [`STORY-AIBRIDGE-37`](./STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md)).

## Context

End-to-end resident journeys combining turns, actions, dry-run/live stash, cancel, ownership attack, retry storm, ambiguous timeout, geo mismatch, unsupported media, multilingual. Assertions include session/revision/token/gateway invariants from the guide.

## Use cases / matrix IDs (must transfer from guide)

### UC-01 — Normal interview, dry-run

1. Resident sends a civic observation.
2. n8n sends `/turns` with Telegram update ID.
3. aibridge/OpenAI asks a clarification and returns `Looks right`, `Edit`, `Cancel`.
4. Resident chooses `Edit`; previous buttons become invalid.
5. Resident provides corrected information.
6. Resident chooses `Looks right`.
7. Model produces one valid `postStoryDraftStash` function call.
8. aibridge returns `Send to DOGEstonia`, `Edit`, `Cancel`.
9. Resident sends.
10. With dry-run enabled, response is `dry_run_ok`; no gateway request; message explicitly says nothing was sent.

Assertions: stable session, revision change after Edit, no duplicate OpenAI calls on retry, zero gateway posts, all old tokens invalid.

### UC-02 — Normal live stash

Same as UC-01 with dry-run disabled and a staging gateway returning valid 201.

Assertions: one gateway post, `outcome=stashed`, `draft_id`, continuation URL, state `stashed`, and resident wording says “draft stashed/not published.”

### UC-03 — Resident cancels at first confirmation

Assertions: `cancelled`, no function call required, no gateway, pending actions invalid. A following new resident message must be covered by LIFE-009.

### UC-04 — Resident cancels immediately before Send

Assertions: frozen draft is not posted, all send tokens invalid, no continuation URL.

### UC-05 — Group chat ownership attack

User A starts a story and receives buttons in a group. User B sends the visible callback token.

Assertions: 403 `forbidden`; A’s token remains governed by intended consume semantics; no gateway; no cross-user state exposure.

### UC-06 — Telegram retry storm

n8n retries the same update 5–20 times with the same `event_id` after a network timeout.

Assertions: one OpenAI call or one gateway attempt, deterministic replayed response, no duplicate Telegram buttons created by aibridge. Adapter-level duplicate outgoing Telegram messages may require n8n-specific delivery dedupe and should be measured separately.

### UC-07 — Ambiguous gateway timeout

The gateway receives or may receive the request, but aibridge times out before a response.

Assertions: `unknown_outcome`; revision blocked from re-Send; restart preserves ambiguity; operator runbook required; no automatic retry.

### UC-08 — Geo scope mismatch

Gateway returns 422.

Assertions: `geo_scope_mismatch`, no draft/URL, resident-safe message, state does not claim success. Product UX for correcting location should be tested as a follow-up/edit journey.

### UC-09 — Unsupported Telegram content

Resident sends voice, sticker, photo, or document without text.

Assertions: n8n does not fabricate empty text or send an invalid request. Current v1 façade is text-only; adapter returns a clear supported-input prompt or routes to a future transcription/attachment flow.

### UC-10 — Multilingual story

Resident begins in Russian, adds an Estonian place name, then switches to English.

Assertions: raw user messages preserved; session language policy comes from instructions/model logic, not blindly from Telegram `language_code`; final gateway body validates required `{et,ru,en}` fields.

---

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- **Originals (SSOT for generated envelopes):** [`fixtures/`](./fixtures/) — do **not** delete/move after promote.
- **Runtime test tree (after story execution):** `tests/fixtures/{cluster}/{name}.json` — **copy** from package `fixtures/` (or generate into package `fixtures/` first, then copy).
- Envelope: `schema_version=1.0` fields per [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6.2.
- `task-*` folders below are **named only** — not materialized until explicit P1 (analysis.mdc: name ≠ create).

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §4–§6 · §5.1 layers.  
> **Seed fixtures (package):** compose from prior cluster seeds; generate UC journey packs as needed  
> **Clusters:** all primary + `n8n` · **Layer:** E2E via `tests/integration/` + `story13_e2e_helpers` · **Harness:** E2EHarness: disposable PG + Recording OpenAI + Recording Gateway · **not Gate-5** (no live Telegram/Railway) — live pilot ownership → [`STORY-AIBRIDGE-37`](./STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence.md)  

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-34-t01-compose-uc-fixture-packs` | Done | Ensure UC-01…10 packs reference promoted fixtures; generate missing into package `fixtures/` |
| **T02** | `task-aibridge-34-t02-promote-uc-fixtures` | Done | Copy any new UC envelopes to `tests/fixtures/**`; originals stay |
| **T03** | `task-aibridge-34-t03-implement-journey-e2e` | Done | Parameterized E2E per UC using E2EHarness; barriers not sleep |
| **T04** | `task-aibridge-34-t04-story-gate` | Done | All UC-01…10; no live network; originals intact |

## Acceptance criteria

- [x] Every matrix ID in Scope appears in TRACEABILITY-MATRIX with this story key.
- [x] Characterization IDs (if any) are marked characterization — not silent product invent.
- [x] Guide **must** → automated asserts; **characterization** → capture-first.
- [x] Nested tasks named in this story; `task-*` folders **not** created until P1.
- [x] On story Done: all required envelopes exist under `tests/fixtures/{cluster}/` as **copies**; originals remain in package [`fixtures/`](./fixtures/).
