import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from codeguarder.stage5_paper.attacks.loader import load_attack_matrix
from codeguarder.stage5_paper.attacks.renderer import render_prompt
from codeguarder.stage5_paper.proxy.service import ProxyService


class RecordingProvider:
    def __init__(self, output, events):
        self.output = output
        self.events = events

    def generate(self, messages, model, seed):
        self.events.append("upstream_call")
        return self.output


class OutputOnlyBehaviorTests(unittest.TestCase):
    def test_raw_hash_precedes_output_guard(self):
        sample = load_attack_matrix(ROOT / "data" / "stage5_paper")[6]
        events = []
        service = ProxyService(RecordingProvider("I hate humans", events))
        result = service.process(
            {
                "model": "mock",
                "messages": list(render_prompt(sample.prompt).messages),
                "seed": 42,
            },
            guard_code="O",
            sample=sample,
            events=events,
        )
        self.assertEqual(
            ["upstream_call", "raw_hash", "output_guard", "detectors"], events
        )
        self.assertTrue(result.audit["upstream_called"])
        self.assertFalse(result.audit["input_blocked"])
        self.assertTrue(result.audit["raw_model_output_hash"])
        self.assertNotIn("raw_model_output", result.audit)


if __name__ == "__main__":
    unittest.main()
