# STORY-AIBRIDGE-REQ9-01 — Makefile serve/dev + .env + railpack 8080

## Meta
- **Key:** `STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack`
- **Status:** P6 Done · G-01/G-02/G-03 **CLOSED** · next **P7** · pkg-000045 · 2026-09-26T12:20:13Z · [p6](../../run-reports/run-summary-20260926-1220-story-aibridge-req9-01-p6.md) · [p3](../../run-reports/run-summary-20260926-1214-story-aibridge-req9-01-p3.md)
- **Parent REQ:** [`REQ-08`](../../../requirements/REQ-08-REQ9-OPS-PARITY-AND-GATEWAY-NAMING.md) §1–§2 · G1 G3 G8 G9
- **Tech-arch:** [`01-runtime-and-probes.md`](../../../../../docs/architecture/req9-ops-naming/01-runtime-and-probes.md)
- **Package:** [`INDEX.md`](INDEX.md)
- **Siblings:** [02](STORY-AIBRIDGE-REQ9-02-health-ready-aliases.md) · [03](STORY-AIBRIDGE-REQ9-03-gateway-spa-env-hard-cut.md) · [04](STORY-AIBRIDGE-REQ9-04-local-railway-verify.md); identity `STORY-IDS-REQ9-01` (G8 etalon)
- **Skill declared:** `python-pro` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md) · soft `devops-engineer` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md)
- **Emitted:** 2026-09-26T12:02:45Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Pipeline:** [`STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md`](../../epics/EPIC-AIBRIDGE-06-req-08-req9-ops-parity-gateway-naming/stories/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack/STORY-AIBRIDGE-REQ9-01-make-serve-env-railpack.md)

## Scope
- Add `Makefile`: `serve` / `dev` → uvicorn `aibridge.app:app` on `:8080` with required `.env` load (`set -a && . ./.env && set +a`, G8).
- README primary start → `make serve` / `make dev` (G1); `python -m aibridge` may remain thin alias.
- `railpack.json` startCommand: `${PORT:-8080}` (G3); keep `aibridge.app:app` (G9).

## Out of scope
- Probe aliases (02); env/Python hard-cut R1/R2/R4 (03); Railway live verify (04).
- Renaming channel Bearer to `SERVICE_API_TOKEN`.

## Verified current state
- **Makefile present** — `serve`/`dev` load `./.env` via `set -a && . ./.env && set +a`; uvicorn `aibridge.app:app` `$${PORT:-8080}` (P3 2026-09-26T12:14:54Z).
- README Quick start primary: `make serve` / `make dev`; thin alias `PORT=8080 python -m aibridge`.
- `__main__.py` runs `aibridge.app:app` (`src/aibridge/__main__.py`).
- `railpack.json`: `${PORT:-8080}` (G3).

## Target / AC
- [x] G1 Makefile + README primary start
- [x] G8 `.env` required on Make serve/dev
- [x] G3 railpack fallback 8080
- [x] G9 uvicorn app string `aibridge.app:app`

## Code points
- `Makefile`; `README.md`; `railpack.json`; `src/aibridge/__main__.py` (G9 unchanged)

## Dependencies
- None (∥ 02)
