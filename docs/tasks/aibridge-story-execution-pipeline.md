# AI Bridge — Story execution pipeline

> **Профиль Builder Queue:** `aibridge`  
> **Операторский маршрут:** [`docs/methodology/Zeya888-builder-queue/core/workflow.md`](../../../docs/methodology/Zeya888-builder-queue/core/workflow.md) §P1–P8  
> **Runtime plan:** [`.cursor/plans/aibridge_builder.plan.md`](../../../.cursor/plans/aibridge_builder.plan.md)

## SSOT

| Слой | Источник |
|------|----------|
| Builder Queue statuses | [`bullrun-launch-index.md`](bullrun-launch-index.md) |
| Очередь исполнения | immutable `aibridge-active-packages/pkg-*.yaml` |
| Backlog | [`backlog-stories/INDEX.md`](backlog-stories/INDEX.md) |
| Requirements | [`doge-ai-bridge/docs/requirements/REQ-01-….md`](../requirements/REQ-01-doge-ai-bridge-runtime.md) · parent [GPT UI REQ-47](../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md) |
| Parent protocol | [`REQ-47`](../../../GPT%20UI/docs/requirements/REQ-47-responses-api-https-bearer-bridge.md) (do not duplicate framing) |
| Operator contract | [`aibridge-operator-contract.md`](../../../docs/methodology/Zeya888-builder-queue/contracts/aibridge-operator-contract.md) |
| Tests | `cd doge-ai-bridge && python3 -V` (`profiles.yaml` → `test_command`; product tests after scaffold) |

## Skill routing

| Зона | Skill |
|------|-------|
| Python runtime / FastAPI-style / tests | `python-pro` |
| Task README override | as declared in README |

## Перед batch-run (обязательно)

1. [`bullrun-launch-index.md`](bullrun-launch-index.md) §«Актуальная точка».
2. [`aibridge-active-package.current.yaml`](aibridge-active-package.current.yaml) → `package_file`.
3. `python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify`
4. Epic/story without materialized task queue → **P1.1** / **P1.3**, not P3 Execute.
5. One `input_mode` per session (contract §4).
6. **Не** смешивать с `builder_project: gpt` без явной команды.

## Gate: Story AC / Epic AC

After last task in story — Story parent AC; after epic — Epic AC. Live gates = task README (+ pytest when present).

## Build window

```bash
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --verify
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --list
python3 docs/methodology/Zeya888-builder-queue/cli/builder_resolve_queue.py --project aibridge --write-build-window --window-flat-start 1 --window-flat-end K
```

## Artifact dates

SSOT: [`builder-artifact-dates.md`](../../../docs/methodology/Zeya888-builder-queue/guides/builder-artifact-dates.md).

## Аудит (P4 / P7)

Reports: `doge-ai-bridge/docs/analysis/` (создать при необходимости). Disposition — workflow §P5/§P7.
