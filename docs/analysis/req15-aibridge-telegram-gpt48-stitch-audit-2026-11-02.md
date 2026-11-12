# REQ15 stitch audit — aibridge / telegram / GPT-48 (2026-11-02)

**Supersession (2026-11-03):** GPT-48 export / stitch **S5** «export Absent» is **no longer current truth** — see [`req15-target-state-code-gap-audit-2026-11-03.md`](./req15-target-state-code-gap-audit-2026-11-03.md) (export bodies Present on disk). Rows below marked **Superseded** keep historical snapshot wording only where noted.

**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc) — claims from Present code + REQ Status / package INDEX only.  
**Wave:** docs sync only (parent + GPT UI REQ-48 + this report). **No** runtime code, instruction bodies, Railway deploy, or ASGI wire in this turn.

**Parent:** [`../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](<../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>)  
**Peers cited (do not duplicate wholesale):**  
[`req15-t1-keep-adapt-replace-2026-11-01.md`](./req15-t1-keep-adapt-replace-2026-11-01.md) · [`req15-aibridge-wave-readiness-2026-11-01.md`](./req15-aibridge-wave-readiness-2026-11-01.md) · [`../../doge-telegram/docs/analysis/zeya888.telegram-local-stub-run-and-ac-req15-02-gap-2026-11-01.md`](../../doge-telegram/docs/analysis/zeya888.telegram-local-stub-run-and-ac-req15-02-gap-2026-11-01.md)

---

## 1. Present map (verified)

| Surface | Artifact | Reality |
|---------|----------|---------|
| Parent REQ15 | Root product | **Draft / Proposed** — Product Story Done ≠ Draft |
| aibridge REQ-11 | Dual confirm / stash / SPA | Stories **56–58** package Done; REQ Status Draft; AC-07 live **Partial** |
| aibridge REQ-12 | Interview DeepSeek \| OpenAI | Stories **59–61** Product Done; wired at ASGI start; AC-04 live **Explicit Partial** |
| aibridge REQ-13 | Semantic state / roles / assembly | Stories **62–64** Product Done (harness); **ASGI/channel wire WAIVED**; AC-05 **Explicit Partial** |
| telegram REQ-01 | `doge-telegram-channel` under folder `doge-telegram/` | Package `src/doge_telegram_channel/` **Present**; stories **01–04 Done**; **STORY-05 live BLOCKED**; Railway **Absent** |
| GPT UI REQ-48 | Role-oriented line + export | **Draft**; export/mapping/new line bodies **Present** on disk (**S5 superseded** — gap audit 2026-11-03); Product Done ≠ Draft |
| T1 | AC-REQ15-01 | **Present** (`req15-t1-keep-adapt-replace-2026-11-01.md`) |

**Exec order (aibridge):** 11 → 12 → 13 (post-renumber 2026-11-01). Parent §8 paths match disk.

**Channel path today:** telegram long-poll → `POST /v1/channel/turns|actions` → aibridge Keep **InterviewEngine** + ConfirmGuard + gateway stash. REQ-13 `SemanticStateService` / `assemble_role_prompt` / `select_next_role` are **not** wired in `app.py` channel handlers.

---

## 2. Stitch mismatches

| ID | Severity | Mismatch | Docs / intent | Present reality |
|----|----------|----------|---------------|-----------------|
| **S1** | High (ops) | Bearer env **names** | Same secret on both sides | Telegram: `CHANNEL_BEARER`. Bridge: `AIBRIDGE_CHANNEL_BEARER_TOKEN`. Values must match; names differ — easy mis-pair |
| **S2** | High (UX/E2E) | SPA handoff delivery | OpenAPI may expose `continuation_url` / `draft_id` after stash | Telegram client applies only `reply_text` + `actions[]` buttons. SPA URL reaches user **only if** bridge embeds it in `reply_text` (or future additive delivery) |
| **S3** | High (content) | Dual instruction schema | Hybrid **C** + roles cutover | Phase-A `files[]` via `content.py` /ready still Present. REQ15 roles-schema via `roles/assembly.py` + fixture `tests/fixtures/content/roles.manifest.json`. Concurrent dual schema = **wire residual**; channel still mega-string path |
| **S4** | High (AC) | REQ-13 harness ≠ channel | AC-REQ15-06 / 09 semantic + role assembly | Harness Confirmed; production ASGI persist/orchestration **Partial/Absent** (G-02 WAIVED) |
| **S5** | High (parity) | GPT-48 export lag | AC-REQ15-12 / 13 both Pass | **Superseded 2026-11-03** — export/mapping/new line **Present** ([gap audit](./req15-target-state-code-gap-audit-2026-11-03.md)); consume/volume residual tracked as V8 / STORY-67, not «export Absent» |
| **S6** | Medium (docs) | Telegram tree wording | Parent Method / §8 historically «name≠create service tree» | Tree **materialized** under `doge-telegram/`; product name ≠ folder still true; Railway/live still Open |
| **S7** | Medium (live) | AC-REQ15-02 | Traffic through channel without n8n | Code path Present + stub evidence; **live** Telegram→reachable bridge **BLOCKED** (STORY-05) |
| **S8** | Medium (docs) | Client framing | Some OpenAPI/arch still «n8n ↔ aibridge» | Target transport client = `doge-telegram-channel` |
| **S9** | Low (cascade) | Index lag | Package INDEX Done for stories | aibridge requirements README / backlog INDEX / dashboard may still show Todo for some 56–64 — cascade hygiene, not runtime |
| **S10** | Low (ops) | Provider primary | Product: DeepSeek primary once enabled | Config fail-closed requires `AIBRIDGE_INTERVIEW_PROVIDER`; `.env.example` often shows `openai` as Keep nest — ops trap vs product L5 |
| **S11** | Medium (GPT-48) | Export contract not copied | REQ-13 §3b locked for cascade | GPT-48 pre-sync: bare `INSTRUCTIONS_DIR`, Role registry «Absent», no roles-schema table — **addressed in docs wave** (REQ-48 + parent), not by creating files |

---

## 3. Key contracts (cite-only)

| Contract | Value |
|----------|--------|
| Channel HTTP | `POST /v1/channel/turns`, `POST /v1/channel/actions` · OpenAPI `doge-ai-bridge/docs/openapi/aibridge-channel-v1.openapi.yaml` |
| Gateway stash | `POST {GATEWAY_BASE_URL}/story-drafts` · Bearer = gateway service token |
| SPA URL builder | `{SPA_BASE_URL}/#/story/submit?draft_id=…` in aibridge `gateway.build_continuation_url` |
| Interview env | `AIBRIDGE_INTERVIEW_PROVIDER` ∈ `{deepseek,openai}` + nested OpenAI / `AIBRIDGE_INTERVIEW_DEEPSEEK_*` |
| Content env | `DOGESTONIA_INSTRUCTIONS_DIR` + `DOGESTONIA_INSTRUCTIONS_MANIFEST` |
| Roles schema | `bundle_version` · `core` · `roles.{id}.{file,version}` · ids: `communication_setup` · `interviewer` · `extractor` · `normalizer` · `checker` |
| Telegram env | `TELEGRAM_BOT_TOKEN` · `BRIDGE_BASE_URL` · `CHANNEL_BEARER` · `SQLITE_PATH` · optional `BRIDGE_STUB` |

---

## 4. Parent AC snapshot (honesty)

| AC | Snapshot 2026-11-02 |
|----|---------------------|
| AC-01 | **Met** (T1 Present) |
| AC-02 | Code/stub path Present; **live Open/BLOCKED** |
| AC-03 | Boundary/code support Present; live E2E not proven |
| AC-04 | Selectable providers Present; live Explicit Partial |
| AC-05 | Orthogonal worker env distinct — Confirmed in design/code |
| AC-06 | Harness Present; channel persist Partial |
| AC-07 / 08 | Pipe Present; live Partial |
| AC-09 | Roles assembly harness Present; channel Partial |
| AC-10 | Evidence split docs/gates Present; live Incomplete |
| AC-11–14 | Blocked on GPT-48 authoring/export + consume joint Pass + volume ops |

---

## 5. Closed by this docs wave vs remain Open

**Closed (docs):**

- Parent stale «service tree not created» → Present package + Railway/live residual.
- Parent Present-progress + stitch Open list + link to this audit.
- GPT-48: embed REQ-13 §3b; refresh Verified; `DOGESTONIA_INSTRUCTIONS_*`; role id mapping; AC-05 roles-schema SSOT.

**Remain Open (not this wave):**

- ASGI wire of semantic state + role assembly into channel turns.
- STORY-TELEGRAM-05 live + Railway bootstrap + reachable `BRIDGE_BASE_URL`.
- GPT-48 implement: archive / mapping / new line / export bodies (name ≠ create until ordered).
- Joint inventory/hash SSOT for export↔consume.
- Bulk stale dashboard/README index repair (S9).
- Explicit SPA URL delivery policy if bridge stops putting URL in `reply_text`.

---

## 6. Recommended next orders (labels only)

| Label | Intent |
|-------|--------|
| `gpt48-pa2-archive-mapping` | PA.2 then archive + mapping under GPT UI |
| `gpt48-export-roles-schema` | Produce roles-schema bundle matching §3b |
| `aibridge-asgi-role-semantic-wire` | Lift G-02 WAIVER; channel uses assembly + state |
| `telegram-story-05-live` | Reachable peer + evidence AC-REQ15-02 |
| `ops-bearer-env-pairing-note` | Document S1 in runtime runbooks both sides |
| `cascade-index-hygiene` | Align aibridge README/dashboard with package Done |

**STOP** — no code / STORY / pkg in this analysis turn.
