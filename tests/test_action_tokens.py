"""t03 — opaque action token mint + hash store."""

from __future__ import annotations

from aibridge.action_tokens import (
    ActionTokenStore,
    TokenActionKind,
    hash_token,
    mint_opaque_token,
)


def test_mint_token_max_64_utf8_bytes() -> None:
    for _ in range(20):
        raw = mint_opaque_token()
        assert 1 <= len(raw.encode("utf-8")) <= 64


def test_store_hash_not_raw() -> None:
    store = ActionTokenStore()
    raw, rec = store.issue(
        action=TokenActionKind.CONFIRM_SEND,
        session_id="s1",
        user_id="1",
        chat_id="2",
        deployment_id="local",
        revision=1,
        expected_state="awaiting_send_confirm",
    )
    assert raw not in store._by_hash  # type: ignore[attr-defined]
    assert hash_token(raw) in store._by_hash  # type: ignore[attr-defined]
    snap = store.bind_snapshot(raw)
    assert snap["raw_stored"] is False
    assert snap["token_hash"] == rec.token_hash
    assert snap["revision"] == 1
    assert snap["action"] == "confirm_send"
    assert snap["nonce"] == rec.nonce
    assert len(rec.nonce) >= 16
    assert snap["draft_hash"] is None


def test_issue_binds_draft_hash_and_unique_nonce() -> None:
    store = ActionTokenStore()
    dh = "abc" * 21 + "d"  # 64-char stand-in
    raw1, rec1 = store.issue(
        action=TokenActionKind.CONFIRM_SEND,
        session_id="s1",
        user_id="1",
        chat_id="2",
        deployment_id="local",
        revision=2,
        expected_state="awaiting_send_confirm",
        draft_hash=dh,
    )
    raw2, rec2 = store.issue(
        action=TokenActionKind.EDIT,
        session_id="s1",
        user_id="1",
        chat_id="2",
        deployment_id="local",
        revision=2,
        expected_state="awaiting_send_confirm",
        draft_hash=dh,
    )
    assert rec1.draft_hash == dh
    assert rec2.draft_hash == dh
    assert rec1.nonce != rec2.nonce
    snap = store.bind_snapshot(raw1)
    assert snap["draft_hash"] == dh
    assert snap["nonce"] == rec1.nonce
    assert "raw" not in snap
    assert raw1 != raw2
