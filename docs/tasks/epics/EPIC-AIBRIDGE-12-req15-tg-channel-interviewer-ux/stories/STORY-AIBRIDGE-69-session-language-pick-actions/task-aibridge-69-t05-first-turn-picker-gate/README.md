# Task: First-turn picker gate

**Status:** Done · P3 2026-11-06T12:32:14Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-69-session-language-pick-actions.md`  
**Parent story:** [`STORY-AIBRIDGE-69-session-language-pick-actions.md`](../STORY-AIBRIDGE-69-session-language-pick-actions.md)  
**P1 scaffold:** 2026-11-06T12:29:18Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_69_scaffold_20261106T122734Z.plan.md) · pkg-000072  
**Maps:** t05 · AC-69-01

## Purpose

gate before interview engine advance

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/02 §2 · §6
- Inbound `language_code` Present (telegram mapper · schemas); engine consume Absent until implement.
- Lang-pick actions Absent until t04; `ConfirmSession.locale` Absent until t02.
- Honesty: locale SSOT=ConfirmSession · EN=🇺🇸 · no invent full i18n / live TG SUCCESS · STORY-68 OOS.

## AC/DoD

- [x] AC-69-01 DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: channel.py / coordinator gate
- [x] OOS respected: Block on STORY-68 CONTINUE
- [x] Skill python-pro present.
- [x] No invent Railway/live TG SUCCESS · no full i18n invent · locale not in semantic_state facts.

## Where to change (P3)

- channel.py / coordinator gate

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story69 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-69-t05-first-turn-picker-gate.md`](./acceptance-verification-task-aibridge-69-t05-first-turn-picker-gate.md)

### P3 evidence (2026-11-06T12:32:14Z)

- channel._maybe_language_pick_gate · test_t05_*
- unclear gates engine; clear soft-binds
