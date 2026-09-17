"""STORY-AIBRIDGE-25 — n8n thin-adapter Telegram mapping (no live Telegram).

Fixture-driven asserts mirroring docs/ops/n8n-channel-workflow/README.md §2–§3.
ADR-Q5: mapping via fixtures only; never call live Bot API / invent Railway SUCCESS.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import pytest

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

STORY = "STORY-AIBRIDGE-25-qa-n8n-telegram-mapping"
N8N_IDS = {f"N8N-{i:03d}" for i in range(1, 19)}
PKG_FIXTURES = (
    _TESTS_ROOT.parents[0]
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)


def _fid_to_name(fixture_id: str) -> tuple[str, str]:
    cluster, name = fixture_id.split(".", 1)
    return cluster, name


def telegram_event_id(update_id: int | str) -> str:
    return str(update_id)


def map_telegram_message_to_turns(update: dict[str, Any]) -> dict[str, Any]:
    """Mirror n8n README §3 turns mapping (thin adapter only)."""
    msg = update["message"]
    body: dict[str, Any] = {
        "channel": "telegram",
        "event_id": telegram_event_id(update["update_id"]),
        "principal": {
            "user_id": str(msg["from"]["id"]),
            "chat_id": str(msg["chat"]["id"]),
        },
        "message": {
            "message_id": str(msg["message_id"]),
            "text": msg.get("text") or "",
        },
    }
    lang = msg.get("from", {}).get("language_code") or msg.get("language_code")
    if lang:
        body["message"]["language_code"] = lang
    return body


def map_telegram_callback_to_actions(update: dict[str, Any]) -> dict[str, Any]:
    cq = update["callback_query"]
    return {
        "channel": "telegram",
        "event_id": telegram_event_id(update["update_id"]),
        "callback_query_id": str(cq["id"]),
        "principal": {
            "user_id": str(cq["from"]["id"]),
            "chat_id": str(cq["message"]["chat"]["id"]),
        },
        "action_token": cq["data"],
    }


def render_outbound_keyboard(actions: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Map aibridge actions[] → Telegram inline keyboard callback_data=token."""
    return [{"label": a["label"], "callback_data": a["token"]} for a in actions]


def should_present_continuation(outcome: str | None) -> bool:
    return outcome == "stashed"


def simulate_post_ack_failure_timeline(steps: list[dict[str, Any]]) -> list[str]:
    """Fixture-driven adapter replay: ack must complete before aibridge fail (no live TG)."""
    completed: list[str] = []
    ack_done = False
    for step in sorted(steps, key=lambda s: int(s["seq"])):
        event = step["event"]
        if event == "answerCallbackQuery":
            assert step.get("status") == "ok"
            completed.append(event)
            ack_done = True
            continue
        if event == "aibridge_unavailable":
            assert ack_done, "N8N-014: answerCallbackQuery must complete before aibridge fail"
            assert step.get("after_ack") is True
            completed.append(event)
            continue
        if event == "SendOrEditMessage_resident_safe_error":
            assert ack_done, "resident-safe error must follow prompt ack"
            completed.append(event)
            continue
        completed.append(event)
    return completed


def _load_by_id(fixture_id: str) -> dict[str, Any]:
    cluster, name = _fid_to_name(fixture_id)
    return load_fixture(cluster, name)


def test_traceability_story_covers_all_n8n_ids() -> None:
    n8n_names = [
        "map-private-text",
        "map-start-command",
        "map-unicode-ru",
        "map-unicode-et",
        "map-mixed-lang",
        "map-emoji",
        "map-group-user-a",
        "map-group-user-b",
        "map-edited-message",
        "map-unsupported-media",
        "map-media-caption",
        "map-non-workflow-update",
        "callback-ack-before-actions",
        "map-actions-empty",
        "map-actions-three",
        "map-outcome-stashed",
        "map-outcome-non-stashed-no-link",
    ]
    seen: set[str] = set()
    for name in n8n_names:
        env = load_fixture("n8n", name)
        assert STORY in env["story_keys"]
        seen.update(i for i in env["matrix_ids"] if i.startswith("N8N-"))
    assert N8N_IDS == seen


def test_seed_originals_intact_hash_eq() -> None:
    import hashlib

    pairs = [
        ("message-private-ru-pothole.json", "telegram"),
        ("callback-ack-before-actions.json", "n8n"),
    ]
    for fname, cluster in pairs:
        original = PKG_FIXTURES / fname
        copy = _TESTS_ROOT / "fixtures" / cluster / fname
        assert original.is_file() and copy.is_file()
        assert hashlib.sha256(original.read_bytes()).digest() == hashlib.sha256(
            copy.read_bytes()
        ).digest()


@pytest.mark.parametrize(
    "n8n_name",
    [
        "map-private-text",
        "map-start-command",
        "map-unicode-ru",
        "map-unicode-et",
        "map-mixed-lang",
        "map-emoji",
        "map-group-user-a",
        "map-group-user-b",
    ],
)
def test_message_flow_maps_to_turns(n8n_name: str) -> None:
    case = load_fixture("n8n", n8n_name)
    payload = case["payload"]
    assert payload["flow"] == "message"
    tg = _load_by_id(payload["inbound_telegram_fixture_id"])
    update = tg["payload"]
    mapped = map_telegram_message_to_turns(update)

    if payload.get("expected_channel_fixture_id"):
        ch = _load_by_id(payload["expected_channel_fixture_id"])
        assert mapped == ch["payload"]["body"]

    if payload.get("expected_turns_text") is not None:
        assert mapped["message"]["text"] == payload["expected_turns_text"]

    if payload.get("preserve_unicode") or payload.get("text_must_equal_source"):
        assert mapped["message"]["text"] == update["message"]["text"]

    if payload.get("hint_must_not_override_text"):
        # language_code may be present but must not rewrite message.text
        assert mapped["message"]["text"] == update["message"]["text"]

    if payload.get("expect_principal"):
        assert mapped["principal"] == payload["expect_principal"]

    if payload.get("session_distinct_from_fixture_id"):
        other = _load_by_id(payload["session_distinct_from_fixture_id"])
        other_mapped = map_telegram_message_to_turns(other["payload"])
        assert mapped["principal"] != other_mapped["principal"]

    assert payload["ack_order"][0] == "POST /v1/channel/turns"
    assert "answerCallbackQuery" not in payload["ack_order"]

    if n8n_name == "map-private-text":
        # G-02 / N8N-001: one reply outbound contract
        assert payload["outbound_telegram"].get("one_reply") is True
        assert payload["ack_order"].count("SendOrEditMessage") == 1


def test_callback_ack_order_before_actions() -> None:
    case = load_fixture("n8n", "callback-ack-before-actions")
    payload = case["payload"]
    assert payload["ack_order"] == [
        "answerCallbackQuery",
        "POST /v1/channel/actions",
        "SendOrEditMessage",
    ]
    assert payload["outbound_telegram"]["must_ack_callback_before_actions"] is True
    assert payload["ack_order"].index("answerCallbackQuery") < payload["ack_order"].index(
        "POST /v1/channel/actions"
    )

    tg = _load_by_id(payload["inbound_telegram_fixture_id"])
    mapped = map_telegram_callback_to_actions(tg["payload"])
    ch = _load_by_id(payload["expected_channel_fixture_id"])
    assert mapped == ch["payload"]["body"]

    # N8N-014: slow/unavailable after ack — fixture-driven ordered timeline (G-01)
    slow = payload["outbound_telegram"]["aibridge_slow_or_unavailable_after_ack"]
    assert slow["callback_still_acknowledged_promptly"] is True
    assert slow["later_resident_safe_error_via"] == "SendOrEditMessage"
    timeline = payload["failure_timeline"]
    completed = simulate_post_ack_failure_timeline(timeline)
    assert completed[0] == "answerCallbackQuery"
    assert "aibridge_unavailable" in completed
    assert completed.index("answerCallbackQuery") < completed.index("aibridge_unavailable")
    assert completed[-1] == "SendOrEditMessage_resident_safe_error"
    assert completed.index("answerCallbackQuery") == 0


def test_edited_message_characterization_capture_first() -> None:
    case = load_fixture("n8n", "map-edited-message")
    assert "characterization" in case["notes"].lower() or case["payload"].get("characterization")
    payload = case["payload"]
    assert payload["must_not_map_as_ordinary_message"] is True
    assert payload["workflow_supports_edited"] is False
    # Capture-first: do not invent ordinary /turns mapping for undocumented edited path
    assert payload["captured_behavior"] == "skip_ordinary_turns_when_undocumented"
    tg = _load_by_id(payload["inbound_telegram_fixture_id"])
    assert "edited_message" in tg["payload"]
    assert "message" not in tg["payload"]


def test_unsupported_media_no_turns() -> None:
    case = load_fixture("n8n", "map-unsupported-media")
    payload = case["payload"]
    assert payload["must_not_build_turns"] is True
    assert payload["outbound_telegram"]["unsupported_prompt"] is True
    tg = _load_by_id(payload["inbound_telegram_fixture_id"])
    msg = tg["payload"]["message"]
    assert "text" not in msg
    assert "photo" in msg


def test_media_caption_characterization_capture_first() -> None:
    case = load_fixture("n8n", "map-media-caption")
    assert "characterization" in case["notes"].lower() or case["payload"].get("characterization")
    payload = case["payload"]
    assert payload["workflow_documents_caption_as_text"] is False
    assert payload["captured_behavior"] == "do_not_invent_caption_as_text"
    tg = _load_by_id(payload["inbound_telegram_fixture_id"])
    assert "caption" in tg["payload"]["message"]


def test_non_workflow_update_skipped() -> None:
    case = load_fixture("n8n", "map-non-workflow-update")
    payload = case["payload"]
    assert payload["must_not_enter_workflow"] is True
    tg = _load_by_id(payload["inbound_telegram_fixture_id"])
    assert "channel_post" in tg["payload"]
    assert "message" not in tg["payload"]


def test_actions_empty_no_keyboard() -> None:
    case = load_fixture("n8n", "map-actions-empty")
    actions = case["payload"]["aibridge_response"]["actions"]
    assert actions == []
    assert render_outbound_keyboard(actions) == []
    assert case["payload"]["outbound_telegram"]["inline_keyboard_expected"] is False


def test_actions_three_order_and_tokens() -> None:
    case = load_fixture("n8n", "map-actions-three")
    out = case["payload"]["outbound_telegram"]
    actions = case["payload"]["aibridge_response"]["actions"]
    kb = render_outbound_keyboard(actions)
    assert [b["label"] for b in kb] == out["keyboard_labels_in_order"]
    assert [b["callback_data"] for b in kb] == out["keyboard_tokens_unchanged"]


def test_outcome_stashed_continuation_claim_published_forbidden() -> None:
    case = load_fixture("n8n", "map-outcome-stashed")
    resp = case["payload"]["aibridge_response"]
    out = case["payload"]["outbound_telegram"]
    assert resp["outcome"] == "stashed"
    assert should_present_continuation(resp["outcome"]) is True
    assert out["render_continuation_link"] is True
    assert out["claim_published_forbidden"] is True
    # Adapter must not claim publication when only stashed continuation exists
    assert "published" not in (resp.get("reply_text") or "").lower()


def test_non_stashed_must_not_present_accidental_link() -> None:
    case = load_fixture("n8n", "map-outcome-non-stashed-no-link")
    resp = case["payload"]["aibridge_response"]
    out = case["payload"]["outbound_telegram"]
    assert resp["outcome"] != "stashed"
    assert should_present_continuation(resp["outcome"]) is False
    assert out["must_not_present_continuation_link"] is True
    # Producer inconsistency: accidental URL present but adapter must suppress
    assert resp.get("continuation_url")
    assert should_present_continuation(resp["outcome"]) is False
