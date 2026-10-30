"""CPU checks for the fixed Oracle claim-alignment prompt."""
from __future__ import annotations

import inspect

from pathlib import Path

from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_oracle_align import (
    CLAIM_ALIGNMENT_SUFFIX,
    aligned_messages,
    require_seal,
    research_judgment,
)
from llmguard.domains.retrieval.hidden_poisoning.method_engineering.llm_verification import SYSTEM_PROMPT, messages, sha_text


def evidence(text: str, uid: str) -> dict:
    return {"uid": uid, "document_uid": "DOC-" + uid, "title": uid, "official_url": "SYNTHETIC", "text": text, "text_sha256": sha_text(text), "metadata": {}}


def test_only_the_system_suffix_changes_and_evidence_order_stays() -> None:
    row = {"candidate_id": "SYN", "candidate_text": "甲规定为十日。", "evidence": [evidence("第一段。", "E1"), evidence("", "E2")]}
    original = messages(row)
    aligned = aligned_messages(row)
    assert original[1]["content"] == aligned[1]["content"]
    assert aligned[0]["content"] == SYSTEM_PROMPT + "\n" + CLAIM_ALIGNMENT_SUFFIX
    assert "逐断言对齐核验" not in SYSTEM_PROMPT
    assert aligned[1]["content"].index("E1") < aligned[1]["content"].index("E2")
    protocol = (Path(__file__).resolve().parents[2] / "docs/research/stage6_1_hidden_knowledge_poisoning/core144/vace_lite/VACE_L0_ORACLE_CLAIM_ALIGNMENT_V1.md").read_text(encoding="utf-8")
    assert CLAIM_ALIGNMENT_SUFFIX in protocol


def test_historical_parser_and_generation_contract_stay_untouched() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    verifier = (root / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/llm_verification.py").read_text(encoding="utf-8")
    worker = (root / "src/llmguard/domains/retrieval/hidden_poisoning/method_engineering/l0_worker.py").read_text(encoding="utf-8")
    old_evaluator = (root / "scripts/research/evaluate_l0_worker.py").read_text(encoding="utf-8")
    assert "CLAIM_ALIGNMENT_SUFFIX" not in verifier
    assert "messages(row)" in worker
    assert 'lock["rows"] != 240' in old_evaluator


def test_inference_cannot_read_labels_or_sealed_predictions() -> None:
    from llmguard.domains.retrieval.hidden_poisoning.method_engineering.l0_oracle_align import infer_aligned

    source = inspect.getsource(infer_aligned)
    module = inspect.getsource(inspect.getmodule(infer_aligned))
    assert "labels.jsonl" not in source
    assert "FULL01_PREDICTIONS" not in source
    assert "PRIVATE_CASE_REVIEW" not in source
    assert "_deny(" in source
    assert "SEALED_REFERENCE_FORBIDDEN_DURING_INFERENCE" in module


def test_incomplete_predictions_cannot_be_scored() -> None:
    try:
        require_seal({"rows": 119, "raw": {}}, 119)
    except RuntimeError as exc:
        assert "INCOMPLETE" in str(exc)
    else:
        raise AssertionError("119 rows were accepted")


def test_research_judgment_does_not_treat_recall_alone_as_success() -> None:
    assert research_judgment(15, 14, 4, 4, 2, 2) == "DETECTION_UP_WITHOUT_EXTRA_FPR_ON_THIS_DEV_BATCH"
    assert research_judgment(15, 14, 5, 4, 2, 2) == "TRADEOFF_FPR_INCREASED"
    assert research_judgment(14, 14, 4, 4, 2, 2) == "NO_DETECTION_GAIN_SHOWN"
    assert research_judgment(13, 14, 4, 4, 2, 2) == "NO_DETECTION_GAIN_SHOWN"
