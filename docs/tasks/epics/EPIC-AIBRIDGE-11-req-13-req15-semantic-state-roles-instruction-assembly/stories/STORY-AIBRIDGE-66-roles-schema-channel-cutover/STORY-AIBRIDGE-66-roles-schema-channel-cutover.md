# STORY-AIBRIDGE-66 — Roles-schema channel cutover (+ local consume)

## Meta
- **Key:** `STORY-AIBRIDGE-66-roles-schema-channel-cutover`
- **Status:** ✅ **Done · Product Done** · G-01 **CLOSED** · G-02 **WAIVE** · pkg-000069 · P8 `36b45bd`/`4c6d327`/`a678b32` · residual **STORY-67** · 2026-11-04T14:31:36Z
- **Parent Epic:** [`EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md`](../../EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md)
- **source:** `backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md`
- **decision_ref:** [`STORY-AIBRIDGE-66-….md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md) · [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) §3b · gap V3 (+ V8-light)
- **Package:** [`req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000069-20261104-epic-aibridge-11-story-66-roles-schema-channel-cutover.yaml`
- **P1 materialize:** 2026-11-04T13:44:52Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_66_scaffold_20261104T134107Z.plan.md)
- **Depends:** hard STORY-65 Present (Done · Product Done · G-02 Lifted)
- **OOS:** Railway volume STORY-67 · GPT-48 authoring / invent instruction bodies · telegram · gateway/spa redesign · invent new channel HTTP · invent hash SSOT

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Roles-schema §3b | [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) §3b |
| Roles / assembly | [`02-roles-coordinator-assembly.md`](../../../../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md) · runtime [`10`](../../../../runtime-docs/10-roles-coordinator-assembly.md) |
| Channel wire (65) | runtime [`12`](../../../../runtime-docs/12-asgi-channel-semantic-roles-wire.md) |
| Peer export | `GPT UI/instructions-roles/` · GPT UI REQ-48 |
| Soft peers | STORY-65 Done · residual 67 |

## Scope
- Point channel/ready content consume at **roles-schema** manifest (`bundle_version` / `core` / `roles.*`) — not Phase-A `files[]` as live SSOT.
- Local MVP: configure `DOGESTONIA_INSTRUCTIONS_DIR` / `_MANIFEST` to GPT UI `instructions-roles/` (or equivalent mount) and prove consume against export inventory (light parity).
- Retire dual-schema ambiguity on the **channel** path (wire residual closed for product turns).

## Вне scope
- Railway volume Product Done / AC-14 full (STORY-67).
- Authoring new instruction bodies (GPT-48).
- Telegram delivery / gateway contracts.

## Verified current state
- Export Present: `GPT UI/instructions-roles/roles.manifest.json` + role files.
- Channel wire Present (STORY-65) + cutover Present (STORY-66): roles-schema via `DOGESTONIA_ROLES_*` or INSTRUCTIONS_* unify; ADR-1 mega = legacy/dev when cutover active.
- `content.py` accepts roles-schema live; Phase-A `files[]` = legacy/dev-only (runtime [`13`](../../../../runtime-docs/13-roles-schema-channel-cutover.md)).
- Fixture consume: `tests/fixtures/content/roles.manifest.json`.

## Target / AC
- [x] Channel/ready uses roles-schema per REQ-13 §3b.
- [x] Local consume Pass vs GPT-48 export inventory (MVP light — not Railway volume).
- [x] Phase-A `files[]` documented as legacy/dev-only after cutover.
- [x] Depends on STORY-65 wire Present (ordered 65→66).

## Nested tasks (pkg-000069)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-66-t01-instructions-env-roles-schema-cutover](./task-aibridge-66-t01-instructions-env-roles-schema-cutover/README.md) | Scope-1 · AC-1 · §3b env | Done |
| t02 | [task-aibridge-66-t02-content-ready-roles-schema-loader](./task-aibridge-66-t02-content-ready-roles-schema-loader/README.md) | Scope-1 · AC-1 · readiness | Done |
| t03 | [task-aibridge-66-t03-channel-wire-assemble-default-cutover](./task-aibridge-66-t03-channel-wire-assemble-default-cutover/README.md) | Scope-1 · AC-1 · wire | Done |
| t04 | [task-aibridge-66-t04-local-gpt48-export-consume-light](./task-aibridge-66-t04-local-gpt48-export-consume-light/README.md) | Scope-2 · AC-2 · V8-light | Done |
| t05 | [task-aibridge-66-t05-phase-a-files-legacy-dev-docs](./task-aibridge-66-t05-phase-a-files-legacy-dev-docs/README.md) | Scope-3 · AC-3 | Done |
| t08 | [task-aibridge-66-t08-story-gate-checklist](./task-aibridge-66-t08-story-gate-checklist/README.md) | package gate | PASS |
| t09 | [task-aibridge-66-t09-audit-g01-runtime-readme-index-13](./task-aibridge-66-t09-audit-g01-runtime-readme-index-13/README.md) | P5 G-01 | Done |

## Code points
- `src/aibridge/content.py` · `deployment.py` · `readiness.py` · `config.py`
- `src/aibridge/channel_wire.py` · `app.py` (wire bind / ADR-1)
- `src/aibridge/roles/assembly.py`
- Peer: `GPT UI/instructions-roles/` · Keep dual-confirm
