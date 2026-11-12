# STORY-AIBRIDGE-41 — OpenAI schema compatibility projection

## Meta
- **Key:** `STORY-AIBRIDGE-41-openai-schema-projection`
- **Status:** P6 Done · next P7 · `run_mode=aibridge_41_audit_20260924` · pkg-000040 · 2026-09-24T11:08:43Z
- **Parent REQ:** [`REQ-07`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §§1,5–8.1 · AIB-COMPAT-01/02/03/06/09–12
- **Tech-arch:** [`TECH-ARCH-REQ-07`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §2.1–2.2
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [42](STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [43](STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [44](STORY-AIBRIDGE-44-compat-merge-gate-proof.md) · [45](STORY-AIBRIDGE-45-compat-live-telegram-verify.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-09-24T10:28:49Z

## Scope
- In `generate_strict_tool`: deep-copy; recursive OpenAI projection removing schema keyword `uniqueItems` (not data fields named similarly); post-assert forbidden keywords absent; keep `strict: true`.
- Code-level policy constant (e.g. `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS`).
- No disk writes to Story Intake OAS or pack JSON; tool stored once in `DeploymentBundleState.strict_tool` and reused.
- Optional redacted init event (REQ §10) — must not be a readiness dependency if logging fails.

## Out of scope
- Canonical `uniqueItems` enforcement (42); ValidationContext bind (43); live Telegram (45); editing pack JSON; `strict: false`; channel OAS; broad strip of unknown keywords.

## Verified current state
- P3 2026-09-24T11:00:27Z: `OPENAI_UNSUPPORTED_SCHEMA_KEYWORDS` + `project_schema_for_openai` in `src/aibridge/tool_gen.py`; wired in `generate_strict_tool`; pack on disk still has `uniqueItems` (`schema-packs.uus_veerenni_civic.v3.payload.schema.json`); OpenAI tool projection strips keyword (tests 12 passed).

## Target / AC
- [x] AC-01 / AC-02: canonical pack JSON + Story Intake YAML unchanged on disk after generation.
- [x] AC-03: OpenAI-facing tool has no `uniqueItems`, `strict: true`, name `postStoryDraftStash`.
- [x] AC-05 / AC-07: projection at deploy/init; deterministic serialization; input Python object unchanged (T-COMPAT-02/03).
- [x] Fail closed on projection error or remaining forbidden keyword (`tool_gen_failed:*`).

## Code points
- `src/aibridge/tool_gen.py`, `deployment.py`, `readiness.py` (`_strict_tool_ok`)
- Tests: extend `tests/test_tool_gen.py` and/or dedicated module (REQ §11.1) — create at implement, not now

## Dependencies
- None (parallel with 42)
