# Node aibridge customization — operator manual

**Audience:** people who configure a civic DOGEstonia interview node for one neighbourhood, district, or city (content owners / aibridge operators).  
**Language:** English  
**Code SSOT:** `doge-ai-bridge/src/aibridge/` (`content.py`, `tool_gen.py`, `deployment.py`, `request_assembly.py`, `app.py`, `interview.py`, `config.py`)  
**Active content dump:** `doge-ai-bridge/src/instructions/` · wire OAS: `doge-ai-bridge/docs/openapi/story-intake-actions.openapi.yaml`  
**Architecture notes:** `docs/architecture/runtime/02-content-packaging.md`, `docs/requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md`  
**Landing contrast:** marketing landings use a **Railway Volume** bundle ([landing operator manual](../../../landing/docs/manuals/node-landing-customization-operator-manual.md)). Aibridge Phase A does **not** — node content ships in the **Git image**.

This guide explains **how to customize a node’s interview instructions and pack schema without forking or editing the shared Python runtime**.

---

## Quick: pin the active node and confirm readiness

Phase A content lives under `src/instructions/` (flat files) plus Story Intake OpenAPI under `docs/openapi/`. The Dockerfile copies both into the image (`COPY src`, `COPY docs/openapi`). Changing node text or pack schema requires a **rebuild/redeploy**, not a Volume upload.

**From `doge-ai-bridge/` — local Phase A pins** (canonical names from `.env.example` / `Settings`):

```env
DOGESTONIA_INSTRUCTIONS_DIR=src/instructions
DOGESTONIA_INSTRUCTIONS_MANIFEST=src/instructions/instructions.manifest.json
DOGESTONIA_CONTENT_SOURCE_COMMIT=<git-sha-you-pin>
DOGESTONIA_OPENAPI_PATH=docs/openapi/story-intake-actions.openapi.yaml
DOGESTONIA_PAYLOAD_SCHEMA_PATH=src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json
DOGESTONIA_TOOL_SCHEMA_PATH=
DOGESTONIA_SCHEMA_ID=uus_veerenni_civic
DOGESTONIA_SCHEMA_VERSION=v3
```

**Image paths (WORKDIR `/app`):**

```env
DOGESTONIA_INSTRUCTIONS_DIR=/app/src/instructions
DOGESTONIA_INSTRUCTIONS_MANIFEST=/app/src/instructions/instructions.manifest.json
DOGESTONIA_OPENAPI_PATH=/app/docs/openapi/story-intake-actions.openapi.yaml
DOGESTONIA_PAYLOAD_SCHEMA_PATH=/app/src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json
```

`content_configured()` is true only when **all five** are non-empty: `CONTENT_SOURCE_COMMIT`, `INSTRUCTIONS_DIR`, `INSTRUCTIONS_MANIFEST`, `OPENAPI_PATH`, `PAYLOAD_SCHEMA_PATH`.

After deploy/restart, check `GET /readyz` — content verify + strict tool generation must succeed (see §10). Full smoke: `docs/ops/req-05-phase-a-smoke.md`. Web/Railway notes: `docs/runbooks/aibridge-web-service-local-railway.md` §1.1b.

---

## 1. The idea in one minute

There is **one** shared aibridge runtime (Python in Git).  
Each civic **node** is expressed as a **flat content dump** + env pins — not as a Python branch.

| Lives in Git (shared app) | Lives in the node content dump |
|---------------------------|--------------------------------|
| Channel façade, confirm FSM, budgets, gateway client | Module-1 instruction Markdown + node overlays |
| `generate_strict_tool` / three gates / stable prefix | Pack `payload.schema.json`, `pack.json`, taxonomy, locale |
| Dockerfile packaging rules | `instructions.manifest.json` `files[]` order |
| Allowlisted tool name `postStoryDraftStash` | `DOGESTONIA_SCHEMA_ID` / `SCHEMA_VERSION` identity |

You deploy the **same** runtime image shape for every node. You change **only** flat files under `src/instructions/`, the Story Intake OAS path pin (rarely), and `DOGESTONIA_*` env — then rebuild.

**What OpenAI receives is not the YAML file.** At startup, aibridge loads the Story Intake OpenAPI YAML, projects a **strict Responses function tool** JSON, injects the pack payload schema into `schema_binding.structured_payload`, and sends that tool in `POST /v1/responses` together with a **stable system prefix** built from assembled instructions.

```text
ENV (DOGESTONIA_*)
  → load_content_bundle()          # manifest files[] → assembled_instructions
  → generate_strict_tool()         # OAS YAML + pack JSON → strict tool
  → _apply_deployment_to_engine()  # prompt_channel=prefix, tools=[strict_tool]
  → each turn: build_stable_prefix + assemble_responses_request → OpenAI
  → on function_call: validate_function_calls → run_three_gates (if ValidationContext bound)
```

---

## 2. What you prepare

### 2.1 Folder layout (Phase A flat dump)

Point `DOGESTONIA_INSTRUCTIONS_DIR` at a directory that looks like this (paths in `files[]` must be **root children only** — no `/`, no `..`):

```text
src/instructions/
├── instructions.manifest.json          ← required entry point
├── root.md / bootstrap.md / base.md    ← Module-1 core (shared)
├── … other Module-1 *.md …
├── schema-packs.README.md              ← active schema_id / schema_version index
├── schema-packs.<schema_id>.<ver>.interview-overlay.md
├── schema-packs.<schema_id>.<ver>.inbound-validation.md
├── schema-packs.<schema_id>.<ver>.locale-jurisdiction.md
├── schema-packs.<schema_id>.<ver>.pack.json
├── schema-packs.<schema_id>.<ver>.payload.schema.json
└── schema-packs.<schema_id>.<ver>.taxonomy.json
```

Wire OAS (not inside the instructions dir):

```text
docs/openapi/
├── story-intake-actions.openapi.yaml   ← DOGESTONIA_OPENAPI_PATH (tools + Gate 3)
└── aibridge-channel-v1.openapi.yaml     ← channel contract; NOT for tools / not in files[]
```

**Hard rules (enforced by `content.py`):**

- Every `manifest.files[]` entry is a **single path segment** under the instructions dir (no nested paths).
- Files must exist, be non-empty, UTF-8.
- `bundle_version` is a required non-empty string; `files` is a non-empty list without duplicates.
- No network fetch of instructions at request time — local FS only (`DOGESTONIA_CONTENT_SOURCE_COMMIT` is a pin string, not a live Git pull).

### 2.2 Start from the shipped node (recommended)

| Artifact | Path | Role |
|----------|------|------|
| Active civic pack | `src/instructions/schema-packs.uus_veerenni_civic.v3.*` | Current Phase A node |
| Manifest | `src/instructions/instructions.manifest.json` | Ordered join list (`bundle_version`: `uus-veerenni-v3-local-1`) |
| Pack index | `src/instructions/schema-packs.README.md` | Documents active `schema_id` / `schema_version` |
| Minimal test dump | `tests/fixtures/content/` | Loader / tool_gen tests only — not a production node |

Copy the six flat pack files to a new `<schema_id>.<ver>` prefix, edit content, update `files[]` + README + env. Do **not** invent parallel nested `schema-packs/` upload trees for aibridge Phase A (nested layout is retired for this dump; gateway may still keep a nested tree as its own SSOT — see pack README).

---

## 3. How OpenAI sees the node

### 3.1 Assembled instructions (prompt text)

`load_content_bundle` reads each `files[]` entry in order and joins with `"\n\n"` (`STABLE_SEPARATOR`). That string becomes `InterviewEngine.instructions`.

`_apply_deployment_to_engine` sets:

- `engine.prompt_channel = "prefix"`
- `engine.instructions = assembled_instructions`
- `engine.tools = [strict_tool]` when tool gen succeeded
- `engine.pack_id = "{schema_id}/{schema_version}"` when both env values are set

Empty assembled text after strip → fail-closed error `assembled_instructions_empty` (readiness stays unhealthy).

### 3.2 Stable prefix (what the model reads every turn)

Production channel is **prefix**, not the Responses `instructions` field. Each turn, `InterviewEngine._build_request` builds:

```text
<<<INSTRUCTIONS>>>
<assembled_instructions>
<<<TOOL_SCHEMA>>>
<json.dumps(tools, sort_keys=True)>
<<<PACK_ID>>>
<schema_id>/<schema_version>
```

That string is sent as a **system** message. The API payload must **not** also set `instructions` (`assert_prompt_xor` — dual channel is an error).

Because `store:false` is forced, the LLM does **not** retain the bundle across turns in OpenAI storage — aibridge resends the prefix every turn.

### 3.3 Tools array (the “YAML” outcome)

`assemble_responses_request` always sets:

- `store: false`
- `parallel_tool_calls: false`
- `tools`: the strict function tool list (one consequential tool in Phase A)

The tool is **not** the raw OpenAPI document. See §4.

---

## 4. Story Intake OAS YAML → strict OpenAI tool

### 4.1 Inputs

| Input | Env / path | Used by |
|-------|------------|---------|
| Wire OAS (YAML) | `DOGESTONIA_OPENAPI_PATH` → `story-intake-actions.openapi.yaml` | `generate_strict_tool`, Gate 3 wire shape, content hash |
| Pack payload JSON Schema | `DOGESTONIA_PAYLOAD_SCHEMA_PATH` | Injected into tool parameters; Gate 2; content hash |
| Pack identity | `DOGESTONIA_SCHEMA_ID` + `DOGESTONIA_SCHEMA_VERSION` | Required together to run tool gen at deploy; become `pack_id` / `x_aibridge` |
| Optional recorded tool JSON | `DOGESTONIA_TOOL_SCHEMA_PATH` | Hash pin only; generation still runs from OAS + pack when id/version set |

### 4.2 What `generate_strict_tool` does (`tool_gen.py`)

1. Load OAS with `yaml.safe_load`.
2. Resolve the **canonical** operation: `operationId == postStoryDraftStash`, `POST /story-drafts`, Bearer security, success `201`. Any other shape → `ToolGenError` (readiness failure — no silent non-strict fallback).
3. Deref `$ref` / merge `allOf`; reject unsupported keywords (`oneOf`, `anyOf`, `not`, `if`/`then`/`else`, …).
4. Strip OpenAPI-only fields from the request schema.
5. Inject the pack JSON Schema as `properties.schema_binding.properties.structured_payload`.
6. Force strict object shape (`additionalProperties: false`, every property required).
7. Emit a Responses-flat tool:

```json
{
  "type": "function",
  "name": "postStoryDraftStash",
  "description": "Stash a story draft for browser submit",
  "strict": true,
  "parameters": { "...": "wire schema with pack inject" },
  "x_aibridge": {
    "schema_id": "<DOGESTONIA_SCHEMA_ID>",
    "schema_version": "<DOGESTONIA_SCHEMA_VERSION>",
    "operation_path": "/story-drafts",
    "operation_method": "POST"
  }
}
```

That object is what appears under `tools` in the OpenAI request (and again, serialized, under `<<<TOOL_SCHEMA>>>` in the system prefix).

### 4.3 What operators may change vs what is fixed

| You customize | Fixed in code |
|---------------|---------------|
| Pack `payload.schema.json` (shape of `structured_payload`) | Tool name / path: `postStoryDraftStash` / `POST /story-drafts` |
| Overlay Markdown + `pack.json` / taxonomy (as **prompt** text via manifest) | Strict generation + server-owned field strip |
| Manifest order and Module-1 wording | `store:false`, `parallel_tool_calls:false`, prefix XOR |
| `SCHEMA_ID` / `SCHEMA_VERSION` env | Envelope stamp `m2.story_intake_envelope.v2` in `ServerConstants` |
| Story Intake OAS only in **lockstep** with gateway | No per-node `if schema_id == …` branches in Python |

**Channel OAS** (`aibridge-channel-v1.openapi.yaml`) describes `/v1/channel/*` for n8n adapters. It rides in the image but must **not** be `DOGESTONIA_OPENAPI_PATH` and must **not** appear in `files[]`.

### 4.4 Server-owned fields

Models must not set paths listed in `SERVER_OWNED_FIELD_PATHS` (e.g. envelope `schema_version`, `schema_binding.schema_id` / `schema_version`, `origin.*`, Authorization). `strip_server_owned_fields` + `assemble_server_body` stamp server values from `ServerConstants` / env (`DOGESTONIA_ORIGIN_SOURCE`, schema id/version).

---

## 5. File-by-file checklist

### 5.1 `instructions.manifest.json`

```json
{
  "bundle_version": "your-node-label-1",
  "files": [
    "root.md",
    "…",
    "schema-packs.README.md",
    "schema-packs.<id>.<ver>.interview-overlay.md",
    "schema-packs.<id>.<ver>.inbound-validation.md",
    "schema-packs.<id>.<ver>.locale-jurisdiction.md",
    "schema-packs.<id>.<ver>.pack.json",
    "schema-packs.<id>.<ver>.payload.schema.json",
    "schema-packs.<id>.<ver>.taxonomy.json"
  ]
}
```

Bump `bundle_version` when you change the dump so operators can tell pins apart. Order in `files[]` **is** the prompt order.

### 5.2 Module-1 core Markdown

Shared interview policy (`story-interview-flow.md`, `api-orchestrator.md`, `story-normalizer.md`, …). Prefer pack overlays for node-specific civic fields; keep core files protocol-generic when possible (orchestrator text points at the active pack via `schema-packs.README.md`).

### 5.3 Pack six-file set (flat names)

| File | Runtime role |
|------|----------------|
| `…payload.schema.json` | **Executable for aibridge:** tool inject + Gate 2; also joined into prompt if listed in `files[]` |
| `…pack.json` | **Prompt-only** for aibridge Python (not parsed as JSON by the loader) — cards / field_policy / geo_intake for the model |
| `…taxonomy.json` | Prompt-only knowledge |
| `…interview-overlay.md` | Prompt-only interview behavior for the node |
| `…inbound-validation.md` | Prompt-only pre-flight rules |
| `…locale-jurisdiction.md` | Prompt-only locale / jurisdiction framing |
| `schema-packs.README.md` | Prompt-only active pair index |

Gateway may keep a nested executable copy under `doge-complaints-gateway/schema-packs/…` — keep identities aligned when you change `schema_id` / `schema_version`.

### 5.4 Dual role of `payload.schema.json`

The same file is typically:

1. Listed in `files[]` → concatenated into `assembled_instructions` (model can read the schema text).
2. Pointed to by `DOGESTONIA_PAYLOAD_SCHEMA_PATH` → loaded again as JSON for `generate_strict_tool` and (when bound) Gate 2.

Keep those two references on the **same** artifact for one active pack.

---

## 6. Env map (content → OpenAI)

### 6.1 Content / schema pins (`config.py` → `Settings`)

| Env | Purpose |
|-----|---------|
| `DOGESTONIA_INSTRUCTIONS_DIR` | Flat dump root (**directory**, not a file) |
| `DOGESTONIA_INSTRUCTIONS_MANIFEST` | Path to `instructions.manifest.json` |
| `DOGESTONIA_CONTENT_SOURCE_COMMIT` | Required pin string for verify |
| `DOGESTONIA_OPENAPI_PATH` | Story Intake wire YAML |
| `DOGESTONIA_PAYLOAD_SCHEMA_PATH` | Pack payload JSON Schema |
| `DOGESTONIA_TOOL_SCHEMA_PATH` | Optional recorded tool JSON (hash); empty OK |
| `DOGESTONIA_SCHEMA_ID` | e.g. `uus_veerenni_civic` |
| `DOGESTONIA_SCHEMA_VERSION` | e.g. `v3` |
| `DOGESTONIA_OPERATION_ID` | Present on `Settings` (default `postStoryDraftStash`); **tool gen + allowlist use hardcoded** `CANONICAL_OPERATION_ID` in `tool_gen.py` / `coordinator.py` — changing this env alone does not retarget the tool |
| `DOGESTONIA_ORIGIN_SOURCE` | Stamped into assembled body `origin.source` |

### 6.2 Not content paths

`AIBRIDGE_*` covers channel auth, budgets, dry-run, deployment id, memory-store policy, etc. Those are **ops/runtime**, not instruction pins. There are no live `CONTENT_*` / `INSTRUCTIONS_*` / `OPENAPI_*` / `PACK_*` aliases without the `DOGESTONIA_` prefix — comments in `.env` that mention short names are documentation shorthand only.

### 6.3 Intake / model (needed to run interviews, not to assemble the tool)

Also configure `OPENAI_API_KEY`, `OPENAI_MODEL`, `OPENAI_STORE_RESPONSES=false`, `GATEWAY_BASE_URL`, gateway bearer, channel bearer, etc. Those do not change pack shape; without them channel turns fail readiness or outbound calls.

---

## 7. Three gates and `structured_payload`

When a consequential `function_call` arrives, `validate_function_calls` (`coordinator.py`) allowlists the tool name, then runs `run_three_gates` **if** a `ValidationContext` is present:

| Gate | Validates |
|------|-----------|
| 1 | Full tool args vs strict tool `parameters` |
| 2 | `schema_binding.structured_payload` vs **pack** schema (missing payload → `gate2: structured_payload required`) |
| 3 | Server-assembled body vs **wire** schema |

Then `assemble_server_body` stamps envelope / pack ids / origin and computes `draft_hash`.

### As-built composition gap (do not ignore)

`ConfirmationGuard.validation_context` exists as a field (`confirm.py`), and tests / helpers bind a `ValidationContext` manually. **`create_app` does not set `validation_context` today.** Without binding, FC validation raises `schemas not configured` (message from `validate_function_calls`). Pilot runbooks document this gap; this manual does **not** claim production has gates wired end-to-end until composition binds the context.

Engine **instructions + tools** from the content dump **are** applied at startup (`_apply_deployment_to_engine`). The gap is specifically the confirm-path schema binding for three gates.

---

## 8. Recipe: customize or add a node (Phase A)

1. **Copy** the six `schema-packs.uus_veerenni_civic.v3.*` files to `schema-packs.<new_id>.<new_ver>.*`.
2. **Edit** overlays, `pack.json`, taxonomy, and especially `payload.schema.json` for the new civic fields / enums.
3. **Update** `schema-packs.README.md` active pair table.
4. **Update** `instructions.manifest.json` — replace old pack filenames in `files[]`, bump `bundle_version`.
5. **Retarget env:** `DOGESTONIA_PAYLOAD_SCHEMA_PATH`, `DOGESTONIA_SCHEMA_ID`, `DOGESTONIA_SCHEMA_VERSION`, and a fresh `DOGESTONIA_CONTENT_SOURCE_COMMIT`.
6. **Do not** change Python for a normal node swap. Change Story Intake OAS only with gateway lockstep.
7. **Rebuild and redeploy** the aibridge image (Dockerfile must include `src/instructions` + `docs/openapi`).
8. **Verify** `/readyz` and a smoke turn (see §10).

Phase B scalable packaging (REQ-06) is **not** as-built for operators yet — do not assume Volume hot-swap or multi-pack registries beyond what this dump + env provide.

---

## 9. What changes when you swap the dump (same runtime)

With the same Python revision, a different valid flat dump + pins can change:

- Interview wording and node overlays
- Pack identity (`pack_id` in the prefix)
- Strict tool `parameters` (via pack inject and optional OAS update)
- Hashes registered in the content bundle registry (`bundle_hash`, instruction/OAS/pack hashes)

It must **not** redefine channel HTTP contracts, confirm FSM semantics, or allowlist a second consequential tool without a runtime change.

Contrast with landing: swapping aibridge content is an **image/content commit** operation, not a Volume subdirectory swap.

---

## 10. Verify

### 10.1 Startup / readiness

- `Settings.content_configured()` → all five pins set.
- `verify_and_register_deployment` succeeds (no `content_verify_failed:*`, no `tool_gen_failed:*`).
- `_apply_deployment_to_engine` does not return `assembled_instructions_empty`.
- `GET /readyz` healthy for content + strict tool checks (`readiness.py` re-runs / checks tool gen as implemented).

### 10.2 Smoke and proof pointers

| Check | Where |
|-------|--------|
| Ops smoke | `docs/ops/req-05-phase-a-smoke.md` |
| Local/Railway pins | `docs/runbooks/aibridge-web-service-local-railway.md` §1.1b |
| Full manifest load | `tests/test_story_20_full_manifest.py` |
| Engine wire / prefix | `tests/test_story_19_engine_wire.py` |
| OPENAPI_PATH = story-intake; channel not in `files[]` | `tests/test_story_21_oas_path_contract.py` |
| Phase A proof | `tests/test_story_22_phase_a_proof.py` |

### 10.3 Turn-level mental model

```http
POST /v1/channel/turns
```

n8n (or any channel client) sends user text; aibridge builds the Responses request with system prefix + tools. On stash intent, the model emits `function_call` `postStoryDraftStash` with `schema_binding.structured_payload` matching the pack. Confirm / gateway path is separate (see confirm + gateway architecture docs).

---

## 11. Common mistakes

| Mistake | What happens |
|---------|----------------|
| Point `DOGESTONIA_OPENAPI_PATH` at `aibridge-channel-v1.openapi.yaml` | Wrong wire for tools/gates — must be Story Intake |
| Set `DOGESTONIA_INSTRUCTIONS_DIR` to a file (e.g. the manifest path) | Load fails — must be the instructions **directory** |
| Nested paths in `manifest.files[]` (`schema-packs/foo.md`) | `ContentLoadError` — root children only |
| Empty file in `files[]` | Load fails |
| Change pack id/version in env but leave old filenames in `files[]` | Prompt and tool identity diverge |
| Expect Volume hot-swap like landing | Phase A requires image rebuild with updated `src/instructions` |
| Assume three gates run in production create_app | `validation_context` not bound — FC → `schemas not configured` until composition is fixed |
| Treat `pack.json` as parsed by Python | Only prompt text unless you also change runtime |
| Edit OAS keywords unsupported by tool_gen (`oneOf`, …) | `tool_gen_failed:*` at startup |
| Set `OPENAI_STORE_RESPONSES=true` | Settings reject — store must stay false |
| Change only `DOGESTONIA_OPERATION_ID` expecting a new tool | Ignored by `generate_strict_tool` / allowlist — both use `CANONICAL_OPERATION_ID` |

---

## 12. Related docs

| Doc | Path |
|-----|------|
| REQ-05 Phase A | `docs/requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md` |
| REQ-06 Phase B (draft / future) | `docs/requirements/REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md` |
| Content packaging architecture | `docs/architecture/runtime/02-content-packaging.md` |
| Phase A smoke | `docs/ops/req-05-phase-a-smoke.md` |
| Web / Railway pins | `docs/runbooks/aibridge-web-service-local-railway.md` |
| Pilot (incl. validation_context notes) | `docs/runbooks/AIBRIDGE-RAILWAY-N8N-TELEGRAM-PILOT-RUNBOOK.md` |
| QA inbound/outbound data flow | `docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md` |
| Pack naming SSOT | `src/instructions/schema-packs.README.md` |
| Landing node customization (Volume) | `landing/docs/manuals/node-landing-customization-operator-manual.md` |
| n8n integration context | `docs/analysis/aibridge-n8n-integration-context-2026-09-19.md` |

---

## 13. Code map (operators who need to cite symbols)

| Concern | Module | Symbols |
|---------|--------|---------|
| Env / `content_configured` | `src/aibridge/config.py` | `Settings`, `content_configured` |
| Flat load + hash | `src/aibridge/content.py` | `load_manifest`, `load_content_bundle`, `LoadedContentBundle` |
| Deploy + tool gen | `src/aibridge/deployment.py` | `verify_and_register_deployment`, `DeploymentBundleState` |
| OAS → tool | `src/aibridge/tool_gen.py` | `generate_strict_tool`, `CANONICAL_OPERATION_ID` |
| Prefix + gates | `src/aibridge/request_assembly.py` | `build_stable_prefix`, `run_three_gates`, `assemble_server_body` |
| Engine bind | `src/aibridge/app.py` | `_init_stores`, `_apply_deployment_to_engine` |
| Per-turn OpenAI request | `src/aibridge/interview.py`, `responses_client.py` | `_build_request`, `assemble_responses_request` |
| FC freeze / gates call | `src/aibridge/coordinator.py` | `ValidationContext`, `validate_function_calls` |
| Guard slot | `src/aibridge/confirm.py` | `ConfirmationGuard.validation_context` |
| Image packaging | `Dockerfile` | `COPY src`, `COPY docs/openapi` |

---

**Bottom line:** customize the node by editing the flat instruction dump and pack payload schema, pinning `DOGESTONIA_*`, and redeploying the image. The YAML you care about for OpenAI is Story Intake OAS — converted at startup into a strict `postStoryDraftStash` tool with your pack’s `structured_payload` schema injected — plus the assembled Markdown prefix, not a raw YAML upload to the API.
