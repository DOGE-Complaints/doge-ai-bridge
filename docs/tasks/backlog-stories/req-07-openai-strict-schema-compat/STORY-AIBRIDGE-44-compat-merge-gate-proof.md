# STORY-AIBRIDGE-44 — Compat merge-gate proof (automated)

## Meta
- **Key:** `STORY-AIBRIDGE-44-compat-merge-gate-proof`
- **Status:** P6 Done · G-01/G-02 CLOSED · next P7 · `run_mode=aibridge_44_audit_20260924` · pkg-000043 · 2026-09-24T12:01:55Z · **implemented, live verification pending**
- **Parent REQ:** [`REQ-07`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §11.1–11.4 · AC-08
- **Tech-arch:** [`TECH-ARCH-REQ-07`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §5.1 merge gate
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [41](STORY-AIBRIDGE-41-openai-schema-projection.md) · [42](STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [43](STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [45](STORY-AIBRIDGE-45-compat-live-telegram-verify.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md)
- **Emitted:** 2026-09-24T10:28:49Z

## Scope
- Automated merge-gate suite proving:
  1. `uniqueItems` absent from entire OpenAI-facing `tools` payload (fake/recording Responses transport);
  2. canonical pack unchanged by projection;
  3. Gate 2 rejects duplicate `houses`;
  4. missing/invalid ValidationContext → `/readyz` not_ready;
  5. regression fixture for prior `invalid_function_parameters` / uniqueItems path.
- After this story **Implemented**: package/focus status **implemented, live verification pending** (not production verified / Done for REQ-07).

## Out of scope
- Real Telegram + live OpenAI call (45); weakening pack schema; using live as sole proof.

## Verified current state
- P3+ merge-gate: `tests/test_req07_merge_gate.py` proves TECH-ARCH §5.1 #1–#5 (RecordingResponsesClient · pack unchanged · Gate 2 duplicates · VC readyz · fixture).
- Sibling suites present: `tests/test_openai_schema_projection.py` (T-COMPAT) · `tests/test_uniqueitems_gate2.py` (T-UNIQUE) · `tests/test_validation_context_bind.py` (VC bind).
- Fixture: `tests/fixtures/openai/invalid_function_parameters_uniqueitems.json`.
- Focus status: **implemented, live verification pending** (live AC-09 = STORY-45).
- Emit-era note: pre-P3 Verified claimed T-COMPAT/T-UNIQUE absent — superseded by suites above.

## Target / AC
- [x] Merge-gate checklist green in CI/local (TECH-ARCH §5.1).
- [x] Responses payload contract §11.4: Responses-flat tool, `store:false`, `parallel_tool_calls:false`, no `uniqueItems` under `tools[*].parameters`.
- [x] T-READY behaviors covered without calling OpenAI from `/readyz`.
- [x] Fixture path chosen at implement under `tests/fixtures/` (`openai/invalid_function_parameters_uniqueitems.json`).

## Code points
- `tests/` modules per REQ §11; `src/aibridge/` seams from 41–43

## Dependencies
- Requires **41**, **42**, **43** Done/Implemented
