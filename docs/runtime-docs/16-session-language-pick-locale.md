# Session language pick + ConfirmSession.locale (STORY-69 / EPIC-12)

Thin runtime note — **Adapt** ConfirmSession SSOT. Detail SSOT:

- Arch: [`../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md`](../architecture/req15-tg-channel-interviewer-ux/02-session-language-locale.md)

## What landed (P3 · 2026-11-06T12:32:14Z)

| Concern | Code | Must |
|---------|------|------|
| Unclear detector | `locale_policy.is_unclear_language` | digits/`888`/opaque → pick; clear-text may skip |
| Locale SSOT | `ConfirmSession.locale ∈ {et,ru,en}` | **Not** semantic_state facts |
| Persist | `state_json` via `_persist_session` / PG store | memory + PG round-trip |
| Pick mint | `offer_language_pick` | Eesti / Русский / **English 🇺🇸** |
| Consume | `PICK_LOCALE_*` | bind locale; never stash / gateway |
| Gate | `channel._maybe_language_pick_gate` | before engine when unbound + unclear |
| Apply | `locale_prompt_prefix` on engine text | thin Adapt — not full i18n catalog |

## Honesty

- Code/harness Done ≠ invent Railway / live TG SUCCESS.
- STORY-68 seam/Send OOS this story.
- No invent full UI string catalog.

## Verify harness

`tests/test_story_69_session_language_pick.py`
