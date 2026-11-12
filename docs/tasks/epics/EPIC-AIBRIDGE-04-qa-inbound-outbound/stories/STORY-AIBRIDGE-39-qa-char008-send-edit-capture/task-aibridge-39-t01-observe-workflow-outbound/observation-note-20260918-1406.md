# Observation note — CHAR-008 outbound Send/Edit (P3)

| Field | Value |
|-------|-------|
| **Date** | 2026-09-18T14:06:43Z |
| **Story** | STORY-AIBRIDGE-39-qa-char008-send-edit-capture |
| **Task** | t01 observe-workflow-outbound |
| **Result** | **Deferred** (capture-first · no invent) |

## Facts verified

| Claim | Fact |
|-------|------|
| Export path | `docs/ops/n8n-channel-workflow/exports/aibridge-telegram-channel-v1.json` — **ABSENT** |
| Pin pointer | `tests/fixtures/meta/n8n-wf-001-pin-pointer.json` · `status=deferred` (STORY-36) |
| Ops README §2 | Present — high-level `Send Message` / `Edit Message` after `/turns` and `/actions` |
| Per-state map from export | **Not available** — cannot invent `send_message` \| `edit_message` per response state without export |
| Retry dedupe from export | **Not available** — cannot invent n8n retry dedupe mechanism |

## Ops README §2 (source=`ops_readme_not_export` — not CHAR-008 capture)

High-level flow only (not a per-state characterization answer):

```text
message → HTTP POST /v1/channel/turns → Send Message (+ actions)
callback_query → answerCallbackQuery → POST /actions → Send/Edit Message
```

## Disposition

- Keep **visible** `defer_reason` until credential-stripped export is placed.
- Do **not** invent export body / live TG / Send-Edit policy.
- Downstream t02 writes defer capture envelope; t03 asserts honesty path.

## Depends

STORY-36 N8N-WF-001 pin deferred · same export path.
