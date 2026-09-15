"""Execute the approved Final72 label-blind signal-feasibility study.

The three subcommands are intentionally separate processes:

1. ``prepare`` creates a label-free projection from immutable inputs.
2. ``extract`` consumes only that projection and locks the raw matrix.
3. ``analyze`` verifies the lock before it is allowed to load labels.

No detector is trained and no threshold is selected in this workflow.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from collections.abc import Iterable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, cast

from llmguard.domains.retrieval.hidden_poisoning.method_engineering import (
    FIVE_VIEW_SIGNAL_REGISTRY,
    SignalComputationStatus,
    SignalView,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.feasibility import (
    EXTRACTOR_VERSION,
    cliffs_delta,
    describe,
    diagnostic_auroc,
    diagnostic_average_precision,
    extract_sample_signals,
    forbidden_key_hits,
    instance_to_dict,
    numeric_value,
    oriented_value,
    spearman,
    validate_orientation_contract,
)

FINAL72_GT_SHA256 = "9e6224ef2cb2cb8e729f9ab569d09589c951e6df4ed3327c63c82913066d720a"
CANDIDATE_CORPUS_SHA256 = (
    "f530471ecd6551300d68c8ddf104cadce2305d8ff91e64010be222820628252d"
)
EXPECTED_SIGNAL_COUNT = 42
EXPECTED_SAMPLE_COUNT = 72
EXPECTED_RAW_ROWS = EXPECTED_SIGNAL_COUNT * EXPECTED_SAMPLE_COUNT
TASK_ID = "P1-FINAL72-FIVE-VIEW-SIGNAL-FEASIBILITY-EXECUTION-01"

FORBIDDEN_KEYS = {
    "candidate_kind",
    "clean_poison_hard_negative",
    "ground_truth",
    "gt_outcome",
    "hkp",
    "intended_stealth",
    "label",
    "labels",
    "overall_fact_status",
    "owner_adjudication",
    "owner_only",
    "poison_label",
    "semantic_attack_type",
    "stealth_level",
    "target",
}

RAW_FIELDS = (
    "sample_id",
    "signal_name",
    "view",
    "value",
    "applicable",
    "confidence",
    "computation_status",
    "reason_code",
    "reason",
    "source_refs",
    "extractor_version",
    "orientation",
    "details",
)


def utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def require_sha(path: Path, expected: str) -> dict[str, object]:
    actual = sha256_file(path)
    if actual != expected:
        raise ValueError(
            f"SHA mismatch for {path.name}: expected {expected}, got {actual}"
        )
    return {"filename": path.name, "bytes": path.stat().st_size, "sha256": actual}


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def write_jsonl(path: Path, rows: Iterable[Mapping[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            value = json.loads(line)
            if not isinstance(value, dict):
                raise ValueError(f"{path.name}:{line_number} is not an object")
            rows.append(value)
    return rows


def write_csv(
    path: Path, rows: Sequence[Mapping[str, object]], fields: Sequence[str]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fields), extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            serialized = dict(row)
            for field in fields:
                value = serialized.get(field)
                if isinstance(value, (list, dict)):
                    serialized[field] = json.dumps(
                        value, ensure_ascii=False, sort_keys=True
                    )
                elif value is None:
                    serialized[field] = ""
            writer.writerow(serialized)


def normalized_url(url: str) -> str:
    return url.replace("http://", "https://").rstrip("/")


def clean_snapshot_text(text: str) -> str:
    no_scripts = re.sub(r"<script\b[^>]*>.*?</script>", " ", text, flags=re.I | re.S)
    no_styles = re.sub(r"<style\b[^>]*>.*?</style>", " ", no_scripts, flags=re.I | re.S)
    no_tags = re.sub(r"<[^>]+>", " ", no_styles)
    return re.sub(r"\s+", " ", no_tags).strip()


def _registry_by_url(paths: Sequence[Path]) -> dict[str, dict[str, object]]:
    registry: dict[str, dict[str, object]] = {}
    for path in paths:
        payload = json.loads(path.read_text(encoding="utf-8"))
        records = payload.get("records")
        if not isinstance(records, list):
            raise ValueError(f"registry {path.name} has no records")
        for record in records:
            if not isinstance(record, dict):
                continue
            for field in ("source_url", "final_url"):
                raw_url = record.get(field)
                if isinstance(raw_url, str) and raw_url:
                    registry.setdefault(normalized_url(raw_url), record)
    return registry


def _snapshot_by_url(
    provenance: Path, snapshot_root: Path
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for record in read_jsonl(provenance):
        url = record.get("official_source_url")
        relative = record.get("snapshot_path")
        if not isinstance(url, str) or not isinstance(relative, str):
            continue
        path = snapshot_root / relative
        if not path.exists():
            raise FileNotFoundError(path)
        expected = record.get("snapshot_sha256")
        if expected and sha256_file(path) != expected:
            raise ValueError(f"snapshot hash mismatch: {path.name}")
        result[normalized_url(url)] = {
            "snapshot_text": clean_snapshot_text(
                path.read_text(encoding="utf-8", errors="replace")
            ),
            "content_hash": sha256_file(path),
            "official_role": None,
            "retrieval_status": "FROZEN_SNAPSHOT_VERIFIED",
            "http_status": 200,
        }
    return result


def prepare_inputs(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    if output.exists():
        raise FileExistsError(f"output already exists: {output}")
    output.mkdir(parents=True)

    candidate_identity = require_sha(args.candidate_corpus, CANDIDATE_CORPUS_SHA256)
    candidate_rows = read_jsonl(args.candidate_corpus)
    if len(candidate_rows) != EXPECTED_SAMPLE_COUNT:
        raise ValueError("candidate corpus must contain 72 rows")

    pool = json.loads(args.evidence_pool.read_text(encoding="utf-8"))
    items = pool.get("items")
    if not isinstance(items, list) or len(items) != 144:
        raise ValueError("neutral Evidence pool must contain 144 items")
    evidence_by_sample: dict[str, list[dict[str, object]]] = defaultdict(list)
    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Evidence pool item is not an object")
        evidence_by_sample[str(item["sample_id"])].append(dict(item))

    repair = json.loads(args.evidence_repair.read_text(encoding="utf-8"))
    for change in repair.get("changes", []):
        sample_id = str(change["sample_id"])
        evidence_by_sample[sample_id] = [dict(item) for item in change["new_E1_E2"]]

    registry = _registry_by_url([args.source_registry, args.companion_registry])
    snapshots = _snapshot_by_url(args.snapshot_provenance, args.snapshot_root)
    projection: list[dict[str, object]] = []
    source_coverage: Counter[str] = Counter()
    for row in candidate_rows:
        sample_id = str(row["sample_id"])
        phase1 = row.get("phase1_view")
        if not isinstance(phase1, dict):
            raise ValueError(f"{sample_id}: phase1_view missing")
        evidence_items = evidence_by_sample.get(sample_id, [])
        if len(evidence_items) != 2:
            raise ValueError(f"{sample_id}: expected two Evidence items")
        safe_evidence: list[dict[str, object]] = []
        for item in evidence_items:
            url = str(item.get("official_source_url") or "")
            key = normalized_url(url)
            record = registry.get(key)
            source_kind = "FROZEN_REGISTRY"
            if record is None:
                record = snapshots.get(key)
                source_kind = "FROZEN_TARGETED_REPAIR_SNAPSHOT"
            if record is None:
                raise ValueError(f"no frozen Evidence content for {sample_id} {url}")
            excerpt = str(
                record.get("support_excerpt") or record.get("snapshot_text") or ""
            )
            if not excerpt:
                raise ValueError(f"empty Evidence snapshot for {sample_id} {url}")
            content_hash = str(
                record.get("content_hash") or sha256_bytes(excerpt.encode("utf-8"))
            )
            safe_evidence.append(
                {
                    "evidence_id": str(item.get("evidence_id") or ""),
                    "official_source_title": str(
                        item.get("official_source_title")
                        or item.get("official_page_title")
                        or ""
                    ),
                    "official_source_url": url,
                    "source_type": str(item.get("source_type") or "OFFICIAL_SOURCE"),
                    "snapshot_text": excerpt,
                    "content_hash": content_hash,
                    "retrieval_status": str(
                        record.get("retrieval_status") or "UNKNOWN"
                    ),
                    "http_status": record.get("http_status"),
                    "official_role": record.get("official_role"),
                    "source_ref": f"{item.get('evidence_id')}:{content_hash}",
                    "projection_source": source_kind,
                }
            )
            source_coverage[source_kind] += 1
        projection.append(
            {
                "sample_id": sample_id,
                "candidate_text": str(phase1["candidate_text"]),
                "source_title": str(phase1["source_title"]),
                "primary_subject": str(row.get("primary_subject") or ""),
                "related_subjects": list(row.get("related_subjects") or []),
                "evidence": safe_evidence,
            }
        )

    hits = forbidden_key_hits(projection, FORBIDDEN_KEYS)
    if hits:
        raise ValueError(f"forbidden keys in safe projection: {sorted(set(hits))}")
    projection_path = (
        output / "input" / "PAPER1_FINAL72_SIGNAL_INPUT_PROJECTION_V1.jsonl"
    )
    write_jsonl(projection_path, projection)
    manifest = {
        "task_id": TASK_ID,
        "stage": "LABEL_FREE_INPUT_PROJECTION",
        "created_at": utc_now(),
        "candidate_source": candidate_identity,
        "source_identities": {
            "evidence_pool": require_sha(
                args.evidence_pool, sha256_file(args.evidence_pool)
            ),
            "source_registry": require_sha(
                args.source_registry, sha256_file(args.source_registry)
            ),
            "companion_registry": require_sha(
                args.companion_registry, sha256_file(args.companion_registry)
            ),
            "evidence_repair": require_sha(
                args.evidence_repair, sha256_file(args.evidence_repair)
            ),
            "snapshot_provenance": require_sha(
                args.snapshot_provenance, sha256_file(args.snapshot_provenance)
            ),
        },
        "projection": {
            "path": projection_path.relative_to(output).as_posix(),
            "sha256": sha256_file(projection_path),
            "rows": len(projection),
            "evidence_items": sum(
                len(evidence)
                for row in projection
                if isinstance((evidence := row["evidence"]), list)
            ),
            "forbidden_key_hits": 0,
            "allowed_top_level_keys": sorted(projection[0]),
            "source_coverage": dict(source_coverage),
        },
        "signal_extraction_executed": False,
        "labels_loaded": False,
    }
    write_json(output / "input" / "input_projection_manifest.json", manifest)
    print(json.dumps(manifest["projection"], ensure_ascii=False))


def _availability(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    by_view: dict[str, Counter[str]] = defaultdict(Counter)
    by_signal: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        status = str(row["computation_status"])
        by_view[str(row["view"])][status] += 1
        by_signal[str(row["signal_name"])][status] += 1
    return {
        "task_id": TASK_ID,
        "generated_before_labels": True,
        "raw_rows": len(rows),
        "by_view": {view: dict(counts) for view, counts in sorted(by_view.items())},
        "by_signal": {name: dict(counts) for name, counts in sorted(by_signal.items())},
    }


def _availability_markdown(payload: Mapping[str, object]) -> str:
    statuses = [status.value for status in SignalComputationStatus]
    lines = [
        "# Paper 1 Final72 Signal Availability Report",
        "",
        "Status: `PRE_LABEL / LABEL_BLIND`",
        "",
        "本表只报告能否计算，不包含任何 Clean/Poison/Hard Negative、HKP、S 或 Ground Truth 信息。",
        "",
        "| View | " + " | ".join(statuses) + " |",
        "| --- | " + " | ".join("---:" for _ in statuses) + " |",
    ]
    by_view = payload["by_view"]
    assert isinstance(by_view, dict)
    for view, counts in by_view.items():
        assert isinstance(counts, dict)
        lines.append(
            f"| {view} | "
            + " | ".join(str(counts.get(status, 0)) for status in statuses)
            + " |"
        )
    lines.extend(
        [
            "",
            "`NOT_APPLICABLE`、`INPUT_MISSING`、`MODEL_UNAVAILABLE` 的 value 均为 null；它们不代表安全或零风险。",
            "",
        ]
    )
    return "\n".join(lines)


def _quality(
    rows: Sequence[Mapping[str, object]], rerun: Sequence[Mapping[str, object]]
) -> dict[str, object]:
    if rows != rerun:
        raise ValueError("determinism rerun mismatch")
    values_by_signal: dict[str, list[float]] = defaultdict(list)
    invalid_finite = 0
    unexpected_null = 0
    for row in rows:
        value = row.get("value")
        status = row["computation_status"]
        if status == SignalComputationStatus.COMPUTED.value and value is None:
            unexpected_null += 1
        numeric = numeric_value(row)
        if numeric is not None:
            if not math.isfinite(numeric):
                invalid_finite += 1
            values_by_signal[str(row["signal_name"])].append(numeric)
    constant = sorted(
        name for name, values in values_by_signal.items() if len(set(values)) == 1
    )
    near_constant = sorted(
        name
        for name, values in values_by_signal.items()
        if len(set(values)) > 1
        and Counter(values).most_common(1)[0][1] / len(values) >= 0.95
    )
    perfect_duplicates: list[dict[str, object]] = []
    names = sorted(values_by_signal)
    rows_by_sample_signal = {
        (str(row["sample_id"]), str(row["signal_name"])): row for row in rows
    }
    sample_ids = sorted({str(row["sample_id"]) for row in rows})
    for index, left in enumerate(names):
        for right in names[index + 1 :]:
            pairs = [
                (
                    numeric_value(rows_by_sample_signal[(sample, left)]),
                    numeric_value(rows_by_sample_signal[(sample, right)]),
                )
                for sample in sample_ids
            ]
            overlap = [(a, b) for a, b in pairs if a is not None and b is not None]
            if len(overlap) >= 10 and all(a == b for a, b in overlap):
                perfect_duplicates.append(
                    {"left": left, "right": right, "overlap": len(overlap)}
                )
    return {
        "determinism_rerun_parity": True,
        "nan_or_inf": invalid_finite,
        "unexpected_null": unexpected_null,
        "constant_signals": constant,
        "near_constant_signals": near_constant,
        "perfect_duplicate_pairs": perfect_duplicates,
    }


def extract(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    manifest_path = output / "input" / "input_projection_manifest.json"
    projection_path = (
        output / "input" / "PAPER1_FINAL72_SIGNAL_INPUT_PROJECTION_V1.jsonl"
    )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_projection_sha = manifest["projection"]["sha256"]
    if sha256_file(projection_path) != expected_projection_sha:
        raise ValueError("safe input projection changed")
    projection = read_jsonl(projection_path)
    hits = forbidden_key_hits(projection, FORBIDDEN_KEYS)
    if hits:
        raise ValueError(f"label-bearing key reached extractor: {sorted(set(hits))}")
    validate_orientation_contract()

    first = [
        instance_to_dict(instance)
        for sample in projection
        for instance in extract_sample_signals(sample)
    ]
    second = [
        instance_to_dict(instance)
        for sample in projection
        for instance in extract_sample_signals(sample)
    ]
    if len(first) != EXPECTED_RAW_ROWS:
        raise ValueError(f"expected {EXPECTED_RAW_ROWS} raw rows, got {len(first)}")
    if forbidden_key_hits(first, FORBIDDEN_KEYS):
        raise ValueError("forbidden label-bearing key in raw matrix")
    raw_path = output / "matrix" / "PAPER1_FINAL72_SIGNAL_MATRIX_RAW_V1.jsonl"
    raw_csv = output / "matrix" / "PAPER1_FINAL72_SIGNAL_MATRIX_RAW_V1.csv"
    write_jsonl(raw_path, first)
    write_csv(raw_csv, first, RAW_FIELDS)

    availability = _availability(first)
    availability_path = output / "availability" / "signal_availability.json"
    write_json(availability_path, availability)
    availability_md = (
        output / "availability" / "PAPER1_FINAL72_SIGNAL_AVAILABILITY_REPORT.md"
    )
    availability_md.parent.mkdir(parents=True, exist_ok=True)
    availability_md.write_text(_availability_markdown(availability), encoding="utf-8")

    quality = _quality(first, second)
    quality.update(
        {
            "raw_matrix_label_key_hits": 0,
            "expected_v3_loaded": False,
            "ground_truth_loaded": False,
            "adjudication_loaded": False,
            "detector_training": False,
            "threshold_tuning": False,
        }
    )
    write_json(output / "qa" / "pre_label_signal_quality.json", quality)
    write_json(
        output / "gaps" / "RETRIEVAL_SIGNAL_INPUT_GAP_REPORT.json",
        {
            "status": "INPUT_MISSING",
            "affected_signals": 10,
            "affected_instances": 720,
            "reason": "No frozen query, retriever configuration, top-k trace, score, or repeat trace exists for Final72.",
            "label_derived_query_created": False,
        },
    )
    write_json(
        output / "baselines" / "baseline_execution_status.json",
        {
            "MLM": "MODEL_UNAVAILABLE_NO_FROZEN_CHECKPOINT",
            "PPL": "MODEL_UNAVAILABLE_NO_FROZEN_CHECKPOINT",
            "GMTP_FEASIBILITY_STATUS": "DEFERRED_WITH_REASON",
            "GMTP_reason": "No frozen compatible retriever, gradient path, token attribution path, and MLM dependency bundle for this study.",
            "downloads_or_model_changes": 0,
        },
    )
    lock_time = utc_now()
    lock = {
        "event": "SIGNAL_MATRIX_PRE_LABEL_LOCK",
        "status": "PASS",
        "timestamp": lock_time,
        "raw_matrix": {
            "path": raw_path.relative_to(output).as_posix(),
            "bytes": raw_path.stat().st_size,
            "sha256": sha256_file(raw_path),
            "rows": len(first),
            "samples": len({row["sample_id"] for row in first}),
            "signals_per_sample": EXPECTED_SIGNAL_COUNT,
        },
        "raw_csv_sha256": sha256_file(raw_csv),
        "availability_sha256": sha256_file(availability_path),
        "quality_sha256": sha256_file(output / "qa" / "pre_label_signal_quality.json"),
        "label_blind": True,
        "labels_loaded": False,
        "forbidden_key_hits": 0,
        "extractor_version": EXTRACTOR_VERSION,
    }
    write_json(output / "lock" / "SIGNAL_MATRIX_PRE_LABEL_LOCK.json", lock)
    write_jsonl(
        output / "events" / "execution_events.jsonl",
        [
            {
                "event": "SAFE_INPUT_PROJECTION_READY",
                "timestamp": manifest["created_at"],
                "labels_loaded": False,
            },
            {
                "event": "SIGNAL_MATRIX_PRE_LABEL_LOCK",
                "timestamp": lock_time,
                "raw_sha256": lock["raw_matrix"]["sha256"],
                "labels_loaded": False,
            },
        ],
    )
    print(json.dumps(lock, ensure_ascii=False))


def _design_labels(candidate_corpus: Path) -> dict[str, dict[str, object]]:
    require_sha(candidate_corpus, CANDIDATE_CORPUS_SHA256)
    result: dict[str, dict[str, object]] = {}
    for row in read_jsonl(candidate_corpus):
        owner = row.get("owner_only")
        if not isinstance(owner, dict):
            raise ValueError("owner_only experimental design missing")
        kind = str(owner.get("candidate_kind"))
        class_name = {
            "CLEAN_CURRENT": "CLEAN_CURRENT",
            "POISON_CANDIDATE": "POISON",
            "MATCHED_HARD_NEGATIVE": "HARD_NEGATIVE",
        }.get(kind)
        if class_name is None:
            raise ValueError(f"unknown candidate class {kind}")
        coverage = str(owner.get("coverage_cell") or "")
        match = re.fullmatch(r"HKP_(\d)_[A-Z_]+\|(S[123])", coverage)
        if not match:
            raise ValueError(f"invalid coverage cell {coverage}")
        result[str(row["sample_id"])] = {
            "class": class_name,
            "hkp": f"HKP{match.group(1)}",
            "stealth": match.group(2),
            "group_id": str(row["independence_group"]),
        }
    return result


def _distribution(values: Sequence[float]) -> dict[str, float | int | None]:
    return describe(values)


def _comparison(
    rows: Sequence[Mapping[str, object]],
    labels: Mapping[str, Mapping[str, object]],
    positive: str,
    negatives: set[str],
    *,
    subset_axis: str | None = None,
    subset_value: str | None = None,
) -> list[dict[str, object]]:
    by_signal: dict[str, dict[str, list[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in rows:
        label = labels[str(row["sample_id"])]
        if subset_axis is not None and str(label[subset_axis]) != subset_value:
            continue
        value = oriented_value(row)
        if value is None:
            continue
        class_name = str(label["class"])
        by_signal[str(row["signal_name"])][class_name].append(value)
    result: list[dict[str, object]] = []
    for signal_name, classes in sorted(by_signal.items()):
        pos = classes.get(positive, [])
        neg = [
            value for class_name in negatives for value in classes.get(class_name, [])
        ]
        if len(pos) < 3 or len(neg) < 3:
            continue
        result.append(
            {
                "signal_name": signal_name,
                "positive": positive,
                "negative": sorted(negatives),
                "positive_distribution": _distribution(pos),
                "negative_distribution": _distribution(neg),
                "cliffs_delta_oriented": cliffs_delta(pos, neg),
                "mann_whitney_u_exploratory": sum(a > b for a in pos for b in neg)
                + 0.5 * sum(a == b for a in pos for b in neg),
                "diagnostic_auroc": diagnostic_auroc(pos, neg),
                "diagnostic_auprc": diagnostic_average_precision(pos, neg),
                "claim_boundary": "DEVELOPMENT_SET_UNIVARIATE_DIAGNOSTIC_NOT_DETECTOR_RESULT",
            }
        )
    return result


def _raw_value_index(
    rows: Sequence[Mapping[str, object]],
) -> dict[tuple[str, str], Mapping[str, object]]:
    return {(str(row["sample_id"]), str(row["signal_name"])): row for row in rows}


def _matched_analysis(
    rows: Sequence[Mapping[str, object]], labels: Mapping[str, Mapping[str, object]]
) -> list[dict[str, object]]:
    index = _raw_value_index(rows)
    group_members: dict[str, dict[str, str]] = defaultdict(dict)
    for sample_id, label in labels.items():
        group_members[str(label["group_id"])][str(label["class"])] = sample_id
    output: list[dict[str, object]] = []
    for signal in sorted({str(row["signal_name"]) for row in rows}):
        counts: Counter[str] = Counter()
        for members in group_members.values():
            poison = oriented_value(index[(members["POISON"], signal)])
            hard_negative = oriented_value(index[(members["HARD_NEGATIVE"], signal)])
            clean = oriented_value(index[(members["CLEAN_CURRENT"], signal)])
            for comparison, other in (
                ("POISON_VS_HARD_NEGATIVE", hard_negative),
                ("POISON_VS_CLEAN", clean),
            ):
                if poison is None or other is None:
                    counts[f"{comparison}__UNAVAILABLE"] += 1
                elif poison > other:
                    counts[f"{comparison}__DIRECTIONALLY_CORRECT"] += 1
                elif poison == other:
                    counts[f"{comparison}__TIE"] += 1
                else:
                    counts[f"{comparison}__OPPOSITE"] += 1
        output.append({"signal_name": signal, **dict(counts)})
    return output


def _redundancy(rows: Sequence[Mapping[str, object]]) -> dict[str, object]:
    samples = sorted({str(row["sample_id"]) for row in rows})
    index = _raw_value_index(rows)
    signals = sorted({str(row["signal_name"]) for row in rows})
    pairs: list[dict[str, object]] = []
    for offset, left in enumerate(signals):
        for right in signals[offset + 1 :]:
            overlap: list[tuple[float, float]] = []
            for sample in samples:
                a = numeric_value(index[(sample, left)])
                b = numeric_value(index[(sample, right)])
                if a is not None and b is not None:
                    overlap.append((a, b))
            if len(overlap) < 10:
                continue
            rho = spearman([item[0] for item in overlap], [item[1] for item in overlap])
            if rho is not None and abs(rho) >= 0.9:
                pairs.append(
                    {
                        "left": left,
                        "right": right,
                        "rho": rho,
                        "overlap": len(overlap),
                        "status": "HIGH_REDUNDANCY",
                    }
                )
    adjacency: dict[str, set[str]] = defaultdict(set)
    for pair in pairs:
        left = str(pair["left"])
        right = str(pair["right"])
        adjacency[left].add(right)
        adjacency[right].add(left)
    clusters: list[list[str]] = []
    unseen = set(adjacency)
    while unseen:
        root = unseen.pop()
        cluster = {root}
        frontier = [root]
        while frontier:
            current = frontier.pop()
            new = adjacency[current] - cluster
            cluster.update(new)
            unseen.difference_update(new)
            frontier.extend(new)
        clusters.append(sorted(cluster))
    return {
        "threshold": 0.9,
        "highly_correlated_pairs": pairs,
        "redundancy_clusters": sorted(clusters),
        "signals_automatically_removed": 0,
    }


def _applicability_bias(
    rows: Sequence[Mapping[str, object]], labels: Mapping[str, Mapping[str, object]]
) -> dict[str, object]:
    counts: dict[str, dict[str, Counter[str]]] = defaultdict(
        lambda: defaultdict(Counter)
    )
    for row in rows:
        signal = str(row["signal_name"])
        class_name = str(labels[str(row["sample_id"])]["class"])
        counts[signal][class_name]["total"] += 1
        if row.get("applicable"):
            counts[signal][class_name]["applicable"] += 1
    findings: list[dict[str, object]] = []
    for signal, by_class in sorted(counts.items()):
        rates = {
            class_name: values["applicable"] / values["total"]
            for class_name, values in by_class.items()
        }
        spread = max(rates.values()) - min(rates.values())
        if spread >= 0.25:
            findings.append(
                {
                    "signal_name": signal,
                    "applicability_rates": rates,
                    "max_rate_difference": spread,
                    "status": "APPLICABILITY_LEAKAGE_RISK",
                }
            )
    return {
        "risk_threshold": 0.25,
        "finding_count": len(findings),
        "findings": findings,
        "automatic_feature_use_allowed": False,
    }


def _evidence_missingness_bias(
    labels: Mapping[str, Mapping[str, object]], gt: Mapping[str, object]
) -> dict[str, object]:
    records = gt.get("records")
    if not isinstance(records, list):
        raise ValueError("GT records missing")
    limited: set[str] = set()
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("labels"), dict):
            continue
        gt_labels = record["labels"]
        if (
            gt_labels.get("overall_fact_status") == "INSUFFICIENT_EVIDENCE"
            or gt_labels.get("phase2_issue") == "EVIDENCE_MISSING"
        ):
            limited.add(str(record["sample_id"]))
    class_counts = Counter(str(value["class"]) for value in labels.values())
    limited_counts = Counter(str(labels[sample]["class"]) for sample in limited)
    rates = {
        class_name: limited_counts[class_name] / count
        for class_name, count in sorted(class_counts.items())
    }
    spread = max(rates.values()) - min(rates.values())
    return {
        "known_evidence_limitation_samples": len(limited),
        "by_class_count": dict(limited_counts),
        "by_class_rate": rates,
        "max_rate_difference": spread,
        "bias_risk": "EVIDENCE_MISSINGNESS_LABEL_SHORTCUT_RISK"
        if spread >= 0.2
        else "NO_STRONG_CLASS_CONCENTRATION_OBSERVED",
        "evidence_missingness_feature_allowed": False,
    }


def _axis_summary(
    rows: Sequence[Mapping[str, object]],
    labels: Mapping[str, Mapping[str, object]],
    axis: str,
) -> dict[str, object]:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        label_value = str(labels[str(row["sample_id"])][axis])
        grouped[label_value][str(row["computation_status"])] += 1
    return {value: dict(counts) for value, counts in sorted(grouped.items())}


def _subgroup_diagnostics(
    rows: Sequence[Mapping[str, object]],
    labels: Mapping[str, Mapping[str, object]],
    axis: str,
) -> dict[str, object]:
    values = sorted({str(label[axis]) for label in labels.values()})
    output: dict[str, object] = {}
    for value in values:
        comparisons = _comparison(
            rows,
            labels,
            "POISON",
            {"HARD_NEGATIVE"},
            subset_axis=axis,
            subset_value=value,
        )
        strongest = sorted(
            comparisons,
            key=lambda item: abs(float(str(item.get("cliffs_delta_oriented") or 0.0))),
            reverse=True,
        )[:5]
        output[value] = {
            "comparison": "POISON_VS_HARD_NEGATIVE",
            "eligible_signal_count": len(comparisons),
            "strongest_diagnostics": strongest,
            "claim_boundary": "DEVELOPMENT_SET_HYPOTHESIS_GENERATION_ONLY",
        }
    return output


def _view_level_summary(
    availability: Mapping[str, object],
    quality: Mapping[str, object],
    comparisons_hn: Sequence[Mapping[str, object]],
    comparisons_clean: Sequence[Mapping[str, object]],
    redundancy: Mapping[str, object],
    applicability: Mapping[str, object],
) -> dict[str, object]:
    by_view = cast(Mapping[str, Mapping[str, int]], availability["by_view"])
    signal_to_view = {
        definition.signal_name: definition.view.value
        for definition in FIVE_VIEW_SIGNAL_REGISTRY
    }
    constant = set(cast(Sequence[str], quality["constant_signals"]))
    near_constant = set(cast(Sequence[str], quality["near_constant_signals"]))
    redundant_pairs = cast(
        Sequence[Mapping[str, object]], redundancy["highly_correlated_pairs"]
    )
    leakage_findings = cast(Sequence[Mapping[str, object]], applicability["findings"])

    def best(
        rows: Sequence[Mapping[str, object]], view: str
    ) -> Mapping[str, object] | None:
        eligible = [
            row for row in rows if signal_to_view[str(row["signal_name"])] == view
        ]
        if not eligible:
            return None
        return max(
            eligible,
            key=lambda row: abs(float(str(row.get("cliffs_delta_oriented") or 0.0))),
        )

    output: dict[str, object] = {}
    for view in SignalView:
        counts = by_view[view.value]
        total = sum(counts.values())
        computed = counts.get("COMPUTED", 0)
        if computed == total:
            implementation = "READY"
        elif computed > 0:
            implementation = "READY_WITH_LIMITATIONS"
        else:
            implementation = "INPUT_GAP"
        view_signals = {
            name
            for name, signal_view in signal_to_view.items()
            if signal_view == view.value
        }
        output[view.value] = {
            "implementation_status": implementation,
            "availability": {
                **counts,
                "total": total,
                "computed_rate": computed / total,
            },
            "data_quality": {
                "constant_signals": sorted(view_signals & constant),
                "near_constant_signals": sorted(view_signals & near_constant),
            },
            "poison_vs_hard_negative_diagnostic": best(comparisons_hn, view.value),
            "poison_vs_clean_diagnostic": best(comparisons_clean, view.value),
            "redundancy_pair_count": sum(
                str(pair["left"]) in view_signals or str(pair["right"]) in view_signals
                for pair in redundant_pairs
            ),
            "leakage_risk_count": sum(
                str(finding["signal_name"]) in view_signals
                for finding in leakage_findings
            ),
            "detector_readiness": implementation,
        }
    return output


def _readiness(
    availability: Mapping[str, object],
    comparisons: Sequence[Mapping[str, object]],
    applicability: Mapping[str, object],
) -> dict[str, object]:
    by_view = availability["by_view"]
    assert isinstance(by_view, dict)
    temporal = by_view[SignalView.TEMPORAL_VERSION.value]
    retrieval = by_view[SignalView.RETRIEVAL_BEHAVIOR.value]
    assert isinstance(temporal, dict) and isinstance(retrieval, dict)
    temporal_computed = int(temporal.get("COMPUTED", 0))
    retrieval_computed = int(retrieval.get("COMPUTED", 0))
    potential = [
        row
        for row in comparisons
        if isinstance(row.get("cliffs_delta_oriented"), (int, float))
        and abs(float(str(row["cliffs_delta_oriented"]))) >= 0.2
    ]
    if temporal_computed == 0 or not potential:
        decision = "SIGNAL_REPAIR_REQUIRED"
    elif retrieval_computed == 0:
        decision = "READY_WITH_VIEW_LIMITATIONS"
    else:
        decision = "READY_FOR_FIRST_DETECTOR"
    return {
        "decision": decision,
        "temporal_computed_instances": temporal_computed,
        "retrieval_computed_instances": retrieval_computed,
        "poison_vs_hn_potential_signal_count": len(potential),
        "applicability_leakage_finding_count": applicability["finding_count"],
        "label_leakage_blocker": False,
        "formal_detector_training_authorized": False,
    }


def _feasibility_report(
    class_counts: Counter[str],
    availability: Mapping[str, object],
    comparisons_hn: Sequence[Mapping[str, object]],
    comparisons_clean: Sequence[Mapping[str, object]],
    redundancy: Mapping[str, object],
    applicability: Mapping[str, object],
    evidence_bias: Mapping[str, object],
    quality: Mapping[str, object],
    view_summary: Mapping[str, object],
    readiness: Mapping[str, object],
) -> str:
    def strongest(rows: Sequence[Mapping[str, object]]) -> list[Mapping[str, object]]:
        return sorted(
            rows,
            key=lambda row: abs(float(str(row.get("cliffs_delta_oriented") or 0.0))),
            reverse=True,
        )[:5]

    lines = [
        "# Paper 1 Final72 五视角 Signal Feasibility Report V1",
        "",
        "> 这是 Final72 development set 的描述性诊断，不是 Detector 结果、正式测试结果或论文显著性结论。",
        "",
        "## 1. 为什么做这轮",
        "",
        "本轮不是训练分类器，而是检查五种安全证据是否存在、能否稳定提取，以及是否可能区分 Poison 与合法历史 Hard Negative。",
        "",
        "## 2. 数据与物理顺序",
        "",
        f"类别计数：`{dict(class_counts)}`。信号先在无标签投影上提取并锁定，之后才加载实验设计标签。",
        "",
        "## 3. 各 View 实际可用性",
        "",
        "```json",
        json.dumps(availability["by_view"], ensure_ascii=False, indent=2),
        "```",
        "",
        "MLM/PPL 因没有冻结模型而记录为 MODEL_UNAVAILABLE；Retrieval 因没有冻结 query/retrieval trace 而记录为 INPUT_MISSING。",
        "",
        "各 View 的 implementation、data quality、diagnostic、redundancy、leakage 与 readiness 已固化在 `view_level_summary.json`。",
        "",
        "## 4. Poison vs Hard Negative 最强诊断信号",
        "",
    ]
    for row in strongest(comparisons_hn):
        lines.append(
            f"- `{row['signal_name']}`：Cliff's delta={float(str(row['cliffs_delta_oriented'])):.3f}，diagnostic AUROC={float(str(row['diagnostic_auroc'])):.3f}。"
        )
    lines.extend(["", "## 5. Poison vs Clean Current 最强诊断信号", ""])
    for row in strongest(comparisons_clean):
        lines.append(
            f"- `{row['signal_name']}`：Cliff's delta={float(str(row['cliffs_delta_oriented'])):.3f}，diagnostic AUROC={float(str(row['diagnostic_auroc'])):.3f}。"
        )
    lines.extend(
        [
            "",
            "## 6. 无效、重复与不稳定项",
            "",
            f"常量/近常量项和高度相关对见 QA；|rho|≥0.90 的高冗余对为 `{len(cast(Sequence[object], redundancy['highly_correlated_pairs']))}`，本轮自动删除 `0` 项。",
            f"常量 signals：`{list(cast(Sequence[str], quality['constant_signals']))}`；近常量 signals：`{list(cast(Sequence[str], quality['near_constant_signals']))}`。",
            "",
            "## 7. Leakage / artifact 风险",
            "",
            f"Applicability 风险项 `{applicability['finding_count']}`；Evidence missingness：`{evidence_bias['bias_risk']}`。这些字段不得直接作为预测捷径。",
            "",
            "## 8. 是否可以进入 Detector engineering",
            "",
            f"结论：`{readiness['decision']}`。这是下一审批门建议，不等于已经训练 Detector。",
            f"View-level readiness：`{json.dumps({name: cast(Mapping[str, object], value)['detector_readiness'] for name, value in view_summary.items()}, ensure_ascii=False)}`。",
            "",
            "## 9. 必须先解决的问题",
            "",
            "- 建立冻结 query、retriever、corpus、top-k、score 与重复运行 trace，补齐 Retrieval View。",
            "- 冻结可复现 MLM/PPL baseline bundle，或继续明确保持 unavailable。",
            "- 为 current/historical Evidence 增加显式 version_role、effective interval、issuer/publisher/repost role，降低规则代理的不确定性。",
            "- 在正式 scale benchmark 中保存 detector 所需 metadata，且保持 version-chain group-aware split。",
            "",
        ]
    )
    return "\n".join(lines)


def _manifest(output: Path) -> dict[str, object]:
    entries = []
    for path in sorted(item for item in output.rglob("*") if item.is_file()):
        if path.relative_to(output).as_posix() == "manifest/final_manifest.json":
            continue
        entries.append(
            {
                "path": path.relative_to(output).as_posix(),
                "bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    aggregate = sha256_bytes(
        "\n".join(f"{item['path']}\t{item['sha256']}" for item in entries).encode(
            "utf-8"
        )
    )
    return {
        "task_id": TASK_ID,
        "generated_at": utc_now(),
        "entries": entries,
        "aggregate_sha256": aggregate,
    }


def analyze(args: argparse.Namespace) -> None:
    output = args.output.resolve()
    lock_path = output / "lock" / "SIGNAL_MATRIX_PRE_LABEL_LOCK.json"
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if lock.get("status") != "PASS" or not lock.get("label_blind"):
        raise ValueError("pre-label raw lock is not PASS")
    raw_path = output / str(lock["raw_matrix"]["path"])
    if sha256_file(raw_path) != lock["raw_matrix"]["sha256"]:
        raise ValueError("raw matrix changed after lock")
    raw_rows = read_jsonl(raw_path)
    if forbidden_key_hits(raw_rows, FORBIDDEN_KEYS):
        raise ValueError("raw matrix contains label-bearing keys")

    label_load_time = utc_now()
    if label_load_time <= str(lock["timestamp"]):
        raise ValueError("label load timestamp does not follow raw lock")
    gt_identity = require_sha(args.ground_truth, FINAL72_GT_SHA256)
    gt = json.loads(args.ground_truth.read_text(encoding="utf-8"))
    mismatch_rows = read_jsonl(args.mismatch_taxonomy)
    known_evidence_limitation_items = sum(
        row.get("taxonomy") == "EVIDENCE_DEFECT" for row in mismatch_rows
    )
    if known_evidence_limitation_items != 11:
        raise ValueError(
            "Expected 11 known Evidence limitation mismatch items, got "
            f"{known_evidence_limitation_items}"
        )
    design = _design_labels(args.candidate_corpus)
    raw_ids = {str(row["sample_id"]) for row in raw_rows}
    if raw_ids != set(design):
        raise ValueError("raw/design sample ID parity failed")
    gt_ids = {str(row["sample_id"]) for row in gt["records"]}
    if raw_ids != gt_ids:
        raise ValueError("raw/GT sample ID parity failed")

    known_limited = {
        str(row["sample_id"])
        for row in gt["records"]
        if row["labels"]["overall_fact_status"] == "INSUFFICIENT_EVIDENCE"
        or row["labels"]["phase2_issue"] == "EVIDENCE_MISSING"
    }
    analysis_rows: list[dict[str, object]] = []
    for row in raw_rows:
        sample_id = str(row["sample_id"])
        analysis_rows.append(
            {
                **row,
                **design[sample_id],
                "known_evidence_limitation": sample_id in known_limited,
                "analysis_only_labels": True,
                "detector_feature_allowed": False,
            }
        )
    analysis_path = output / "matrix" / "PAPER1_FINAL72_SIGNAL_MATRIX_ANALYSIS_V1.jsonl"
    write_jsonl(analysis_path, analysis_rows)
    analysis_fields = (
        *RAW_FIELDS,
        "class",
        "hkp",
        "stealth",
        "group_id",
        "known_evidence_limitation",
        "analysis_only_labels",
        "detector_feature_allowed",
    )
    analysis_csv = output / "matrix" / "PAPER1_FINAL72_SIGNAL_MATRIX_ANALYSIS_V1.csv"
    write_csv(analysis_csv, analysis_rows, analysis_fields)

    class_counts = Counter(str(value["class"]) for value in design.values())
    hkp_counts = Counter(str(value["hkp"]) for value in design.values())
    stealth_counts = Counter(str(value["stealth"]) for value in design.values())
    group_counts = Counter(str(value["group_id"]) for value in design.values())
    if any(count != 3 for count in group_counts.values()):
        raise ValueError("matched group does not contain exactly three samples")
    class_audit = {
        "class_counts": dict(class_counts),
        "hkp_counts": dict(hkp_counts),
        "stealth_counts": dict(stealth_counts),
        "group_count": len(group_counts),
        "matched_group_size_parity": True,
    }
    write_json(output / "analysis" / "class_distribution_audit.json", class_audit)

    comparisons_hn = _comparison(raw_rows, design, "POISON", {"HARD_NEGATIVE"})
    comparisons_clean = _comparison(raw_rows, design, "POISON", {"CLEAN_CURRENT"})
    comparisons_all = _comparison(
        raw_rows, design, "POISON", {"CLEAN_CURRENT", "HARD_NEGATIVE"}
    )
    comparisons = {
        "claim_boundary": "DEVELOPMENT_SET_DIAGNOSTIC_ONLY_NOT_DETECTOR_RESULT",
        "poison_vs_hard_negative": comparisons_hn,
        "poison_vs_clean_current": comparisons_clean,
        "poison_vs_all_non_poison": comparisons_all,
    }
    write_json(output / "analysis" / "univariate_diagnostics.json", comparisons)
    matched = _matched_analysis(raw_rows, design)
    write_json(output / "analysis" / "matched_group_analysis.json", matched)
    redundancy = _redundancy(raw_rows)
    write_json(output / "analysis" / "signal_redundancy.json", redundancy)
    applicability = _applicability_bias(raw_rows, design)
    write_json(output / "bias" / "applicability_leakage_audit.json", applicability)
    evidence_bias = _evidence_missingness_bias(design, gt)
    write_json(output / "bias" / "EVIDENCE_MISSINGNESS_BIAS_REPORT.json", evidence_bias)

    availability = json.loads(
        (output / "availability" / "signal_availability.json").read_text(
            encoding="utf-8"
        )
    )
    breakdown = {
        "hkp_availability": _axis_summary(raw_rows, design, "hkp"),
        "stealth_availability": _axis_summary(raw_rows, design, "stealth"),
        "hkp_poison_vs_hard_negative_diagnostics": _subgroup_diagnostics(
            raw_rows, design, "hkp"
        ),
        "stealth_poison_vs_hard_negative_diagnostics": _subgroup_diagnostics(
            raw_rows, design, "stealth"
        ),
        "interpretation": "Availability only; separability remains development-set hypothesis generation.",
    }
    write_json(output / "analysis" / "hkp_stealth_breakdown.json", breakdown)
    readiness = _readiness(availability, comparisons_hn, applicability)
    write_json(output / "readiness" / "signal_to_detector_readiness.json", readiness)

    quality = json.loads(
        (output / "qa" / "pre_label_signal_quality.json").read_text(encoding="utf-8")
    )
    view_summary = _view_level_summary(
        availability,
        quality,
        comparisons_hn,
        comparisons_clean,
        redundancy,
        applicability,
    )
    write_json(output / "analysis" / "view_level_summary.json", view_summary)

    report = _feasibility_report(
        class_counts,
        availability,
        comparisons_hn,
        comparisons_clean,
        redundancy,
        applicability,
        evidence_bias,
        quality,
        view_summary,
        readiness,
    )
    report_path = (
        output / "report" / "PAPER1_FINAL72_FIVE_VIEW_SIGNAL_FEASIBILITY_REPORT_V1.md"
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    events_path = output / "events" / "execution_events.jsonl"
    events = read_jsonl(events_path)
    events.append(
        {
            "event": "LABELS_FIRST_LOADED_AFTER_SIGNAL_LOCK",
            "timestamp": label_load_time,
            "raw_lock_timestamp": lock["timestamp"],
            "condition": label_load_time > str(lock["timestamp"]),
            "gt_sha256": gt_identity["sha256"],
        }
    )
    write_jsonl(events_path, events)
    final_qa = {
        "raw_lock_timestamp": lock["timestamp"],
        "label_load_timestamp": label_load_time,
        "labels_first_loaded_after_signal_lock": True,
        "raw_matrix_sha_verified_after_labels": sha256_file(raw_path)
        == lock["raw_matrix"]["sha256"],
        "raw_matrix_forbidden_key_hits": 0,
        "expected_v3_feature_use": 0,
        "gt_value_feature_use": 0,
        "adjudication_feature_use": 0,
        "detector_training_runs": 0,
        "threshold_tuning_runs": 0,
        "formal_test_runs": 0,
        "analysis_matrix": {
            "path": analysis_path.relative_to(output).as_posix(),
            "sha256": sha256_file(analysis_path),
            "rows": len(analysis_rows),
        },
        "ground_truth": gt_identity,
        "known_evidence_limitation_items": known_evidence_limitation_items,
        "known_evidence_limitation_samples": len(known_limited),
        "mismatch_taxonomy_sha256": sha256_file(args.mismatch_taxonomy),
        "readiness": readiness["decision"],
    }
    write_json(output / "qa" / "final_execution_qa.json", final_qa)
    write_json(output / "manifest" / "final_manifest.json", _manifest(output))
    print(json.dumps(final_qa, ensure_ascii=False))


def finalize(args: argparse.Namespace) -> None:
    """Validate the completed evidence tree and documentation closeout."""

    output = args.output.resolve()
    repo = args.repo_root.resolve()
    lock = json.loads(
        (output / "lock" / "SIGNAL_MATRIX_PRE_LABEL_LOCK.json").read_text(
            encoding="utf-8"
        )
    )
    final_qa = json.loads(
        (output / "qa" / "final_execution_qa.json").read_text(encoding="utf-8")
    )
    class_audit = json.loads(
        (output / "analysis" / "class_distribution_audit.json").read_text(
            encoding="utf-8"
        )
    )
    availability = json.loads(
        (output / "availability" / "signal_availability.json").read_text(
            encoding="utf-8"
        )
    )
    required_docs = {
        "PROJECT_MASTER_CONTEXT.md": "READY_WITH_VIEW_LIMITATIONS",
        "README.md": "3,024",
        "docs/governance/current_work_state.md": TASK_ID,
        "docs/governance/experiment_master_record.md": TASK_ID,
        "docs/governance/project_owner_decision_register.md": "PODR-098",
        "docs/governance/research_execution_log.md": "REL-2026-0065",
        "docs/research/stage6_1_hidden_knowledge_poisoning/README.md": (
            "FINAL72_SIGNAL_FEASIBILITY_COMPLETE"
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/agent/experiment_ledger_agentUse.md": (
            TASK_ID
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/experiment_ledger_tingfeng.md": (
            "我们现在不是在“训练分类器”"
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/owner_requirement_register.md": (
            "OR-060"
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/human/research_plan_authority.md": (
            "RPC-009"
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/stage_process/S6.1-P1_work_process.md": (
            "Final72 Five-view Signal Feasibility Execution"
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/benchmark/PAPER1_SIGNAL_TO_SCALE_REQUIREMENT_FEEDBACK_V1.md": (
            "240-group"
        ),
        "docs/research/stage6_1_hidden_knowledge_poisoning/method_engineering/PAPER1_FINAL72_FIVE_VIEW_SIGNAL_FEASIBILITY_REPORT_V1.md": (
            "READY_WITH_VIEW_LIMITATIONS"
        ),
    }
    doc_checks: dict[str, bool] = {}
    for relative, marker in required_docs.items():
        path = repo / relative
        doc_checks[relative] = path.is_file() and marker in path.read_text(
            encoding="utf-8"
        )
    if not all(doc_checks.values()):
        failed = [path for path, passed in doc_checks.items() if not passed]
        raise ValueError(f"documentation closeout failed: {failed}")

    raw_path = output / str(lock["raw_matrix"]["path"])
    raw_rows = read_jsonl(raw_path)
    raw_statuses = {str(row["computation_status"]) for row in raw_rows}
    expected_statuses = {status.value for status in SignalComputationStatus}
    by_view = cast(Mapping[str, Mapping[str, int]], availability["by_view"])
    checks = {
        "final72_gt_sha_exact": final_qa["ground_truth"]["sha256"] == FINAL72_GT_SHA256,
        "signal_registry_42": len(FIVE_VIEW_SIGNAL_REGISTRY) == 42,
        "raw_rows_3024": len(raw_rows) == EXPECTED_RAW_ROWS,
        "raw_unique_lineage_3024": len(
            {(str(row["sample_id"]), str(row["signal_name"])) for row in raw_rows}
        )
        == EXPECTED_RAW_ROWS,
        "raw_sha_locked": sha256_file(raw_path) == lock["raw_matrix"]["sha256"],
        "raw_has_no_forbidden_labels": forbidden_key_hits(raw_rows, FORBIDDEN_KEYS)
        == [],
        "labels_loaded_only_after_lock": final_qa[
            "labels_first_loaded_after_signal_lock"
        ],
        "signal_status_enum_valid": raw_statuses <= expected_statuses,
        "null_not_zero_semantics": all(
            (row["value"] is not None)
            if row["computation_status"] == "COMPUTED"
            else (row["value"] is None)
            for row in raw_rows
        ),
        "expected_feature_leakage_zero": final_qa["expected_v3_feature_use"] == 0,
        "gt_value_feature_leakage_zero": final_qa["gt_value_feature_use"] == 0,
        "adjudication_feature_leakage_zero": final_qa["adjudication_feature_use"] == 0,
        "class_counts_24_each": class_audit["class_counts"]
        == {"CLEAN_CURRENT": 24, "POISON": 24, "HARD_NEGATIVE": 24},
        "matched_groups_24": class_audit["group_count"] == 24
        and class_audit["matched_group_size_parity"],
        "retrieval_gap_720": by_view[SignalView.RETRIEVAL_BEHAVIOR.value].get(
            "INPUT_MISSING"
        )
        == 720,
        "availability_complete": (
            output / "availability" / "signal_availability.json"
        ).is_file(),
        "effect_size_complete": (
            output / "analysis" / "univariate_diagnostics.json"
        ).is_file(),
        "matched_analysis_complete": (
            output / "analysis" / "matched_group_analysis.json"
        ).is_file(),
        "hkp_s_breakdown_complete": (
            output / "analysis" / "hkp_stealth_breakdown.json"
        ).is_file(),
        "redundancy_complete": (
            output / "analysis" / "signal_redundancy.json"
        ).is_file(),
        "applicability_audit_complete": (
            output / "bias" / "applicability_leakage_audit.json"
        ).is_file(),
        "evidence_bias_audit_complete": (
            output / "bias" / "EVIDENCE_MISSINGNESS_BIAS_REPORT.json"
        ).is_file(),
        "no_detector_training": final_qa["detector_training_runs"] == 0,
        "no_threshold_tuning": final_qa["threshold_tuning_runs"] == 0,
        "documentation_closeout_pass": all(doc_checks.values()),
    }
    if not all(checks.values()):
        failed = [name for name, passed in checks.items() if not passed]
        raise ValueError(f"comprehensive validation failed: {failed}")
    write_json(
        output / "qa" / "documentation_closeout.json",
        {
            "task_id": TASK_ID,
            "status": "PASS",
            "checked_at": utc_now(),
            "documents": doc_checks,
            "stage1_5_mutation": 0,
            "prior_evidence_mutation": 0,
        },
    )
    write_json(
        output / "qa" / "comprehensive_validation.json",
        {"task_id": TASK_ID, "status": "PASS", "checks": checks},
    )
    write_json(output / "manifest" / "final_manifest.json", _manifest(output))
    print(json.dumps({"status": "PASS", "checks": len(checks)}, ensure_ascii=False))


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    sub = root.add_subparsers(dest="command", required=True)
    prepare = sub.add_parser("prepare")
    prepare.add_argument("--candidate-corpus", type=Path, required=True)
    prepare.add_argument("--evidence-pool", type=Path, required=True)
    prepare.add_argument("--source-registry", type=Path, required=True)
    prepare.add_argument("--companion-registry", type=Path, required=True)
    prepare.add_argument("--evidence-repair", type=Path, required=True)
    prepare.add_argument("--snapshot-provenance", type=Path, required=True)
    prepare.add_argument("--snapshot-root", type=Path, required=True)
    prepare.add_argument("--output", type=Path, required=True)
    prepare.set_defaults(func=prepare_inputs)

    extract_parser = sub.add_parser("extract")
    extract_parser.add_argument("--output", type=Path, required=True)
    extract_parser.set_defaults(func=extract)

    analyze_parser = sub.add_parser("analyze")
    analyze_parser.add_argument("--output", type=Path, required=True)
    analyze_parser.add_argument("--ground-truth", type=Path, required=True)
    analyze_parser.add_argument("--candidate-corpus", type=Path, required=True)
    analyze_parser.add_argument("--mismatch-taxonomy", type=Path, required=True)
    analyze_parser.set_defaults(func=analyze)

    finalize_parser = sub.add_parser("finalize")
    finalize_parser.add_argument("--output", type=Path, required=True)
    finalize_parser.add_argument("--repo-root", type=Path, required=True)
    finalize_parser.set_defaults(func=finalize)
    return root


def main() -> int:
    args = parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
