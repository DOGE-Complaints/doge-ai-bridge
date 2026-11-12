# REQ15 T1 — keep / adapt / replace (interview path)

**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc) — claims from code path:line + REQ paths  
**Emitted:** 2026-11-01T12:30:40Z (`builder_resolve_queue.py --print-utc-now`)  
**Parent:** [`../requirements backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](../requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md) §4 O1 / AC-REQ15-01 / §12  
**Primary focus:** `doge-ai-bridge` · light peers: gateway stash, GPT UI instructions  
**Children (aibridge):** REQ-11 · REQ-12 · REQ-13  
**Status:** T1 analysis Present — **not** Product Story Done; does **not** invent env/HTTP/DB SSOT

---

## 1) Use case

Executable-path audit before Architect Studio / behavioral change: what to **Keep / Adapt / Replace** for interview runtime under REQ15 locks (DeepSeek|OpenAI interview providers, semantic state + roles, dual confirm server pipe, telegram transport peer).

---

## 2) Verified as-is (path:line)

### Channel
| Piece | Cite |
|-------|------|
| Prefix | `doge-ai-bridge/src/aibridge/app.py:57` `CHANNEL_PATH_PREFIX = "/v1/channel/"` |
| Turns | `app.py:909–937` → `process_turn_async` + `ConfirmationGuard` + `interview_engine` |
| Actions | `app.py:939–973` → `process_action` |
| Envelope | `channel.py:25–49`, `78–120` |
| Runtime docs still n8n-first | `doge-ai-bridge/docs/runtime-docs/01-api.md:35–36`, `:194–199` |

### Interview engine + OpenAI
| Piece | Cite |
|-------|------|
| Engine | `interview.py:29–51`, turn `67–121`, `last_confirmed_state` string map `:47,:156` |
| Wire instructions | `app.py:234–268` |
| OpenAI Responses only | `app.py:414–426` · `responses_client.py:327–346` `base_url=api.openai.com` `/responses` |
| DeepSeek / interview provider id in `src/` | **Absent** (grep zero) |
| Worker providers orthogonal | `providers/ids.py:8–14` · `config.py:220–228` |

### Dual confirm + stash + SPA
| Piece | Cite |
|-------|------|
| FSM | `confirm_fsm.py:8–67` |
| Guard | `confirm.py:28–46`, offer `344–382`, EDIT invalidate `407–425`, consume `530–587` |
| Coordinator auto-offer interpret | `coordinator.py:173–248` (FC-less interviewing → always interpret offer) |
| Stash | `gateway.py:13` `STASH_PATH="/story-drafts"` · `execute_stash` `209–345` |
| Continuation | `gateway.py:118–120` `{SPA}/#/story/submit?draft_id=` |

### Content / stores / ready
| Piece | Cite |
|-------|------|
| Dir+manifest | `config.py:91–98` · `content.py:81–116` |
| Baked instructions | `src/instructions/instructions.manifest.json` |
| History / sessions | `history.py` · `sessions.py` · PG wire `app.py:439–465` |
| Readyz | `readiness.py:105–188` |

### Light peers
| Peer | Cite |
|------|------|
| Gateway `POST /story-drafts` | `doge-complaints-gateway/src/core/api/asgi_app.py:685–698` |
| GPT UI Module-1 index | `GPT UI/instructions/instruction-modules-index.md` |
| Model-owned stash prose | `GPT UI/instructions/api-orchestrator.md` §5.2 / §5.2.B (~240–256) |
| Archive folder | `GPT UI/instructions/archive/` — **not** full Module-1 as-was archive (REQ-48 prerequisite Incomplete) |

---

## 3) Keep / Adapt / Replace

| Component | Verdict | Notes |
|-----------|---------|-------|
| `/v1/channel/turns` + `/actions` | **Keep** | REQ15 L2 starting contract |
| Channel Bearer ≠ gateway Bearer; stash on bridge | **Keep** | L3 / L19 |
| `ConfirmationGuard` + FSM + EDIT invalidation | **Keep** (+ minor Adapt for resume-gating) | L11–L12 |
| `execute_stash` + continuation URL | **Keep** | L4 |
| HistoryStore + session pin | **Keep** | Not semantic-state substitute |
| content dir+manifest + ready fail-closed | **Keep** shape; **Adapt** hybrid C + consume parity + per-role slices | L13/L17/L20 |
| InterviewEngine + Responses mechanics | **Adapt** → behind role/provider port | O5 |
| OpenAI `/responses` client | **Keep** as OpenAI adapter | L6 |
| Interview DeepSeek + selector | **Replace** (Absent → new) | L5/L7 · REQ-12 |
| `AIBRIDGE_WORKER_*_PROVIDER` | **Keep** orthogonal | L16 · AC-REQ15-05 |
| Auto-offer interpret every plain turn | **Adapt** | O5 resume readiness |
| Monolithic Module-1 string | **Adapt** → role templates + GPT-48 | L8–L9 |
| Five-role registry | **Replace** (Absent) | §6 |
| App semantic state store | **Replace** (Absent) | O4 |
| Model-owned stash in instruction SSOT | **Replace** for new line (archive as-was) | L18–L19 · GPT-48 |
| n8n transport ownership (docs) | **Replace** → telegram channel peer | L1 · O3 |
| Sense-brief/poster worker | **Keep** untouched | L16 |

---

## 4) Gaps vs aibridge child AC

> **Renumber 2026-11-01:** child numbers aligned to arch order — REQ-11 = dual-confirm (was 13), REQ-12 = providers (was 11), REQ-13 = state/roles (was 12). AC-AIB ids follow the new child numbers.

### REQ-11 (dual confirm / stash / SPA)
| AC | Status |
|----|--------|
| AC-AIB-11-01 dual confirms | **Present** |
| AC-AIB-11-02 invalidate on change | **Present** (EDIT/revision); semantic-without-EDIT **Partial** |
| AC-AIB-11-03 config submit URL | **Present** |
| AC-AIB-11-04 factual gateway success | **Present** |
| AC-AIB-11-05 SPA hash + draft_id | **Present** |
| AC-AIB-11-06 telegram never stashes | **Present** (bridge design) |
| AC-AIB-11-07 live E2E evidence | **Partial / Unknown** (not claimed Done) |

### REQ-12 (interview providers)
| AC | Status |
|----|--------|
| AC-AIB-12-01 interview provider config | **Absent** |
| AC-AIB-12-02 worker ≠ interview switch | **Present** by isolation (no positive interview selector yet) |
| AC-AIB-12-03 both adapters harness | **Absent** (DeepSeek) |
| AC-AIB-12-04 live evidence per provider | **Absent** |
| AC-AIB-12-05 interview provider fail-closed | **Partial** (missing key → recording engine, not typed interview-provider fail) |

### REQ-13 (semantic state / roles / assembly)
| AC | Status |
|----|--------|
| AC-AIB-13-01 semantic state | **Absent** |
| AC-AIB-13-02 five roles + pins | **Absent** |
| AC-AIB-13-03 dir+manifest assemble | **Present** |
| AC-AIB-13-04 Railway volume docs | **Partial** (env pattern Present) |
| AC-AIB-13-05 consume parity Pass | **Absent** |
| AC-AIB-13-06 incomplete content ready fail | **Present** (when content configured) |
| AC-AIB-13-07 prompts ≠ stash owner | **Partial** (code owns stash; baked/GPT texts still teach Actions stash) |
| AC-AIB-13-08 resume / confirm-offer policy | **Partial** (T1 Adapt — auto-offer interpret) |

---

## 5) Reference interview scenarios

1. **S1 Session start + turn loop** — Present can channel→engine reply; cannot DeepSeek / app fact store / setup role.  
2. **S2 Resume vs correct understanding** — Present can interpret confirm + EDIT; cannot explicit resume-readiness gate (auto-offer interpret).  
3. **S3 Extract → normalize → checker** — Present can single model turn + tool after interpret; cannot discrete role chain.  
4. **S4 Dual confirm Send + stash + SPA** — Present can server pipe; cannot Checker-as-role pre-send.  
5. **S5 Meaning/draft change invalidates send** — Present can EDIT invalidate; cannot semantic SSOT invalidation.  
6. **S6 Gateway error without blind resend** — Present can UNKNOWN_OUTCOME + revision block; live Telegram→…→SPA per provider Unknown.

---

## 6) Contradictions (docs vs code)

| Topic | Doc target | Code today |
|-------|------------|------------|
| Transport | `doge-telegram-channel` | Runtime docs still n8n façade; bridge contract channel-agnostic |
| Interview providers | DeepSeek primary \| OpenAI | OpenAI-only interview path |
| Semantic state | App-owned O4 | History + confirm FSM strings only |
| Roles | Five v1 | One InterviewEngine |
| Stash ownership in content | Server-only new line | `api-orchestrator` still model Actions stash |
| REQ-48 archive | Full as-was | `archive/` incomplete vs Module-1 |
| Resume readiness | Ordinary reply ≠ final confirm offer | Auto interpret offer while INTERVIEWING |

---

## 7) Explicit Unknowns (for Architect Studio / PA.2 — not invented here)

- ~~Interview provider **env names**~~ — **resolved 2026-11-01:** product lock **L12-1** = `AIBRIDGE_INTERVIEW_PROVIDER` (orthogonal to `AIBRIDGE_WORKER_*`; was L11-1 before renumber).  
- DeepSeek **model id** availability — still Open until live confirm (**L12-2**).  
- Additive channel OAS fields for semantic/role outcomes — only after PA.2.  
- DB shape for semantic state.  
- Confirm artifact versioning beyond Present tokens/`draft_hash`.  
- Whether Responses tool loop remains internal after role split.  
- Live E2E per provider; consume parity hash procedure; Railway volume ops evidence.  
- GPT UI → aibridge sync script (not found).

---

## 8) Bottom line for Architect Studio

- **REQ-11 core pipe is largely Keep** — dual confirm + config stash + SPA handoff Present.  
- **REQ-12 / most of REQ-13 are Replace/Adapt** — providers, semantic state, roles, content line.  
- Transport cutover is **peer** (`doge-telegram` REQ-01); aibridge keeps L2 contract unless PA.2 says otherwise.  
- Next: per-child `target-tech-architecture` (operator-run) using this T1 as as-is SSOT cite — **order and copy-paste:** [`req15-aibridge-wave-readiness-2026-11-01.md`](./req15-aibridge-wave-readiness-2026-11-01.md) (§4–§5: **11 → 12 → 13**).

---

## 9) Related

| Artifact | Role |
|----------|------|
| Parent REQ15 | Product locks / AC-REQ15-01 |
| aibridge REQ-11/12/13 | Child functional REQs (exec order = number order after 2026-11-01 renumber) |
| [`req15-aibridge-wave-readiness-2026-11-01.md`](./req15-aibridge-wave-readiness-2026-11-01.md) | Wave safety + operator handoff (arch order, peers, stories gate) |
| This file | T1 analysis SSOT |
