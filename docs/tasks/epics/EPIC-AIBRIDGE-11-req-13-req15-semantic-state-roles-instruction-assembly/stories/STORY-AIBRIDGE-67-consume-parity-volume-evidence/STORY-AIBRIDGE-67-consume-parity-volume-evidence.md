# STORY-AIBRIDGE-67 — Consume parity + volume evidence (Track B)

## Meta
- **Key:** `STORY-AIBRIDGE-67-consume-parity-volume-evidence`
- **Status:** 🟢 **Done · Product Done · Code Done** · pkg-000070 · P8 `75f5f95`/`ca77c69`/`d6430fe` · 2026-11-05T12:30:45Z · AC-05 live **Explicit Partial** (t07 · G-03 WAIVE) · stale ≠ Export Pass
- **Parent Epic:** [`EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md`](../../EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md)
- **source:** `backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md`
- **decision_ref:** [`STORY-AIBRIDGE-67-….md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-67-consume-parity-volume-evidence.md) · [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) AC-05/04/06 · gap V8 / G7 Track B
- **Package:** [`req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000070-20261105-epic-aibridge-11-story-67-consume-parity-volume-evidence.yaml`
- **activation (audit):** `run_mode=aibridge_67_audit_20261105`
- **P1 materialize:** 2026-11-05T11:57:24Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_67_scaffold_20261105T115528Z.plan.md)
- **P3 execute:** 2026-11-05T12:02:38Z · t01–t06 Done · t07 Explicit Partial · t08 Done
- **P5 APPLY:** 2026-11-05T12:22:28Z · [p5 APPLIED](../../../../../../.cursor/plans/p5_aibridge_67_gap_20261105T121931Z.plan.md) · G-01/G-02 TASKED t09/t10 · G-03 WAIVE
- **P6:** 2026-11-05T12:26:35Z · t09/t10 **Done** · G-01/G-02 CLOSED · [run-summary](../../../../run-reports/run-summary-20261105-1226-story-aibridge-67-p6-t09-t10.md)
- **P7/P8:** 2026-11-05T12:30:45Z · [p7](../../../../analysis/p7-reaudit-STORY-AIBRIDGE-67-consume-parity-volume-evidence-20261105.md) · Code Done · live AC-05 Explicit Partial
- **Depends:** hard STORY-66 Done · soft GPT-48 Export Pass reconfirm (t01 Block stale) · soft ops window (t07 Absent)
- **OOS:** GPT-48 authoring · invent alternate hash · invent Railway/live SUCCESS · telegram packaging · Parent Phase F reaudit · CI auto-sync
- **Honesty:** **Code Done** OK · live AC-05 remains **Explicit Partial** · adopt **GPT E1** only · stale evidence ≠ Export Pass · do **not** invent Railway/live SUCCESS

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Volume / parity arch | [`03-content-volume-parity-verify.md`](../../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) · [`runtime/02`](../../../../architecture/runtime/02-content-packaging.md) |
| GPT E1 | [`GPT UI …/03-publish-verify-parity.md`](../../../../../../GPT%20UI/docs/architecture/req-48-role-oriented-instruction-line/03-publish-verify-parity.md) |
| Runtime | [`11`](../../../../runtime-docs/11-content-volume-parity-stub-live-evidence.md) · [`13`](../../../../runtime-docs/13-roles-schema-channel-cutover.md) · [`14`](../../../../runtime-docs/14-hybrid-c-volume-consume-parity-runbook.md) |
| Soft peers | 64 Explicit Partial · 65/66 Done |

## Scope
- Evidence Consume Pass vs GPT-48 Export Pass inventory/hash — joint wire = **Present GPT E1** (no invent alternate).
- Prod-capable read via configured dir / Railway volume (hybrid C · L13-2); authoring remains GPT UI.
- Close Explicit Partial on AC-AIB-13-05 when live/volume window + evidence Present; else stay Explicit Partial.

## Вне scope
- Channel wire (65) / roles-schema cutover (66) — Done prerequisites.
- GPT-48 mapping/archive authoring / rewriting instruction bodies.
- Telegram/Railway packaging peer; invent hash beyond E1; invent live SUCCESS.

## Verified current state (P3)
- E1 wire **Locked** in REQ-13 / runtime-11 · comparator Present (`export_parity.py`) · `/readyz` mismatch + seam fail-closed.
- Export preflight: path/hash **stale** → Explicit Block on Export Pass claim.
- Live Railway volume evidence **Absent** → t07 Explicit Partial.

## Target / AC
- [x] Consume Pass evidence vs export inventory Present (code/harness via t03–t05; live via t07 → Partial).
- [x] Volume/hybrid C read path documented + proven (t06; t07 ops Absent → Partial).
- [x] Joint inventory locked = E1 (t02) without inventing alternate format.
- [x] Package/REQ honesty: code Done ≠ live AC-05 Pass without t07 (Explicit Partial OK).

## Nested tasks (pkg-000070)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-67-t01-export-preflight-reconfirm-e1](./task-aibridge-67-t01-export-preflight-reconfirm-e1/README.md) | export preflight · E1 | Done |
| t02 | [task-aibridge-67-t02-lock-joint-inventory-e1](./task-aibridge-67-t02-lock-joint-inventory-e1/README.md) | lock E1 docs | Done |
| t03 | [task-aibridge-67-t03-consume-comparator-module](./task-aibridge-67-t03-consume-comparator-module/README.md) | AC-05 code | Done |
| t04 | [task-aibridge-67-t04-readyz-parity-fail-closed-seam](./task-aibridge-67-t04-readyz-parity-fail-closed-seam/README.md) | AC-06 · seam | Done |
| t05 | [task-aibridge-67-t05-harness-parity-matrix](./task-aibridge-67-t05-harness-parity-matrix/README.md) | harness | Done |
| t06 | [task-aibridge-67-t06-hybrid-c-volume-runbook](./task-aibridge-67-t06-hybrid-c-volume-runbook/README.md) | AC-04 docs | Done |
| t07 | [task-aibridge-67-t07-live-volume-evidence-ops-window](./task-aibridge-67-t07-live-volume-evidence-ops-window/README.md) | live · Partial OK | **Partial** · G-03 WAIVE |
| t08 | [task-aibridge-67-t08-story-gate-checklist](./task-aibridge-67-t08-story-gate-checklist/README.md) | package gate | Done |
| t09 | [task-aibridge-67-t09-audit-g01-backlog-verified-refresh](./task-aibridge-67-t09-audit-g01-backlog-verified-refresh/README.md) | P5 G-01 | **Done** · P6 |
| t10 | [task-aibridge-67-t10-audit-g02-runtime-readme-index-14](./task-aibridge-67-t10-audit-g02-runtime-readme-index-14/README.md) | P5 G-02 | **Done** · P6 |

## Code points
- `src/aibridge/export_parity.py` · `content.py` · `deployment.py` · `readiness.py` · `config.py` · `app.py`
- `src/aibridge/roles/assembly.py` (session pin ≠ file inventory)
- Peer: `GPT UI/instructions-roles/` · GPT E1 · Keep dual-confirm
