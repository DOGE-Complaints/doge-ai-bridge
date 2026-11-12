# req-13-req15-semantic-state-roles-instruction-assembly — INDEX

> **Пакет:** REQ-13 — REQ15 semantic state / roles / instruction assembly (hybrid C)  
> **Parent REQ:** [`REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md)  
> **Parent product:** [`REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md`](../../../../../docs/requirements%20backlog/REQ15-DOGEstonia-Interview-DeepSeek-And-Telegram-Channel.md)  
> **Tech-arch:** [`../../../architecture/req15-semantic-state-roles/00-overview.md`](../../../architecture/req15-semantic-state-roles/00-overview.md) (`01`–`03`)  
> **Interview:** [`../../../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md`](../../../analysis/zeya888.target-tech-arch-interview-req15-semantic-state-roles-2026-11-02.md)  
> **T1 / readiness:** [`../../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md`](../../../../../docs/analysis/req15-t1-keep-adapt-replace-2026-11-01.md) · [`req15-aibridge-wave-readiness-2026-11-01.md`](../../../../../docs/analysis/req15-aibridge-wave-readiness-2026-11-01.md) §5.3  
> **Emitted:** 2026-11-02T08:32:08Z · materialize REQ→backlog (operator Q1: AC-05 Product Done = gate/docs + Explicit Partial)  
> **Tech subtasks:** **67 Done · Product Done · Code Done** · pkg-000070 · P8 · E1 Locked · AC-05 live Explicit Partial · (62–67)  
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)  
> **Operator locks:** L13-1 soft confirm · L13-2 volume/fixture · L13-3 A+transition C · arch D1–D6 · **stub fixtures ≠ GPT UI checkout**  
> **Honesty:** STORY-67 **Code Done** · AC-05 live = **Explicit Partial** until refreshed GPT-48 Export Pass + ops window; **no invent** Railway / live SUCCESS · stale evidence ≠ Export Pass · E1 inventory/hash wire **Locked**

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| **Done** · Product Done · pkg-000065 · G-02 WAIVED ASGI residual | STORY-AIBRIDGE-62-semantic-state-store-invalidation | [Semantic state store + invalidation](STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-62-semantic-state-store-invalidation/STORY-AIBRIDGE-62-semantic-state-store-invalidation.md) · [runtime 09](../../../runtime-docs/09-semantic-state-store-invalidation.md) · [p7 reaudit](../../../analysis/p7-reaudit-STORY-AIBRIDGE-62-semantic-state-store-invalidation-20261102.md) | — |
| **Done** · Product Done · pkg-000066 · P8 `1efea66`/`893cd39`/`9eb32f0` · G-02 WAIVED ASGI | STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures | [Roles + coordinator + assembly (fixtures)](STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) · [runtime 10](../../../runtime-docs/10-roles-coordinator-assembly.md) · [p5 disposition](../../../analysis/p5-disposition-STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures-20261102.md) | soft 62 |
| **Done** · Product Done · pkg-000067 · P8 `2368a35`/`71d9958`/`ae01652` · AC-05 Explicit Partial residual | STORY-AIBRIDGE-64-content-parity-stub-live-evidence | [Content parity + stub/live evidence](STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-64-content-parity-stub-live-evidence/STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) · [runtime 11](../../../runtime-docs/11-content-volume-parity-stub-live-evidence.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-64-content-parity-stub-live-evidence-20261102.md) | soft 63 |
| **Done** · Product Done · pkg-000068 · G-02 Lifted · P8 `0ccedc6`/`15fc620`/`fde569a` | STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire | [ASGI channel semantic+roles wire](STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire/STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) · [runtime 12](../../../runtime-docs/12-asgi-channel-semantic-roles-wire.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire-20261104.md) | 62–64 |
| **Done** · Product Done · pkg-000069 · P8 `36b45bd`/`4c6d327`/`a678b32` · G-02 WAIVE→67 | STORY-AIBRIDGE-66-roles-schema-channel-cutover | [Roles-schema channel cutover](STORY-AIBRIDGE-66-roles-schema-channel-cutover.md) · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-66-roles-schema-channel-cutover/STORY-AIBRIDGE-66-roles-schema-channel-cutover.md) · [runtime 13](../../../runtime-docs/13-roles-schema-channel-cutover.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-66-roles-schema-channel-cutover-20261104.md) | 65 |
| **Done** · Product Done · Code Done · pkg-000070 · P8 `75f5f95`/`ca77c69`/`d6430fe` · AC-05 Explicit Partial (t07) · stale ≠ Export Pass | STORY-AIBRIDGE-67-consume-parity-volume-evidence | [Consume parity + volume evidence](STORY-AIBRIDGE-67-consume-parity-volume-evidence.md) · [pipeline](../../epics/EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly/stories/STORY-AIBRIDGE-67-consume-parity-volume-evidence/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md) · [p7](../../../analysis/p7-reaudit-STORY-AIBRIDGE-67-consume-parity-volume-evidence-20261105.md) · [runtime 14](../../../runtime-docs/14-hybrid-c-volume-consume-parity-runbook.md) | 66 Done |

## Build order

`62 → 63 → 64 → 65 → 66 → 67` (**Done**)

## Out of package

- GPT UI REQ-48 authoring / export bodies (peer — blocks live AC-05 Pass only)
- REQ-12 provider HTTP · REQ-11 gateway redesign · telegram transport
- Worker REQ-09 · NEW ADMIN / mockups
