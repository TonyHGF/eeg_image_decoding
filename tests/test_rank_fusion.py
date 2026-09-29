import sys
from pathlib import Path
import unittest
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from rank_fusion import fuse, metrics, rank_scores


class FusionTests(unittest.TestCase):
    def test_requested_curve_and_cutoff(self):
        ranks = np.arange(1, 11)[None, None, :]
        _, votes = fuse(ranks, [1], '5/3', 5)
        self.assertAlmostEqual(votes[0, 0], 1)
        self.assertAlmostEqual(votes[0, 4], .4)
        np.testing.assert_array_equal(votes[0, 5:], 0)
        for c in ('1', '4/3', '5/3', '2'):
            for window in (5, 10):
                _, v = fuse(ranks, [1], c, window)
                self.assertTrue(np.all(np.diff(v[0, :window]) < 0))

    def test_agreement_can_beat_disagreeing_first_choices(self):
        # Candidate 1 is second in both lists; candidates 0/2 each lead one list.
        ranks = np.array([[[1, 2, 10, 3, 4, 5, 6, 7, 8, 9]],
                          [[10, 2, 1, 3, 4, 5, 6, 7, 8, 9]]])
        order, _ = fuse(ranks, [.5, .5], '5/3', 5)
        self.assertEqual(order[0, 0], 1)
        self.assertEqual(metrics(order, [1])['top1'], 1)

    def test_ties_and_branch_permutation(self):
        ranks = np.array([[[1, 2, 3, 4, 5]], [[2, 1, 3, 4, 5]]])
        order, _ = fuse(ranks, [.5, .5], 1, 5)
        other, _ = fuse(ranks[::-1], [.5, .5], 1, 5)
        np.testing.assert_array_equal(order, other)
        self.assertEqual(order[0, 0], 0)
        ids = np.array([[9, 3, 1, 8, 7]])
        by_id, _ = fuse(ranks, [.5, .5], 1, 5, ids)
        self.assertEqual(by_id[0, 0], 1)
        np.testing.assert_array_equal(rank_scores(np.array([[2., 2., 1.]])), [[1, 2, 3]])

    def test_invalid_ranks_rejected(self):
        with self.assertRaises(ValueError):
            fuse(np.array([[[1, 1, 3, 4, 5]]]), [1], 1, 5)


if __name__ == '__main__':
    unittest.main()
