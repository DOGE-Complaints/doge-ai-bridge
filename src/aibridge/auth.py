"""Channel Bearer authentication helpers."""

from __future__ import annotations

import hmac
import secrets

from aibridge.config import Settings


def constant_time_token_match(provided: str, accepted: tuple[str, ...]) -> bool:
    """Return True if provided matches any accepted token (constant-time per candidate)."""
    if not provided or not accepted:
        return False
    provided_bytes = provided.encode("utf-8")
    matched = False
    for token in accepted:
        # Always compare to avoid short-circuit on first match length differences.
        candidate = token.encode("utf-8")
        if len(provided_bytes) != len(candidate):
            # Still perform a compare against a dummy of equal length to reduce timing leak.
            hmac.compare_digest(provided_bytes, secrets.token_bytes(len(provided_bytes)))
            continue
        if hmac.compare_digest(provided_bytes, candidate):
            matched = True
    return matched


def extract_bearer(authorization: str | None) -> str | None:
    if authorization is None:
        return None
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer" or not parts[1]:
        return None
    return parts[1].strip()


def is_channel_authorized(authorization: str | None, settings: Settings) -> bool:
    token = extract_bearer(authorization)
    if token is None:
        return False
    return constant_time_token_match(token, settings.accepted_channel_tokens())
