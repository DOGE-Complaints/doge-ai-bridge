# L11-1 invalidation seam (STORY-57 / REQ-11)

Thin runtime note. Arch SSOT: [`../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md`](../architecture/req15-dual-confirm-handoff/02-l11-invalidation-seam.md).

## Named seam (Present)

| Symbol | Role |
|--------|------|
| `ConfirmationGuard.invalidate_send_permission()` | Clear send permission: invalidate tokens for revision, bump revision, clear `gateway_authorized` / frozen intent / draft / continuation |
| `ConfirmationGuard.apply_edit()` | Transition **C** enforce: FSM `EDIT` → then calls the same seam |

No second permission store · no new HTTP · no REQ-13 field taxonomy invent.

## AC-AIB-11-02 honesty

| Phase | Status |
|-------|--------|
| **Transition C** (EDIT/revision only while semantic state Absent) | **Pass** — harness + Present EDIT path |
| **Target A** (meaning-change invalidates without Telegram EDIT) | **Partial** — seam callable for future REQ-13; **not Done** until REQ-13 semantic state Present + meaning-change evidence |

Do **not** claim AC-AIB-11-02 target A **Done** in this wave.

## Verify

`tests/test_story_57_l11_invalidation_seam.py`

## Out of this note

Keep-pipe re-verify (56) · stub/live evidence (58) · REQ-13 state store implement.
