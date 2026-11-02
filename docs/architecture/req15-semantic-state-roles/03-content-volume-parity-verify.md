# Content volume, consume parity, verify

**Overview:** [`00-overview.md`](./00-overview.md)  
**Locks:** Interview D4=A · D6=A · REQ **L13-2** · AC-04/05/06  
**Peer packaging:** [`../runtime/02-content-packaging.md`](../runtime/02-content-packaging.md) — **Git ownership ≠ image packaging**

---

## 1) Hybrid C read contract

| Environment | Instructions home |
|-------------|-------------------|
| **Local / CI** | Path from `DOGESTONIA_INSTRUCTIONS_DIR` + `DOGESTONIA_INSTRUCTIONS_MANIFEST` — **may** point at GPT UI checkout or at a GPT-48 **export** layout |
| **Prod** | Configured dir = **Railway volume** (ops upload from GPT UI export); image-baked `src/instructions/` = **fixture/dev only** after cutover (L13-2) |
| **Forbidden** | Mutable GitHub fetch at request time (`content.py` / runtime/02) |

Authoring SSOT remains GPT UI. Aibridge never becomes the instruction workshop.

### Operator local intent (2026-11-02)

Operator sets aibridge `.env` `DOGESTONIA_INSTRUCTIONS_*` to the GPT UI `instructions/` tree so local runs consume GPT UI files.

**Verified gap (analysis.mdc):** as of materialize, `GPT UI/instructions/instructions.manifest.json` is **Absent**. Present `content.py` requires a manifest file whose `files[]` entries are **root children** of the instructions dir (no nested `/` paths in entries). Until GPT-48 export (or an aibridge-compatible manifest) is Present, pointing DIR at GPT UI alone is **intent**, not yet consume Pass — expect ContentLoadError / not-ready until manifest+layout match the loader.

---

## 2) Consume parity (AC-05/06)

| Gate | Behavior |
|------|----------|
| Pass | Mounted/dir inventory+hashes match GPT UI **export** Pass (format joint Open) |
| Fail | Incomplete or mismatched content → `/ready`-class **fail-closed** — no silent subset |

Exact hash/inventory wire format = Open (product joint GPT-48); this arch locks **gate behavior**.

---

## 3) Verify / evidence (D6)

| Gate | Required for |
|------|----------------|
| **Stub / harness** | Semantic store writes + D2 invalidation; policy coordinator one-role; assembly core+slice+pin; parity/incomplete fail-closed; L13-1 send≠auto | Tech accept |
| **Live** | Volume mount + real export parity + ≥1 role path recorded | Live Pass per surface; only with ops window |
| Without window | Explicit **Partial** for live AC sides | Do not claim full Done on stub alone |

Honesty: Product Story Done ≠ Draft REQ ≠ green smoke without parity evidence.

---

## 4) Env touchpoints (Present names)

| Variable | Use |
|----------|-----|
| `DOGESTONIA_INSTRUCTIONS_DIR` | Directory root for instruction files |
| `DOGESTONIA_INSTRUCTIONS_MANIFEST` | Manifest path (Present content load) |
| Related Present | `DOGESTONIA_CONTENT_SOURCE_COMMIT` · OAS · pack schema (existing content_configured gates) |

No invent of new env name SSOT beyond Present + L13 locks.
