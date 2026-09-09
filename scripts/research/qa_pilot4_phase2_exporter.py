from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

from scripts.research import export_pilot4_phase2_xlsx as exporter


NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def _sha256(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _synthetic_completed_copy(source: Path, destination: Path, sheet_name: str) -> None:
    with zipfile.ZipFile(source, "r") as archive:
        parts = {name: archive.read(name) for name in archive.namelist()}
        sheet_path = exporter._sheet_target(archive, sheet_name)
    root = ET.fromstring(parts[sheet_path])
    values = {
        "F": "CURRENTLY_CONSISTENT",
        "G": "NOT_PRESENT",
        "H": "NOT_PRESENT",
        "I": "NOT_APPLICABLE",
        "J": "E1+E2",
        "K": "NONE",
    }
    for cell in root.findall(f".//{{{NS_MAIN}}}c"):
        reference = cell.attrib.get("r", "")
        match = re.fullmatch(r"([F-L])(\d+)", reference)
        if not match or not 4 <= int(match.group(2)) <= 75:
            continue
        value = cell.find(f"{{{NS_MAIN}}}v")
        if value is None:
            value = ET.SubElement(cell, f"{{{NS_MAIN}}}v")
        value.text = (
            values[match.group(1)]
            if match.group(1) != "L"
            else f"EXPORTER_QA_SYNTHETIC_REASON_{match.group(2)}"
        )
        cell.set("t", "str")
    parts[sheet_path] = ET.tostring(root, encoding="utf-8", xml_declaration=True)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in parts.items():
            archive.writestr(name, content)


def run(package_root: Path) -> dict[str, object]:
    results: dict[str, object] = {}
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        tag = annotator.replace("HUMAN-", "")
        workbook = (
            package_root
            / annotator
            / "phase2_v3_distribution"
            / f"PILOT4_AB_HUMAN_{tag}_PHASE2_ANNOTATION_WORKBOOK_V3.xlsx"
        )
        contract_path = (
            package_root
            / "export"
            / "contracts"
            / f"{annotator}_phase2_export_contract.json"
        )
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        blank_rows = exporter._extract(workbook, contract)
        blank_blocked = False
        try:
            exporter._validate(blank_rows, contract)
        except ValueError:
            blank_blocked = True
        if not blank_blocked:
            raise ValueError(f"BLANK_WORKBOOK_EXPORT_SHOULD_BLOCK:{annotator}")

        qa_dir = package_root / "qa" / "exporter" / annotator
        synthetic = qa_dir / "synthetic_completed_for_exporter_qa.xlsx"
        _synthetic_completed_copy(workbook, synthetic, str(contract["worksheet"]))
        rows = exporter._extract(synthetic, contract)
        exporter._validate(rows, contract)
        headers = [str(value) for value in contract["canonical_output_headers"]]
        run1 = exporter._csv_bytes(rows, headers)
        run2 = exporter._csv_bytes(rows, headers)
        if run1 != run2:
            raise ValueError(f"DETERMINISTIC_EXPORT_BLOCKER:{annotator}")
        first = qa_dir / "synthetic_export_run1.csv"
        second = qa_dir / "synthetic_export_run2.csv"
        first.write_bytes(run1)
        second.write_bytes(run2)
        decoded_header = run1.decode("utf-8-sig").splitlines()[0].split(",")
        if decoded_header != headers:
            raise ValueError(f"EXPORT_SCHEMA_BLOCKER:{annotator}:{decoded_header}")
        lowered = run1.lower()
        if any(
            token in lowered
            for token in [b"candidate_text", b"official_source_url", b"filling_check"]
        ):
            raise ValueError(f"EXPORT_HELPER_COLUMN_LEAKAGE_BLOCKER:{annotator}")
        results[annotator] = {
            "blank_template_export_blocked": True,
            "synthetic_completed_row_count": len(rows),
            "unique_id_count": len({row["blind_review_id"] for row in rows}),
            "exact_schema": headers,
            "deterministic_run1_sha256": _sha256(run1),
            "deterministic_run2_sha256": _sha256(run2),
            "byte_identical": run1 == run2,
            "candidate_evidence_helper_columns_excluded": True,
        }
    return {"status": "PASS", "results": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package-root", type=Path, required=True)
    args = parser.parse_args()
    result = run(args.package_root.resolve())
    _write_json(args.package_root / "qa" / "deterministic_exporter_qa.json", result)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
