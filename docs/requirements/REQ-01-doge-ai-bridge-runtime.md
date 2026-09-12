# REQ-01: `doge-ai-bridge` — runtime service

**Parent (protocol):** [GPT UI REQ-47](../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md) — Responses → Story Intake HTTPS/Bearer channel  
**Index key:** REQ-01 (первый REQ профиля `aibridge`; исторически GPT UI REQ-47.1)  
**Service / repo:** `doge-ai-bridge`  
**Status:** Ready for implementation  
**Version:** 0.4.0 · 2026-09-12  
**Target path:** `doge-ai-bridge/docs/requirements/REQ-01-doge-ai-bridge-runtime.md`  
**Implementation language:** Python  
**Deployment target:** Railway-compatible Docker service  

**Related — Architecture:** [docs/architecture/runtime/00-overview.md](../architecture/runtime/00-overview.md) · [01-channel-facade](../architecture/runtime/01-channel-facade.md) · [02-content-packaging](../architecture/runtime/02-content-packaging.md) · [03-confirm-gateway](../architecture/runtime/03-confirm-gateway.md) · [04-ops-security](../architecture/runtime/04-ops-security.md)  
**Related — Tech-arch interview:** [docs/analysis/zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md](../analysis/zeya888.req-tech-arch-interview-REQ-01-doge-ai-bridge-runtime-2026-09-12.md)  
**Related — Runbook:** [docs/runbooks/channel-bearer-rotation.md](../runbooks/channel-bearer-rotation.md)  

---

## 1. Goal

Реализовать `doge-ai-bridge` — channel-neutral runtime, который:

1. принимает Telegram channel events от внешнего n8n workflow;
2. ведёт интервью через OpenAI Responses API;
3. загружает стабильный bundle поведенческих инструкций;
4. загружает активный node pack и канонический Story Intake OpenAPI;
5. генерирует strict function tool для allowlisted операции `postStoryDraftStash`;
6. владеет сессиями, revision/hash и dual-confirm policy;
7. не выполняет consequential HTTPS до отдельного Send confirmation;
8. собирает и валидирует `StoryDraftStashRequest`;
9. вызывает gateway `POST /story-drafts` с отдельным gateway Bearer;
10. возвращает n8n только безопасный текст, UI actions и bounded outcome;
11. после успешного stash возвращает SPA continuation URL.

`doge-ai-bridge` является protocol bridge, а не Telegram-ботом и не UI-приложением.

## 2. Canonical topology

```text
Resident ↔ Telegram
         ↔ n8n (Telegram UI + routing)
         ↔ doge-ai-bridge (Responses + state + confirm + validation)
         ↔ doge-complaints-gateway POST /story-drafts (gateway Bearer)
         ↔ SPA {DOGESTONIA_DRAFT_REDIRECT_BASE_URL}/#/story/submit?draft_id=
```

| Concern | Owner |
|---|---|
| Telegram webhook/trigger, messages, inline keyboards, callback acknowledgement | n8n |
| Responses API, prompt, tool loop, conversation state | `doge-ai-bridge` |
| Node pack injection and validation | `doge-ai-bridge` |
| Dual-confirm policy, nonce/hash/expiry/consume | `doge-ai-bridge` |
| Gateway URL, method and Bearer | `doge-ai-bridge` |
| Story draft stash | `doge-complaints-gateway` |
| Final review/submission | SPA |

### 2.1 Operator decisions

- One deployment = one node = one active pack.
- n8n is used as-is; no n8n fork and no custom node are required for this release.
- `doge-ai-bridge` does not own Telegram Bot API credentials.
- n8n never receives the gateway Bearer or OpenAI API key.
- n8n → aibridge uses Railway private networking plus a dedicated API Bearer.
- `origin.source` defaults to `openai_responses_telegram`.
- `stashed` never means Story created or published.
- Localhost SPA base is allowed only for the pilot when it is reachable by the resident device.

## 3. Scope

### 3.1 In scope

- Versioned channel HTTP façade for n8n.
- Channel Bearer authentication.
- PostgreSQL persistence and migrations.
- Per-session serialization and transactional state transitions.
- Telegram event deduplication.
- Responses API with `store: false` and self-managed replayable history.
- Deterministic instruction bundle assembly.
- Deterministic strict tool generation from OpenAPI + active pack.
- Dual-confirm and opaque action tokens.
- Pack/tool/wire validation.
- Constrained HTTPS/Bearer gateway execution.
- Best-effort local at-most-once behavior and explicit ambiguous outcome handling.
- Redacted audit, health/readiness and metrics.
- Unit, contract, concurrency, restart and E2E tests.

### 3.2 Out of scope

- Telegram polling/webhook implementation inside aibridge.
- n8n workflow JSON as source code of this service.
- Forking or patching n8n.
- Changing the Story Intake OpenAPI contract in this implementation.
- Creating or publishing a Story directly.
- Browser automation of SPA submission.
- Multi-pack selection inside one running process.
- Automatic retry after an ambiguous gateway outcome.
- Claiming strict distributed at-most-once semantics while gateway has no idempotency contract.
- User-facing DOGEstonia Identity authentication; this release trusts the authenticated channel principal supplied by n8n under channel service authentication.

## 4. Source-of-truth rules

| Material | SSOT |
|---|---|
| Channel rationale and parent framing | GPT UI REQ-47 |
| Gateway operation, request and response wire | Canonical Story Intake OpenAPI |
| Node-specific structured payload | Active pack `payload.schema.json` |
| Interview behavior | Root-level instruction bundle manifest |
| n8n → aibridge transport | Version-controlled `docs/openapi/aibridge-channel-v1.openapi.yaml`, constrained by §6 |

The channel façade is not a second Story Intake contract. It is a transport contract between n8n and aibridge.

The committed channel OpenAPI is contract SSOT. A live framework-generated `/openapi.json` may be exposed for diagnostics, but must be contract-tested against the committed schema and must not silently replace it.

## 5. Runtime components

| Component | Responsibility |
|---|---|
| `InstructionBundleLoader` | Load manifest-listed root files, normalize, hash and assemble stable prompt material. |
| `OpenApiLoader` | Read canonical YAML, resolve and hash it. |
| `OperationResolver` | Resolve exact allowlisted operation/method/path/security. |
| `ResponsesToolGenerator` | Produce deterministic strict Responses tool JSON. |
| `ConversationRepository` | Store replayable Responses items and session state. |
| `ChannelFacade` | Authenticate n8n and expose the two channel endpoints. |
| `TurnCoordinator` | Serialize turns and run the Responses loop. |
| `RequestAssembler` | Merge model-owned semantic data with server-owned constants. |
| `WireValidator` | Validate tool arguments, pack payload and final wire body. |
| `ConfirmationGuard` | Issue/hash/expire/invalidate/consume action tokens. |
| `GatewayExecutor` | Perform constrained HTTPS with gateway Bearer. |
| `OutcomeMapper` | Convert internal/gateway results to bounded outcomes. |
| `AuditLogger` | Emit redacted structured audit events and metrics. |

Components may use Python naming conventions but must remain independently testable.

## 6. Channel HTTP façade

### AIB-CH-01 — General protocol

- Base path: `/v1`.
- Content type: `application/json` only.
- Authentication: `Authorization: Bearer <channel-token>` on every `/v1/channel/*` request.
- Encoding: UTF-8.
- Telegram IDs are represented as decimal strings at the façade boundary.
- Unknown fields are rejected.
- Request bodies are size-bounded.
- CORS is disabled because this is server-to-server API.
- The façade binds to Railway `$PORT`; public exposure is not required.
- Error bodies never include secrets, prompts, raw backend bodies or stack traces.

### AIB-CH-02 — Process an ordinary message

```http
POST /v1/channel/turns
Authorization: Bearer <channel-token>
Content-Type: application/json
```

Request schema:

```json
{
  "channel": "telegram",
  "event_id": "telegram-update-id",
  "principal": {
    "user_id": "telegram-user-id",
    "chat_id": "telegram-chat-id"
  },
  "message": {
    "message_id": "telegram-message-id",
    "text": "resident message",
    "language_code": "ru"
  }
}
```

Rules:

- `channel` must equal `telegram` for this release.
- `event_id`, user/chat/message IDs and non-empty text are required.
- `language_code` is optional and untrusted; language is detected/confirmed by interview behavior.
- Timestamp, node ID, pack, operation ID and origin are server-owned and not accepted from n8n.
- Duplicate `event_id` for the same channel returns the stored response and does not call OpenAI twice.
- The active session is resolved by deployment/node + channel + user + chat.

### AIB-CH-03 — Process an inline-button callback

```http
POST /v1/channel/actions
Authorization: Bearer <channel-token>
Content-Type: application/json
```

Request schema:

```json
{
  "channel": "telegram",
  "event_id": "telegram-update-id",
  "callback_query_id": "telegram-callback-query-id",
  "principal": {
    "user_id": "telegram-user-id",
    "chat_id": "telegram-chat-id"
  },
  "action_token": "opaque-token-from-callback-data"
}
```

Rules:

- n8n must call Telegram `answerCallbackQuery` promptly; aibridge does not call Telegram.
- `action_token` is the only value copied from Telegram `callback_data`.
- Action name, draft, revision, session and secrets are not encoded in callback data.
- Duplicate `event_id` returns the stored response.
- The token record determines the action and must match the supplied user/chat.
- Invalid, expired, cancelled, consumed or foreign tokens fail closed.

### AIB-CH-04 — Common successful response

Both endpoints return this bounded envelope:

```json
{
  "request_id": "bridge-generated-id",
  "session_id": "opaque-session-reference",
  "state": "interviewing",
  "reply_text": "text for Telegram",
  "callback_ack_text": null,
  "actions": [
    {
      "label": "Send to DOGEstonia",
      "token": "opaque-one-time-token",
      "style": "primary"
    }
  ],
  "outcome": null,
  "draft_id": null,
  "continuation_url": null
}
```

Contract rules:

- `actions` may be empty.
- `style` is presentation guidance only: `primary`, `success`, `danger` or `default`.
- n8n puts only `actions[].token` into `callback_data`.
- Only `outcome=stashed` may include `draft_id` and `continuation_url`.
- `reply_text` is resident-safe and must not claim publication after stash.
- `session_id` is not an authorization credential.
- n8n must not be required to interpret internal state to enforce security.

### AIB-CH-05 — HTTP statuses

| HTTP | Meaning |
|---:|---|
| 200 | Event processed or safely replayed from event dedupe |
| 400 | Malformed request or unknown field |
| 401 | Missing/invalid channel Bearer |
| 403 | Principal does not own the referenced token/session |
| 404 | Action/session reference unavailable |
| 409 | Expired/consumed/invalidated token or invalid state transition |
| 413 | Request body too large |
| 422 | Semantically invalid channel input |
| 429 | Channel rate limit |
| 500 | Internal bridge failure with redacted body |
| 503 | Not ready or required dependency unavailable |

All non-2xx responses use:

```json
{
  "request_id": "bridge-generated-id",
  "error": {
    "code": "bounded_machine_code",
    "message": "resident-safe or operator-safe message",
    "retryable": false
  }
}
```

### AIB-CH-06 — n8n mapping

The expected no-fork workflow is:

```text
Telegram Trigger
  → Switch
      message
        → HTTP Request POST /v1/channel/turns
        → Telegram Send Message (+ inline actions if returned)
      callback_query
        → Telegram Answer Callback Query
        → HTTP Request POST /v1/channel/actions
        → Telegram Send/Edit Message (+ replacement actions if returned)
```

The same n8n Header Auth credential is used for both HTTP Request nodes. n8n must never call `POST /story-drafts` directly.

## 7. Channel authentication

### AIB-AUTH-01 — Dedicated opaque Bearer

- Environment variable: `AIBRIDGE_CHANNEL_BEARER_TOKEN`.
- Token is distinct from gateway Bearer and OpenAI key.
- Generate with a CSPRNG; minimum 256 bits of entropy.
- Compare using a constant-time primitive.
- Return a generic 401 for missing and invalid credentials.
- Never log or return the `Authorization` header.
- Store the raw value only as a Railway secret environment variable; local `.env` is development-only and gitignored.
- n8n stores the same value only in a Header Auth credential.
- Token rotation must allow a short, explicit overlap window using current and previous token, then remove the previous token.

### AIB-AUTH-02 — Network boundary

- n8n calls the Railway private hostname and internal port.
- The façade rejects missing Bearer even on the private interface.
- Public domain creation for aibridge is not required for the pilot.
- If the channel crosses an untrusted network later, TLS or mTLS becomes mandatory.
- Rate limits apply per channel principal and globally per channel credential.

## 8. Instruction bundle

### AIB-INS-01 — Included material

- Source: `GPT UI/instructions` root directory.
- Load only files explicitly listed by `instructions.manifest.json`.
- Listed files must be direct children of the configured root.
- Do not recursively traverse nested directories.
- Do not include onboarding or archive content.
- Do not treat schema-pack JSON/YAML files as behavioral instructions.
- Node-specific schemas and configuration are loaded separately as active pack material.

### AIB-INS-02 — Manifest

The manifest defines version and exact order, for example:

```json
{
  "bundle_version": "module1-v1",
  "files": [
    "first-root-instruction.md",
    "second-root-instruction.md"
  ]
}
```

The actual filenames are supplied by the content repository and must not be guessed by runtime.

### AIB-INS-03 — Deterministic assembly

- Normalize text to UTF-8 and LF line endings.
- Reject duplicate, missing, empty, absolute or parent-traversal paths.
- Reject manifest paths containing directory separators for this release.
- Concatenate in manifest order using one stable separator.
- Compute SHA-256 for every file and the assembled bundle.
- Log only version/hash metadata, not full instruction text.
- A running session remains pinned to the instruction/tool/pack version with which it started.
- Changing bundle/pack/tool version starts a new session or executes an explicit migration; silent mid-session replacement is forbidden.

### AIB-INS-04 — Delivery into Docker

- Runtime does not fetch mutable instructions from GitHub at request time.
- Build/release pipeline supplies an immutable content bundle pinned to source commit SHA.
- Docker image or read-only deployment artifact contains the manifest, instruction files, OpenAPI and pack files.
- Startup records source commit, bundle hash, OAS hash and pack hash.
- Missing/mismatched artifacts make readiness fail.

## 9. OpenAPI reuse and strict tool generation

### AIB-OAS-01 — Canonical operation

At startup resolve exactly one allowlisted operation:

```text
operationId = postStoryDraftStash
method      = POST
path        = /story-drafts
```

Fail readiness unless the operation is unique, uses JSON, declares HTTP Bearer and declares success `201`.

### AIB-OAS-02 — Two schema views

1. Wire validator uses the canonical OpenAPI request semantics.
2. Responses tool schema is a deterministic strict JSON Schema projection.

No manually maintained duplicate of `StoryDraftStashRequest` is allowed.

### AIB-GEN-01 — Strict conversion

- Dereference supported `$ref` values.
- Map nullable fields to JSON Schema type unions with `null`.
- Remove OpenAPI-only keywords unsupported by Responses strict tools.
- Set `additionalProperties: false` on every object.
- Put every property in `required`; optional values use nullable types.
- Validate generated schema before accepting traffic.
- Unsupported constructs fail build/startup; no silent non-strict fallback.
- Tool name, description, schema serialization and order are deterministic.

### AIB-GEN-02 — Pack projection

- Replace open `structured_payload` in the model-facing tool only with the active pack `payload.schema.json`.
- Wire validation still uses canonical OpenAPI.
- Fail startup on schema ID/version/hash mismatch.
- Do not hardcode `uus_veerenni_civic` in reusable runtime code.

### AIB-GEN-03 — Server-owned fields

The model and n8n cannot set or override:

- envelope schema version;
- pack schema ID/version;
- `origin.source`;
- gateway URL, method or path;
- headers or credentials;
- timestamps, audit IDs or idempotency references.

### AIB-GEN-04 — Null pruning

Before wire validation, omit nulls only for fields that the OpenAPI treats as omit-optional. Never prune `false`, `0`, valid empty arrays or required values.

## 10. Responses API and conversation state

### AIB-RSP-01 — Privacy/state mode

- Every Responses request sets `store: false`.
- Do not create OpenAI Conversation objects in this release.
- Do not depend on `previous_response_id`; continuation is rebuilt from locally stored replayable items.
- Aibridge stores the replayable conversation history in PostgreSQL.
- Preserve all required Responses output items, not only visible assistant text.
- Where the chosen reasoning model requires it, request and retain replayable encrypted reasoning content without logging or displaying it.
- Model input is rebuilt deterministically from the pinned stable prefix plus stored replayable history.
- Session history has explicit retention and deletion rules.

### AIB-RSP-02 — Turn serialization

- At most one active Responses turn per session.
- Concurrent Telegram events for one session are serialized using a database-backed lock or equivalent transactional mechanism.
- Duplicate channel event does not create a second Responses call.
- A failed turn cannot silently advance the stored conversation pointer/history.
- Request cancellation and process shutdown leave the session in a recoverable explicit state.

### AIB-RSP-03 — Tool availability lifecycle

1. During ordinary interview turns, consequential execution is disabled.
2. Bridge produces a draft interpretation summary and an interpretation-confirm action.
3. Interpretation confirmation records approval but does not authorize gateway HTTPS.
4. After interpretation confirmation, the model may emit one `postStoryDraftStash` `function_call` as a pending intent.
5. Bridge validates and assembles the proposed body, freezes its canonical revision/hash and stores the original `call_id` and replayable output items.
6. Bridge creates Send/Edit/Cancel action tokens and returns them to n8n.
7. Send action atomically verifies and consumes authorization, then executes the stored confirmed intent.
8. Bridge submits bounded `function_call_output` with the original `call_id` and continues the Responses turn.

A `function_call` is an intent, not permission to execute. No network side effect occurs before step 7.

### AIB-RSP-04 — Tool-call constraints

- Accept only `type=function_call` with the exact allowlisted name.
- Set `parallel_tool_calls: false` where supported.
- Reject malformed arguments, unknown names, duplicate/unknown call IDs and more than one consequential call per turn.
- A tool call before the permitted state is blocked and cannot reach `GatewayExecutor`.
- The stored canonical body/hash, not newly regenerated arguments, is the Send-confirm target.
- Every `function_call_output` uses the original `call_id`.

### AIB-RSP-05 — Output safety

- Model text cannot override state transitions or claim backend success.
- System-generated outcome text takes precedence for consequential results.
- Only validated `stashed` outcome permits a continuation URL.
- Usage metadata is recorded without narrative content.

## 11. Prompt caching

### AIB-CACHE-01 — Stable prefix

The rendered request order is stable:

1. model/tool-affecting stable settings;
2. deterministic tool definitions;
3. assembled instruction bundle;
4. stable pack reference material permitted for the model;
5. dynamic session history and current user input.

Do not place timestamps, user IDs, session IDs or other dynamic content before the stable cache boundary.

### AIB-CACHE-02 — Breakpoints and capability detection

- Use explicit cache breakpoint after stable material when supported by the selected model/API.
- Otherwise preserve an exact stable prefix and use supported implicit caching behavior.
- Do not assume identical caching parameters across models.
- Model change requires cache compatibility verification.
- Do not pad a short prompt with useless content merely to reach a cache threshold.

### AIB-CACHE-03 — Observability

Record per request:

- total input/output tokens;
- cached input tokens;
- cache-write tokens when exposed;
- bundle/tool/pack hashes;
- model and relevant request settings;
- latency and estimated cost where configured.

Acceptance is based on measured cache reuse, not only byte-stable local serialization.

## 12. Request assembly and validation

### AIB-REQ-01 — Server constants

```text
schema_version                = m2.story_intake_envelope.v2
schema_binding.schema_id      = DOGESTONIA_SCHEMA_ID
schema_binding.schema_version = DOGESTONIA_SCHEMA_VERSION
origin.source                 = DOGESTONIA_ORIGIN_SOURCE
```

Pilot pack may be `uus_veerenni_civic` / `v3`, but runtime remains config-driven.

### AIB-REQ-02 — Three validation gates

1. Function arguments against strict tool schema.
2. `structured_payload` against active pack schema.
3. Final assembled body against canonical wire schema.

Model assertions such as “validation passed” have no authority.

### AIB-REQ-03 — Canonical draft hash

- Canonicalize the complete server-assembled semantic draft using a documented deterministic JSON serialization.
- Include operation ID, schema binding and revision in the hash domain.
- Use SHA-256.
- Any content-affecting edit increments revision and invalidates pending action tokens.
- Presentation-only changes that do not alter the canonical request do not create a new revision.

## 13. Dual-confirm and action tokens

### AIB-CONF-01 — Two human decisions

- **Interpretation confirm:** “You understood my draft.” It never authorizes gateway HTTPS.
- **Send confirm:** “Send to DOGEstonia.” Only it may authorize gateway HTTPS.

The actions must be distinct in state, audit and UI.

### AIB-CONF-01A — Canonical session states

The implementation must use an explicit finite state machine equivalent to:

```text
interviewing
awaiting_interpretation_confirm
interpretation_confirmed
awaiting_send_confirm
executing
stashed
cancelled
unknown_outcome
failed
```

Permitted transitions are declared centrally and tested. Handlers must not assign arbitrary states. In particular:

- `awaiting_interpretation_confirm → interpretation_confirmed` performs no gateway HTTP;
- `interpretation_confirmed → awaiting_send_confirm` requires a validated frozen tool intent;
- `awaiting_send_confirm → executing` requires a valid Send token;
- `executing → stashed` requires the verified 201 contract;
- any content edit returns to `interviewing`, increments revision and invalidates existing actions;
- `unknown_outcome` cannot transition back to `executing` automatically.

### AIB-CONF-02 — Token construction

- Generate one separate opaque token per offered action.
- Use at least 128 bits of CSPRNG entropy; recommended 256 bits.
- Use URL-safe encoding no longer than 64 UTF-8 bytes for Telegram `callback_data`.
- Store only a cryptographic hash of the raw action token.
- Return the raw token once to n8n.
- Token record binds action, node/deployment, session, user, chat, operation, revision/hash, issue/expiry time and state.
- Token never contains Bearer, draft content, action name or signed client-controlled JSON.

### AIB-CONF-03 — State verification

Before applying an action, atomically verify:

- channel and deployment;
- user/chat ownership;
- token hash;
- expiry;
- expected session state;
- operation ID;
- current draft revision/hash;
- not cancelled, invalidated or consumed.

Send token transitions `pending_send → executing` in the same transaction that consumes it.

### AIB-CONF-04 — Edit and Cancel

- Edit invalidates every pending action for the old revision and returns the session to interview mode.
- Cancel invalidates pending actions and records a non-success terminal/cancelled state.
- New content never inherits an old Send confirmation.
- Replayed callback returns the recorded bounded result and never repeats the gateway call.

## 14. Persistence model

### AIB-DB-01 — PostgreSQL requirement

Production/pilot runtime uses PostgreSQL, not process memory, for security state.

Persist at minimum:

- sessions and pinned content/tool/pack versions;
- replayable Responses items;
- draft revisions and canonical hashes;
- action-token hashes and state;
- channel events and stored responses;
- tool call IDs and frozen arguments/body;
- gateway attempts and outcomes;
- redacted audit references.

### AIB-DB-02 — Isolation

- Prefer a dedicated Railway PostgreSQL service/database.
- Sharing a PostgreSQL server is allowed only with separate database/schema and least-privilege credentials.
- Do not use n8n application tables as aibridge storage.
- Database migrations are versioned and run through an explicit deployment step.

### AIB-DB-03 — Required uniqueness

Database constraints must prevent:

- duplicate `(channel, event_id)` processing;
- duplicate active action token hash;
- more than one recorded gateway execution attempt for the same locally authorized revision unless an explicit operator reconciliation transition permits otherwise;
- duplicate tool `call_id` within a session.

Application checks alone are insufficient; concurrency tests must exercise database constraints.

### AIB-DB-04 — Retention

- Session, narrative and Responses item retention is configured.
- Expired action tokens are retained only as long as required for replay/audit, then deleted or irreversibly minimized.
- Provide an operator mechanism to delete a resident session and associated narrative data.
- Audit retention is separate and contains no full narrative by default.

## 15. Gateway HTTPS execution

### AIB-HTTP-01 — Constrained destination

- Resolve gateway method/path from the canonical operation at startup.
- Allow exact configured HTTPS origin only.
- TLS certificate verification is mandatory.
- No arbitrary redirects; redirects are disabled by default.
- Fixed JSON POST to `/story-drafts`.
- Explicit connect/total timeouts and request/response size limits.
- Model, n8n and backend response cannot change destination or headers.

### AIB-HTTP-02 — Gateway Bearer

- Read only from `DOGESTONIA_API_BEARER_TOKEN`.
- Inject only inside `GatewayExecutor` as `Authorization: Bearer …`.
- Never place it in Responses input/tools/output, channel requests, n8n credentials, URLs, exceptions or logs.
- It must differ from `AIBRIDGE_CHANNEL_BEARER_TOKEN`; equality fails readiness.

### AIB-HTTP-03 — Success verification

Treat the operation as `stashed` only when:

- HTTP status is 201;
- response is valid bounded JSON;
- `data.draft_id` is a non-empty valid value;
- `trace_id` is non-empty.

Anything else is not success.

### AIB-HTTP-04 — Gateway outcome mapping

| Condition | Outcome |
|---|---|
| Valid 201 contract | `stashed` |
| 400 | `validation_error` |
| Gateway 401 | `gateway_unauthorized` |
| 422 | `geo_scope_mismatch` |
| 429 or explicit retry-safe pre-send failure | `transient_failure` |
| 5xx before a body can be accepted as success | `transient_failure` or `unknown_outcome` according to attempt state |
| Timeout/disconnect after request may have reached gateway | `unknown_outcome` |
| Malformed 201 | `contract_mismatch` |
| Internal exception before send | `internal_bridge_error` |
| No valid Send confirmation | `blocked_by_confirmation` |

Bounded outcomes are:

```text
stashed
validation_error
gateway_unauthorized
geo_scope_mismatch
transient_failure
unknown_outcome
contract_mismatch
blocked_by_confirmation
internal_bridge_error
cancelled
```

### AIB-HTTP-05 — Idempotency boundary

The gateway currently has no confirmed server-side idempotency contract. Therefore:

- aibridge performs local event and revision dedupe;
- no automatic retry is allowed once a request may have reached gateway;
- ambiguous delivery becomes terminal `unknown_outcome` pending operator reconciliation;
- UI must not offer an automatic Send retry for that same revision;
- local behavior is documented as best-effort at-most-once, not strict distributed at-most-once;
- strict `≤1 draft per revision` becomes possible only after gateway adds an idempotency key, unique client operation ID or authoritative outcome lookup.

If gateway gains such a contract, adopting it requires a separate reviewed protocol change and contract tests.

## 16. Continuation URL

Build only after verified `stashed`:

```text
{DOGESTONIA_DRAFT_REDIRECT_BASE_URL}/#/story/submit?draft_id={url-encoded-draft-id}
```

Rules:

- Base origin comes only from environment configuration.
- `draft_id` comes only from validated gateway response.
- No other query parameters are copied from model/n8n/backend text.
- Return `continuation_url` only together with `outcome=stashed`.
- Resident copy says the draft was saved/stashed for review, not published.

## 17. Configuration

| Variable | Required | Meaning |
|---|---:|---|
| `PORT` | yes | Railway-provided listening port |
| `DATABASE_URL` | yes | Aibridge PostgreSQL connection |
| `OPENAI_API_KEY` | yes | OpenAI project/service credential |
| `OPENAI_MODEL` | yes | Responses-compatible model |
| `OPENAI_STORE_RESPONSES` | yes | Must be `false` in this release |
| `DOGESTONIA_INSTRUCTIONS_DIR` | yes | Root-level instruction bundle path |
| `DOGESTONIA_INSTRUCTIONS_MANIFEST` | yes | Explicit ordered manifest path |
| `DOGESTONIA_CONTENT_SOURCE_COMMIT` | yes | Pinned source commit/release ID |
| `DOGESTONIA_OPENAPI_PATH` | yes | Canonical Story Intake YAML |
| `DOGESTONIA_OPERATION_ID` | yes | `postStoryDraftStash` |
| `DOGESTONIA_PAYLOAD_SCHEMA_PATH` | yes | Active pack payload schema |
| `DOGESTONIA_SCHEMA_ID` | yes | Active pack ID |
| `DOGESTONIA_SCHEMA_VERSION` | yes | Active pack version |
| `DOGESTONIA_ORIGIN_SOURCE` | yes | Default `openai_responses_telegram` |
| `DOGESTONIA_API_BASE_URL` | yes | Exact approved HTTPS gateway origin |
| `DOGESTONIA_API_BEARER_TOKEN` | yes | Gateway Bearer; bridge only |
| `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` | yes | SPA base origin |
| `AIBRIDGE_CHANNEL_BEARER_TOKEN` | yes | n8n → aibridge Bearer |
| `AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN` | no | Temporary rotation overlap only |
| `AIBRIDGE_MAX_REQUEST_BYTES` | yes | Channel body limit |
| `AIBRIDGE_MAX_RESPONSE_BYTES` | yes | Gateway response limit |
| `AIBRIDGE_SESSION_TTL_SECONDS` | yes | Inactive session retention/expiry |
| `AIBRIDGE_ACTION_TOKEN_TTL_SECONDS` | yes | Confirmation token lifetime |
| `AIBRIDGE_HTTP_CONNECT_TIMEOUT_MS` | yes | Gateway connect timeout |
| `AIBRIDGE_HTTP_TOTAL_TIMEOUT_MS` | yes | Gateway total timeout |
| `AIBRIDGE_LOG_LEVEL` | yes | Structured log level |
| `AIBRIDGE_DRY_RUN` | no | Validate without gateway execution; default false |

`TELEGRAM_BOT_TOKEN` is not an aibridge variable in the n8n topology.

## 18. Startup, health and shutdown

### AIB-OPS-01 — Startup validation

Fail readiness when any of the following is invalid:

- database connectivity/migration version;
- channel or gateway Bearer missing or equal;
- OpenAI key/model configuration;
- `OPENAI_STORE_RESPONSES` is not false;
- instruction manifest/files/hash;
- OpenAPI or operation resolution;
- generated tool strictness;
- pack identity/schema/hash;
- non-HTTPS gateway origin;
- declared 201 response contract;
- redirect base syntax.

### AIB-OPS-02 — Health endpoints

- `GET /healthz`: process liveness only; no secrets/config dump.
- `GET /readyz`: readiness of required startup invariants and critical dependencies.
- Health endpoints do not require channel Bearer but expose only minimal status and must not expose dependency URLs or credentials.

### AIB-OPS-03 — Graceful shutdown

- Stop accepting new turns.
- Finish or explicitly mark in-flight database transactions.
- Never automatically repeat an in-flight gateway attempt after restart.
- Preserve enough attempt state to return `unknown_outcome` when delivery was ambiguous.

## 19. Security and audit

### AIB-SEC-01 — Trust boundaries

Treat as untrusted:

- Telegram text and metadata;
- n8n request fields except authentication of the channel service;
- model text and function arguments;
- YAML descriptions;
- gateway error bodies.

None may override configuration, allowlists, pack identity, auth, destination, confirmation policy or audit redaction.

### AIB-SEC-02 — Logging

Allowed by default:

- request/session/event references;
- hashed principal reference;
- operation and artifact hashes;
- Responses ID/call ID where policy permits;
- confirmation state/action reference;
- HTTP status, gateway trace ID, duration and bounded outcome;
- cache/token usage metrics.

Forbidden by default:

- Bearer tokens and API keys;
- `Authorization` headers;
- raw action tokens;
- full resident narrative;
- full model prompt/history;
- full gateway error body;
- stack traces in channel responses.

### AIB-SEC-03 — Defensive controls

- Constant-time channel-token comparison.
- Cryptographic action-token generation and hashed storage.
- Parameterized SQL/ORM and least-privilege DB credentials.
- Request/rate/timeout/response bounds.
- No CORS and no arbitrary outbound URL.
- Dependency versions pinned and security scanning in CI.
- Secrets redaction tests.
- Production debug mode disabled.

## 20. Testing requirements

### 20.1 Unit tests

- instruction manifest/path/order/normalization/hash;
- OpenAPI `$ref` resolution and operation allowlist;
- strict schema conversion and unsupported-keyword failure;
- pack projection and mismatch;
- null pruning without pruning false/zero/valid empty arrays;
- canonical draft serialization/revision/hash;
- channel Bearer comparison and redaction;
- action token generation/hash/expiry/ownership;
- outcome mapping;
- continuation URL encoding;
- prompt stable-prefix serialization.

### 20.2 Contract tests

- façade request/response schema snapshots;
- unknown fields and oversized bodies;
- missing/invalid channel Bearer;
- duplicate Telegram `event_id` returns stored response;
- minimum/maximum valid pack payload;
- malformed/unknown tool call and wrong `call_id`;
- `parallel_tool_calls: false` request configuration where supported;
- valid/malformed 201 and 400/401/422/429/5xx mapping;
- callback token encoded length ≤64 bytes;
- gateway and channel Bearers accidentally equal → readiness failure;
- `store: false` on every Responses request.

### 20.3 Concurrency and restart tests

- two simultaneous Send callbacks execute at most one local gateway attempt;
- simultaneous messages in one session are serialized;
- callback from another user/chat is rejected;
- callback after expiry/Edit/Cancel is rejected;
- restart between pending and Send preserves pending state;
- restart during gateway request never causes automatic resend;
- gateway accepted request but response was lost → `unknown_outcome`;
- database uniqueness wins over racing application processes;
- graceful shutdown preserves recoverable state.

### 20.4 E2E tests

- n8n/test-double ordinary message → interview reply;
- interpretation confirm produces no gateway HTTP;
- confirmed interpretation → pending tool intent → Send/Edit/Cancel actions;
- Send with correct owner/revision performs one gateway attempt;
- Edit invalidates Send token;
- valid 201 → `stashed` + `draft_id` + continuation URL;
- failures never produce success/publication text;
- Russian, Estonian and English resident-safe paths;
- pack swap requires new deployment/session version and no hardcoded civic fields;
- instruction prefix cache telemetry is present.

## 21. Acceptance criteria

- [ ] Two versioned channel endpoints are implemented exactly as §6.
- [ ] n8n can integrate using two HTTP Request nodes without custom code or platform fork.
- [ ] Channel Bearer is required and distinct from gateway Bearer.
- [ ] PostgreSQL persists sessions, events, action tokens, tool intents and outcomes.
- [ ] Event dedupe and session serialization work across concurrent instances.
- [ ] Responses uses `store: false` and self-managed replayable history.
- [ ] Root-only manifest instructions are deterministic, pinned and hashed.
- [ ] Canonical OpenAPI remains the only Story Intake wire SSOT.
- [ ] Generated tool is deterministic and strict.
- [ ] `parallel_tool_calls` is disabled for the consequential tool flow where supported.
- [ ] Active pack schema is injected in model projection and validated independently.
- [ ] Server-owned fields cannot be overridden by model or n8n.
- [ ] Interpretation confirmation produces no gateway request.
- [ ] Send confirmation is bound to principal, session, operation, revision/hash, nonce and expiry.
- [ ] Telegram callback payload contains only an opaque token ≤64 bytes.
- [ ] Edit/Cancel/expiry invalidate prior Send authorization.
- [ ] Gateway destination/method/path/auth are constrained and TLS-verified.
- [ ] Ambiguous gateway delivery becomes `unknown_outcome` with no automatic retry.
- [ ] Strict distributed at-most-once is not claimed without gateway support.
- [ ] Only valid 201 with `draft_id` and `trace_id` becomes `stashed`.
- [ ] `contract_mismatch` is part of the bounded outcome vocabulary.
- [ ] Stash text never claims Story creation or publication.
- [ ] Prompt cache behavior is measured through usage telemetry.
- [ ] Startup/readiness fail closed on invalid artifacts, secrets or dependencies.
- [ ] Unit, contract, concurrency, restart and E2E suites pass.

## 22. Deliverables

1. Python application and Dockerfile.
2. Version-controlled `docs/openapi/aibridge-channel-v1.openapi.yaml` matching §6, plus runtime contract test.
3. `InstructionBundleLoader` and manifest validation.
4. Canonical OpenAPI loader and operation resolver.
5. Strict tool generator and snapshots.
6. PostgreSQL models and versioned migrations.
7. Conversation/session repository.
8. Turn coordinator and Responses tool loop.
9. Confirmation guard and action-token repository.
10. Request assembler and three validation gates.
11. Constrained gateway executor.
12. Outcome/error mapper.
13. Health/readiness endpoints and graceful shutdown.
14. Redacted audit and metrics.
15. `.env.example` containing names/placeholders only.
16. Unit, contract, concurrency, restart and E2E tests.
17. Validated `instructions.manifest.json` supplied with the immutable content bundle.
18. Operator README covering Railway private networking, n8n mapping, secret generation/rotation, migrations, rollback and reconciliation.

Explicitly not delivered: Telegram bot process, n8n fork/custom node, committed n8n workflow JSON or gateway idempotency extension.

## 23. References

- OpenAI Function calling: <https://developers.openai.com/api/docs/guides/function-calling>
- OpenAI Conversation state: <https://developers.openai.com/api/docs/guides/conversation-state>
- OpenAI Prompt caching: <https://developers.openai.com/api/docs/guides/prompt-caching>
- Telegram Bot API, inline keyboard: <https://core.telegram.org/bots/api#inlinekeyboardbutton>
- Telegram Bot API, callback acknowledgement: <https://core.telegram.org/bots/api#answercallbackquery>
- n8n HTTP Request node: <https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.httprequest/>

## 24. History

- v0.3.0 — n8n selected as external UI; bridge owns Responses/tools/confirmation/gateway.
- v0.3.1 — private network + application authentication selected.
- v0.3.2 — channel authentication standardized on API Bearer.
- v0.4.0 — implementable channel façade; PostgreSQL state; `store:false`; deterministic instruction manifest; transactional dual-confirm; Telegram callback limits; explicit idempotency boundary; operations, security and expanded tests.

---

*End of REQ-01 v0.4.0*
