"""Success / fail bind payloads (AC-09-04 / success bind).

Implement JSON keys (Open in arch; chosen for this wave — not gateway public SSOT):
``issue_id``, ``generation_version``, ``outcome``, ``poster_url``, ``apply``,
``reason_class``.
"""

from __future__ import annotations

from typing import Any

from aibridge.sense_bind.errors import BindFailureClass


def build_success_bind_payload(
    *,
    issue_id: str,
    generation_version: str,
    brief: dict[str, Any],
    poster_url: str,
) -> dict[str, Any]:
    """Logical success bind: apply slice + HTTPS URL + version — no board SSOT."""
    if not poster_url.startswith("https://"):
        raise ValueError("poster_url must be public https://")
    title = brief.get("title")
    summary = brief.get("summary")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("brief.title required for success bind")
    if not isinstance(summary, dict):
        raise ValueError("brief.summary object required for success bind")
    return {
        "issue_id": issue_id,
        "generation_version": generation_version,
        "outcome": "success",
        "poster_url": poster_url,
        "apply": {
            "title": title.strip(),
            "summary": summary,
        },
    }


def build_fail_bind_payload(
    *,
    issue_id: str,
    generation_version: str,
    reason_class: BindFailureClass | str,
) -> dict[str, Any]:
    """Fail bind: reason class only — never include a fabricated brief."""
    cls = (
        reason_class.value
        if isinstance(reason_class, BindFailureClass)
        else str(reason_class)
    )
    payload = {
        "issue_id": issue_id,
        "generation_version": generation_version,
        "outcome": "failure",
        "reason_class": cls,
    }
    # Hard guard — no fake brief on fail path.
    assert "brief" not in payload
    assert "apply" not in payload
    return payload


def assert_no_fake_brief_on_fail(payload: dict[str, Any]) -> None:
    if payload.get("outcome") == "failure" and (
        "brief" in payload or "apply" in payload
    ):
        raise AssertionError("fail bind must not carry brief/apply")
