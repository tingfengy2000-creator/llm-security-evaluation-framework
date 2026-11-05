from __future__ import annotations

import io
import json
import socket
from collections import Counter
from pathlib import Path
from time import monotonic
from typing import Any

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060 import pilot_live_transport as wire
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_admission import Stop, json_bytes
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_design import messages
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_live_stage import StageProgress
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.pilot_transport import FakeTransport, Reply, encode

HOST = "fixture.cn-beijing.maas.aliyuncs.com"
BODY = encode(messages("synthetic", [{"id": "C1", "text": "synthetic"}]))


@pytest.mark.parametrize("host", [
    "fixture.cn-beijing.maas.aliyuncs.com.example.org", "https://" + HOST, HOST + ":443",
    "fixture.ap-southeast-1.maas.aliyuncs.com", "nested.fixture.cn-beijing.maas.aliyuncs.com",
])
def test_host_must_be_official_in_exact_region(host: str) -> None:
    with pytest.raises(Stop, match="HOST_NOT_IN_OFFICIAL_REGION"):
        wire.verify_host("cn-beijing", host)
    wire.verify_host("cn-beijing", HOST)


def test_conditional_transport_refuses_before_endpoint_or_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DASHSCOPE_API_KEY", "SYNTHETIC")
    with pytest.raises(Stop, match="LIVE_DENIAL_WHEN_GATE_FAILED"):
        wire.ConditionalLiveTransport("cn-beijing", HOST)


class Peer:
    def __init__(self, status: bytes, content: bytes, length: int | None = None) -> None:
        size = len(content) if length is None else length
        self.read = io.BytesIO(b"HTTP/1.1 " + status + b"\r\nConnection: close\r\nContent-Length: "
                               + str(size).encode() + b"\r\nX-Request-ID: SYNTHETIC\r\n\r\n" + content)
        self.writes: list[bytes] = []
        self.connects: list[Any] = []
        self.timeouts: list[float] = []
        self.sni: str | None = None

    def __enter__(self) -> Peer:
        return self

    def __exit__(self, *_: object) -> None:
        pass

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)

    def connect(self, address: Any) -> None:
        self.connects.append(address)

    def wrap_socket(self, tcp: Peer, *, server_hostname: str, do_handshake_on_connect: bool) -> Peer:
        assert tcp is self and do_handshake_on_connect is False
        self.sni = server_hostname
        return self

    def do_handshake(self) -> None:
        assert self.sni == HOST

    def sendall(self, data: bytes) -> None:
        self.writes.append(data)

    def recv_into(self, buffer: Any) -> int:
        return self.read.readinto(buffer)


def patch_peer(monkeypatch: pytest.MonkeyPatch, peer: Peer) -> None:
    def resolve(scope: Any, deadline: float) -> tuple[int, int, tuple[str, int]]:
        assert scope.host == HOST and 0 < deadline - monotonic() <= 10
        return socket.AF_INET, socket.IPPROTO_TCP, ("192.0.2.1", 443)

    monkeypatch.setattr(wire, "_resolve", resolve)
    monkeypatch.setattr(wire, "_tls_context", lambda: peer)
    monkeypatch.setattr(wire.socket, "socket", lambda *_: peer)


@pytest.mark.parametrize(("status", "expected"), [(b"200 OK", 200), (b"307 Redirect", 307)])
def test_one_post_bytes_sni_deadlines_and_no_redirect(
    monkeypatch: pytest.MonkeyPatch, status: bytes, expected: int,
) -> None:
    peer = Peer(status, b"synthetic")
    patch_peer(monkeypatch, peer)
    monkeypatch.setenv("HTTPS_PROXY", "http://synthetic.invalid")
    result = wire._exchange("cn-beijing", HOST, BODY, "SYNTHETIC")
    assert result == Reply(expected, b"synthetic", "SYNTHETIC")
    assert len(peer.connects) == len(peer.writes) == 1
    header, body = peer.writes[0].split(b"\r\n\r\n", maxsplit=1)
    assert header.startswith(b"POST /compatible-mode/v1/chat/completions HTTP/1.1\r\n")
    assert f"Host: {HOST}".encode() in header
    assert body == BODY and peer.sni == HOST
    assert max(peer.timeouts[:3]) <= 10 and max(peer.timeouts) <= 60


def test_short_response_preserves_partial_bytes(monkeypatch: pytest.MonkeyPatch) -> None:
    peer = Peer(b"200 OK", b"short", length=10)
    patch_peer(monkeypatch, peer)
    with pytest.raises(wire.InterruptedResponse) as caught:
        wire._exchange("cn-beijing", HOST, BODY, "SYNTHETIC")
    assert caught.value.partial == b"short"
    assert len(peer.writes) == 1


def test_socket_audit_scope_only_host_and_address() -> None:
    with pytest.raises(PermissionError):
        wire._socket_audit("socket.getaddrinfo", (HOST, 443))
    with wire._network_scope(wire._SocketScope(HOST, ("192.0.2.1", 443))):
        wire._socket_audit("socket.getaddrinfo", (HOST, 443))
        wire._socket_audit("socket.connect", (None, ("192.0.2.1", 443)))
        for event, args in (
            ("socket.getaddrinfo", ("fixture.invalid", 443)),
            ("socket.getaddrinfo", (HOST, 80)),
            ("socket.connect", (None, ("192.0.2.2", 443))),
            ("socket.bind", (None, ("192.0.2.1", 443))),
        ):
            with pytest.raises(PermissionError):
                wire._socket_audit(event, args)


@pytest.mark.parametrize(("fault", "position", "code"), [
    ("timeout", 1, "TIMEOUT"),
    ("missing_usage", 3, "USAGE_MISSING"),
    ("model", 4, "RETURNED_MODEL_MISMATCH"),
    ("non_json", 4, "INVALID_JSON"),
    ("usage_over", 5, "USAGE_TOKEN_CAP_EXCEEDED"),
])
def test_mock_staged_fault_preserves_108(fault: str, position: int, code: str) -> None:
    stage = StageProgress()
    fake = FakeTransport({position: fault})
    observed = ""
    for i in range(1, position + 1):
        assert stage.begin() == i
        try:
            validate_fixture(fake.send(BODY, 128))
        except (Stop, TimeoutError) as exc:
            observed = "TIMEOUT" if isinstance(exc, TimeoutError) else str(exc)
            stage.finish(i, engineering_success=False)
        else:
            stage.finish(i, engineering_success=True)
    assert observed == code and fake.attempts == position
    counts = Counter(stage.outcomes)
    assert (counts["SUCCESS"], counts["FAIL"], counts["NOT_RUN"]) == (position - 1, 1, 108 - position)
    with pytest.raises(Stop, match="STAGE_NO_FURTHER_SEND"):
        stage.begin()


def validate_fixture(reply: Reply) -> None:
    result = json.loads(reply.body)
    result["id"] = "synthetic-provider-id"
    wire.validate_reply(Reply(reply.status_code, json_bytes(result)), 128, ("C1",))


def test_three_then_one_hundred_five_preserve_order() -> None:
    stage = StageProgress()
    fake = FakeTransport()
    for i in range(1, 109):
        assert stage.initial3_passed is (i > 3)
        assert stage.begin() == i
        with pytest.raises(Stop, match="STAGE_NO_FURTHER_SEND"):
            stage.begin()
        validate_fixture(fake.send(BODY, 128))
        stage.finish(i, engineering_success=True)
    assert fake.attempts == 108
    assert stage.outcomes == ("SUCCESS",) * 108
    with pytest.raises(Stop, match="STAGE_NO_FURTHER_SEND"):
        stage.begin()


def test_refusal_cli_with_caller_supplied_digest(tmp_path: Path) -> None:
    import subprocess
    import sys

    root = Path(__file__).resolve().parents[2]
    out = tmp_path / "must-not-exist"
    command = [sys.executable, "-I", "-S", "-B", "scripts/research/check_chinese5060_pilot12_live.py",
               "--live", "--manifest-sha256", "1" * 64, "--output-dir", str(out)]
    reply = subprocess.run(command, cwd=root, capture_output=True, check=False)
    assert reply.returncode == 2
    assert reply.stderr.strip() == b"LIVE_DENIAL_WHEN_GATE_FAILED"
    assert not out.exists()
