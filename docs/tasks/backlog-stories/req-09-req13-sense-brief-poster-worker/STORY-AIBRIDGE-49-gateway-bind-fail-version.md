# STORY-AIBRIDGE-49 — Gateway bind-in + fail classes + regenerate version

## Meta
- **Key:** `STORY-AIBRIDGE-49-gateway-bind-fail-version`
- **Status:** P5 Done · TASKED=0 · WAIVED G-01…G-03 · pkg-000052 · next **P7** (skip P6) · activation **none** · 2026-10-14T14:25:21Z  
- **P1 materialize:** 2026-10-14T14:08:54Z · [p1 APPLIED](../../../../../.cursor/plans/p1_aibridge_49_scaffold_20261014T140705Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker/stories/STORY-AIBRIDGE-49-gateway-bind-fail-version/STORY-AIBRIDGE-49-gateway-bind-fail-version.md)
- **P3 Execute:** 2026-10-14T14:13:53Z · [p3](../../run-reports/run-summary-20261014-1413-story-aibridge-49-p3.md)
- **P5 APPLY:** 2026-10-14T14:25:21Z · [p5](../../run-reports/run-summary-20261014-1425-story-aibridge-49-p5-disposition.md)
- **Parent REQ:** [`REQ-09`](../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1.4,2,4.4–5,5 AC-04/06,8.5–6
- **Tech-arch:** [`03-storage-bind-verify.md`](../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [46](STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md) · [47](STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) · [48](STORY-AIBRIDGE-48-poster-storage-https-url.md) · [50](STORY-AIBRIDGE-50-worker-isolation-harness.md); gateway sibling arch `issue-sense-brief-poster`
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-14T11:37:31Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Subtasks:** derived from sense-brief-poster-worker arch (2026-10-14)

## Scope
- Outbound bind-in to gateway (service-auth): success = brief apply payload + HTTPS URL + generation-version; failure = reason class, no fake brief.
- Logical fail classes per arch DP9 (exact wire strings Open).
- Regenerate = new version → new URL/asset distinguishable from prior (AC-09-06).
- Worker does not own board pending/ready/failed SSOT.
- Reuse Present aibridge→gateway intake direction; path strings Open.
- PII-safe success/fail/latency signals (REQ §4.6).

## Out of scope
- Gateway projection apply implementation (sibling 57); renaming gateway public fields; SPA.

## Verified current state
- aibridge→gateway client Present — `src/aibridge/gateway.py`.
- Sense-brief bind-in — **Present** (P3): `src/aibridge/sense_bind/`.

## Target / AC
- [x] AC-09-04: Failure returns explicit error to gateway (no fake brief).
- [x] AC-09-06: Regenerate produces new version id/URL distinguishable from prior.
- [x] Success bind includes brief-derived apply payload + HTTPS URL + version (keys Open).

**Implement names (P3):** `src/aibridge/sense_bind/` · `/v1/issue-sense-brief/bind` (implement) · `GATEWAY_SERVICE_API_TOKEN`.

## Code points
- Bind client — **Present**: `src/aibridge/sense_bind/client.py`
- Path/keys — implement choice (Open as arch SSOT)

## Technical subtasks

Arch: [`03-storage-bind-verify.md`](../../../architecture/sense-brief-poster-worker/03-storage-bind-verify.md) · DP5/DP9 · AC-09-04 / AC-09-06 · sibling gateway Wave-1 bind-in.

### T01 — Outbound bind-in client (service-auth)

- Client posts to gateway bind-in using gateway **service-auth** (pattern near `gateway.py` `authorization_header` ~204–207).
- Direction aibridge→gateway; path strings **Open** (do not invent SSOT).
- Worker does **not** own board pending/ready/failed SSOT.

**Gate:** bind uses gateway service token domain, not channel Bearer / worker-accept S2S.  
**Не:** gateway projection apply implementation (sibling 57); rename public fields.

### T02 — Success bind payload

- Success: brief apply payload + public HTTPS URL + generation-version (logical; exact keys Open).
- Feeds gateway apply → title/summary; status ready (sibling ownership).

**Gate:** success path includes apply payload + HTTPS URL + version.  
**Не:** invent public wire key names as SSOT.

### T03 — Fail bind + DP9 reason classes (AC-09-04)

- On failure: bind reason **class**, **no** fake brief.
- Logical classes per arch: e.g. `brief_generation_failed`, `image_generation_failed`, `storage_upload_failed`, `bind_rejected`, `internal_error`, `corpus_insufficient` (and accept-side `accept_unauthorized` usually pre-bind).
- Exact wire enum strings — **Open**.

**Gate:** fail path never presents fabricated successful brief.  
**Не:** free-text-only reasons without class.

### T04 — Regenerate / version distinguishability (AC-09-06)

- After gateway version bump + re-nudge: new work yields URL/asset **distinguishable** from prior version.
- Same version remains idempotent at worker (46); this story owns bind semantics for new version success.

**Gate:** two successful versions produce distinguishable version id and/or URL.  
**Не:** silent overwrite without version bump.

### T05 — PII-safe observability (REQ §4.6)

- Log/metric: job correlation, Issue id, success/fail, latency, reason class.
- No citizen message bodies / tokens / secrets.

**Gate:** observability fields present without PII bodies in default logs.  
**Не:** invent metric backend SSOT.

### T06 — Bind success/fail tests vs gateway mock

- Isolation tests: success payload shape; fail with reason class; mock gateway reject → `bind_rejected` (or equivalent mapping).

**Gate:** tests green without live gateway/LLM/bucket.  
**Не:** live Railway smoke as merge gate.

## Dependencies
- STORY-AIBRIDGE-47, STORY-AIBRIDGE-48
