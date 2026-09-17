"""Load QA envelope fixtures from tests/fixtures/{cluster}/{name}.json."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FIXTURES_ROOT = Path(__file__).resolve().parent / "fixtures"


def load_fixture(cluster: str, name: str) -> dict[str, Any]:
    """Return full envelope; validates schema_version and cluster match."""
    path = FIXTURES_ROOT / cluster / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(f"fixture not found: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise ValueError(f"unsupported schema_version in {path}: {data.get('schema_version')!r}")
    if data.get("cluster") != cluster:
        raise ValueError(
            f"cluster mismatch in {path}: envelope={data.get('cluster')!r} expected={cluster!r}"
        )
    return data
