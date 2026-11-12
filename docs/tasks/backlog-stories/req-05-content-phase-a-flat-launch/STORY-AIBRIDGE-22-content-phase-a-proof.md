# STORY-AIBRIDGE-22 — Content Phase A proof (tests + smoke)

## Meta
- **Key:** `STORY-AIBRIDGE-22-content-phase-a-proof`
- **Status:** 🟢 Implemented (P6 · next P7)
- **Pipeline:** [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-22-content-phase-a-proof/STORY-AIBRIDGE-22-content-phase-a-proof.md)
- **Active pkg:** `pkg-000019-20260916-epic-aibridge-03-story-22-content-phase-a-proof.yaml`
- **P1 materialize:** 2026-09-16T13:36:35Z
- **P3 closed:** 2026-09-16T13:41:13Z
- **Gate:** [acceptance-verification … t05](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-22-content-phase-a-proof/acceptance-verification-task-aibridge-22-t05-story-gate.md) PASS
- **Parent REQ:** [`REQ-05`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 §2.5 · §4.5 · R5-A-05
- **Package:** [`req-05-content-phase-a-flat-launch/INDEX.md`](INDEX.md)
- **Siblings:** [19](STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [20](STORY-AIBRIDGE-20-full-instructions-manifest.md) · [21](STORY-AIBRIDGE-21-oas-image-env-docs.md)
- **Tech decomposition:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) §8 ADR-4 · §13 sequence
- **Skill declared:** `test-master` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md)

## Scope
- Automated tests: content_configured + full manifest load → stable prefix / engine несёт non-empty assembled text; coverage обязательных basenames / completeness из REQ-05 §4.2.
- Broken/missing path → readiness fail-closed (не silent empty prompt).
- Ops smoke checklist: `/healthz` 200; полный env → `/readyz` не `content_bundle_not_ready` из‑за OAS/manifest/wiring.
- Phase B не требуется для REQ-05 Done.

## Вне scope
- Live Railway SUCCESS invent; n8n/Telegram; REQ-06; inventing channel OAS paths.
- Creating pipeline task folders until P1.3 (name ≠ create).

## Verified current state
- Proof tests: `tests/test_story_22_phase_a_proof.py` (6 passed · 2026-09-16T13:41:13Z).
- Smoke checklist: `docs/ops/req-05-phase-a-smoke.md` — present.
- Depends 19+20+21: Done.

## Target / AC
- [x] REQ-05 §4.5 automated + smoke checklist at `docs/ops/req-05-phase-a-smoke.md`.
- [x] REQ-05 Done #4.6: Phase B not required.

## Техническое решение (projected)

- **Approach (ADR-4):** pytest — after `create_app` with content env: `interview_engine.instructions` non-empty; `prompt_channel=="prefix"`; optional `_build_request` / recording client shows prefix system message; broken paths → `/readyz` 503. Completeness assert dir vs manifest. Materialize smoke checklist at named path (healthz + readyz).
- **Depends:** 19+20+21 Done first.
- **Skill:** test-master  
- **Arch:** [TECHNICAL-ARCHITECTURE.md](./TECHNICAL-ARCHITECTURE.md) ADR-4

## Nested tasks (materialized — pkg-000019)

> Pipeline: [`STORY-AIBRIDGE-22-content-phase-a-proof.md`](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-22-content-phase-a-proof/STORY-AIBRIDGE-22-content-phase-a-proof.md)

| Task | Folder | Status | Essence |
|------|--------|--------|---------|
| **T01** | `task-aibridge-22-t01-test-engine-wired` | Done | Test: content_configured → non-empty instructions + prefix channel |
| **T02** | `task-aibridge-22-t02-test-readyz-fail-closed` | Done | Test: missing/broken content → `/readyz` 503 |
| **T03** | `task-aibridge-22-t03-test-manifest-completeness` | Done | Test: dir children vs `files[]` (omit = fail) |
| **T04** | `task-aibridge-22-t04-smoke-checklist` | Done | Write `docs/ops/req-05-phase-a-smoke.md` (healthz/readyz) |
| **T05** | `task-aibridge-22-t05-story-gate` | Done | All §4.5 AC + REQ-05 Phase A Done gate |
| **T06** | `task-aibridge-22-t06-audit-g01-intake-hermetic` | Done | P5 G-01 · intake hermetic in proof helper |

## Точки в коде
- `tests/test_story_22_phase_a_proof.py`, `src/aibridge/app.py`, `readiness.py`, `interview.py`, `content.py`
- Smoke: `docs/ops/req-05-phase-a-smoke.md`

## Dependencies
- **Requires Todo→Done:** 19, 20, 21 — **satisfied** (Done this wave).
