"""Runtime configuration for channel façade + content bundle (stories 01–02)."""

from __future__ import annotations

import hmac
from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Env-backed settings."""

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

    database_url: str = Field(default="", validation_alias="DATABASE_URL")
    dogestonia_instructions_dir: str = Field(
        default="",
        validation_alias="DOGESTONIA_INSTRUCTIONS_DIR",
    )
    dogestonia_instructions_manifest: str = Field(
        default="",
        validation_alias="DOGESTONIA_INSTRUCTIONS_MANIFEST",
    )
    dogestonia_content_source_commit: str = Field(
        default="",
        validation_alias="DOGESTONIA_CONTENT_SOURCE_COMMIT",
    )
    dogestonia_openapi_path: str = Field(
        default="",
        validation_alias="DOGESTONIA_OPENAPI_PATH",
    )
    dogestonia_payload_schema_path: str = Field(
        default="",
        validation_alias="DOGESTONIA_PAYLOAD_SCHEMA_PATH",
    )
    dogestonia_tool_schema_path: str = Field(
        default="",
        validation_alias="DOGESTONIA_TOOL_SCHEMA_PATH",
    )
    aibridge_deployment_id: str = Field(
        default="local",
        validation_alias="AIBRIDGE_DEPLOYMENT_ID",
    )
    aibridge_bundle_gc_grace_seconds: int = Field(
        default=86400,
        validation_alias="AIBRIDGE_BUNDLE_GC_GRACE_SECONDS",
    )
    openai_api_key: str = Field(default="", validation_alias="OPENAI_API_KEY")
    openai_model: str = Field(default="", validation_alias="OPENAI_MODEL")
    openai_store_responses: str = Field(
        default="false",
        validation_alias="OPENAI_STORE_RESPONSES",
    )
    dogestonia_operation_id: str = Field(
        default="postStoryDraftStash",
        validation_alias="DOGESTONIA_OPERATION_ID",
    )
    dogestonia_schema_id: str = Field(default="", validation_alias="DOGESTONIA_SCHEMA_ID")
    dogestonia_schema_version: str = Field(
        default="",
        validation_alias="DOGESTONIA_SCHEMA_VERSION",
    )
    dogestonia_origin_source: str = Field(
        default="openai_responses_telegram",
        validation_alias="DOGESTONIA_ORIGIN_SOURCE",
    )
    # Budget placeholders — numeric defaults Unknown until measured (do not invent).
    aibridge_max_input_tokens: int | None = Field(
        default=None,
        validation_alias="AIBRIDGE_MAX_INPUT_TOKENS",
    )
    aibridge_max_output_tokens: int | None = Field(
        default=None,
        validation_alias="AIBRIDGE_MAX_OUTPUT_TOKENS",
    )
    aibridge_max_responses_calls_per_turn: int | None = Field(
        default=None,
        validation_alias="AIBRIDGE_MAX_RESPONSES_CALLS_PER_TURN",
    )
    aibridge_max_tool_calls_per_turn: int | None = Field(
        default=None,
        validation_alias="AIBRIDGE_MAX_TOOL_CALLS_PER_TURN",
    )
    aibridge_openai_timeout_ms: int | None = Field(
        default=None,
        validation_alias="AIBRIDGE_OPENAI_TIMEOUT_MS",
    )
    aibridge_max_session_turns: int | None = Field(
        default=None,
        validation_alias="AIBRIDGE_MAX_SESSION_TURNS",
    )
    # Story 05 — gateway executor
    dogestonia_gateway_origin: str = Field(
        default="",
        validation_alias="DOGESTONIA_GATEWAY_ORIGIN",
    )
    dogestonia_draft_redirect_base_url: str = Field(
        default="",
        validation_alias="DOGESTONIA_DRAFT_REDIRECT_BASE_URL",
    )
    aibridge_dry_run: bool = Field(
        default=False,
        validation_alias="AIBRIDGE_DRY_RUN",
    )
    aibridge_gateway_timeout_seconds: float = Field(
        default=30.0,
        validation_alias="AIBRIDGE_GATEWAY_TIMEOUT_SECONDS",
    )
    # Story 09 — production forbids silent memory stores when false
    aibridge_allow_memory_stores: bool = Field(
        default=True,
        validation_alias="AIBRIDGE_ALLOW_MEMORY_STORES",
    )

    @field_validator(
        "aibridge_channel_bearer_token",
        "aibridge_channel_previous_bearer_token",
        "dogestonia_api_bearer_token",
        "database_url",
        "dogestonia_instructions_dir",
        "dogestonia_instructions_manifest",
        "dogestonia_content_source_commit",
        "dogestonia_openapi_path",
        "dogestonia_payload_schema_path",
        "dogestonia_tool_schema_path",
        "aibridge_deployment_id",
        "openai_api_key",
        "openai_model",
        "openai_store_responses",
        "dogestonia_operation_id",
        "dogestonia_schema_id",
        "dogestonia_schema_version",
        "dogestonia_origin_source",
        "dogestonia_gateway_origin",
        "dogestonia_draft_redirect_base_url",
        mode="before",
    )
    @classmethod
    def _strip_strings(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value

    @field_validator("openai_store_responses", mode="after")
    @classmethod
    def _reject_store_true(cls, value: str) -> str:
        """AC #1: Responses always store:false — refuse conflicting env."""
        normalized = (value or "false").strip().lower()
        if normalized in {"true", "1", "yes", "on"}:
            raise ValueError(
                "OPENAI_STORE_RESPONSES must be false (aibridge forces store:false)"
            )
        return normalized or "false"

    def channel_auth_configured(self) -> bool:
        return bool(self.aibridge_channel_bearer_token)

    def responses_store_false_enforced(self) -> bool:
        """True when env does not request OpenAI store:true (always expected)."""
        return self.openai_store_responses in {"", "false", "0", "no", "off"}

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

    def content_configured(self) -> bool:
        """True when deployment expects a local content bundle (story 02)."""
        return bool(
            self.dogestonia_content_source_commit
            and self.dogestonia_instructions_dir
            and self.dogestonia_instructions_manifest
            and self.dogestonia_openapi_path
            and self.dogestonia_payload_schema_path
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()


def reset_settings_cache() -> None:
    get_settings.cache_clear()
