# REQ15 dual-confirm / stash / SPA handoff — target technical architecture (overview)

| Field | Value |
|-------|--------|
| **Focus** | Keep dual human confirms + factual gateway stash + SPA continuation as **server** pipe; REQ15 delta = L11-1 invalidation seam + evidence honesty |
| **Parent REQ** | [`../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md`](../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) |
| **Keep SSOT (pilot)** | [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md) — do **not** rewrite; this package is a **delta** |
| **T1** | [`../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) |
| **Wave readiness** | [`../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md`](../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) |
| **Story scope** | none (0 STORY files) |
| **Interview** | [`../../analysis/zeya888.target-tech-arch-interview-req15-dual-confirm-handoff-2026-11-01.md`](../../analysis/zeya888.target-tech-arch-interview-req15-dual-confirm-handoff-2026-11-01.md) |
| **Recorded** | 2026-11-01T14:10:30Z |
| **Mode** | Target technical architecture of the focus — not implementation tasks |
| **Slug** | `req15-dual-confirm-handoff` |
| **Layout** | system (`archDocMode=auto` → ≥3 concerns) |

**Levels:** functional = REQ-11 (AC-AIB-11-01…07, L11-1) · this folder = how Keep pipe + REQ15 hooks coexist in `doge-ai-bridge` · work items = **other prompts** (not here).

**Siblings in this package:** [`01-keep-pipe-boundaries.md`](./01-keep-pipe-boundaries.md) · [`02-l11-invalidation-seam.md`](./02-l11-invalidation-seam.md) · [`03-verify-evidence-coexistence.md`](./03-verify-evidence-coexistence.md)

---

## 1) Context & functional vs tech split

| Layer | Lives in | Content |
|-------|----------|---------|
| Product | REQ-11 + parent REQ15 | Goal, OOS, AC, L11-1 (Q5 A + transition C) |
| Keep pilot tech | `docs/architecture/runtime/03-confirm-gateway.md` | Dual-confirm FSM, tokens, gateway, unknown_outcome |
| Target tech (this package) | `docs/architecture/req15-dual-confirm-handoff/` | Delta: boundaries cite, L11-1 seam, evidence split, peer edges |
| Work items | backlog STORY (other prompts) | **Not here** |

**Use case:** Freeze Keep server pipe (confirm → stash → SPA link) and name the REQ15 coexistence hooks so Architect Studio / implement do not Replace a Present path or invent gateway/SPA APIs.

**Packaging:** same deployable image as aibridge runtime (`aibridge.app:app`). **Packaging seam N/A** (Git tree = runtime modules under `src/aibridge/`; no new non-src FS ownership for this focus).

---

## 2) Target technical architecture (summary)

```text
Resident ↔ Telegram transport (peer; no model keys, no gateway write)
         ↔ channel /v1/channel/turns|actions  (Keep)
         ↔ ConfirmationGuard + FSM + ActionTokens  (Keep — runtime/03)
         ↔ [transition] Responses tool-intent freeze ≠ permission
         ↔ GatewayExecutor POST /story-drafts (config URL + service Bearer)
         ↔ SPA continuation {SPA}/#/story/submit?draft_id=
         ↔ [REQ15 delta] semantic meaning-change → same invalidate as EDIT
              (enforce = Present EDIT until REQ-13 state Present)
```

| Concern | Target | Cite |
|---------|--------|------|
| Dual confirms | Keep two stages | REQ-11 AC-01 · `runtime/03` · `confirm.py` offer/consume |
| Stash | Code only; success = factual gateway success | AC-03/04 · `gateway.py` `execute_stash` |
| SPA URL | Present hash + `draft_id` | AC-05 · `gateway.py:118` `build_continuation_url` |
| Confirm storage | Reuse ActionToken + revision/`draft_hash` | Interview D3 · `action_tokens.py` |
| L11-1 | Named seam; transition C = EDIT path | AC-02 · `confirm.py:407–425` `apply_edit` |
| Tool loop | Keep internal as transition | Interview D4 · `runtime/03` tool≠permission |
| Evidence | Stub required; live Pass only with window | AC-07 · Interview D5 |

---

## 3) Ownership / contracts (decided)

| Artifact / secret | Owner | Note |
|-------------------|-------|------|
| Channel Bearer | aibridge channel façade | ≠ gateway token |
| `GATEWAY_SERVICE_API_TOKEN` / submit URL | aibridge GatewayExecutor from **config** | Model never supplies URL (AC-03) |
| Stash HTTP | aibridge only | Telegram never stashes (AC-06) |
| SPA publish UX | spa-app (peer 25 verify) | Stash ≠ publication |
| Instruction prose stash/redirect | GPT UI REQ-48 (strip) | Server owns pipe |

---

## 4) Runtime / packaging / verify / env

- **Runtime:** single ASGI process — Keep [`../runtime/00-overview.md`](../runtime/00-overview.md).  
- **Packaging:** N/A for this focus.  
- **Env / fail-closed:** gateway origin + token required for live stash — cite `runtime/03` / Present config; do not invent new env names here.  
- **Verify:** see [`03-verify-evidence-coexistence.md`](./03-verify-evidence-coexistence.md).

---

## 5) Coexistence with as-is

| As-is | Role vs this package |
|-------|----------------------|
| `runtime/03-confirm-gateway.md` | **Keep SSOT** for FSM, tokens, gateway rules, unknown_outcome |
| `confirm.py` / `confirm_fsm.py` / `gateway.py` / `channel.py` | Present implementation paths (T1) |
| REQ-13 semantic state | **Absent** — transition C until Present; seam named in [`02-…`](./02-l11-invalidation-seam.md) |
| REQ-12 providers | OOS — evidence recording only if needed |
| gateway 59 / spa 25 | Verify-first peers — no API invent |

---

## 6) Open questions

- Sensitivity: which semantic-state field updates = meaning change (REQ-13 + thin product under L11-1 / L13-3).  
- Ops calendar for live evidence window.  
- Timing of hard-cut tool-intent → pure role chat (after REQ-13/48).  
- Whether confirm store needs Adapt after semantic versioning proves a gap (default: no).

---

## 7) Explicit “Not in this doc”

- NEW STORY / pkg / P3 / product code  
- New gateway draft API or SPA submit redesign  
- Provider adapters (REQ-12) · instruction bodies (GPT-48) · telegram transport create  
- Invented DB schemas or field lists for semantic state  

**Method notes:** inputs (REQ) ≠ target tech arch ≠ new work items · Git ownership ≠ image packaging → **packaging N/A** · recommendation advisory; operator decided in interview.
