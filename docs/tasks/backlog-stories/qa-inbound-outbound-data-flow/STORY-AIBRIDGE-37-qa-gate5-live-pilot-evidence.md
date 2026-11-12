# STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence — QA — Gate-5 live pilot evidence pack

## Meta
- **Key:** `STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence`
- **Status:** Done (P3 · pkg-000036 · next P4 · 2026-09-18T12:53:26Z)
- **Tech arch:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md)
- **Tech arch gaps:** [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§37**
- **Seed originals:** [`fixtures/`](./fixtures/) → promote **copies** when execute creates them
- **Package:** [`qa-inbound-outbound-data-flow/INDEX.md`](INDEX.md)
- **Parent SSOT:** [`AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)
- **Guide refs:** §9 Layer F · §15 Gate-5
- **Qualification:** [`TEST-QUALIFICATION-20260918.md`](./TEST-QUALIFICATION-20260918.md) — closes **P0-Q2**, **P0-Q3**, **P2-Q3**
- **Traceability:** [`TRACEABILITY-MATRIX.md`](TRACEABILITY-MATRIX.md)
- **Emitted:** 2026-09-18 · from test qualification gap closure (operator package ask)

## Scope
Task statements for **Gate-5 live channel** evidence: dedicated TG test bot/chat → n8n → private aibridge (dry-run first) → optional authorized staging stash with SPA continuation — **out of default CI**. Clarify UC-01…10 (STORY-34) are PG-backed product journeys, not Gate-5.

## Вне scope
- Materializing `task-*` / epic folders before explicit P1.
- Implementing live automation in default CI / inventing Railway SUCCESS.
- Closing N8N-WF-001 (STORY-36) or CHAR-008 (STORY-39) in this story alone.
- Destructive or production Story submissions.

## Context

P0-Q2: UC harness documents «no live Telegram/Railway»; Recording OAI/GW; green UC ≠ Gate-5.  
P0-Q3: `test_gate5_live_deferred_out_of_default_ci` passes when defer is recorded — not when live works.  
P2-Q3: UC mock-heavy vs pilot — acceptable for CI; Gate-5 remains live.

## Use cases / matrix IDs

| ID | Scenario | Expected |
|----|----------|----------|
| **Gate-5** | live channel (guide §15) | Real Telegram → n8n → private aibridge → response in dry-run; callback acknowledged immediately; one staging stash returns SPA continuation URL; resident-facing text never claims draft published. Evidence pack attached; status leaves `deferred_live` only when pack accepted |
| UC-01…10 | Product journeys | Stay **PG-journey covered** under STORY-34; TRACEABILITY note: **not** Gate-5 |

## Fixture convention (tech-arch §6 · ADR-Q1/Q2)

- Evidence artifacts (checklists, redacted logs, screenshots paths) live under package docs/fixtures **only when execute wave creates them** — this Scaffolded story does not invent bodies.
- `task-*` folders **named only** until P1.

## Nested tasks (named — not materialized)

> Arch: [`TECHNICAL-ARCHITECTURE-GAPS-36-40.md`](./TECHNICAL-ARCHITECTURE-GAPS-36-40.md) **§37**.  
> **Layer:** F_live · **Harness:** operator pilot checklist; secrets redacted; disabled by default  
> `task-*` folders **named only** until P1.

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-37-t01-uc-vs-gate5-docs` | Done | Cross-link STORY-34/37 + ops README: UC-01…10 = PG-journey only; Gate-5 owner = this story; reinforce TRACEABILITY notes |
| **T02** | `task-aibridge-37-t02-pilot-checklist` | Done | Map guide §15 Gate-5 bullets onto [`r3-p1-09-live-gate-checklist.md`](../../../ops/n8n-channel-workflow/r3-p1-09-live-gate-checklist.md) (dry-run first → staging stash; ack before `/actions`; no claim_published) |
| **T03** | `task-aibridge-37-t03-evidence-pack` | Done | Collect redacted pilot evidence; index paths in package `fixtures/meta/gate5-evidence-index.json` and/or ops `live-evidence-*.md` (bodies only on execute — name ≠ create now) |
| **T04** | `task-aibridge-37-t04-story-gate` | Done | Flip Gate-5 / fixture-index off `deferred_live` **only** with accepted pack; default CI keeps no live TG; decide meta assert `deferred_live\|pass_with_evidence` per §37 |
| **T05** | `task-aibridge-37-t05-audit-g02-qual-closed-with-defer` | Done | P5/P6 audit G-02: QUAL closed-with-defer |
| **T06** | `task-aibridge-37-t06-audit-g03-checklist-g3-assert` | Done | P5/P6 audit G-03: suite assert checklist G3 |
| **T07** | `task-aibridge-37-t07-audit-g04-honesty-count-docs` | Done | P5/P6 audit G-04: honesty count docs 5→4 |

## Acceptance criteria

- [x] Gate-5 row in TRACEABILITY owned by this story key.
- [x] UC-01…10 explicitly not claimed as Gate-5.
- [x] Pilot checklist covers guide §15 Gate-5 bullets.
- [x] Default CI remains without live TG/Railway invent.
- [x] Nested tasks named only; no `task-*` folders until P1.
- [x] P0-Q2 / P0-Q3 / P2-Q3 closed or remaining defer explicit in evidence pack.
