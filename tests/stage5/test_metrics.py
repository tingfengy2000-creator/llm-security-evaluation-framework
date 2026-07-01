import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from codeguarder.metrics.metrics import compute_metrics
from codeguarder.evaluation.result_collector import collect_metrics


class MetricsTests(unittest.TestCase):
    def test_core_rates(self):
        records = [
            {
                "benign_sample": False,
                "final_risk": True,
                "raw_model_risk": True,
                "input_blocked": False,
                "output_blocked": False,
                "upstream_called": True,
                "failure_types": ["T1", "T2"],
                "latency_ms": 100,
            },
            {
                "benign_sample": False,
                "final_risk": False,
                "raw_model_risk": True,
                "input_blocked": True,
                "output_blocked": False,
                "upstream_called": False,
                "failure_types": ["T1"],
                "latency_ms": 20,
            },
        ]
        metrics = compute_metrics(records)
        self.assertEqual(50.0, metrics["asr_percent"])
        self.assertEqual(50.0, metrics["input_block_rate_percent"])
        self.assertEqual(50.0, metrics["upstream_call_rate_percent"])
        self.assertEqual(50.0, metrics["detector_miss_rate_percent"])

    def test_guard_bypass_denominator_is_guard_enabled_attacks(self):
        records = [
            {
                "benign_sample": False,
                "final_risk": True,
                "raw_model_risk": True,
                "input_guard_enabled": False,
                "output_guard_enabled": False,
                "input_blocked": False,
                "output_blocked": False,
                "upstream_called": True,
                "failure_types": ["T1"],
                "latency_ms": 100,
            },
            {
                "benign_sample": False,
                "final_risk": True,
                "raw_model_risk": True,
                "input_guard_enabled": True,
                "output_guard_enabled": False,
                "input_blocked": False,
                "output_blocked": False,
                "upstream_called": True,
                "failure_types": ["T1", "T3"],
                "latency_ms": 110,
            },
        ]
        self.assertEqual(100.0, compute_metrics(records)["guard_bypass_rate_percent"])

    def test_latency_overhead_is_relative_to_passthrough(self):
        records = []
        for mode, latency in (
            ("passthrough", 100),
            ("input-only", 120),
            ("output-only", 90),
            ("full-guard", 110),
        ):
            records.append(
                {
                    "sample_id": "s1",
                    "category": "prompt_injection",
                    "guard_mode": mode,
                    "benign_sample": False,
                    "final_risk": False,
                    "raw_model_risk": False,
                    "input_guard_enabled": mode in {"input-only", "full-guard"},
                    "output_guard_enabled": mode in {"output-only", "full-guard"},
                    "input_blocked": False,
                    "output_blocked": False,
                    "upstream_called": True,
                    "failure_types": [],
                    "latency_ms": latency,
                }
            )
        rows = collect_metrics(records)
        input_only = next(
            row
            for row in rows
            if row["scope"] == "mode" and row["guard_mode"] == "input-only"
        )
        self.assertEqual(20.0, input_only["latency_overhead_percent"])

    def test_detector_miss_denominator_is_raw_risky_attacks(self):
        records = [
            {
                "benign_sample": False,
                "raw_model_risk": True,
                "failure_types": ["T1", "T2"],
            },
            {
                "benign_sample": False,
                "raw_model_risk": False,
                "failure_types": [],
            },
        ]
        self.assertEqual(
            100.0,
            compute_metrics(records)["detector_miss_rate_percent"],
        )
