# REQ-05 package — activated skills (architecture deep-dive)

**Package:** [`req-05-content-phase-a-flat-launch`](./INDEX.md)  
**Parent REQ:** [`REQ-05`](../../../requirements/REQ-05-CONTENT-PHASE-A-FLAT-LAUNCH.md) v0.2.0  
**Purpose:** SSOT списка skills для **глубокой проработки архитектуры** решения Phase A (wiring + full manifest + OAS-in-image + proof), до/во время PA.3 / design notes.  
**Method rule (не skill):** [`.cursor/rules/analysis.mdc`](../../../../../.cursor/rules/analysis.mdc) — claims только после Read/Grep; name ≠ create.  
**As-of:** 2026-09-16 · skills verified on disk under workspace `.cursor/skills/`

**Activation rule for agents:** before architecture design / ADR / composition redesign for this package, **Read** every skill marked **ACTIVE** below (full `SKILL.md`), then apply. Story-level `Skill declared` remains binding for P3 implementation tasks.

Relative links resolve from this folder → workspace root `.cursor/skills/`.

---

## 1. ACTIVE — architecture deep-dive (package-level)

| Skill | Why for this package | Path |
|-------|----------------------|------|
| **architecture-designer** | Composition: deploy→engine order, stable-prefix vs tools, content pin vs image packaging; ADRs / trade-offs without spaceship | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/architecture-designer/SKILL.md) |
| **api-designer** | Two OAS contracts: Story Intake wire (`DOGESTONIA_OPENAPI_PATH`) vs channel façade; what enters image vs what enters `files[]` | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/api-designer/SKILL.md) |
| **openai-custom-gpt-builder** | Parity Module-1 Knowledge/Actions → bridge Responses; full dump semantics vs Custom GPT upload | [SKILL.md](../../../../../.cursor/skills/openai-custom-gpt-builder/SKILL.md) |
| **prompt-engineer** | Full-set assembly order in stable prefix; token/attention risks of large Module-1+pack JSON in prefix (design notes, not Phase A subset) | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/prompt-engineer/SKILL.md) |
| **code-documenter** | Env/runbook/manifest docs quality; keep packaging docs aligned with code | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/code-documenter/SKILL.md) |
| **code-reviewer** | Architecture/composition review of wiring + fail-closed readiness (pre-P3 design or post-diff) | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/code-reviewer/SKILL.md) |

---

## 2. ACTIVE — story implementation (from STORY Skill declared)

| Skill | Stories | Path |
|-------|---------|------|
| **python-pro** | 19, 20 | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/python-pro/SKILL.md) |
| **fastapi-expert** | 19 (composition / `create_app`) | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/fastapi-expert/SKILL.md) |
| **devops-engineer** | 21 (Dockerfile / openapi in image) | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/devops-engineer/SKILL.md) |
| **test-master** | 22 | [SKILL.md](../../../../../.cursor/skills/sources/jeffallan-claude-skills/skills/test-master/SKILL.md) |

---

## 3. Suggested load order (architecture session)

1. `analysis.mdc` (method)  
2. `architecture-designer`  
3. `openai-custom-gpt-builder` + `prompt-engineer` (content/prompt semantics)  
4. `api-designer` (OAS split)  
5. `fastapi-expert` + `python-pro` (as-built composition constraints)  
6. `devops-engineer` (image packaging)  
7. `code-documenter` / `code-reviewer` / `test-master` as needed for docs, review, proof design  

---

## 4. Explicitly NOT activated (out of Phase A / not on disk need)

| Skill / concern | Why excluded |
|-----------------|--------------|
| nested-loader / layered-manifest invent | REQ-05 / REQ-06 out of Done |
| `postgres-pro` | No new DB schema in this package (registry already Done STORY-02) |
| `kubernetes-specialist` / heavy IaC | Railway Dockerfile slice only |
| REQ-06 multi-repo CI platform | Separate REQ |

---

## 5. Story ↔ skill map (quick)

| Story | Implementation skills | Architecture skills to consult |
|-------|----------------------|--------------------------------|
| [19](./STORY-AIBRIDGE-19-assembled-instructions-engine-wire.md) | python-pro, fastapi-expert | architecture-designer, prompt-engineer |
| [20](./STORY-AIBRIDGE-20-full-instructions-manifest.md) | python-pro | openai-custom-gpt-builder, prompt-engineer |
| [21](./STORY-AIBRIDGE-21-oas-image-env-docs.md) | devops-engineer | api-designer, code-documenter |
| [22](./STORY-AIBRIDGE-22-content-phase-a-proof.md) | test-master | code-reviewer |

---

## 6. Version log

- v0.1.0 — 2026-09-16: identified + activated for package architecture deep-dive; paths verified under workspace `.cursor/skills/`.
