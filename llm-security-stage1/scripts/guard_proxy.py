import argparse
import base64
import copy
import hashlib
import json
import os
import re
import threading
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import openai


DEFAULT_UPSTREAM_BASE_URL = "https://api.groq.com/openai/v1"
SUPPORTED_MODES = ("passthrough", "input-only", "output-only", "guarded")
REFUSAL_TEXT = (
    "I cannot process this request because it conflicts with the local "
    "security policy."
)
MAX_BODY_BYTES = 2 * 1024 * 1024
PREVIEW_LIMIT = 240

UPSTREAM_STRIPPED_FIELDS = {
    "frequency_penalty",
    "logit_bias",
    "logprobs",
    "n",
    "presence_penalty",
    "top_logprobs",
}


@dataclass
class GuardDecision:
    blocked: bool
    matches: list[str] = field(default_factory=list)
    decoded_payloads: list[str] = field(default_factory=list)


def extract_text(messages):
    parts = []
    for message in messages or []:
        if not isinstance(message, dict):
            continue
        content = message.get("content", "")
        if isinstance(content, str):
            parts.append(content)
        elif isinstance(content, list):
            for item in content:
                if (
                    isinstance(item, dict)
                    and item.get("type", "text") == "text"
                    and isinstance(item.get("text"), str)
                ):
                    parts.append(item["text"])
    return "\n".join(parts)


def text_sha256(text):
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def bounded_preview(text, limit=PREVIEW_LIMIT):
    normalized = text.replace("\r", "\\r").replace("\n", "\\n")
    return normalized[:limit]


def _sanitize_diagnostic_text(value, limit=500):
    text = str(value or "")
    text = re.sub(
        r"\bgsk_[A-Za-z0-9_-]+\b",
        "[REDACTED]",
        text,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r"\bBearer\s+\S+",
        "Bearer [REDACTED]",
        text,
        flags=re.IGNORECASE,
    )
    return text[:limit]


def upstream_error_details(exc):
    body = getattr(exc, "body", None)
    error = body.get("error", body) if isinstance(body, dict) else {}
    if not isinstance(error, dict):
        error = {}
    return {
        "message": _sanitize_diagnostic_text(
            error.get("message") or "No upstream error message returned."
        ),
        "type": _sanitize_diagnostic_text(error.get("type"), limit=100),
        "code": _sanitize_diagnostic_text(error.get("code"), limit=100),
    }


class GuardEngine:
    INPUT_RULES = (
        (
            "prompt_injection.ignore_previous",
            re.compile(
                r"\b(ignore|disregard|forget)\b.{0,50}"
                r"\b(previous|prior|above|following)\b.{0,30}"
                r"\b(instruction|instructions|rules?|prompt)?\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
        (
            "prompt_injection.nevermind",
            re.compile(r"\bnever\s*mind\b|\bnevermind\b", re.IGNORECASE),
        ),
        (
            "prompt_injection.system_prompt",
            re.compile(
                r"\b(reveal|show|print|repeat|extract)\b.{0,40}"
                r"\b(system|developer)\s+(prompt|message|instructions?)\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
        (
            "jailbreak.developer_mode",
            re.compile(r"\bdeveloper\s+mode\b", re.IGNORECASE),
        ),
        (
            "jailbreak.dan",
            re.compile(r"\bDAN\b|\bdo\s+anything\s+now\b", re.IGNORECASE),
        ),
        (
            "jailbreak.bypass_safety",
            re.compile(
                r"\b(bypass|disable|remove|ignore)\b.{0,40}"
                r"\b(safety|policy|guardrails?|restrictions?)\b",
                re.IGNORECASE | re.DOTALL,
            ),
        ),
    )

    ENCODED_DANGER_RULES = (
        re.compile(r"<\s*script\b", re.IGNORECASE),
        re.compile(r"\bjavascript\s*:", re.IGNORECASE),
        re.compile(r"\balert\s*\(", re.IGNORECASE),
        re.compile(r"<\?php\b", re.IGNORECASE),
        re.compile(
            r"\b(ignore|disregard|forget)\b.{0,50}\b(instructions?|rules?)\b",
            re.IGNORECASE | re.DOTALL,
        ),
    )

    OUTPUT_RULES = (
        (
            "output.rogue_hate_string",
            re.compile(r"\bI\s+hate\s+humans\b", re.IGNORECASE),
        ),
        (
            "output.script_payload",
            re.compile(
                r"<\s*script\b|\bjavascript\s*:|\balert\s*\(|<\?php\b",
                re.IGNORECASE,
            ),
        ),
        (
            "output.prompt_leakage",
            re.compile(
                r"\b(system|developer)\s+(prompt|message)\s+(is|says|contains)\b",
                re.IGNORECASE,
            ),
        ),
    )

    BASE64_TOKEN = re.compile(
        r"(?<![A-Za-z0-9+/])([A-Za-z0-9+/]{16,}={0,2})(?![A-Za-z0-9+/=])"
    )

    def _decode_base64_candidates(self, text):
        decoded = []
        for token in self.BASE64_TOKEN.findall(text):
            if len(token) % 4 != 0:
                continue
            try:
                raw = base64.b64decode(token, validate=True)
            except (ValueError, base64.binascii.Error):
                continue
            if not raw:
                continue
            candidate = raw.decode("utf-8", errors="replace")
            printable = sum(char.isprintable() or char.isspace() for char in candidate)
            if printable / max(len(candidate), 1) < 0.65:
                continue
            decoded.append(candidate[:2000])
        return decoded

    def inspect_input(self, text):
        matches = [
            rule_name
            for rule_name, pattern in self.INPUT_RULES
            if pattern.search(text)
        ]

        decoded_payloads = self._decode_base64_candidates(text)
        for decoded in decoded_payloads:
            if any(pattern.search(decoded) for pattern in self.ENCODED_DANGER_RULES):
                matches.append("encoding.base64_suspicious")
                break

        matches = list(dict.fromkeys(matches))
        return GuardDecision(
            blocked=bool(matches),
            matches=matches,
            decoded_payloads=decoded_payloads,
        )

    def inspect_output(self, text):
        matches = [
            rule_name
            for rule_name, pattern in self.OUTPUT_RULES
            if pattern.search(text)
        ]
        matches = list(dict.fromkeys(matches))
        return GuardDecision(blocked=bool(matches), matches=matches)


class ProxyService:
    def __init__(
        self,
        client,
        mode,
        log_path=None,
        default_model="llama-3.1-8b-instant",
        engine=None,
    ):
        if mode not in SUPPORTED_MODES:
            raise ValueError(f"unsupported guard mode: {mode}")
        self.client = client
        self.mode = mode
        self.log_path = Path(log_path) if log_path else None
        self.default_model = default_model
        self.engine = engine or GuardEngine()
        self._log_lock = threading.Lock()

    @property
    def input_enforced(self):
        return self.mode in ("input-only", "guarded")

    @property
    def output_enforced(self):
        return self.mode in ("output-only", "guarded")

    def _completion(self, model, content):
        prompt_tokens = 0
        completion_tokens = len(content.split())
        return {
            "id": f"chatcmpl-guard-{uuid.uuid4().hex}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": content},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "total_tokens": prompt_tokens + completion_tokens,
            },
        }

    @staticmethod
    def _assistant_text(response):
        choices = response.get("choices") or []
        if not choices:
            return ""
        message = choices[0].get("message") or {}
        content = message.get("content", "")
        return content if isinstance(content, str) else str(content)

    @staticmethod
    def _sanitize_upstream_payload(payload):
        sanitized = dict(payload)
        sanitized.pop("stream", None)
        stripped = []
        for field_name in sorted(UPSTREAM_STRIPPED_FIELDS):
            if field_name in sanitized:
                stripped.append(field_name)
                sanitized.pop(field_name, None)
        return sanitized, stripped

    def _base_record(self, request_id, model, prompt):
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "mode": self.mode,
            "model": model,
            "prompt_sha256": text_sha256(prompt),
            "prompt_preview": bounded_preview(prompt),
            "input_matches": [],
            "input_action": "allow",
            "upstream_called": False,
            "upstream_request_id": None,
            "stripped_upstream_fields": [],
            "output_sha256": None,
            "output_preview": "",
            "output_matches": [],
            "final_action": None,
            "latency_ms": None,
            "error_type": None,
        }

    def process_chat(self, payload, request_id=None):
        started = time.perf_counter()
        if not isinstance(payload, dict):
            raise ValueError("request body must be a JSON object")
        if payload.get("stream") is True:
            raise ValueError("streaming is not supported by this guard baseline")
        messages = payload.get("messages")
        if not isinstance(messages, list) or not messages:
            raise ValueError("messages must be a non-empty array")

        model = payload.get("model") or self.default_model
        prompt = extract_text(messages)
        record = self._base_record(
            request_id or f"guard-{uuid.uuid4().hex}",
            model,
            prompt,
        )

        input_decision = self.engine.inspect_input(prompt)
        record["input_matches"] = input_decision.matches

        if self.input_enforced and input_decision.blocked:
            response = self._completion(model, REFUSAL_TEXT)
            output = self._assistant_text(response)
            record["input_action"] = "block"
            record["final_action"] = "input_block"
            record["output_sha256"] = text_sha256(output)
            record["output_preview"] = bounded_preview(output)
            record["latency_ms"] = round(
                (time.perf_counter() - started) * 1000,
                3,
            )
            return 200, response, record

        upstream_payload, stripped = self._sanitize_upstream_payload(payload)
        record["stripped_upstream_fields"] = stripped
        record["upstream_called"] = True

        upstream_response = self.client.chat.completions.create(**upstream_payload)
        record["upstream_request_id"] = getattr(
            upstream_response,
            "_request_id",
            None,
        )
        response = upstream_response.model_dump(mode="json")
        output = self._assistant_text(response)
        output_decision = self.engine.inspect_output(output)
        record["output_matches"] = output_decision.matches

        if self.output_enforced and output_decision.blocked:
            response = copy.deepcopy(response)
            response["choices"][0]["message"]["content"] = REFUSAL_TEXT
            response["choices"][0]["finish_reason"] = "stop"
            output = REFUSAL_TEXT
            record["final_action"] = "output_block"
        elif self.mode == "passthrough":
            record["final_action"] = "passthrough"
        else:
            record["final_action"] = "allow"

        record["output_sha256"] = text_sha256(output)
        record["output_preview"] = bounded_preview(output)
        record["latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        return 200, response, record

    def error_record(self, request_id, error_type, started=None):
        elapsed = None
        if started is not None:
            elapsed = round((time.perf_counter() - started) * 1000, 3)
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request_id,
            "mode": self.mode,
            "model": self.default_model,
            "prompt_sha256": None,
            "prompt_preview": "",
            "input_matches": [],
            "input_action": "error",
            "upstream_called": False,
            "upstream_request_id": None,
            "stripped_upstream_fields": [],
            "output_sha256": None,
            "output_preview": "",
            "output_matches": [],
            "final_action": "error",
            "latency_ms": elapsed,
            "error_type": error_type,
        }

    def write_log(self, record):
        if self.log_path is None:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        with self._log_lock:
            with self.log_path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(line + "\n")


def openai_error(status, message, code):
    return {
        "error": {
            "message": message,
            "type": "guard_proxy_error",
            "param": None,
            "code": code,
        }
    }


class GuardProxyHandler(BaseHTTPRequestHandler):
    server_version = "Stage4GuardProxy/1.0"

    def _send_json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path.rstrip("/") == "/health":
            self._send_json(
                200,
                {
                    "status": "ok",
                    "mode": self.server.service.mode,
                    "upstream": DEFAULT_UPSTREAM_BASE_URL,
                },
            )
            return
        if self.path.rstrip("/") == "/v1/models":
            self._send_json(
                200,
                {
                    "object": "list",
                    "data": [
                        {
                            "id": self.server.service.default_model,
                            "object": "model",
                        }
                    ],
                },
            )
            return
        self._send_json(404, openai_error(404, "not found", "not_found"))

    def do_POST(self):
        request_id = f"guard-{uuid.uuid4().hex}"
        started = time.perf_counter()
        if self.path.rstrip("/") != "/v1/chat/completions":
            record = self.server.service.error_record(
                request_id,
                "not_found",
                started,
            )
            self.server.service.write_log(record)
            self._send_json(404, openai_error(404, "not found", "not_found"))
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError("invalid request body size")
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            status, response, record = self.server.service.process_chat(
                payload,
                request_id=request_id,
            )
            self.server.service.write_log(record)
            self._send_json(status, response)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
            record = self.server.service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            self.server.service.write_log(record)
            self._send_json(
                400,
                openai_error(400, str(exc), "invalid_request"),
            )
        except openai.APIStatusError as exc:
            status = int(getattr(exc, "status_code", 502) or 502)
            details = upstream_error_details(exc)
            record = self.server.service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            record["upstream_called"] = True
            record["upstream_error_message"] = details["message"]
            record["upstream_error_type"] = details["type"]
            record["upstream_error_code"] = details["code"]
            self.server.service.write_log(record)
            detail_suffix = (
                f": {details['message']}" if details["message"] else ""
            )
            self._send_json(
                status,
                openai_error(
                    status,
                    (
                        f"upstream Groq request failed with HTTP {status}"
                        f"{detail_suffix}"
                    ),
                    "upstream_error",
                ),
            )
        except (openai.APIConnectionError, openai.APITimeoutError) as exc:
            record = self.server.service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            record["upstream_called"] = True
            self.server.service.write_log(record)
            self._send_json(
                502,
                openai_error(
                    502,
                    "upstream Groq connection failed",
                    "upstream_connection_error",
                ),
            )
        except Exception as exc:
            record = self.server.service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            self.server.service.write_log(record)
            self._send_json(
                500,
                openai_error(500, "guard proxy internal error", "internal_error"),
            )

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser(
        description="Stage 4 OpenAI-compatible rule-based guard proxy"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument("--mode", choices=SUPPORTED_MODES, default="guarded")
    parser.add_argument("--log-path", required=True)
    parser.add_argument("--model", default="llama-3.1-8b-instant")
    parser.add_argument(
        "--upstream-base-url",
        default=DEFAULT_UPSTREAM_BASE_URL,
    )
    args = parser.parse_args()

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        parser.error("GROQ_API_KEY is required")

    client = openai.OpenAI(
        api_key=api_key,
        base_url=args.upstream_base_url,
    )
    service = ProxyService(
        client=client,
        mode=args.mode,
        log_path=args.log_path,
        default_model=args.model,
    )
    server = ThreadingHTTPServer((args.host, args.port), GuardProxyHandler)
    server.service = service
    print(
        f"Stage 4 guard proxy listening on "
        f"http://{args.host}:{args.port}/v1 mode={args.mode}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
