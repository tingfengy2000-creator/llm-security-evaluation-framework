"""Synthetic-only tests: no real annotations, workbook authoring or labels."""
import unittest

from scripts.research.validate_core144_d1_human_phase2_returns import (
    FIELDS, SHEET, comparison_allowed, difference_kind, readonly_differences,
    row_checks, strict_receipt_gate,
)


def row():
    return dict(zip(FIELDS, ("CURRENTLY_CONSISTENT", "NOT_PRESENT", "NOT_PRESENT", "NOT_APPLICABLE",
                            "E1", "NONE", "NO", "SUFFICIENT", "E1 supports the statement.", "")))


class ReceiptTests(unittest.TestCase):
    def test_legal_row(self):
        self.assertEqual(row_checks(row(), "NO", {"E1"})["legal_categorical_cells"], 8)

    def test_no_enum_trim(self):
        data = row()
        data["overall_fact_status"] += " "
        self.assertEqual(row_checks(data, "NO", {"E1"})["errors"][0]["code"], "ILLEGAL_ENUM")

    def test_reason_required(self):
        data = row()
        data["phase2_reason"] = " \n"
        self.assertTrue(row_checks(data, "NO", {"E1"})["errors"])

    def test_answer_formula_blocked(self):
        data = row()
        data["reviewer_note"] = "=A1"
        self.assertTrue(row_checks(data, "NO", {"E1"})["errors"])

    def test_whitespace_not_waiver(self):
        diff = readonly_differences({(SHEET, 2, 4): "\nFictional evidence "}, {(SHEET, 2, 4): "Fictional evidence"})
        self.assertEqual(diff[0]["kind"], "BOUNDARY_WHITESPACE_ONLY")
        self.assertFalse(strict_receipt_gate([], diff))

    def test_blank_storage_diagnostic(self):
        diff = readonly_differences({("Fictional", 1, 1): None}, {("Fictional", 1, 1): ""})
        self.assertTrue(strict_receipt_gate([], diff))

    def test_interior_change_not_boundary(self):
        self.assertEqual(difference_kind("a b", "ab"), "CONTENT_CHANGE")

    def test_only_answer_region_is_writable(self):
        before = {(SHEET, 2, 11): None, (SHEET, 146, 11): None}
        after = {(SHEET, 2, 11): "CURRENTLY_CONSISTENT", (SHEET, 146, 11): "NEW"}
        self.assertEqual(len(readonly_differences(before, after)), 1)

    def test_zero_rule(self):
        data = row()
        data["overall_fact_status"] = "FACTUAL_CONFLICT"
        data["minimum_external_evidence_needed"] = "ZERO_EXTERNAL_EVIDENCE_REQUIRED"
        self.assertFalse(row_checks(data, "YES", {"E1"})["consistency_flags"])
        self.assertIn("ZERO_WITHOUT_OWN_LOCKED_PHASE1_LOCAL_YES", row_checks(data, "NO", {"E1"})["consistency_flags"])

    def test_nonconflict_minimum(self):
        data = row()
        data["minimum_external_evidence_needed"] = "ONE_OFFICIAL_EVIDENCE"
        self.assertTrue(row_checks(data, "NO", {"E1"})["consistency_flags"])

    def test_unsupplied_e2(self):
        data = row()
        data["evidence_selection"] = "E1+E2"
        self.assertIn("UNSUPPLIED_EVIDENCE_SELECTED", row_checks(data, "NO", {"E1"})["consistency_flags"])

    def test_reference_only_lead(self):
        data = row()
        data["phase2_reason"] = "E2 is not needed; E1 alone is sufficient."
        checks = row_checks(data, "NO", {"E1", "E2"})
        self.assertFalse(checks["consistency_flags"])
        self.assertTrue(checks["review_leads"])

    def test_one_held_gate_prevents_join(self):
        self.assertFalse(comparison_allowed(False, True))
        self.assertTrue(comparison_allowed(True, True))


if __name__ == "__main__":
    unittest.main()
