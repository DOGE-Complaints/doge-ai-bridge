# QA inbound/outbound — persistent docs

Долгоживущая зона для прогона и матриц QA stories **23–35** (пакет `qa-inbound-outbound-data-flow`). Не заменяет backlog/epic pipeline — только ops-facing копии и мануал.

| Doc | Role |
|-----|------|
| [`TEST-MANUAL.md`](./TEST-MANUAL.md) | Как поднять сервер и прогнать pytest-сьют |
| [`TRACEABILITY-MATRIX.md`](./TRACEABILITY-MATRIX.md) | Matrix IDs ↔ stories (ops copy · sync from package; 190 rows after 36–40) |
| [`MATRIX-COVERAGE-VERIFICATION.md`](./MATRIX-COVERAGE-VERIFICATION.md) | Statement coverage check (persistent copy) |
| [`pytest-report-20260918.md`](./pytest-report-20260918.md) | Прогон 2026-09-18: 232 passed, 12 skipped (no disposable PG) |
| [`pytest-report-20260918-rerun.md`](./pytest-report-20260918-rerun.md) | Re-run с disposable PG: **244 passed, 0 skipped** (+ agent sandbox 232/12) |
| [`pytest-report-20260918-post36-40.md`](./pytest-report-20260918-post36-40.md) | Post 36–40: **263 passed / 0 skipped** (operator + PG); matrix honesty note |
| [`test-qualification-20260918-post36-40.md`](./test-qualification-20260918-post36-40.md) | Pointer → package SSOT квалификации post-36–40 |
| [`test-qualification-20260918.md`](./test-qualification-20260918.md) | Pointer → current + prior qualification SSOTs |
| Package SSOT (post) | [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TEST-QUALIFICATION-20260918-post36-40.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TEST-QUALIFICATION-20260918-post36-40.md) |
| Package SSOT (prior) | [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TEST-QUALIFICATION-20260918.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TEST-QUALIFICATION-20260918.md) |
| `pytest-report-*.md` | Последующие факты прогона (pass/fail/skip + gaps) |

## Upstream SSOT

| Artifact | Path |
|----------|------|
| QA guide | [`../../tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md`](../../tasks/qa-requirements/AIBRIDGE-QA-INBOUND-OUTBOUND-DATA-FLOW-GUIDE.md) |
| Package INDEX | [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/INDEX.md) |
| Tech arch | [`../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md`](../../tasks/backlog-stories/qa-inbound-outbound-data-flow/TECHNICAL-ARCHITECTURE.md) |
| Web runbook | [`../../runbooks/aibridge-web-service-local-railway.md`](../../runbooks/aibridge-web-service-local-railway.md) |

When matrix IDs change in the package, refresh the copies in this folder.
