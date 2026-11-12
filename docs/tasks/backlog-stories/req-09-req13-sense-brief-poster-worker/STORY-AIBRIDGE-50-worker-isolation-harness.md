# STORY-AIBRIDGE-50 — Contract + isolation harness (AC-09 proof)

## Meta
- **Key:** `STORY-AIBRIDGE-50-worker-isolation-harness`
- **Status:** P6 Done · t09 Done · WAIVED G-02/G-03 · pkg-000053 · next **P7** · 2026-10-14T14:53:46Z  
- **P1 materialize:** 2026-10-14T14:33:55Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_50_scaffold_20261014T143127Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker/stories/STORY-AIBRIDGE-50-worker-isolation-harness/STORY-AIBRIDGE-50-worker-isolation-harness.md)
- **P3 Execute:** 2026-10-14T14:40:44Z · [p3](../../run-reports/run-summary-20261014-1440-story-aibridge-50-p3.md)
- **P4 Audit:** 2026-10-14T14:45:44Z · [p4](../../analysis/p4-audit-STORY-AIBRIDGE-50-worker-isolation-harness-20261014.md)
- **P5 APPLY:** 2026-10-14T14:50:21Z · [p5](../../run-reports/run-summary-20261014-1450-story-aibridge-50-p5-disposition.md)
- **P6 Execute:** 2026-10-14T14:53:46Z · [p6](../../run-reports/run-summary-20261014-1453-story-aibridge-50-p6.md)
- **Parent REQ:** [`REQ-09`](../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§4.6,5 AC-01…06
- **Tech-arch:** [`03-storage-bind-verify.md`](../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) DP8
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [46](STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) · [47](STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) · [48](STORY-AIBRIDGE-48-poster-storage-https-url.md) · [49](STORY-AIBRIDGE-49-gateway-bind-fail-version.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-14T11:37:31Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Subtasks:** derived from sense-brief-poster-worker arch (2026-10-14)

## Scope
- Automated isolation harness (mocks OK):
  1) accept rejects channel Bearer;
  2) logical L2 brief shape;
  3) upload→HTTPS URL mock;
  4) bind success/fail payloads to gateway mock;
  5) same Issue+version idempotent.
- Live LLM/image/bucket smoke = optional ops residual — not merge gate.
- Test modules **Present** (P3): `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py`.

## Out of scope
- Requiring live OpenAI/bucket secrets in CI; SPA E2E; inventing production path SSOT.

## Verified current state
- Isolation harness Present (P3): `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py`.
- Prior verify patterns under `tests/` for 46–49 reused; no interview as worker entry.

## Target / AC
- [x] Harness proves AC-09-01…06 per arch AC map (isolation).
- [x] No dependency on live vendor for package merge gate.

## Code points
- `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py`

## Technical subtasks

Arch: [`03-storage-bind-verify.md`](../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) DP8 + Verify↔AC map · isolation harness for AC-09-01…06.

### T01 — Harness skeleton + mocks

- Isolation harness **Present**: `tests/harness/sense_brief_isolation.py` · `tests/test_worker_isolation_harness_story_50.py`.
- Mocks/fakes for LLM text slot, image slot, storage upload, gateway bind — **no** live vendor secrets required in CI.

**Gate:** harness runs without OpenAI/bucket/gateway live creds.  
**Не:** invent production path SSOT; SPA E2E.

### T02 — AC-09-01 check

- Assert separate worker entry ≠ channel handler; channel Bearer **rejected** on accept.

**Gate:** AC-09-01 covered by automated check.  
**Не:** change interview channel auth behavior beyond reject-on-worker.

### T03 — AC-09-02 check

- Assert successful brief matches logical L2 (title ≤80; summary et/ru/en present).

**Gate:** AC-09-02 covered.  
**Не:** freeze exact JSON key spellings in harness as product SSOT if still Open — assert logical outcomes.

### T04 — AC-09-03 check

- Assert upload mock returns public HTTPS poster URL on success path.

**Gate:** AC-09-03 covered via mock.  
**Не:** live bucket required.

### T05 — AC-09-04 check

- Assert fail bind carries reason class; **no** fake brief on failure.

**Gate:** AC-09-04 covered.  
**Не:** free-text-only without class.

### T06 — AC-09-05 check

- Assert EN instruction / dedicated prompt path isolation; invent-refusal fixture (no invented civic facts beyond corpus).

**Gate:** AC-09-05 covered.  
**Не:** require live model for policy proof if fixture/mock suffices.

### T07 — AC-09-06 check

- Assert same Issue+version idempotent; version bump yields distinguishable URL/asset (or version id).

**Gate:** AC-09-06 covered.  
**Не:** gateway-owned regenerate auth implementation (sibling).

### T08 — Package gate checklist

- [x] Isolation pytest suite for T02–T07 green
- [x] No CI dependency on live OpenAI / image vendor / bucket secrets
- [x] Live LLM+image+bucket smoke = **optional ops residual**, not arch/merge Done gate
- [x] Exact test module names documented when created

**Gate:** package merge gate = isolation harness only.  
**Не:** treat live smoke as blocking Done for this story.

## Dependencies
- STORY-AIBRIDGE-46, STORY-AIBRIDGE-47, STORY-AIBRIDGE-48, STORY-AIBRIDGE-49
