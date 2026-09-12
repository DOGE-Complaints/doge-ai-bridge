"""Constrained gateway HTTPS executor — AIB-HTTP-01…05 (story 05)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol
from urllib.parse import quote, urlparse

from aibridge.metrics import get_metrics

STASH_PATH = "/story-drafts"

# Operator reconciliation SSOT (do not invent lookup API).
UNKNOWN_OUTCOME_RUNBOOK = (
    "docs/runbooks/unknown-outcome-reconciliation.md"
)

STASH_REPLY = (
    "Draft stashed in DOGEstonia. Open the link to continue editing — "
    "this is not a published Story."
)
DRY_RUN_REPLY = (
    "Dry-run: local validation OK. Draft was not sent to DOGEstonia."
)
UNKNOWN_REPLY = (
    "Send result is unclear. Do not send the same revision again — "
    f"operator: see {UNKNOWN_OUTCOME_RUNBOOK}"
)


class GatewayOutcome(StrEnum):
    STASHED = "stashed"
    VALIDATION_ERROR = "validation_error"
    GATEWAY_UNAUTHORIZED = "gateway_unauthorized"
    GEO_SCOPE_MISMATCH = "geo_scope_mismatch"
    TRANSIENT_FAILURE = "transient_failure"
    UNKNOWN_OUTCOME = "unknown_outcome"
    CONTRACT_MISMATCH = "contract_mismatch"
    BLOCKED_BY_CONFIRMATION = "blocked_by_confirmation"
    INTERNAL_BRIDGE_ERROR = "internal_bridge_error"
    CANCELLED = "cancelled"
    DRY_RUN_OK = "dry_run_ok"


@dataclass(frozen=True)
class RawHttpResponse:
    status_code: int
    body: bytes
    final_url: str = ""


@dataclass
class GatewayResult:
    outcome: GatewayOutcome
    draft_id: str | None = None
    trace_id: str | None = None
    http_status: int | None = None
    reply_text: str = ""
    continuation_url: str | None = None
    http_posted: bool = False


class GatewayTransport(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout: float,
        allow_redirects: bool,
    ) -> RawHttpResponse: ...


@dataclass
class RecordingGatewayTransport:
    """Injectable / recorded fixtures — never contacts a live gateway."""

    scripted: list[RawHttpResponse] = field(default_factory=list)
    calls: list[dict[str, Any]] = field(default_factory=list)
    raise_on_call: Exception | None = None

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout: float,
        allow_redirects: bool,
    ) -> RawHttpResponse:
        if allow_redirects:
            raise AssertionError("redirects must be disabled")
        self.calls.append(
            {
                "method": method,
                "url": url,
                "headers": dict(headers),
                "json_body": dict(json_body),
                "timeout": timeout,
                "allow_redirects": allow_redirects,
            }
        )
        if self.raise_on_call is not None:
            raise self.raise_on_call
        if not self.scripted:
            raise RuntimeError("RecordingGatewayTransport: no scripted response")
        return self.scripted.pop(0)


def build_continuation_url(*, redirect_base: str, draft_id: str) -> str:
    base = redirect_base.rstrip("/")
    return f"{base}/#/story/submit?draft_id={quote(draft_id, safe='')}"


def parse_success_body(
    body: bytes,
) -> tuple[str | None, str | None, str | None]:
    """Return (draft_id, trace_id, error_reason)."""
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, None, "invalid_json"
    if not isinstance(payload, dict):
        return None, None, "not_object"
    data = payload.get("data")
    draft_id: str | None = None
    if isinstance(data, dict):
        raw = data.get("draft_id")
        if isinstance(raw, str) and raw.strip():
            draft_id = raw.strip()
    trace_raw = payload.get("trace_id")
    trace_id = trace_raw.strip() if isinstance(trace_raw, str) and trace_raw.strip() else None
    if draft_id and trace_id:
        return draft_id, trace_id, None
    return draft_id, trace_id, "missing_fields"


def map_http_outcome(
    status: int,
    body: bytes,
    *,
    ambiguous: bool = False,
) -> GatewayOutcome:
    if ambiguous:
        return GatewayOutcome.UNKNOWN_OUTCOME
    if status == 201:
        draft_id, trace_id, err = parse_success_body(body)
        if err or not draft_id or not trace_id:
            return GatewayOutcome.CONTRACT_MISMATCH
        return GatewayOutcome.STASHED
    if status == 400:
        return GatewayOutcome.VALIDATION_ERROR
    if status == 401:
        return GatewayOutcome.GATEWAY_UNAUTHORIZED
    if status == 422:
        return GatewayOutcome.GEO_SCOPE_MISMATCH
    if status == 429:
        return GatewayOutcome.TRANSIENT_FAILURE
    if 500 <= status <= 599:
        return GatewayOutcome.TRANSIENT_FAILURE
    return GatewayOutcome.UNKNOWN_OUTCOME


def validate_stash_body_local(body: dict[str, Any]) -> None:
    """Minimal local validation for dry-run (no inventing full OAS run)."""
    if not isinstance(body, dict) or not body:
        raise ValueError("stash body must be a non-empty object")


@dataclass
class GatewayExecutor:
    """Posts only to configured HTTPS origin with gateway Bearer (never channel)."""

    origin: str
    gateway_bearer: str
    channel_bearer: str = ""
    dry_run: bool = False
    redirect_base: str = ""
    transport: GatewayTransport = field(default_factory=RecordingGatewayTransport)
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        self.origin = self.origin.rstrip("/")
        self.redirect_base = self.redirect_base.strip()

    def constrained_stash_url(self) -> str:
        parsed = urlparse(self.origin)
        if parsed.scheme != "https":
            raise ValueError("gateway origin must be https")
        if not parsed.netloc:
            raise ValueError("gateway origin missing host")
        return f"{self.origin}{STASH_PATH}"

    def authorization_header(self) -> str:
        if not self.gateway_bearer:
            raise ValueError("DOGESTONIA_API_BEARER_TOKEN required for gateway")
        return f"Bearer {self.gateway_bearer}"

    def execute_stash(
        self,
        body: dict[str, Any],
        *,
        gateway_authorized: bool,
    ) -> GatewayResult:
        if not gateway_authorized:
            return GatewayResult(
                outcome=GatewayOutcome.BLOCKED_BY_CONFIRMATION,
                reply_text="Send confirmation required before gateway.",
                http_posted=False,
            )
        try:
            validate_stash_body_local(body)
        except ValueError as exc:
            return GatewayResult(
                outcome=GatewayOutcome.VALIDATION_ERROR,
                reply_text=str(exc),
                http_posted=False,
            )

        if self.dry_run:
            return GatewayResult(
                outcome=GatewayOutcome.DRY_RUN_OK,
                reply_text=DRY_RUN_REPLY,
                http_posted=False,
            )

        try:
            url = self.constrained_stash_url()
        except ValueError as exc:
            return GatewayResult(
                outcome=GatewayOutcome.INTERNAL_BRIDGE_ERROR,
                reply_text=str(exc),
                http_posted=False,
            )

        import hmac

        if (
            self.channel_bearer
            and self.gateway_bearer
            and hmac.compare_digest(
                self.channel_bearer.encode("utf-8"),
                self.gateway_bearer.encode("utf-8"),
            )
        ):
            return GatewayResult(
                outcome=GatewayOutcome.INTERNAL_BRIDGE_ERROR,
                reply_text="Channel Bearer must never equal gateway Bearer.",
                http_posted=False,
            )

        headers = {
            "Authorization": self.authorization_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        # Authorization is always gateway_bearer — never channel token value.
        assert headers["Authorization"] == f"Bearer {self.gateway_bearer}"

        try:
            get_metrics().inc_gateway_posts()
            resp = self.transport.request(
                "POST",
                url,
                headers=headers,
                json_body=body,
                timeout=self.timeout_seconds,
                allow_redirects=False,
            )
        except TimeoutError:
            return GatewayResult(
                outcome=GatewayOutcome.UNKNOWN_OUTCOME,
                reply_text=UNKNOWN_REPLY,
                http_posted=True,
            )
        except Exception as exc:  # noqa: BLE001 — map to bounded outcome
            if _looks_ambiguous(exc):
                return GatewayResult(
                    outcome=GatewayOutcome.UNKNOWN_OUTCOME,
                    reply_text=UNKNOWN_REPLY,
                    http_posted=True,
                )
            return GatewayResult(
                outcome=GatewayOutcome.INTERNAL_BRIDGE_ERROR,
                reply_text="Gateway call failed before send.",
                http_posted=False,
            )

        if resp.final_url and resp.final_url.rstrip("/") != url.rstrip("/"):
            return GatewayResult(
                outcome=GatewayOutcome.CONTRACT_MISMATCH,
                http_status=resp.status_code,
                reply_text="Redirects are not allowed for gateway stash.",
                http_posted=True,
            )

        outcome = map_http_outcome(resp.status_code, resp.body)
        draft_id: str | None = None
        trace_id: str | None = None
        continuation: str | None = None
        reply = f"Gateway outcome: {outcome.value}."

        if outcome is GatewayOutcome.STASHED:
            draft_id, trace_id, _err = parse_success_body(resp.body)
            reply = STASH_REPLY
            if draft_id and self.redirect_base:
                continuation = build_continuation_url(
                    redirect_base=self.redirect_base, draft_id=draft_id
                )
        elif outcome is GatewayOutcome.CONTRACT_MISMATCH:
            reply = "Gateway response did not match stash contract (not stashed)."
        elif outcome is GatewayOutcome.UNKNOWN_OUTCOME:
            reply = UNKNOWN_REPLY

        return GatewayResult(
            outcome=outcome,
            draft_id=draft_id if outcome is GatewayOutcome.STASHED else None,
            trace_id=trace_id if outcome is GatewayOutcome.STASHED else None,
            http_status=resp.status_code,
            reply_text=reply,
            continuation_url=continuation if outcome is GatewayOutcome.STASHED else None,
            http_posted=True,
        )


def _looks_ambiguous(exc: BaseException) -> bool:
    name = type(exc).__name__.lower()
    msg = str(exc).lower()
    return "timeout" in name or "timeout" in msg or "disconnect" in msg


@dataclass
class HttpxGatewayTransport:
    """Production HTTPS transport — TLS verify on; redirects off.

    Live gateway host comes only from ``DOGESTONIA_GATEWAY_ORIGIN`` (Unknown until
    ops configures it). Do not invent Railway or other URLs in code/tests.
    """

    verify_tls: bool = True

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str],
        json_body: dict[str, Any],
        timeout: float,
        allow_redirects: bool,
    ) -> RawHttpResponse:
        import httpx

        if allow_redirects:
            raise AssertionError("redirects must be disabled for gateway stash")
        # Explicit TLS verify — never disable for production path.
        with httpx.Client(
            verify=self.verify_tls,
            follow_redirects=False,
            timeout=timeout,
        ) as client:
            resp = client.request(method, url, headers=headers, json=json_body)
            return RawHttpResponse(
                status_code=resp.status_code,
                body=resp.content,
                final_url=str(resp.url),
            )


def default_executor_from_settings(settings: Any, transport: GatewayTransport | None = None) -> GatewayExecutor:
    return GatewayExecutor(
        origin=getattr(settings, "dogestonia_gateway_origin", "") or "",
        gateway_bearer=getattr(settings, "dogestonia_api_bearer_token", "") or "",
        channel_bearer=getattr(settings, "aibridge_channel_bearer_token", "") or "",
        dry_run=bool(getattr(settings, "aibridge_dry_run", False)),
        redirect_base=getattr(settings, "dogestonia_draft_redirect_base_url", "") or "",
        transport=transport if transport is not None else HttpxGatewayTransport(verify_tls=True),
        timeout_seconds=float(getattr(settings, "aibridge_gateway_timeout_seconds", 30.0) or 30.0),
    )
