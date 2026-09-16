"""STORY-AIBRIDGE-20 — full flat instructions.manifest.json (ADR-2 / REQ-05 §4.2)."""

from __future__ import annotations

from pathlib import Path

from aibridge.content import load_content_bundle, load_manifest

ROOT = Path(__file__).resolve().parents[1]
INSTRUCTIONS = ROOT / "src" / "instructions"
MANIFEST = INSTRUCTIONS / "instructions.manifest.json"
WIRE_OAS = ROOT / "docs" / "openapi" / "story-intake-actions.openapi.yaml"
PAYLOAD = INSTRUCTIONS / "schema-packs.uus_veerenni_civic.v3.payload.schema.json"
MANIFEST_NAME = "instructions.manifest.json"

# REQ-05 §4.2 layer order (verbatim architecture list; all present in dump).
REQ_05_42_ORDER = [
    "root.md",
    "bootstrap.md",
    "base.md",
    "communication-presets-reference.md",
    "instruction-modules-index.md",
    "story-data-model.md",
    "story-label-taxonomy.md",
    "story-interview-flow.md",
    "story-i18n-policy.md",
    "story-lifecycle-instructions.md",
    "ingest-validation.md",
    "ingest-deep-parsing.md",
    "safety-compliance.md",
    "story-policy-gate.md",
    "story-normalizer.md",
    "api-orchestrator.md",
    "story-api-methods-reference.md",
    "schema-packs.README.md",
    "schema-packs.uus_veerenni_civic.v3.interview-overlay.md",
    "schema-packs.uus_veerenni_civic.v3.inbound-validation.md",
    "schema-packs.uus_veerenni_civic.v3.locale-jurisdiction.md",
    "schema-packs.uus_veerenni_civic.v3.pack.json",
    "schema-packs.uus_veerenni_civic.v3.payload.schema.json",
    "schema-packs.uus_veerenni_civic.v3.taxonomy.json",
    "activity-legacy-paths-inventory.md",
]

PACK_JSON = [
    "schema-packs.uus_veerenni_civic.v3.pack.json",
    "schema-packs.uus_veerenni_civic.v3.payload.schema.json",
    "schema-packs.uus_veerenni_civic.v3.taxonomy.json",
]


def _dir_children() -> set[str]:
    return {p.name for p in INSTRUCTIONS.iterdir() if p.is_file()} - {MANIFEST_NAME}


def test_completeness_dir_set_equals_files_set() -> None:
    files = load_manifest(MANIFEST)["files"]
    assert set(files) == _dir_children()
    assert MANIFEST_NAME not in files
    assert "aibridge-channel-v1.openapi.yaml" not in files


def test_layer_order_matches_req_05_4_2() -> None:
    files = load_manifest(MANIFEST)["files"]
    assert files == REQ_05_42_ORDER


def test_pack_json_in_files() -> None:
    files = set(load_manifest(MANIFEST)["files"])
    for name in PACK_JSON:
        assert name in files


def test_omit_would_fail_completeness() -> None:
    files = list(load_manifest(MANIFEST)["files"])
    omitted = files[0]
    remaining = set(files) - {omitted}
    assert remaining != _dir_children()


def test_load_content_bundle_full_dump() -> None:
    loaded = load_content_bundle(
        instructions_dir=INSTRUCTIONS,
        manifest_path=MANIFEST,
        source_commit="story-20-p3",
        wire_oas_path=WIRE_OAS,
        pack_schema_path=PAYLOAD,
    )
    assert loaded.assembled_instructions.strip()
    assert len(loaded.bundle_hash) == 64
    assert len(loaded.instructions_hash) == 64
    assert len(loaded.pack_hash) == 64
    hashes = dict(loaded.file_hashes)
    assert "root.md" in hashes
    assert "schema-packs.uus_veerenni_civic.v3.payload.schema.json" in hashes
    assert loaded.assembled_instructions.count("\n\n") >= 1
