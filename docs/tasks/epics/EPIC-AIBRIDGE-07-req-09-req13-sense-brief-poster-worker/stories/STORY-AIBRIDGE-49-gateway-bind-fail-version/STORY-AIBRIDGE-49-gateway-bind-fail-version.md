# STORY-AIBRIDGE-49 — Gateway bind-in + fail classes + regenerate version

## Meta
- **Key:** `STORY-AIBRIDGE-49-gateway-bind-fail-version`
- **Status:** P5 Done · TASKED=0 · WAIVED G-01…G-03 · pkg-000052 · next **P7** (skip P6) · activation **none** · 2026-10-14T14:25:21Z
- **Parent Epic:** [`EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md`](../../EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md)
- **source:** `backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-49-gateway-bind-fail-version.md`
- **decision_ref:** [`STORY-AIBRIDGE-49-….md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-49-gateway-bind-fail-version.md) · [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) · [`03-storage-bind-verify.md`](../../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)
- **Package:** [`req-09-req13-sense-brief-poster-worker/INDEX.md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000052-20261014-epic-aibridge-07-story-49-gateway-bind-fail-version.yaml`
- **P1 materialize:** 2026-10-14T14:08:54Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_49_scaffold_20261014T140705Z.plan.md)
- **P3 Execute:** 2026-10-14T14:13:53Z · [p3](../../../../run-reports/run-summary-20261014-1413-story-aibridge-49-p3.md)
- **P4 Audit:** 2026-10-14T14:21:01Z · [p4](../../../../analysis/p4-audit-STORY-AIBRIDGE-49-gateway-bind-fail-version-20261014.md)
- **P5 APPLY:** 2026-10-14T14:25:21Z · [p5](../../../../run-reports/run-summary-20261014-1425-story-aibridge-49-p5-disposition.md)
- **Gate:** [t07](./task-aibridge-49-t07-story-gate/README.md) · **PASS**
- **Depends:** STORY-AIBRIDGE-47 · STORY-AIBRIDGE-48

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Bind / fail / version | [`03-storage-bind-verify.md`](../../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) |
| Implement | `src/aibridge/sense_bind/` |

## Scope
- Outbound bind-in (service-auth); success/fail payloads; AC-09-04/06; PII-safe signals.

## Вне scope
- Sibling 57 apply; SPA; STORY-50 harness; invent path/key SSOT.

## Context
Brief + poster Present. Bind-in — **Present** (P3).

## Target / AC
- [x] AC-09-04: Failure returns explicit error to gateway (no fake brief).
- [x] AC-09-06: Regenerate produces new version id/URL distinguishable from prior.
- [x] Success bind includes brief-derived apply payload + HTTPS URL + version (keys Open).
- [x] Nested tasks Done at execute

**Implement names (P3):** `src/aibridge/sense_bind/` · path `/v1/issue-sense-brief/bind` (implement) · keys `apply`/`poster_url`/`reason_class` · DP9 wire as enum values.

## Nested tasks (pkg-000052)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-49-t01-outbound-bind-in-client-service-auth](./task-aibridge-49-t01-outbound-bind-in-client-service-auth/README.md) | T01 | **Done** |
| t02 | [task-aibridge-49-t02-success-bind-payload](./task-aibridge-49-t02-success-bind-payload/README.md) | T02 | **Done** |
| t03 | [task-aibridge-49-t03-fail-bind-dp9-reason-classes](./task-aibridge-49-t03-fail-bind-dp9-reason-classes/README.md) | T03 | **Done** |
| t04 | [task-aibridge-49-t04-regenerate-version-distinguishability](./task-aibridge-49-t04-regenerate-version-distinguishability/README.md) | T04 | **Done** |
| t05 | [task-aibridge-49-t05-pii-safe-observability](./task-aibridge-49-t05-pii-safe-observability/README.md) | T05 | **Done** |
| t06 | [task-aibridge-49-t06-bind-success-fail-tests-gateway-mock](./task-aibridge-49-t06-bind-success-fail-tests-gateway-mock/README.md) | T06 | **Done** |
| t07 | [task-aibridge-49-t07-story-gate](./task-aibridge-49-t07-story-gate/README.md) | gate | **PASS** |
