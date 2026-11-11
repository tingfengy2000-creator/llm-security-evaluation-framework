"""Fictional Owner32 source-availability checks. No network and no real gold."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[2] / "scripts/research/owner32_source_availability.py"
    spec = importlib.util.spec_from_file_location("owner32_source_availability", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class SourceAvailabilityTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_module()

    def usable_record(self) -> dict:
        return {
            "id": "FICTION-1",
            "url": "https://example.test/version",
            "effective_from": "2020-01-01",
            "superseded_on": "2024-01-01",
            "scope": "只适用于虚构对象甲，不适用于虚构对象乙。",
            "rights_status": "RIGHTS_CLEARED",
            "outbound_status": "AUTHORIZED",
            "independent_receipt_status": "FROZEN",
            "document_sha256": "a" * 64,
            "tls_receipt_sha256": "b" * 64,
            "access_status": "METADATA_READ",
        }

    def test_complete_fictional_record_is_usable(self) -> None:
        decision = self.mod.assess(self.usable_record())
        self.assertTrue(decision["usable"])
        self.assertEqual(decision["reasons"], [])
        self.assertEqual(decision["tls_status"], "RECEIPT_PRESENT")

    def test_missing_document_hash_is_not_usable(self) -> None:
        record = self.usable_record()
        record["document_sha256"] = ""
        decision = self.mod.assess(record)
        self.assertFalse(decision["usable"])
        self.assertIn("NO_DOCUMENT_BYTES_HASH", decision["reasons"])

    def test_answer_card_field_is_rejected(self) -> None:
        record = self.usable_record()
        record["gold_value"] = "虚构数值"
        decision = self.mod.assess(record)
        self.assertFalse(decision["usable"])
        self.assertIn("ORACLE_CARD_FIELD", decision["reasons"])


if __name__ == "__main__":
    unittest.main()
