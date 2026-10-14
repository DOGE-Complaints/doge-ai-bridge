"""STORY-AIBRIDGE-50 — isolation harness for AC-09-01…06 (mocks only; no live vendors)."""

from __future__ import annotations

from aibridge.poster.pipeline import upload_poster_https
from aibridge.sense_bind.errors import BindFailureClass
from aibridge.sense_bind.payload import (
    assert_no_fake_brief_on_fail,
    build_fail_bind_payload,
)
from aibridge.sense_bind.version import regenerate_assets_distinguishable
from aibridge.sense_brief.errors import BriefFailure, BriefFailureClass
from aibridge.sense_brief.pipeline import generate_sense_brief, refuse_invented_civic_facts
from aibridge.sense_brief.prompts import (
    assert_not_interview_ssot,
    load_system_instructions_en,
    package_resource_exists,
)
from tests.harness.sense_brief_isolation import (
    CHANNEL_TOKEN,
    GOLDEN_CORPUS,
    IMAGE_POSTER_MODEL,
    INSUFFICIENT_CORPUS,
    STORAGE_CREDENTIAL,
    TEXT_BRIEF_MODEL,
    WORKER_ACCEPT_PATH,
    WORKER_TOKEN,
    accept_body,
    channel_auth_headers,
    isolation_client,
    isolation_settings,
    mock_storage_uploader,
    recording_gateway,
    worker_auth_headers,
)


def test_t01_harness_runs_without_live_vendor_secrets() -> None:
    """Skeleton: dry_run accept + mock storage — no OpenAI/bucket/gateway live creds."""
    client = isolation_client()
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(issue_id="issue-50-skel"),
        headers=worker_auth_headers(),
    )
    assert r.status_code == 200
    data = r.json()
    assert data["pipeline"] == "bind_ready"
    assert str(data["poster_url"]).startswith("https://")
    uploader = mock_storage_uploader()
    url = uploader.upload(b"\x89PNG\r\n\x1a\nfake", content_type="image/png", object_key="k")
    assert url.startswith("https://")
    transport = recording_gateway()
    assert transport.calls == []


def test_ac_09_01_channel_bearer_rejected_on_accept() -> None:
    assert not WORKER_ACCEPT_PATH.startswith("/v1/channel/")
    assert WORKER_ACCEPT_PATH.startswith("/v1/worker/")
    client = isolation_client()
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(),
        headers=channel_auth_headers(),
    )
    assert r.status_code == 401
    assert r.json()["error"]["code"] == "unauthorized"
    # Worker S2S still admits (separate entry).
    ok = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(issue_id="issue-50-ok", generation_version="v-ok"),
        headers=worker_auth_headers(),
    )
    assert ok.status_code == 200
    assert CHANNEL_TOKEN not in WORKER_TOKEN


def test_ac_09_02_logical_l2_brief_shape() -> None:
    brief = generate_sense_brief(GOLDEN_CORPUS, text_brief_model=TEXT_BRIEF_MODEL)
    assert brief.satisfies_l2()
    assert len(brief.title) <= 80
    assert brief.summary.et and brief.summary.ru and brief.summary.en
    client = isolation_client()
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(issue_id="issue-50-l2"),
        headers=worker_auth_headers(),
    )
    assert r.status_code == 200
    body = r.json()["brief"]
    assert len(body["title"]) <= 80
    assert body["summary"]["et"] and body["summary"]["ru"] and body["summary"]["en"]


def test_ac_09_03_upload_mock_returns_https_url() -> None:
    brief = generate_sense_brief(GOLDEN_CORPUS, text_brief_model=TEXT_BRIEF_MODEL)
    url = upload_poster_https(
        brief,
        image_poster_model=IMAGE_POSTER_MODEL,
        storage_credential=STORAGE_CREDENTIAL,
        object_key="issue-50/v1.png",
        uploader=mock_storage_uploader(),
    )
    assert url.startswith("https://")
    client = isolation_client()
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(issue_id="issue-50-https"),
        headers=worker_auth_headers(),
    )
    assert r.status_code == 200
    assert str(r.json()["poster_url"]).startswith("https://")


def test_ac_09_04_fail_bind_reason_class_no_fake_brief() -> None:
    payload = build_fail_bind_payload(
        issue_id="issue-50-fail",
        generation_version="v1",
        reason_class=BindFailureClass.CORPUS_INSUFFICIENT,
    )
    assert payload["outcome"] == "failure"
    assert payload["reason_class"] == "corpus_insufficient"
    assert "brief" not in payload
    assert "apply" not in payload
    assert_no_fake_brief_on_fail(payload)

    transport = recording_gateway()
    client = isolation_client(
        isolation_settings(AIBRIDGE_DRY_RUN=False),
        transport=transport,
    )
    r = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(issue_id="issue-50-insuf", corpus=INSUFFICIENT_CORPUS),
        headers=worker_auth_headers(),
    )
    assert r.status_code == 422
    assert r.json()["error"]["code"] == "corpus_insufficient"
    assert len(transport.calls) == 1
    bind_body = transport.calls[0]["json_body"]
    assert bind_body["outcome"] == "failure"
    assert bind_body["reason_class"] == "corpus_insufficient"
    assert "brief" not in bind_body
    assert "apply" not in bind_body


def test_ac_09_05_prompt_isolation_and_invent_refusal() -> None:
    assert package_resource_exists()
    text = load_system_instructions_en()
    assert "English" in text or "EN" in text or "Do not invent" in text
    assert_not_interview_ssot(text)
    assert "InterviewEngine" not in text
    assert "dogestonia_instructions" not in text
    proposed = {"agency": "Invented Agency LLC", "address": "Nowhere 1"}
    try:
        refuse_invented_civic_facts(INSUFFICIENT_CORPUS, proposed)
        raise AssertionError("expected invent refusal")
    except BriefFailure as exc:
        assert exc.failure_class == BriefFailureClass.BRIEF_GENERATION_FAILED


def test_ac_09_06_idempotent_same_version_and_bump_distinguishable() -> None:
    client = isolation_client()
    headers = worker_auth_headers()
    body = accept_body(issue_id="issue-50-idem", generation_version="v1")
    r1 = client.post(WORKER_ACCEPT_PATH, json=body, headers=headers)
    r2 = client.post(WORKER_ACCEPT_PATH, json=body, headers=headers)
    assert r1.status_code == 200 and r2.status_code == 200
    assert r1.json()["idempotent"] is False
    assert r2.json()["idempotent"] is True
    assert r2.json()["status"] == r1.json()["status"]

    r3 = client.post(
        WORKER_ACCEPT_PATH,
        json=accept_body(issue_id="issue-50-idem", generation_version="v2"),
        headers=headers,
    )
    assert r3.status_code == 200
    assert r3.json()["idempotent"] is False
    d1, d3 = r1.json(), r3.json()
    assert regenerate_assets_distinguishable(
        version_a=d1["generation_version"],
        version_b=d3["generation_version"],
        url_a=d1["poster_url"],
        url_b=d3["poster_url"],
    )
