# STORY-AIBRIDGE-63 — Roles, coordinator, assembly (in-repo fixtures)

## Meta
- **Key:** `STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures`
- **Status:** **Done** · **Product Done** · pkg-000066 · P8 `1efea66`/`893cd39`/`9eb32f0` · G-02 WAIVED ASGI · next **STORY-64** · 2026-11-02T10:21:23Z
- **Parent Epic:** [`EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md`](../../EPIC-AIBRIDGE-11-req-13-req15-semantic-state-roles-instruction-assembly.md)
- **source:** `backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md`
- **decision_ref:** [`STORY-AIBRIDGE-63-….md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/STORY-AIBRIDGE-63-roles-coordinator-assembly-fixtures.md) · [`REQ-13`](../../../../requirements/REQ-13-REQ15-SEMANTIC-STATE-ROLES-INSTRUCTION-ASSEMBLY.md) · [`02-roles-coordinator-assembly.md`](../../../../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md)
- **Package:** [`req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md`](../../../../backlog-stories/req-13-req15-semantic-state-roles-instruction-assembly/INDEX.md)
- **Skill declared:** `python-pro`
- **Active pkg (wave):** `pkg-000066-20261102-epic-aibridge-11-story-63-roles-coordinator-assembly-fixtures.yaml`
- **P1 materialize:** 2026-11-02T09:05:07Z · [p1 APPLIED](../../../../../../.cursor/plans/p1_aibridge_63_scaffold_20261102T090322Z.plan.md)
- **Depends:** soft STORY-62 Done · REQ-12 interview port Present
- **OOS:** store DDL (62) · live volume/GPT-48 (64) · provider HTTP · telegram

## Doc pointers (read first)

| Topic | Where |
|-------|--------|
| Roles / coordinator / assembly | [`02-roles-coordinator-assembly.md`](../../../../architecture/req15-semantic-state-roles/02-roles-coordinator-assembly.md) |
| Arch overview | [`00-overview.md`](../../../../architecture/req15-semantic-state-roles/00-overview.md) |
| Soft state flags | STORY-62 `semantic_state/` Present |

## Scope
- Five v1 roles callable via coordinator; version pins; policy table → one next role (no LLM-router).
- Assembly: shared core + per-role slice + session pin from configured dir+manifest.
- Stub harness uses **in-repo fixtures** only — must not require GPT UI checkout.
- Model calls via REQ-12 interview port Keep.
- L13-1: understanding soft OK; send never auto from ordinary reply.
- AC-07: fixture role texts must not encode gateway stash/SPA redirect procedure.

## Вне scope
- Semantic store DDL body (62); live volume/GPT-48 export (64); provider HTTP; telegram.

## Verified current state
- Role registry: **Present** (`src/aibridge/roles/`) · P3 2026-11-02T09:16:58Z.
- `coordinator.py` — policy `select_next_role` + FC-less → interpret offer (L13-1 Keep).
- Assembly Present: `roles/assembly.py` · fixtures `tests/fixtures/content/roles-instructions/` + `roles.manifest.json`.
- `interview_providers/` Keep · `roles/invoke.py` → bind Keep.

## Target / AC
- [x] AC-AIB-13-02: five roles + pins via coordinator (harness).
- [x] AC-AIB-13-03: assemble only from configured dir+manifest (fixture env).
- [x] AC-AIB-13-07: role instruction fixtures do not own gateway/SPA procedure.
- [x] AC-AIB-13-08 / L13-1: ordinary reply ≠ send-permission offer.
- [x] Stub isolation: suite green without GPT UI tree.

## Nested tasks (pkg-000066)

| # | Task folder | Maps | Status |
|---|-------------|------|--------|
| t01 | [task-aibridge-63-t01-five-roles-version-pins-registry](./task-aibridge-63-t01-five-roles-version-pins-registry/README.md) | AC-02 · five roles + pins | Done |
| t02 | [task-aibridge-63-t02-coordinator-policy-one-role](./task-aibridge-63-t02-coordinator-policy-one-role/README.md) | D3 · policy → one role | Done |
| t03 | [task-aibridge-63-t03-assembly-dir-manifest-session-pin](./task-aibridge-63-t03-assembly-dir-manifest-session-pin/README.md) | AC-03 · D5 assembly | Done |
| t04 | [task-aibridge-63-t04-in-repo-fixtures-no-gpt-ui](./task-aibridge-63-t04-in-repo-fixtures-no-gpt-ui/README.md) | stub isolation | Done |
| t05 | [task-aibridge-63-t05-interview-port-keep-model-calls](./task-aibridge-63-t05-interview-port-keep-model-calls/README.md) | REQ-12 port Keep | Done |
| t06 | [task-aibridge-63-t06-l13-1-ordinary-reply-ne-send](./task-aibridge-63-t06-l13-1-ordinary-reply-ne-send/README.md) | AC-08 · L13-1 | Done |
| t07 | [task-aibridge-63-t07-ac07-fixtures-no-gateway-spa](./task-aibridge-63-t07-ac07-fixtures-no-gateway-spa/README.md) | AC-07 | Done |
| t08 | [task-aibridge-63-t08-story-gate-checklist](./task-aibridge-63-t08-story-gate-checklist/README.md) | package gate | PASS |
| t09 | [task-aibridge-63-t09-audit-g01-req13-t1-verified-state-sync](./task-aibridge-63-t09-audit-g01-req13-t1-verified-state-sync/README.md) | P4 G-01 · REQ T1 sync | **PASS** |

## Code points
- `coordinator.py` · `content.py` · `interview.py` · `interview_providers/` · `tests/fixtures/…` (path at implement)
