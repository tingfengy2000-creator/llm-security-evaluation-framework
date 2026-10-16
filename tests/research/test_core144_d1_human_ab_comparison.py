"""Synthetic comparisons only; no construction mapping or real annotations."""
import unittest

from scripts.research.compare_core144_d1_human_annotations import (
    agreement, exact_pairs, exception_applies, partitions,
)


class ComparisonTests(unittest.TestCase):
    def test_reordered_rows_join_by_text(self):
        a=[{'candidate_text':'fiction A'}, {'candidate_text':'fiction B'}]
        b=list(reversed(a))
        self.assertEqual([(x['candidate_text'],y['candidate_text']) for x,y in exact_pairs(a,b,2)], [('fiction A','fiction A'),('fiction B','fiction B')])

    def test_no_trim_join(self):
        with self.assertRaises(ValueError):
            exact_pairs([{'candidate_text':'fiction'}],[{'candidate_text':' fiction'}],1)

    def test_duplicate_fails_closed(self):
        with self.assertRaises(ValueError):
            exact_pairs([{'candidate_text':'same'}]*2,[{'candidate_text':'same'}]*2,2)

    def test_missing_fails_closed(self):
        with self.assertRaises(ValueError):
            exact_pairs([{'candidate_text':'A'}],[{'candidate_text':'B'}],1)

    def test_observed_agreement(self):
        result=agreement(['YES','NO','YES','NO'],['YES','NO','NO','YES'])
        self.assertEqual(result['agree'],2)
        self.assertEqual(result['cohen_kappa'],0)

    def test_constant_kappa_not_invented(self):
        result=agreement(['NO']*4,['NO']*4)
        self.assertIsNone(result['cohen_kappa'])
        self.assertEqual(result['agreement_rate'],1)

    def test_perfect_nonconstant(self):
        self.assertEqual(agreement(['YES','NO'],['YES','NO'])['cohen_kappa'],1)

    def test_empty_not_zero(self):
        with self.assertRaises(ValueError):
            agreement([],[])

    def test_only_exact_approved_exception(self):
        diffs=[{'kind':'BOUNDARY_WHITESPACE_ONLY','before':' a','after':'a','row':i} for i in range(123)]
        self.assertTrue(exception_applies('raw','raw','issued','issued',diffs,diffs))
        self.assertFalse(exception_applies('changed','raw','issued','issued',diffs,diffs))
        self.assertFalse(exception_applies('raw','raw','issued','issued',diffs[:-1],diffs))

    def test_content_change_not_waived(self):
        diffs=[{'kind':'CONTENT_CHANGE','before':'a','after':'b'}]*123
        self.assertFalse(exception_applies('raw','raw','issued','issued',diffs,diffs))

    def test_process_is_separate(self):
        rows=[{'semantic_differences':['overall'], 'process_difference':True},
              {'semantic_differences':[], 'process_difference':True},
              {'semantic_differences':[], 'process_difference':False}]
        self.assertEqual(partitions(rows),{'semantic_rows':1,'process_only_rows':1,'all_categorical_equal_rows':1})


if __name__ == '__main__':
    unittest.main()
