# req-03-runtime-remediation — INDEX

> **Пакет:** REQ-03 runtime remediation (agreed)  
> **Parent REQ:** [`REQ-03-RUNTIME-REMEDIATION-AGREED.md`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) v0.2.1 · **Ready for implementation**  
> **Does not modify:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
> **Related:** [`req-01-runtime`](../req-01-runtime/INDEX.md) (01–06 Done; 07/08 **Superseded by AIBRIDGE-09**)  
> **Emitted:** 2026-09-13T15:08:35Z · operator decisions: 07/08→09; SPA tracker+spa evidence; delete ops-only Unknown path; P2 Deferred; story 11 unsplit  
> **P1.3 note (2026-09-13T15:16:41Z):** story 09 pipeline materialized under `epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/` · active `pkg-000007` — backlog file kept.  
> **P3 Done (2026-09-13T15:25:46Z):** STORY-AIBRIDGE-09 🟢 · pytest 109 passed, 1 skipped · migrations + pg_runtime · next **P4**  
> **P5 APPLY (2026-09-13T15:29:22Z):** G-01/G-02 TASKED t08/t09 · `run_mode=aibridge_09_audit_20260913`  
> **P6 Done (2026-09-13T15:35:44Z):** G-01/G-02 CLOSED · pytest 113 passed, 1 skipped · next **P7**  
> **P1.3 note (2026-09-13T15:40:24Z):** story 10 pipeline materialized · active `pkg-000008` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T15:46:08Z):** STORY-AIBRIDGE-10 🟢 · pytest 112 passed, 14 skipped · Responses adapter + flat tools + prompt xor · next **P4**  
> **P5 APPLY (2026-09-13T15:49:46Z):** G-01/G-02/G-03 TASKED t06–t08 · `run_mode=aibridge_10_audit_20260913`  
> **P6 Done (2026-09-13T15:52:34Z):** G-01/G-02/G-03 CLOSED · pytest 114 passed, 14 skipped · next **P7**  
> **P1.3 note (2026-09-13T15:55:55Z):** story 11 pipeline materialized · active `pkg-000009` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T16:03:23Z):** STORY-AIBRIDGE-11 🟢 · pytest 122 passed, 14 skipped · coordinator + pause/resume + Send · next **P4**  
> **P5 APPLY (2026-09-13T16:07:28Z):** G-01/G-02/G-03 TASKED t08–t10 · `run_mode=aibridge_11_audit_20260913`  
> **P6 Done (2026-09-13T16:12:58Z):** G-01/G-02/G-03 CLOSED · pytest 125 passed, 15 skipped · next **P7**  
> **P1.3 note (2026-09-13T16:15:49Z):** story 12 pipeline materialized · active `pkg-000010` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T16:22:32Z):** STORY-AIBRIDGE-12 🟢 · pytest 136 passed, 15 skipped · env/readyz/dry-run/500 · next **P4**  
> **P5 APPLY (2026-09-13T16:26:12Z):** G-01/G-02/G-03 TASKED t07–t09 · `run_mode=aibridge_12_audit_20260913`  
> **P6 Done (2026-09-13T16:30:46Z):** G-01/G-02/G-03 CLOSED · pytest 146 passed, 15 skipped · next **P7**  
> **P1.3 note (2026-09-13T16:34:47Z):** story 13 pipeline materialized · active `pkg-000011` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T16:49:42Z):** STORY-AIBRIDGE-13 🟢 · pytest 170 passed, 1 skipped · wave-1 ASGI E2E · next **P4**  
> **P5 APPLY (2026-09-13T16:54:19Z):** G-01/G-02/G-03 TASKED t07–t09 · `run_mode=aibridge_13_audit_20260913`  
> **P6 Done (2026-09-13T16:58:55Z):** G-01/G-02/G-03 CLOSED · pytest 177 passed, 1 skipped · next **P7**  
> **P1.3 note (2026-09-13T17:03:24Z):** story 14 pipeline materialized · active `pkg-000012` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T17:14:26Z):** STORY-AIBRIDGE-14 🟢 · pytest 191 passed, 1 skipped · ops/schema/restart/Dockerfile · next **P4**  
> **P5 APPLY (2026-09-13T17:18:05Z):** G-01/G-02/G-03 TASKED t08–t10 · `run_mode=aibridge_14_audit_20260913`  
> **P6 Done (2026-09-13T17:23:30Z):** G-01/G-02/G-03 CLOSED · pytest 196 passed, 1 skipped · next **P7**  
> **P1.3 note (2026-09-13T17:28:28Z):** story 15 pipeline materialized · active `pkg-000013` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T17:34:04Z):** STORY-AIBRIDGE-15 🟢 · pytest 203 passed, 1 skipped · §6.1 checklist + contract tests · live residual BLOCKED · next **P4**  
> **P5 APPLY (2026-09-13T17:38:54Z):** STORY-15 G-01/G-02 **WAIVED** · **activation: none** · skip P6 · next **P7**  
> **P8 Done (2026-09-13T17:42:08Z):** STORY-15 commits feat/test/docs · **next STORY-AIBRIDGE-16**  
> **P1.3 note (2026-09-13T17:43:00Z):** story 16 pipeline materialized · active `pkg-000014` — backlog file kept · next **P2**  
> **P3 Done (2026-09-13T17:49:14Z):** STORY-AIBRIDGE-16 🟢 · pytest 177 passed, 38 skipped · privacy TTL/ops-delete · **no** channel OAS invent · next **P4**  
> **P5 APPLY (2026-09-13T17:52:16Z):** G-01/G-02/G-03 TASKED t07–t09 · `run_mode=aibridge_16_audit_20260913`  
> **P6 Done (2026-09-13T17:55:59Z):** G-01/G-02/G-03 CLOSED · pytest 181 passed, 39 skipped · next **P7**  
> **P8 Done (2026-09-13T18:18:12Z):** STORY-16 commits feat/test/docs · **next STORY-AIBRIDGE-17**  
> **P1.3 note (2026-09-13T18:20:16Z):** story 17 pipeline materialized · active `pkg-000015` — backlog file kept · next **P2** · tracker/gate only (spa owns evidence)  
> **P3 Done (2026-09-13T18:23:58Z):** STORY-AIBRIDGE-17 🟢 · R3-P1-08 checklist + dashboard wave-2 block · spa evidence **BLOCKED** · no spa invent · next **P4**  
> **P5 APPLY (2026-09-13T18:28:13Z):** STORY-17 G-01/G-02 **WAIVED** · **activation: none** · skip P6 · next **P7**  
> **P8 Done (2026-09-13T18:30:59Z):** STORY-17 commits feat/docs · **queue exhausted** (Deferred 18 only)  
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| Done | STORY-AIBRIDGE-09-postgres-ssot-migrations | [Postgres SSOT + migrations + concurrency](STORY-AIBRIDGE-09-postgres-ssot-migrations.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-09-postgres-ssot-migrations/STORY-AIBRIDGE-09-postgres-ssot-migrations.md) | — (after Done 01–06) |
| Done | STORY-AIBRIDGE-10-responses-adapter-tools | [Responses adapter + flat tools + prompt](STORY-AIBRIDGE-10-responses-adapter-tools.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-10-responses-adapter-tools/STORY-AIBRIDGE-10-responses-adapter-tools.md) | 09 |
| Done | STORY-AIBRIDGE-11-coordinator-pause-resume-send | [Coordinator + pause/resume + Send txn](STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-11-coordinator-pause-resume-send/STORY-AIBRIDGE-11-coordinator-pause-resume-send.md) | 09, 10 |
| Done | STORY-AIBRIDGE-12-readyz-env-dryrun-gate | [Env + /readyz + 500 + dry-run gate](STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-12-readyz-env-dryrun-gate/STORY-AIBRIDGE-12-readyz-env-dryrun-gate.md) | 09 |
| Done | STORY-AIBRIDGE-13-wave1-asgi-e2e | [Wave-1 ASGI E2E fake/dry-run + Postgres](STORY-AIBRIDGE-13-wave1-asgi-e2e.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-13-wave1-asgi-e2e/STORY-AIBRIDGE-13-wave1-asgi-e2e.md) | 09–12 |
| Done | STORY-AIBRIDGE-14-p1-ops-schema-restart | [P1 ops + full schema + restart tests](STORY-AIBRIDGE-14-p1-ops-schema-restart.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-14-p1-ops-schema-restart/STORY-AIBRIDGE-14-p1-ops-schema-restart.md) | 13 |
| Done | STORY-AIBRIDGE-15-n8n-telegram-gate | [Live n8n/Telegram integration gate](STORY-AIBRIDGE-15-n8n-telegram-gate.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-15-n8n-telegram-gate/STORY-AIBRIDGE-15-n8n-telegram-gate.md) | 13 |
| Done | STORY-AIBRIDGE-16-privacy-retention | [Privacy retention enforcement](STORY-AIBRIDGE-16-privacy-retention.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-16-privacy-retention/STORY-AIBRIDGE-16-privacy-retention.md) | 09, 14 |
| Done | STORY-AIBRIDGE-17-spa-https-continuation-e2e | [SPA HTTPS continuation E2E (tracker)](STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) · [pipeline](../../epics/EPIC-AIBRIDGE-02-req-03-runtime-remediation/stories/STORY-AIBRIDGE-17-spa-https-continuation-e2e/STORY-AIBRIDGE-17-spa-https-continuation-e2e.md) | 14 |
| Deferred | STORY-AIBRIDGE-18-p2-replicas-observability | [P2 replicas / observability](STORY-AIBRIDGE-18-p2-replicas-observability.md) | 14+ |

**Progress (active):** 9/9 Done · **Deferred:** 1 (18) · **Active pkg:** pkg-000015 (story 17 P8 · **queue exhausted**) · wave-2 residents **blocked** pending spa evidence  
**Order:** `09 → 10 → 11 ∥ 12 → 13 → 14 ∥ 15 → 16 → 17` · then 18 after first node

## Operator decisions (2026-09-13)

1. STORY-07/08 → **Superseded by 09** (pointers in req-01-runtime).  
2. STORY-17 = aibridge **gate/tracker**; execution/evidence owned by spa profile.  
3. Operator session-delete = **ops-only authz**; HTTP path **Unknown** until explicit decision — do not invent channel OAS.  
4. STORY-18 = **Deferred** (вне active %).  
5. Coordinator + Send txn = **single** STORY-11.

## Cross-links

- Parent backlog INDEX: [../INDEX.md](../INDEX.md)
- Gap analysis: [req-01-runtime-code-gap-2026-09-13.md](../../../analysis/req-01-runtime-code-gap-2026-09-13.md)
- Out of package: [REQ-02](../../../requirements/REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md), ADMIN/*, mockups, optional token-hash UX
