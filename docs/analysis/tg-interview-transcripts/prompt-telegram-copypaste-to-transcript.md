# Prompt — Telegram copy-paste → labeled interview transcript

**Use when:** operator pastes a raw Telegram chat export/copy and asks to materialize a dialogue `.md` for this folder.  
**Method:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc)  
**Deliverable class:** transcript extract only — **no** process/G4 analysis unless a separate ask.

---

## Agent instructions (paste into chat or follow as operator)

1. **Input:** raw Telegram copy-paste (may lack speaker labels; may truncate first characters).
2. **Output path:** `docs/analysis/tg-interview-transcripts/req15-tg-interview-dialogue-YYYY-MM-DD-<slug>.md`  
   Prefer a short topic slug from the draft title/place (e.g. `pille`).
3. **Do not invent** missing turns. If a line is truncated (e.g. `...сторию`), restore only when obvious from context/screenshot; note the restore in Meta.
4. **Speaker attribution** (apply in order):
   - Short commands / confirmations / drafts the human pastes → **User**
   - Intake questions, checklists, validation reports, ET/EN packs, refusals to stash/redirect → **Bot**
   - Prior-bot wording that appears **inside** a user paste (e.g. «Верно ли, что…» at end of copied draft) → keep under **User** as pasted
5. **Structure of the `.md`:**
   - Meta: date, source = operator TG paste, context, honesty (labels from paste structure, not server logs)
   - Link method to `analysis.mdc`
   - Ordered `### User` / `### Bot` blocks with verbatim text in fenced code blocks
6. **Out of scope for this prompt:** changing instructions/code; inventing stash PASS; rewriting bot replies «how they should have looked».
7. **Honesty:** server logs usually lack message bodies — do not claim log reconstruction if the source was paste.

---

## Minimal template

```markdown
# REQ15 TG interview dialogue — YYYY-MM-DD (<slug>)

**Role:** full transcript extract only — no process analysis.
**Method:** [`.cursor/rules/analysis.mdc`](../../../.cursor/rules/analysis.mdc)
**Source:** operator Telegram copy-paste (YYYY-MM-DD)
**Context:** …
**Honesty:** speaker labels from paste turn structure (User ↔ Bot), not from server logs.

---

## Transcript

### User

\`\`\`
…
\`\`\`

### Bot

\`\`\`
…
\`\`\`
```

---

## Reference example

[`req15-tg-interview-dialogue-2026-11-05-pille.md`](./req15-tg-interview-dialogue-2026-11-05-pille.md)
