# Acceptance — task-aibridge-51-t09-audit-g01-env-example-provider-selectors

| Field | Value |
|-------|-------|
| **Date** | 2026-10-16T10:58:46Z |
| **Result** | **PASS** |

## Disk facts

| Claim | Evidence |
|-------|----------|
| Selectors documented | `.env.example` has `AIBRIDGE_WORKER_TEXT_BRIEF_PROVIDER` + `AIBRIDGE_WORKER_IMAGE_POSTER_PROVIDER` near model knobs |
| Default note | Comment: unset/blank → `mock`; values `mock`\|`openai` |
| Scope | No accept wire / allow-mock / live OpenAI product changes |
| Cite | `src/aibridge/config.py` provider fields Present |
