"""Runtime configuration for channel façade (story 01 minimal set)."""

from __future__ import annotations

import hmac
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Env-backed settings. Story 01 focuses on channel auth + body limits."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    port: int = Field(default=8080, validation_alias="PORT")
    aibridge_channel_bearer_token: str = Field(
        default="",
        validation_alias="AIBRIDGE_CHANNEL_BEARER_TOKEN",
    )
    aibridge_channel_previous_bearer_token: str = Field(
        default="",
        validation_alias="AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN",
    )
    dogestonia_api_bearer_token: str = Field(
        default="",
        validation_alias="DOGESTONIA_API_BEARER_TOKEN",
    )
    aibridge_max_request_bytes: int = Field(
        default=65536,
        validation_alias="AIBRIDGE_MAX_REQUEST_BYTES",
    )

    @field_validator(
        "aibridge_channel_bearer_token",
        "aibridge_channel_previous_bearer_token",
        "dogestonia_api_bearer_token",
        mode="before",
    )
    @classmethod
    def _strip_tokens(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    def channel_auth_configured(self) -> bool:
        return bool(self.aibridge_channel_bearer_token)

    def channel_gateway_bearers_equal(self) -> bool:
        channel = self.aibridge_channel_bearer_token
        gateway = self.dogestonia_api_bearer_token
        if not channel or not gateway:
            return False
        return hmac.compare_digest(channel.encode("utf-8"), gateway.encode("utf-8"))

    def accepted_channel_tokens(self) -> tuple[str, ...]:
        tokens = [self.aibridge_channel_bearer_token]
        if self.aibridge_channel_previous_bearer_token:
            tokens.append(self.aibridge_channel_previous_bearer_token)
        return tuple(t for t in tokens if t)


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
