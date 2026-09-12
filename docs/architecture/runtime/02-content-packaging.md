# Content packaging & pin

**Parent REQ:** [REQ-01 §8–§9, §14, §17–§18](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)  
**Wire OAS in-repo:** [story-intake-actions.openapi.yaml](../../openapi/story-intake-actions.openapi.yaml)

---

## 1. Method note

**Git ownership ≠ image packaging.**  
Owning files in `GPT UI/instructions` or a pack tree in another checkout does **not** place them in the Railway container. CI must stage a pinned immutable bundle.

---

## 2. What is bundled

- Manifest-listed instruction files only (root children; no recursive archive/onboarding).
- Canonical Story Intake OpenAPI ([story-intake-actions.openapi.yaml](../../openapi/story-intake-actions.openapi.yaml)).
- Active pack `payload.schema.json` (+ identity used at readiness).
- Recorded source commit id(s) and hashes (instructions, wire OAS, pack, generated tool schema).

Runtime must **not** fetch mutable instructions from GitHub at request time.

---

## 3. CI shape (multi-repository)

```text
Content owners merge (instructions / pack repos as applicable)
        ↓
Aibridge operator selects commit SHA(s)
        ↓
CI multi-repo checkout → immutable tarball
        ↓
Docker build (aibridge app + tarball)
        ↓
Startup verify → Postgres register-once by bundle_hash
        ↓
/readyz + façade smoke → accept traffic
```

**Do not** rely on a fragile monorepo-only `COPY` of sibling checkouts that may be absent on the build agent. Prefer explicit multi-repository checkout → stage tarball → image layer.

Merge to content paths must **not** auto-promote production.

Exact absolute paths for instruction/pack checkouts: **Unknown** until CI config pins them (env: `DOGESTONIA_INSTRUCTIONS_DIR`, `DOGESTONIA_INSTRUCTIONS_MANIFEST`, `DOGESTONIA_OPENAPI_PATH`, `DOGESTONIA_PAYLOAD_SCHEMA_PATH`, `DOGESTONIA_CONTENT_SOURCE_COMMIT`).

---

## 4. PostgreSQL versioned bundle registry (pilot physical store)

**Chosen store:** PostgreSQL registry — not Railway Volume, not “Unknown”.

Logical model:

```text
content_bundle
  bundle_hash (unique, PK)
  source_commit
  bundle_version
  instructions_hash
  wire_oas_hash
  pack_hash
  tool_schema_hash
  verified_at
  immutable_payload_or_components

session
  ...
  content_bundle_hash → content_bundle.bundle_hash
  deployment_id / node_id (server-owned)
```

Rules:

1. After image verify, register bundle **once** by `bundle_hash`.
2. Payload/components stored once per hash — not copied into every session row.
3. Bundle rows are **immutable** after registration.
4. Session pins `content_bundle_hash`; resume loads **that** bundle, not “whatever is current”.
5. `/readyz` validates the **current deployment** bundle; session resume validates presence of its pinned bundle.
6. **GC** deletes a bundle only if no active sessions reference it **and** audit/recovery grace has elapsed.
7. Multiple ASGI instances share the same registry via Postgres — no single-container Volume dependency.
8. Later object-storage for payloads can keep the same hash/FK contract ([REQ-02](../../requirements/REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md) territory).

### Operator GC trigger (pilot)

Runtime exposes `gc_unreferenced_bundles(registry, sessions, grace_seconds=…)` in `src/aibridge/bundle_gc.py`. **It is not called from the ASGI lifecycle** (`app.py`) in this pilot — no in-process cron.

| When | How |
|------|-----|
| Manual / ops job | Invoke the function (or a thin ops script wrapping it) against the shared registry + session store with `AIBRIDGE_BUNDLE_GC_GRACE_SECONDS` (default 86400). |
| Schedule | Operator-owned (cron / Railway cron / external job). Do **not** invent absolute paths or credentials here. |
| Safety | Skips hashes still referenced by **active** sessions; honors grace since `verified_at`. |

Default CI / unit coverage: `tests/test_bundle_gc.py`. Live Postgres GC is the same library against `PostgresBundleRegistry` / `PostgresSessionStore`.

---

## 5. Why this scales to new nodes

- Same code + image; new node = new verified bundle + env/secrets.
- No Python `if node == uus_veerenni`.
- Redeploy with a new bundle does not break in-flight sessions still pinned to older hashes (within TTL).

---

## 6. Verify surfaces

| Surface | Role |
|---------|------|
| Unit tests on loaders | Dev/CI |
| Startup register + `/readyz` | Current bundle + secrets + DB |
| Session resume path | Pinned bundle must exist |
| Façade smoke (V2) | Auth boundary |
| Contract tests | Channel OAS vs ASGI; wire OAS vs tool/wire validation |
