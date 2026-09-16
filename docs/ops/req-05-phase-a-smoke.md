# REQ-05 Phase A — ops smoke checklist

**Story:** STORY-AIBRIDGE-22 · **ADR-4** · **REQ-05** §4.5  
**Service:** `doge-ai-bridge`  
**Do not** invent live Railway SUCCESS here — record only what you observe.

Pins (local / image): see `.env.example` Phase A block and
`docs/runbooks/aibridge-web-service-local-railway.md` §1.1b.

## Checklist

1. [ ] Process up with **complete** Phase A content env:
   - `DOGESTONIA_CONTENT_SOURCE_COMMIT`
   - `DOGESTONIA_INSTRUCTIONS_DIR` → instructions **directory** (not a file path)
   - `DOGESTONIA_INSTRUCTIONS_MANIFEST` → `instructions.manifest.json`
   - `DOGESTONIA_OPENAPI_PATH` → Story Intake wire (`story-intake-actions.openapi.yaml`)
   - `DOGESTONIA_PAYLOAD_SCHEMA_PATH` → pack payload schema under instructions dump
2. [ ] `GET /healthz` → **200**
3. [ ] `GET /readyz` with full Phase A env → **not** failing for OAS / manifest / wiring:
   - reason must **not** be `content_bundle_not_ready` caused by missing OAS, incomplete
     manifest, or engine wiring gap
   - other readiness reasons (auth, dry-run, DB, …) are out of this Phase A content proof
4. [ ] (Optional local) automated proof:
   ```bash
   cd doge-ai-bridge && DATABASE_URL=memory AIBRIDGE_ALLOW_MEMORY_STORES=1 \
     .venv/bin/pytest tests/test_story_22_phase_a_proof.py -q --noconftest
   ```

## Explicit non-claims

- This checklist does **not** assert Railway deploy SUCCESS.
- Live n8n / Telegram / SPA HTTPS gates are out of REQ-05 Phase A Done.
- Phase B profiles (REQ-06) are **not** required for Phase A Done (§4.6).
