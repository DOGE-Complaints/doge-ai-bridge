# Implement — req15-roles-interview-ux-prose-accum-batch

**Status:** **Superseded** (2026-11-06) — do **not** execute.  
**Successor:** GPT UI package [`req15-tg-interviewer-roles-ux`](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/INDEX.md) · [STORY-GPT-ROL-05](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-05-channel-interview-stage-proactivity.md) · [STORY-GPT-ROL-06](../../GPT-UI/docs/tasks/backlog-stories/req15-tg-interviewer-roles-ux/STORY-GPT-ROL-06-channel-interview-surface-readability.md) · [triage](./req15-tg-interviewer-ux-gap-triage-2026-11-06.md)

**Project:** GPT UI (`instructions-roles`) · plan home: DOGEstonia root analysis  
**Execute in:** monorepo / GPT UI focus chat  
**Class:** ~~accumulative instruction-prose batch~~ → **Superseded by STORY**  
**Triage:** [`req15-tg-interviewer-ux-gap-triage-2026-11-06.md`](./req15-tg-interviewer-ux-gap-triage-2026-11-06.md)  
**Validate:** [`req15-roles-interview-ux-prose-accum-batch-validate.md`](./req15-roles-interview-ux-prose-accum-batch-validate.md) (also Superseded)  
**LAUNCH:** [`req15-roles-interview-ux-prose-accum-batch-LAUNCH.md`](./req15-roles-interview-ux-prose-accum-batch-LAUNCH.md) (also Superseded)  
**Evidence:** [`req15-tg-interviewer-ux-gap-pille-2026-11-06.md`](./req15-tg-interviewer-ux-gap-pille-2026-11-06.md) Goals 1/5/6 · [`req15-tg-interviewer-target-ux-2026-11-06.md`](./req15-tg-interviewer-target-ux-2026-11-06.md)  
**MODE:** ~~edit `GPT UI/instructions-roles/**` prose only~~ — use ROL-05/06 instead. [analysis.mdc](../../.cursor/rules/analysis.mdc).

## Todos

- [ ] proactive — Instruct roles to auto-advance stages (check → normalize → i18n) without requiring user «дальше / продолжай / проверяй» when enough data Present
- [ ] air — Prefer short paragraphs + blank lines; break dense bullet walls
- [ ] markers — Prefer light emoji / orange-ish Unicode bullets over heavy `**` star-bold; honesty: TG has no CSS orange
- [ ] no-vague-ui — Ban prose «используйте интерфейс» without naming in-chat actions or stating that server will offer Send confirm / URL after stash (do not invent HTTP)
- [ ] core-align — Ensure [`core.md`](../../GPT-UI/instructions-roles/core.md) still forbids model-owned stash/redirect; refine UX wording only

## Locks

- Server owns stash + SPA URL (REQ-11 / roles strip). Prose may say buttons/URL will appear — must not teach model to POST gateway.
- Languages in scope of volume: et/ru/en as already used by roles line.
- Touch set: `GPT UI/instructions-roles/` (and symlink `GPT-UI/` only if Present as same tree).

## Touch list (candidates)

- `GPT UI/instructions-roles/core.md`
- Role-specific files under `GPT UI/instructions-roles/` that drive interview / checker / normalizer citizen-facing copy
- Avoid rewriting schema-pack bodies

## OOS

- STORY-68/69 runtime actions; telegram logging LF; code in aibridge; archive Module1 model stash restore; commits unless asked.

## Prove

- Grep roles volume: no instruction to model-call gateway stash / invent redirect URL.
- Grep: no standalone «используйте интерфейс» without action/URL guidance.
- Spot-check: at least one role file shows spacing / marker guidance consistent with target UX §3 goals 5–6.
