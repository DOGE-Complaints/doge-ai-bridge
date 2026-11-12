# STORY-AIBRIDGE-46 — Worker entry + S2S auth + idempotency

## Meta
- **Key:** `STORY-AIBRIDGE-46-worker-entry-s2s-idempotency`
- **Status:** P6 Done · t08–t09 Done · pkg-000049 · next **P7** · `run_mode=aibridge_46_audit_20261014` · 2026-10-14T12:33:45Z
- **Parent Epic:** [`EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md`](../../EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker.md)
- **source:** `backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md`
- **decision_ref:** [`STORY-AIBRIDGE-46-….md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) · [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1–2,4.1,5 AC-01,8.1–2 · [`01-entry-auth-idempotency.md`](../../../../architecture/sense-brief-poster-worker/01-entry-auth-idempotency.md)
- **Package:** [`req-09-req13-sense-brief-poster-worker/INDEX.md`](../../../../backlog-stories/req-09-req13-sense-brief-poster-worker/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000049-20261014-epic-aibridge-07-story-46-worker-entry-s2s-idempotency.yaml`
- **P1 materialize:** 2026-10-14T11:54:36Z · [p1 draft](../../../../../../.cursor/plans/p1_aibridge_46_scaffold_20261014T114919Z.plan.md)
- **Gate:** [t07](./task-aibridge-46-t07-story-gate/README.md) · **PASS** · [p3](../../../../run-reports/run-summary-20261014-1202-story-aibridge-46-p3.md)
- **Depends:** none (foundation)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-09 | [`REQ-09`](../../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| Entry / auth / idempotency | [`01-entry-auth-idempotency.md`](../../../../architecture/sense-brief-poster-worker/01-entry-auth-idempotency.md) |
| Overview DP1/DP3/DP5 | [`00-overview.md`](../../../../architecture/sense-brief-poster-worker/00-overview.md) |

## Scope
- Separate worker accept entry ≠ `/v1/channel/` interview/channel handler (same image OK).
- Dedicated worker S2S token auth; reject channel Bearer / citizen creds.
- Idempotency on Issue id + generation-version (same version → no-op / same outcome).
- Fail-closed when worker enabled and required S2S config missing.
- Exact HTTP path / env var **names** remain Open (do not invent SSOT).

## Вне scope
- Brief/LLM, poster, storage upload, gateway bind client (47–49).
- Changing Telegram interview / REQ-05 behavior.
- Gateway public wire; SPA.
- Inventing final HTTP path / env / JSON key SSOT.

## Context
Channel façade Present (`CHANNEL_PATH_PREFIX = "/v1/channel/"`). Worker accept Present: `POST /v1/worker/sense-brief/accept` · `AIBRIDGE_WORKER_SENSE_BRIEF_*` · `worker_accept.py` / `auth.is_worker_s2s_authorized`. Brief/poster/bind (47–49) still Absent. Soft: gateway Wave-1 nudge contract Present (path strings Open).

## Target / AC
- [x] AC-09-01: Worker accept path is not the interview/channel handler.
- [x] Channel Bearer cannot authorize worker accept.
- [x] Valid worker S2S admits accept (further pipeline may still fail).
- [x] Same Issue+generation-version duplicate accept is idempotent (no required second full compute).
- [x] Worker enabled + missing S2S → fail-closed (no accept).
- [x] Nested tasks Done at execute

**Implement names (P3):** `POST /v1/worker/sense-brief/accept` · `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` · `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` · JSON `issue_id` / `generation_version` / optional `corpus`.

## Nested tasks (pkg-000049)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-46-t01-worker-enable-settings-fail-closed](./task-aibridge-46-t01-worker-enable-settings-fail-closed/README.md) | T01 settings fail-closed | Done |
| t02 | [task-aibridge-46-t02-separate-accept-entry](./task-aibridge-46-t02-separate-accept-entry/README.md) | T02 · AC-09-01 | Done |
| t03 | [task-aibridge-46-t03-worker-s2s-auth](./task-aibridge-46-t03-worker-s2s-auth/README.md) | T03 · DP3 | Done |
| t04 | [task-aibridge-46-t04-accept-logical-inputs](./task-aibridge-46-t04-accept-logical-inputs/README.md) | T04 inputs | Done |
| t05 | [task-aibridge-46-t05-idempotency-issue-version](./task-aibridge-46-t05-idempotency-issue-version/README.md) | T05 · DP5 | Done |
| t06 | [task-aibridge-46-t06-entry-auth-idempotency-tests](./task-aibridge-46-t06-entry-auth-idempotency-tests/README.md) | T06 tests | Done |
| t07 | [task-aibridge-46-t07-story-gate](./task-aibridge-46-t07-story-gate/README.md) | story AC gate | PASS |
| t08 | [task-aibridge-46-t08-audit-g01-sync-verified-state](./task-aibridge-46-t08-audit-g01-sync-verified-state/README.md) | P4 G-01 | Done |
| t09 | [task-aibridge-46-t09-audit-g03-channel-eq-worker-test](./task-aibridge-46-t09-audit-g03-channel-eq-worker-test/README.md) | P4 G-03 | Done |
