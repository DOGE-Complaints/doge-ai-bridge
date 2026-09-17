"""STORY-AIBRIDGE-34 — UC-01…10 product-journey E2E (E2EHarness; no live Telegram/Railway)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest

from aibridge.confirm_fsm import SessionState
from aibridge.gateway import GatewayOutcome, RawHttpResponse, STASH_REPLY
from story13_e2e_helpers import (
    ROOT,
    action_body,
    assert_channel_error_conforms,
    assert_channel_success_conforms,
    build_e2e_harness,
    fc_openai_payload,
    followup_openai_payload,
    good_tool_args,
    pg_available,
    rebuild_app_same_pg,
    text_openai_payload,
    turn_body,
)

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

pytestmark = pytest.mark.skipif(
    not pg_available(),
    reason="disposable Postgres (.pgdata-test) not running — ./scripts/start-disposable-pg.sh",
)

STORY = "STORY-AIBRIDGE-34-qa-product-journey-scenarios"
PKG_FIXTURES = (
    _TESTS_ROOT.parent
    / "docs"
    / "tasks"
    / "backlog-stories"
    / "qa-inbound-outbound-data-flow"
    / "fixtures"
)


def _tok(actions: list[dict[str, Any]], *, style: str) -> str:
    return next(a["token"] for a in actions if a["style"] == style)


def _raw_from_gateway(name: str) -> RawHttpResponse:
    env = load_fixture("gateway", name)
    body = json.dumps(env["payload"]["body"]).encode()
    return RawHttpResponse(status_code=int(env["payload"]["status_code"]), body=body)


def _hash(path: Path) -> str:
    import hashlib

    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_uc_fixture_packs_promoted_hash_eq() -> None:
    idx = load_fixture("meta", "uc-journey-index")
    assert STORY in idx["story_keys"]
    assert set(idx["matrix_ids"]) == {f"UC-{i:02d}" for i in range(1, 11)}
    for pack in idx["payload"]["packs"]:
        rel = Path(pack["path"])
        cluster, name = rel.parts[0], rel.stem
        copy = _TESTS_ROOT / "fixtures" / cluster / f"{name}.json"
        pkg = PKG_FIXTURES / f"{name}.json"
        assert pkg.is_file(), pkg
        assert copy.is_file(), copy
        assert _hash(pkg) == _hash(copy)
        env = load_fixture(cluster, name)
        assert pack["matrix_id"] in env["matrix_ids"]
        assert STORY in env["story_keys"]
        if pack.get("characterization"):
            assert "characterization" in env["notes"].lower() or env.get("characterization") is True


def test_uc_01_normal_interview_dry_run() -> None:
    spy = load_fixture("spies", "uc-01-normal-dry-run")
    assert "UC-01" in spy["matrix_ids"]
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Clarify civic observation?"),
            text_openai_payload("Looks right / Edit / Cancel"),
            fc_openai_payload(call_id="call_uc01"),
            followup_openai_payload("Dry-run follow-up."),
        ],
        gateway_scripted=[],
        dry_run_gateway=True,
    )
    uid, cid = "3401", "-1003401"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc01-0", text="Яма на дороге", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r0.status_code == 200
    assert_channel_success_conforms(r0.json())
    labels = {a["label"] for a in r0.json()["actions"]}
    assert {"Looks right", "Edit", "Cancel"} <= labels
    old_edit = _tok(r0.json()["actions"], style="default")
    sess = h.guard.get_or_create_session(user_id=uid, chat_id=cid)
    rev0 = sess.revision

    r_edit = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="uc01-edit", token=old_edit, user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r_edit.status_code == 200
    assert r_edit.json()["state"] == SessionState.INTERVIEWING.value
    sess_after_edit = h.guard.get_or_create_session(user_id=uid, chat_id=cid)
    assert sess_after_edit.session_id == sess.session_id
    # G-03: strict revision change after Edit (no tautology)
    assert sess_after_edit.revision > rev0
    assert expect.get("revision_increases_after_edit") is True
    # Old interpretation tokens invalid after Edit
    r_stale = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc01-stale",
            token=_tok(r0.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="stale",
        ),
        headers=h.auth_header,
    )
    assert r_stale.status_code in (404, 409)

    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc01-1", text="Яма у перекрёстка X", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r1.status_code == 200
    looks = _tok(r1.json()["actions"], style="success")
    h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="uc01-lr", token=looks, user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    r_fc = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc01-fc", text="stash", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r_fc.status_code == 200
    assert r_fc.json()["state"] == SessionState.AWAITING_SEND_CONFIRM.value
    send = _tok(r_fc.json()["actions"], style="primary")
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc01-send", token=send, user_id=uid, chat_id=cid, callback_query_id="s1"
        ),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    body = r_s.json()
    assert_channel_success_conforms(body)
    assert body["outcome"] == expect["outcome"]
    assert len(h.transport.calls) == expect["gateway_call_count"]
    assert len(h.openai.calls) >= expect["openai_min_calls"]
    text = (body.get("reply_text") or "").lower()
    if expect.get("must_mention_not_sent"):
        assert "not sent" in text or "dry-run" in text or "dry run" in text
    for needle in expect.get("forbid_substrings", []):
        assert needle.lower() not in text
    sess2 = h.guard.get_or_create_session(user_id=uid, chat_id=cid)
    assert sess2.session_id == sess.session_id


def test_uc_02_normal_live_stash() -> None:
    spy = load_fixture("spies", "uc-02-normal-live-stash")
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_uc02"),
            followup_openai_payload("Draft noted — not published."),
        ],
        gateway_scripted=[_raw_from_gateway("stashed-201")],
        dry_run_gateway=False,
    )
    uid, cid = "3402", "-1003402"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc02-0", text="hi", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc02-lr",
            token=_tok(r0.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
        ),
        headers=h.auth_header,
    )
    r_fc = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc02-fc", text="go", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc02-send",
            token=_tok(r_fc.json()["actions"], style="primary"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="s2",
        ),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    body = r_s.json()
    assert body["outcome"] == expect["outcome"]
    assert body["state"] == expect["final_state"]
    assert body["draft_id"] == expect["draft_id"]
    assert body["continuation_url"]
    assert len(h.transport.calls) == expect["gateway_call_count"]
    assert "not a published" in (body.get("reply_text") or "").lower() or body[
        "reply_text"
    ] == STASH_REPLY


def test_uc_03_cancel_first_confirmation() -> None:
    spy = load_fixture("spies", "uc-03-cancel-first-confirm")
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("Need confirm")],
        dry_run_gateway=True,
    )
    uid, cid = "3403", "-1003403"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc03-0", text="start", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    cancel = _tok(r0.json()["actions"], style="danger")
    r_c = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="uc03-c", token=cancel, user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r_c.status_code == 200
    assert r_c.json()["state"] == expect["final_state"]
    assert len(h.transport.calls) == expect["gateway_call_count"]
    assert len(h.openai.calls) <= expect["openai_calls_max"]
    # Pending tokens invalid
    r_stale = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc03-stale",
            token=_tok(r0.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="x",
        ),
        headers=h.auth_header,
    )
    assert r_stale.status_code in (404, 409)
    # G-02 / LIFE-009: wire fixture flag; post-cancel /turns capture-first (no product invent)
    assert expect.get("life009_followup") is True
    life = load_fixture("spies", "life-after-cancelled")
    assert "LIFE-009" in life["matrix_ids"]
    assert life["payload"]["prior_state"] == SessionState.CANCELLED.value
    assert life["payload"].get("capture") is True
    openai_before = len(h.openai.calls)
    r_life = h.client.post(
        "/v1/channel/turns",
        json=turn_body(
            event_id="uc03-life009",
            text="new message after cancel",
            user_id=uid,
            chat_id=cid,
        ),
        headers=h.auth_header,
    )
    assert r_life.status_code == 200
    body_life = r_life.json()
    again = h.guard.get_or_create_session(user_id=uid, chat_id=cid)
    captured = {
        "state": body_life["state"],
        "actions_empty": body_life["actions"] == [],
        "same_session_id": body_life["session_id"] == again.session_id,
        "openai_calls_delta": len(h.openai.calls) - openai_before,
    }
    # Characterization: cancelled terminal session; empty actions; same session (LIFE-009)
    assert captured["state"] == SessionState.CANCELLED.value
    assert captured["actions_empty"] is True
    assert captured["same_session_id"] is True
    assert again.state.value == SessionState.CANCELLED.value
    assert captured["openai_calls_delta"] >= 0  # capture; do not invent resume invent


def test_uc_04_cancel_before_send() -> None:
    spy = load_fixture("spies", "uc-04-cancel-before-send")
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_uc04"),
        ],
        gateway_scripted=[_raw_from_gateway("stashed-201")],
        dry_run_gateway=False,
    )
    uid, cid = "3404", "-1003404"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc04-0", text="hi", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc04-lr",
            token=_tok(r0.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
        ),
        headers=h.auth_header,
    )
    r_fc = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc04-fc", text="go", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    send_tok = _tok(r_fc.json()["actions"], style="primary")
    cancel = _tok(r_fc.json()["actions"], style="danger")
    r_c = h.client.post(
        "/v1/channel/actions",
        json=action_body(event_id="uc04-c", token=cancel, user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r_c.status_code == 200
    assert r_c.json()["state"] == expect["final_state"]
    assert r_c.json().get("continuation_url") is None
    assert len(h.transport.calls) == expect["gateway_call_count"]
    r_send = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc04-send-stale",
            token=send_tok,
            user_id=uid,
            chat_id=cid,
            callback_query_id="late",
        ),
        headers=h.auth_header,
    )
    assert r_send.status_code in (404, 409)


def test_uc_05_group_ownership_attack() -> None:
    spy = load_fixture("spies", "uc-05-group-ownership-attack")
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("Need confirm")],
        dry_run_gateway=True,
    )
    owner_u, owner_c = "501", "-10034"
    attacker_u = "999"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc05-0", text="group story", user_id=owner_u, chat_id=owner_c),
        headers=h.auth_header,
    )
    owner_tok = _tok(r0.json()["actions"], style="success")
    r_atk = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc05-atk",
            token=owner_tok,
            user_id=attacker_u,
            chat_id=owner_c,
            callback_query_id="atk",
        ),
        headers=h.auth_header,
    )
    assert r_atk.status_code == expect["http_status"]
    err = r_atk.json()
    assert_channel_error_conforms(err)
    assert err["error"]["code"] == expect["error_code"]
    assert len(h.transport.calls) == expect["gateway_call_count"]
    # Owner token still consumable by owner
    r_ok = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc05-owner",
            token=owner_tok,
            user_id=owner_u,
            chat_id=owner_c,
            callback_query_id="own",
        ),
        headers=h.auth_header,
    )
    assert r_ok.status_code == 200


def test_uc_06_telegram_retry_storm_characterization() -> None:
    spy = load_fixture("spies", "uc-06-telegram-retry-storm")
    assert spy.get("characterization") is True or "characterization" in spy["notes"]
    expect = spy["payload"]["expect"]
    retries = int(spy["payload"]["retry_count"])
    h = build_e2e_harness(
        openai_scripted=[text_openai_payload("Stable reply")],
        dry_run_gateway=True,
    )
    uid, cid = "3406", "-1003406"
    bodies = []
    for i in range(retries):
        r = h.client.post(
            "/v1/channel/turns",
            json=turn_body(event_id="uc06-same", text="retry storm", user_id=uid, chat_id=cid),
            headers=h.auth_header,
        )
        assert r.status_code == 200
        bodies.append(r.json())
    assert len(h.openai.calls) == expect["openai_call_count"]
    assert len(h.transport.calls) == expect["gateway_call_count"]
    if expect["deterministic_replay"]:
        assert all(b["reply_text"] == bodies[0]["reply_text"] for b in bodies)
        assert all(b["request_id"] == bodies[0]["request_id"] for b in bodies)


def test_uc_07_ambiguous_gateway_timeout() -> None:
    spy = load_fixture("spies", "uc-07-ambiguous-gateway-timeout")
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_uc07"),
        ],
        gateway_scripted=[],
        dry_run_gateway=False,
    )
    h.transport.raise_on_call = TimeoutError("read timeout")
    uid, cid = "3407", "-1003407"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc07-0", text="hi", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc07-lr",
            token=_tok(r0.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
        ),
        headers=h.auth_header,
    )
    r_fc = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc07-fc", text="go", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    send = _tok(r_fc.json()["actions"], style="primary")
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc07-send", token=send, user_id=uid, chat_id=cid, callback_query_id="t7"
        ),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    body = r_s.json()
    assert body["outcome"] == expect["outcome"]
    assert body["state"] == SessionState.UNKNOWN_OUTCOME.value
    assert len(h.transport.calls) == expect["gateway_call_count"]
    # No automatic second gateway attempt
    assert len(h.transport.calls) == 1
    # Re-Send with consumed/sibling tokens blocked
    r_retry = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc07-retry",
            token=send,
            user_id=uid,
            chat_id=cid,
            callback_query_id="t7b",
        ),
        headers=h.auth_header,
    )
    assert r_retry.status_code in (404, 409)
    assert len(h.transport.calls) == 1
    # G-04: restart preserves ambiguity; no auto gateway retry
    sess = h.guard.get_or_create_session(user_id=uid, chat_id=cid)
    assert sess.state is SessionState.UNKNOWN_OUTCOME
    h2 = rebuild_app_same_pg(h, openai_scripted=[], gateway_scripted=[], dry_run_gateway=False)
    assert h2.transport.calls == []
    sess2 = h2.guard.get_or_create_session(user_id=uid, chat_id=cid)
    assert sess2.session_id == sess.session_id
    assert sess2.state is SessionState.UNKNOWN_OUTCOME
    assert h2.guard.send_blocked_for_revision(sess2) is True
    assert len(h2.transport.calls) == 0
    # Operator runbook required: documented unknown_outcome handling (assert path exists)
    runbook = ROOT / "docs" / "runtime-docs" / "01-api.md"
    assert runbook.is_file()
    assert "unknown_outcome" in runbook.read_text(encoding="utf-8")
    assert expect.get("restart_preserves_ambiguity") is True or spy["payload"].get(
        "expect", {}
    ).get("resend_blocked") is True


def test_uc_08_geo_scope_mismatch() -> None:
    spy = load_fixture("spies", "uc-08-geo-scope-mismatch")
    expect = spy["payload"]["expect"]
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("Need confirm"),
            fc_openai_payload(call_id="call_uc08"),
            followup_openai_payload("Geo mismatch follow-up."),
        ],
        gateway_scripted=[_raw_from_gateway("gw-422")],
        dry_run_gateway=False,
    )
    uid, cid = "3408", "-1003408"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc08-0", text="hi", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc08-lr",
            token=_tok(r0.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
        ),
        headers=h.auth_header,
    )
    r_fc = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc08-fc", text="go", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc08-send",
            token=_tok(r_fc.json()["actions"], style="primary"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="g8",
        ),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    body = r_s.json()
    assert body["outcome"] == expect["outcome"]
    assert body["draft_id"] is None
    assert body["continuation_url"] is None
    assert body["state"] != SessionState.STASHED.value
    assert len(h.transport.calls) == expect["gateway_call_count"]


def test_uc_09_unsupported_telegram_characterization() -> None:
    """Characterization: adapter seam — must not invent empty /turns (capture-first)."""
    env = load_fixture("n8n", "uc-09-unsupported-telegram-content")
    assert env.get("characterization") is True or "characterization" in env["notes"]
    expect = env["payload"]["expect"]
    mapped = load_fixture("n8n", "map-unsupported-media")
    tg = load_fixture("telegram", "message-photo-no-text")
    assert mapped["payload"]["must_not_build_turns"] is expect["must_not_build_turns"]
    assert mapped["payload"]["outbound_telegram"]["unsupported_prompt"] is expect[
        "unsupported_prompt"
    ]
    assert "photo" in tg["payload"]["message"]
    assert not tg["payload"]["message"].get("text")
    # Capture-first: aibridge v1 is text-only — no product invent of transcription path
    assert expect["aibridge_text_only_v1"] is True
    assert env["payload"]["refs"]["inbound_telegram_fixture"].endswith("message-photo-no-text")


def test_uc_10_multilingual_story() -> None:
    spy = load_fixture("spies", "uc-10-multilingual-story")
    expect = spy["payload"]["expect"]
    msgs = spy["payload"]["messages"]
    i18n_args = {
        "narrative": {
            "et": msgs["et_place"],
            "ru": msgs["ru"],
            "en": msgs["en"],
            "note": "multilingual",
        },
        "schema_binding": {"structured_payload": {"title": "pothole-i18n"}},
    }
    h = build_e2e_harness(
        openai_scripted=[
            text_openai_payload("RU clarify"),
            text_openai_payload("ET place noted"),
            text_openai_payload("EN summary noted"),
            fc_openai_payload(call_id="call_uc10", args=i18n_args),
            followup_openai_payload("Draft noted — not published."),
        ],
        gateway_scripted=[_raw_from_gateway("stashed-201")],
        dry_run_gateway=False,
    )
    uid, cid = "3410", "-1003410"
    r0 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc10-ru", text=msgs["ru"], user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r0.status_code == 200
    # Edit between language turns so interviewing continues (awaiting confirm blocks plain turns)
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc10-ed1",
            token=_tok(r0.json()["actions"], style="default"),
            user_id=uid,
            chat_id=cid,
        ),
        headers=h.auth_header,
    )
    r1 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc10-et", text=msgs["et_place"], user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r1.status_code == 200
    # language_code not on channel body — policy not blindly from Telegram
    assert "language_code" not in turn_body(event_id="x", text="y")
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc10-ed2",
            token=_tok(r1.json()["actions"], style="default"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="ed2",
        ),
        headers=h.auth_header,
    )
    r2 = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc10-en", text=msgs["en"], user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    assert r2.status_code == 200
    h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc10-lr",
            token=_tok(r2.json()["actions"], style="success"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="lr10",
        ),
        headers=h.auth_header,
    )
    r_fc = h.client.post(
        "/v1/channel/turns",
        json=turn_body(event_id="uc10-fc", text="finalize", user_id=uid, chat_id=cid),
        headers=h.auth_header,
    )
    r_s = h.client.post(
        "/v1/channel/actions",
        json=action_body(
            event_id="uc10-send",
            token=_tok(r_fc.json()["actions"], style="primary"),
            user_id=uid,
            chat_id=cid,
            callback_query_id="i10",
        ),
        headers=h.auth_header,
    )
    assert r_s.status_code == 200
    body = r_s.json()
    assert body["outcome"] == expect["outcome"]
    assert len(h.transport.calls) == expect["gateway_call_count"]
    gw_body = h.transport.calls[0]["json_body"]
    # Frozen tool args land in gateway narrative/schema — require et/ru/en keys present
    blob = json.dumps(gw_body, ensure_ascii=False)
    for lang in expect["narrative_langs"]:
        assert f'"{lang}"' in blob or msgs.get(lang) in blob or msgs.get(
            {"et": "et_place"}.get(lang, lang), ""
        ) in blob
    # Raw user texts preserved in OpenAI call inputs
    all_input = json.dumps(h.openai.calls, ensure_ascii=False)
    assert msgs["ru"] in all_input
    assert msgs["et_place"] in all_input
    assert msgs["en"] in all_input
