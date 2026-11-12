# STORY-AIBRIDGE-17 — SPA HTTPS continuation E2E (tracker)

## Meta
- **Key:** `STORY-AIBRIDGE-17-spa-https-continuation-e2e`
- **Status:** 🟢 Done (P8 · queue exhausted)
- **Pipeline:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-17-spa-https-continuation-e2e/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md)
- **Active pkg:** `pkg-000015-20260913-epic-aibridge-02-story-17-spa-https-continuation-e2e.yaml`
- **P1 materialize:** 2026-09-13T18:20:16Z
- **P3 Done:** 2026-09-13T18:23:58Z · spa evidence **BLOCKED** residual · no spa invent
- **P5 APPLY:** 2026-09-13T18:28:13Z · G-01/G-02 **WAIVED** · activation **none** · skip P6
- **P8 Done:** 2026-09-13T18:30:59Z · feat `b45c6e4` · docs `f758d20` · **no push**
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6 R3-P1-08
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Siblings:** [14](STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md)
- **Operator decision:** aibridge owns **gate/tracker** only; SPA profile owns UI/E2E execution and evidence artifact. Link spa `STORY-SPA-*` / run-summary when available.

## Scope
- Track pilot-policy real-device HTTPS SPA continuation E2E as a **wave-2 residents gate** for aibridge.
- DoD: evidence pack (spa story Done / run-summary / checklist) proving continuation URL path works on HTTPS device — not re-implement spa UI inside aibridge.

## Вне scope
- Implementing spa frontend in `doge-ai-bridge`.
- Multi-replica load (18).

## Verified current state
- SPA backlog owner story key: **Unknown** (not invented).
- P3: R3-P1-08 checklist + dashboard wave-2 **blocked** + spa evidence **BLOCKED** residual on disk.

## Target / AC
- [x] Evidence linked from this story proving R3-P1-08 — **BLOCKED residual** (spa pack absent; no invented PASS).
- [x] aibridge dashboard can treat residents wave-2 blocked until evidence present.

## Dependencies
- [14](STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
