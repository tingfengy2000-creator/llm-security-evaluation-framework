"""Synthetic guardrails for proposal-only bounded annotation review."""
import unittest

from scripts.research.core144_d1_bounded54_review import (
    check_proposals, evidence_witness, validate_coverage,
)


class BoundedReviewTests(unittest.TestCase):
    def test_exact_coverage_and_order(self):
        validate_coverage([{'comparison_id': 'x'}], [{'comparison_id': 'x'}], 1)

    def test_duplicate_rejected(self):
        with self.assertRaises(ValueError):
            validate_coverage([{'comparison_id': 'x'}] * 2, [{'comparison_id': 'x'}] * 2, 2)

    def test_missing_extra_or_reordered_rejected(self):
        for ids in (['x'], ['x', 'z'], ['y', 'x']):
            with self.assertRaises(ValueError):
                validate_coverage([{'comparison_id': x} for x in ['x', 'y']],
                                  [{'comparison_id': x} for x in ids], 2)

    def test_canonical_proposal(self):
        check_proposals({'version_claim_status': 'NOT_PRESENT'})

    def test_illegal_enum_rejected(self):
        with self.assertRaises(ValueError):
            check_proposals({'overall_fact_status': 'SAFE'})

    def test_process_field_never_reconstructed(self):
        with self.assertRaises(ValueError):
            check_proposals({'evidence_selection': 'E1+E2'})

    def test_unknown_field_rejected(self):
        with self.assertRaises(ValueError):
            check_proposals({'new_label': 'x'})

    def test_witness_exact_offset_and_spacing(self):
        text = '标题。 第七条 女职工享受 98 天产假。结束。'
        w = evidence_witness(text, '享受98天产假')
        self.assertEqual(text[w['start']:w['end']], w['quote'])
        self.assertIn('98 天', w['quote'])

    def test_witness_cannot_be_invented(self):
        with self.assertRaises(ValueError):
            evidence_witness('唯一冻结事实', '新增事实')


if __name__ == '__main__':
    unittest.main()
