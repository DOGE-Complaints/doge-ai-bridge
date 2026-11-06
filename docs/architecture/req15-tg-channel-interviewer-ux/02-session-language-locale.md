# Session language pick + locale persistence

**Overview:** [`00-overview.md`](./00-overview.md)  
**Story:** [`STORY-AIBRIDGE-69`](../../tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-69-session-language-pick-actions.md)  
**Peers:** ChannelAction Keep · telegram `language_code` map Keep · ConfirmSession Adapt

---

## 1) Present foundation (cite)

| Piece | Status | Path |
|-------|--------|------|
| Inbound `language_code` on channel message | **Present** (telegram mapper → bridge schema) | doge-telegram `mapper.py` · aibridge `schemas.py` |
| Engine use of `language_code` | **Absent** — turn passes `message.text` only | `channel.py` |
| Session locale field | **Absent** on `ConfirmSession` / `state_json` | `confirm.py` |
| Lang-pick actions | **Absent** | — |
| Action label flags | Producer **Absent**; telegram will render any Present label | `outbound.py` Keep |

---

## 2) Confidence / gate policy (target)

| Input | Behavior |
|-------|----------|
| Unclear start text (opaque tokens, digits-only e.g. `888`, empty/whitespace) | **MUST** mint language-pick **actions** before continuing interview in a guessed locale |
| Clear natural-language start (e.g. «историю хочу подать») | **MAY** skip picker (AC-69-04) |
| Telegram `language_code` | Soft hint only — **MUST NOT** silently lock locale when text is unclear |

Gate runs on first-turn (and until locale bound) **before** interview engine advance that would commit a guessed locale.

---

## 3) Locale SSOT

| Lock | Value |
|------|--------|
| Home | **Adapt** `ConfirmSession` (+ persisted `state_json`) — field `locale ∈ {et,ru,en}` |
| Not | Semantic-state facts/hypotheses payload as locale SSOT |
| Persist | Across subsequent channel turns until explicit change (product may add change later; v1 = bind once) |
| Apply | Subsequent turns use bound locale for interview prompt/context (wire path at implement — Adapt interview/channel) |

---

## 4) Action surface

| Pick | Label contract (on `ChannelAction.label`) |
|------|-------------------------------------------|
| Eesti | Language name + Estonian flag emoji |
| Русский | Language name + Russian flag emoji |
| English | Language name + **US** flag 🇺🇸 (product lock) |

Token kinds: new pick kinds (or parameterized CONTINUE-style locale picks) registered in `action_tokens` — literal enum names at implement. Consume binds `ConfirmSession.locale` and resumes interview.

Telegram: render Present list only — **no** new telegram STORY for strings.

---

## 5) Trust / coexistence

| Must | Must not |
|------|----------|
| Locale chosen by user action or clear-text skip policy | Model invents locale mid-turn without bind |
| Soft-dep independent of STORY-68 seam tokens | Block 69 on CONTINUE invent |
| Keep ChannelAction contract | Invent parallel keyboard protocol |

---

## 6) Touchpoints (implement)

| Concern | Modules |
|---------|---------|
| Detect unclear | channel / thin policy helper |
| Persist locale | `confirm.py` ConfirmSession · store |
| Mint/consume picks | `action_tokens.py` · `confirm.py` / channel gate |
| Apply locale | interview / channel wire Adapt |
| Tests | unclear→actions; clear skip; persist; EN=🇺🇸 |
