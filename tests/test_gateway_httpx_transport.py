"""G-02 — HttpxGatewayTransport TLS verify (mocked; no live Railway URL)."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import httpx
import pytest

from aibridge.config import Settings
from aibridge.gateway import (
    GatewayExecutor,
    GatewayOutcome,
    HttpxGatewayTransport,
    RawHttpResponse,
    default_executor_from_settings,
)


def test_httpx_transport_verify_tls_and_no_redirects() -> None:
    transport = HttpxGatewayTransport(verify_tls=True)
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.content = (
        b'{"data":{"draft_id":"d1"},"trace_id":"t1"}'
    )
    mock_resp.url = "https://gateway.example.invalid/story-drafts"

    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = False
    mock_client.request.return_value = mock_resp

    with patch("httpx.Client", return_value=mock_client) as client_cls:
        out = transport.request(
            "POST",
            "https://gateway.example.invalid/story-drafts",
            headers={"Authorization": "Bearer gw"},
            json_body={"a": 1},
            timeout=12.0,
            allow_redirects=False,
        )
    assert isinstance(out, RawHttpResponse)
    assert out.status_code == 201
    client_cls.assert_called_once()
    kwargs = client_cls.call_args.kwargs
    assert kwargs["verify"] is True
    assert kwargs["follow_redirects"] is False
    assert kwargs["timeout"] == 12.0
    mock_client.request.assert_called_once()
    assert mock_client.request.call_args.args[0] == "POST"


def test_httpx_transport_rejects_allow_redirects_true() -> None:
    transport = HttpxGatewayTransport()
    with pytest.raises(AssertionError, match="redirects"):
        transport.request(
            "POST",
            "https://gateway.example.invalid/story-drafts",
            headers={},
            json_body={},
            timeout=1.0,
            allow_redirects=True,
        )


def test_default_executor_uses_httpx_transport() -> None:
    settings = Settings(
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_API_BEARER_TOKEN="gw",
        AIBRIDGE_CHANNEL_BEARER_TOKEN="ch",
    )
    ex = default_executor_from_settings(settings)
    assert isinstance(ex.transport, HttpxGatewayTransport)
    assert ex.transport.verify_tls is True


def test_executor_with_mocked_httpx_stashes() -> None:
    """Unit path: TLS client mocked — no live host (URL Unknown / not invented)."""
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.content = b'{"data":{"draft_id":"draft-1"},"trace_id":"trace-1"}'
    mock_resp.url = "https://gateway.example.invalid/story-drafts"
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = False
    mock_client.request.return_value = mock_resp

    with patch("httpx.Client", return_value=mock_client):
        ex = GatewayExecutor(
            origin="https://gateway.example.invalid",
            gateway_bearer="gw-secret",
            channel_bearer="ch-secret",
            redirect_base="https://spa.example",
            transport=HttpxGatewayTransport(verify_tls=True),
        )
        result = ex.execute_stash({"body": True}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.STASHED
    assert result.draft_id == "draft-1"
    assert result.http_posted is True


def test_httpx_timeout_maps_unknown() -> None:
    mock_client = MagicMock()
    mock_client.__enter__.return_value = mock_client
    mock_client.__exit__.return_value = False
    mock_client.request.side_effect = httpx.TimeoutException("timeout")

    with patch("httpx.Client", return_value=mock_client):
        ex = GatewayExecutor(
            origin="https://gateway.example.invalid",
            gateway_bearer="gw",
            channel_bearer="ch",
            transport=HttpxGatewayTransport(),
        )
        result = ex.execute_stash({"a": 1}, gateway_authorized=True)
    assert result.outcome is GatewayOutcome.UNKNOWN_OUTCOME
    assert result.http_posted is True
