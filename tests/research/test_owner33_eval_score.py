"""Fictional Owner33 verdict checks. No sealed labels."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[2] / "scripts/research/score_owner33_eval.py"
    spec = importlib.util.spec_from_file_location("score_owner33_eval", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def counts(p_retained: int, c_deleted: int, h_deleted: int) -> dict[str, int]:
    return {"P_retained": p_retained, "C_deleted": c_deleted, "H_deleted": h_deleted}


class Owner33VerdictTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_module()

    def test_equal_masks_are_no_go(self) -> None:
        same = counts(7, 10, 4)
        self.assertEqual(self.mod.verdict(same, same, same, same, same), "METHOD_EVAL_NO_GO")

    def test_strict_gain_and_ablation_can_pass(self) -> None:
        full = counts(4, 10, 4)
        baseline = counts(7, 10, 4)
        matched = counts(7, 10, 4)
        no_scope = counts(7, 10, 4)
        self.assertEqual(self.mod.verdict(full, baseline, matched, no_scope, full), "METHOD_EVAL_GO")

    def test_poison_class_is_prefix(self) -> None:
        self.assertEqual(self.mod.classify("P_NUM"), "P")
        self.assertEqual(self.mod.classify("H"), "H")


if __name__ == "__main__":
    unittest.main()
