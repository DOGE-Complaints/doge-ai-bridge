# Hybrid-C volume + consume parity runbook (STORY-67 / AC-AIB-13-04)

Thin ops note. Arch SSOT: [`../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md`](../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md). Peer packaging: [`../architecture/runtime/02-content-packaging.md`](../architecture/runtime/02-content-packaging.md). Stub/live honesty: [`11-content-volume-parity-stub-live-evidence.md`](./11-content-volume-parity-stub-live-evidence.md). Cutover: [`13-roles-schema-channel-cutover.md`](./13-roles-schema-channel-cutover.md).

**Honesty:** this runbook ≠ live Railway SUCCESS. Live Pass only with ops window + refreshed Export Pass + recorded evidence (t07). Do **not** invent live SUCCESS. Automatic CI sync **OOS** (GPT V3 rejected).

---

## 1) Hybrid C read contract (L13-2)

| Environment | Instructions home |
|-------------|-------------------|
| **Local / CI** | `DOGESTONIA_INSTRUCTIONS_DIR` + `DOGESTONIA_INSTRUCTIONS_MANIFEST` → roles-schema export layout or fixtures |
| **Prod** | Same env names on a **Railway volume** — ops **manual** publish from GPT UI export (SSH / volume UI) |
| **Image-baked** | `src/instructions/` = **fixture/dev only** after cutover — not prod SSOT |
| **Forbidden** | Mutable GitHub fetch at request time |

Authoring SSOT remains GPT UI. Aibridge never becomes the instruction workshop.

---

## 2) Env (no secrets in evidence)

| Variable | Role |
|----------|------|
| `DOGESTONIA_INSTRUCTIONS_DIR` | Mounted/export root (roles-schema children) |
| `DOGESTONIA_INSTRUCTIONS_MANIFEST` | `roles.manifest.json` under that root (or equivalent path) |
| `DOGESTONIA_ROLES_*` | Optional; if set must **resolve equal** to INSTRUCTIONS_* (seam fail-closed) |
| `DOGESTONIA_EXPORT_INVENTORY_PATH` | Locked **GPT E1** JSON inventory artifact — when set, `/readyz` fail-closed on mismatch |
| `DOGESTONIA_CONTENT_SOURCE_COMMIT` · OAS · pack | Existing `content_configured` gates |

### E1 inventory artifact shape (locked · no invent alternate)

```json
{
  "wire": "e1",
  "bundle_version": "<from roles.manifest.json>",
  "hash_method": "normalize_text+sha256_hex",
  "files": {
    "roles.manifest.json": "<sha256>",
    "core.md": "<sha256>",
    "communication_setup.md": "<sha256>",
    "interviewer.md": "<sha256>",
    "extractor.md": "<sha256>",
    "normalizer.md": "<sha256>",
    "checker.md": "<sha256>"
  }
}
```

`session_pin` / assembled core+role hash ≠ file inventory (do not conflate). Registry/session pin remains packaging/runtime concern in [`02-content-packaging.md`](../architecture/runtime/02-content-packaging.md).

---

## 3) Manual publish steps (v1)

1. Confirm GPT Export Pass on Present tree (`instructions-roles/` or published copy) — stale evidence ≠ Export Pass (see analysis preflight).  
2. Copy export root → Railway volume path (or local dir).  
3. Point `DOGESTONIA_INSTRUCTIONS_*` at volume.  
4. Place/refresh E1 inventory JSON; set `DOGESTONIA_EXPORT_INVENTORY_PATH`.  
5. Ensure `ROLES_*` unset **or** same resolved paths as `INSTRUCTIONS_*`.  
6. Check `/readyz` → `ready` (parity Pass) · exercise ≥1 role path.  
7. Record UTC evidence artifact (t07) — without window stay **Explicit Partial**.

---

## 4) Reconcile arch 03 ↔ runtime/02

| Concept | Meaning |
|---------|---------|
| File inventory / E1 hashes | Consume parity (AC-05) — this runbook + `export_parity.py` |
| Bundle registry / `bundle_hash` | Deployment register-once (runtime/02) |
| `session_pin` | Per-turn assembly pin — **≠** E1 file inventory |

---

## 5) Out of this note

Opening ops window · inventing hash beyond E1 · GPT-48 authoring rewrite · CI auto-sync · inventing Railway SUCCESS.
