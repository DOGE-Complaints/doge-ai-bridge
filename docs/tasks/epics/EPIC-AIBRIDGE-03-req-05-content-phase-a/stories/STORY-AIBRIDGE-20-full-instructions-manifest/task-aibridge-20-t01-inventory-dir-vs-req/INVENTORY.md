# Inventory — `src/instructions/` vs REQ-05 §4.2 (t01)

**Date:** 2026-09-16T12:32:27Z (P3)  
**Dir:** `doge-ai-bridge/src/instructions/` (root children only)  
**Manifest excluded:** `instructions.manifest.json`  
**Invented files:** none

## Layer map (REQ-05 §4.2)

| Layer | Files present in dir |
|-------|----------------------|
| 1 Wrappers | `root.md` → `bootstrap.md` → `base.md` → `communication-presets-reference.md` |
| 2 Navigation / model | `instruction-modules-index.md` → `story-data-model.md` → `story-label-taxonomy.md` |
| 3 Interview / i18n / lifecycle | `story-interview-flow.md` → `story-i18n-policy.md` → `story-lifecycle-instructions.md` |
| 4 Strict chain | `ingest-validation.md` → `ingest-deep-parsing.md` → `safety-compliance.md` → `story-policy-gate.md` → `story-normalizer.md` |
| 5 HTTP / wire companion | `api-orchestrator.md` → `story-api-methods-reference.md` |
| 6 Pack uus_veerenni_civic v3 | `schema-packs.README.md` → `…interview-overlay.md` → `…inbound-validation.md` → `…locale-jurisdiction.md` → `…pack.json` → `…payload.schema.json` → `…taxonomy.json` |
| 7 Legacy | `activity-legacy-paths-inventory.md` |

**Count:** 25 root-children + manifest = 26 entries. No extras vs §4.2 list.

## Ordered candidate `files[]` (t02)

Same order as table (25 names). Pack JSON is in layer 6.
