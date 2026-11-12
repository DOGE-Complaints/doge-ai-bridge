# STORY-AIBRIDGE-46 — Worker entry + S2S auth + idempotency

## Meta
- **Key:** `STORY-AIBRIDGE-46-worker-entry-s2s-idempotency`
- **Status:** P6 Done · t08–t09 Done · pkg-000049 · next **P7** · `run_mode=aibridge_46_audit_20261014` · 2026-10-14T12:33:45Z
- **Parent REQ:** [`REQ-09`](../../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) §§1–2,4.1,5 AC-01,8.1–2
- **Tech-arch:** [`sense-brief-poster-worker/01-entry-auth-idempotency.md`](../../../architecture/sense-brief-poster-worker/01-entry-auth-idempotency.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [47](STORY-AIBRIDGE-47-sense-brief-prompts-policy.md) · [48](STORY-AIBRIDGE-48-poster-storage-https-url.md) · [49](STORY-AIBRIDGE-49-gateway-bind-fail-version.md) · [50](STORY-AIBRIDGE-50-worker-isolation-harness.md)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md)
- **Emitted:** 2026-10-14T11:37:31Z
- **P1 materialize:** 2026-10-14T11:54:36Z · [p1 draft](../../../../../.cursor/plans/p1_aibridge_46_scaffold_20261014T114919Z.plan.md) · pipeline [`STORY-….md`](../../epics/EPIC-AIBRIDGE-07-req-09-req13-sense-brief-poster-worker/stories/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency/STORY-AIBRIDGE-46-worker-entry-s2s-idempotency.md)
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Subtasks:** derived from sense-brief-poster-worker arch (2026-10-14)

## Scope
- Separate worker accept entry ≠ `/v1/channel/` interview/channel handler (same image OK).
- Dedicated worker S2S token auth; reject channel Bearer / citizen creds.
- Idempotency on Issue id + generation-version (same version → no-op / same outcome).
- Fail-closed when worker enabled and required S2S config missing.
- Exact HTTP path / env var **names** remain Open (do not invent SSOT).

## Out of scope
- Brief/LLM, poster, storage upload, gateway bind client (47–49).
- Changing Telegram interview / REQ-05 behavior.
- Gateway public wire; SPA.

## Verified current state
- Channel façade Present: `CHANNEL_PATH_PREFIX = "/v1/channel/"` — `src/aibridge/app.py` (~50); turns/actions routes (~613+).
- Channel Bearer middleware Present — `app.py` (~542+).
- `GATEWAY_SERVICE_API_TOKEN` for aibridge→gateway — `config.py` / `gateway.py` (outbound; ≠ worker accept).
- Sense-brief worker accept entry — **Present** (P3 · 2026-10-14):
  - Path: `POST /v1/worker/sense-brief/accept` — `src/aibridge/worker_accept.py` · wired in `app.py` (`WORKER_PATH_PREFIX=/v1/worker/`).
  - Settings fail-closed: `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` · `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` — `config.py`.
  - Dedicated S2S: `is_worker_s2s_authorized` — `auth.py` (rejects channel Bearer first, even if equal to worker S2S).
  - Idempotency Issue+`generation_version`: in-process `WorkerIdempotencyStore` — `worker_accept.py`.
  - Tests: `tests/test_worker_accept_story_46.py`.
- Brief LLM / civic poster / gateway bind (47–49) — still **Absent** (out of story 46).

## Target / AC
- [x] AC-09-01: Worker accept path is not the interview/channel handler.
- [x] Channel Bearer cannot authorize worker accept.
- [x] Valid worker S2S admits accept (further pipeline may still fail).
- [x] Same Issue+generation-version duplicate accept is idempotent (no required second full compute).
- [x] Worker enabled + missing S2S → fail-closed (no accept).

**Implement names (P3):** `POST /v1/worker/sense-brief/accept` · `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED` · `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` · JSON `issue_id` / `generation_version` / optional `corpus`.

## Code points
- Extend near `src/aibridge/app.py` (separate from channel routes) — exact module Open
- Auth/settings near `src/aibridge/config.py` — env name Open
- Do not reuse channel Bearer middleware as worker auth

## Technical subtasks

Arch: [`01-entry-auth-idempotency.md`](../../../architecture/sense-brief-poster-worker/01-entry-auth-idempotency.md) · overview DP1/DP3/DP5 · AC-09-01 / AC-09-06 (same-version).

### T01 — Worker enable + settings (fail-closed)

- Add settings surface for worker enable + dedicated worker S2S secret near `src/aibridge/config.py`.
- When worker **enabled** and S2S (or required peer config) missing/invalid → **fail-closed** (do not accept).
- Env **names** remain **Open** (do not invent SSOT).

**Gate:** enabled+missing S2S → no accept / readiness or accept path refuses.  
**Не:** channel Bearer rename; brief/poster/bind (47–49).

### T02 — Separate accept entry (AC-09-01)

- Wire accept on a surface **≠** `CHANNEL_PATH_PREFIX` / channel turns/actions (`app.py` ~50, ~613+).
- Same deployable image OK; sharing interview request path as accept is **out** (DP1).
- Exact route string / process argv — **Open**.

**Gate:** accept handler is not the channel turns/actions handler.  
**Не:** invent final path SSOT; change REQ-05 interview behavior.

### T03 — Dedicated worker S2S auth (DP3)

- Validate dedicated worker S2S on accept; **reject** channel Bearer and citizen credentials.
- Do **not** reuse `channel_bearer_middleware` (~542+) as worker auth.
- Outbound gateway service token remains a **separate** direction (not inverted for accept).

**Gate:** channel Bearer → unauthorized; valid worker S2S → admitted (pipeline may still fail later).  
**Не:** mTLS-only MVP; citizen regenerate.

### T04 — Accept logical inputs

- Parse logical accept: Issue id + generation-version; corpus may passthrough as opaque/stub for later 47.
- Optional locale hints per arch — shape **Open**.
- Exact JSON field **names** — **Open** (joint with gateway).

**Gate:** well-formed accept with S2S reaches idempotency gate.  
**Не:** finalize brief L2 schema (47); invent wire keys as SSOT.

### T05 — Idempotency gate Issue+version (DP5)

- Same Issue id + generation-version as in-flight/completed → no-op / equivalent outcome; **no** required second full LLM+image spend.
- New version (after gateway regenerate bump) → new work allowed.
- Sweep re-nudge same version must be safe.

**Gate:** duplicate same version does not imply second successful bind with a new version.  
**Не:** version bump ownership on gateway board SSOT; bind client (49).

### T06 — Entry/auth/idempotency tests

- Unit/integration: channel Bearer rejected; valid S2S admits; same-version idempotent.
- Full AC-09 harness suite remains STORY-50.

**Gate:** tests green for T03–T05 behaviors without live LLM/storage.  
**Не:** live vendor smoke; storage/bind mocks beyond accept scope.

## Dependencies
- None (foundation). Soft: gateway Wave-1 nudge contract Present (sibling arch) — path strings Open.
