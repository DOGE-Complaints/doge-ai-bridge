# STORY-AIBRIDGE-61 — Interview provider stub + live evidence gates

## Meta
- **Key:** `STORY-AIBRIDGE-61-interview-provider-stub-live-evidence`
- **Status:** **Done** · **Product Done** · pkg-000064 · P8 SHAs `05609c2`/`d45d872`/`a8b064c` · live **Explicit Partial** residual · [pipeline](../../epics/EPIC-AIBRIDGE-10-req-12-req15-interview-deepseek-openai-providers/stories/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence/STORY-AIBRIDGE-61-interview-provider-stub-live-evidence.md) · [p7 reaudit](../../../analysis/p7-reaudit-STORY-AIBRIDGE-61-interview-provider-stub-live-evidence-20261101.md)
- **Parent REQ:** [`REQ-12`](../../../requirements/REQ-12-REQ15-INTERVIEW-DEEPSEEK-OPENAI-PROVIDERS.md) §4.4 · AC-04 · parent AC-10
- **Tech-arch:** [`req15-interview-providers/03-verify-evidence-coexistence.md`](../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [59](STORY-AIBRIDGE-59-interview-port-env-fail-closed.md) · [60](STORY-AIBRIDGE-60-openai-deepseek-interview-adapters.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-11-01T19:38:04Z
- **Tech subtasks:** Present (arch-bound; pre-P1.3)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)

## Scope
- Stub/harness: both adapters + fail-closed unset/unknown/incomplete nest + worker env cannot select interview (ties 59/60) — required for tech accept.
- Live evidence path **per provider** documented; Pass only with ops window + recorded path; else AC-04 = Explicit Partial for that provider.
- Honesty: stub ≠ Product Story Done; cite peers (worker arch, REQ-11 confirm Keep, REQ-13 when Present).

## Out of scope
- Opening live windows / mandatory live this wave.
- Implementing adapters (60) beyond citing harness.
- Worker REQ-10 live matrix body; telegram transport; gateway redesign.

## Verified current state
- Per-provider interview live matrix / runbook: **Present** as Explicit Partial — `docs/runtime-docs/08-ac04-interview-stub-live-evidence-gates.md` (no live Pass claimed).
- Arch D5 split gate locked in `03-verify-evidence-coexistence.md`.
- Present wire recording path: `app.py:427–428` — not typed provider Pass.
- Env template §4b Present for ops to fill real keys before live.

## Target / AC
- [x] AC-AIB-12-04 stub side: harness evidence for both providers + fail-closed/orthogonality.
- [x] AC-AIB-12-04 live side: runbook per provider Present; **Explicit Partial** (ops window not open).
- [x] Package INDEX honesty note: stub ≠ full AC-04 Done.

## Code points
- Tests from 59/60 · thin runtime-docs note path chosen at implement (no invent Railway / live SUCCESS)

## Technical subtasks (arch-bound; pre-P1.3)

| ID | Subtask | Arch cite | AC / DoD | Touch (as-is) | OOS | Status |
|----|---------|-----------|----------|---------------|-----|--------|
| **t01** | Stub evidence matrix: map 59/60 harness → AC-01/02/03/05 | [`03` §1](../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md) stub | AC-AIB-12-04 stub | Tests from 59/60 · thin runtime-docs at implement | Live E2E run | Done |
| **t02** | Live Pass runbook **per provider**; Done only with ops window; else Explicit Partial | [`03` §1](../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md) live | AC-AIB-12-04 live | Runbook/checklist doc | Opening ops window / invent Railway SUCCESS | Done |
| **t03** | Peer cite table: worker arch, REQ-11 confirm, REQ-13, GPT-48, telegram/gateway no keys | [`03` §2](../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md) | boundary honesty | Matrix/runbook peer rows | Worker/gateway redesign | Done |
| **t04** | Package INDEX honesty: stub ≠ AC-04 / Product Done | [`03` §1](../../../architecture/req15-interview-providers/03-verify-evidence-coexistence.md) honesty | process gate | [`INDEX.md`](INDEX.md) | — | Done |
| **t08** | Story gate: stub matrix Present; live Partial without window | [`00-overview`](../../../architecture/req15-interview-providers/00-overview.md) evidence row | Package gate for 61 | After t01–t04 | Adapter implement beyond cite | **PASS** |

## Dependencies
- STORY-AIBRIDGE-59 · soft: 60
