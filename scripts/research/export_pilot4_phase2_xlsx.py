from __future__ import annotations

import argparse
import codecs
import csv
import io
import json
import re
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET


NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _column_number(reference: str) -> int:
    match = re.match(r"([A-Z]+)", reference.upper())
    if not match:
        raise ValueError(f"INVALID_CELL_REFERENCE:{reference}")
    value = 0
    for character in match.group(1):
        value = value * 26 + ord(character) - 64
    return value


def _sheet_target(archive: zipfile.ZipFile, sheet_name: str) -> str:
    workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    targets = {
        node.attrib["Id"]: node.attrib["Target"]
        for node in relationships.findall(f"{{{NS_PKG}}}Relationship")
    }
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("WORKBOOK_SHEETS_MISSING")
    for sheet in sheets:
        if sheet.attrib.get("name") != sheet_name:
            continue
        rel_id = sheet.attrib[f"{{{NS_REL}}}id"]
        target = targets[rel_id].replace("\\", "/")
        if target.startswith("/"):
            return target.lstrip("/")
        if target.startswith("xl/"):
            return target
        return "xl/" + target.lstrip("./")
    raise ValueError(f"WORKSHEET_NOT_FOUND:{sheet_name}")


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    if "xl/sharedStrings.xml" not in archive.namelist():
        return []
    root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    values = []
    for item in root.findall(f"{{{NS_MAIN}}}si"):
        values.append(
            "".join(node.text or "" for node in item.findall(f".//{{{NS_MAIN}}}t"))
        )
    return values


def _cell_value(cell: ET.Element, shared: list[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(f".//{{{NS_MAIN}}}t"))
    value = cell.find(f"{{{NS_MAIN}}}v")
    raw = "" if value is None or value.text is None else value.text
    if cell_type == "s" and raw:
        return shared[int(raw)]
    return raw


def _worksheet_rows(path: Path, sheet_name: str) -> dict[int, dict[int, str]]:
    with zipfile.ZipFile(path, "r") as archive:
        shared = _shared_strings(archive)
        root = ET.fromstring(archive.read(_sheet_target(archive, sheet_name)))
    result: dict[int, dict[int, str]] = {}
    for row in root.findall(f".//{{{NS_MAIN}}}row"):
        row_number = int(row.attrib["r"])
        values = {}
        for cell in row.findall(f"{{{NS_MAIN}}}c"):
            values[_column_number(cell.attrib["r"])] = _cell_value(cell, shared)
        result[row_number] = values
    return result


def _extract(path: Path, contract: dict[str, Any]) -> list[dict[str, str]]:
    rows = _worksheet_rows(path, str(contract["worksheet"]))
    header_row_number = int(contract["header_row"])
    display_map = {
        str(key): str(value)
        for key, value in contract["display_to_canonical_header"].items()
    }
    header_cells = rows.get(header_row_number, {})
    canonical_columns = {
        display_map[value]: column
        for column, value in header_cells.items()
        if value in display_map
    }
    expected_headers = [str(value) for value in contract["canonical_output_headers"]]
    if set(canonical_columns) != set(expected_headers):
        raise ValueError(f"EXPORT_HEADER_MAPPING_BLOCKER:{canonical_columns}")
    output_rows = []
    for row_number in range(
        header_row_number + 1,
        header_row_number + 1 + int(contract["expected_row_count"]),
    ):
        values = rows.get(row_number, {})
        output_rows.append(
            {
                header: values.get(canonical_columns[header], "").strip()
                for header in expected_headers
            }
        )
    return output_rows


def _validate(rows: list[dict[str, str]], contract: dict[str, Any]) -> None:
    expected_ids = [
        str(value) for value in contract["expected_blind_review_ids_in_order"]
    ]
    ids = [row["blind_review_id"] for row in rows]
    if len(rows) != 72 or len(set(ids)) != 72 or ids != expected_ids:
        raise ValueError("EXPORT_72_ID_ORDER_BLOCKER")
    enums = {
        field: set(values) for field, values in contract["canonical_enums"].items()
    }
    for row_number, row in enumerate(rows, start=2):
        for field, allowed in enums.items():
            if row[field] not in allowed:
                raise ValueError(
                    f"EXPORT_ENUM_BLOCKER:{row_number}:{field}:{row[field]}"
                )
        if not row["phase2_reason"].strip():
            raise ValueError(f"EXPORT_REASON_BLOCKER:{row_number}")
        is_conflict = row["overall_fact_status"] == "FACTUAL_CONFLICT"
        minimum = row["minimum_external_evidence_needed"]
        if is_conflict and minimum == "NOT_APPLICABLE":
            raise ValueError(
                f"EXPORT_MINIMUM_LOGIC_BLOCKER:{row_number}:CONFLICT_NOT_APPLICABLE"
            )
        if not is_conflict and minimum != "NOT_APPLICABLE":
            raise ValueError(
                f"EXPORT_MINIMUM_LOGIC_BLOCKER:{row_number}:NONCONFLICT_APPLICABLE"
            )


def _csv_bytes(rows: list[dict[str, str]], headers: list[str]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(
        buffer, fieldnames=headers, lineterminator="\n", extrasaction="raise"
    )
    writer.writeheader()
    writer.writerows(rows)
    return codecs.BOM_UTF8 + buffer.getvalue().encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--blocker-output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise SystemExit("OUTPUT_ALREADY_EXISTS_BLOCKER")
    contract = json.loads(args.contract.read_text(encoding="utf-8"))
    try:
        rows = _extract(args.input, contract)
        _validate(rows, contract)
        content = _csv_bytes(
            rows, [str(value) for value in contract["canonical_output_headers"]]
        )
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(content)
    except Exception as error:
        _write_json(
            args.blocker_output,
            {
                "status": "EXPORT_VALIDATION_BLOCKER",
                "input": str(args.input),
                "error_type": type(error).__name__,
                "error": str(error),
                "canonical_csv_created": False,
            },
        )
        return 2
    _write_json(
        args.blocker_output,
        {
            "status": "PASS",
            "input": str(args.input),
            "output": str(args.output),
            "row_count": len(rows),
            "schema": contract["canonical_output_headers"],
            "encoding": contract["output_encoding"],
            "newline": contract["output_newline"],
        },
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
