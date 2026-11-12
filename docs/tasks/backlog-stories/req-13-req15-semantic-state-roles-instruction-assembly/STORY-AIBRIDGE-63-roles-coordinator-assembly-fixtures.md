# STORY-AIBRIDGE-63 — Roles, coordinator, assembly (in-repo fixtures)

## Meta
- **Key:** `STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures`
- **Status:** **Done** · **Product Done** · pkg-000066 · P8 SHAs `1efea66`/`893cd39`/`9eb32f0` · G-02 WAIVED ASGI · next **STORY-64** · 2026-11-02T10:21:23Z · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) · [runtime 10](../../../runtime-docs/10-roles-coordinator-assembly.md) · [p7 reaudit](../../../analysis/p7-reaudit-STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures-20261102.md)
- **Parent REQ:** [`REQ-13`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) §§2,4.2–3,5 AC-02/03/07/08 · L13-1 · arch D3/D5
- **Tech-arch:** [`req15-semantic-state-roles/02-roles-coordinator-assembly.md`](../../../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [62](STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [64](STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-02T08:32:08Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Five v1 roles callable via coordinator; version pins; policy table → one next role (no LLM-router).
- Assembly: shared core + per-role slice + session pin from configured dir+manifest.
- **Isolation:** stub harness uses **in-repo fixtures** (extend `tests/fixtures/content/` or sibling tree — path at implement); **must not** require GPT UI checkout.
- Model calls via REQ-12 interview port Keep.
- L13-1: understanding soft OK; send never auto from ordinary reply (Adapt `coordinator.py` offer path).
- AC-07: fixture role texts must not encode gateway stash/SPA redirect procedure.

## Out of scope
- Semantic store DDL body (62); live volume/GPT-48 export bodies (64/peer); provider HTTP; telegram.

## Verified current state
- Role registry: **Present** (`src/aibridge/roles/`) · P3 2026-11-02T09:16:58Z.
- `coordinator.py` — `select_next_role` + FC-less → interpret offer (L13-1); send only after FC.
- Assembly Present: `roles/assembly.py` · fixtures `tests/fixtures/content/roles-instructions/` + `roles.manifest.json`.
- `interview_providers/` Keep · `roles/invoke.bind_role_interview_engine`.

## Target / AC
- [x] AC-AIB-13-02: five roles + pins via coordinator (harness).
- [x] AC-AIB-13-03: assemble only from configured dir+manifest (fixture env).
- [x] AC-AIB-13-07: role instruction fixtures do not own gateway/SPA procedure.
- [x] AC-AIB-13-08 / L13-1: ordinary reply ≠ send-permission offer.
- [x] Stub isolation: suite green without GPT UI tree.

## Code points
- `coordinator.py` · `content.py` · `interview.py` · `app.py` content wire · `interview_providers/`
- Fixture tree under `tests/fixtures/…` (implement choice)

## Dependencies
- Soft: 62 (state flags for policy) · REQ-12 port Present
