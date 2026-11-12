# STORY-AIBRIDGE-41 — OpenAI schema compatibility projection

## Meta
- **Key:** `STORY-AIBRIDGE-41-openai-schema-projection`
- **Status:** ✅ P6 Done · next **P7** · `run_mode=aibridge_41_audit_20260924` · pkg-000040 · 2026-09-24T11:08:43Z
- **Parent Epic:** [`EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md`](../../EPIC-AIBRIDGE-05-req-07-openai-strict-schema-compat.md)
- **source:** `backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md`
- **decision_ref:** [`STORY-AIBRIDGE-41-….md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-41-openai-schema-projection.md) · [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) · [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.1–2.2
- **Package:** [`req-07-openai-strict-schema-compat/INDEX.md`](../../../../backlog-stories/req-07-openai-strict-schema-compat/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000040-20260924-epic-aibridge-05-story-41-openai-schema-projection.yaml` (immutable under override)
- **P1 materialize:** 2026-09-24T10:55:45Z
- **P3 close:** 2026-09-24T11:00:27Z · [run-summary](../../../../run-reports/run-summary-20260924-1100-story-aibridge-41-p3.md)
- **P4 audit:** 2026-09-24T11:02:40Z · [p4-audit](../../../../analysis/p4-audit-STORY-AIBRIDGE-41-openai-schema-projection-20260924.md)
- **P6 close:** 2026-09-24T11:08:43Z · [p6](../../../../run-reports/run-summary-20260924-1108-story-aibridge-41-p6.md)
- **Gate:** [t04](./task-aibridge-41-t04-story-gate/README.md) **PASS** · G-01/G-02 CLOSED (t05–t06)

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| REQ-07 projection | [`REQ-07`](../../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §§1,5–8.1 · AIB-COMPAT-01/02/03/06/09–12 |
| Tech-arch dual schemas | [`TECH-ARCH-REQ-07`](../../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.1–2.2 |
| Code seam | `src/aibridge/tool_gen.py` · `deployment.py` · `readiness.py` |

## Scope
In `generate_strict_tool`: deep-copy; recursive OpenAI projection removing schema keyword `uniqueItems`; post-assert; keep `strict: true`. Policy constant. No disk writes. Optional redacted init (non-blocking for readiness).

## Вне scope
- Canonical uniqueItems enforcement (STORY-42); ValidationContext bind (43); live Telegram (45); editing pack JSON; `strict: false`.

## Context
Pack retains `"uniqueItems": true` on houses; OpenAI-facing tool strips keyword via projection (P3).

## Target / AC
- [x] AC-01 / AC-02: pack JSON + Story Intake YAML unchanged on disk after generation.
- [x] AC-03: OpenAI tool has no `uniqueItems`, `strict: true`, name `postStoryDraftStash`.
- [x] AC-05 / AC-07: projection at deploy/init; deterministic; input object unchanged.
- [x] Fail closed on projection error or remaining forbidden keyword (`tool_gen_failed:*`).
- [x] Nested tasks Done at execute.

## Nested tasks (pkg-000040 order)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-41-t01-openai-unsupported-keywords-policy](./task-aibridge-41-t01-openai-unsupported-keywords-policy/README.md) | policy + strip helper | **Done** |
| t02 | [task-aibridge-41-t02-generate-strict-tool-projection](./task-aibridge-41-t02-generate-strict-tool-projection/README.md) | wire generate_strict_tool | **Done** |
| t03 | [task-aibridge-41-t03-compat-projection-tests](./task-aibridge-41-t03-compat-projection-tests/README.md) | AC/T-COMPAT tests | **Done** |
| t04 | [task-aibridge-41-t04-story-gate](./task-aibridge-41-t04-story-gate/README.md) | story AC gate | **PASS** |
| t05 | [task-aibridge-41-t05-audit-g01-keyword-helper-align](./task-aibridge-41-t05-audit-g01-keyword-helper-align/README.md) | G-01 keyword helper | **Done** |
| t06 | [task-aibridge-41-t06-audit-g02-t-compat-06-assert](./task-aibridge-41-t06-audit-g02-t-compat-06-assert/README.md) | G-02 T-COMPAT-06 | **Done** |
