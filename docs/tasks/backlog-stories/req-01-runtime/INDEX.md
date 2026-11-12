# req-01-runtime — INDEX

> **Пакет:** REQ-01 doge-ai-bridge runtime (pilot)  
> **Parent REQ:** [`REQ-01-doge-ai-bridge-runtime.md`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
> **Architecture:** [`docs/architecture/runtime/`](../../../architecture/runtime/00-overview.md)  
> **Emitted:** 2026-09-12T20:14:11Z · STORY-AIBRIDGE-01…06 · parent REQ-01  
> **P1.3 note (2026-09-12T20:30:51Z):** story 01 pipeline materialized under `epics/EPIC-AIBRIDGE-01-req-01-runtime/` · active `pkg-000001` — backlog file kept.  
> **P3 Done (2026-09-12T20:35:41Z):** STORY-AIBRIDGE-01 🟢 · pytest 21 passed · module `src/aibridge/`  
> **P1.3 note (2026-09-12T20:56:43Z):** story 02 pipeline materialized · active `pkg-000002` — backlog file kept.  
> **P3 Done (2026-09-12T21:03:47Z):** STORY-AIBRIDGE-02 🟢 · pytest 31 passed · content/registry/sessions/gc modules  
> **P1.3 note (2026-09-12T21:16:48Z):** story 03 pipeline materialized · active `pkg-000003` — backlog file kept.  
> **P3 Done (2026-09-12T21:23:18Z):** STORY-AIBRIDGE-03 🟢 · pytest 50 passed, 1 skipped · Responses/tool/budgets modules  
> **P5 APPLY (2026-09-12T21:27:29Z):** G-01 WAIVED→[STORY-AIBRIDGE-07](STORY-AIBRIDGE-07-replayable-history-postgres.md); G-02/G-03 TASKED t07/t08 · `run_mode=aibridge_03_audit_20260912`  
> **P6 Done (2026-09-12T21:30:01Z):** t07/t08 Done · G-02/G-03 CLOSED · pytest 54 passed, 1 skipped  
> **P1.3 note (2026-09-12T21:34:18Z):** story 04 pipeline materialized · active `pkg-000004` — backlog file kept.  
> **P3 Done (2026-09-12T21:40:45Z):** STORY-AIBRIDGE-04 🟢 · pytest 70 passed, 1 skipped · confirm FSM/tokens  
> **P5 APPLY (2026-09-12T21:45:18Z):** G-01 WAIVED→[STORY-AIBRIDGE-08](STORY-AIBRIDGE-08-confirm-token-persistence.md); G-02 TASKED t07 · `run_mode=aibridge_04_audit_20260912`  
> **P6 Done (2026-09-12T21:47:12Z):** t07 Done · G-02 CLOSED · pytest 72 passed, 1 skipped  
> **P1.3 note (2026-09-12T21:50:08Z):** story 05 pipeline materialized · active `pkg-000005` — backlog file kept.  
> **P3 Done (2026-09-12T21:54:48Z):** STORY-AIBRIDGE-05 🟢 · pytest 83 passed, 1 skipped · gateway executor/dry-run/outcomes  
> **P5 APPLY (2026-09-12T21:58:17Z):** G-01/G-02 TASKED t07/t08 · `run_mode=aibridge_05_audit_20260912`  
> **P6 Done (2026-09-12T21:59:49Z):** t07/t08 Done · G-01/G-02 CLOSED · pytest 90 passed, 1 skipped  
> **P1.3 note (2026-09-12T22:02:06Z):** story 06 pipeline materialized · active `pkg-000006` — backlog file kept.  
> **P3 Done (2026-09-12T22:06:45Z):** STORY-AIBRIDGE-06 🟢 · pytest 96 passed, 1 skipped · metrics/audit/ops/wave-1 · next **P4**  
> **P5 APPLY (2026-09-12T22:11:56Z):** G-01 TASKED t07 · G-02 WAIVED · `run_mode=aibridge_06_audit_20260912`  
> **P6 Done (2026-09-12T22:14:25Z):** t07 Done · G-01 CLOSED · pytest 100 passed, 1 skipped · next **P7**

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| Done | STORY-AIBRIDGE-01-channel-facade-auth | [Channel façade + Bearer + event dedupe](STORY-AIBRIDGE-01-channel-facade-auth.md) · [pipeline](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-01-channel-facade-auth/STORY-AIBRIDGE-01-channel-facade-auth.md) | — |
| Done | STORY-AIBRIDGE-02-content-bundle-registry | [Content bundle + Postgres registry + GC](STORY-AIBRIDGE-02-content-bundle-registry.md) · [pipeline](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-02-content-bundle-registry/STORY-AIBRIDGE-02-content-bundle-registry.md) | 01 |
| Done | STORY-AIBRIDGE-03-responses-tool-budgets | [Responses loop, strict tool, LLM budgets](STORY-AIBRIDGE-03-responses-tool-budgets.md) · [pipeline](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-03-responses-tool-budgets/STORY-AIBRIDGE-03-responses-tool-budgets.md) | 02 |
| Done | STORY-AIBRIDGE-04-dual-confirm-tokens | [Dual-confirm FSM + action tokens](STORY-AIBRIDGE-04-dual-confirm-tokens.md) · [pipeline](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-04-dual-confirm-tokens/STORY-AIBRIDGE-04-dual-confirm-tokens.md) | 03 |
| Done | STORY-AIBRIDGE-05-gateway-outcomes | [Gateway executor, dry-run, outcomes](STORY-AIBRIDGE-05-gateway-outcomes.md) · [pipeline](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-05-gateway-outcomes/STORY-AIBRIDGE-05-gateway-outcomes.md) | 04 |
| Done | STORY-AIBRIDGE-06-ops-wave1-proof | [Ops, metrics, wave-1 proof](STORY-AIBRIDGE-06-ops-wave1-proof.md) · [pipeline](../../epics/EPIC-AIBRIDGE-01-req-01-runtime/stories/STORY-AIBRIDGE-06-ops-wave1-proof/STORY-AIBRIDGE-06-ops-wave1-proof.md) | 01–05 |
| Superseded | STORY-AIBRIDGE-07-replayable-history-postgres | [Replayable history Postgres](STORY-AIBRIDGE-07-replayable-history-postgres.md) → **[AIBRIDGE-09](../req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md)** | — |
| Superseded | STORY-AIBRIDGE-08-confirm-token-persistence | [Confirm FSM + token persistence](STORY-AIBRIDGE-08-confirm-token-persistence.md) → **[AIBRIDGE-09](../req-03-runtime-remediation/STORY-AIBRIDGE-09-postgres-ssot-migrations.md)** | — |

**Progress:** 6/6 core Done · 07/08 **Superseded by REQ-03 AIBRIDGE-09** (2026-09-13)  
**Order (historical):** `01 → 02 → 03 → 04 → 05 → 06` · residuals → [`req-03-runtime-remediation`](../req-03-runtime-remediation/INDEX.md)

## Cross-links

- Parent backlog INDEX: [../INDEX.md](../INDEX.md)
- Dashboard: [../../aibridge-mvp-dashboard.md](../../aibridge-mvp-dashboard.md)
- Arch overview + story-slice hints: [00-overview.md §12](../../../architecture/runtime/00-overview.md)
- Pilot recommendations: [ARCH-RECOMMENDATIONS-REQ-01](../../../analysis/ARCH-RECOMMENDATIONS-REQ-01-PILOT-AND-NODE-SCALING.md)
- Out of package: [REQ-02](../../../requirements/REQ-02-DOGE-AI-BRIDGE-POST-PILOT-EVOLUTION.md)
