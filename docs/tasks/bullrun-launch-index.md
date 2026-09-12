# AI Bridge — bullrun launch index (Builder Queue)

**Профиль:** `aibridge` · **Focus:** `doge-ai-bridge/` · **Стек:** Python (Responses → Story Intake bridge)  
**Pipeline:** [aibridge-story-execution-pipeline.md](./aibridge-story-execution-pipeline.md)  
**Active pkg:** [aibridge-active-package.current.yaml](./aibridge-active-package.current.yaml) · **pkg-000000** bootstrap marker  
**Requirement:** [REQ-01](../requirements/REQ-01-doge-ai-bridge-runtime.md) · Parent protocol [GPT UI REQ-47](../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md)  
**Remote:** https://github.com/DOGE-Complaints/doge-ai-bridge (`dev`)  
**Runtime plan:** [aibridge_builder.plan.md](../../../.cursor/plans/aibridge_builder.plan.md)  
**Contract:** [aibridge-operator-contract.md](../../../docs/methodology/Zeya888-builder-queue/contracts/aibridge-operator-contract.md)

## Актуальная точка

| Поле | Значение |
|------|----------|
| **Active pkg** | `pkg-000000-20260910-bootstrap.yaml` (1 path — t00 profile marker) |
| **Status** | Bootstrap Done (methodology). **Не** P3 product на t00. |
| **Next default** | `input_mode=requirement` on REQ-01 → PA/P1; or author `STORY-AIBRIDGE-*` → **P1.3** |
| **Verify** | `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify` → ok 1 paths |
| **Updated** | 2026-09-10T12:21:02Z |

## Packages

| Pkg | Label | Paths | Status |
|-----|-------|-------|--------|
| [pkg-000000](./aibridge-active-packages/pkg-000000-20260910-bootstrap.yaml) | bootstrap | 1 (t00) | Done (marker) |

## Epics / stories

*Empty until first P1 materialize.* Keys: `EPIC-AIBRIDGE-*` / `STORY-AIBRIDGE-*`.

## Input package (run metadata)

Column / field: `aibridge_input_package`.
