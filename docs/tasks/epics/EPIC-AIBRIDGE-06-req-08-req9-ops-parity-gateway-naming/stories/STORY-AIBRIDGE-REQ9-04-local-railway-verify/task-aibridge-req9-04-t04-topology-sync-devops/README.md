# Task: docs — topology sync (Make + probes + GATEWAY_*)

**Status:** Done · 2026-09-26T13:03:46Z  
**Skill declared:** code-documenter  
**Decision Ref:** `doge-ai-bridge/docs/tasks/backlog-stories/req-08-req9-ops-parity-gateway-naming/STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`  
**Parent story:** [`STORY-AIBRIDGE-REQ9-04-local-railway-verify.md`](../STORY-AIBRIDGE-REQ9-04-local-railway-verify.md)  
**P1 scaffold:** 2026-09-26T12:58:34Z  
**Maps:** tech-arch 04 topology

## Purpose

Sync `docs/network-architecture/dogestonia-microservices-devops-topology.md` (workspace) for aibridge Make start, `/health`/`/ready`, GATEWAY_* auth matrix when facts exist; else note residual / do not invent closed gaps.

## AC/DoD

- [x] Topology rows updated to match verified facts **or** residual/skip documented.
- [x] No invent waitlist / nginx / closed gaps without evidence.
- [x] `Skill declared: code-documenter` present.

## Where to change (P3)

- `docs/network-architecture/dogestonia-microservices-devops-topology.md` (DOGEstonia root docs)

## Evidence

- Acceptance: `acceptance-verification-task-aibridge-req9-04-t04-topology-sync-devops.md` (create at P3 close)
