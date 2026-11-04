# Roles-schema channel cutover (STORY-66 / REQ-13 §3b)

Thin runtime note. Arch: [`../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md`](../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md). Soft peers: runtime `10` / `12`. Gap V3 (+ local V8-light).

## Live SSOT

- **Roles-schema** manifest: `bundle_version` (string) · `core` (root child) · `roles` (object of `{file, version}`).
- Env: `DOGESTONIA_INSTRUCTIONS_DIR` + `DOGESTONIA_INSTRUCTIONS_MANIFEST` point at roles-schema for product ready/channel.
- Optional explicit `DOGESTONIA_ROLES_*`; when empty, channel wire **reuses** INSTRUCTIONS_* if that manifest is roles-schema (STORY-66 unify).
- Loader: `content.load_content_bundle` accepts roles-schema; hashes core + all role files; ADR-1 readiness prefix = **core** text; per-turn assembly via `assemble_role_prompt` (STORY-65 wire).

## Phase-A `files[]` — legacy/dev-only

- Phase-A `bundle_version` + `files[]` loader **remains** for legacy/dev fixtures (`src/instructions/…`, older tests).
- After cutover, Phase-A is **not** live SSOT of the GPT-48 / REQ15 roles line.
- Dual schema on one manifest (`files[]` **and** `roles.*`) → fail-closed (`ContentLoadError`).

## Local consume (MVP light)

- Configure DIR/MANIFEST to Present GPT UI export: `GPT UI/instructions-roles-req15/` (+ `roles.manifest.json`).
- Prove inventory: core + five v1 role files load; no invent instruction bodies.
- **OOS:** Railway volume / AC-14 full → **STORY-67**. Hash SSOT invent → joint Open with GPT-48.

## Evidence

- Code: `src/aibridge/content.py` · `channel_wire.py` · `app.py` bind unify · `roles/assembly.py`
- Tests: `tests/test_story_66_roles_schema_channel_cutover.py`
- Peer export: `GPT UI/instructions-roles-req15/roles.manifest.json`
