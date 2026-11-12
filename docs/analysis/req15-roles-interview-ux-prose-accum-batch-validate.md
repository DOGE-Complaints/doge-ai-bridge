# Validate — req15-roles-interview-ux-prose-accum-batch

**Status:** **Superseded** (2026-11-06) — do **not** execute. Successor: [STORY-GPT-ROL-05](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-05-channel-interview-stage-proactivity.md) / [06](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-06-channel-interview-surface-readability.md).

**Implement:** [`req15-roles-interview-ux-prose-accum-batch.md`](./req15-roles-interview-ux-prose-accum-batch.md) (Superseded)  
**Triage:** [`req15-tg-interviewer-ux-gap-triage-2026-11-06.md`](./req15-tg-interviewer-ux-gap-triage-2026-11-06.md)  
**Method:** [`.cursor/rules/analysis.mdc`](../../.cursor/rules/analysis.mdc)  
**MODE:** ~~validate only~~ — N/A while Superseded.

## Checks

| ID | Check | Pass when |
|----|-------|-----------|
| V1 | Proactive advance | Roles prose tells model to continue stages without waiting for «дальше» when data enough |
| V2 | Visual air | Guidance Present for short paragraphs / blank lines vs wall-of-bullets |
| V3 | Markers | Preference for light emoji / orange-ish Unicode over dense `**`; TG orange honesty noted |
| V4 | No vague UI | No «используйте интерфейс» without pointing to channel actions or post-stash URL behavior |
| V5 | Stash lock | `core.md` (or equivalent) still forbids model-owned stash/SPA redirect HTTP |
| V6 | OOS clean | No aibridge/telegram runtime edits in this batch |

## Report template

```text
PASS|FAIL
V1…V6: path cites
```
