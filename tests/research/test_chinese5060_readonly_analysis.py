import hashlib

import pytest

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.readonly_analysis import VerifiedReader, flip_key, stage_features


def row(scores, n, removed):
    return {"world_id": "synthetic", "status": "PASS", "observations": {"n_adv": n, "n_tfidf": 1,
        "frequency_scores": scores, "equal_frequency_score_pairs": sum(scores[i] == scores[j] for i in range(5) for j in range(i+1, 5))},
        "removed_indices": removed, "latency_seconds": 0.01}


def test_ties_below_cutoff_do_not_imply_boundary_tie():
    feature = stage_features(row([.8, .8, 0., 0., 0.], 2, [0, 1]))
    assert feature["any_score_tie"] and not feature["boundary_tie"]


def test_lower_index_boundary_choice_is_reconstructed():
    feature = stage_features(row([.8, .8, 0., 0., 0.], 1, [0]))
    assert feature["boundary_tie"] and feature["score_order"][:2] == [0, 1]
    with pytest.raises(ValueError, match="SAVED_SCORES"):
        stage_features(row([.8, .8, 0., 0., 0.], 1, [1]))


def test_no_synthetic_scores_if_trace_missing():
    value = row([0., 0., 0., 0., 0.], 1, [0])
    del value["observations"]["frequency_scores"]
    assert stage_features(value)["stage2_status"] == "INSUFFICIENT_TRACE"


def test_reader_denies_unknown_before_io_and_detects_tamper(tmp_path):
    p = tmp_path / "allowed.json"
    p.write_bytes(b"{}")
    reader = VerifiedReader(tmp_path, {"allowed.json": hashlib.sha256(b"{}").hexdigest()})
    assert reader.json("allowed.json") == {}
    with pytest.raises(PermissionError, match="DENIED_BEFORE_IO"):
        reader.read("synthetic_denied/nonexistent.json")
    p.write_bytes(b"changed")
    with pytest.raises(ValueError, match="INPUT_HASH"):
        reader.read("allowed.json")


def test_all_four_flip_cells_are_distinct():
    assert {flip_key(a, b) for a in (False, True) for b in (False, True)} == {"00", "01", "10", "11"}
