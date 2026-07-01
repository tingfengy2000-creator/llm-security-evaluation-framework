import argparse
import copy
import json
import os
import threading
import time
import uuid
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import openai

from guard_proxy import (
    DEFAULT_UPSTREAM_BASE_URL,
    MAX_BODY_BYTES,
    REFUSAL_TEXT,
    UPSTREAM_STRIPPED_FIELDS,
    GuardEngine,
    bounded_preview,
    extract_text,
    openai_error,
    text_sha256,
    upstream_error_details,
)


EXPERIMENT_MODES = {
    "passthrough": {
        "internal_mode": "passthrough",
        "input_guard_enabled": False,
        "output_guard_enabled": False,
    },
    "input-only": {
        "internal_mode": "input-only",
        "input_guard_enabled": True,
        "output_guard_enabled": False,
    },
    "output-only": {
        "internal_mode": "output-only",
        "input_guard_enabled": False,
        "output_guard_enabled": True,
    },
    "full-guard": {
        "internal_mode": "guarded",
        "input_guard_enabled": True,
        "output_guard_enabled": True,
    },
}

REQUIRED_LOG_FIELDS = {
    "experiment_name",
    "internal_mode",
    "input_guard_enabled",
    "output_guard_enabled",
    "upstream_called",
    "input_blocked",
    "output_blocked",
    "final_decision",
    "original_model_output_hash",
}


class AblationProxyService:
    def __init__(
        self,
        client,
        experiment_name,
        log_path=None,
        default_model="llama-3.1-8b-instant",
        engine=None,
    ):
        if experiment_name not in EXPERIMENT_MODES:
            raise ValueError(f"unsupported experiment: {experiment_name}")
        self.client = client
        self.experiment_name = experiment_name
        self.config = EXPERIMENT_MODES[experiment_name]
        self.log_path = Path(log_path) if log_path else None
        self.default_model = default_model
        self.engine = engine or GuardEngine()
        self._log_lock = threading.Lock()

    @property
    def internal_mode(self):
        return self.config["internal_mode"]

    @property
    def input_guard_enabled(self):
        return self.config["input_guard_enabled"]

    @property
    def output_guard_enabled(self):
        return self.config["output_guard_enabled"]

    @staticmethod
    def _completion(model, content):
        prompt_tokens = 0
        completion_tokens = len(content.split())
        return {
            "id": f"chatcmpl-ablation-{uuid.uuid4().hex}",
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
            "experiment_name": self.experiment_name,
            "internal_mode": self.internal_mode,
            "model": model,
            "prompt_sha256": text_sha256(prompt),
            "prompt_preview": bounded_preview(prompt),
            "input_guard_enabled": self.input_guard_enabled,
            "output_guard_enabled": self.output_guard_enabled,
            "input_matches": [],
            "input_blocked": False,
            "upstream_called": False,
            "upstream_request_id": None,
            "stripped_upstream_fields": [],
            "original_model_output_hash": None,
            "original_model_output_length": None,
            "output_matches": [],
            "output_blocked": False,
            "final_output_hash": None,
            "final_output_summary": None,
            "final_decision": None,
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
            request_id or f"ablation-{uuid.uuid4().hex}",
            model,
            prompt,
        )

        input_decision = self.engine.inspect_input(prompt)
        record["input_matches"] = input_decision.matches
        if self.input_guard_enabled and input_decision.blocked:
            response = self._completion(model, REFUSAL_TEXT)
            record["input_blocked"] = True
            record["final_decision"] = "input_block"
            record["final_output_hash"] = text_sha256(REFUSAL_TEXT)
            record["final_output_summary"] = "local_refusal"
            record["latency_ms"] = round(
                (time.perf_counter() - started) * 1000,
                3,
            )
            return 200, response, record

        upstream_payload, stripped = self._sanitize_upstream_payload(payload)
        record["stripped_upstream_fields"] = stripped
        record["upstream_called"] = True
        try:
            upstream_response = self.client.chat.completions.create(
                **upstream_payload
            )
        except openai.APIStatusError as exc:
            setattr(exc, "_ablation_record", record)
            raise

        record["upstream_request_id"] = getattr(
            upstream_response,
            "_request_id",
            None,
        )
        response = upstream_response.model_dump(mode="json")
        original_output = self._assistant_text(response)
        record["original_model_output_hash"] = text_sha256(original_output)
        record["original_model_output_length"] = len(original_output)

        output_decision = self.engine.inspect_output(original_output)
        record["output_matches"] = output_decision.matches
        if self.output_guard_enabled and output_decision.blocked:
            response = copy.deepcopy(response)
            response["choices"][0]["message"]["content"] = REFUSAL_TEXT
            response["choices"][0]["finish_reason"] = "stop"
            final_output = REFUSAL_TEXT
            record["output_blocked"] = True
            record["final_decision"] = "output_block"
            record["final_output_summary"] = "local_refusal"
        else:
            final_output = original_output
            record["final_decision"] = "allow"
            record["final_output_summary"] = "upstream_allowed"

        record["final_output_hash"] = text_sha256(final_output)
        record["latency_ms"] = round((time.perf_counter() - started) * 1000, 3)
        return 200, response, record

    def error_record(self, request_id, error_type, started=None):
        record = self._base_record(
            request_id,
            self.default_model,
            "",
        )
        record["prompt_sha256"] = None
        record["prompt_preview"] = ""
        record["final_decision"] = "error"
        record["error_type"] = error_type
        if started is not None:
            record["latency_ms"] = round(
                (time.perf_counter() - started) * 1000,
                3,
            )
        return record

    def write_log(self, record):
        if self.log_path is None:
            return
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        line = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        with self._log_lock:
            with self.log_path.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(line + "\n")


class AblationGuardProxyHandler(BaseHTTPRequestHandler):
    server_version = "Stage41AblationGuardProxy/1.0"

    def _send_json(self, status, payload):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        service = self.server.service
        if self.path.rstrip("/") == "/health":
            self._send_json(
                200,
                {
                    "status": "ok",
                    "experiment_name": service.experiment_name,
                    "internal_mode": service.internal_mode,
                    "input_guard_enabled": service.input_guard_enabled,
                    "output_guard_enabled": service.output_guard_enabled,
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
                            "id": service.default_model,
                            "object": "model",
                        }
                    ],
                },
            )
            return
        self._send_json(404, openai_error(404, "not found", "not_found"))

    def do_POST(self):
        service = self.server.service
        request_id = f"ablation-{uuid.uuid4().hex}"
        started = time.perf_counter()
        if self.path.rstrip("/") != "/v1/chat/completions":
            record = service.error_record(request_id, "not_found", started)
            service.write_log(record)
            self._send_json(404, openai_error(404, "not found", "not_found"))
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > MAX_BODY_BYTES:
                raise ValueError("invalid request body size")
            raw = self.rfile.read(length)
            payload = json.loads(raw.decode("utf-8"))
            status, response, record = service.process_chat(
                payload,
                request_id=request_id,
            )
            service.write_log(record)
            self._send_json(status, response)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as exc:
            record = service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            service.write_log(record)
            self._send_json(
                400,
                openai_error(400, str(exc), "invalid_request"),
            )
        except openai.APIStatusError as exc:
            status = int(getattr(exc, "status_code", 502) or 502)
            details = upstream_error_details(exc)
            record = getattr(
                exc,
                "_ablation_record",
                service.error_record(request_id, type(exc).__name__, started),
            )
            record["upstream_called"] = True
            record["final_decision"] = "error"
            record["error_type"] = type(exc).__name__
            record["upstream_error_message"] = details["message"]
            record["upstream_error_type"] = details["type"]
            record["upstream_error_code"] = details["code"]
            record["latency_ms"] = round(
                (time.perf_counter() - started) * 1000,
                3,
            )
            service.write_log(record)
            self._send_json(
                status,
                openai_error(
                    status,
                    (
                        f"upstream Groq request failed with HTTP {status}: "
                        f"{details['message']}"
                    ),
                    "upstream_error",
                ),
            )
        except (openai.APIConnectionError, openai.APITimeoutError) as exc:
            record = service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            record["upstream_called"] = True
            service.write_log(record)
            self._send_json(
                502,
                openai_error(
                    502,
                    "upstream Groq connection failed",
                    "upstream_connection_error",
                ),
            )
        except Exception as exc:
            record = service.error_record(
                request_id,
                type(exc).__name__,
                started,
            )
            service.write_log(record)
            self._send_json(
                500,
                openai_error(500, "ablation proxy internal error", "internal_error"),
            )

    def log_message(self, fmt, *args):
        return


def main():
    parser = argparse.ArgumentParser(
        description="Stage 4.1 OpenAI-compatible guard ablation proxy"
    )
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8011)
    parser.add_argument(
        "--experiment-name",
        choices=tuple(EXPERIMENT_MODES),
        required=True,
    )
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
    service = AblationProxyService(
        client=client,
        experiment_name=args.experiment_name,
        log_path=args.log_path,
        default_model=args.model,
    )
    server = ThreadingHTTPServer((args.host, args.port), AblationGuardProxyHandler)
    server.service = service
    print(
        f"Stage 4.1 ablation proxy listening on "
        f"http://{args.host}:{args.port}/v1 "
        f"experiment={args.experiment_name} "
        f"internal={service.internal_mode}",
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
