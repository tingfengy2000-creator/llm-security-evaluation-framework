"""Synthetic checks, never real Candidate/label fixtures."""

import tempfile
import unittest
from pathlib import Path

from scripts.research.d1_exploratory_detection import (
    family_folds,
    fit_configuration,
    lock_predictions,
    metrics,
    predict_oof,
)
from scripts.research.lock_d1_exploratory_inputs import FILENAMES, lock_inputs


class DevelopmentDiagnosticTests(unittest.TestCase):
    def test_family_isolation_and_exact_oof(self):
        ids = ["a", "b", "c", "d", "e", "f"]
        mapping = {i: str(n // 2) for n, i in enumerate(ids)}
        folds = family_folds(ids, mapping)
        self.assertEqual(len(folds), 3)
        self.assertEqual(
            sorted(i for f in folds for i in f["test_indices"]), list(range(6))
        )
        for f in folds:
            self.assertFalse(
                {mapping[ids[i]] for i in f["test_indices"]}
                & {mapping[ids[i]] for i in f["train_indices"]}
            )

    def test_one_family_invalid(self):
        with self.assertRaises(ValueError):
            family_folds(["a", "b"], {"a": "same", "b": "same"})

    def test_extra_label_field_rejected_at_features(self):
        with self.assertRaises(ValueError):
            predict_oof(
                [{"candidate_id": "x", "candidate_text": "虚构句", "label": 1}],
                {"x": 1},
                [],
            )

    def test_no_labels_in_prediction_lock(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                lock_predictions(
                    Path(d) / "p.jsonl", [{"candidate_id": "x", "label": 1}]
                )

    def test_no_nested_family_leakage(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                lock_predictions(
                    Path(d) / "p.jsonl",
                    [
                        {
                            "candidate_id": "x",
                            "feature_availability": {"family": "forbidden"},
                        }
                    ],
                )

    def test_fixed_configuration(self):
        c = fit_configuration()
        self.assertEqual(c["threshold"], 0.5)
        self.assertEqual(c["model"]["C"], 1.0)
        self.assertEqual(c["vectorizer"]["ngram_range"], [2, 3])
        self.assertFalse(c["hyperparameter_search"])

    def test_metric_denominators_and_hn(self):
        rows = [
            {
                "label": 1,
                "derived_s": "S1",
                "oof_prediction": 1,
                "oof_probability": 0.8,
                "true_class": "POISON",
            },
            {
                "label": 1,
                "derived_s": "S2",
                "oof_prediction": 0,
                "oof_probability": 0.2,
                "true_class": "POISON",
            },
            {
                "label": 0,
                "derived_s": None,
                "oof_prediction": 1,
                "oof_probability": 0.7,
                "true_class": "HARD_NEGATIVE",
            },
            {
                "label": 0,
                "derived_s": None,
                "oof_prediction": 0,
                "oof_probability": 0.1,
                "true_class": "CLEAN_CURRENT",
            },
        ]
        m = metrics(rows)
        self.assertEqual(m["S1_Recall"], 1)
        self.assertEqual(m["S2_Recall"], 0)
        self.assertIsNone(m["S3_Recall"])
        self.assertEqual(m["HN_FPR"], 1)
        self.assertEqual(m["Overall_Recall"], 0.5)

    def test_missingness_not_zero_risk(self):
        self.assertIsNone(metrics([])["Overall_Recall"])

    def test_raw_lock_is_exact_and_exclusive(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            source = base / "source"
            source.mkdir()
            for n in FILENAMES:
                (source / n).write_bytes(b"raw\r\nnot necessarily parseable")
            lock_inputs(source, base / "out")
            for n in FILENAMES:
                self.assertEqual(
                    (source / n).read_bytes(), (base / "out" / n).read_bytes()
                )
                (base / "out" / n).chmod(0o666)
            with self.assertRaises(ValueError):
                lock_inputs(source, base / "out")


if __name__ == "__main__":
    unittest.main()
