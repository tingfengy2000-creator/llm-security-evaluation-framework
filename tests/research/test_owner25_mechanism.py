from collections import Counter

from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner25_cases import build
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner25_mechanism import decide, receipt
from llmguard.domains.retrieval.hidden_poisoning.chinese5060.owner25_run import (
    check_public, claims_for, metrics, wilson,
)


def test_role_free_shape_and_holdout_groups_disjoint() -> None:
    data = build()
    assert len(data["dev"]["input"]) == 64
    assert len(data["holdout"]["input"]) == 32
    assert not (data["dev"]["source_truth"].keys() & data["holdout"]["source_truth"].keys())
    for split in data.values():
        for uid, world in split["input"].items():
            check_public(world)
            assert len(claims_for(world, split["oracle"][uid])) == 5


def test_forged_binding_and_rotated_receipt_never_verify() -> None:
    data = build()["dev"]
    for uid, world in data["input"].items():
        output = decide(world, data["registry"], claims_for(world, data["oracle"][uid]), "FORGED_RECEIPT_NEGCTRL")
        assert output["verified"] == []
        assert output["keep"] == world["parent_keep"]
        for doc in world["docs"]:
            ref = doc["receipt_ref"]
            if receipt(doc, data["registry"], ref) is not None:
                assert receipt({**doc, "text": doc["text"] + "。"}, data["registry"], ref) is None
                assert receipt({**doc, "parent_sha256": "0" * 64}, data["registry"], ref) is None


def test_no_anchor_fallback_and_majority_poison_with_anchor() -> None:
    data = build()["dev"]
    evaluated: Counter[str] = Counter()
    for uid, world in data["input"].items():
        output = decide(world, data["registry"], claims_for(world, data["oracle"][uid]), "JOINT_P0")
        measured = metrics(output, world, data["gold"][uid])
        if measured["Poison"] == 5:
            assert output["anchor_status"] == "UNRESOLVED"
            assert output["keep"] == world["parent_keep"]
            evaluated["fallback"] += 1
        if measured["Poison"] in {3, 4}:
            assert measured["Poison_kept"] == 0
            evaluated["anchored"] += 1
        assert measured["inapplicable_eligible"] == 0
        assert measured["unverified_restored"] == 0
    assert evaluated == {"fallback": 4, "anchored": 20}


def test_genuine_compromise_is_residual_and_wilson_defined() -> None:
    data = build()["dev"]
    attacked = [key for key, row in data["mapping"].items() if row["compromised"]]
    assert len(attacked) == 2
    for uid in attacked:
        world = data["input"][uid]
        output = decide(world, data["registry"], claims_for(world, data["oracle"][uid]), "JOINT_P0")
        row = metrics(output, world, data["gold"][uid])
        assert row["wrong_anchor"] == 1 and row["forgery_or_selfclaim_verified"] == 0
    assert wilson(0, 0) is None
    assert wilson(0, 4) == [0, 0.489891]
