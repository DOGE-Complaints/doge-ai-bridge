# Task: test — canonical pack unchanged by projection (§5.1 #2)

**Status:** Done · P3 2026-09-24T11:52:39Z  
**Skill declared:** test-master  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-07-openai-strict-schema-compat/STORY-AIBRIDGE-44-compat-merge-gate-proof.md`  
**Parent story:** [`STORY-AIBRIDGE-44-compat-merge-gate-proof.md`](../STORY-AIBRIDGE-44-compat-merge-gate-proof.md)  
**P1 scaffold:** 2026-09-24T11:49:26Z  
**P3 closed:** 2026-09-24T11:52:39Z  
**Maps:** TECH-ARCH §5.1 #2 · AC-01 · REQ-07

## Purpose

Merge-gate proof: canonical pack object/file still contains houses `uniqueItems: true` after projection; projection must not mutate pack source.

## AC/DoD

- [x] Canonical pack houses rule retains `"uniqueItems": true` (AC-01 seam).
- [x] Projection does not mutate pack source semantics.
- [x] No pack JSON weakening / delete invent.
- [x] `Skill declared: test-master` present.

## Where changed

- `tests/test_req07_merge_gate.py` — `test_merge_gate_canonical_pack_unchanged_by_projection`
