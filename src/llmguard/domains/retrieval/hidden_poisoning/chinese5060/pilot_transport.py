"""Provider-compatible JSON codec and in-memory, single-attempt fake transport."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .pilot_admission import INPUT_CAP, MODEL, OUTPUT_CAP, Stop, json_bytes, strict_json, token_int

# Candidate wire only. max_tokens limits visible output when thinking is off.
# Endpoint-specific acceptance and billing are still WIRE_UNVERIFIED.
WIRE_PATH = "/compatible-mode/v1/chat/completions"


def encode(messages: list[dict[str, str]]) -> bytes:
    return json_bytes({
        "model": MODEL, "messages": messages, "temperature": 0, "top_p": 1,
        "enable_thinking": False, "enable_search": False, "stream": False,
        "max_tokens": OUTPUT_CAP, "response_format": {"type": "json_object"},
    })


class LiveTransport:
    def __init__(self, *, approval: object = None) -> None:
        # A new Owner decision and reviewed activation are required in a later phase.
        # No credentials, SDK or socket implementation are reachable in this build.
        raise Stop("LIVE_NOT_AUTHORIZED")


@dataclass(frozen=True)
class Reply:
    status_code: int
    body: bytes
    # Only this typed, non-header field is retained, never authorization/cookies.
    provider_request_id: str | None = None


class FakeTransport:
    """Exactly one deterministic reply per cell, with optional synthetic failures."""
    automatic_retries = 0

    def __init__(self, faults: dict[int, str] | None = None) -> None:
        self.faults = faults or {}
        self.attempts = 0

    def send(self, body: bytes, input_tokens: int) -> Reply:
        self.attempts += 1
        fault = self.faults.get(self.attempts)
        request = strict_json(body)
        citations = [c["id"] for c in strict_json(request["messages"][1]["content"])["context"]]
        response: dict[str, Any] = {
            "model": MODEL,
            "usage": {"prompt_tokens": input_tokens, "completion_tokens": 18, "total_tokens": input_tokens + 18,
                      "prompt_tokens_details": {"cached_tokens": min(input_tokens, 16)},
                      "completion_tokens_details": {"reasoning_tokens": 0}},
            "choices": [{"index": 0, "finish_reason": "stop", "message": {
                "role": "assistant", "content": json_bytes({
                    "status": "ANSWER", "answer": "SYNTHETIC_FIXTURE_ONLY", "citations": citations[:1],
                }).decode().strip(),
            }}],
        }
        if fault == "timeout":
            raise TimeoutError
        if fault == "http":
            return Reply(429, b'{"error":{"message":"SYNTHETIC_RATE_LIMIT"}}')
        if fault == "missing_usage":
            del response["usage"]
        if fault == "model":
            response["model"] = "unapproved-alias"
        if fault == "non_json":
            response["choices"][0]["message"]["content"] = "SYNTHETIC_NOT_JSON"
        if fault == "empty":
            response["choices"][0]["message"]["content"] = ""
        if fault == "citation":
            response["choices"][0]["message"]["content"] = '{"status":"ANSWER","answer":"mock","citations":["C99"]}'
        if fault == "length":
            response["choices"][0]["finish_reason"] = "length"
        if fault == "hidden":
            response["usage"]["completion_tokens_details"]["reasoning_tokens"] = 2
        if fault == "tool":
            response["choices"][0]["message"]["tool_calls"] = [{"id": "fake"}]
        if fault == "usage_over":
            response["usage"]["completion_tokens"] = OUTPUT_CAP + 1
            response["usage"]["total_tokens"] = input_tokens + OUTPUT_CAP + 1
        if fault == "usage_drift":
            response["usage"]["prompt_tokens"] += 1
            response["usage"]["total_tokens"] += 1
        return Reply(200, json_bytes(response), f"FAKE-{self.attempts:03d}")


@dataclass(frozen=True)
class Usage:
    prompt: int
    cached: int | None
    output: int
    reasoning: int | None

    def record(self) -> dict[str, int | None]:
        return {"input_tokens": self.prompt, "cached_input_tokens": self.cached,
                "output_tokens": self.output, "hidden_reasoning_tokens": self.reasoning}


def _details(value: Any, allowed: set[str]) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict) or set(value) - allowed:
        raise Stop("USAGE_UNVERIFIED_DETAIL")
    return value


def parse_usage(response: Any, expected_input: int, *, output_cap: int = OUTPUT_CAP) -> Usage:
    if not isinstance(response, dict) or response.get("model") != MODEL:
        raise Stop("RETURNED_MODEL_MISMATCH")
    if response.get("error") is not None:
        raise Stop("PROVIDER_ERROR_ENVELOPE")
    usage = response.get("usage")
    required = {"prompt_tokens", "completion_tokens", "total_tokens"}
    if not isinstance(usage, dict) or not required <= set(usage):
        raise Stop("USAGE_MISSING")
    if set(usage) - (required | {"prompt_tokens_details", "completion_tokens_details"}):
        raise Stop("USAGE_UNKNOWN_BILLABLE_FIELD")
    prompt = token_int(usage["prompt_tokens"])
    output = token_int(usage["completion_tokens"])
    if not 0 < prompt <= INPUT_CAP or not 0 < output <= output_cap:
        raise Stop("USAGE_TOKEN_CAP_EXCEEDED")
    if prompt != expected_input or token_int(usage["total_tokens"]) != prompt + output:
        raise Stop("USAGE_TOKEN_DRIFT")
    details_in = _details(usage.get("prompt_tokens_details"),
                          {"cached_tokens", "text_tokens", "audio_tokens", "image_tokens", "video_tokens",
                           "cache_creation", "cache_creation_input_tokens", "cache_type"})
    details_out = _details(usage.get("completion_tokens_details"),
                           {"reasoning_tokens", "text_tokens", "audio_tokens"})
    if any(details.get(field) is not None and token_int(details[field]) != 0
           for details, field in ((details_in, "audio_tokens"), (details_in, "image_tokens"),
                                  (details_in, "video_tokens"), (details_out, "audio_tokens"),
                                  (details_in, "cache_creation_input_tokens"))):
        raise Stop("USAGE_UNEXPECTED_MODALITY_OR_CACHE_WRITE")
    if details_in.get("cache_creation") is not None or details_in.get("cache_type") is not None:
        raise Stop("USAGE_EXPLICIT_CACHE_UNAPPROVED")
    for details, limit in ((details_in, prompt), (details_out, output)):
        text = details.get("text_tokens")
        if text is not None and token_int(text) != limit:
            raise Stop("USAGE_TEXT_DETAIL_DRIFT")
    cached_raw = details_in.get("cached_tokens")
    reasoning_raw = details_out.get("reasoning_tokens")
    cached = None if cached_raw is None else token_int(cached_raw)
    reasoning = None if reasoning_raw is None else token_int(reasoning_raw)
    if (cached is not None and cached > prompt) or reasoning:
        raise Stop("USAGE_CACHE_OR_REASONING_VIOLATION")
    return Usage(prompt, cached, output, reasoning)


def parse_answer(response: Any, allowed_citations: tuple[str, ...]) -> str:
    choices = response.get("choices")
    if not isinstance(choices, list) or len(choices) != 1 or not isinstance(choices[0], dict):
        raise Stop("RESPONSE_CHOICE_COUNT")
    choice = choices[0]
    if choice.get("finish_reason") != "stop":
        raise Stop("RESPONSE_NOT_COMPLETE")
    message = choice.get("message")
    if not isinstance(message, dict) or message.get("role") != "assistant":
        raise Stop("RESPONSE_ROLE_INVALID")
    if set(message) - {"role", "content", "reasoning_content", "refusal", "function_call", "tool_calls"}:
        raise Stop("RESPONSE_UNKNOWN_MESSAGE_FIELD")
    if any(message.get(k) not in (None, "", []) for k in (
        "reasoning_content", "refusal", "function_call", "tool_calls"
    )):
        raise Stop("RESPONSE_UNAPPROVED_REASONING_TOOL_OR_REFUSAL")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise Stop("RESPONSE_EMPTY")
    answer = strict_json(content)
    if not isinstance(answer, dict) or set(answer) != {"status", "answer", "citations"}:
        raise Stop("ANSWER_SCHEMA")
    text, cites = answer["answer"], answer["citations"]
    if not isinstance(text, str) or not isinstance(cites, list) or any(not isinstance(c, str) for c in cites):
        raise Stop("ANSWER_SCHEMA")
    if answer["status"] == "ABSTAIN" and text == "" and cites == []:
        return "ABSTAIN"
    if answer["status"] != "ANSWER" or not text.strip():
        raise Stop("ANSWER_SCHEMA")
    if not cites or len(set(cites)) != len(cites) or any(c not in allowed_citations for c in cites):
        raise Stop("ANSWER_INVALID_CITATIONS")
    return "ANSWER"
