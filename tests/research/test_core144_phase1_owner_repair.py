"""Synthetic checks only; no actual reviewer annotations are generated."""

import tempfile
import unittest
from pathlib import Path

from scripts.research.repair_core144_d2_d3_phase1_candidates import (
    derive_path,
    repaired_row,
    surface,
    write_new,
)


class OwnerRepairTests(unittest.TestCase):
    def test_additive_identity_and_frozen_fields(self) -> None:
        old = {
            "sample_id": "group-C-V1",
            "candidate_text": "原句",
            "blind_review_id": "old",
            "group_id": "group",
            "construction_role": "CLEAN_CURRENT",
            "family_cluster_id": "family",
        }
        new = repaired_row(old, {"text": "修复句"}, "stamp")
        self.assertEqual(new["group_id"], old["group_id"])
        self.assertEqual(new["construction_role"], old["construction_role"])
        self.assertEqual(new["family_cluster_id"], old["family_cluster_id"])
        self.assertNotEqual(new["blind_review_id"], old["blind_review_id"])
        self.assertEqual(old["candidate_text"], "原句")
        self.assertEqual(new, repaired_row(old, {"text": "修复句"}, "stamp"))

    def test_unchanged_recipe_fails(self) -> None:
        with self.assertRaises(ValueError):
            repaired_row({"candidate_text": "原句"}, {"text": "原句"}, "stamp")

    def test_output_does_not_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "artifact.json"
            write_new(path, {"first": True})
            before = path.read_bytes()
            with self.assertRaises(FileExistsError):
                write_new(path, {"second": True})
            self.assertEqual(path.read_bytes(), before)

    def test_single_page_is_not_multi_even_with_proof_object(self) -> None:
        self.assertEqual(
            derive_path([], {"single_full_official_page": "official"})[:2],
            ("S2", "ONE_OFFICIAL_EVIDENCE"),
        )

    def test_multi_joint(self) -> None:
        self.assertEqual(
            derive_path(
                [],
                {
                    "left_only": "insufficient",
                    "right_only": "insufficient",
                    "joint": "sufficient",
                },
            )[:2],
            ("S3", "MULTI_EVIDENCE_OR_VERSION_CHAIN"),
        )

    def test_s1_same_field_conflict_not_target_driven(self) -> None:
        atoms = [
            {"declaration": {"field_identity": "same", "asserted_value": value}}
            for value in (5, 10)
        ]
        self.assertEqual(derive_path(atoms, None)[0], "S1")

    def test_unknown_path_fails_closed(self) -> None:
        with self.assertRaises(ValueError):
            derive_path([], {"unknown": "not proof"})

    def test_surface_separates_narration_and_intrinsic_conflict(self) -> None:
        rows = [
            {
                "blind_review_id": "x",
                "construction_role": "POISON",
                "candidate_text": "这里比较机关。同一机关又有不同身份。",
            }
        ]
        audit = surface(rows)
        self.assertEqual(audit["semantic_families"][0]["counts"]["POISON"], 1)
        family = next(
            f
            for f in audit["semantic_families"]
            if f["family"] == "same_subject_transition"
        )
        self.assertEqual(family["counts"]["POISON"], 1)
        self.assertEqual(
            family["interpretation"],
            "INTRINSIC_SAME_SCOPE_RELATION_NOT_AUTOMATIC_SHORTCUT",
        )


if __name__ == "__main__":
    unittest.main()
