# STORY-AIBRIDGE-17 — SPA HTTPS continuation E2E (tracker)

## Meta
- **Key:** `STORY-AIBRIDGE-17-spa-https-continuation-e2e`
- **Status:** 🟢 Done (P8 · queue exhausted)
- **Parent Epic:** [`EPIC-AIBRIDGE-02-req-03-runtime-remediation.md`](../../EPIC-AIBRIDGE-02-req-03-runtime-remediation.md)
- **source:** `backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`
- **decision_ref:** [`STORY-AIBRIDGE-17-spa-https-continuation-e2e.md`](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) · [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6 R3-P1-08 · REQ-01 §16 / §21
- **Parent REQ:** [`REQ-03`](../../../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §6 R3-P1-08
- **Package:** [`req-03-runtime-remediation/INDEX.md`](../../../../backlog-stories/req-03-runtime-remediation/INDEX.md)
- **Siblings:** [14](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md)
- **Operator decision:** aibridge owns **gate/tracker** only; SPA profile owns UI/E2E execution and evidence artifact. Link spa `STORY-SPA-*` / run-summary when available. **Do not invent spa product work.**
- **Active pkg (wave):** `pkg-000015-20260913-epic-aibridge-02-story-17-spa-https-continuation-e2e.yaml`
- **P1 materialize:** 2026-09-13T18:20:16Z
- **P3 Done:** 2026-09-13T18:23:58Z
- **P5 APPLY:** 2026-09-13T18:28:13Z · G-01/G-02 **WAIVED** · activation **none** · skip P6 · [p5 draft](../../../../../../../../.cursor/plans/p5_aibridge17_gap_20260913T182813Z.plan.md)
- **P8 Done:** 2026-09-13T18:30:59Z · feat `b45c6e4` · docs `f758d20` · test n/a · **no push** · **queue exhausted**

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| R3-P1-08 gate SSOT | [`r3-p1-08-spa-https-continuation-gate.md`](../../../../../ops/r3-p1-08-spa-https-continuation-gate.md) |
| Evidence BLOCKED | [`spa-https-continuation-evidence-BLOCKED-20260913.md`](../../../../../ops/spa-https-continuation-evidence-BLOCKED-20260913.md) |
| MVP dashboard wave-2 block | [`aibridge-mvp-dashboard.md`](../../../../aibridge-mvp-dashboard.md) §Wave-2 |
| continuation URL builder | `src/aibridge/gateway.py` `build_continuation_url` |
| SPA redirect base | `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` |

## Scope
- Track pilot-policy real-device HTTPS SPA continuation E2E as a **wave-2 residents gate** for aibridge.
- DoD: evidence pack (spa story Done / run-summary / checklist) proving continuation URL path works on HTTPS device — not re-implement spa UI inside aibridge.

## Вне scope
- Implementing spa frontend in `doge-ai-bridge`.
- Multi-replica load (18).

## Verified current state (post-P3)
- R3-P1-08 tracker checklist on disk; spa owner slots remain **Unknown** (no invent).
- Spa evidence pack: **BLOCKED** — no `STORY-SPA-*` / run-summary / device proof linked.
- Dashboard §Wave-2 treats residents as **blocked** until spa evidence linked.
- No spa UI code added in aibridge.

## Target / AC
- [x] Evidence linked from this story proving R3-P1-08 — **via BLOCKED residual** (spa pack absent; no invented PASS). Live PASS deferred to spa unblock.
- [x] aibridge dashboard can treat residents wave-2 blocked until evidence present.

## Точки в коде / docs
- `docs/ops/r3-p1-08-spa-https-continuation-gate.md`
- `docs/ops/spa-https-continuation-evidence-BLOCKED-20260913.md`
- `docs/tasks/aibridge-mvp-dashboard.md`
- `src/aibridge/gateway.py` (`build_continuation_url`) — reference only

## Dependencies
- [14](../../../../backlog-stories/req-03-runtime-remediation/STORY-AIBRIDGE-14-p1-ops-schema-restart.md)

## Nested tasks (pkg-000015 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-02-17-t01-r3-p1-08-checklist-ssot](./task-aibridge-02-17-t01-r3-p1-08-checklist-ssot/README.md) | Scope #1 · R3-P1-08 | Done |
| t02 | [task-aibridge-02-17-t02-spa-owner-evidence-link-protocol](./task-aibridge-02-17-t02-spa-owner-evidence-link-protocol/README.md) | Scope #2 · Operator | Done |
| t03 | [task-aibridge-02-17-t03-dashboard-wave2-blocked-until-evidence](./task-aibridge-02-17-t03-dashboard-wave2-blocked-until-evidence/README.md) | Target #2 | Done |
| t04 | [task-aibridge-02-17-t04-evidence-pack-or-blocked-residual](./task-aibridge-02-17-t04-evidence-pack-or-blocked-residual/README.md) | Scope #2 · Target #1 | Done |
| t05 | [task-aibridge-02-17-t05-story-acceptance-verification](./task-aibridge-02-17-t05-story-acceptance-verification/README.md) | Target AC gate | Done |
