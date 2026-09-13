# R3-P1-08 — SPA HTTPS continuation E2E gate (aibridge tracker)

**Story:** STORY-AIBRIDGE-17-spa-https-continuation-e2e  
**REQ:** REQ-03 §6 R3-P1-08 · anchors REQ-01 §16 / §21  
**Stamp:** 2026-09-13T18:23:58Z  
**Ownership:** aibridge = **gate/tracker only**; SPA profile owns real-device HTTPS UI/E2E and evidence artifacts.

**Not this gate:** [wave1-gate-checklist.md](./wave1-gate-checklist.md) · [n8n R3-P1-09](./n8n-channel-workflow/r3-p1-09-live-gate-checklist.md)

---

## 1. Boundary (do not invent)

| Role | Owns | Must not |
|------|------|----------|
| **aibridge** | Tracker checklist, dashboard wave-2 block, link slots for spa evidence, continuation URL emission after `stashed` | Implement spa frontend / Playwright / invent `STORY-SPA-*` keys |
| **spa** | Real-device HTTPS continuation E2E, screenshots/logs, spa story Done / run-summary | — |

SPA owner story key at materialize / P3: **Unknown** (fill only when a real spa backlog/pipeline path exists on disk).

---

## 2. aibridge continuation URL (reference — not spa proof)

Code SSOT: `src/aibridge/gateway.py` `build_continuation_url`:

```text
{DOGESTONIA_DRAFT_REDIRECT_BASE_URL}/#/story/submit?draft_id={url-encoded draft_id}
```

Env: `DOGESTONIA_DRAFT_REDIRECT_BASE_URL` (`.env.example` / Settings).  
Wave-1 dry-run may assert URL **shape** in aibridge tests — that is **not** R3-P1-08 real-device SPA proof.

---

## 3. Executable tracker checklist

### A. aibridge gate hygiene

- [x] This checklist exists as R3-P1-08 SSOT (STORY-17 t01).
- [x] Dashboard treats wave-2 residents as **blocked** until spa evidence linked (STORY-17 t03).
- [x] Spa evidence link protocol documented with **Unknown** slots (STORY-17 t02).
- [x] Spa evidence pack linked **or** BLOCKED residual recorded (STORY-17 t04) — **BLOCKED** this session.

### B. Spa-owned evidence pack (fill when available — do not invent)

| Slot | Value |
|------|-------|
| spa story key | **Unknown** |
| spa story / pipeline path | **Unknown** |
| spa run-summary path | **Unknown** |
| spa evidence checklist / screenshots (redacted) | **Unknown** |
| Device: HTTPS SPA base reachable by resident | **Unknown** |
| Proof: open continuation URL → submit flow works on device | **Unknown** |

### C. Claim rule

- Do **not** mark R3-P1-08 live PASS until spa evidence paths exist on disk and are linked here.
- Do **not** invent spa story ids or fake device screenshots.
- BLOCKED residual is valid aibridge P3 deliverable when spa pack is missing.

---

## 4. Evidence status (this session)

See [spa-https-continuation-evidence-BLOCKED-20260913.md](./spa-https-continuation-evidence-BLOCKED-20260913.md).

---

## 5. Operator unblock (spa profile)

1. Resolve spa backlog story for HTTPS continuation E2E; record real `STORY-SPA-*` key on disk.
2. Run real-device HTTPS proof against pilot `DOGESTONIA_DRAFT_REDIRECT_BASE_URL`.
3. Link Done story + run-summary + redacted evidence into slots above; clear BLOCKED.
4. Then aibridge may flip Target #1 and lift wave-2 block on the dashboard.
