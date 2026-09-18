# TRACEABILITY MATRIX — QA inbound/outbound data flow

**Persistent copy** (ops/QA zone): synced from package 2026-09-18T12:42:35Z (N8N-WF-001 deferred + stories 36–40).  
**Package source (SSOT):** [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md)  
**Parent SSOT (guide):** [`../../tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md)  
**Package INDEX:** [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md)  
**Purpose:** Stable IDs from guide §10–11, §15–16 mapped to backlog stories.


| ID | Scenario | Expected | Story key | Coverage |
|----|----------|----------|-----------|----------|
| AUTH-001 | Valid current Channel Bearer on `/turns` | Request reaches validation/processing. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-002 | Valid previous Channel Bearer during rotation | Accepted. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-003 | Missing Authorization | 401 `unauthorized`, redacted body. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-004 | Wrong scheme, e.g. `Basic` | 401. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-005 | `Bearer` without value | 401. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-006 | Wrong token of same length | 401. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-007 | Wrong token of different length | 401 without timing-dependent functional difference. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-008 | Gateway Bearer supplied to channel endpoint | 401 unless misconfigured equal; readiness must reject equality. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-009 | Channel Bearer appears in logs/metrics/error | Fail test; secret must be absent. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-010 | `/healthz` without Bearer | 200 `{"status":"ok"}`. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-011 | `/readyz` without Bearer | 200 ready or 503 bounded reason; no generation/write. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| AUTH-012 | `/metrics` from allowed private test network | Prometheus text; no PII/secrets. | `STORY-AIBRIDGE-23-qa-auth-ops-boundaries` | covered |
| VAL-001 | Valid `/turns` body | 200 bounded success. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-002 | Valid `/actions` body | 200 or token-domain 403/404/409. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-003 | Malformed JSON | 400 `bad_request`. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-004 | Invalid UTF-8 body | 400 `bad_request`. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-005 | Unknown top-level field | 400 `bad_request`. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-006 | Unknown nested field | 400 `bad_request`. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-007 | Missing required field | 422 `semantic_invalid`. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-008 | `channel` other than `telegram` | 422. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-009 | Empty `event_id` | 422. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-010 | Numeric Telegram ID instead of string | 422. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-011 | Non-decimal `user_id`, `chat_id`, or `message_id` | 422. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-012 | Negative group `chat_id` decimal string | Accepted. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-013 | Empty message text | 422. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-014 | Whitespace-only message | Characterization: currently passes min-length; record result and open product decision if trimming is required. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-015 | Action token length 65 | 422. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-016 | Body exceeds `AIBRIDGE_MAX_REQUEST_BYTES` | 413 `payload_too_large`; no OpenAI/DB side effect beyond request handling. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-017 | Invalid/negative Content-Length | 400 bounded error. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| VAL-018 | Missing `Content-Type` but valid JSON | Characterization test; OAS requires JSON even if current parser accepts raw body. | `STORY-AIBRIDGE-24-qa-json-schema-boundary` | covered |
| N8N-001 | Private text message | Correct `/turns` mapping; one reply. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-002 | `/start` command | Sent as ordinary text; model/instructions decide response. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-003 | Russian text | Unicode preserved; language hint optional. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-004 | Estonian text | Unicode preserved. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-005 | Mixed-language message | Text unchanged; hint must not override actual content. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-006 | Emoji and combining characters | Round-trip without corruption. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-007 | Group message from user A | Principal = A + group chat. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-008 | Same group message from user B | Separate session. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-009 | Edited message update | Must not be silently treated as a new ordinary message unless workflow explicitly supports it. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-010 | Photo/document/voice without text | Do not build invalid `/turns`; route to explicit unsupported-content response or future adapter. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-011 | Media with caption | Product decision/characterization: caption may be mapped as text only if workflow explicitly documents it. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-012 | Channel post, poll, shipping/pre-checkout update | Must not enter this workflow branch. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-013 | Callback query | `answerCallbackQuery` occurs before `/actions`. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-014 | aibridge slow/unavailable after callback | Telegram callback still acknowledged promptly; later resident-safe error handling. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-015 | `actions=[]` | No inline keyboard added. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-016 | Three actions | Labels/tokens mapped in order; token unchanged. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-017 | `outcome=stashed` | Render continuation link; do not claim publication. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-018 | Non-stashed outcome with accidental draft/URL | Adapter should not present link; contract test should fail producer inconsistency. | `STORY-AIBRIDGE-25-qa-n8n-telegram-mapping` | fixture-covered (runtime honesty → STORY-36 / N8N-WF-001) |
| N8N-WF-001 | n8n workflow export pin + Layer E honesty | Pinned export matches pilot workflow; `tests/n8n/` labeled adapter-contract; optional out-of-CI smoke | `STORY-AIBRIDGE-36-qa-n8n-workflow-contract-honesty` | deferred (export absent · capture-first · no invent body; Layer E adapter-contract labeled; out-of-CI checklist bound) |
| IDEM-001 | Same `/turns` request and same event ID twice | Same stored response; one OpenAI call. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-002 | Retry uses new event ID | Demonstrate why this is wrong: second OpenAI call; n8n test must prevent it. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-003 | Same event ID but different body | First stored result wins; no second side effect; log safe collision signal if implemented. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-004 | Two concurrent identical turns | One claim/one OpenAI call; second waits/replays or receives bounded in-flight response. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-005 | OpenAI exception after dedupe claim | Claim aborted; a safe retry can process again. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-006 | Same callback update retried | Same stored `/actions` envelope; token not executed twice. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-007 | Two concurrent Send callbacks with different update IDs but same token | Exactly one consumes token/attempts gateway; other gets conflict. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-008 | Two different messages for same session concurrently | Serialized by session lock; history order deterministic. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-009 | Messages for different sessions concurrently | May proceed independently; no global serialization. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| IDEM-010 | `/turns` and `/actions` accidentally reuse same channel/event ID | Dedupe namespace collision is safely replayed; workflow must use genuine unique Telegram update IDs. | `STORY-AIBRIDGE-26-qa-idempotency-concurrency` | covered |
| OAI-001 | Ordinary text response | 200, visible reply, interpretation buttons on first interviewing response. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-002 | Empty output array | Bounded fallback text; no crash. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-003 | Output containing `Received:` stub | Stub not echoed; mapped to `Acknowledged.`. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-004 | Valid cached token usage | Cache metric records value. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-005 | `store` attempted true by config | Startup/settings or readiness fails closed. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-006 | Both stable prefix and `instructions` used | Fail test; mutually exclusive. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-007 | Parallel tool calls requested | Fail test; must be false. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-008 | OpenAI 429 | Transport `RATE_LIMITED`; channel **429** `rate_limited` retryable (CHAR-006 Option A); no secret/raw; no gateway. Distinct from client middleware RL. | `STORY-AIBRIDGE-38-qa-oai-channel-error-outcome` · suite STORY-27 | covered |
| OAI-009 | OpenAI 5xx | Transport `TRANSIENT_FAILURE`; channel **503** `transient_failure` retryable (CHAR-006 Option A); no gateway. | `STORY-AIBRIDGE-38-qa-oai-channel-error-outcome` · suite STORY-27 | covered |
| OAI-010 | OpenAI timeout | Bounded 500 `internal_error`, `retryable=true`; dedupe claim aborted so message retry can run. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-011 | Invalid OpenAI JSON/body | Bounded error, no history corruption or gateway. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-012 | Input/output/call/turn budget breach | No gateway; last confirmed state preserved; resident-safe rejection. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-013 | Malicious prompt asks to reveal instructions/tokens | No secret or system prompt disclosure in output/logs. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-014 | User text contains JSON/tool-looking syntax | Treated as user content, not trusted function call. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-015 | Stable prefix across two sessions | Identical prefix bytes/hash for same bundle/model/tool/pack. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| OAI-016 | Content bundle changes | New deployment/session uses new pinned bundle; active pinned session behavior follows bundle retention policy. | `STORY-AIBRIDGE-27-qa-openai-prompt-behavior` | covered |
| TOOL-001 | Function call before `Looks right` | Blocked; no Send buttons/gateway. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-002 | Exactly one allowed call after interpretation confirmation | Three gates run; frozen intent persisted; Send buttons returned. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-003 | Two function calls | Rejected. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-004 | Unknown tool name | Rejected. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-005 | Missing call ID | Rejected. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-006 | Malformed argument string | Rejected. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-007 | Arguments are array/scalar | Rejected. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-008 | Gate 1 type/required/enum/const/bounds failure | Rejected before freeze. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-009 | Missing `structured_payload` | Gate 2 failure. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-010 | Node-pack payload violates active schema | Gate 2 failure. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-011 | Complete body violates gateway wire schema | Gate 3 failure. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-012 | Model tries to override server-owned schema/origin fields | Values stripped/replaced by server constants. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-013 | Persist failure before actions are returned | No Send actions exposed; fail closed. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| TOOL-014 | Same call ID replay | No duplicate consequential execution. | `STORY-AIBRIDGE-28-qa-tool-call-validation` | covered |
| ACT-001 | Valid `Looks right` token by owner | 200; `interpretation_confirmed`; zero gateway calls. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-002 | Valid Edit token | 200; `interviewing`; revision incremented; sibling tokens invalidated. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-003 | Valid Cancel token | 200; `cancelled`; pending tokens invalidated; no gateway. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-004 | Valid Send token | One authorized attempt using frozen body. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-005 | Random token | 404 `not_found`. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-006 | Token owned by different user | 403 `forbidden`. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-007 | Correct user, different chat | 403. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-008 | Expired token | 409 `conflict`. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-009 | Already consumed token, new event ID | 409. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-010 | Invalidated sibling token after another action | 409. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-011 | Token revision differs from session | 409. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-012 | Token expected state differs | 409. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-013 | Token deployment differs | 409 for Send. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-014 | Draft hash differs | 409 for Send. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-015 | Frozen tool intent missing | 409; gateway not called. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-016 | Illegal FSM transition | 409. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-017 | Raw token found in PostgreSQL/logs | Fail security test; only hash may persist. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| ACT-018 | Token longer than Telegram limit | 422 at façade; generated tokens must remain ≤64 bytes. | `STORY-AIBRIDGE-29-qa-action-token-fsm` | covered |
| GW-001 | Dry-run Send | `dry_run_ok`; no HTTP transport call; no published/stashed claim. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-002 | Valid 201 | `stashed`, state `stashed`, URL-encoded continuation URL. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-003 | 201 missing `trace_id` | `contract_mismatch`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-004 | 201 missing `draft_id` | `contract_mismatch`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-005 | 201 invalid JSON/non-object | `contract_mismatch`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-006 | 400 | `validation_error`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-007 | 401 | `gateway_unauthorized`; no credential leak. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-008 | 422 | `geo_scope_mismatch`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-009 | 429 | `transient_failure`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-010 | 500–599 | `transient_failure`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-011 | Timeout/disconnect after attempted post | `unknown_outcome`; same revision cannot auto-Send again. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-012 | Unusual status such as 204/409 | `unknown_outcome` under current mapping. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-013 | Redirect response/final URL changes | `contract_mismatch`; no redirect follow. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-014 | Oversized response | `contract_mismatch`. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-015 | Non-HTTPS origin | readiness/executor fails closed. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-016 | Channel and gateway Bearers equal | readiness fails; no traffic accepted as ready. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-017 | Gateway call attempted from interpretation confirmation | Fail test; zero calls. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-018 | Gateway call attempted from Edit/Cancel | Fail test. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-019 | Restart while attempt is `executing` | Recover to `unknown_outcome`; do not resend automatically. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| GW-020 | Function-call follow-up fails after successful stash | Stash outcome remains authoritative. | `STORY-AIBRIDGE-30-qa-gateway-continuation` | covered |
| LIFE-001 | Graceful shutdown begins | New channel requests receive 503 `shutting_down`, retryable true. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-002 | Restart during ordinary interview | PostgreSQL history/session restored; no duplicate confirmed side effect. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-003 | Restart after buttons issued | Pending token remains usable until TTL, if persistence is active. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-004 | Restart after token consumed | Token remains consumed. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-005 | Restart with open gateway attempt | Mark unknown and require reconciliation. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-006 | Session inactive beyond TTL | New session; old narrative minimized/deleted; old tokens unusable. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-007 | Content bundle still referenced by active session | Bundle retained until safe GC. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-008 | Bundle unreferenced after grace period | Eligible for GC without breaking active sessions. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-009 | New message after `cancelled` | Characterization test: document whether current session restarts or remains terminal; raise mismatch if resident cannot start over. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-010 | New message after `stashed` | Characterization test: verify intended creation of next story/session; current behavior must not silently trap resident in terminal state. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-011 | Edit from `unknown_outcome` | New revision/interview allowed; old revision remains non-resendable. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| LIFE-012 | Same deployment ID changes unexpectedly | Existing token must not become valid for a different deployment. | `STORY-AIBRIDGE-31-qa-restart-lifecycle-retention` | covered |
| SEC-001 | Narrative contains email/phone/personal name | Full narrative absent from structured audit logs and metrics. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-002 | Error raised with secret in exception text | Secret redacted from response/logs. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-003 | Channel request audited | Log only bounded IDs/statuses/lengths; not raw Bearer or full narrative. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-004 | `/metrics` scrape | Contains counts/latencies/cache telemetry only; no IDs, text, token, draft body, or URL secrets. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-005 | Error envelope | Stable bounded schema and generated `request_id`. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-006 | PostgreSQL token inspection | Only token hash stored. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-007 | OpenAI request capture | `store=false`; no gateway/channel secrets. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-008 | Gateway request capture | Gateway Bearer only; no Channel Bearer. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-009 | n8n workflow export | No credentials or secrets committed. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| SEC-010 | Prompt injection asks model to call arbitrary URL/tool | Only allowlisted generated function is available; gateway origin/path remain server-owned. | `STORY-AIBRIDGE-32-qa-privacy-logs-observability` | covered |
| READY-001 | Complete valid configuration and migrated PostgreSQL | 200 `ready`. Preference A / disposable-PG stand-in OK in CI (`ready-ok-migrated-pg`); memory `ready-ok` remains baseline. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-002 | Channel Bearer missing | 503 `channel_auth_missing`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-003 | Gateway Bearer missing | 503 `gateway_bearer_missing`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-004 | Bearers equal | 503 `channel_gateway_bearer_equal`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-005 | Gateway URL missing/conflicting/non-HTTPS | Corresponding bounded reason. Covered: `intake_base_url_missing` + `intake_base_url_not_https`. «conflicting» **N/A** (no distinct code in `readiness.py`). | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-006 | SPA redirect base invalid | 503 `draft_redirect_base_invalid`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-007 | OpenAI key/model missing | 503 `openai_config_missing`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-008 | OpenAI storage requested true | Settings/readiness fails closed. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-009 | Live mode without completed schema validation flag | 503 `dry_run_required`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-010 | Content manifest/hash/path invalid | 503 bundle reason. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-011 | Tool generation fails | 503 `tool_gen_failed:*`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-012 | PostgreSQL unreachable | 503 `database_unreachable`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-013 | Required migration missing/mismatch | 503 migration reason (`migration_version_mismatch` / `migrations_missing` / `migration_version_missing`; Preference A `/readyz`). | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-014 | Non-Postgres store while memory stores forbidden | 503 `database_not_postgres`. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| READY-015 | `/readyz` called | No OpenAI generation and no gateway write. | `STORY-AIBRIDGE-33-qa-readiness-configuration` | covered |
| UC-01 | Normal interview, dry-run | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-02 | Normal live stash | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-03 | Resident cancels at first confirmation | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-04 | Resident cancels immediately before Send | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-05 | Group chat ownership attack | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-06 | Telegram retry storm | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-07 | Ambiguous gateway timeout | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-08 | Geo scope mismatch | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-09 | Unsupported Telegram content | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| UC-10 | Multilingual story | See guide §11 full scenario + assertions | `STORY-AIBRIDGE-34-qa-product-journey-scenarios` | PG-journey covered (≠ Gate-5 · see STORY-37) |
| Gate-1 | channel contract | See guide §15 pass criteria | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| Gate-2 | interview safety | See guide §15 pass criteria | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| Gate-3 | consequential-action safety | See guide §15 pass criteria | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| Gate-4 | durable runtime | See guide §15 pass criteria | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| Gate-5 | live channel | See guide §15 pass criteria | `STORY-AIBRIDGE-37-qa-gate5-live-pilot-evidence` | deferred (deferred_live · out of default CI · no pilot env · capture-first · evidence index deferred · no invent live PASS) |
| CHAR-001 | What starts a fresh story after `cancelled`? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| CHAR-002 | What starts a fresh story after `stashed`? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| CHAR-003 | Should whitespace-only messages be rejected after trimming? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| CHAR-004 | Should Telegram media captions enter the text-only façade? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| CHAR-005 | How should n8n notify a resident when aibridge is unavailable after callback acknowledgement? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| CHAR-006 | Should OpenAI 429/5xx remain a channel 500, or later gain a distinct retryable channel outcome? | **Option A** recorded: map transport → bounded channel (`429 rate_limited` / `503 transient_failure`); decision fixture + tests; middleware RL distinct | `STORY-AIBRIDGE-38-qa-oai-channel-error-outcome` | covered |
| CHAR-007 | Should unusual known gateway statuses such as 409 be a specific outcome rather than `unknown_outcome`? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-35-qa-gates-layers-dod` | covered |
| CHAR-008 | Does the n8n workflow use Send Message or Edit Message for each response state, and how does it prevent duplicate outbound Telegram messages after its own retry? | Characterization — capture current; do not silently guess | `STORY-AIBRIDGE-39-qa-char008-send-edit-capture` | deferred (export absent · capture envelope status=deferred · capture-first · no invent Send/Edit · P3 2026-09-18T14:06:43Z) |
| QUAL-001 | VAL characterization asserts without tautology HTTP band | Explicit expected status (+ shape); no `100<=status<600` sole success | `STORY-AIBRIDGE-40-qa-suite-assert-hygiene` | open (Scaffolded) |
| QUAL-002 | Fixture promote hash_eq policy | Integrity-only; never sole evidence for matrix Expected | `STORY-AIBRIDGE-40-qa-suite-assert-hygiene` | open (Scaffolded) |
| QUAL-003 | Optional non-Recording GW / real-PG concurrency probe | Named probe or explicit WAIVE (not Gate-5) | `STORY-AIBRIDGE-40-qa-suite-assert-hygiene` | open (Scaffolded) |

**Total rows:** 190 (was 186 · +N8N-WF-001 · +QUAL-001…003)
