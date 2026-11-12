# STORY-AIBRIDGE-18 — P2 replicas / observability

## Meta
- **Key:** `STORY-AIBRIDGE-18-p2-replicas-observability`
- **Status:** Deferred
- **Parent REQ:** [`REQ-03`](../../../requirements/REQ-03-RUNTIME-REMEDIATION-AGREED.md) §7 P2-01–04
- **Package:** [`req-03-runtime-remediation/INDEX.md`](INDEX.md)
- **Skill declared:** `devops-engineer` — [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md)
- **Operator decision:** Deferred until after first node — **outside active dashboard %**.

## Scope (when activated)
- Multiple production ASGI **replicas** — deploy/load/capacity (not transactional correctness — that is P0/P1 / story 09).
- Dedicated Prometheus prompt-cache series.
- Distributed rate limiter / external APM.
- Credential-stripped n8n workflow JSON as ops template (not REQ-01 code blocker).

## Вне scope
- Re-doing DB concurrency (09); inventing mandatory n8n JSON before P2 activation.

## Target / AC
- [ ] P2-01…04 evidenced when operator promotes status Todo → active.

## Dependencies
- After wave-2 gates (14+) and first node experience.
