"""Capture a new official Evidence page as immutable raw bytes before candidate writing.

This is a transport/provenance utility; a human must still verify factual atoms.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


OFFICIAL_HOST_SUFFIXES = (".gov.cn",)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc-id", required=True)
    parser.add_argument("--url", required=True)
    parser.add_argument("--marker")
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    parsed = urllib.parse.urlparse(args.url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or not host.endswith(OFFICIAL_HOST_SUFFIXES):
        raise ValueError("HTTPS official .gov.cn host required")
    if not args.doc_id.replace("-", "").replace("_", "").isalnum():
        raise ValueError("Unsafe document ID")
    if args.output_dir.exists():
        raise FileExistsError(args.output_dir)
    request = urllib.request.Request(args.url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        final_url = response.geturl()
        status = response.status
        content_type = response.headers.get("Content-Type", "")
        raw = response.read()
    final_host = (urllib.parse.urlparse(final_url).hostname or "").lower()
    if status != 200 or not final_host.endswith(OFFICIAL_HOST_SUFFIXES):
        raise ValueError(f"Unacceptable HTTP status/redirect: {status} {final_url}")
    is_pdf = "pdf" in content_type.lower() or final_url.lower().endswith(".pdf")
    if len(raw) < 3000:
        raise ValueError("Snapshot too short")
    if is_pdf and not raw.startswith(b"%PDF-"):
        raise ValueError("PDF signature absent")
    if not is_pdf and args.marker and args.marker.encode("utf-8") not in raw:
        raise ValueError("Exact UTF-8 marker absent")
    digest = hashlib.sha256(raw).hexdigest()
    args.output_dir.mkdir(parents=True)
    raw_path = args.output_dir / f"{args.doc_id}.{'pdf' if is_pdf else 'html'}"
    raw_path.write_bytes(raw)
    os.chmod(raw_path, 0o444)
    manifest = {
        "doc_id": args.doc_id,
        "requested_url": args.url,
        "final_url": final_url,
        "host": final_host,
        "http_status": status,
        "content_type": content_type,
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "raw_path": str(raw_path),
        "raw_bytes": len(raw),
        "raw_sha256": digest,
        "marker_transport_check": "PASS" if args.marker or is_pdf else "NOT_REQUESTED",
        "factual_metadata_review": "NOT_DONE_BY_THIS_TOOL",
    }
    manifest_path = args.output_dir / "capture_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.chmod(manifest_path, 0o444)
    print(json.dumps(manifest, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
