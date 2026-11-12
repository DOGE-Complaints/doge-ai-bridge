# STORY-AIBRIDGE-66 — Roles-schema channel cutover (+ local consume)

## Meta
- **Key:** `STORY-AIBRIDGE-66-roles-schema-channel-cutover`
- **Status:** **Done** · **Product Done** · pkg-000069 · P8 `36b45bd`/`4c6d327`/`a678b32` · G-01 CLOSED · G-02 WAIVE→67 · 2026-11-04 · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-66-roles-schema-channel-cutover/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-66-roles-schema-channel-cutover-20261104.md) · [wave](../../run-reports/operator-waves/wave-20261104-req13-wire-65-66.md)
- **Parent REQ:** [`REQ-13`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) §3b
- **Peer export:** [`GPT UI REQ-48`](<../../../../../GPT UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md>) · `instructions-roles/`
- **Package:** [`INDEX.md`](INDEX.md)
- **Gap:** V3 (+ local V8 light) — closed for channel; Railway volume → [67](STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)
- **Siblings:** [65](STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) · [67](STORY-AIBRIDGE-67-consume-parity-volume-evidence.md)
- **Skill declared:** `python-pro`
- **Emitted:** 2026-11-03
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Point channel/ready content consume at **roles-schema** manifest (`bundle_version` / `core` / `roles.*`) — not Phase-A `files[]` as live SSOT.
- Local MVP: configure `DOGESTONIA_INSTRUCTIONS_DIR` / `_MANIFEST` to GPT UI `instructions-roles/` (or equivalent mount) and prove consume against export inventory (light parity).
- Retire dual-schema ambiguity on the **channel** path (wire residual closed for product turns).

## Out of scope
- Railway volume Product Done / AC-14 full (STORY-67).
- Authoring new instruction bodies (GPT-48).
- Telegram delivery / gateway contracts.

## Verified current state
- Export Present: `GPT UI/instructions-roles/roles.manifest.json` + role files.
- Channel wire Present (STORY-65) + cutover Present: roles-schema via `DOGESTONIA_ROLES_*` or `INSTRUCTIONS_*` unify when manifest is roles-schema; ADR-1 mega = legacy/dev when cutover active.
- `content.py` accepts roles-schema live; Phase-A `files[]` = legacy/dev-only (runtime [`13`](../../../runtime-docs/13-roles-schema-channel-cutover.md)).
- Fixture consume: `tests/fixtures/content/roles.manifest.json`.

## Target / AC
- [x] Channel/ready uses roles-schema per REQ-13 §3b.
- [x] Local consume Pass vs GPT-48 export inventory (MVP light — not Railway volume).
- [x] Phase-A `files[]` documented as legacy/dev-only after cutover.
- [x] Depends on STORY-65 wire Present (ordered 65→66).

## Dependencies
- Hard: STORY-65 (**Done**).
- Soft: GPT-48 export artifacts Present.
