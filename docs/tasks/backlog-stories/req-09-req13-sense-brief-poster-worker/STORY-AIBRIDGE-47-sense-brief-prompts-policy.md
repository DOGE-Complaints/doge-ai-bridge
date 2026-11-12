# STORY-AIBRIDGE-47 — Sense brief + dedicated prompts + policy

## Meta
- **Key:** `STORY-AIBRIDGE-47-sense-brief-prompts-policy`
- **Status:** P6 Done · t08 Done · pkg-000050 · next **P7** · `run_mode=aibridge_47_audit_20261014` · 2026-10-14T13:31:42Z  
- **P1 materialize:** 2026-10-14T12:46:03Z · [p1 draft](../../../../../.cursor/plans/p1_aibridge_47_scaffold_20261014T124254Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker/stories/STORY-AIBRIDGE-47-sense-brief-prompts-policy/STORY-AIBRIDGE-47-sense-brief-prompts-policy.md)
- **Parent REQ:** [`REQ-09`](../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1.1,2,4.2,5 AC-02/05,8.3
- **Tech-arch:** [`02-brief-poster-pipeline.md`](../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [46](STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) · [48](STORY-AIBRIDGE-48-poster-storage-https-url.md) · [49](STORY-AIBRIDGE-49-gateway-bind-fail-version.md) · [50](STORY-AIBRIDGE-50-worker-isolation-harness.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-14T11:37:31Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Subtasks:** derived from sense-brief-poster-worker arch (2026-10-14)

## Scope
- Corpus → structured sense brief (logical L2): title ≤80; summary et/ru/en; problem/context/severity/audience/desired_outcome/evidence_refs (exact JSON keys Open).
- Dedicated worker prompt module (EN instructions); not interview/content templates as SSOT.
- text-brief capability slot; model id via env (no model catalog SSOT).
- Refuse inventing civic facts beyond corpus (AC-09-05 / L11).
- PII-safe logging hooks for job/Issue (bodies/secrets out).

## Out of scope
- Poster image / storage (48); bind-in (49); harness suite (50).
- Public raw brief blob on gateway (gateway DP4).
- Inventing final model IDs as SSOT.

## Verified current state
- Interview/content prompt paths Present (REQ-01/05 runtime) — must not be civic SSOT.
- Issue sense-brief pipeline — **Present** (P3): `src/aibridge/sense_brief/` · prompts `system_en.md` · `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL`.

## Target / AC
- [x] AC-09-02: Successful brief has title ≤80 and summary et/ru/en.
- [x] AC-09-05: EN instruction language; no invented addresses/agencies beyond corpus.
- [x] Prompts live in dedicated worker module (not interview templates).
- [x] text-brief slot fail-closed if unset when worker enabled.

**Implement names (P3):** `src/aibridge/sense_brief/` · `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` · L2 keys `title`/`summary.{et,ru,en}`/… · fail `corpus_insufficient`/`brief_generation_failed`.

## Code points
- Worker brief module — **Present** (P3): `src/aibridge/sense_brief/` (`model.py` · `pipeline.py` · `prompts/system_en.md` · `errors.py` · `logging_safe.py`).
- Env text-brief slot — **Present**: `AIBRIDGE_WORKER_TEXT_BRIEF_MODEL` (`config.py` / readiness / middleware).
- Must not wire through `InterviewEngine` channel turns as entry — **Confirmed** (worker accept → `generate_sense_brief` only).

## Technical subtasks

Arch: [`02-brief-poster-pipeline.md`](../../../architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md) · overview DP4/DP6/DP7 · AC-09-02 / AC-09-05.

### T01 — Logical L2 brief model

- Represent logical L2 outcomes: title ≤80 plain; summary et/ru/en; problem/context/severity/audience/desired_outcome/evidence_refs.
- Exact JSON **keys** remain **Open** (joint freeze with gateway apply).

**Gate:** successful brief object satisfies logical L2 checks (title length + three summaries).  
**Не:** public raw brief blob on gateway; invent key spellings as SSOT.

### T02 — Dedicated prompt module packaging (DP7)

- Separate EN system/instructions for sense-brief (and poster-facing constraints as needed by brief).
- **Must not** use Telegram interview / content-launch templates as civic SSOT.
- On-disk path inside image — **Open**; packaging seam: module must ship with worker image.

**Gate:** brief path loads worker prompts, not interview corpus templates.  
**Не:** invent prompt body SSOT in story; external CMS.

### T03 — text-brief capability slot (DP6)

- Bind text-brief model/vendor id via env/config only (no model catalog SSOT).
- Worker enabled ⇒ text-brief configured or **fail-closed**.

**Gate:** missing text-brief id when worker enabled → fail-closed before inventing brief.  
**Не:** lock concrete OpenAI model string as SSOT; multi-provider abstraction v1.

### T04 — Corpus→brief pipeline + no-invent policy (AC-09-05)

- Generate structured brief from accept corpus; EN instruction language; i18n outputs allowed.
- Refuse inventing addresses/agencies/events beyond corpus (omit/refuse rather than fabricate).
- PII-safe logging: job/Issue ids OK; no citizen message bodies/secrets.

**Gate:** fixture corpus with missing civic facts does not invent them.  
**Не:** poster bytes (48); bind-in (49).

### T05 — Brief failure reason classes

- Map failures to logical classes `corpus_insufficient` / `brief_generation_failed` (arch DP9).
- Exact wire **strings** remain **Open**.

**Gate:** insufficient corpus / generation abort surfaces explicit class (no fake brief).  
**Не:** full bind client (49); invent enum freeze as SSOT.

### T06 — Golden L2 + invent-refusal fixtures

- Golden/fixture brief for logical L2 shape; invent-refusal policy tests.
- Feeds STORY-50 harness checks for AC-09-02/05.

**Gate:** fixtures prove title≤80, summary et/ru/en, no-invent behavior without live vendor required.  
**Не:** require live OpenAI in CI.

## Dependencies
- STORY-AIBRIDGE-46
