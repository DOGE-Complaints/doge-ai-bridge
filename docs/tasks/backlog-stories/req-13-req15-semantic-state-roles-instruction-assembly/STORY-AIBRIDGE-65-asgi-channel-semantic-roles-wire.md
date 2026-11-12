# STORY-AIBRIDGE-65 — ASGI channel: semantic state + roles wire

## Meta
- **Key:** `STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire`
- **Status:** **Done** · **Product Done** · pkg-000068 · G-02 **Lifted** · P8 `0ccedc6`/`15fc620`/`fde569a` · 2026-11-04 · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire-20261104.md) · [wave](../../run-reports/operator-waves/wave-20261104-req13-wire-65-66.md)
- **Parent REQ:** [`REQ-13`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) · G-02 Lifted
- **Parent product:** [`REQ15`](<../../../../../docs/requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>) AC-06 / AC-09
- **Package:** [`INDEX.md`](INDEX.md)
- **Gap:** V2 ([gap audit](../../../../../docs/analysis/req15-target-state-code-gap-audit-2026-11-03.md)) — closed by this story
- **Closure process:** [`req15-gap-closure-process-zeya888-2026-11-03.md`](../../../../../docs/analysis/req15-gap-closure-process-zeya888-2026-11-03.md)
- **Siblings:** [62](STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [63](STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) · [66](STORY-AIBRIDGE-66-roles-schema-channel-cutover.md)
- **Skill declared:** `python-pro`
- **Emitted:** 2026-11-03
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Lift REQ-13 **G-02**: bind Present `SemanticStateService`, `select_next_role`, `assemble_role_prompt` into **channel** `/v1/channel/turns` (and related action path as needed) so product path ≠ harness-only.
- Preserve REQ-11 dual-confirm / gateway pipe; do not invent new channel HTTP surface.
- Meaning-change → send invalidation (L13-3 Target A) on channel when semantic writes occur.

## Out of scope
- GPT UI instruction authoring (REQ-48).
- Telegram transport; gateway/spa redesign.
- Full Railway volume Pass (STORY-67).
- Roles-schema env cutover details beyond wire readiness (STORY-66).

## Verified current state
- Modules Present: `semantic_state/`, `roles/` (assembly/policy/registry); stories 62–64 Product Done (harness).
- Channel ASGI wire **Present**: `channel_wire.apply_before_engine_turn` on `/v1/channel/turns` · `SemanticStateService` + `select_next_role` (+ `assemble_role_prompt` when roles paths Present). G-02 **Lifted** (runtime [`12`](../../../runtime-docs/12-asgi-channel-semantic-roles-wire.md)).
- InterviewEngine Keep; ADR-1 mega-string Keep when roles paths unset (cutover = STORY-66).

## Target / AC
- [x] Channel turn path invokes role selection + assembly (not harness-only).
- [x] Semantic state persists/reads on channel sessions (AC-AIB-13-01 live path Partial→Met evidence).
- [x] G-02 WAIVER lifted or explicitly re-scoped with operator note.
- [x] Dual-confirm + stash path still Pass for regression smoke.

## Dependencies
- Hard: STORY-62 / 63 Present modules.
- Soft: before full quality smoke — STORY-66 cutover (**Done**).
