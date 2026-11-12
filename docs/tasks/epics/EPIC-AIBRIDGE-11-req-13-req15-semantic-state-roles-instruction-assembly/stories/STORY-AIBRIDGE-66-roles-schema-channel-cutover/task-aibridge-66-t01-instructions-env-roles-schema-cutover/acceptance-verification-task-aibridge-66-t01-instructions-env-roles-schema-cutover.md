# Acceptance — task-aibridge-66-t01-instructions-env-roles-schema-cutover

| Field | Value |
|-------|-------|
| **Date** | 2026-11-04T13:51:20Z |
| **Result** | **Done** · P3 |
| **Skill** | python-pro |
| **Note** | INSTRUCTIONS_* roles-schema unifies into channel_wire when ROLES_* empty |

## Claims

| Claim | Evidence |
|-------|----------|
| Env unify | `app.py` peek_manifest_schema → ChannelWireContext |
| Tests | `test_t01_instructions_env_roles_schema_cutover_unify` |
| Locks | no invent bodies · OOS 67 |
