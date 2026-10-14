# P4 Audit — STORY-AIBRIDGE-48-poster-storage-https-url

| Field | Value |
|-------|-------|
| **Date** | 2026-10-14T13:56:01Z |
| **Mode** | `input_mode=backlog_story` / epic_story pipeline |
| **builder_project** | `aibridge` |
| **$bullrun** | `doge-ai-bridge/docs/tasks/run-reports/run-summary-20261014-1350-story-aibridge-48-p3.md` |
| **$story** | `…/STORY-AIBRIDGE-48-poster-storage-https-url/STORY-AIBRIDGE-48-poster-storage-https-url.md` |
| **$storyFile** | `doge-ai-bridge/docs/tasks/backlog-stories/req-09-req13-sense-brief-poster-worker/STORY-AIBRIDGE-48-poster-storage-https-url.md` |
| **Method** | Read `poster/` + config/app/readiness/worker_accept + tests; live pytest 46+47+48; no product patches; no invent bind/live bucket/provider SSOT |
| **Thinking** | `.cursor/rules/analysis.mdc` · aibridge-operator-contract §6 · workflow §P4 |
| **Scope** | image-poster slot · brief→bytes · aibridge-owned storage · HTTPS URL · fail classes · mock port |
| **Out of scope** | Gateway bind (49) · harness suite (50) · Arweave · live bucket/vendor as Done gate |

## Verdict

| Axis | Result |
|------|--------|
| **Story Target AC (AC-09-03 · aibridge creds fail-closed · brief-derived poster)** | **PASS** |
| **Bullrun t01–t07 Done** | **Confirmed** vs code + gate + **30 passed** |
| **OPEN gaps** | **0 Crit · 0 High · 0 Med · 0 Low · 3 Info** |
| **Critical / High OPEN** | **0** |
| **Live pytest** | **30 passed** (`test_poster_storage_story_48` + 47 + 46) @ 2026-10-14T13:56:01Z |

---

## Bullrun touchpoints (актуализация `$bullrun`)

| ID | P3 claim | P4 fact |
|----|----------|---------|
| **STORY-48** | P3 Done · gate PASS · next P4 | **Confirmed** · **this P4** → next **P5** |
| **t01** | Done · image-poster fail-closed | **Confirmed** middleware/readyz `worker_image_poster_missing` |
| **t02** | Done · `poster/image.py` from brief | **Confirmed** PNG + title marker · dedicated prompts |
| **t03** | Done · `CredentialGatedUploader` | **Confirmed** aibridge cred gate · no gateway keys |
| **t04** | Done · HTTPS + fail classes | **Confirmed** `https://` · `image_generation_failed` / `storage_upload_failed` |
| **t05** | Done · `PosterUploadPort` | **Confirmed** injectable Protocol |
| **t06** | Done · storage-mock tests | **Confirmed** this P4 **30 passed** |
| **t07** | PASS · story gate | **Confirmed** acceptance |
| **Backlog Verified / Code points** | Present | **Aligned** (no stale Open) |

---

## AC matrix (pipeline / `$storyFile` · arch 02–03 · REQ-09)

| ID | Expected | Status | Evidence |
|----|----------|--------|----------|
| **AC-09-03** | Successful job → public HTTPS poster URL | **PASS** · **Info G-02** | accept `pipeline=poster_ready` · `poster_url` starts with `https://` · `test_t06_accept_*` |
| **Creds fail-closed** | Missing storage/image when worker enabled → no accept | **PASS** · **Info G-03** | `worker_image_poster_fail_closed` · `worker_storage_upload_fail_closed` · image accept 503 · storage readyz 503 |
| **Brief-derived poster** | Not interview templates | **PASS** · **Info G-01** | `generate_poster_bytes(SenseBrief)` · `poster/prompts/system_en.md` · assert markers |
| Nested t01–t07 | Done / PASS | **PASS** | README + acceptance + **30 passed** |

### Scope / DoD extras

| Item | Status | Evidence |
|------|--------|----------|
| Fail classes | **PASS** | `PosterFailureClass` · unit raises mapped codes |
| Mockable upload port | **PASS** | `PosterUploadPort` · `test_t05_*` inject |
| Gateway no storage write keys | **PASS** | upload only via aibridge env credential |
| Provider/bucket/CDN not SSOT | **PASS** | Open; mint host implement-local only |
| No live bucket as Done gate | **PASS** · **Info G-02** | `MockHttpsUploader` default |
| `.env.example` knobs | **PASS** | L63–64 |
| Bind (49) not invented | **PASS** | deferred |

---

## Gaps

| ID | Severity | Finding | How to close (findings only) |
|----|----------|---------|------------------------------|
| **G-01** | **Info** | `generate_poster_bytes` builds a **deterministic minimal PNG** (tEXt + title); `AIBRIDGE_WORKER_IMAGE_POSTER_MODEL` is required (fail-closed) but **not** used for a live image-vendor call (documented in `image.py`). AC fixtures OK without live vendor. | Later wave may bind vendor invoke; not required for this story AC. |
| **G-02** | **Info** | Default upload path is **credential-gated + `MockHttpsUploader`** minting `https://aibridge-poster.test/objects/…` — no live object-store PUT; credential value is presence-checked only. Matches «live bucket not Done gate» / provider Open. | Ops/live adapter later; keep mock port for STORY-50. |
| **G-03** | **Info** | Storage creds fail-closed covered on **readyz** + unit upload; **no dedicated accept-path** assert for `worker_storage_creds_missing` (middleware present; image-slot has accept 503 test). | Optional mirror accept test in `test_poster_storage_story_48.py`. |

### Non-gaps

| Topic | Note |
|-------|------|
| Interview templates as poster SSOT | Avoided — dedicated poster prompts + brief input |
| Softening image/storage fail-closed | Avoided — middleware before handler |
| Inventing provider/bucket/CDN SSOT | Avoided |
| Inventing bind-in (49) | Avoided |
| Silent fake non-HTTPS URL | Avoided — gate requires `https://` |

### Regressions

| Topic | Note |
|-------|------|
| vs P3 gate (30 passed) | **None** — re-run **30 passed** |
| STORY-46/47 suites | Preserved (settings carry poster env) |

---

## Cited paths

- `src/aibridge/poster/image.py` · `storage.py` · `pipeline.py` · `port.py` · `errors.py`
- `src/aibridge/poster/prompts.py` · `prompts/system_en.md` · `logging_safe.py`
- `src/aibridge/config.py` · `readiness.py` · `app.py` (`worker_sense_brief_accept`)
- `src/aibridge/worker_accept.py` (`poster_url`)
- `tests/test_poster_storage_story_48.py`
- `.env.example`
- Pipeline / tasks under `…/STORY-AIBRIDGE-48-poster-storage-https-url/`
- P3: `docs/tasks/run-reports/run-summary-20261014-1350-story-aibridge-48-p3.md`
- Arch: `docs/architecture/sense-brief-poster-worker/02-brief-poster-pipeline.md` · `03-storage-bind-verify.md`

---

## Handoff

- **OPEN gaps:** 0 Crit · 0 High · 0 Med · **0 Low** · **3 Info**
- **OPEN IDs:** G-01, G-02, G-03
- **AC vs story:** **PASS**
- **next:** **P5**
