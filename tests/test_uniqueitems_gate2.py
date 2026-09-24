"""STORY-AIBRIDGE-42 — Gate 2 uniqueItems (T-UNIQUE / AC-04)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from aibridge.request_assembly import (
    FULL_SCHEMA_KEYWORDS,
    ValidationGateError,
    schema_validation_complete,
    validate_gate2_pack_payload,
)

ROOT = Path(__file__).resolve().parents[1]
PACK_CANONICAL = (
    ROOT / "src" / "instructions" / "schema-packs.uus_veerenni_civic.v3.payload.schema.json"
)


def _houses_schema(*, unique: bool | None) -> dict:
    schema: dict = {
        "type": "array",
        "items": {"type": "string"},
    }
    if unique is not None:
        schema["uniqueItems"] = unique
    return schema


def test_uniqueitems_in_keyword_set() -> None:
    assert "uniqueItems" in FULL_SCHEMA_KEYWORDS


def test_t_unique_01_distinct_strings_pass() -> None:
    """T-UNIQUE-01 — ['24','26'] with uniqueItems:true passes."""
    validate_gate2_pack_payload(["24", "26"], _houses_schema(unique=True))


def test_t_unique_02_duplicate_strings_fail() -> None:
    """T-UNIQUE-02 — duplicate strings rejected at path."""
    with pytest.raises(ValidationGateError, match=r"gate2:.*uniqueItems"):
        validate_gate2_pack_payload(["24", "24"], _houses_schema(unique=True))


def test_t_unique_03_objects_key_order_independent() -> None:
    """T-UNIQUE-03 — equal nested objects with different key order fail."""
    schema = {
        "type": "array",
        "uniqueItems": True,
        "items": {"type": "object"},
    }
    with pytest.raises(ValidationGateError, match=r"uniqueItems"):
        validate_gate2_pack_payload(
            [{"a": 1, "b": 2}, {"b": 2, "a": 1}],
            schema,
        )


def test_t_unique_04_nested_arrays_duplicate() -> None:
    """T-UNIQUE-04 — repeated nested arrays fail."""
    schema = {
        "type": "array",
        "uniqueItems": True,
        "items": {"type": "array", "items": {"type": "string"}},
    }
    with pytest.raises(ValidationGateError, match=r"uniqueItems"):
        validate_gate2_pack_payload([["x"], ["x"]], schema)


def test_t_unique_05_uniqueitems_false_allows_duplicates() -> None:
    """T-UNIQUE-05 — uniqueItems:false → duplicates pass."""
    validate_gate2_pack_payload(["24", "24"], _houses_schema(unique=False))


def test_t_unique_06_keyword_absent_allows_duplicates() -> None:
    """T-UNIQUE-06 — keyword absent → duplicates pass."""
    validate_gate2_pack_payload(["24", "24"], _houses_schema(unique=None))


def test_t_unique_07_empty_and_singleton() -> None:
    """T-UNIQUE-07 — empty and one-element arrays pass."""
    validate_gate2_pack_payload([], _houses_schema(unique=True))
    validate_gate2_pack_payload(["24"], _houses_schema(unique=True))


def test_t_unique_08_uus_veerenni_duplicate_houses_under_street() -> None:
    """T-UNIQUE-08 / AC-04 — duplicate houses under one street → Gate 2 reject."""
    pack = json.loads(PACK_CANONICAL.read_text(encoding="utf-8"))
    assert (
        pack["properties"]["geo"]["properties"]["streets"]["items"]["properties"]["houses"][
            "uniqueItems"
        ]
        is True
    )
    payload = {
        "signals": {"civic_domain": "roads", "failure_pattern": "pothole"},
        "geo": {
            "streets": [
                {"street": "Veerenni", "houses": ["24", "24"]},
            ]
        },
    }
    with pytest.raises(ValidationGateError, match=r"gate2:.*uniqueItems"):
        validate_gate2_pack_payload(payload, pack)


def test_t_unique_09_same_house_different_streets_ok() -> None:
    """T-UNIQUE-09 — same house under two streets is not conflated."""
    pack = json.loads(PACK_CANONICAL.read_text(encoding="utf-8"))
    payload = {
        "signals": {"civic_domain": "roads", "failure_pattern": "pothole"},
        "geo": {
            "streets": [
                {"street": "Veerenni", "houses": ["24"]},
                {"street": "Pärnu mnt", "houses": ["24"]},
            ]
        },
    }
    validate_gate2_pack_payload(payload, pack)


def test_schema_validation_complete_proves_uniqueitems() -> None:
    """Readiness probe includes uniqueItems behavioral prove."""
    assert schema_validation_complete() is True


def test_schema_validation_complete_false_when_uniqueitems_broken(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """G-02 — negative prove: broken uniqueItems enforce → completeness False.

    Readiness maps this to ``schema_validation_incomplete``
    (``readiness.py`` when ``aibridge_dry_run`` is False and flag set).
    """
    monkeypatch.setattr(
        "aibridge.request_assembly._assert_unique_items",
        lambda instance, path: None,
    )
    assert schema_validation_complete() is False


def test_pack_disk_still_has_uniqueitems() -> None:
    """AC hygiene — canonical pack on disk retains uniqueItems."""
    raw = PACK_CANONICAL.read_text(encoding="utf-8")
    assert '"uniqueItems": true' in raw
