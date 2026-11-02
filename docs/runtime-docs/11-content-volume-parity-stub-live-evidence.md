# Content volume / parity + stub/live evidence (STORY-64 / REQ-13)

Thin runtime note. Arch SSOT: [`../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md`](../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md). Peer packaging: [`../architecture/runtime/02-content-packaging.md`](../architecture/runtime/02-content-packaging.md). Etalon honesty: [`08-ac04-interview-stub-live-evidence-gates.md`](./08-ac04-interview-stub-live-evidence-gates.md).

**Honesty:** stub harness ≠ AC-AIB-13-05 **live/parity Done**. Live Pass only with GPT-48 **export** Pass + ops evidence window + recorded path. This wave: AC-05 live = **Explicit Partial**. Do **not** invent Railway / live SUCCESS. Do **not** invent inventory/hash SSOT format (joint Open with GPT-48).

---

## 1) Prod volume path (AC-AIB-13-04 · L13-2)

| Environment | Instructions home |
|-------------|-------------------|
| **Prod** | Configured `DOGESTONIA_INSTRUCTIONS_DIR` (+ `DOGESTONIA_INSTRUCTIONS_MANIFEST`) on a **Railway volume** — ops may upload GPT UI export manually v1 |
| **Image-baked** | `src/instructions/` = **fixture/dev only** after cutover — not prod SSOT |
| **Local / CI** | Same env names; may point at export layout or GPT UI tree (intent ≠ consume Pass until manifest+layout match loader) |
| **Forbidden** | Mutable GitHub fetch at request time (`content.py`) |

Env names Present: `DOGESTONIA_INSTRUCTIONS_DIR` · `DOGESTONIA_INSTRUCTIONS_MANIFEST` · `DOGESTONIA_CONTENT_SOURCE_COMMIT` · OAS / pack schema (existing `content_configured` gates).

---

## 2) Stub evidence matrix — STORY-62 / 63 (required · tech accept)

Runnable harness (Present):

- `tests/test_story_62_semantic_state_store_invalidation.py`
- `tests/test_story_63_roles_coordinator_assembly_fixtures.py`
- AC-06 stub: `tests/test_story_64_content_parity_stub_live_evidence.py` (+ Present `test_content.py` / `test_readyz_bundle.py`)

| AC | Meaning | Stub harness (pytest) | Status |
|----|---------|----------------------|--------|
| **AC-AIB-13-01** | Semantic state persists across turns | `test_t03_ac01_persist_across_turns_no_gpt_ui` · `test_t02_memory_persists_logical_classes` (62) | Present |
| **AC-AIB-13-02** | Five roles + pins via coordinator | `test_t01_five_v1_roles_with_version_pins` · `test_t02_policy_selects_exactly_one_role` (63) | Present |
| **AC-AIB-13-03** | Assemble from dir+manifest + session pin | `test_t03_assemble_from_configured_dir_and_manifest` (63) | Present |
| **AC-AIB-13-07** | Fixtures ≠ gateway/SPA procedure | `test_t07_fixture_texts_exclude_gateway_spa_procedure` (63) | Present |
| **AC-AIB-13-08** / L13-1 | Ordinary reply ≠ send offer | `test_t06_ordinary_reply_does_not_offer_send` (63) | Present |
| **AC-AIB-13-06** stub | Incomplete/mismatch fail-closed | `test_t03_incomplete_manifest_fail_closed` · `test_t03_readyz_fail_closed_incomplete_fixture` (64) · `test_missing_file_fails` · `test_readyz_fails_missing_pack` | Present |

Command (from `doge-ai-bridge/`):

```bash
.venv/bin/python -m pytest \
  tests/test_story_62_semantic_state_store_invalidation.py \
  tests/test_story_63_roles_coordinator_assembly_fixtures.py \
  tests/test_story_64_content_parity_stub_live_evidence.py -q
```

No claim of live volume mount / Railway Pass / GPT-48 export Pass from this matrix.

---

## 3) Consume parity gate (AC-AIB-13-05) + Explicit Partial

| Gate | Behavior |
|------|----------|
| **Pass (live)** | Mounted/dir inventory matches GPT UI **export** Pass **and** ops window open **and** evidence recorded |
| **Fail** | Incomplete or mismatched content → `/readyz`-class **fail-closed** — no silent subset |
| **Hash/inventory wire format** | **Open** (joint GPT-48) — **not invented** here |

### Wave status (STORY-64 / this implement)

| Field | Value |
|-------|-------|
| Ops evidence window | **Not open** (mandatory live not required this wave) |
| GPT-48 export Pass | **Unknown** / not claimed |
| Live volume + parity E2E | **Unknown** / not claimed Done |
| AC-AIB-13-05 live side | **Explicit Partial** |
| Invented Railway / live SUCCESS | **Forbidden · Absent** |

### Live Pass checklist (ops · when window open)

| Step | Fact to record | Blocker if missing |
|------|----------------|--------------------|
| 1 | Ops evidence window open | Without window → stay **Partial** |
| 2 | GPT-48 export layout + aibridge-compatible manifest Present | Absent → ContentLoadError / not-ready |
| 3 | Volume mounted; `DOGESTONIA_INSTRUCTIONS_*` point at volume | Misconfig → fail-closed |
| 4 | Inventory/parity check Pass (format when joint SSOT lands) | Fail → not live Pass |
| 5 | Evidence artifact path + UTC in analysis/run-report | Absent record → cannot claim Done |

---

## 4) Incomplete fixture (AC-06 harness)

Broken fixture under `tests/fixtures/content/incomplete/` — manifest lists a missing root-child file → `ContentLoadError` / `/readyz` `content_verify_failed` (fail-closed).

---

## 5) Out of this note

Opening ops window · inventing hash SSOT · GPT-48 authoring bodies · ASGI roles wire invent (63 G-02 WAIVED) · telegram / gateway redesign.
