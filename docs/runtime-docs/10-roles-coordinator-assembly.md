# Roles, coordinator, assembly fixtures (STORY-63 / REQ-13)

Thin runtime note. Arch SSOT: [`../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md`](../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md). Peer port: [`07-interview-provider-port-env.md`](./07-interview-provider-port-env.md).

**Honesty:** stub fixtures ≠ GPT UI checkout / GPT-48 export SSOT. OOS store DDL (62) / live volume+parity (64). No LLM-router.

---

## 1) Module home

| Piece | Path |
|-------|------|
| Package | `src/aibridge/roles/` |
| Registry | five v1 roles + version pins (`RoleRegistry`) |
| Policy | `select_next_role` — phase/flags → **one** role |
| Assembly | `assemble_role_prompt` — core + role slice + session pin |
| Model path | `bind_role_interview_engine` → `interview_providers` Keep |

**AC-AIB-13-02:** five roles callable via coordinator (`coordinator.select_next_role` / policy).

---

## 2) Assembly (AC-AIB-13-03)

Read only from configured `DOGESTONIA_INSTRUCTIONS_DIR` + roles manifest (fixture env uses `tests/fixtures/content/roles-instructions/` + `roles.manifest.json`). Session pin = hash of core+role(+node) at start — no mid-flight silent swap. Live volume = STORY-64.

---

## 3) Confirm-offer (L13-1 / AC-08)

| Kind | Policy |
|------|--------|
| Understanding / interpretation | Soft auto-offer **may** remain (`offer_interpretation_confirm` on FC-less turn) |
| Send | **Never** automatic from ordinary reply — `offer_send_confirm` only after frozen FC |

---

## 4) AC-07 boundary

Fixture role/core texts must **not** encode gateway stash URL or SPA redirect procedure — server pipe stays REQ-11.

---

## 5) Isolation

Harness suite green without GPT UI tree. Bodies under `tests/fixtures/content/` only for stub.
