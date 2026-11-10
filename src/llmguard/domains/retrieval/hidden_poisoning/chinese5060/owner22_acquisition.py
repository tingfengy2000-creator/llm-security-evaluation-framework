"""Owner22 fixed-asset transfer only. No model or runtime execution."""
from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import os
import shutil
import ssl
import stat
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import HTTPSHandler, HTTPRedirectHandler, Request, build_opener

ROOT = Path(r"D:\experiments\paper1_chinese5060\owner22-assets")
RUN = "W1-5060-OWNER22-QWEN-GGUF-ASSET-STATIC-20261110-01"
HF_REPO = "Qwen/Qwen2.5-1.5B-Instruct-GGUF"
HF_REV = "91cad51170dc346986eccefdc2dd33a9da36ead9"
GH_REPO = "ggml-org/llama.cpp"
GH_COMMIT = "3b4d6ab3f79651935fba1dd93732f29022a7f5f5"
GH_TAG = "b12242"
CAP = 1_142_252_137
DISK_CAP = 4 * 1024**3
FREE_RESERVE = 10 * 1024**3
ZIP_CAP = 512 * 1024**2
CHUNK = 1024**2


@dataclass(frozen=True)
class Asset:
    filename: str
    size: int
    sha256: str
    url: str
    endpoint_hosts: tuple[str, ...]


MODEL = Asset("qwen2.5-1.5b-instruct-q4_k_m.gguf", 1_117_320_736,
              "6a1a2eb6d15622bf3c96857206351ba97e1af16c30d7a74ee38970e434e9407e",
              f"https://huggingface.co/{HF_REPO}/resolve/{HF_REV}/qwen2.5-1.5b-instruct-q4_k_m.gguf",
              ("us.aws.cdn.hf.co",))
RUNTIME = Asset("llama-b12242-bin-win-cpu-x64.zip", 24_931_401,
                "4723cd1f1b10169b6ca681f787ea37238e449b1c56538b4b90c71a82fad949a0",
                f"https://github.com/{GH_REPO}/releases/download/{GH_TAG}/llama-b12242-bin-win-cpu-x64.zip",
                ("release-assets.githubusercontent.com",))
ASSETS = (MODEL, RUNTIME)


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args: Any, **kwargs: Any) -> None:
        return None


def now() -> str:
    return datetime.now(UTC).isoformat()


def need(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def safe(path: Path) -> None:
    need(path.is_absolute() and path.resolve() == path, "PATH_DRIFT")
    for part in (path, *path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        need(not info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT, "REPARSE_POINT")


def check_disk(additional: int) -> None:
    safe(ROOT)
    total = 0
    for path in ROOT.rglob("*"):
        info = path.lstat()
        need(not info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT, "REPARSE_POINT_IN_ROOT")
        if stat.S_ISREG(info.st_mode):
            need(info.st_nlink == 1, "HARD_LINK_IN_ROOT")
            total += info.st_size
    need(total + additional <= DISK_CAP and shutil.disk_usage(ROOT).free >= FREE_RESERVE + additional,
         "DISK_CAP_OR_RESERVE")


def checked_environment() -> None:
    for key in ("TEMP", "TMP", "HF_HOME", "HF_HUB_CACHE", "HUGGINGFACE_HUB_CACHE", "LLAMA_CACHE",
                "XDG_CACHE_HOME", "USERPROFILE"):
        path = Path(os.environ[key])
        safe(path)
        need(path.is_relative_to(ROOT), "CACHE_OUTSIDE_ROOT:" + key)
    check_disk(0)


def write_json(name: str, value: Any) -> None:
    path = ROOT / "logs" / name
    safe(path)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, sort_keys=True, indent=2)
        handle.write("\n")


def sha_file(path: Path) -> str:
    safe(path)
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def opener() -> Any:
    return build_opener(NoRedirect(), HTTPSHandler(context=ssl.create_default_context()))


def request(net: Any, url: str, method: str, accept: str) -> Any:
    try:
        return net.open(Request(url, method=method, headers={"Accept": accept, "Accept-Encoding": "identity",
                        "Cache-Control": "no-cache", "User-Agent": "LLMGuard-Owner22-fixed-assets/1"}), timeout=90)
    except HTTPError as response:
        return response


def peer(response: Any) -> dict[str, Any]:
    stream = getattr(response, "fp", None)
    stream = getattr(stream, "fp", stream)
    socket = getattr(getattr(stream, "raw", None), "_sock", None)
    certificate = socket.getpeercert(binary_form=True) if socket is not None else None
    return {"ssl_default_verify": True, "tls_version": socket.version() if socket is not None else None,
            "peer_certificate_der_sha256": hashlib.sha256(certificate).hexdigest() if certificate else None}


def metadata(net: Any, url: str) -> Any:
    with request(net, url, "GET", "application/json") as response:
        need(response.code == 200 and "json" in response.headers.get("Content-Type", ""), "METADATA_RESPONSE")
        data = response.read(1024**2)
        need(len(data) < 1024**2, "METADATA_RESPONSE_LIMIT")
    return json.loads(data)


def publisher(net: Any) -> dict[str, Any]:
    hf = metadata(net, f"https://huggingface.co/api/models/{HF_REPO}/revision/{HF_REV}?blobs=true")
    model = [row for row in hf["siblings"] if row["rfilename"] == MODEL.filename]
    need(hf["sha"] == HF_REV and hf["id"] == HF_REPO and hf["cardData"]["license"] == "apache-2.0"
         and len(model) == 1 and model[0]["size"] == MODEL.size and model[0]["lfs"]["sha256"] == MODEL.sha256,
         "HF_PUBLISHER_DRIFT")
    base = f"https://api.github.com/repos/{GH_REPO}"
    gh = metadata(net, f"{base}/releases/tags/{GH_TAG}")
    item = metadata(net, f"{base}/releases/assets/729746535")
    tag = metadata(net, f"{base}/git/ref/tags/{GH_TAG}")
    need(gh["id"] == 439859799 and gh["tag_name"] == GH_TAG and gh["target_commitish"] == GH_COMMIT
         and tag["object"]["type"] == "commit" and tag["object"]["sha"] == GH_COMMIT
         and item["id"] == 729746535 and item["name"] == RUNTIME.filename and item["size"] == RUNTIME.size
         and item["digest"] == "sha256:" + RUNTIME.sha256 and item["browser_download_url"] == RUNTIME.url
         and item["state"] == "uploaded" and any(
             a["id"] == item["id"] and a["digest"] == item["digest"] and a["size"] == item["size"] for a in gh["assets"]
         ), "GITHUB_PUBLISHER_DRIFT")
    return {"checked_utc": now(), "hf": {"repo": HF_REPO, "revision": HF_REV, "license": "Apache-2.0", "file": model[0]},
            "github": {"release_id": gh["id"], "asset_id": item["id"], "tag": GH_TAG, "commit": GH_COMMIT,
                       "digest": item["digest"], "size": item["size"], "prerelease": gh["prerelease"],
                       "immutable": gh["immutable"], "source_license_from_owner21": "MIT"}}


def endpoint(url: str, allowed: tuple[str, ...]) -> str:
    p = urlsplit(url)
    need(p.scheme == "https" and p.hostname in allowed and p.port in {None, 443} and not p.username and
         not p.password and not p.fragment and bool(p.path), "UNAPPROVED_REDIRECT")
    return str(p.hostname)


def final_response(net: Any, asset: Asset, method: str, hops: list[dict[str, Any]]) -> Any:
    # Only a single publisher redirect to a named official CDN is allowed.
    with request(net, asset.url, method, "*/*") as origin:
        hops.append({"host": urlsplit(asset.url).hostname, "status": origin.code, **peer(origin)})
        need(origin.code in {301, 302, 303, 307, 308}, "ORIGIN_DID_NOT_ISSUE_ASSET_REDIRECT")
        if asset == MODEL:
            need(origin.headers.get("X-Repo-Commit") == HF_REV and
                 origin.headers.get("X-Linked-Size") == str(asset.size) and
                 origin.headers.get("X-Linked-ETag", "").strip('"') == asset.sha256, "HF_REDIRECT_IDENTITY")
        url = origin.headers.get("Location", "")
        host = endpoint(url, asset.endpoint_hosts)
    response = request(net, url, method, "*/*")
    hops.append({"host": host, "status": response.code, "content_length": response.headers.get("Content-Length"),
                 "content_type": response.headers.get("Content-Type"), **peer(response)})
    try:
        need(response.code == 200 and response.headers.get_all("Content-Length") == [str(asset.size)] and
             response.headers.get("Transfer-Encoding") is None and response.headers.get("Content-Range") is None and
             response.headers.get("Content-Encoding", "identity").lower() == "identity" and
             "text/" not in response.headers.get("Content-Type", "").lower(), "ASSET_RESPONSE_FRAMING")
    except ValueError:
        response.close()
        raise
    return response


def preflight() -> None:
    check_disk(CAP + ZIP_CAP + 16 * CHUNK)
    net = opener()
    write_json("publisher_metadata.json", publisher(net))
    audit: dict[str, Any] = {"time_utc": now(), "run_id": RUN, "assets": [], "actual_body_bytes": 0}
    try:
        for asset in ASSETS:
            hops: list[dict[str, Any]] = []
            audit["assets"].append({"filename": asset.filename, "head_chain": hops})
            with final_response(net, asset, "HEAD", hops):
                pass
        audit["status"] = "PASS"
    except Exception as exc:
        audit["status"] = "BLOCKED"
        audit["error_class"] = type(exc).__name__
        audit["error"] = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
        raise
    finally:
        write_json("network_preflight.json", audit)


def acquire() -> None:
    need(json.loads((ROOT / "logs/network_preflight.json").read_bytes())["status"] == "PASS", "NO_HEAD_PREFLIGHT")
    check_disk(CAP + ZIP_CAP + 16 * CHUNK)
    need(sum(a.size for a in ASSETS) == CAP, "CONTRACT_TOTAL")
    write_json("transfer_started.json", {"time_utc": now(), "run_id": RUN, "assets": [asdict(a) for a in ASSETS]})
    net = opener()
    total = 0
    for asset in ASSETS:
        partial = ROOT / "staging" / (asset.filename + ".part")
        final = ROOT / "download" / asset.filename
        safe(partial)
        safe(final)
        need(not partial.exists() and not final.exists(), "EXISTING_ASSET")
        item: dict[str, Any] = {"file": asset.filename, "sha256_expected": asset.sha256, "size_expected": asset.size,
                                "started_utc": now(), "body_bytes": 0, "get_chain": [], "status": "BLOCKED"}
        running = hashlib.sha256()
        try:
            need(total + asset.size <= CAP, "TRANSFER_CAP")
            with final_response(net, asset, "GET", item["get_chain"]) as response, partial.open("xb") as handle:
                while item["body_bytes"] < asset.size:
                    try:
                        block = response.read(min(CHUNK, asset.size - item["body_bytes"]))
                    except http.client.IncompleteRead as exc:
                        item["body_bytes"] += len(exc.partial)
                        raise
                    need(bool(block), "BODY_TRUNCATED")
                    item["body_bytes"] += len(block)
                    need(total + item["body_bytes"] <= CAP, "TRANSFER_CAP")
                    handle.write(block)
                    running.update(block)
                    if item["body_bytes"] % (128 * CHUNK) == 0:
                        check_disk(asset.size - item["body_bytes"] + ZIP_CAP)
                        print(f"{asset.filename}: {item['body_bytes']} bytes", flush=True)
            item["sha256_actual"] = sha_file(partial)
            need(partial.stat().st_size == asset.size and
                 item["sha256_actual"] == running.hexdigest() == asset.sha256, "ASSET_HASH_OR_SIZE_MISMATCH")
            partial.rename(final)
            item["status"] = "PASS"
        except Exception as exc:
            item["error_class"] = type(exc).__name__
            item["error"] = str(exc) if isinstance(exc, ValueError) else type(exc).__name__
            raise
        finally:
            total += item["body_bytes"]
            item["cumulative_body_bytes"] = total
            item["finished_utc"] = now()
            write_json(asset.filename + ".receipt.json", item)
        print(f"{asset.filename}: verified {item['body_bytes']} bytes", flush=True)
    need(total == CAP, "TRANSFER_TOTAL")
    write_json("transfer_complete.json", {"time_utc": now(), "body_bytes": total, "asset_count": 2, "retries": 0})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=("preflight", "acquire"))
    args = parser.parse_args()
    checked_environment()
    {"preflight": preflight, "acquire": acquire}[args.stage]()


if __name__ == "__main__":
    main()
