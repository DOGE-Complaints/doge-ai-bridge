# STORY-AIBRIDGE-45 — Live Telegram deployment verification (AC-09)

## Meta
- **Key:** `STORY-AIBRIDGE-45-compat-live-telegram-verify`
- **Status:** P5 Done · deferred_live / BLOCKED AC-09 · G-01…G-03 WAIVED · TASKED=0 · next **P7** · pkg-000044 · 2026-09-24T12:17:21Z · [BLOCKED](../../ops/req-07-ac09-live-evidence-BLOCKED-20260924.md) · [p5](../../run-reports/run-summary-20260924-1217-story-aibridge-45-p5-disposition.md)
- **Parent REQ:** [`REQ-07`](../../../requirements/REQ-07-OPENAI-STRICT-SCHEMA-COMPATIBILITY-PROJECTION.md) §11.5 · AC-09 · §15
- **Tech-arch:** [`TECH-ARCH-REQ-07`](../../../architecture/TECH-ARCH-REQ-07-openai-strict-schema-compat.md) §5.2–5.3
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [41](STORY-AIBRIDGE-41-openai-schema-projection.md) · [42](STORY-AIBRIDGE-42-canonical-uniqueitems-validation.md) · [43](STORY-AIBRIDGE-43-validation-context-bind-readyz.md) · [44](STORY-AIBRIDGE-44-compat-merge-gate-proof.md)
- **Skill declared:** `test-master` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md) (evidence discipline)
- **Emitted:** 2026-09-24T10:28:49Z

## Scope
- After Railway deploy of image containing 41–44: one real Telegram → n8n → aibridge → **real** OpenAI turn; no `invalid_function_parameters`; meaningful interview reply; no gateway stash before existing dual-confirm.
- Write redacted live evidence under template path:  
  `docs/ops/req-07-ac09-live-evidence-YYYYMMDD.md`  
  Fields: UTC time, deployment/version or commit SHA, scenario id, pass/fail, correlation/request ID. **No** user narrative, Bearer, API keys, or full tool/args.
- Only after PASS: focus **production verified / rollout complete**. Until then keep **implemented, live verification pending** (after 44).

## Out of scope
- Using live as the only proof; n8n workflow redesign; creating the evidence file before the live run (name ≠ create).

## Verified current state
- Failure mode documented in REQ §2 (HTTP 400 `uniqueItems` on houses).
- Evidence file not present until live run.

## Target / AC
- [ ] AC-09 satisfied; evidence artifact linked from this story or package INDEX.
- [ ] Deployed `/readyz` ready before the live turn (§15).

## Code points
- Ops/runtime only; no product code required beyond 41–44 image

## Dependencies
- Requires **44** Implemented; deployed image with that code
