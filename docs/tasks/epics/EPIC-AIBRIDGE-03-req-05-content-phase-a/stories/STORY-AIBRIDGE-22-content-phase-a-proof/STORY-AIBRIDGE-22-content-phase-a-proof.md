# STORY-AIBRIDGE-22 — Content Phase A proof (tests + smoke)

## Meta
- **Key:** `STORY-AIBRIDGE-22-content-phase-a-proof`
- **Status:** 🟢 Implemented (P6 · next P7)
- **Parent Epic:** [`EPIC-AIBRIDGE-03-req-05-content-phase-a.md`](../../EPIC-AIBRIDGE-03-req-05-content-phase-a.md)
- **source:** `backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md`
- **decision_ref:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-22-content-phase-a-proof.md) · [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.5 · §4.5 · R5-A-05 · [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) ADR-4
- **Parent REQ:** [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.5 · §4.5 · R5-A-05
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/INDEX.md)
- **Siblings:** [19](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [20](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-20-full-instructions-manifest.md) · [21](../../../../backlog-stories/req-05-content-phase-a-flat-launch/STORY-AIBRIDGE-21-oas-image-env-docs.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) §8 ADR-4 · §13 sequence
- **Skill declared:** `test-master` — [SKILL.md](../../../../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md) · pytest `python-pro`
- **Active pkg (wave):** `pkg-000019-20260916-epic-aibridge-03-story-22-content-phase-a-proof.yaml`
- **P1 materialize:** 2026-09-16T13:36:35Z
- **P3 closed:** 2026-09-16T13:41:13Z
- **Gate:** [acceptance-verification-task-aibridge-22-t05-story-gate.md](./acceptance-verification-task-aibridge-22-t05-story-gate.md) PASS
- **Run summary:** [run-summary-20260916-1341-story-aibridge-22-p3.md](../../../../run-reports/run-summary-20260916-1341-story-aibridge-22-p3.md)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-05 §4.5 / R5-A-05 | [`REQ-05`](../../../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) |
| ADR-4 fail-closed / proof | [`TECHNICAL-ARCHITECTURE.md`](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) §8 |
| Wire / manifest / OAS | stories 19–21 Done |
| Smoke target | `docs/ops/req-05-phase-a-smoke.md` (P3) |

## Scope
- Automated tests: content_configured + full manifest load → stable prefix / engine несёт non-empty assembled text; coverage обязательных basenames / completeness из REQ-05 §4.2.
- Broken/missing path → readiness fail-closed (не silent empty prompt).
- Ops smoke checklist: `/healthz` 200; полный env → `/readyz` не `content_bundle_not_ready` из‑за OAS/manifest/wiring.
- Phase B не требуется для REQ-05 Done.

## Вне scope
- Live Railway SUCCESS invent; n8n/Telegram; REQ-06; inventing channel OAS paths.

## Verified current state
- Readiness: `src/aibridge/readiness.py`; `/readyz` in `app.py`.
- Proof tests: `tests/test_story_22_phase_a_proof.py` (6 passed · 2026-09-16T13:41:13Z).
- Smoke checklist: `docs/ops/req-05-phase-a-smoke.md` — present.
- Depends 19+20+21: Done on disk (wire, full manifest, OAS COPY).

## Target / AC
- [x] REQ-05 §4.5 automated + smoke checklist at `docs/ops/req-05-phase-a-smoke.md`.
- [x] REQ-05 Done #4.6: Phase B not required.

## Техническое решение (projected)

- **Approach (ADR-4):** pytest — after `create_app` with content env: `interview_engine.instructions` non-empty; `prompt_channel=="prefix"`; optional `_build_request` / recording client shows prefix system message; broken paths → `/readyz` 503. Completeness assert dir vs manifest. Materialize smoke checklist at named path (healthz + readyz).
- **Depends:** 19+20+21 Done first.
- **Skill:** test-master · python-pro  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](../../../../backlog-stories/req-05-content-phase-a-flat-launch/TECHNICAL-ARCHITECTURE.md) ADR-4

## Точки в коде
- `tests/**`, `src/aibridge/app.py`, `readiness.py`, `interview.py`, `content.py`
- Acceptance target (not yet on disk): `docs/ops/req-05-phase-a-smoke.md`

## Dependencies
- **Requires Todo→Done:** 19, 20, 21 — **satisfied** (Implemented/Done this wave).

## Nested tasks (pkg-000019 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-22-t01-test-engine-wired](./task-aibridge-22-t01-test-engine-wired/README.md) | Scope #1 · engine wired + prefix | Done |
| t02 | [task-aibridge-22-t02-test-readyz-fail-closed](./task-aibridge-22-t02-test-readyz-fail-closed/README.md) | Scope #2 · readyz fail-closed | Done |
| t03 | [task-aibridge-22-t03-test-manifest-completeness](./task-aibridge-22-t03-test-manifest-completeness/README.md) | Scope #1 · completeness | Done |
| t04 | [task-aibridge-22-t04-smoke-checklist](./task-aibridge-22-t04-smoke-checklist/README.md) | Scope #3 · ops smoke md | Done |
| t05 | [task-aibridge-22-t05-story-gate](./task-aibridge-22-t05-story-gate/README.md) | §4.5 + §4.6 gate | Done |
| t06 | [task-aibridge-22-t06-audit-g01-intake-hermetic](./task-aibridge-22-t06-audit-g01-intake-hermetic/README.md) | P5 G-01 · intake hermetic | Done |
