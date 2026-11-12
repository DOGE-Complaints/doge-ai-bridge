# STORY-AIBRIDGE-42 — Canonical uniqueItems validation (Gate 2)

## Meta
- **Key:** `STORY-AIBRIDGE-42-canonical-uniqueitems-validation`
- **Status:** P6 Done · G-01/G-02 CLOSED · next P7 · pkg-000041 · 2026-09-24T11:25:01Z
- **Parent REQ:** [`REQ-07`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) AIB-COMPAT-04/05 · §8.2 · §9.1 · T-UNIQUE-*
- **Tech-arch:** [`TECH-ARCH-REQ-07`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.3 · §2.5
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [41](STORY-AIBRIDGE-41-openai-schema-projection.md) · [43](STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [44](STORY-AIBRIDGE-44-compat-merge-gate-proof.md) · [45](STORY-AIBRIDGE-45-compat-live-telegram-verify.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-09-24T10:28:49Z

## Scope
- Enforce JSON Schema `uniqueItems: true` in the canonical validator used by Gate 2 (structural equality; object key order independent).
- Extend `schema_validation_complete()` so readiness **proves** uniqueness enforcement (not frozenset membership alone).
- Gate 2 always validates against untouched canonical pack schema.

## Out of scope
- OpenAI projection (41); `create_app` ValidationContext bind (43); trusting the model prompt alone for duplicates.

## Verified current state
- P3 2026-09-24T11:17:36Z: `uniqueItems` in `FULL_SCHEMA_KEYWORDS`; Gate 2 enforces structural uniqueness (`request_assembly.py`); `schema_validation_complete()` proves uniqueItems; pack on disk retains keyword; tests T-UNIQUE-01…09 (16 passed with request_assembly).

## Target / AC
- [x] AC-04: duplicate house ids under one street rejected at **unit Gate 2** (`validate_gate2_pack_payload`). Evidence = Gate 2 contract only — **not** invent freeze / Send / gateway write proof in this story.
- [x] T-UNIQUE-01…09 behaviors covered by tests (incl. active Uus Veerenni pack path).
- [x] Incomplete uniqueness capability → readiness fail-closed (align AIB-COMPAT-07 / `schema_validation_incomplete*` family).

> **Footnote (G-01 / P6):** end-to-end FC path (freeze / Send / gateway) requires `ValidationContext` bind — owned by [STORY-AIBRIDGE-43](STORY-AIBRIDGE-43-validation-context-bind-readyz.md). Do not invent `app.py` VC bind here.

## Code points
- `src/aibridge/request_assembly.py` — `validate_gate2_pack_payload`, `run_three_gates`, `schema_validation_complete`
- `src/aibridge/readiness.py` — uses `schema_validation_complete`

## Dependencies
- None (parallel with 41); required by 43 / 44
