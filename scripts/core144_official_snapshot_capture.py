"""Additive official-source capture, before any Core144 candidate construction.

This records source bytes and extraction identity, not legal validity, current
status, factual correctness or independent annotation. No label input is read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests
from pypdf import PdfReader


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style"}:
            self.skip += 1
        if tag in {"p", "div", "br", "tr", "h1", "h2"}:
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style"}:
            self.skip = max(0, self.skip - 1)

    def handle_data(self, data: str) -> None:
        if not self.skip:
            self.parts.append(data)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_new(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)


def capture(item: dict[str, Any], root: Path) -> dict[str, Any]:
    url = item["official_url"]
    host = urlparse(url).hostname or ""
    if not (host.endswith(".gov.cn") or host.endswith(".chinatax.gov.cn")):
        raise ValueError(f"Unapproved non-government source: {host}")
    record = {**item, "source_host": host, "started_utc": datetime.now(timezone.utc).isoformat()}
    try:
        response = requests.get(url, timeout=(10, 40), headers={"User-Agent": "Mozilla/5.0"})
        raw = response.content
        record.update({"status_code": response.status_code, "final_url": response.url,
                       "content_type": response.headers.get("Content-Type"),
                       "raw_bytes": len(raw), "raw_sha256": sha(raw)})
        write_new(root / "raw" / f"{item['evidence_doc_id']}.bin", raw)
        response.raise_for_status()
        final_host = urlparse(response.url).hostname or ""
        if not final_host.endswith(".gov.cn"):
            raise ValueError(f"Redirect left official source boundary: {final_host}")
        if raw.startswith(b"%PDF"):
            reader = PdfReader(BytesIO(raw))
            visible = "\n".join(page.extract_text() or "" for page in reader.pages)
            record.update({"extraction_method": "pypdf_text_not_layout_verification",
                           "pdf_pages": len(reader.pages), "encoding": "PDF_TEXT_EXTRACTION"})
        else:
            encoding = response.encoding or "utf-8"
            if encoding.lower() in {"iso-8859-1", "ascii"}:
                encoding = ("utf-8" if b"utf-8" in raw[:10000].lower()
                            else response.apparent_encoding or "utf-8")
            parser = VisibleText()
            parser.feed(raw.decode(encoding, errors="strict"))
            visible = "\n".join(line.strip() for line in "".join(parser.parts).splitlines() if line.strip())
            record["encoding"] = encoding
        encoded = visible.encode("utf-8")
        write_new(root / "text" / f"{item['evidence_doc_id']}.txt", encoded)
        normalized = re.sub(r"\s", "", visible)
        found = all(re.sub(r"\s", "", anchor) in normalized
                    for anchor in item["required_identity_anchors"])
        record.update({"text_sha256": sha(encoded), "text_characters": len(visible),
                       "identity_anchors_present": found,
                       "capture_status": "CAPTURED_IDENTITY_ANCHORS_PRESENT" if found
                       else "CAPTURED_IDENTITY_PRECHECK_FAILED"})
    except (requests.RequestException, UnicodeError, ValueError) as exc:
        record.update({"capture_status": "SOURCE_CAPTURE_OR_DECODE_FAILED", "error": str(exc)})
    record["locked_utc"] = datetime.now(timezone.utc).isoformat()
    return record


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise ValueError("Refusing to overwrite a capture attempt")
    catalog_bytes = args.catalog.read_bytes()
    catalog = json.loads(catalog_bytes)
    items = catalog["sources"]
    if len({item["evidence_doc_id"] for item in items}) != len(items):
        raise ValueError("Duplicate source identity")
    args.output.mkdir(parents=True)
    write_new(args.output / "catalog_raw.json", catalog_bytes)
    with ThreadPoolExecutor(max_workers=6) as executor:
        records = list(executor.map(lambda item: capture(item, args.output), items))
    manifest = {"status": "RAW_CAPTURE_ONLY_NOT_FACT_OR_CANDIDATE_ACCEPTANCE",
                "catalog_sha256": sha(catalog_bytes), "records": records,
                "candidate_records_created": 0}
    write_new(args.output / "snapshot_registry.json",
              (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode())
    for record in records:
        print(record["evidence_doc_id"], record["capture_status"], record.get("raw_bytes", 0))


if __name__ == "__main__":
    main()
