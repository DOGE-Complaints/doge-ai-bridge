# Entry, auth & idempotency — sense brief + civic poster worker

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Recorded** | 2026-10-14T11:23:06Z |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

How the worker is **reached**, who may call it, and how duplicate nudges / sweeps stay safe under gateway Issue lifecycle (no separate job table on gateway v1).

---

## 2) Target behavior

### Separate entry (DP1, AC-09-01)

- Worker accept lives on a **distinct** entry from Telegram interview / channel façade handlers.  
- Same deployable image is allowed; sharing the interview request path as accept is **out**.  
- Exact route string / process argv — **Open**.

### Trust boundary (DP3, F12)

| Caller | Credential | Worker accept |
|--------|------------|---------------|
| Gateway thin nudge | Dedicated **worker S2S** token (env name Open) | **Allowed** when valid |
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

Exact payload field names for Issue id / generation-version — **Open** (joint with gateway).

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

- Exact path/header names  
- mTLS-only / network-only auth as MVP  
- Citizen-triggered regenerate on worker  
