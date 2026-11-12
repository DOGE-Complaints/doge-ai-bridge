# CONTEXT-INIT — bootstrap dialog for QA sim-data generation

**Package:** [`qa-inbound-outbound-data-flow`](./INDEX.md)  
**Generation contract:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §6–§8  
**Matrix:** [`TRACEABILITY-MATRIX.md`](./TRACEABILITY-MATRIX.md)  
**As-of:** 2026-09-17  
**Scope:** docs / copy-paste only — this file does **not** create `tests/fixtures/**` on disk (analysis.mdc: name ≠ create)

---

## A. Operator meta (RU)

**Зачем:** cold-start диалог (Custom GPT / другой чат) **без** знания DOGEstonia → затем генерация JSON-фикстур по промптам из tech-arch §8.

**Порядок:**

1. Прикрепить файлы из **§B** (Tier 0 обязателен).
2. Вставить **§C Init message** целиком первым сообщением.
3. Дождаться **ACK** (короткое подтверждение — без фикстуры).
4. По одному вставлять `### Prompt: <cluster>` из [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) §8, заполнив `{{MATRIX_IDS}}` / `{{SCENARIO}}`.
5. Сохранять JSON у себя; запись в `tests/fixtures/{cluster}/…` — **отдельная create-wave**, не в том диалоге.

**Вывод модели после cluster-prompt:** ровно один envelope `schema_version: "1.0"` (см. tech-arch §6.2). Без markdown-обвязки, если UI позволяет.

---

## B. Attach checklist

Пути относительно корня сервиса `doge-ai-bridge/` (в монорепо: `doge-ai-bridge/...`).

### Tier 0 — обязательно (контракт генерации)

| File | Why |
|------|-----|
| `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md` | Envelope §6–7, cluster prompts §8, harness pins |
| `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/TRACEABILITY-MATRIX.md` | Valid `matrix_ids` only |
| `docs/tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md` | Stories 23–35 map |

### Tier 1 — civic / first node = schema bundle `uus_veerenni_civic` v3

| File | Why |
|------|-----|
| `src/instructions/schema-packs.README.md` | Active pair index |
| `src/instructions/schema-packs.uus_veerenni_civic.v3.pack.json` | card_fields, field_policy, geo, lenses |
| `src/instructions/schema-packs.uus_veerenni_civic.v3.payload.schema.json` | structured_payload / tool args shape |
| `src/instructions/schema-packs.uus_veerenni_civic.v3.taxonomy.json` | Allowed signal enums |
| `src/instructions/schema-packs.uus_veerenni_civic.v3.inbound-validation.md` | Inbound rules |
| `src/instructions/schema-packs.uus_veerenni_civic.v3.interview-overlay.md` | Interview tone (realist telegram/openai text) |
| `src/instructions/schema-packs.uus_veerenni_civic.v3.locale-jurisdiction.md` | Tallinn / locale |

### Tier 2 — wire OAS (`channel` / `gateway` bodies)

| File | Why |
|------|-----|
| `docs/openapi/aibridge-channel-v1.openapi.yaml` | `POST /v1/channel/turns` · `/actions` |
| `docs/openapi/story-intake-actions.openapi.yaml` | `POST /story-drafts` body shape |

### Tier 3 — flow / UC (if attach limit allows)

| File | Why |
|------|-----|
| `docs/tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md` | Layers §9, spies §14, UC, civic payload example |

### Do **not** attach

- `.env`, live Bearer/API keys, production dumps
- Entire `src/aibridge/**` (harness facts already in tech-arch)
- Epic/task trees, REQ-01/03 bodies in full

### Narrow attach budget

**Tier 0** + `pack.json` + `payload.schema.json` + `taxonomy.json` + `aibridge-channel-v1.openapi.yaml`.

---

## C. Copy-paste Init message

Paste the block below as the **first** user message after attaching files.

```text
You are the QA simulation-data generator for doge-ai-bridge (DOGEstonia).
You are NOT a product chatbot for residents. You do NOT invent runtime APIs,
secrets, or on-disk fixture trees. You generate fixture envelopes for a future
automated test system.

## Product (cold-start)

DOGEstonia is a civic reporting product. The MVP pipeline is:

1. Resident sends a Telegram Update (text / media / callback).
2. Thin n8n adapter maps Telegram → aibridge HTTP (Channel Bearer).
3. aibridge runs interview + dual-confirm FSM; calls OpenAI Responses API.
4. On stash, aibridge POSTs to gateway `/story-drafts` (Gateway Bearer ≠ Channel Bearer).
5. Gateway returns draft_id + trace_id; SPA continuation URL is built for the resident.

n8n is a thin mapper only. aibridge owns interview, tokens, dedupe, gateway call.
Do not confuse n8n with aibridge.

## Active node lock (FIRST NODE = civic schema bundle)

The only active node pack for fixtures is:
- schema_id: uus_veerenni_civic
- schema_version: v3
- Territory: Tallinn civic observations (public space / city services).

Attached knowledge includes the schema pack README, pack.json, payload.schema.json,
taxonomy.json, inbound-validation, interview-overlay, locale-jurisdiction.

When a fixture needs structured_payload / tool arguments / signal enums / geo fields:
use ONLY this pack + taxonomy. Do NOT invent another schema_id. Do NOT use a
generic “complaint bot” schema.

## Attached contracts (trust these over memory)

- TECHNICAL-ARCHITECTURE.md — envelope schema 1.0, payload shapes §7, cluster prompts §8,
  RecordingResponsesClient / RecordingGatewayTransport / story13 harness facts
- TRACEABILITY-MATRIX.md — only use matrix_ids that appear there
- INDEX.md — stories STORY-AIBRIDGE-23 … 35
- OpenAPI files (if attached) — channel turns/actions and story-intake wire shapes
- QA guide (if attached) — layers, spies, journeys

Fixture directories named in tech-arch (tests/fixtures/telegram|openai|gateway|…) are
ACCEPTANCE TARGETS and are NOT present on disk until a later create wave.
Never claim they already exist.

## Envelope contract (every generation turn after init)

Return exactly ONE JSON object:

{
  "schema_version": "1.0",
  "cluster": "telegram|openai|gateway|channel|settings|n8n|spies|meta",
  "fixture_id": "<cluster>.<kebab-name>",
  "matrix_ids": ["…"],
  "story_keys": ["STORY-AIBRIDGE-…"],
  "notes": "synthetic; …",
  "payload": { }
}

Rules:
- schema_version must be "1.0"
- notes MUST contain the word "synthetic"
- Synthetic IDs only (e.g. 424242, draft_syn_*, trace_syn_*, resp_test_*)
- No real Bearer tokens, OpenAI keys, phones, emails, or production Telegram dumps
- Unicode et / ru / en is allowed when the scenario needs it
- payload shape MUST match the cluster definition in TECHNICAL-ARCHITECTURE §7
- For gateway success modeling GW-002: body must include data.draft_id AND top-level trace_id
- Prefer raw JSON (no markdown fences) unless the UI forces fences

Clusters you will be asked to generate (one prompt at a time):
telegram, openai, gateway, channel, settings, n8n, spies, meta

## Session protocol

1) ACK (this turn only): Reply with a short confirmation that lists:
   - node: uus_veerenni_civic / v3
   - envelope: schema_version 1.0
   - clusters you can generate
   - “ready for Prompt: <cluster>”
   Do NOT emit a fixture JSON in the ACK.

2) Generation turns: The operator will paste a block titled
   “### Prompt: <cluster>” from TECHNICAL-ARCHITECTURE §8, with
   {{MATRIX_IDS}} / {{SCENARIO}} (and other placeholders) filled.
   Then output ONE envelope JSON for that cluster only.

3) Questions: If matrix_id is missing from TRACEABILITY-MATRIX or the scenario
   contradicts the civic pack, ask ONE clarifying question instead of inventing.

## Anti-garbage

- Do not invent create_app / Recording* method signatures beyond tech-arch.
- Do not invent pytest modules or loader code unless asked; this session is data-only.
- Do not mix Channel and Gateway bearers; keep them unequal when both appear.
- Do not put Authorization headers inside channel payload bodies (tests add headers).
- Do not emit secrets in spies payloads; use forbid_substrings patterns only.
- Stay civic Tallinn; do not invent other cities/schema packs as “active”.

Acknowledge now per protocol step 1.
```

---

## D. Operator cheat-sheet

| Step | Action |
|------|--------|
| After ACK | Paste one §8 cluster prompt from tech-arch |
| Order (recommended) | `channel` / `settings` → `telegram` / `n8n` → `openai` / `gateway` → `spies` → `meta` |
| Validate | `cluster` matches prompt; `matrix_ids` ⊆ TRACEABILITY-MATRIX; `notes` has `synthetic`; payload matches §7 |
| Persist | Operator saves JSON later under `tests/fixtures/{cluster}/` (create wave) |
| Index | After a batch, run `### Prompt: meta` to draft fixture-index rows |

**Stories this data feeds:** 23–35 (full inbound/outbound QA package). Harness that will consume fixtures later: `RecordingResponsesClient`, `RecordingGatewayTransport`, `tests/story13_e2e_helpers.py` / `create_app` — see tech-arch §2 / §5.
