# req-05-content-phase-a-flat-launch — INDEX

> **Пакет:** REQ-05 Content Phase A — full flat dump + stable-prefix wiring  
> **Parent REQ:** [`REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0 · **Ready for implementation**  
> **Does not modify:** [`REQ-01`](../../../requirements/REQ-01-doge-ai-bridge-runtime.md) body  
> **Related:** [`req-01-runtime`](../req-01-runtime/INDEX.md) (STORY-02 loader/registry Done) · [`REQ-06`](../../../requirements/REQ-06-CONTENT-PHASE-B-SCALABLE-PACKAGING.md) (after Phase A) · [`REQ-07` OpenAI strict-schema compat](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) (context seams for this package; AC live in REQ-07)  
> **Emitted:** 2026-09-16T14:25:00Z · materialize from REQ→backlog plan (operator «запиши») · aligned REQ-05 v0.2.0  
> **Architecture skills:** [`ARCHITECTURE-SKILLS-ACTIVATED.md`](./ARCHITECTURE-SKILLS-ACTIVATED.md)  
> **Technical architecture:** [`TECHNICAL-ARCHITECTURE.md`](./TECHNICAL-ARCHITECTURE.md) (REQ-05 Phase A) · related focus arch: [`../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) · interview: [`../../../analysis/zeya888.target-tech-arch-interview-REQ-07-openai-strict-schema-compat-2026-09-24.md`](../../../analysis/zeya888.target-tech-arch-interview-REQ-07-openai-strict-schema-compat-2026-09-24.md)  
> **P1.3 note (2026-09-16T12:04:31Z):** story 19 pipeline materialized under `epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/` · active `pkg-000016` — backlog file kept  
> **P3 note (2026-09-16T12:10:09Z):** STORY-19 Implemented · ADR-1 wire · gate PASS · next **P4**  
> **P6 note (2026-09-16T12:19:26Z):** G-01/G-02 CLOSED (t06/t07) · G-03 WAIVED · next **P7**  
> **P1.3 note (2026-09-16T12:28:09Z):** story 20 pipeline materialized · active `pkg-000017` — backlog file kept  
> **P3 note (2026-09-16T12:32:27Z):** STORY-20 Implemented · ADR-2 full `files[]` · gate PASS · next **P4**  
> **P5 note (2026-09-16T12:41:29Z):** G-01/G-03 TASKED (t06/t07) · G-02 WAIVED · `run_mode=aibridge_20_audit_20260916` · next **P6**  
> **P6 note (2026-09-16T12:47:01Z):** G-01/G-03 CLOSED · G-02 WAIVED · next **P7**  
> **P1.3 note (2026-09-16T12:52:52Z):** story 21 pipeline materialized · active `pkg-000018` — backlog file kept · next **P2**  
> **P3 note (2026-09-16T12:55:52Z):** STORY-21 Implemented · ADR-3 OAS COPY + Phase A pins · gate PASS · next **P4**  
> **P5 note (2026-09-16T13:23:26Z):** G-01/G-02 WAIVED · TASKED=0 · activation=none · skip P6 · next **P7**  
> **P1.3 note (2026-09-16T13:36:35Z):** story 22 pipeline materialized · active `pkg-000019` — backlog file kept · next **P2**  
> **P3 note (2026-09-16T13:41:13Z):** STORY-22 Implemented · ADR-4 proof tests + smoke · gate PASS · next **P4**  
> **P5 note (2026-09-16T13:47:10Z):** G-01 TASKED (t06) · G-02 WAIVED · activation=`run_mode=aibridge_22_audit_g01_intake` · next **P6**  
> **P6 note (2026-09-16T13:49:48Z):** t06 Done · G-01 CLOSED · gate PASS · next **P7**  
> **Dashboard:** [`../../aibridge-mvp-dashboard.md`](../../aibridge-mvp-dashboard.md)

## Stories

| Status | Key | Title | Depends |
|--------|-----|-------|---------|
| Implemented | STORY-AIBRIDGE-19-assembled-instructions-engine-wire | [Assembled instructions → stable prefix + tools](STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) · [pipeline](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-19-assembled-instructions-engine-wire/STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) | — |
| Implemented | STORY-AIBRIDGE-20-full-instructions-manifest | [Full flat manifest (complete dump)](STORY-AIBRIDGE-20-full-instructions-manifest.md) · [pipeline](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-20-full-instructions-manifest/STORY-AIBRIDGE-20-full-instructions-manifest.md) | — |
| Implemented | STORY-AIBRIDGE-21-oas-image-env-docs | [OpenAPI in image + Phase A env docs](STORY-AIBRIDGE-21-oas-image-env-docs.md) · [pipeline](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-21-oas-image-env-docs/STORY-AIBRIDGE-21-oas-image-env-docs.md) | — |
| Implemented | STORY-AIBRIDGE-22-content-phase-a-proof | [Phase A proof tests + smoke](STORY-AIBRIDGE-22-content-phase-a-proof.md) · [pipeline](../../epics/EPIC-AIBRIDGE-03-req-05-content-phase-a/stories/STORY-AIBRIDGE-22-content-phase-a-proof/STORY-AIBRIDGE-22-content-phase-a-proof.md) | 19, 20, 21 |

## Build order

`19 ∥ 20 ∥ 21 → 22`

## Out of package

- REQ-06 profiles / multi-repo publish  
- ADMIN/*, mockups, channel OAS redesign
