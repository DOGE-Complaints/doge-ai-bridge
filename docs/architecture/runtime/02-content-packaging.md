# Content packaging & pin

**Parent REQ:** [REQ-01 §8–§9, §17–§18](../../requirements/REQ-01-doge-ai-bridge-runtime.md)  
**Overview:** [00-overview.md](./00-overview.md)

---

## 1. Method note

**Git ownership ≠ image packaging.**  
Owning files under `GPT UI/instructions` or a pack tree in the monorepo does **not** place them in the Railway container. A deliberate CI/image step must copy pinned artifacts.

---

## 2. What is bundled

Per [REQ-01 §8 AIB-INS-04](../../requirements/REQ-01-doge-ai-bridge-runtime.md):

- Manifest-listed instruction files only (root children; no recursive archive/onboarding).
- Canonical Story Intake OpenAPI YAML.
- Active pack `payload.schema.json` (+ identity used at readiness).
- Recorded `DOGESTONIA_CONTENT_SOURCE_COMMIT`, bundle/OAS/pack hashes at startup.

Runtime must **not** fetch mutable instructions from GitHub at request time.

---

## 3. CI shape (interview T4 = B)

```text
Content owners merge to Git
        ↓
Aibridge operator selects commit SHA
        ↓
CI content stage → immutable tarball (instructions + OAS + pack + commit id)
        ↓
Docker build (aibridge app + tarball)
        ↓
/readyz + façade smoke → redeploy
```

Merge to content paths must **not** auto-promote production (interview T8 = B).

Exact absolute paths for OAS/pack sources in the monorepo: **Unknown** until implement pins them in CI config.

---

## 4. Multi-bundle retention (interview T8)

Sessions pin instruction/tool/pack versions for their lifetime ([REQ-01 §8 AIB-INS-03](../../requirements/REQ-01-doge-ai-bridge-runtime.md)).  
With session TTL **7 days**, a redeploy that drops the previous bundle breaks in-flight sessions.

**Preferred architecture:** keep **current + still-referenced** bundle versions; GC when no session references a version.  
**Fallback (not preferred):** controlled termination of old sessions.  
Physical mechanism (volume vs multi-version layers vs object store): **Unknown** — document choice at implement.

---

## 5. Verify surfaces

| Surface | Role |
|---------|------|
| Unit tests on loaders | Dev/CI correctness |
| `/readyz` | Production entry: DB, secrets, hashes, tool strictness, pack match |
| Façade smoke (V2) | Deploy gate: auth boundary alive |
| Contract tests vs channel OpenAPI | When OpenAPI file exists |

Do not treat “src unit tests green” alone as production packaging proof.
