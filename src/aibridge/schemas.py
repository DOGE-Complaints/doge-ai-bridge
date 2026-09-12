"""Pydantic models aligned with aibridge-channel-v1 OpenAPI."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

_DECIMAL_ID = re.compile(r"^-?\d+$")


def _require_decimal_string(value: str) -> str:
    if not _DECIMAL_ID.fullmatch(value):
        raise ValueError("must be a decimal string")
    return value


class ChannelPrincipal(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    chat_id: str

    @field_validator("user_id", "chat_id")
    @classmethod
    def _ids(cls, value: str) -> str:
        return _require_decimal_string(value)


class ChannelMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_id: str
    text: str = Field(min_length=1)
    language_code: str | None = None

    @field_validator("message_id")
    @classmethod
    def _message_id(cls, value: str) -> str:
        return _require_decimal_string(value)


class ChannelTurnRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: Literal["telegram"]
    event_id: str = Field(min_length=1)
    principal: ChannelPrincipal
    message: ChannelMessage


class ChannelActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    channel: Literal["telegram"]
    event_id: str = Field(min_length=1)
    callback_query_id: str = Field(min_length=1)
    principal: ChannelPrincipal
    action_token: str = Field(min_length=1, max_length=64)


class ChannelAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str
    token: str = Field(max_length=64)
    style: Literal["primary", "success", "danger", "default"]


class ChannelSuccessResponse(BaseModel):
    """Bounded success envelope — intentionally no callback_ack_text."""

    model_config = ConfigDict(extra="forbid")

    request_id: str
    session_id: str
    state: str
    reply_text: str
    actions: list[ChannelAction]
    outcome: str | None
    draft_id: str | None
    continuation_url: str | None


class ChannelErrorDetail(BaseModel):
    model_config = ConfigDict(extra="forbid")

    code: str
    message: str
    retryable: bool


class ChannelErrorBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_id: str
    error: ChannelErrorDetail
