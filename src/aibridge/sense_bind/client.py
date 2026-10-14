"""Outbound sense-brief bind-in client (service-auth) — aibridge → gateway.

Implement path (Open in arch; chosen for this wave — not gateway SSOT freeze):
``POST {GATEWAY_BASE_URL}/v1/issue-sense-brief/bind``

Uses ``GATEWAY_SERVICE_API_TOKEN`` only — never channel Bearer / worker S2S.
Worker does not own board pending/ready/failed SSOT (sibling gateway).
"""

from __future__ import annotations

import hmac
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlparse

from aibridge.gateway import (
    GatewayTransport,
    HttpxGatewayTransport,
    RawHttpResponse,
    RecordingGatewayTransport,
)
from aibridge.sense_bind.errors import BindFailure, BindFailureClass
from aibridge.sense_bind.logging_safe import BindLatencyTimer, log_bind_job
from aibridge.sense_bind.payload import (
    assert_no_fake_brief_on_fail,
    build_fail_bind_payload,
    build_success_bind_payload,
)

# Implement choice — not arch SSOT.
BIND_PATH = "/v1/issue-sense-brief/bind"


@dataclass
class BindResult:
    ok: bool
    http_status: int | None = None
    reason_class: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    http_posted: bool = False


@dataclass
class SenseBriefBindClient:
    """Posts success/fail bind payloads with gateway service-auth."""

    origin: str
    gateway_bearer: str
    channel_bearer: str = ""
    worker_s2s_token: str = ""
    dry_run: bool = False
    transport: GatewayTransport = field(default_factory=RecordingGatewayTransport)
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        self.origin = self.origin.rstrip("/")

    def authorization_header(self) -> str:
        if not self.gateway_bearer:
            raise ValueError("GATEWAY_SERVICE_API_TOKEN required for bind-in")
        return f"Bearer {self.gateway_bearer}"

    def bind_url(self) -> str:
        parsed = urlparse(self.origin)
        if parsed.scheme != "https":
            raise ValueError("bind origin must be https")
        if not parsed.netloc:
            raise ValueError("bind origin missing host")
        return f"{self.origin}{BIND_PATH}"

    def _assert_service_auth_domain(self) -> None:
        """Refuse if gateway bearer equals channel or worker S2S (≠ service-auth)."""
        gw = self.gateway_bearer.encode("utf-8")
        if self.channel_bearer and hmac.compare_digest(
            self.channel_bearer.encode("utf-8"), gw
        ):
            raise BindFailure(
                BindFailureClass.INTERNAL_ERROR,
                "gateway service token must not equal channel Bearer",
            )
        if self.worker_s2s_token and hmac.compare_digest(
            self.worker_s2s_token.encode("utf-8"), gw
        ):
            raise BindFailure(
                BindFailureClass.INTERNAL_ERROR,
                "gateway service token must not equal worker S2S",
            )

    def _post(self, body: dict[str, Any]) -> RawHttpResponse:
        self._assert_service_auth_domain()
        headers = {
            "Authorization": self.authorization_header(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        assert headers["Authorization"] == f"Bearer {self.gateway_bearer}"
        return self.transport.request(
            "POST",
            self.bind_url(),
            headers=headers,
            json_body=body,
            timeout=self.timeout_seconds,
            allow_redirects=False,
        )

    def bind_success(
        self,
        *,
        issue_id: str,
        generation_version: str,
        brief: dict[str, Any],
        poster_url: str,
    ) -> BindResult:
        timer = BindLatencyTimer()
        payload = build_success_bind_payload(
            issue_id=issue_id,
            generation_version=generation_version,
            brief=brief,
            poster_url=poster_url,
        )
        if self.dry_run:
            log_bind_job(
                issue_id=issue_id,
                generation_version=generation_version,
                event="success_dry_run",
                success=True,
                latency_ms=timer.elapsed_ms(),
            )
            return BindResult(ok=True, payload=payload, http_posted=False)
        try:
            resp = self._post(payload)
        except BindFailure:
            raise
        except Exception as exc:  # noqa: BLE001
            log_bind_job(
                issue_id=issue_id,
                generation_version=generation_version,
                event="success_transport_error",
                success=False,
                reason_class=BindFailureClass.INTERNAL_ERROR.value,
                latency_ms=timer.elapsed_ms(),
            )
            raise BindFailure(
                BindFailureClass.INTERNAL_ERROR, f"bind transport: {exc}"
            ) from exc
        ok = 200 <= resp.status_code < 300
        reason = None if ok else BindFailureClass.BIND_REJECTED.value
        log_bind_job(
            issue_id=issue_id,
            generation_version=generation_version,
            event="success_posted" if ok else "success_rejected",
            success=ok,
            reason_class=reason,
            latency_ms=timer.elapsed_ms(),
        )
        if not ok:
            raise BindFailure(
                BindFailureClass.BIND_REJECTED,
                f"gateway rejected success bind: http {resp.status_code}",
            )
        return BindResult(
            ok=True,
            http_status=resp.status_code,
            payload=payload,
            http_posted=True,
        )

    def bind_failure(
        self,
        *,
        issue_id: str,
        generation_version: str,
        reason_class: BindFailureClass | str,
    ) -> BindResult:
        timer = BindLatencyTimer()
        payload = build_fail_bind_payload(
            issue_id=issue_id,
            generation_version=generation_version,
            reason_class=reason_class,
        )
        assert_no_fake_brief_on_fail(payload)
        cls = payload["reason_class"]
        if self.dry_run:
            log_bind_job(
                issue_id=issue_id,
                generation_version=generation_version,
                event="fail_dry_run",
                success=False,
                reason_class=cls,
                latency_ms=timer.elapsed_ms(),
            )
            return BindResult(
                ok=True,
                reason_class=cls,
                payload=payload,
                http_posted=False,
            )
        try:
            resp = self._post(payload)
        except BindFailure:
            raise
        except Exception as exc:  # noqa: BLE001
            log_bind_job(
                issue_id=issue_id,
                generation_version=generation_version,
                event="fail_transport_error",
                success=False,
                reason_class=BindFailureClass.INTERNAL_ERROR.value,
                latency_ms=timer.elapsed_ms(),
            )
            raise BindFailure(
                BindFailureClass.INTERNAL_ERROR, f"fail-bind transport: {exc}"
            ) from exc
        # Fail-bind delivery itself rejected → still surface bind_rejected.
        delivered = 200 <= resp.status_code < 300
        log_bind_job(
            issue_id=issue_id,
            generation_version=generation_version,
            event="fail_posted" if delivered else "fail_delivery_rejected",
            success=False,
            reason_class=cls if delivered else BindFailureClass.BIND_REJECTED.value,
            latency_ms=timer.elapsed_ms(),
        )
        if not delivered:
            raise BindFailure(
                BindFailureClass.BIND_REJECTED,
                f"gateway rejected fail bind: http {resp.status_code}",
            )
        return BindResult(
            ok=True,
            http_status=resp.status_code,
            reason_class=cls,
            payload=payload,
            http_posted=True,
        )


def client_from_settings(
    settings: Any, transport: GatewayTransport | None = None
) -> SenseBriefBindClient:
    origin = (
        settings.intake_base_url()
        if hasattr(settings, "intake_base_url")
        else (getattr(settings, "gateway_base_url", "") or "")
    )
    return SenseBriefBindClient(
        origin=origin,
        gateway_bearer=getattr(settings, "gateway_service_api_token", "") or "",
        channel_bearer=getattr(settings, "aibridge_channel_bearer_token", "") or "",
        worker_s2s_token=getattr(settings, "aibridge_worker_sense_brief_s2s_token", "")
        or "",
        dry_run=bool(getattr(settings, "aibridge_dry_run", False)),
        transport=transport
        if transport is not None
        else HttpxGatewayTransport(verify_tls=True),
    )
