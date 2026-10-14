# Storage, bind-in & verify — sense brief + civic poster worker

| Field | Value |
|-------|--------|
| **Parent overview** | [`00-overview.md`](./00-overview.md) |
| **Parent REQ** | [`../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md`](../../requirements/REQ-09-REQ13-SENSE-BRIEF-AND-CIVIC-POSTER-WORKER.md) |
| **Recorded** | 2026-10-14T11:23:06Z |
| **Mode** | Target technical architecture — not STORY/pkg |

---

## 1) Concern

How poster bytes become a **public HTTPS URL**, how results **bind** to gateway, how **failures** are signaled, and what **verify** proves AC-09-* without live vendor as arch gate.

---

## 2) Target behavior

### Object storage (DP2, AC-09-03)

- Upload runs **in aibridge** with aibridge-owned credentials.  
- Gateway MVP does **not** receive storage write keys.  
- Successful upload yields a **public HTTPS** poster URL included in success bind.  
- Provider / bucket id / CDN — **Open**.  
- Fail-closed when worker enabled and storage creds missing.

### Bind-in client (gateway Wave-1 DP2/DP3/DP6)

| Outcome | Worker sends (logical) | Gateway effect (sibling) |
|---------|------------------------|---------------------------|
| Success | Brief apply payload + HTTPS URL + generation-version | Apply title/summary; status ready; URL+version |
| Failure | Reason **class** (no fake brief) | Fail-closed/placeholder; status failed |

Bind uses gateway **service-auth** (direction aibridge→gateway). Path strings — **Open**.

### Fail reason classes (DP9, AC-09-04)

Logical classes (wire strings Open):

| Class | Meaning |
|-------|---------|
| `accept_unauthorized` | Bad/missing worker S2S (usually before bind) |
| `corpus_insufficient` | Cannot build honest brief from provided corpus |
| `brief_generation_failed` | Text slot / parse / policy abort |
| `image_generation_failed` | Image slot failure |
| `storage_upload_failed` | Upload / URL obtain failure |
| `bind_rejected` | Gateway rejected bind (auth/schema/version) |
| `internal_error` | Unexpected worker fault |

No silent success with fabricated brief.

### Verify harness (DP8)

Arch gate = **contract + isolation** (mocks/fakes OK):

1. Accept rejects channel Bearer.  
2. Brief output matches logical L2 shape.  
3. Upload → URL via storage mock.  
4. Bind success and fail payloads to gateway mock.  
5. Same Issue+version idempotent.

Live OpenAI/image/bucket smoke = **optional ops**, not the architecture Done gate. Exact test paths — **Open**.

### Observability (REQ-09 §4)

- Log/metric: job correlation, Issue id, success/fail, latency, reason class — **PII-safe** (no citizen message bodies / tokens).

---

## 3) Ownership

| Actor | Owns |
|-------|------|
| aibridge | Storage write, URL mint, outbound bind client, harness |
| Gateway | Bind-in receiver, public status/URL/version SSOT |
| Ops | Bucket provisioning, live smoke evidence location |

---

## 4) Verify ↔ AC map

| AC | Harness check |
|----|---------------|
| AC-09-01 | Separate entry + channel Bearer rejected |
| AC-09-02 | Logical L2 brief shape |
| AC-09-03 | Mock upload returns HTTPS URL on success path |
| AC-09-04 | Fail bind with reason class; no fake brief |
| AC-09-05 | Policy/prompt isolation (EN instructions; no invent fixture) |
| AC-09-06 | Version bump → distinguishable URL/asset; same version idempotent |

---

## 5) Explicit not in this doc

- Bucket name / CDN hostname SSOT  
- Exact bind path or enum wire strings  
- Requiring live vendor in CI  
- Arweave as primary MVP media (REQ-09 OOS)  
