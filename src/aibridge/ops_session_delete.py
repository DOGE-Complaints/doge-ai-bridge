"""Ops-only session delete CLI — no channel OpenAPI path (HTTP Unknown).

Usage::

    AIBRIDGE_OPS_BEARER_TOKEN=… DATABASE_URL=postgres://… \\
      python -m aibridge.ops_session_delete --session-id sess_… --ops-bearer …

Fail-closed when ops bearer env is unset or does not match ``--ops-bearer``.
Requires Postgres ``DATABASE_URL`` for production delete (history/tokens/confirm).
"""

from __future__ import annotations

import argparse
import sys

from aibridge.config import get_settings
from aibridge.db import is_postgres_url
from aibridge.privacy_retention import OpsAuthError, ops_delete_session, verify_ops_bearer


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Ops-only session delete (privacy retention). "
            "Not a channel OpenAPI route — HTTP path remains Unknown."
        )
    )
    parser.add_argument("--session-id", required=True)
    parser.add_argument(
        "--ops-bearer",
        required=True,
        help="Must match AIBRIDGE_OPS_BEARER_TOKEN (fail-closed otherwise)",
    )
    args = parser.parse_args(argv)
    settings = get_settings()
    expected = (settings.aibridge_ops_bearer_token or "").strip()
    try:
        verify_ops_bearer(presented=args.ops_bearer, expected=expected)
    except OpsAuthError as exc:
        print(f"FAIL closed: {exc}", file=sys.stderr)
        return 2

    url = (settings.database_url or "").strip()
    if not is_postgres_url(url):
        print(
            "FAIL closed: DATABASE_URL must be Postgres for production ops delete "
            "(no channel OAS invent; empty HistoryStore path removed).",
            file=sys.stderr,
        )
        return 3

    from aibridge.confirm import ConfirmationGuard
    from aibridge.migrate import apply_migrations
    from aibridge.pg_runtime import (
        PostgresActionTokenStore,
        PostgresConfirmSessionStore,
        PostgresHistoryStore,
    )
    from aibridge.sessions import PostgresSessionStore

    apply_migrations(url)
    token_ttl = (
        int(settings.aibridge_action_token_ttl_seconds)
        if settings.aibridge_action_token_ttl_seconds is not None
        else 900
    )
    history = PostgresHistoryStore(url)
    tokens = PostgresActionTokenStore(url, ttl_seconds=token_ttl)
    confirm_sessions = PostgresConfirmSessionStore(url)
    session_store = PostgresSessionStore(url)
    guard = ConfirmationGuard(tokens=tokens, confirm_sessions=confirm_sessions)
    try:
        result = ops_delete_session(
            session_id=args.session_id,
            ops_bearer_presented=args.ops_bearer,
            ops_bearer_expected=expected,
            history=history,
            tokens=tokens,
            guard=guard,
            session_store=session_store,
        )
    except OpsAuthError as exc:
        print(f"FAIL closed: {exc}", file=sys.stderr)
        return 2
    print(
        "ok ops_session_delete "
        f"session={result.session_id} "
        f"minimized={result.narrative_minimized} "
        f"invalidated={result.tokens_invalidated} "
        f"confirm_dropped={result.confirm_dropped} "
        f"session_deactivated={result.session_deactivated}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
