# Verify, evidence, peer coexistence

**Overview:** [`00-overview.md`](./00-overview.md)

---

## 1) Verify surfaces (Interview D5 = A)

| Gate | What | When |
|------|------|------|
| **Stub / harness** | Dual-confirm + stash client + continuation URL shape against fixtures/mocks; no claim of live Telegram E2E | **Required** for technical acceptance of changes to this pipe |
| **Live evidence** | ≥1 recorded path Telegram→bridge→gateway→SPA open (AC-AIB-11-07; parent AC-10) | **Required** to claim **live Pass / AC-07 Done**; only when ops opens an evidence window |
| Without live window | AC-AIB-11-07 stays **Partial** | Do not claim Product/child Done on stub alone |

Honesty: Product Story Done ≠ Draft REQ ≠ green local smoke alone.

---

## 2) Peer verify-first (no invent)

| Peer | Role | Arch stance |
|------|------|-------------|
| [gateway 59](../../../../doge-complaints-gateway/docs/requirements/59-req15-story-draft-stash-channel-parity-verify.md) | Stash contract verify | Cite Present `/story-drafts`; no new draft API |
| [spa 25](../../../../spa-app/docs/requirements/25-req15-story-submit-handoff-continuity-verify.md) | `#/story/submit?draft_id=` continuity | Cite Present hash contract |
| [telegram REQ-01](../../../../doge-telegram/docs/requirements/REQ-01-REQ15-TELEGRAM-CHANNEL-TRANSPORT.md) | Transport only | Never holds model keys / never stashes (AC-06) |
| [GPT UI REQ-48](../../../../GPT%20UI/docs/requirements/REQ-48-req15-role-oriented-instruction-line-and-export.md) | Strip model-owned stash/redirect from new line | Content OOS here |
| [REQ-12](../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) | Interview providers | OOS except evidence-per-provider when live |
| [REQ-13](../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) | State/roles | Calls L11-1 seam when Present |

---

## 3) Coexistence with `runtime/` package

| Doc | Relationship |
|-----|----------------|
| [`../runtime/03-confirm-gateway.md`](../runtime/03-confirm-gateway.md) | **Keep SSOT** — waves, unknown_outcome, token rules |
| This package | REQ15 **delta** only — do not fork conflicting gateway rules |

If a future change must alter Keep rules, prefer amending via explicit story after proving insufficiency — not silent drift in this delta.

---

## 4) Open (ops)

- When the live evidence window opens (calendar / env).  
- Per-provider live matrix interacts with REQ-12 (record here only as peer dependency).
