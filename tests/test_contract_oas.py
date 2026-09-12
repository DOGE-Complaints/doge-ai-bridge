"""t05 — contract alignment vs committed channel OpenAPI."""

from __future__ import annotations

from pathlib import Path

import yaml
from fastapi.testclient import TestClient
from openapi_spec_validator import validate


REPO_ROOT = Path(__file__).resolve().parents[1]
OAS_PATH = REPO_ROOT / "docs" / "openapi" / "aibridge-channel-v1.openapi.yaml"

SUCCESS_REQUIRED = {
    "request_id",
    "session_id",
    "state",
    "reply_text",
    "actions",
    "outcome",
    "draft_id",
    "continuation_url",
}


def test_committed_oas_validates() -> None:
    spec = yaml.safe_load(OAS_PATH.read_text(encoding="utf-8"))
    validate(spec)
    assert "/v1/channel/turns" in spec["paths"]
    assert "/v1/channel/actions" in spec["paths"]
    props = spec["components"]["schemas"]["ChannelSuccessResponse"]["properties"]
    assert "callback_ack_text" not in props


def test_live_response_matches_oas_required_fields(
    client: TestClient, auth_header: dict[str, str], turn_payload: dict
) -> None:
    spec = yaml.safe_load(OAS_PATH.read_text(encoding="utf-8"))
    required = set(
        spec["components"]["schemas"]["ChannelSuccessResponse"]["required"]
    )
    assert required == SUCCESS_REQUIRED

    response = client.post(
        "/v1/channel/turns", json=turn_payload, headers=auth_header
    )
    body = response.json()
    assert set(body.keys()) == required
    assert "callback_ack_text" not in body


def test_action_request_required_fields_in_oas() -> None:
    spec = yaml.safe_load(OAS_PATH.read_text(encoding="utf-8"))
    required = set(
        spec["components"]["schemas"]["ChannelActionRequest"]["required"]
    )
    assert required == {
        "channel",
        "event_id",
        "callback_query_id",
        "principal",
        "action_token",
    }
