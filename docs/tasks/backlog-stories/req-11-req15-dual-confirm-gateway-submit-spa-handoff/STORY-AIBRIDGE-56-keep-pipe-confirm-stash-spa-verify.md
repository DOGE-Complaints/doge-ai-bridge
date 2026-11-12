# STORY-AIBRIDGE-56 — Keep pipe: dual-confirm + stash + SPA verify

## Meta
- **Key:** `STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify`
- **Status:** Done · Product Done · P8 · pkg-000059 · SHAs 8a4774e/db5f5ac/22bccc3 · 2026-11-01T14:51:13Z · [pipeline](../../epics/EPIC-AIBRIDGE-09-req-11-req15-dual-confirm-gateway-submit-spa-handoff/stories/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify/STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) · [p4](../../../analysis/p4-audit-STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify-20261101.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify-20261101.md)
- **P8 Commits:** 8a4774e feat · db5f5ac test · 22bccc3 docs · push=NO
- **Parent REQ:** [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) §§2–5 AC-01/03/04/05/06
- **Tech-arch:** [`req15-dual-confirm-handoff/01-keep-pipe-boundaries.md`](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) · Keep [`runtime/03-confirm-gateway.md`](../../../architecture/runtime/03-confirm-gateway.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [57](STORY-AIBRIDGE-57-l11-invalidation-seam.md) · [58](STORY-AIBRIDGE-58-stub-live-evidence-gates.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-01T14:15:37Z
- **Tech subtasks:** Present · Status synced P6 2026-11-01T14:47:16Z (t01–t07 Done · t08 PASS)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Re-verify Present server pipe: interpretation confirm ≠ send confirm; ActionToken + revision/`draft_hash` (arch D3 reuse).
- Gateway submit URL + Bearer only from bridge config (`GatewayExecutor`); model cannot supply arbitrary URL.
- User-visible success only after factual stash success; continuation `{SPA}/#/story/submit?draft_id=`.
- Prove telegram/channel path does not perform stash (secrets on bridge).
- Harness/tests + thin runtime note if missing — **Keep**, not rewrite FSM/gateway API.

## Out of scope
- L11-1 semantic seam implement (57); stub/live evidence gates doc (58).
- Gateway schema / SPA UX redesign (peers 59/25).
- REQ-12 providers · GPT-48 instruction rewrite · NEW confirm store.
- Checker/PII role body (REQ-13 — operator Q1).

## Verified current state
- Dual-confirm: `confirm_fsm.py` · `confirm.py` offer/consume (T1 / REQ §3).
- Stash + URL: `gateway.py` `execute_stash` · `build_continuation_url` (~L118–120).
- Channel: `app.py` `/v1/channel/turns`·`actions` · `channel.py` `process_action`.
- `GATEWAY_SERVICE_API_TOKEN` required in executor (`gateway.py` ~L206).

## Target / AC
- [x] AC-AIB-11-01: two distinct confirm stages enforced in harness.
- [x] AC-AIB-11-03: submit URL from config only.
- [x] AC-AIB-11-04: success only after factual gateway success.
- [x] AC-AIB-11-05: continuation uses Present SPA hash + `draft_id`.
- [x] AC-AIB-11-06: no stash from telegram-service responsibility (bridge-owned client).

**P3 evidence:** `tests/test_story_56_keep_pipe_confirm_stash_spa.py` · `docs/runtime-docs/04-confirm-gateway-keep-pipe.md` · suite 587 passed.

## Code points
- `src/aibridge/confirm.py` · `confirm_fsm.py` · `action_tokens.py`
- `src/aibridge/gateway.py` · `channel.py` · `app.py` channel routes
- Tests: extend Present confirm/gateway harness (path chosen at implement; no invent API)

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Dual-confirm stages harness: interpretation offer ≠ send offer/consume | [`01` §1](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) · [`runtime/03` §1](../../../architecture/runtime/03-confirm-gateway.md) | AC-AIB-11-01 | `confirm.py` offer_* / consume · `confirm_fsm.py` | L11-1 seam (57) | Done |
| **t02** | Confirm storage reuse: ActionToken + revision/`draft_hash`; no parallel schema | [`01` §3](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) (D3) | AC-01 support | `action_tokens.py` · session revision fields | NEW confirm store | Done |
| **t03** | Trust: tool-intent freeze ≠ gateway permission; intent alone must not stash | [`01` §2](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) (D4) · [`runtime/03` §3](../../../architecture/runtime/03-confirm-gateway.md) | Keep outcome contract | ConfirmGuard / frozen tool intent path | Pure role hard-cut (REQ-13/48) | Done |
| **t04** | GatewayExecutor: submit URL + Bearer only from config; fail-closed without token | [`01` §1–2](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) ownership | AC-AIB-11-03 | `gateway.py` ~L202–206 · settings origin/token | Invent new env names | Done |
| **t05** | Factual stash success → user-visible success; clear failure; `unknown_outcome` no blind resend | [`01` §4](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) · [`runtime/03` §5–6](../../../architecture/runtime/03-confirm-gateway.md) | AC-AIB-11-04 | `gateway.py` `execute_stash` / outcomes | Gateway schema redesign | Done |
| **t06** | Continuation `{SPA}/#/story/submit?draft_id=` only when stashed; copy ≠ Story published | [`01` §1](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) · §4.5 | AC-AIB-11-05 | `gateway.py:118` `build_continuation_url` | SPA UX redesign (spa 25) | Done |
| **t07** | Bridge owns stash: channel/telegram must not hold gateway Bearer / not own stash client | [`01` §1](../../../architecture/req15-dual-confirm-handoff/01-keep-pipe-boundaries.md) transport | AC-AIB-11-06 | `channel.py` · `app.py` channel routes · boundary assert | telegram REQ-01 implement | Done |
| **t08** | Story gate checklist: AC-01/03/04/05/06 stub-Pass; Keep — no FSM/gateway API rewrite | [`00-overview`](../../../architecture/req15-dual-confirm-handoff/00-overview.md) Keep SSOT | Package gate for 56 | Harness + thin note if gap | 57/58 scopes | PASS |

## Dependencies
- Soft: tech-arch `req15-dual-confirm-handoff/` Present · `runtime/03` Keep SSOT
