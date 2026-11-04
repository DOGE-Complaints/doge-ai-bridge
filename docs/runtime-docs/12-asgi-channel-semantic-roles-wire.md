# ASGI channel: semantic state + roles wire (STORY-65 / REQ-13)

Thin runtime note. Arch: [`../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md`](../architecture/req15-semantic-state-roles/01-semantic-state-store-invalidation.md) · [`02-roles-coordinator-assembly.md`](../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md). Soft peers: runtime `09` / `10`. Gap V2 close.

**G-02:** ASGI/channel bind **Lifted** (STORY-65) — product path `/v1/channel/turns` invokes `SemanticStateService`, `select_next_role`, and (when roles paths configured) `assemble_role_prompt`. Harness-only residual closed for wire.

**Honesty:** STORY-66 roles-schema cutover details OOS · STORY-67 Railway volume Pass OOS · GPT-48 authoring OOS. No new channel HTTP surface.

---

## 1) Wire (Present)

| Piece | Where |
|-------|--------|
| Context | `aibridge.channel_wire.ChannelWireContext` on `app.state.channel_wire` |
| Semantic | `app.state.semantic_state_service` — Memory or Postgres store; `confirm_guard` → `invalidate_send_permission` |
| Turn hook | `apply_before_engine_turn` inside `channel.process_turn` / `process_turn_async` before InterviewEngine |
| Routes | Keep `/v1/channel/turns` + `/v1/channel/actions` only — **no new HTTP** |

## 2) Roles assembly env (optional until STORY-66)

| Env | Role |
|-----|------|
| `DOGESTONIA_ROLES_INSTRUCTIONS_DIR` | Roles instruction files root |
| `DOGESTONIA_ROLES_MANIFEST` | Roles manifest JSON (`core` + `roles`) |

When unset: `select_next_role` still runs; ADR-1 mega-string instructions Keep until cutover.

## 3) Meaning → invalidate (L13-3 Target A)

`SemanticStateService` meaning writes (confirmed fact / correction / phase-with-rights) call `ConfirmationGuard.invalidate_send_permission` on the channel session — no Telegram EDIT required.

## 4) Regression Keep

Dual-confirm + stash / gateway pipe unchanged. No invent FSM rewrite.
