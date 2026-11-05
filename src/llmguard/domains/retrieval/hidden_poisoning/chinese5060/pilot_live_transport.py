"""Single POST HTTPS candidate. Owner 10's offline checker currently issues no lease."""
from __future__ import annotations

import http.client
import io
import os
import queue
import re
import socket
import ssl
import sys
import threading
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from time import monotonic
from typing import Any

from .pilot_admission import Stop, strict_json
from .pilot_live_admission import require_live_lease
from .pilot_transport import WIRE_PATH, Reply, Usage, parse_answer, parse_usage

REGIONS = frozenset({"cn-beijing", "cn-hongkong", "ap-southeast-1", "us-east-1",
                     "eu-central-1", "ap-northeast-1"})
LEGACY = {
    "cn-beijing": "dashscope.aliyuncs.com",
    "ap-southeast-1": "dashscope-intl.aliyuncs.com",
    "cn-hongkong": "cn-hongkong.dashscope.aliyuncs.com",
}
MAX_RESPONSE = 1024 * 1024
CONNECT_SECONDS = 10
READ_SECONDS = 60
TOTAL_SECONDS = 90


def verify_host(region: str, host: str) -> None:
    if region not in REGIONS:
        raise Stop("UNBOUND_REGION")
    suffix = f".{region}.maas.aliyuncs.com"
    label = host.removesuffix(suffix)
    if host != LEGACY.get(region) and (
        not host.endswith(suffix) or not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
    ):
        raise Stop("HOST_NOT_IN_OFFICIAL_REGION")


@dataclass
class _SocketScope:
    host: str
    address: Any = None


_scope: ContextVar[_SocketScope | None] = ContextVar("bailian_one_post_scope", default=None)
_policy_installed = False


def _socket_audit(event: str, args: tuple[Any, ...]) -> None:
    if not event.startswith("socket."):
        return
    active = _scope.get()
    if active is not None:
        if event == "socket.getaddrinfo" and args[:2] == (active.host, 443):
            return
        if active.address is not None:
            if (event == "socket.__new__" and args[1] in (socket.AF_INET, socket.AF_INET6)
                    and args[2] == socket.SOCK_STREAM and args[3] in (0, socket.IPPROTO_TCP)):
                return
            if event == "socket.connect" and args[1] == active.address:
                return
    raise PermissionError("LIVE_SOCKET_OUTSIDE_BOUND_REQUEST")


def _install_socket_policy() -> None:
    global _policy_installed
    if not _policy_installed:
        sys.addaudithook(_socket_audit)
        _policy_installed = True


@contextmanager
def _network_scope(scope: _SocketScope) -> Iterator[None]:
    token = _scope.set(scope)
    try:
        yield
    finally:
        _scope.reset(token)


def _left(deadline: float) -> float:
    left = deadline - monotonic()
    if left <= 0:
        raise TimeoutError("LIVE_DEADLINE")
    return left


def _resolve(scope: _SocketScope, deadline: float) -> tuple[int, int, Any]:
    result: queue.Queue[tuple[int, int, Any] | None] = queue.Queue(1)

    def lookup() -> None:
        try:
            with _network_scope(scope):
                answers = socket.getaddrinfo(scope.host, 443, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP)
            family, _, protocol, _, address = next(
                item for item in answers if item[0] in (socket.AF_INET, socket.AF_INET6)
            )
            result.put_nowait((family, protocol, address))
        except (OSError, StopIteration):
            result.put_nowait(None)

    threading.Thread(target=lookup, daemon=True).start()
    try:
        found = result.get(timeout=_left(deadline))
    except queue.Empty:
        raise TimeoutError("LIVE_DNS_DEADLINE") from None
    if found is None:
        raise Stop("LIVE_DNS_FAILED")
    return found


def _tls_context() -> ssl.SSLContext:
    # SSLContext avoids ssl.create_default_context's SSLKEYLOGFILE behavior.
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.load_default_certs(ssl.Purpose.SERVER_AUTH)
    return ctx


class _TimedStream(io.RawIOBase):
    def __init__(self, sock: ssl.SSLSocket, deadline: float) -> None:
        self.sock = sock
        self.deadline = deadline

    def readable(self) -> bool:
        return True

    def readinto(self, buffer: Any) -> int:
        self.sock.settimeout(min(READ_SECONDS, _left(self.deadline)))
        return self.sock.recv_into(buffer)


class _ResponseSocket:
    def __init__(self, sock: ssl.SSLSocket, deadline: float) -> None:
        self.sock = sock
        self.deadline = deadline

    def makefile(self, mode: str) -> io.BufferedReader:
        if mode != "rb":
            raise Stop("INVALID_RESPONSE_STREAM_MODE")
        return io.BufferedReader(_TimedStream(self.sock, self.deadline))


class InterruptedResponse(Stop):
    """Partial private bytes for the run evidence. The exception message is a safe code."""
    def __init__(self, partial: bytes) -> None:
        super().__init__("LIVE_RESPONSE_INTERRUPTED")
        self.partial = partial


def _exchange(region: str, host: str, body: bytes, key: str) -> Reply:
    """Internal wire primitive. Caller must hold a checked lease and a durable send intent."""
    verify_host(region, host)
    if not re.fullmatch(r"[A-Za-z0-9._-]{1,256}", key):
        raise Stop("INVALID_CREDENTIAL_FORMAT")
    start = monotonic()
    connect_by, total_by = start + CONNECT_SECONDS, start + TOTAL_SECONDS
    scope = _SocketScope(host)
    family, proto, scope.address = _resolve(scope, connect_by)
    head = (
        f"POST {WIRE_PATH} HTTP/1.1\r\nHost: {host}\r\nAuthorization: Bearer {key}\r\n"
        f"Content-Type: application/json\r\nAccept-Encoding: identity\r\n"
        f"Connection: close\r\nContent-Length: {len(body)}\r\n\r\n"
    ).encode("ascii")
    with _network_scope(scope), socket.socket(family, socket.SOCK_STREAM, proto) as tcp:
        tcp.settimeout(_left(connect_by))
        tcp.connect(scope.address)
        tcp.settimeout(_left(connect_by))
        with _tls_context().wrap_socket(tcp, server_hostname=host, do_handshake_on_connect=False) as tls:
            tls.settimeout(_left(connect_by))
            tls.do_handshake()
            tls.settimeout(min(READ_SECONDS, _left(total_by)))
            tls.sendall(head + body)
            with http.client.HTTPResponse(_ResponseSocket(tls, total_by)) as response:  # type: ignore[arg-type]
                data = bytearray()
                try:
                    response.begin()
                    while len(data) <= MAX_RESPONSE:
                        block = response.read1(min(65536, MAX_RESPONSE + 1 - len(data)))
                        if not block:
                            break
                        data.extend(block)
                except (OSError, http.client.HTTPException):
                    raise InterruptedResponse(bytes(data)) from None
                if len(data) > MAX_RESPONSE:
                    raise InterruptedResponse(bytes(data))
                if response.length not in (None, 0):
                    raise InterruptedResponse(bytes(data))
                request_id = response.getheader("x-request-id")
                if request_id is not None and not re.fullmatch(r"[A-Za-z0-9._:-]{1,192}", request_id):
                    request_id = None
                return Reply(response.status, bytes(data), request_id)


class ConditionalLiveTransport:
    """The only intended runtime entry. No lease is released by the current checker."""
    automatic_retries = 0

    def __init__(self, region: str, host: str) -> None:
        require_live_lease()
        verify_host(region, host)
        self.region, self.host = region, host
        _install_socket_policy()

    def send(self, body: bytes) -> Reply:
        require_live_lease()
        key = os.environ.get("DASHSCOPE_API_KEY")
        if not key:
            raise Stop("LIVE_CREDENTIAL_UNAVAILABLE")
        return _exchange(self.region, self.host, body, key)


def validate_reply(reply: Reply, input_upper: int, citations: tuple[str, ...]) -> tuple[str, Usage, str]:
    if reply.status_code != 200:
        raise Stop("LIVE_HTTP_NOT_200")
    value = strict_json(reply.body)
    response_id = value.get("id") if isinstance(value, dict) else None
    if not isinstance(response_id, str) or not re.fullmatch(r"[A-Za-z0-9._:-]{1,192}", response_id):
        raise Stop("LIVE_RESPONSE_ID_INVALID")
    usage_obj = value.get("usage")
    actual = usage_obj.get("prompt_tokens") if isinstance(usage_obj, dict) else None
    if type(actual) is not int:
        raise Stop("USAGE_MISSING")
    if actual > input_upper:
        raise Stop("LIVE_INPUT_PROOF_VIOLATION")
    usage = parse_usage(value, actual)
    return parse_answer(value, citations), usage, response_id
