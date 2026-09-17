"""STORY-AIBRIDGE-23 — AUTH-* contract tests (ops + channel Bearer boundaries)."""

from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from aibridge.app import create_app
from aibridge.config import Settings, reset_settings_cache
from aibridge.dedupe import EventDedupeStore
from aibridge.interview import default_recording_engine
from aibridge.rate_limit import RateLimiter, hash_principal_key

_TESTS_ROOT = Path(__file__).resolve().parents[1]
if str(_TESTS_ROOT) not in sys.path:
    sys.path.insert(0, str(_TESTS_ROOT))
from fixture_loader import load_fixture  # noqa: E402

CHANNEL = "channel-token-aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
PREVIOUS = "previous-token-cccccccccccccccccccccccccccccccc"
GATEWAY = "gateway-token-bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
WRONG_SAME = "channel-token-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
WRONG_DIFF = "short-wrong"

STORY = "STORY-AIBRIDGE-23-qa-auth-ops-boundaries"
AUTH_IDS = {f"AUTH-{i:03d}" for i in range(1, 13)}


def _base_settings(**overrides: object) -> Settings:
    reset_settings_cache()
    base: dict[str, object] = dict(
        AIBRIDGE_CHANNEL_BEARER_TOKEN=CHANNEL,
        AIBRIDGE_CHANNEL_PREVIOUS_BEARER_TOKEN=PREVIOUS,
        DOGESTONIA_API_BEARER_TOKEN=GATEWAY,
        DATABASE_URL="memory",
        DOGESTONIA_INTAKE_BASE_URL="https://gateway.example.invalid",
        DOGESTONIA_DRAFT_REDIRECT_BASE_URL="https://spa.example.invalid",
        OPENAI_API_KEY="sk-test-not-real",
        OPENAI_MODEL="gpt-test",
        AIBRIDGE_DRY_RUN=True,
    )
    base.update(overrides)
    return Settings(_env_file=None, **base)


def _client(settings: Settings | None = None) -> TestClient:
    cfg = settings or _base_settings()
    app = create_app(
        settings=cfg,
        dedupe_store=EventDedupeStore(),
        interview_engine=default_recording_engine(),
    )
    return TestClient(app)


def _auth_header(auth_ref: str | None) -> dict[str, str] | None:
    if auth_ref in (None, "none"):
        return None
    if auth_ref == "basic":
        return {"Authorization": "Basic dXNlcjpwYXNz"}
    if auth_ref == "bearer_empty":
        return {"Authorization": "Bearer"}
    if auth_ref == "channel":
        return {"Authorization": f"Bearer {CHANNEL}"}
    if auth_ref == "previous":
        return {"Authorization": f"Bearer {PREVIOUS}"}
    if auth_ref == "gateway":
        return {"Authorization": f"Bearer {GATEWAY}"}
    if auth_ref == "wrong_same_length":
        return {"Authorization": f"Bearer {WRONG_SAME}"}
    if auth_ref == "wrong_diff_length":
        return {"Authorization": f"Bearer {WRONG_DIFF}"}
    raise AssertionError(f"unknown auth_ref: {auth_ref!r}")


def _request(client: TestClient, payload: dict[str, Any]):
    method = payload["method"].upper()
    path = payload["path"]
    headers = _auth_header(payload.get("auth_ref"))
    kw: dict[str, Any] = {}
    if headers is not None:
        kw["headers"] = headers
    if method == "GET":
        return client.get(path, **kw)
    if method == "POST":
        return client.post(path, json=payload.get("body"), **kw)
    raise AssertionError(f"unsupported method {method}")


def test_traceability_story_covers_all_auth_ids() -> None:
    """AC: every AUTH-* matrix ID is bound to this story via fixtures."""
    names = [
        ("channel", "auth-valid-current"),
        ("channel", "turns-valid-private"),
        ("channel", "auth-previous-bearer"),
        ("channel", "auth-missing"),
        ("channel", "auth-basic-scheme"),
        ("channel", "auth-bearer-empty"),
        ("channel", "auth-wrong-same-length"),
        ("channel", "auth-wrong-diff-length"),
        ("channel", "auth-gateway-as-channel"),
        ("settings", "auth-channel-equals-gateway"),
        ("spies", "auth-forbid-bearer-leak"),
        ("channel", "auth-healthz-no-bearer"),
        ("channel", "auth-readyz-no-bearer"),
        ("channel", "auth-metrics-private"),
    ]
    seen: set[str] = set()
    for cluster, name in names:
        env = load_fixture(cluster, name)
        assert STORY in env["story_keys"] or "AUTH-001" in env["matrix_ids"]
        seen.update(i for i in env["matrix_ids"] if i.startswith("AUTH-"))
    # seed may only list AUTH-001 among AUTH; auth-valid-current also AUTH-001
    assert AUTH_IDS <= seen | {"AUTH-001"}
    assert AUTH_IDS == seen


@pytest.mark.parametrize(
    "name,matrix_id",
    [
        ("auth-valid-current", "AUTH-001"),
        ("auth-previous-bearer", "AUTH-002"),
        ("auth-missing", "AUTH-003"),
        ("auth-basic-scheme", "AUTH-004"),
        ("auth-bearer-empty", "AUTH-005"),
        ("auth-wrong-same-length", "AUTH-006"),
        ("auth-wrong-diff-length", "AUTH-007"),
        ("auth-gateway-as-channel", "AUTH-008"),
        ("auth-healthz-no-bearer", "AUTH-010"),
        ("auth-readyz-no-bearer", "AUTH-011"),
        ("auth-metrics-private", "AUTH-012"),
    ],
)
def test_channel_auth_matrix_from_fixtures(name: str, matrix_id: str) -> None:
    env = load_fixture("channel", name)
    assert matrix_id in env["matrix_ids"]
    assert env["cluster"] == "channel"
    client = _client()
    # Default client: Channel ≠ Gateway
    settings = _base_settings()
    assert not settings.channel_gateway_bearers_equal()
    client = _client(settings)

    payload = env["payload"]
    response = _request(client, payload)
    expect = payload["expect"]

    if "http_status" in expect:
        assert response.status_code == expect["http_status"]
    if "http_status_in" in expect:
        assert response.status_code in expect["http_status_in"]
    if "error_code" in expect:
        body = response.json()
        assert body["error"]["code"] == expect["error_code"]
        assert "Authorization" not in body["error"].get("message", "")
        assert CHANNEL not in response.text
    if "json" in expect:
        assert response.json() == expect["json"]
    if expect.get("no_generation"):
        # Recording engine unused on GET /readyz — no OpenAI calls.
        engine = client.app.state.interview_engine
        assert getattr(engine.client, "calls", []) == []
    if "content_type_contains" in expect:
        assert expect["content_type_contains"] in (response.headers.get("content-type") or "")
    for needle in expect.get("forbid_substrings", []):
        assert needle not in response.text


def test_auth_008_readyz_rejects_equal_bearers() -> None:
    env = load_fixture("settings", "auth-channel-equals-gateway")
    assert "AUTH-008" in env["matrix_ids"]
    overrides = {k: v for k, v in env["payload"]["overrides"].items()}
    settings = _base_settings(**overrides)
    assert settings.channel_gateway_bearers_equal()
    client = _client(settings)
    response = client.get("/readyz")
    expect = env["payload"]["expect_readyz"]
    assert response.status_code == expect["http_status"]
    assert response.json()["reason"] == expect["reason"]


def test_auth_009_channel_bearer_absent_from_error_and_metrics() -> None:
    env = load_fixture("spies", "auth-forbid-bearer-leak")
    assert "AUTH-009" in env["matrix_ids"]
    forbid_err = env["payload"]["forbid_substrings_in_error_body"]
    forbid_metrics = env["payload"]["forbid_substrings_in_metrics"]
    forbid_logs = env["payload"]["forbid_substrings_in_logs"]

    # CHANNEL appears in Authorization; settings accept a different token → 401.
    other = "other-token-zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz"
    client = _client(_base_settings(AIBRIDGE_CHANNEL_BEARER_TOKEN=other))

    bag: list[str] = []

    class _Bag(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            bag.append(self.format(record))

    handler = _Bag()
    handler.setFormatter(logging.Formatter("%(name)s %(levelname)s %(message)s"))
    loggers = [logging.getLogger("aibridge"), logging.getLogger()]
    prev_levels = [lg.level for lg in loggers]
    for lg in loggers:
        lg.addHandler(handler)
        lg.setLevel(logging.DEBUG)
    try:
        response = client.post(
            "/v1/channel/turns",
            json=load_fixture("channel", "turns-valid-private")["payload"]["body"],
            headers={"Authorization": f"Bearer {CHANNEL}"},
        )
    finally:
        for lg, level in zip(loggers, prev_levels, strict=True):
            lg.removeHandler(handler)
            lg.setLevel(level)

    assert response.status_code == 401
    for needle in forbid_err:
        assert needle not in response.text

    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    for needle in forbid_metrics:
        assert needle not in metrics.text

    log_blob = "\n".join(bag)
    for needle in forbid_logs:
        assert needle not in log_blob


def test_rate_limit_principal_key_is_hashed() -> None:
    """G-05: rate-limit store keys must not contain raw Authorization / Bearer prefix."""
    auth = f"Bearer {CHANNEL}"
    key = hash_principal_key(auth)
    assert key.startswith("p:")
    assert "Bearer" not in key
    assert CHANNEL not in key
    assert auth[:24] not in key
    assert hash_principal_key(auth) == key
    assert hash_principal_key(f"Bearer {WRONG_SAME}") != key
    assert hash_principal_key(None) == "anonymous"
    assert hash_principal_key("") == "anonymous"

    limiter = RateLimiter(principal_limit=2, window_seconds=60.0)
    assert limiter.allow(key) is None
    assert key in limiter._principal
    assert CHANNEL not in key
    for stored in limiter._principal:
        assert "Bearer" not in stored
        assert CHANNEL not in stored


def test_seed_turns_valid_private_copy_intact() -> None:
    """AUTH-001 overlap seed: tests copy exists; package original path still present."""
    from pathlib import Path

    original = (
        Path(__file__).resolve().parents[2]
        / "docs"
        / "tasks"
        / "backlog-stories"
        / "qa-inbound-outbound-data-flow"
        / "fixtures"
        / "turns-valid-private.json"
    )
    assert original.is_file()
    env = load_fixture("channel", "turns-valid-private")
    assert "AUTH-001" in env["matrix_ids"]
    assert env["payload"]["body"]["channel"] == "telegram"
