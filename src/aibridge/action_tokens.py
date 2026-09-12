"""Opaque action tokens — mint, hash store, consume (AIB-CONF-02/03)."""

from __future__ import annotations

import hashlib
import secrets
import time
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class TokenActionKind(StrEnum):
    CONFIRM_INTERPRETATION = "confirm_interpretation"
    CONFIRM_SEND = "confirm_send"
    EDIT = "edit"
    CANCEL = "cancel"


class TokenRecordState(StrEnum):
    PENDING = "pending"
    CONSUMED = "consumed"
    INVALIDATED = "invalidated"


class TokenError(Exception):
    """Base token failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class TokenNotFoundError(TokenError):
    def __init__(self) -> None:
        super().__init__("not_found", "Action token not found")


class TokenOwnershipError(TokenError):
    def __init__(self) -> None:
        super().__init__("forbidden", "Principal does not own this token")


class TokenConflictError(TokenError):
    def __init__(self, message: str = "Token expired, consumed, or invalidated") -> None:
        super().__init__("conflict", message)


def hash_token(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def mint_opaque_token(*, nbytes: int = 32) -> str:
    """URL-safe token ≤64 UTF-8 bytes (Telegram callback_data)."""
    # token_urlsafe(32) → ~43 chars; ensure hard cap.
    raw = secrets.token_urlsafe(nbytes)
    if len(raw.encode("utf-8")) > 64:
        raw = raw.encode("utf-8")[:64].decode("utf-8", errors="ignore")
    return raw


@dataclass
class TokenRecord:
    token_hash: str
    action: TokenActionKind
    session_id: str
    user_id: str
    chat_id: str
    deployment_id: str
    revision: int
    issued_at: float
    expires_at: float
    expected_state: str
    state: TokenRecordState = TokenRecordState.PENDING
    operation_id: str = "postStoryDraftStash"
    draft_hash: str | None = None
    nonce: str = ""


@dataclass
class ActionTokenStore:
    """In-process hash store — Postgres persistence later (AIB-DB)."""

    ttl_seconds: int = 15 * 60  # pilot TTL per arch §2
    _by_hash: dict[str, TokenRecord] = field(default_factory=dict)

    def issue(
        self,
        *,
        action: TokenActionKind,
        session_id: str,
        user_id: str,
        chat_id: str,
        deployment_id: str,
        revision: int,
        expected_state: str,
        draft_hash: str | None = None,
        nonce: str | None = None,
        now: float | None = None,
    ) -> tuple[str, TokenRecord]:
        raw = mint_opaque_token()
        assert len(raw.encode("utf-8")) <= 64
        th = hash_token(raw)
        ts = now if now is not None else time.time()
        rec = TokenRecord(
            token_hash=th,
            action=action,
            session_id=session_id,
            user_id=user_id,
            chat_id=chat_id,
            deployment_id=deployment_id,
            revision=revision,
            issued_at=ts,
            expires_at=ts + self.ttl_seconds,
            expected_state=expected_state,
            draft_hash=draft_hash,
            nonce=nonce if nonce is not None else secrets.token_hex(16),
        )
        self._by_hash[th] = rec
        return raw, rec

    def lookup(self, raw: str) -> TokenRecord:
        rec = self._by_hash.get(hash_token(raw))
        if rec is None:
            raise TokenNotFoundError()
        return rec

    def verify_for_consume(
        self,
        raw: str,
        *,
        user_id: str,
        chat_id: str,
        now: float | None = None,
    ) -> TokenRecord:
        rec = self.lookup(raw)
        if rec.user_id != user_id or rec.chat_id != chat_id:
            raise TokenOwnershipError()
        ts = now if now is not None else time.time()
        if rec.state is TokenRecordState.CONSUMED:
            raise TokenConflictError("Token already consumed")
        if rec.state is TokenRecordState.INVALIDATED:
            raise TokenConflictError("Token invalidated")
        if ts > rec.expires_at:
            raise TokenConflictError("Token expired")
        return rec

    def consume(self, raw: str) -> TokenRecord:
        rec = self.lookup(raw)
        if rec.state is not TokenRecordState.PENDING:
            raise TokenConflictError("Token not pending")
        rec.state = TokenRecordState.CONSUMED
        return rec

    def invalidate_session_revision(
        self, session_id: str, revision: int | None = None
    ) -> int:
        """Invalidate pending tokens for session (optionally matching revision)."""
        n = 0
        for rec in self._by_hash.values():
            if rec.session_id != session_id:
                continue
            if revision is not None and rec.revision != revision:
                continue
            if rec.state is TokenRecordState.PENDING:
                rec.state = TokenRecordState.INVALIDATED
                n += 1
        return n

    def pending_for_session(self, session_id: str) -> list[TokenRecord]:
        return [
            r
            for r in self._by_hash.values()
            if r.session_id == session_id and r.state is TokenRecordState.PENDING
        ]

    def bind_snapshot(self, raw: str) -> dict[str, Any]:
        """Debug/test helper — never expose raw."""
        rec = self.lookup(raw)
        return {
            "token_hash": rec.token_hash,
            "action": rec.action.value,
            "session_id": rec.session_id,
            "revision": rec.revision,
            "state": rec.state.value,
            "draft_hash": rec.draft_hash,
            "nonce": rec.nonce,
            "raw_stored": False,
        }
