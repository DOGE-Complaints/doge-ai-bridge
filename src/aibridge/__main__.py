"""Uvicorn entrypoint: bind to Railway $PORT."""

from __future__ import annotations

import os

import uvicorn

from aibridge.app import app
from aibridge.config import get_settings


def main() -> None:
    settings = get_settings()
    port = int(os.environ.get("PORT", str(settings.port)))
    uvicorn.run(
        "aibridge.app:app",
        host="0.0.0.0",
        port=port,
        factory=False,
    )


if __name__ == "__main__":
    main()
