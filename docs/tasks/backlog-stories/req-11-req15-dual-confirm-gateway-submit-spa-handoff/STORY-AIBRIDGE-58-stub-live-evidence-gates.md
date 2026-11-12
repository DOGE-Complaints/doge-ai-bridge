# STORY-AIBRIDGE-58 — Stub + live evidence gates

## Meta
- **Key:** `STORY-AIBRIDGE-58-stub-live-evidence-gates`
- **Status:** Done · P8 · pkg-000061 · Product Done (**gate/docs scope**) · 1e2229c/2d850b6/406ef49 · 2026-11-01T18:32:20Z · residual AC-07 live **Explicit Partial** / E2E **Unknown** · **not** live SUCCESS Done · [pipeline](../../epics/EPIC-AIBRIDGE-09-req-11-req15-dual-confirm-gateway-submit-spa-handoff/stories/STORY-AIBRIDGE-58-stub-live-evidence-gates/STORY-AIBRIDGE-58-stub-live-evidence-gates.md) · [p3](../../run-reports/run-summary-20261101-1823-story-aibridge-58-p3.md) · [p4](../../analysis/p4-audit-STORY-AIBRIDGE-58-stub-live-evidence-gates-20261101.md) · [p5](../../run-reports/run-summary-20261101-1829-story-aibridge-58-p5-disposition.md) · [p7](../../analysis/p7-reaudit-STORY-AIBRIDGE-58-stub-live-evidence-gates-20261101.md)
- **Parent REQ:** [`REQ-11`](../../../requirements/REQ-11-REQ15-DUAL-CONFIRM-GATEWAY-SUBMIT-SPA-HANDOFF.md) AC-07 · arch D5
- **Tech-arch:** [`req15-dual-confirm-handoff/03-verify-evidence-coexistence.md`](../../../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [56](STORY-AIBRIDGE-56-keep-pipe-confirm-stash-spa-verify.md) · [57](STORY-AIBRIDGE-57-l11-invalidation-seam.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-01T14:15:37Z
- **Tech subtasks:** Present (arch-bound table below; pre-P1.3)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Operator Q2:** this story closes **gate/docs** for AC-07; mandatory live run is **not** required in this wave (Partial until ops window).

## Scope
- Stub/harness evidence matrix for confirm→stash→continuation (required for tech accept of this package).
- Document live Pass gate: ≥1 Telegram→bridge→gateway→SPA open **only when** ops evidence window open; else AC-07 = Partial (not Done).
- Cite peers gateway 59 / spa 25 / telegram REQ-01 as verify-first (no invent APIs).

## Out of scope
- Opening the live window / executing live E2E in this story (ops; Q2).
- Implementing telegram transport / SPA / gateway redesign.
- Per-provider live matrix body (REQ-12) beyond pointer.
- Checker/PII role body (REQ-13 — operator Q1).

## Verified current state
- Stub matrix: **Present** — `docs/runtime-docs/06-ac07-stub-live-evidence-gates.md` §1 · pytest 56/57 + story58 docs gate.
- Live E2E evidence: **Unknown** / not claimed Done · AC-07 live **Explicit Partial**.
- Arch D5 split gate locked.
- Invented Railway / live SUCCESS: **Absent**.

## Target / AC
- [x] AC-AIB-11-07 stub side: documented + runnable harness evidence for Keep pipe (ties to 56).
- [x] AC-AIB-11-07 live side: runbook/checklist Present; Done only with recorded live path when window open; otherwise explicit Partial — **Partial**.
- [x] Honesty note in package INDEX: stub ≠ Product/child Done for AC-07.

## Code points
- Tests from 56 (+ optional seam cases from 57)
- `docs/runtime-docs/06-ac07-stub-live-evidence-gates.md` · `tests/test_story_58_stub_live_evidence_gates.py`

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Stub evidence matrix: map 56 (+ soft 57) harness tests → AC-01/03/04/05/06; required for tech accept | [`03` §1](../../../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md) stub row | AC-AIB-11-07 stub side | `06-ac07-…` §1 · tests 56/57/58 | Live E2E run | Done |
| **t02** | Live Pass runbook/checklist: Telegram→bridge→gateway→SPA; Done only with ops window; else Partial | [`03` §1](../../../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md) live rows (Q2) | AC-AIB-11-07 live side | `06-ac07-…` §2 Explicit Partial | Opening ops window / mandatory live this wave | Done |
| **t03** | Peer verify-first cite table in matrix/runbook (gateway 59, spa 25, telegram REQ-01); no invent APIs | [`03` §2](../../../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md) | Boundary honesty | `06-ac07-…` §3 | Gateway/SPA redesign | Done |
| **t04** | Confirm package INDEX honesty: stub ≠ AC-07 Done / Product Story Done | [`03` §1](../../../architecture/req15-dual-confirm-handoff/03-verify-evidence-coexistence.md) honesty | Process gate | [`INDEX.md`](INDEX.md) | — | Done |
| **t08** | Story gate: stub matrix Present; live Explicit Partial without window | [`00-overview`](../../../architecture/req15-dual-confirm-handoff/00-overview.md) evidence row | Package gate for 58 | After t01–t04 | REQ-12 per-provider live body | PASS |

## Dependencies
- STORY-AIBRIDGE-56 · soft: 57
- Soft peers: gateway 59 · spa 25 · telegram REQ-01
