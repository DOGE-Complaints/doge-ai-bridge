# STORY-AIBRIDGE-65 — ASGI channel: semantic state + roles wire

## Meta
- **Key:** `STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire`
- **Status:** ✅ **Done · Product Done** · pkg-000068 · gate **PASS** · G-02 **Lifted** · P8 `0ccedc6`/`15fc620`/`fde569a` · next **STORY-66** · 2026-11-04T13:38:12Z
- **Parent Epic:** [`EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md`](../../EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md)
- **source:** `backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md`
- **decision_ref:** [`STORY-AIBRIDGE-65-….md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) · [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) · gap V2
- **Package:** [`req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000068-20261104-epic-aibridge-11-story-65-asgi-channel-semantic-roles-wire.yaml`
- **P1 materialize:** 2026-11-04T13:06:36Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_65_scaffold_20261104T130109Z.plan.md)
- **Depends:** hard STORY-62 / 63 Present modules · soft STORY-66 before full quality smoke
- **OOS:** GPT-48 authoring · STORY-66 cutover details · STORY-67 Railway · telegram · gateway/spa redesign · invent new channel HTTP

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Semantic store / Target A | [`01-semantic-state-store-invalidation.md`](../../../../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md) · runtime [`09`](../../../../runtime-docs/09-semantic-state-store-invalidation.md) |
| Roles / assembly | [`02-roles-coordinator-assembly.md`](../../../../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md) · runtime [`10`](../../../../runtime-docs/10-roles-coordinator-assembly.md) |
| Gap V2 / G-02 | [`req15-target-state-code-gap-audit-2026-11-03.md`](../../../../../../docs/analysis/req15-target-state-code-gap-audit-2026-11-03.md) |
| Soft peers | STORY-62 · 63 · 64 Done · residual 66 · 67 |

## Scope
- Lift REQ-13 **G-02**: bind Present `SemanticStateService`, `select_next_role`, `assemble_role_prompt` into **channel** `/v1/channel/turns` (and related action path as needed) so product path ≠ harness-only.
- Preserve REQ-11 dual-confirm / gateway pipe; do not invent new channel HTTP surface.
- Meaning-change → send invalidation (L13-3 Target A) on channel when semantic writes occur.

## Вне scope
- GPT UI instruction authoring (REQ-48).
- Telegram transport; gateway/spa redesign.
- Full Railway volume Pass (STORY-67).
- Roles-schema env cutover details beyond wire readiness (STORY-66).

## Verified current state
- Modules Present: `semantic_state/`, `roles/` (assembly/policy/registry); stories 62–64 Product Done (harness).
- Channel ASGI wire **Present** (STORY-65): `channel_wire.apply_before_engine_turn` on `/v1/channel/turns` · `SemanticStateService` + `select_next_role` (+ `assemble_role_prompt` when roles env set). G-02 **Lifted** (REQ-13 Status · runtime [`12`](../../../../runtime-docs/12-asgi-channel-semantic-roles-wire.md)).
- InterviewEngine Keep; ADR-1 mega-string Keep when roles paths unset (STORY-66 cutover residual).

## Target / AC
- [x] Channel turn path invokes role selection + assembly (not harness-only).
- [x] Semantic state persists/reads on channel sessions (AC-AIB-13-01 live path Partial→Met evidence).
- [x] G-02 WAIVER lifted or explicitly re-scoped with operator note.
- [x] Dual-confirm + stash path still Pass for regression smoke.

## Nested tasks (pkg-000068)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-65-t01-channel-semantic-state-service-bind](./task-aibridge-65-t01-channel-semantic-state-service-bind/README.md) | Scope-1 · AC-2 | Done |
| t02 | [task-aibridge-65-t02-channel-select-assemble-role-wire](./task-aibridge-65-t02-channel-select-assemble-role-wire/README.md) | Scope-1 · AC-1 | Done |
| t03 | [task-aibridge-65-t03-channel-meaning-invalidate-send](./task-aibridge-65-t03-channel-meaning-invalidate-send/README.md) | Scope-3 · L13-3 A | Done |
| t04 | [task-aibridge-65-t04-dual-confirm-stash-regression-smoke](./task-aibridge-65-t04-dual-confirm-stash-regression-smoke/README.md) | Scope-2 · AC-4 | Done |
| t05 | [task-aibridge-65-t05-g02-waiver-lift-or-rescope-note](./task-aibridge-65-t05-g02-waiver-lift-or-rescope-note/README.md) | AC-3 | Done |
| t08 | [task-aibridge-65-t08-story-gate-checklist](./task-aibridge-65-t08-story-gate-checklist/README.md) | package gate | PASS |
| t09 | [task-aibridge-65-t09-audit-g01-verified-state-g02-lifted-sync](./task-aibridge-65-t09-audit-g01-verified-state-g02-lifted-sync/README.md) | P5 G-01 | Done |
| t10 | [task-aibridge-65-t10-audit-g02-req13-ac02-ac03-channel-present](./task-aibridge-65-t10-audit-g02-req13-ac02-ac03-channel-present/README.md) | P5 G-02 | Done |

## Code points
- `src/aibridge/app.py` `/v1/channel/turns` · `channel.py` `process_turn` · `semantic_state/` · `roles/` · `confirm.invalidate_send_permission` · Keep dual-confirm/stash
