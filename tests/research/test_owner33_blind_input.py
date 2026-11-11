"""Fictional checks for the Owner33 public validator."""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


def load_module():
    path = Path(__file__).resolve().parents[2] / "scripts/research/validate_owner33_blind_input.py"
    spec = importlib.util.spec_from_file_location("validate_owner33_blind_input", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Owner33ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.mod = load_module()

    def test_clean_blob_has_no_banned_field(self) -> None:
        self.assertIsNone(self.mod.banned_field('{"world_id":"w-1","query":"问","text":"摘录"}'))

    def test_gold_key_is_rejected(self) -> None:
        self.assertEqual(self.mod.banned_field('{"gold":"hidden"}'), "gold")

    def test_word_inside_text_is_not_a_field(self) -> None:
        self.assertIsNone(self.mod.banned_field('{"text":"这里出现 role 这个词，但不是字段"}'))


if __name__ == "__main__":
    unittest.main()
