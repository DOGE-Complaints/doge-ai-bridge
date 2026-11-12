# STORY-AIBRIDGE-67 — Consume parity + volume evidence (Track B)

## Meta
- **Key:** `STORY-AIBRIDGE-67-consume-parity-volume-evidence`
- **Status:** 🟢 **Done · Product Done · Code Done** · pkg-000070 · P8 · 2026-11-05T12:30:45Z · AC-05 live **Explicit Partial** (t07) · E1 Locked · stale ≠ Export Pass
- **Parent REQ:** [`REQ-13`](../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) AC-AIB-13-05 · AC-04/06 · §3b · parent AC-REQ15-13/14
- **Tech-arch:** [`req15-semantic-state-roles/03-content-volume-parity-verify.md`](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) · peer [`runtime/02-content-packaging.md`](../../../architecture/runtime/02-content-packaging.md)
- **Runtime:** [`11`](../../../runtime-docs/11-content-volume-parity-stub-live-evidence.md) · [`13`](../../../runtime-docs/13-roles-schema-channel-cutover.md) · [`14`](../../../runtime-docs/14-hybrid-c-volume-consume-parity-runbook.md)
- **GPT peer E1:** [`GPT UI …/03-publish-verify-parity.md`](../../../../../GPT%20UI/docs/architecture/req-48-role-oriented-instruction-line/03-publish-verify-parity.md) (Export Pass semantics — joint lock input)
- **Gap order:** [`req15-gap-closure-execution-order-2026-11-03.md`](../../../../../docs/analysis/req15-gap-closure-execution-order-2026-11-03.md) **G7**
- **Package:** [`INDEX.md`](INDEX.md)
- **Gap:** V8 (full) · AC-14 hybrid C
- **Siblings:** [64](STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) · [65](STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) · [66](STORY-AIBRIDGE-66-roles-schema-channel-cutover.md)
- **Skill declared:** `python-pro` · soft ops
- **Emitted:** 2026-11-03 · Tech subtasks: 2026-11-05 · P6 hygiene: 2026-11-05T12:26:35Z
- **Method:** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc)
- **Product Done honesty:** **Code/docs Done** after t01–t06 + t08 with **AC-05 Explicit Partial** if t07 ops window closed. **Full live / AC-05 Pass** only with t07 evidence artifact + UTC. Stale GPT export evidence must **not** be cited as Export Pass. Do **not** invent Railway / live SUCCESS.

## Scope
- Evidence **Consume Pass** vs GPT-48 **Export Pass** inventory/hash — joint wire = **Present GPT E1** (roles-schema root children + SHA-256 after `normalize_text` / `sha256_hex`); do **not** invent alternate format (t02 locks into aibridge docs).
- Prod-capable read via configured dir / Railway volume (hybrid C · L13-2); authoring remains GPT UI; reconcile with runtime/02 (Git ≠ volume).
- Close Explicit Partial on AC-AIB-13-05 when live/volume window + evidence Present; else stay Explicit Partial.

## Out of scope
- Channel wire (65) / roles-schema cutover (66) — prerequisites (**Done**).
- GPT-48 mapping/archive authoring / rewriting instruction bodies.
- Telegram/Railway packaging (peer telegram STORY-06).
- Parent Phase F Product Done re-audit (G7 F Open — after evidence).
- Invent hash SSOT beyond E1; automatic CI sync (GPT V3 rejected).

## Verified current state

| Fact | Status | Cite |
|------|--------|------|
| STORY-64 gate/docs + stub | **Present** · AC-05 Explicit Partial residual | [64](STORY-AIBRIDGE-64-content-parity-stub-live-evidence.md) · runtime [`11`](../../../runtime-docs/11-content-volume-parity-stub-live-evidence.md) |
| STORY-65 ASGI channel wire | **Present** · Product Done | [65](STORY-AIBRIDGE-65-asgi-channel-semantic-roles-wire.md) |
| STORY-66 roles-schema cutover | **Present** · Product Done · G3 closed | [66](STORY-AIBRIDGE-66-roles-schema-channel-cutover.md) · runtime [`13`](../../../runtime-docs/13-roles-schema-channel-cutover.md) |
| STORY-66 local “consume” | **Layout/load smoke only** — **≠** hash Consume Pass | `tests/test_story_66_roles_schema_channel_cutover.py` |
| Export tree GPT UI | **Present** | `GPT UI/instructions-roles/` + `roles.manifest.json` |
| GPT export evidence artifact | **Present but stale** (path / `core.md` hash drift) — **Explicit Block** on Export Pass claim (t01) | [`story-67-export-preflight-e1-reconfirm-20261105.md`](../../../analysis/story-67-export-preflight-e1-reconfirm-20261105.md) · peer `GPT UI/docs/analysis/req-48-export-parity-evidence.md` |
| Joint inventory/hash wire | **Locked = GPT E1** (t02) — `wire: e1` · `normalize_text`+`sha256_hex`; session_pin ≠ file inventory | REQ-13 §3b/§7 · runtime [`11`](../../../runtime-docs/11-content-volume-parity-stub-live-evidence.md) |
| Consume comparator vs export inventory | **Present** | [`export_parity.py`](../../../../src/aibridge/export_parity.py) · `tests/test_story_67_consume_parity_volume_evidence.py` |
| Incomplete/local fail-closed | **Present** | `content.py` · `deployment.py` · `readiness.py` · STORY-64 fixtures |
| Export-mismatch fail-closed | **Present** | `readiness.py` + `DOGESTONIA_EXPORT_INVENTORY_PATH` (when configured) |
| `DOGESTONIA_ROLES_*` vs `INSTRUCTIONS_*` readiness seam | **Present** · fail-closed `roles_instructions_seam_mismatch` (t04) | `config.py` · `readiness.py` |
| Hybrid-C volume runbook | **Present** | runtime [`14`](../../../runtime-docs/14-hybrid-c-volume-consume-parity-runbook.md) · README index (t10) |
| Railway volume mount evidence | **Absent** · AC-05 live **Explicit Partial** (t07 · G-03 WAIVE) | [`story-67-live-volume-evidence-explicit-partial-20261105.md`](../../../analysis/story-67-live-volume-evidence-explicit-partial-20261105.md) — **no invent** SUCCESS |
| Hard dep 66 | **Done** | — |
| Soft: GPT-48 Export Pass | Stale evidence ≠ Export Pass until peer refresh | t01 |

## Target / AC
- [x] Consume Pass evidence vs export inventory Present (code/harness via t03–t05; live via t07 → Explicit Partial).
- [x] Volume/hybrid C read path documented (t06; t07 ops Absent → Partial).
- [x] Parent AC-13/14 honesty: code Done ≠ live Pass without t07 (Partial OK).
- [x] Joint inventory locked = E1 (t02) without inventing alternate format.
- [x] Package/REQ honesty: code Done ≠ live AC-05 Pass without t07.

## Code points
- `src/aibridge/export_parity.py` · `content.py` (`normalize_text` · `sha256_hex` · roles-schema)
- `src/aibridge/deployment.py` · `readiness.py` · `config.py` · `app.py` (INSTRUCTIONS_/ROLES_ wire + seam)
- `src/aibridge/roles/assembly.py` (session pin ≠ file inventory hash)
- Peer export: `GPT UI/instructions-roles/`
- Tests: `tests/test_story_67_consume_parity_volume_evidence.py` · `tests/fixtures/parity/`
- Evidence: `docs/analysis/story-67-*` · runtime [`14`](../../../runtime-docs/14-hybrid-c-volume-consume-parity-runbook.md)

## Technical subtasks (arch-bound)

| ID | Subtask | Arch cite | AC / DoD | Touch | OOS | Status |
|----|---------|-----------|----------|-------|-----|--------|
| **t01** | Export preflight: reconfirm GPT `instructions-roles/` vs E1 evidence; block Pass claim on stale path/hash | [`03` §2](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) · GPT E1 · REQ-13 §3b | Gate before consume claim | Peer evidence / cite only | GPT authoring rewrite | **Done** |
| **t02** | Lock joint inventory = **E1** | [`03` §2](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) · GPT E1 | Joint wire locked without invent | REQ-13 · runtime-docs/11 | Alternate hash schemes | **Done** |
| **t03** | Consume comparator | [`03` §2](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) | AC-AIB-13-05 code side | `export_parity.py` | Invent format · live Railway | **Done** |
| **t04** | Readyz parity fail-closed + seam | [`03` §2](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) · L13-2 · AC-06 | AC-AIB-13-06 + AC-05 gate | `readiness.py` · `config.py` | Telegram/gateway redesign | **Done** |
| **t05** | Harness parity matrix | [`03` §3](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) stub · D6 | Tech accept AC-05/06 | `tests/` + fixtures/parity | Live volume mount | **Done** |
| **t06** | Hybrid-C volume runbook | [`03` §1](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) · L13-2 | AC-AIB-13-04 full | runtime-docs/14 | Automatic CI sync | **Done** |
| **t07** | Live evidence (ops window) | [`03` §3](../../../architecture/req15-semantic-state-roles/03-content-volume-parity-verify.md) live · G7 | AC-AIB-13-05 live Pass | analysis Explicit Partial | Invent SUCCESS without window | **Partial** · G-03 WAIVE |
| **t08** | Story gate | [`00-overview`](../../../architecture/req15-semantic-state-roles/00-overview.md) D6 | Package gate | pipeline · INDEX · REQ-13 | Parent Phase F | **Done** |
| **t09** | Audit G-01 backlog §Verified refresh | P5 disposition | SSOT hygiene | this backlog file | invent AC | **Done** · P6 |
| **t10** | Audit G-02 runtime README → 14 | P5 disposition | SSOT hygiene | `runtime-docs/README.md` | invent live SUCCESS | **Done** · P6 |

## Dependencies
- Hard: STORY-66 cutover (**Done** · roles-schema live on channel).
- Soft: GPT-48 Export Pass **reconfirmed** (t01) — tree Present; evidence stale ≠ Export Pass.
- Soft: ops evidence window for t07 live Pass — **Absent** → Explicit Partial.
