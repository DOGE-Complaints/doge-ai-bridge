# REQ15 target-state ↔ code gap / vulnerability audit (2026-11-03)

**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc) — verified Status lines, package INDEX, and Present code only.  
**Parent target:** [`../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](<../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md>)  
**Prior stitch (cite):** [`req15-aibridge-telegram-gpt48-stitch-audit-2026-11-02.md`](./req15-aibridge-telegram-gpt48-stitch-audit-2026-11-02.md) — **S5 (GPT-48 export Absent) superseded** by this audit (export bodies Present on disk).

**Wave:** docs integration only. No code fixes.

---

## 1. Claim validation — «all children from root REQ15 completed»

**Verdict: NOT confirmed.** Parent Product Story Done ≠ Draft. All seven §8 child **REQ Status = Draft**. Story/package Done ≠ child REQ Product Done ≠ parent AC Done.

| Child | REQ Status | Stories / package | Honest «completed»? | Residual |
|-------|------------|-------------------|---------------------|----------|
| **GPT UI REQ-48** | Draft | ROL-01…04 **4/4 Done** (Awaiting Commits) | **Wave artifacts yes**; REQ Product Done **no** | AC-13 needs consume Pass; live volume Open; REQ Status Draft |
| **aibridge REQ-11** | Draft | 56–58 Done · P8 exhausted | Harness/pipe **yes**; live **no** | AC live Explicit Partial |
| **aibridge REQ-12** | Draft | 59–61 Product Done | Adapters/wire **yes**; live **Partial** | Live per-provider Open |
| **aibridge REQ-13** | Draft | 62–64 Product Done · G-02 **WAIVED** | Harness **yes**; channel **no** | ASGI semantic/roles not on turns path |
| **telegram REQ-01** | Draft | 01–04 Done; **05 BLOCKED** | Transport code **yes**; live/Railway **no** | STORY-05; no Dockerfile/railway |
| **gateway 59** | Draft — awaiting PA.2 | **No** REQ15 story package | **No** | Verify-first AC not packaged |
| **spa 25** | Draft — awaiting PA.2 | **No** story package under 25 | **No** | Continuity verify not packaged |

Keep stash (`POST /story-drafts`) and SPA `#/story/submit?draft_id=` code exist **independently** of gateway-59 / spa-25 verify waves — those children are still **not** Done as REQ15 verify packages.

---

## 2. AC-REQ15-01..14 ↔ Present code

| AC | Status | Evidence |
|----|--------|----------|
| **01** T1 | **Met** | [`req15-t1-keep-adapt-replace-2026-11-01.md`](./req15-t1-keep-adapt-replace-2026-11-01.md) |
| **02** TG channel path | **Partial** | `doge-telegram/src/doge_telegram_channel/` → turns/actions; n8n absent in package. Live STORY-05 **BLOCKED**; Railway packaging **Absent** |
| **03** no AI/gateway in TG | **Met** | `boundary.py` + forbidden env fragments; stash only in aibridge `gateway.py` |
| **04** DeepSeek\|OpenAI; DeepSeek primary | **Partial** | `AIBRIDGE_INTERVIEW_PROVIDER` + adapters + `bind_interview_engine_at_wire`. Fail-closed empty. `.env.example` often **`openai`**, not DeepSeek primary |
| **05** worker env ≠ interview | **Met** | Registry must not read `AIBRIDGE_WORKER_*_PROVIDER`; story-59 tests |
| **06** semantic state | **Partial** | `semantic_state/` + migration `0002` + harness. **Not** imported in channel `app.py` path (G-02 WAIVED) |
| **07** dual confirm + meaning invalidate | **Partial** | Dual FSM Present (`confirm.py` / `confirm_fsm.py`). EDIT invalidate Present. Target-A meaning→invalidate via `SemanticStateService` **not** on channel |
| **08** success after gateway success | **Met** (code) / live **Unknown** | `execute_stash` → STASHED + `draft_id`; harness Present. Live E2E Absent |
| **09** role assembly code-driven | **Partial** | `roles/assembly.py` + policy harness. Channel still Phase-A mega-string `InterviewEngine` via `content.py` `files[]` |
| **10** stub vs live per provider | **Partial** | Stub/gates Present; live Explicit Partial / not claimed |
| **11** transport ≠ rewrite methodology | **Met** | Mapping + roles line separate from telegram transport |
| **12** GPT-48 archive+mapping+line | **Met** (disk) | `GPT UI/instructions-archive-module1-req48/`; `docs/analysis/req-48-module1-role-mapping.md`; `instructions-roles/` + `roles.manifest.json`; new line strips model stash/SPA procedures |
| **13** export **and** consume Pass | **Partial** | Export evidence Present (`req-48-export-parity-evidence.md`). Consume: harness/fixture Partial; channel not on roles-schema; volume ops Unknown |
| **14** hybrid C volume | **Partial** | Env path-agnostic `DOGESTONIA_INSTRUCTIONS_*`; authoring GPT UI. Live Railway volume + roles cutover on channel **Unknown/Absent** |

---

## 3. Vulnerability / seam register

| ID | Severity | Seam | Impact on target |
|----|----------|------|------------------|
| **V1** | **Critical** | SPA URL drop: aibridge sets `continuation_url` (`gateway.build_continuation_url` → confirm → channel schema); telegram delivery uses only `reply_text` + `actions[]` | Stash can succeed without user-visible SPA link → AC-08 handoff UX broken on TG path |
| **V2** | **Critical** | REQ-13 ASGI WAIVER: `SemanticStateService` / `assemble_role_prompt` / `select_next_role` not on channel turns | AC-06 / AC-09 / Target-A meaning-invalidate not on product path |
| **V3** | **High** | Dual content schema: Phase-A `files[]` on ready/engine vs GPT-48 roles-schema export Present | Consume cutover incomplete; dual mount = wire residual |
| **V4** | **High** | Live Telegram→bridge BLOCKED; Railway Absent in `doge-telegram/` | AC-02 live not Met; E2E yellow |
| **V5** | **Medium** | Bearer names: TG `CHANNEL_BEARER` ≠ bridge `AIBRIDGE_CHANNEL_BEARER_TOKEN` | Ops mis-pair → auth failures |
| **V6** | **Medium** | Product DeepSeek-primary vs example default `openai` | Ops trap vs AC-04 primary |
| **V7** | **Medium** | gateway 59 / spa 25: Draft, no stories | REQ15 verify continuity not closed (Keep code ≠ verify Done) |
| **V8** | **High** | Export Pass ≠ Consume Pass | AC-13 Content Done blocked |

---

## 4. Integrate understanding — Done vs blocks Product Done

**Present and useful (do not re-build):**

- Dual-confirm + gateway stash pipe (REQ-11 stories).
- Interview provider port + DeepSeek/OpenAI adapters wired at ASGI start (REQ-12).
- Telegram long-poll transport with no AI/gateway write (REQ-01 01–04).
- GPT-48 archive, mapping, roles line, `roles.manifest.json`, export evidence on disk.
- Gateway `POST /story-drafts` and SPA submit hash-route as Keep peers.

**Blocks parent Product Done / full AC close:**

1. Deliver SPA URL on Telegram path (**V1**).  
2. Wire semantic state + role assembly into channel ASGI (**V2**) and cut over content consume to roles-schema (**V3/V8**).  
3. Unblock live TG peer + Railway (**V4**); close STORY-05.  
4. Materialize/run gateway 59 + spa 25 verify packages (**V7**).  
5. Ops: Bearer pairing (**V5**), DeepSeek primary env honesty (**V6**), volume publish for hybrid C (**AC-14**).  
6. Flip child REQ Status only after residuals accepted — stories Done alone ≠ REQ Accepted.

---

## 5. Supersessions / doc drift fixed this wave

| Prior claim | Now |
|-------------|-----|
| Stitch **S5**: GPT-48 export Absent | **Superseded** — `instructions-roles/` + export evidence Present |
| Parent progress 2026-11-02: GPT-48 blocks until archive/mapping/export | **Cascade** — artifacts Present; AC-12 Met on disk; AC-13/14 still Open |
| GPT-48 §3: export bodies Absent | **Cascade** — Verified refresh; Status remains Draft |
| «All children completed» | **Rejected** as Product Done claim (§1) |

---

## 6. Recommended next orders (labels only — do not implement here)

**Triage into pipes (2026-11-03):** [`req15-gap-triage-pipes-2026-11-03.md`](./req15-gap-triage-pipes-2026-11-03.md) — Pipe1 STORY · Pipe2 LF (V1 PASS) · Pipe3 accumulative hygiene.

| Label | Intent | Pipe |
|-------|--------|------|
| `telegram-continuation-url-delivery` | Close **V1** (telegram-only append `continuation_url`) | **2** LF |
| `aibridge-asgi-role-semantic-wire` | Lift G-02; close **V2** | **1** STORY |
| `roles-schema-channel-cutover` | Point channel/ready at roles-schema; retire dual **V3** | **1** STORY |
| `telegram-story-05-live-railway` | Close **V4** | **1** STORY |
| `gateway-59-spa-25-verify-packages` | Close **V7** | **1** STORY |
| `req15-ops-docs-hygiene-batch` | Close **V5/V6** + index/OpenAPI hygiene | **3** Accum |
| `consume-parity-pass-volume` | Close **V8** / AC-13/14 | **1** STORY |

**STOP** — no code / STORY create in this analysis turn.
