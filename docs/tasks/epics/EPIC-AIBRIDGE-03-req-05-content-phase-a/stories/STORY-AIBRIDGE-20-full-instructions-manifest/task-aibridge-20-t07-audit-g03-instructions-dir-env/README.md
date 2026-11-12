# Task: ops — fix local `DOGESTONIA_INSTRUCTIONS_DIR` (G-03)

**Status:** Done  
**Skill declared:** python-pro  
**Wave:** `run_mode=aibridge_20_audit_20260916`  
**Gap:** G-03 (Medium) — P4 audit 2026-09-16  
**Decision Ref:** `doge-ai-bridge/docs/analysis/p4-audit-STORY-AIBRIDGE-20-full-instructions-manifest-20260916.md`  
**Parent story:** [`STORY-AIBRIDGE-20-full-instructions-manifest.md`](../STORY-AIBRIDGE-20-full-instructions-manifest.md)  
**P5 scaffold:** 2026-09-16T12:41:29Z  
**P6 Done:** 2026-09-16T12:47:01Z

## Purpose

Point local `DOGESTONIA_INSTRUCTIONS_DIR` at the instructions **directory** (`src/instructions` or image `/app/…`), not a non-existent `…/manifest.json` file path. Confirm path is a directory so load / `content_configured` can use the full dump.

**Out of this task:** inventing Phase A pins in `.env.example` / runbook (owned by **STORY-21**); loader schema / fail-closed dir↔`files[]` (G-02 WAIVED → STORY-22); product code beyond env pin; inventing new AC.

## Code Facts (verified exists — post P6)

1. Local `.env` `DOGESTONIA_INSTRUCTIONS_DIR=src/instructions` — existing directory.
2. `DOGESTONIA_PAYLOAD_SCHEMA_PATH` left as-is (pack payload JSON).
3. Phase A `.env.example` documentation remains **STORY-21** (not invented here).

## AC/DoD

- [x] If `doge-ai-bridge/.env` is present: `DOGESTONIA_INSTRUCTIONS_DIR` resolves to an existing **directory** (canonical local: `src/instructions`).
- [x] Note recorded that Phase A `.env.example` documentation remains **STORY-21** (no invent here).
- [x] No `content.py` schema change; no invent of new product AC.
- [x] `Skill declared: python-pro` present.

## Where to change

- `doge-ai-bridge/.env` (local only, if present) — `DOGESTONIA_INSTRUCTIONS_DIR` value

## Verification commands (P6)

```bash
# Do not print secrets; only assert DIR key points at a directory
python3 - <<'PY'
from pathlib import Path
p = Path("doge-ai-bridge/.env")
if not p.is_file():
    print("SKIP: no .env")
    raise SystemExit(0)
raw = p.read_text()
val = None
for line in raw.splitlines():
    if line.startswith("DOGESTONIA_INSTRUCTIONS_DIR="):
        val = line.split("=", 1)[1].strip().strip('"').strip("'")
        break
assert val, "missing DOGESTONIA_INSTRUCTIONS_DIR"
target = Path("doge-ai-bridge") / val if not Path(val).is_absolute() else Path(val)
alt = Path(val)
ok = target.is_dir() or alt.is_dir() or (Path("doge-ai-bridge") / alt).is_dir()
print("DIR=", val, "is_dir=", ok)
assert ok, f"INSTRUCTIONS_DIR must be a directory: {val}"
PY
```
