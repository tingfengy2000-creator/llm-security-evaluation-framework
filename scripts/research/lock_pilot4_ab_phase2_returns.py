from __future__ import annotations

import argparse
import codecs
import csv
import hashlib
import io
import json
import os
import posixpath
import shutil
import stat
import zipfile
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence
from xml.etree import ElementTree as ET

from llmguard.domains.retrieval.hidden_poisoning.annotation_v31 import (
    derive_stealth_level,
)


TASK_ID = "PILOT4-A-B-DUAL-PHASE2-RAW-LOCK-AND-AGREEMENT-PREFLIGHT-01"
PHASE1_FIELDS = (
    "text_naturalness",
    "local_internal_conflict",
    "phase1_issue",
)
PHASE2_FIELDS = (
    "overall_fact_status",
    "version_claim_status",
    "authority_claim_status",
    "minimum_external_evidence_needed",
    "evidence_selection",
    "phase2_issue",
)
PHASE2_CORE_FIELDS = tuple(field for field in PHASE2_FIELDS if field != "evidence_selection")
PHASE2_HEADERS = (
    "blind_review_id",
    *PHASE2_FIELDS,
    "phase2_reason",
)

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


def now_utc() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value.rstrip() + "\n", encoding="utf-8", newline="\n")


def column_number(reference: str) -> int:
    letters = "".join(character for character in reference.upper() if character.isalpha())
    if not letters:
        raise ValueError(f"INVALID_CELL_REFERENCE:{reference}")
    value = 0
    for character in letters:
        value = value * 26 + ord(character) - 64
    return value


def workbook_parts(path: Path) -> dict[str, bytes]:
    with zipfile.ZipFile(path, "r") as archive:
        return {name: archive.read(name) for name in archive.namelist()}


def shared_strings(parts: Mapping[str, bytes]) -> list[str]:
    source = parts.get("xl/sharedStrings.xml")
    if source is None:
        return []
    root = ET.fromstring(source)
    return [
        "".join(node.text or "" for node in item.findall(f".//{{{NS_MAIN}}}t"))
        for item in root.findall(f"{{{NS_MAIN}}}si")
    ]


def sheet_paths(parts: Mapping[str, bytes]) -> tuple[list[str], dict[str, str]]:
    workbook = ET.fromstring(parts["xl/workbook.xml"])
    relationships = ET.fromstring(parts["xl/_rels/workbook.xml.rels"])
    targets = {
        node.attrib["Id"]: node.attrib["Target"]
        for node in relationships.findall(f"{{{NS_PKG}}}Relationship")
    }
    sheets = workbook.find(f"{{{NS_MAIN}}}sheets")
    if sheets is None:
        raise ValueError("WORKBOOK_SHEETS_MISSING")
    names: list[str] = []
    paths: dict[str, str] = {}
    for sheet in sheets:
        name = sheet.attrib["name"]
        target = targets[sheet.attrib[f"{{{NS_REL}}}id"]].replace("\\", "/")
        if target.startswith("/"):
            target = target.lstrip("/")
        elif not target.startswith("xl/"):
            target = "xl/" + target.lstrip("./")
        names.append(name)
        paths[name] = target
    return names, paths


def cell_value(cell: ET.Element, shared: Sequence[str]) -> str:
    cell_type = cell.attrib.get("t")
    if cell_type == "inlineStr":
        return "".join(node.text or "" for node in cell.findall(f".//{{{NS_MAIN}}}t"))
    value = cell.find(f"{{{NS_MAIN}}}v")
    raw = "" if value is None or value.text is None else value.text
    if cell_type == "s" and raw:
        return shared[int(raw)]
    return raw


def cell_semantics(parts: Mapping[str, bytes], target: str) -> dict[str, tuple[str, str]]:
    shared = shared_strings(parts)
    root = ET.fromstring(parts[target])
    result: dict[str, tuple[str, str]] = {}
    for cell in root.findall(f".//{{{NS_MAIN}}}c"):
        reference = cell.attrib.get("r", "")
        formula = cell.find(f"{{{NS_MAIN}}}f")
        formula_text = "" if formula is None or formula.text is None else formula.text
        value_text = "" if formula is not None else cell_value(cell, shared)
        if value_text or formula is not None:
            result[reference] = (value_text, formula_text)
    return result


def formula_references(parts: Mapping[str, bytes], target: str) -> set[str]:
    root = ET.fromstring(parts[target])
    return {
        cell.attrib.get("r", "")
        for cell in root.findall(f".//{{{NS_MAIN}}}c")
        if cell.find(f"{{{NS_MAIN}}}f") is not None
    }


def worksheet_rows(parts: Mapping[str, bytes], target: str) -> dict[int, dict[int, str]]:
    shared = shared_strings(parts)
    root = ET.fromstring(parts[target])
    result: dict[int, dict[int, str]] = {}
    for row in root.findall(f".//{{{NS_MAIN}}}row"):
        row_number = int(row.attrib["r"])
        result[row_number] = {
            column_number(cell.attrib["r"]): cell_value(cell, shared)
            for cell in row.findall(f"{{{NS_MAIN}}}c")
        }
    return result


def hyperlink_targets(parts: Mapping[str, bytes], target: str) -> dict[str, str]:
    root = ET.fromstring(parts[target])
    hyperlinks = root.find(f"{{{NS_MAIN}}}hyperlinks")
    if hyperlinks is None:
        return {}
    rel_path = posixpath.join(
        posixpath.dirname(target), "_rels", posixpath.basename(target) + ".rels"
    )
    relationships = ET.fromstring(parts[rel_path])
    targets = {
        node.attrib["Id"]: node.attrib.get("Target", "")
        for node in relationships.findall(f"{{{NS_PKG}}}Relationship")
    }
    return {
        node.attrib.get("ref", ""): targets.get(node.attrib.get(f"{{{NS_REL}}}id", ""), "")
        for node in hyperlinks
    }


def validation_contract(parts: Mapping[str, bytes], target: str) -> list[dict[str, str]]:
    root = ET.fromstring(parts[target])
    parent = root.find(f"{{{NS_MAIN}}}dataValidations")
    if parent is None:
        return []
    result = []
    for node in parent:
        formula = node.find(f"{{{NS_MAIN}}}formula1")
        result.append(
            {
                "sqref": node.attrib.get("sqref", ""),
                "type": node.attrib.get("type", ""),
                "formula1": "" if formula is None or formula.text is None else formula.text,
            }
        )
    return sorted(result, key=lambda item: item["sqref"])


def read_contract(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_phase2_rows(
    workbook: Path, contract: Mapping[str, Any]
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    parts = workbook_parts(workbook)
    _, paths = sheet_paths(parts)
    rows = worksheet_rows(parts, paths[str(contract["worksheet"])])
    header_row = int(contract["header_row"])
    display_to_canonical = {
        str(display): str(canonical)
        for display, canonical in contract["display_to_canonical_header"].items()
    }
    headers = rows[header_row]
    canonical_to_column = {
        display_to_canonical[value]: column
        for column, value in headers.items()
        if value in display_to_canonical
    }
    if set(canonical_to_column) != set(PHASE2_HEADERS):
        raise ValueError(f"PHASE2_HEADER_MAPPING_BLOCKER:{workbook.name}")
    canonical: list[dict[str, str]] = []
    context: list[dict[str, str]] = []
    expected_count = int(contract["expected_row_count"])
    for row_number in range(header_row + 1, header_row + 1 + expected_count):
        values = rows.get(row_number, {})
        canonical.append(
            {
                field: values.get(canonical_to_column[field], "").strip()
                for field in PHASE2_HEADERS
            }
        )
        context.append(
            {
                "blind_review_id": values.get(1, "").strip(),
                "candidate_text": values.get(2, "").strip(),
                "source_title": values.get(3, "").strip(),
                "e1_title": values.get(4, "").strip(),
                "e1_url": values.get(5, "").strip(),
                "e2_title": values.get(6, "").strip(),
                "e2_url": values.get(7, "").strip(),
            }
        )
    validate_phase2_rows(canonical, contract, workbook.name)
    return canonical, context


def validate_phase2_rows(
    rows: Sequence[Mapping[str, str]], contract: Mapping[str, Any], source_name: str
) -> None:
    expected_ids = [str(value) for value in contract["expected_blind_review_ids_in_order"]]
    ids = [row["blind_review_id"] for row in rows]
    if len(rows) != 72 or len(set(ids)) != 72 or ids != expected_ids:
        raise ValueError(f"PHASE2_72_ID_ORDER_BLOCKER:{source_name}")
    enums = {
        field: set(str(value) for value in values)
        for field, values in contract["canonical_enums"].items()
    }
    for row_number, row in enumerate(rows, start=2):
        for field, allowed in enums.items():
            if row[field] not in allowed:
                raise ValueError(
                    f"PHASE2_ENUM_BLOCKER:{source_name}:{row_number}:{field}:{row[field]}"
                )
        if not row["phase2_reason"].strip():
            raise ValueError(f"PHASE2_REASON_BLOCKER:{source_name}:{row_number}")
        conflict = row["overall_fact_status"] == "FACTUAL_CONFLICT"
        minimum = row["minimum_external_evidence_needed"]
        if conflict and minimum == "NOT_APPLICABLE":
            raise ValueError(f"PHASE2_MINIMUM_BLOCKER:{source_name}:{row_number}")
        if not conflict and minimum != "NOT_APPLICABLE":
            raise ValueError(f"PHASE2_MINIMUM_BLOCKER:{source_name}:{row_number}")


def workbook_semantic_qa(returned: Path, baseline: Path) -> dict[str, Any]:
    returned_parts = workbook_parts(returned)
    baseline_parts = workbook_parts(baseline)
    returned_names, returned_paths = sheet_paths(returned_parts)
    baseline_names, baseline_paths = sheet_paths(baseline_parts)
    if returned_names != baseline_names:
        raise ValueError(f"WORKBOOK_SHEET_PARITY_BLOCKER:{returned.name}")

    allowed_inputs = {
        f"{column}{row}" for column in "HIJKLMN" for row in range(4, 76)
    }
    excel_formula_serialization = {f"O{row}" for row in range(4, 76)}
    sheet_checks: dict[str, Any] = {}
    for sheet_name in returned_names:
        returned_cells = cell_semantics(returned_parts, returned_paths[sheet_name])
        baseline_cells = cell_semantics(baseline_parts, baseline_paths[sheet_name])
        if sheet_name == "01_标注表":
            returned_cells = {
                ref: value
                for ref, value in returned_cells.items()
                if ref not in allowed_inputs and ref not in excel_formula_serialization
            }
            baseline_cells = {
                ref: value
                for ref, value in baseline_cells.items()
                if ref not in allowed_inputs and ref not in excel_formula_serialization
            }
        if returned_cells != baseline_cells:
            changed = sorted(set(returned_cells) ^ set(baseline_cells))
            changed.extend(
                ref
                for ref in sorted(set(returned_cells) & set(baseline_cells))
                if returned_cells[ref] != baseline_cells[ref]
            )
            raise ValueError(
                f"WORKBOOK_READONLY_CELL_PARITY_BLOCKER:{returned.name}:{sheet_name}:{changed[:10]}"
            )
        sheet_checks[sheet_name] = {
            "non_authorized_cell_semantic_parity": True,
            "compared_cell_count": len(returned_cells),
        }

    returned_formula_refs = formula_references(
        returned_parts, returned_paths["01_标注表"]
    )
    baseline_formula_refs = formula_references(
        baseline_parts, baseline_paths["01_标注表"]
    )
    if not excel_formula_serialization.issubset(returned_formula_refs):
        raise ValueError(f"WORKBOOK_QA_FORMULA_BLOCKER:{returned.name}")
    if not excel_formula_serialization.issubset(baseline_formula_refs):
        raise ValueError(f"BASELINE_QA_FORMULA_BLOCKER:{baseline.name}")

    returned_links = hyperlink_targets(returned_parts, returned_paths["01_标注表"])
    baseline_links = hyperlink_targets(baseline_parts, baseline_paths["01_标注表"])
    if returned_links != baseline_links or len(returned_links) != 144:
        raise ValueError(f"WORKBOOK_HYPERLINK_PARITY_BLOCKER:{returned.name}")
    returned_validations = validation_contract(
        returned_parts, returned_paths["01_标注表"]
    )
    baseline_validations = validation_contract(
        baseline_parts, baseline_paths["01_标注表"]
    )
    if returned_validations != baseline_validations or len(returned_validations) != 6:
        raise ValueError(f"WORKBOOK_VALIDATION_PARITY_BLOCKER:{returned.name}")
    return {
        "status": "PASS",
        "workbook": returned.name,
        "baseline": str(baseline.resolve()),
        "sheet_order_parity": True,
        "sheet_count": len(returned_names),
        "readonly_cell_semantic_parity": True,
        "input_cells_allowed_to_change": "H4:N75 only",
        "qa_formula_presence": "72/72",
        "qa_formula_serialization_note": "Excel shared-formula storage accepted; formula cells preserved",
        "hyperlink_target_parity": "144/144",
        "data_validation_parity": "6/6",
        "sheet_checks": sheet_checks,
    }


def canonical_csv_bytes(rows: Sequence[Mapping[str, str]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=PHASE2_HEADERS, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return codecs.BOM_UTF8 + buffer.getvalue().encode("utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    raw = path.read_bytes()
    text = raw.decode("utf-8-sig", errors="strict")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    return [dict(row) for row in reader]


def read_mapping(path: Path, annotator: str) -> tuple[dict[str, dict[str, Any]], dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("classification") != "CONTROL_PLANE_ONLY":
        raise ValueError(f"MAPPING_CLASSIFICATION_BLOCKER:{annotator}")
    if payload.get("annotator_id") != annotator:
        raise ValueError(f"MAPPING_ANNOTATOR_BLOCKER:{annotator}")
    records = payload.get("records", [])
    by_id = {str(record["blind_review_id"]): dict(record) for record in records}
    sample_ids = [str(record["sample_id"]) for record in records]
    if len(records) != 72 or len(by_id) != 72 or len(set(sample_ids)) != 72:
        raise ValueError(f"MAPPING_72_PARITY_BLOCKER:{annotator}")
    return by_id, {
        "annotator": annotator,
        "source_path": str(path.resolve()),
        "source_sha256": sha256(path),
        "record_count": 72,
        "blind_id_parity": "72/72",
        "sample_id_parity": "72/72",
    }


def cohen_kappa(a_values: Sequence[str], b_values: Sequence[str]) -> float | None:
    if len(a_values) != len(b_values) or not a_values:
        raise ValueError("KAPPA_INPUT_BLOCKER")
    size = len(a_values)
    observed = sum(a == b for a, b in zip(a_values, b_values, strict=True)) / size
    a_counts = Counter(a_values)
    b_counts = Counter(b_values)
    expected = sum(
        (a_counts[label] / size) * (b_counts[label] / size)
        for label in set(a_counts) | set(b_counts)
    )
    if expected == 1.0:
        return None
    return (observed - expected) / (1.0 - expected)


def field_agreement(
    a_rows: Mapping[str, Mapping[str, str]],
    b_rows: Mapping[str, Mapping[str, str]],
    field: str,
) -> dict[str, Any]:
    sample_ids = sorted(a_rows)
    a_values = [a_rows[sample_id][field] for sample_id in sample_ids]
    b_values = [b_rows[sample_id][field] for sample_id in sample_ids]
    labels = sorted(set(a_values) | set(b_values))
    matrix = {
        a_label: {
            b_label: sum(
                a_value == a_label and b_value == b_label
                for a_value, b_value in zip(a_values, b_values, strict=True)
            )
            for b_label in labels
        }
        for a_label in labels
    }
    matches = sum(a == b for a, b in zip(a_values, b_values, strict=True))
    kappa = cohen_kappa(a_values, b_values)
    return {
        "field": field,
        "n": len(sample_ids),
        "matches": matches,
        "disagreements": len(sample_ids) - matches,
        "raw_agreement": matches / len(sample_ids),
        "cohen_kappa": kappa,
        "kappa_status": "NOT_ESTIMABLE_NO_MARGINAL_VARIATION" if kappa is None else "DEFINED",
        "a_counts": dict(sorted(Counter(a_values).items())),
        "b_counts": dict(sorted(Counter(b_values).items())),
        "confusion_matrix_a_rows_b_columns": matrix,
    }


def exact_agreement(
    a_rows: Mapping[str, Mapping[str, str]],
    b_rows: Mapping[str, Mapping[str, str]],
    fields: Iterable[str],
) -> tuple[int, list[str]]:
    selected = tuple(fields)
    disagreements = [
        sample_id
        for sample_id in sorted(a_rows)
        if any(a_rows[sample_id][field] != b_rows[sample_id][field] for field in selected)
    ]
    return len(a_rows) - len(disagreements), disagreements


def rows_by_sample(
    rows: Sequence[Mapping[str, str]], mapping: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in rows:
        blind_id = row["blind_review_id"]
        if blind_id not in mapping:
            raise ValueError(f"RETURN_MAPPING_PARITY_BLOCKER:{blind_id}")
        sample_id = str(mapping[blind_id]["sample_id"])
        result[sample_id] = dict(row)
    if len(result) != 72:
        raise ValueError("RETURN_SAMPLE_PARITY_BLOCKER")
    return result


def enrich_context(
    contexts: Sequence[Mapping[str, str]], mapping: Mapping[str, Mapping[str, Any]]
) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    for row in contexts:
        record = mapping[row["blind_review_id"]]
        result[str(record["sample_id"])] = {
            **dict(row),
            "sample_id": str(record["sample_id"]),
            "triplet_id": str(record["triplet_id"]),
        }
    return result


def build_disagreements(
    phase1_a: Mapping[str, Mapping[str, str]],
    phase1_b: Mapping[str, Mapping[str, str]],
    phase2_a: Mapping[str, Mapping[str, str]],
    phase2_b: Mapping[str, Mapping[str, str]],
    context_a: Mapping[str, Mapping[str, str]],
    context_b: Mapping[str, Mapping[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    material: list[dict[str, str]] = []
    process: list[dict[str, str]] = []
    for sample_id in sorted(phase1_a):
        context = context_a[sample_id]
        if context["candidate_text"] != context_b[sample_id]["candidate_text"]:
            raise ValueError(f"A_B_CANDIDATE_PARITY_BLOCKER:{sample_id}")
        for phase, fields, a_rows, b_rows, reason_field in (
            ("PHASE1", PHASE1_FIELDS, phase1_a, phase1_b, "phase1_reason"),
            ("PHASE2", PHASE2_FIELDS, phase2_a, phase2_b, "phase2_reason"),
        ):
            for field in fields:
                if a_rows[sample_id][field] == b_rows[sample_id][field]:
                    continue
                record = {
                    "sample_id": sample_id,
                    "triplet_id": context["triplet_id"],
                    "candidate_text": context["candidate_text"],
                    "source_title": context["source_title"],
                    "phase": phase,
                    "field": field,
                    "a_blind_review_id": context_a[sample_id]["blind_review_id"],
                    "a_value": a_rows[sample_id][field],
                    "a_reason": a_rows[sample_id][reason_field],
                    "b_blind_review_id": context_b[sample_id]["blind_review_id"],
                    "b_value": b_rows[sample_id][field],
                    "b_reason": b_rows[sample_id][reason_field],
                    "e1_title": context["e1_title"] if phase == "PHASE2" else "",
                    "e1_url": context["e1_url"] if phase == "PHASE2" else "",
                    "e2_title": context["e2_title"] if phase == "PHASE2" else "",
                    "e2_url": context["e2_url"] if phase == "PHASE2" else "",
                    "materiality": (
                        "DESCRIPTIVE_PROCESS_ONLY"
                        if field == "evidence_selection"
                        else "OWNER_DECISION_REQUIRED"
                    ),
                    "owner_final_value": "",
                    "owner_decision_reason": "",
                }
                (process if field == "evidence_selection" else material).append(record)
    return material, process


def write_csv(path: Path, rows: Sequence[Mapping[str, str]], headers: Sequence[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_manifest(output: Path) -> None:
    manifest_path = output / "manifest" / "final_manifest.json"
    entries = []
    for path in sorted(output.rglob("*")):
        if path.is_file() and path != manifest_path:
            entries.append(
                {
                    "path": path.relative_to(output).as_posix(),
                    "bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    aggregate = hashlib.sha256(
        "\n".join(f"{item['sha256']}  {item['path']}" for item in entries).encode(
            "utf-8"
        )
    ).hexdigest()
    write_json(
        manifest_path,
        {
            "task_id": TASK_ID,
            "generated_at": now_utc(),
            "entry_count_excluding_manifest": len(entries),
            "aggregate_sha256": aggregate,
            "entries": entries,
        },
    )


def copy_immutable(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if source.read_bytes() != destination.read_bytes():
        raise ValueError(f"IMMUTABLE_COPY_BLOCKER:{source.name}")
    os.chmod(destination, stat.S_IREAD)


def execute(args: argparse.Namespace) -> dict[str, Any]:
    output = args.output.resolve()
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"OUTPUT_MUST_BE_NEW_OR_EMPTY:{output}")
    output.mkdir(parents=True, exist_ok=True)

    inputs = {
        "HUMAN-A01": {
            "workbook": args.a_workbook.resolve(),
            "baseline": args.a_baseline.resolve(),
            "contract": args.a_contract.resolve(),
            "mapping": args.a_mapping.resolve(),
            "phase1": args.a_phase1.resolve(),
        },
        "HUMAN-B01": {
            "workbook": args.b_workbook.resolve(),
            "baseline": args.b_baseline.resolve(),
            "contract": args.b_contract.resolve(),
            "mapping": args.b_mapping.resolve(),
            "phase1": args.b_phase1.resolve(),
        },
    }
    phase2_rows: dict[str, list[dict[str, str]]] = {}
    contexts: dict[str, list[dict[str, str]]] = {}
    semantic_qa: dict[str, Any] = {}
    contracts: dict[str, dict[str, Any]] = {}
    for annotator, paths in inputs.items():
        for label, path in paths.items():
            if label == "mapping":
                continue
            if not path.is_file():
                raise ValueError(f"INPUT_NOT_FOUND:{annotator}:{label}:{path}")
        contract = read_contract(paths["contract"])
        rows, context = extract_phase2_rows(paths["workbook"], contract)
        phase2_rows[annotator] = rows
        contexts[annotator] = context
        contracts[annotator] = contract
        semantic_qa[annotator] = workbook_semantic_qa(
            paths["workbook"], paths["baseline"]
        )
    write_json(output / "qa" / "workbook_semantic_parity.json", semantic_qa)

    lock_timestamp = now_utc()
    lock_records: dict[str, Any] = {}
    for annotator, paths in inputs.items():
        raw_destination = output / "raw_phase2" / annotator / paths["workbook"].name
        copy_immutable(paths["workbook"], raw_destination)
        tag = annotator.replace("HUMAN-", "")
        csv_destination = (
            output
            / "canonical_phase2_csv"
            / annotator
            / f"PILOT4_AB_HUMAN_{tag}_PHASE2_RETURN.csv"
        )
        csv_destination.parent.mkdir(parents=True, exist_ok=True)
        csv_destination.write_bytes(canonical_csv_bytes(phase2_rows[annotator]))
        os.chmod(csv_destination, stat.S_IREAD)
        record = {
            "task_id": TASK_ID,
            "annotator": annotator,
            "received_source_path": str(paths["workbook"]),
            "received_source_mtime_utc": datetime.fromtimestamp(
                paths["workbook"].stat().st_mtime, UTC
            ).isoformat().replace("+00:00", "Z"),
            "raw_workbook_filename": paths["workbook"].name,
            "raw_workbook_bytes": paths["workbook"].stat().st_size,
            "raw_workbook_sha256": sha256(paths["workbook"]),
            "immutable_copy_relative_path": raw_destination.relative_to(
                output
            ).as_posix(),
            "immutable_copy_sha256": sha256(raw_destination),
            "immutable_copy_byte_parity": True,
            "canonical_csv_relative_path": csv_destination.relative_to(output).as_posix(),
            "canonical_csv_bytes": csv_destination.stat().st_size,
            "canonical_csv_sha256": sha256(csv_destination),
            "schema": list(PHASE2_HEADERS),
            "rows": 72,
            "unique_ids": 72,
            "id_order_parity": "72/72 PASS",
            "enum_validation": "PASS",
            "reason_validation": "72/72 PASS",
            "minimum_logic_validation": "PASS",
            "workbook_semantic_parity": "PASS",
            "status": "RECEIVED / SCHEMA_VALID / ROW_PARITY_72_72 / HASH_LOCKED / IMMUTABLE",
            "locked_at_utc": lock_timestamp,
            "descriptive_counts": {
                field: dict(sorted(Counter(row[field] for row in phase2_rows[annotator]).items()))
                for field in PHASE2_FIELDS
            },
        }
        write_json(output / "phase2_lock" / f"{annotator}_phase2_lock.json", record)
        lock_records[annotator] = record

    dual_gate = {
        "task_id": TASK_ID,
        "evaluated_at": lock_timestamp,
        "A_PHASE2_RETURN_RECEIVED": True,
        "B_PHASE2_RETURN_RECEIVED": True,
        "A_PHASE2_RETURN_SCHEMA_VALID": True,
        "B_PHASE2_RETURN_SCHEMA_VALID": True,
        "A_PHASE2_RETURN_72_72": True,
        "B_PHASE2_RETURN_72_72": True,
        "A_PHASE2_RETURN_HASH_LOCKED": True,
        "B_PHASE2_RETURN_HASH_LOCKED": True,
        "A_PHASE2_RETURN_IMMUTABLE": True,
        "B_PHASE2_RETURN_IMMUTABLE": True,
        "DUAL_PHASE2_LOCK_GATE": "PASS",
        "ALL_FOUR_RAW_LOCKS_PASS": True,
        "mapping_unlocked_at_gate_evaluation": False,
        "expected_v3_loaded": False,
        "agreement_computed_at_gate_evaluation": False,
    }
    write_json(output / "phase2_lock" / "dual_phase2_lock_gate.json", dual_gate)

    mapping_loaded_at = now_utc()
    mappings: dict[str, dict[str, dict[str, Any]]] = {}
    mapping_records: dict[str, Any] = {}
    for annotator, paths in inputs.items():
        mapping, record = read_mapping(paths["mapping"], annotator)
        expected_return_ids = {
            row["blind_review_id"] for row in phase2_rows[annotator]
        }
        if set(mapping) != expected_return_ids:
            raise ValueError(f"MAPPING_RETURN_ID_PARITY_BLOCKER:{annotator}")
        mappings[annotator] = mapping
        mapping_records[annotator] = record
    if {record["sample_id"] for record in mappings["HUMAN-A01"].values()} != {
        record["sample_id"] for record in mappings["HUMAN-B01"].values()
    }:
        raise ValueError("A_B_MAPPING_SAMPLE_SET_PARITY_BLOCKER")
    mapping_unlock = {
        "task_id": TASK_ID,
        "authorization": "OWNER_CONTINUE_AFTER_BOTH_PHASE2_RETURNS_RECEIVED",
        "raw_lock_timestamp_utc": lock_timestamp,
        "mapping_load_timestamp_utc": mapping_loaded_at,
        "raw_lock_precedes_mapping_load": lock_timestamp < mapping_loaded_at,
        "mapping_scope": "PILOT4 FORMAL HUMAN A/B FINAL72 ONLY",
        "mapping_records": mapping_records,
        "a_b_sample_set_parity": "72/72 PASS",
        "expected_v3_loaded": False,
    }
    if not mapping_unlock["raw_lock_precedes_mapping_load"]:
        raise ValueError("RAW_LOCK_BEFORE_MAPPING_ORDER_BLOCKER")
    write_json(output / "comparison" / "ab_identity_mapping_unlock_record.json", mapping_unlock)

    phase1_by_sample: dict[str, dict[str, dict[str, str]]] = {}
    phase2_by_sample: dict[str, dict[str, dict[str, str]]] = {}
    context_by_sample: dict[str, dict[str, dict[str, str]]] = {}
    for annotator, paths in inputs.items():
        phase1_by_sample[annotator] = rows_by_sample(
            read_csv(paths["phase1"]), mappings[annotator]
        )
        phase2_by_sample[annotator] = rows_by_sample(
            phase2_rows[annotator], mappings[annotator]
        )
        context_by_sample[annotator] = enrich_context(
            contexts[annotator], mappings[annotator]
        )

    phase1_metrics = {
        field: field_agreement(
            phase1_by_sample["HUMAN-A01"], phase1_by_sample["HUMAN-B01"], field
        )
        for field in PHASE1_FIELDS
    }
    phase2_metrics = {
        field: field_agreement(
            phase2_by_sample["HUMAN-A01"], phase2_by_sample["HUMAN-B01"], field
        )
        for field in PHASE2_FIELDS
    }
    derived_a: dict[str, dict[str, str]] = {}
    derived_b: dict[str, dict[str, str]] = {}
    for annotator, destination in (
        ("HUMAN-A01", derived_a),
        ("HUMAN-B01", derived_b),
    ):
        for sample_id, phase2_row in phase2_by_sample[annotator].items():
            destination[sample_id] = {
                "derived_stealth_level": derive_stealth_level(
                    phase2_row["overall_fact_status"],
                    phase1_by_sample[annotator][sample_id]["local_internal_conflict"],
                    phase2_row["minimum_external_evidence_needed"],
                )
            }
    derived_metric = field_agreement(
        derived_a, derived_b, "derived_stealth_level"
    )

    phase1_exact, phase1_disagreement_samples = exact_agreement(
        phase1_by_sample["HUMAN-A01"],
        phase1_by_sample["HUMAN-B01"],
        PHASE1_FIELDS,
    )
    phase2_exact, phase2_disagreement_samples = exact_agreement(
        phase2_by_sample["HUMAN-A01"],
        phase2_by_sample["HUMAN-B01"],
        PHASE2_FIELDS,
    )
    phase2_core_exact, phase2_core_disagreement_samples = exact_agreement(
        phase2_by_sample["HUMAN-A01"],
        phase2_by_sample["HUMAN-B01"],
        PHASE2_CORE_FIELDS,
    )
    material, process = build_disagreements(
        phase1_by_sample["HUMAN-A01"],
        phase1_by_sample["HUMAN-B01"],
        phase2_by_sample["HUMAN-A01"],
        phase2_by_sample["HUMAN-B01"],
        context_by_sample["HUMAN-A01"],
        context_by_sample["HUMAN-B01"],
    )
    material_samples = sorted({row["sample_id"] for row in material})
    late_defect_flags = []
    for annotator in ("HUMAN-A01", "HUMAN-B01"):
        for sample_id, row in phase2_by_sample[annotator].items():
            if row["phase2_issue"] == "LATE_DISCOVERED_CANDIDATE_DEFECT":
                late_defect_flags.append(
                    {
                        "annotator": annotator,
                        "sample_id": sample_id,
                        "blind_review_id": row["blind_review_id"],
                        "candidate_text": context_by_sample[annotator][sample_id][
                            "candidate_text"
                        ],
                        "phase2_reason": row["phase2_reason"],
                    }
                )

    agreement = {
        "task_id": TASK_ID,
        "computed_at": now_utc(),
        "population": 72,
        "expected_v3_loaded": False,
        "phase1": {
            "field_metrics": phase1_metrics,
            "exact_relevant_fields": f"{phase1_exact}/72",
            "disagreement_sample_count": len(phase1_disagreement_samples),
        },
        "phase2": {
            "field_metrics": phase2_metrics,
            "exact_all_categorical_fields": f"{phase2_exact}/72",
            "all_field_disagreement_sample_count": len(phase2_disagreement_samples),
            "exact_core_fields_excluding_evidence_selection": f"{phase2_core_exact}/72",
            "core_disagreement_sample_count": len(phase2_core_disagreement_samples),
            "evidence_selection_interpretation": "DESCRIPTIVE_PROCESS_EVIDENCE_NOT_BENCHMARK_LABEL_ACCURACY",
        },
        "derived_stealth_level": derived_metric,
        "material_disagreement_field_count": len(material),
        "material_disagreement_sample_count": len(material_samples),
        "descriptive_process_difference_count": len(process),
        "late_discovered_candidate_defect_flags": late_defect_flags,
        "residual_pending_disagreements": len(material),
        "owner_adjudication_required": bool(material or late_defect_flags),
        "ground_truth_created": False,
    }
    write_json(output / "comparison" / "pilot4_ab_agreement_preflight.json", agreement)

    packet_headers = list(material[0]) if material else [
        "sample_id",
        "phase",
        "field",
        "owner_final_value",
        "owner_decision_reason",
    ]
    process_headers = list(process[0]) if process else packet_headers
    write_csv(
        output / "mismatch" / "PILOT4_AB_OWNER_ADJUDICATION_PACKET.csv",
        material,
        packet_headers,
    )
    write_csv(
        output / "mismatch" / "PILOT4_AB_DESCRIPTIVE_PROCESS_DIFFERENCES.csv",
        process,
        process_headers,
    )
    write_json(
        output / "mismatch" / "late_discovered_candidate_defect_flags.json",
        late_defect_flags,
    )

    issue_text = f"""
# PILOT4 A/B Agreement Human Decision Record

1. **Issue ID**: `PILOT4-AB-AGREEMENT-AND-CANDIDATE-DEFECT-BLOCKER-01`
2. **Issue name**: A/B Phase1/Phase2 material disagreement and late Candidate-defect flags
3. **Discovery stage/task**: `{TASK_ID}`
4. **Current facts**:
   - `OBSERVED_FACT`: both Phase2 workbooks passed schema, 72/72 ID/order, enum, mandatory reason, minimum logic, immutable-copy and workbook semantic-parity checks.
   - `OBSERVED_FACT`: Phase1 exact categorical agreement is `{phase1_exact}/72`; Phase2 exact all-category agreement is `{phase2_exact}/72`; Phase2 core exact agreement excluding `evidence_selection` is `{phase2_core_exact}/72`.
   - `OBSERVED_FACT`: `{len(material)}` material field disagreements affect `{len(material_samples)}` unique samples; `{len(process)}` `evidence_selection` differences are descriptive process observations.
   - `OBSERVED_FACT`: `{len(late_defect_flags)}` `LATE_DISCOVERED_CANDIDATE_DEFECT` flags were submitted and remain unresolved.
   - `SOURCE_DERIVED_FACT`: Accepted A/B contract requires disagreement-only Owner adjudication before Ground Truth generation.
   - `INFERENCE`: the raw returns are valid evidence, but reproducibility and Candidate-quality decisions remain open.
   - `UNKNOWN`: which annotator value, if either, should become the Owner-adjudicated value for each material disagreement.
5. **Affected constraints**: raw immutability; Expected-does-not-automatically-win; Candidate repair requires a new version and fresh A/B rereview; zero pending disagreements before Ground Truth.
6. **Why now**: Ground Truth and downstream Dataset work cannot begin while material disagreements and Candidate-defect flags remain unresolved.
7. **Downstream risks**: silent selection would bias labels and paper claims; ignoring Candidate defects risks invalid benchmark items; unnecessary rerun increases human cost; changing accepted protocol without approval reopens calibration.
8. **Options**:
   - **A — Owner disagreement-only adjudication (recommended)**: review the material packet and the five Candidate-defect flags; preserve raw returns. Lowest cost; reversible before Ground Truth lock; no re-annotation unless a real Candidate/Evidence defect is confirmed.
   - **B — Independent targeted rereview after a frozen clarification**: use only for rows where Owner cannot adjudicate from Candidate/Evidence. Higher cost; preserves rigor but delays closure and needs a separately approved contract.
   - **C — Repair Candidate/Evidence/Guide**: use only if a real defect is confirmed. Highest protocol impact; requires additive versioning and the fresh rereview required by the accepted contract.
9. **LOCAL recommendation**: choose A first, and escalate only substantiated Candidate/Evidence/Guide defects to B or C.
10. **Rationale and confidence**: high confidence in raw/QA and count evidence; no claim is made that either annotator automatically wins.
11. **Owner questions**: approve filling the disagreement-only Owner packet; for each late-defect flag decide `CONFIRMED_DEFECT`, `ANNOTATOR_INTERPRETATION_VARIANCE`, or `NEEDS_TARGETED_REREVIEW`.
12. **Before decision**: allowed—read-only review of packet/raw/evidence and additive Owner decision recording. Prohibited—raw edits, automatic adjudication, Expected-as-truth substitution, Ground Truth, Dataset freeze, Detector/Training, 5090, Formal Experiment, Paper Result.
"""
    write_text(output / "mismatch" / "PILOT4_AB_HUMAN_DECISION_REQUIRED.md", issue_text)

    write_json(
        output / "qa" / "expected_non_load_proof.json",
        {
            "task_id": TASK_ID,
            "expected_v3_loaded": False,
            "expected_contract_used_for_agreement": False,
            "mapping_loaded_only_after_dual_phase2_raw_lock": True,
            "raw_reviewer_values_rewritten": False,
            "owner_values_inferred": False,
            "ground_truth_created": False,
        },
    )
    write_json(
        output / "register" / "PILOT4_A_B_RETURN_AND_AGREEMENT_REGISTER.json",
        {
            "task_id": TASK_ID,
            "updated_at": now_utc(),
            "PILOT4_A_B_EXECUTION_APPROVED": True,
            "A_PHASE1_RETURN_LOCKED": True,
            "B_PHASE1_RETURN_LOCKED": True,
            "A_PHASE2_RETURN_LOCKED": True,
            "B_PHASE2_RETURN_LOCKED": True,
            "ALL_FOUR_RAW_LOCKS_PASS": True,
            "MAPPING_UNLOCKED_AFTER_FOUR_LOCKS": True,
            "EXPECTED_V3_LOADED": False,
            "AGREEMENT_PREFLIGHT_COMPUTED": True,
            "OWNER_ADJUDICATION_STATUS": "PENDING",
            "GROUND_TRUTH_CREATED": False,
            "DATASET_FROZEN": False,
            "FORMAL_EXPERIMENT_STARTED": False,
            "AUTO_CONTINUE": False,
        },
    )
    write_manifest(output)
    return {
        "status": "PASS_WITH_HUMAN_DECISION_REQUIRED",
        "output": str(output),
        "raw_locks": lock_records,
        "agreement": agreement,
    }


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--a-workbook", type=Path, required=True)
    result.add_argument("--b-workbook", type=Path, required=True)
    result.add_argument("--a-baseline", type=Path, required=True)
    result.add_argument("--b-baseline", type=Path, required=True)
    result.add_argument("--a-contract", type=Path, required=True)
    result.add_argument("--b-contract", type=Path, required=True)
    result.add_argument("--a-mapping", type=Path, required=True)
    result.add_argument("--b-mapping", type=Path, required=True)
    result.add_argument("--a-phase1", type=Path, required=True)
    result.add_argument("--b-phase1", type=Path, required=True)
    result.add_argument("--output", type=Path, required=True)
    return result


def main() -> int:
    try:
        result = execute(parser().parse_args())
    except Exception as error:
        print(f"{type(error).__name__}:{error}")
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
