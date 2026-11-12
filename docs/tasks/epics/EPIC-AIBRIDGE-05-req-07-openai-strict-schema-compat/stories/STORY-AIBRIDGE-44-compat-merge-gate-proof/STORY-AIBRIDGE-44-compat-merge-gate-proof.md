# STORY-AIBRIDGE-44 — Compat merge-gate proof (automated)

## Meta
- **Key:** `STORY-AIBRIDGE-44-compat-merge-gate-proof`
- **Status:** ✅ P6 Done · G-01/G-02 CLOSED · next **P7** · `run_mode=aibridge_44_audit_20260924` · pkg-000043 · 2026-09-24T12:01:55Z · **implemented, live verification pending**
- **Parent Epic:** [`EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md`](../../EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md)
- **source:** `backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md`
- **decision_ref:** [`STORY-AIBRIDGE-44-….md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md) · [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §11.1–11.4 · AC-08 · [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §5.1
- **Package:** [`req-07-openai-strict-schema-compat/INDEX.md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/INDEX.md)
- **Skill declared:** `test-master`
- **Active pkg (wave):** `pkg-000043-20260924-epic-aibridge-05-story-44-compat-merge-gate-proof.yaml`
- **P1 materialize:** 2026-09-24T11:49:26Z
- **P3 close:** 2026-09-24T11:52:39Z · [run-summary](../../../../run-reports/run-summary-20260924-1152-story-aibridge-44-p3.md)
- **Gate:** [t05](./task-aibridge-44-t05-story-gate/README.md) **PASS**
- **Depends:** STORY-41 · STORY-42 · STORY-43 (Done/Implemented)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-07 tests / AC-08 | [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §11.1–11.4 · AC-08 |
| Merge gate | [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §5.1 |
| Suite | `tests/test_req07_merge_gate.py` · fixture `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json` |

## Scope
Automated merge-gate suite proving:
1. `uniqueItems` absent from entire OpenAI-facing `tools` payload (fake/recording Responses transport);
2. canonical pack unchanged by projection;
3. Gate 2 rejects duplicate `houses`;
4. missing/invalid ValidationContext → `/readyz` not_ready;
5. regression fixture for prior `invalid_function_parameters` / uniqueItems path.

After this story **Implemented**: package/focus status **implemented, live verification pending** (not production verified / Done for REQ-07).

## Вне scope
- Real Telegram + live OpenAI call (45); weakening pack schema; using live as sole proof.

## Context
P3: `tests/test_req07_merge_gate.py` covers TECH-ARCH §5.1 #1–#5 via RecordingResponsesClient / Gate 2 / readyz / fixture.

## Target / AC
- [x] Merge-gate checklist green in CI/local (TECH-ARCH §5.1).
- [x] Responses payload contract §11.4: Responses-flat tool, `store:false`, `parallel_tool_calls:false`, no `uniqueItems` under `tools[*].parameters`.
- [x] T-READY behaviors covered without calling OpenAI from `/readyz`.
- [x] Fixture path: `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json`.
- [x] Nested tasks Done at execute.

## Nested tasks (pkg-000043)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-44-t01-responses-tools-payload-no-uniqueitems](./task-aibridge-44-t01-responses-tools-payload-no-uniqueitems/README.md) | §5.1#1 + §11.4 | **Done** |
| t02 | [task-aibridge-44-t02-canonical-pack-unchanged-by-projection](./task-aibridge-44-t02-canonical-pack-unchanged-by-projection/README.md) | §5.1#2 / AC-01 | **Done** |
| t03 | [task-aibridge-44-t03-gate2-duplicate-houses-and-invalid-params-fixture](./task-aibridge-44-t03-gate2-duplicate-houses-and-invalid-params-fixture/README.md) | §5.1#3+#5 | **Done** |
| t04 | [task-aibridge-44-t04-readyz-vc-and-t-ready-no-openai](./task-aibridge-44-t04-readyz-vc-and-t-ready-no-openai/README.md) | §5.1#4 / T-READY | **Done** |
| t05 | [task-aibridge-44-t05-story-gate](./task-aibridge-44-t05-story-gate/README.md) | story AC gate | **PASS** |
| t06 | [task-aibridge-44-t06-audit-g02-tighten-outbound-tool-assert](./task-aibridge-44-t06-audit-g02-tighten-outbound-tool-assert/README.md) | G-02 assert tighten | **Done** · P6 |
| t07 | [task-aibridge-44-t07-audit-g01-backlog-verified-sync](./task-aibridge-44-t07-audit-g01-backlog-verified-sync/README.md) | G-01 backlog Verified | **Done** · P6 |

### P5 disposition → P6 CLOSED (2026-09-24T12:01:55Z)

| Gap | Sev | Disposition | Task |
|-----|-----|-------------|------|
| G-01 | Low | TASKED → **CLOSED** (P6) | t07 Done |
| G-02 | Low | TASKED → **CLOSED** (P6) | t06 Done |
| G-03 | Low | **WAIVED** out-of-DoD-story-44-merge-gate-only | — |
| G-04 | Info | **WAIVED** info-nonblocking | — |

**activation:** `run_mode=aibridge_44_audit_20260924` · [p6](../../../../run-reports/run-summary-20260924-1201-story-aibridge-44-p6.md) · next=P7
