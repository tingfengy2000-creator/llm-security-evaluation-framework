"""Test fixed receipt rules on invented snippets without experiment inputs."""

from dataclasses import replace
from pathlib import Path

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner27_version_guard import (
    Receipt,
    receipt_filter,
    visible_date_filter,
)

BASE = Receipt("a", "ha", "line", "X", "fact", "v2", "2025-01-01", None, "same", "https://example.test")
OLD = replace(BASE, document="c", content_sha256="hc", version="v1", start="2024-01-01", end="2025-01-01")
NEAR = replace(BASE, document="b", content_sha256="hb", scope="Y")
DOCS = [("a", "ha"), ("b", "hb"), ("c", "hc"), ("d", "forged"), ("e", "unknown")]
REGISTRY = {"a": BASE, "b": NEAR, "c": OLD, "d": replace(BASE, document="d")}
PARENT = (4,)


@pytest.mark.parametrize(("mode", "kept"), [("simple", (0, 4)), ("joint", (0, 1, 4)), ("no_scope", (0, 1, 4))])
def test_same_budget_false_receipt_hash_cannot_restore(mode: str, kept: tuple[int, ...]) -> None:
    actual, reason, added = receipt_filter(PARENT, DOCS, REGISTRY, "2025-01-01", "X", mode)
    assert actual == kept
    assert set(added) == set(kept) - {4}
    assert reason == "BOUND_SCOPE_SUPPORT"


def test_missing_scope_cannot_become_anchor_with_joint() -> None:
    docs = DOCS[1:]
    assert receipt_filter((3,), docs, REGISTRY, "2025-01-01", "X", "joint") == (
        (3,), "NO_APPLICABLE_ANCHOR", (),
    )


def test_old_receipt_uses_half_open_effective_interval() -> None:
    old, _, _ = receipt_filter(PARENT, DOCS, REGISTRY, "2024-12-31", "X", "joint")
    current, _, _ = receipt_filter(PARENT, DOCS, REGISTRY, "2025-01-01", "X", "joint")
    assert old == (2, 4)
    assert current == (0, 1, 4)


def test_conflicting_exact_anchors_fall_back() -> None:
    register = {**REGISTRY, "b": replace(NEAR, scope="X", normalized_value_sha256="other")}
    assert receipt_filter(PARENT, DOCS, register, "2025-01-01", "X", "joint") == (
        PARENT, "ANCHOR_CONFLICT", (),
    )


def test_visible_date_baseline_can_prefer_forged_date() -> None:
    texts = ["旧说自2024年1月1日起", "现行自2025年1月1日起", "自2025年1月3日起另作规定", "未写日期"]
    assert visible_date_filter(texts, "2025-01-04") == (2, 3)
    assert visible_date_filter(texts, "2025-01-02") == (1, 3)
    assert visible_date_filter(texts, "2023-01-01") == (3,)


def test_no_label_access_from_retrieval_or_guard(tmp_path: Path) -> None:
    import sys

    sys.path.insert(0, str(Path("scripts/research").resolve()))
    from run_chinese5060_owner27 import audit_hook

    hidden = tmp_path / "evaluator-only" / "sample.json"
    for stage in ("query", "retrieve", "predict"):
        with pytest.raises(PermissionError, match="EVALUATOR_ONLY_PATH_DENIED"):
            audit_hook(tmp_path, stage, [])("open", (str(hidden),))
    with pytest.raises(PermissionError, match="QUERY_VIEW_ONLY"):
        audit_hook(tmp_path, "query", [])("open", (str(tmp_path / "inputs" / "worlds.json"),))
    audit_hook(tmp_path, "evaluate", [])("open", (str(hidden),))
