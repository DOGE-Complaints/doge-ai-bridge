# Target technical architecture — OpenAI strict-schema compatibility projection

**Focus ID (filename):** REQ-07  
**Note:** The requirement file’s H1 currently reads «REQ-06»; Phase B packaging remains [`REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md`](../requirements/REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md). Canonical cross-links for this focus use **REQ-07** (file stem). H1 renumber is an Open Unknown (operator).  
**Status:** Target architecture (interview-locked 2026-09-24)  
**Parent product REQ:** [`REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md`](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md)  
**Interview report:** [`../analysis/zeya888.target-tech-arch-interview-REQ-07-openai-strict-schema-compat-2026-09-24.md`](../analysis/zeya888.target-tech-arch-interview-REQ-07-openai-strict-schema-compat-2026-09-24.md)  
**Story context (Implemented seams, not uniqueItems AC):** [`../tasks/backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md`](../tasks/backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md) — STORY-AIBRIDGE-19…22  
**Runtime package (do not renumber):** [`runtime/00-overview.md`](./runtime/00-overview.md)

This document is the **target technical architecture of the focus**. It is not a backlog of new STORY/pkg/tasks and does not authorize stub files.

---

## 1. Context & inputs

### 1.1 Why this exists

Production Telegram → n8n → aibridge turns fail when OpenAI Responses rejects the strict function tool because `uniqueItems` appears under `schema_binding.structured_payload` (observed `invalid_function_parameters`). The canonical Uus Veerenni pack **must keep** `"uniqueItems": true` on `geo.streets[].houses`. The runtime must project an OpenAI-compatible tool in memory and enforce uniqueness on the server after the model returns arguments ([REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §§1–3).

### 1.2 Functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product / AC / DoD | REQ-07 | Outcomes, prohibitions, test IDs, rollout |
| Prior content wiring | STORY-AIBRIDGE-19…22 (REQ-05 package) | Assembled prefix, full manifest, OAS in image, Phase A proof — **already Implemented** |
| Target tech of this focus | **This document** | Dual schemas, projection seam, Gate contract, minimal ValidationContext bind, two-stage verify |

### 1.3 Conscious out of scope (architecture)

- Changing meaning of the Uus Veerenni node schema; hand-edited dual node schemas; rewriting YAML/JSON on disk ([REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §4.2, §14).
- Channel OAS redesign; full REQ-04 confirm hardening beyond **minimal ValidationContext bind**.
- REQ-06 Phase B scalable packaging.
- **NEW** STORY keys / pkg / task trees (cite 19–22 only as coexistence).

---

## 2. Target technical architecture

### 2.1 Components & trust boundaries

```text
Canonical Story Intake OAS (disk, read-only)
Canonical pack payload JSON (disk, read-only)
        │
        ▼
generate_strict_tool (+ OpenAI compatibility projection)
        │
        ├─► DeploymentBundleState.strict_tool     (OpenAI-facing, no uniqueItems)
        │         └─► InterviewEngine.tools         (reuse per turn)
        │
        └─► ValidationContext (minimal create_app bind)
                  tool_parameters  ← projected strict_tool["parameters"]
                  pack_schema     ← canonical pack JSON (with uniqueItems)
                  wire_schema     ← Story Intake request body schema
                  constants       ← ServerConstants / env stamps
                        │
                        ▼
              ConfirmationGuard.validation_context
                        │
                        ▼
              validate_function_calls → run_three_gates
                  Gate 1: projected tool_parameters
                  Gate 2: canonical pack_schema (uniqueItems)
                  Gate 3: wire_schema after assemble_server_body
```

**Provider policy (code, not node content):** e.g. `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS = frozenset({"uniqueItems"})` in `tool_gen.py` ([REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) AIB-COMPAT-10). Only explicitly listed keywords may be stripped from the OpenAI-facing copy (AIB-COMPAT-11).

### 2.2 Startup lifecycle (unchanged skeleton)

```text
create_app
  → _init_stores
  → verify_and_register_deployment
  → generate_strict_tool  (+ compatibility projection; deep-copy; no disk write)
  → DeploymentBundleState.strict_tool
  → _apply_deployment_to_engine          # InterviewEngine.tools
  → minimal ValidationContext bind       # NEW for this focus (operator C)
  → /readyz fail-closed if projection or VC bind incomplete
```

Projection runs **once per process init**, not per Telegram message (AIB-COMPAT-06).

### 2.3 Gate contract (operator decision C)

| Gate | Schema | Role |
|------|--------|------|
| 1 | OpenAI **projection** (`tool_parameters`) | Args match what Responses was allowed to see |
| 2 | **Canonical** pack (`pack_schema`) | Domain rules including `uniqueItems: true` |
| 3 | Wire body vs wire schema | After `assemble_server_body` stamps |

Duplicate houses under one street → Gate 2 fail; no freeze / Send / gateway write ([REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §9.1).

### 2.4 Minimal ValidationContext bind (operator decision C)

In scope of this focus:

- Populate `ConfirmationGuard.validation_context` at composition time with dual schemas + `ServerConstants`.
- Existing dataclass shape in `coordinator.ValidationContext` (`tool_parameters`, `pack_schema`, `wire_schema`, `constants`) is sufficient — no invent of new public HTTP APIs.

Out of scope: remaining REQ-04 confirm/FSM/token hardening.

### 2.5 Canonical `uniqueItems` enforcement

Extend `request_assembly` validator / `FULL_SCHEMA_KEYWORDS` so Gate 2 (and any gate receiving a canonical schema with the keyword) enforces JSON-value structural uniqueness ([REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) AIB-COMPAT-04). `schema_validation_complete()` must **prove** enforcement, not only frozenset membership (AIB-COMPAT-07 / §8.2).

---

## 3. Ownership & contracts

| Artifact | Owner | Runtime may modify? |
|----------|-------|---------------------|
| `docs/openapi/story-intake-actions.openapi.yaml` | Git / image | **No** |
| `src/instructions/schema-packs.*.payload.schema.json` | Git / image | **No** |
| In-memory `strict_tool` | aibridge process | Generated once; treat as immutable after init |
| `ValidationContext` | aibridge process | Built from canonical + projected copies at bind |

No generated compatibility YAML/JSON on disk ([REQ-07](../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §5.1). No new Railway env for this change (§15.1).

---

## 4. Runtime / packaging / env

- **Start:** existing aibridge ASGI process; content pins `DOGESTONIA_*` unchanged in role.
- **Packaging:** projection is **in-memory only**. Canonical content already ships via Dockerfile `COPY src` + `COPY docs/openapi` (REQ-05 / STORY-21). **Packaging theme: N/A** for Volume hot-swap; Git ownership ≠ rewriting files at startup.
- **Fail-closed readiness:** projection failure, forbidden keyword remaining on OpenAI tool, missing uniqueness capability, or **absent/invalid ValidationContext** → `/readyz` not ready (operator two-stage DoD). Exact reason **string** remains an Open Unknown (must match existing `tool_gen_failed:*` / similar conventions).
- `/readyz` must not call OpenAI or write gateway (AIB-COMPAT-08).

---

## 5. Verify surfaces & two-stage DoD (operator)

### 5.1 Merge gate (CI / local) — code may merge

Mandatory: unit (projection + uniqueItems validator), readiness, integration with **fake** Responses transport. Must prove:

1. `uniqueItems` absent from entire OpenAI-facing `tools` payload;
2. canonical pack object/file semantics unchanged by projection;
3. Gate 2 rejects duplicate `houses`;
4. missing or invalid `ValidationContext` → `/readyz` not_ready;
5. regression fixture for the prior `invalid_function_parameters` case.

After merge: focus status **`implemented, live verification pending`** — **not** Done / production verified.

### 5.2 Deployment verification gate — production verified

After Railway deploy: one real Telegram turn through n8n + aibridge + **real** OpenAI API; reply without `invalid_function_parameters` (AC-09). Only then: **`production verified / rollout complete`**.

### 5.3 Live evidence (redacted)

Record: time (UTC), deployment/version or commit SHA, scenario id, pass/fail, correlation/request ID. **No** user narrative, Bearer, API keys, or full tool/args dump. Storage location (ops vs analysis file) is operator-chosen at verify time — this arch does not invent a mandatory new path.

---

## 6. Coexistence with as-is

| Concern | As-is (verified) | Target |
|---------|------------------|--------|
| Pack `uniqueItems` | Present at houses array — `schema-packs.uus_veerenni_civic.v3.payload.schema.json` | Keep on disk |
| Tool gen | `tool_gen.generate_strict_tool` deep-copies pack into parameters; **no** OpenAI keyword strip | Add recursive projection + post-assert |
| Validator keywords | `request_assembly.FULL_SCHEMA_KEYWORDS` — **no** `uniqueItems` | Add enforcement + readiness probe |
| Engine tools | `_apply_deployment_to_engine` sets `prompt_channel=prefix` + `tools` | Unchanged reuse of projected tool |
| ValidationContext bind | `create_app` does **not** set `guard.validation_context` | Minimal bind (this focus) |
| REQ-05 stories 19–22 | Implemented (prefix, manifest, OAS image, proof) | Context only |

---

## 7. Open questions

1. REQ file H1 «REQ-06» vs filename REQ-07 vs Phase B REQ-06 — renumber/patch H1?
2. Exact `/readyz` reason token(s) for unbound/invalid ValidationContext.
3. On-disk home for live-evidence note (when AC-09 runs).

---

## 8. Not in this document

- NEW STORY / epic / pkg / task README scaffolding  
- Product code patches (implement separately)  
- Stub schemas or “path existence” files  
- Second architecture prompt / P3 execution  

**Handoff options (operator):** implement against REQ-07 + this TECH-ARCH; optional PA.2 functional polish of REQ with pointers here; optional later `req-to-backlog-stories` if NEW work items are desired — **not** created by this materialize.
