# Task: Bind locale on pick consume

**Status:** Done · P3 2026-11-06T12:32:14Z  
**Skill declared:** python-pro  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req15-tg-channel-interviewer-ux/STORY-AIBRIDGE-69-session-language-pick-actions.md`  
**Parent story:** [`STORY-AIBRIDGE-69-session-language-pick-actions.md`](../STORY-AIBRIDGE-69-session-language-pick-actions.md)  
**P1 scaffold:** 2026-11-06T12:29:18Z · [p1 APPLIED](../../../../../../../../.cursor/plans/p1_aibridge_69_scaffold_20261106T122734Z.plan.md) · pkg-000072  
**Maps:** t06 · AC-69-03

## Purpose

bind + apply subsequent turns

## Code Facts (verify exists)

- Arch cite: docs/architecture/req15-tg-channel-interviewer-ux/02 §3
- Inbound `language_code` Present (telegram mapper · schemas); engine consume Absent until implement.
- Lang-pick actions Absent until t04; `ConfirmSession.locale` Absent until t02.
- Honesty: locale SSOT=ConfirmSession · EN=🇺🇸 · no invent full i18n / live TG SUCCESS · STORY-68 OOS.

## AC/DoD

- [x] AC-69-03 DoD met or Explicit Partial honesty recorded.
- [x] Touch limited to: interview/channel wire
- [x] OOS respected: Full UI i18n catalog
- [x] Skill python-pro present.
- [x] No invent Railway/live TG SUCCESS · no full i18n invent · locale not in semantic_state facts.

## Where to change (P3)

- interview/channel wire

## Verification commands

```bash
cd doge-ai-bridge && .venv/bin/python -m pytest -q --tb=line  # focused story69 as cited in P3
```

## Evidence

- Acceptance: [`acceptance-verification-task-aibridge-69-t06-bind-locale-on-consume.md`](./acceptance-verification-task-aibridge-69-t06-bind-locale-on-consume.md)

### P3 evidence (2026-11-06T12:32:14Z)

- consume bind locale · locale_prompt_prefix · test_t06_consume_bind_locale_no_gateway
- PICK consume binds; never gateway
