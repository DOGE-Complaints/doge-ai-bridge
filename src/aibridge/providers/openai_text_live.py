"""Worker-scoped OpenAI text brief extract from gateway ``{stories:[…]}``.

Uses a dedicated Responses client (not channel InterviewEngine / L10-1).
HTTP transport is injectable — tests must not require live credentials.
"""

from __future__ import annotations

import json
from typing import Any, Callable

from aibridge.responses_client import (
    HttpxResponsesTransport,
    ProductionResponsesClient,
    ResponsesHttpTransport,
    ResponsesRequest,
    ResponsesTransportError,
)
from aibridge.sense_brief.errors import BriefFailure, BriefFailureClass
from aibridge.sense_brief.model import SenseBrief
from aibridge.sense_brief.prompts import assert_not_interview_ssot, load_system_instructions_en

_L2_JSON_SCHEMA_HINT = (
    "Return ONLY a JSON object with keys: title (≤80 chars), "
    "summary {et, ru, en}, problem, context, severity, audience, "
    "desired_outcome, evidence_refs (string array). "
    "Ground every field in the stories corpus; do not invent civic facts."
)


def stories_from_corpus(corpus: Any) -> list[Any]:
    """Extract ``stories`` list or raise corpus_insufficient."""
    if corpus is None or not isinstance(corpus, dict):
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "corpus must be an object with stories",
        )
    stories = corpus.get("stories")
    if stories is None:
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "corpus missing stories",
        )
    if not isinstance(stories, list):
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "stories must be a list",
        )
    if not stories:
        raise BriefFailure(
            BriefFailureClass.CORPUS_INSUFFICIENT,
            "stories empty",
        )
    return stories


def _brief_from_reply_text(text: str) -> SenseBrief:
    raw = (text or "").strip()
    if not raw:
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "empty OpenAI text brief reply",
        )
    # Tolerate fenced markdown from models.
    if raw.startswith("```"):
        lines = raw.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        raw = "\n".join(lines).strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            f"OpenAI brief reply is not JSON: {exc}",
        ) from exc
    if not isinstance(data, dict):
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "OpenAI brief reply must be a JSON object",
        )
    try:
        brief = SenseBrief.model_validate(data)
    except Exception as exc:  # noqa: BLE001
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            f"OpenAI brief failed L2 validation: {exc}",
        ) from exc
    if not brief.satisfies_l2():
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "OpenAI brief failed L2 checks",
        )
    return brief


def _build_responses_payload(*, model: str, stories: list[Any]) -> dict[str, Any]:
    instructions = load_system_instructions_en()
    assert_not_interview_ssot(instructions)
    user = (
        f"{_L2_JSON_SCHEMA_HINT}\n\n"
        f"stories corpus JSON:\n{json.dumps({'stories': stories}, ensure_ascii=False)}"
    )
    return {
        "model": model,
        "store": False,
        "parallel_tool_calls": False,
        "instructions": instructions,
        "input": [
            {
                "role": "user",
                "content": [{"type": "input_text", "text": user}],
            }
        ],
    }


InvokeFn = Callable[[dict[str, Any]], dict[str, Any]]


def extract_brief_from_stories(
    corpus: Any,
    *,
    text_brief_model: str,
    api_key: str,
    transport: ResponsesHttpTransport | None = None,
    invoke: InvokeFn | None = None,
    timeout_ms: int = 30_000,
    connect_timeout_ms: int = 5_000,
) -> SenseBrief:
    """Live extract L2 SenseBrief from gateway stories via OpenAI Responses.

    ``invoke`` (tests) or ``transport`` may be supplied so CI never needs live keys.
    """
    if not (text_brief_model or "").strip():
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "text-brief model slot unset",
        )
    if not (api_key or "").strip():
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            "OPENAI_API_KEY missing for openai text provider",
        )
    stories = stories_from_corpus(corpus)
    payload = _build_responses_payload(model=text_brief_model.strip(), stories=stories)

    try:
        if invoke is not None:
            engine = invoke(payload)
        else:
            client = ProductionResponsesClient(
                api_key=api_key.strip(),
                model=text_brief_model.strip(),
                timeout_ms=timeout_ms,
                connect_timeout_ms=connect_timeout_ms,
                transport=transport or HttpxResponsesTransport(),
            )
            engine = client.create(ResponsesRequest(payload=payload))
    except BriefFailure:
        raise
    except ResponsesTransportError as exc:
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            f"OpenAI text brief transport failed: {exc.outcome}",
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise BriefFailure(
            BriefFailureClass.BRIEF_GENERATION_FAILED,
            f"OpenAI text brief invoke failed: {exc}",
        ) from exc

    reply = ""
    if isinstance(engine, dict):
        parsed = engine.get("aibridge_parsed")
        if isinstance(parsed, dict):
            reply = str(parsed.get("reply_text") or "")
        if not reply:
            # Fallback: scan output_text parts like RecordingResponsesClient.
            for item in engine.get("output") or []:
                if not isinstance(item, dict):
                    continue
                for part in item.get("content") or []:
                    if isinstance(part, dict) and part.get("type") == "output_text":
                        reply = str(part.get("text") or "")
                        break
                if reply:
                    break
    return _brief_from_reply_text(reply)
