# Entry, auth & idempotency — sense brief + civic poster worker

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Recorded** | 2026-10-14T11:23:06Z · as-built 2026-10-15T10:13:28Z |
| **Mode** | Target technical architecture — not STORY/pkg |

### As-built (STORY-46)

- Path: `POST /v1/worker/sense-brief/accept` (`worker_accept.py:21–22`; `app.py:684–685`)  
- Env: `AIBRIDGE_WORKER_SENSE_BRIEF_ENABLED`, `AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN` (`config.py:197–204`)  
- Auth: `is_worker_s2s_authorized` rejects channel Bearer (`auth.py:45–58`)  
- Idempotency: in-process `WorkerIdempotencyStore` on `(issue_id, generation_version)` (`worker_accept.py:48–69`)  

---

## 1) Concern

How the worker is **reached**, who may call it, and how duplicate nudges / sweeps stay safe under gateway Issue lifecycle (no separate job table on gateway v1).

---

## 2) Target behavior

### Separate entry (DP1, AC-09-01)

- Worker accept lives on a **distinct** entry from Telegram interview / channel façade handlers.  
- Same deployable image is allowed; sharing the interview request path as accept is **out**.  
- Exact route — **as-built** § above (was Open at interview).

### Trust boundary (DP3, F12)

| Caller | Credential | Worker accept |
|--------|------------|---------------|
| Gateway thin nudge | Dedicated **worker S2S** (`AIBRIDGE_WORKER_SENSE_BRIEF_S2S_TOKEN`) | **Allowed** when valid |
| Channel / n8n / Telegram path | Channel Bearer | **Rejected** |
| Citizen SPA / public | Citizen Bearer or none | **Rejected** |

Outbound bind-in to gateway uses gateway’s own service-auth (gateway DP6) — **separate** secret direction from worker accept token. Do not invert/`reuse` channel Bearer for either side.

Fail-closed: if worker is enabled and the worker S2S token (or required peer URL config) is missing/invalid → do not accept jobs.

### Idempotency (DP5, AC-09-06)

| Event | Behavior |
|-------|----------|
| Accept with Issue id + **same** generation-version as an in-flight or already-completed job for that pair | No-op or return equivalent outcome — **no** second LLM+image spend required |
| Gateway manual regenerate (version bump) then nudge | New version → new work → new poster URL/asset distinguishable from prior |
| Sweep re-nudge while pending same version | Safe duplicate at worker |

Payload fields as-built: `issue_id`, `generation_version`, optional `corpus` (`worker_accept.py:25–32`). Gateway nudge must send these names until joint rename.

---

## 3) Ownership

| Actor | Owns |
|-------|------|
| aibridge worker | Accept surface, S2S validation, local idempotency handling |
| Gateway | Issue generation status/version SSOT; when to nudge / regenerate |
| Neither | Inventing final HTTP path strings as SSOT in this doc |

---

## 4) Verify (logical)

- Channel Bearer (or interview auth) **cannot** authorize worker accept.  
- Valid worker S2S + well-formed accept → admitted (further pipeline may still fail).  
- Second accept same Issue+version does not imply a second successful bind with a new version.  
- Mapping: AC-09-01, AC-09-06.

---

## 5) Explicit not in this doc

- mTLS-only / network-only auth as MVP  
- Citizen-triggered regenerate on worker  
- Multi-replica shared idempotency store (current = in-process)  
