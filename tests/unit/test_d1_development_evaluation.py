"""Independent tiny gold cases for the new development metric implementation."""
from __future__ import annotations

import numpy as np
import pytest

from scripts.research.evaluate_d1_development_first_results import manual_auc_ap


@pytest.mark.parametrize("scores,auc,ap", [
    ([0.0, 1.0, 2.0, 3.0], 1.0, 1.0),
    ([3.0, 2.0, 1.0, 0.0], 0.0, 5 / 12),
    ([1.0, 1.0, 1.0, 1.0], 0.5, 0.5),
    ([0.0, 1.0, 1.0, 2.0], 0.875, 5 / 6),
])
def test_auc_ap_against_hand_computed_ties(scores: list[float], auc: float, ap: float) -> None:
    actual_auc, actual_ap = manual_auc_ap(np.asarray([0, 0, 1, 1]), np.asarray(scores))
    assert actual_auc == pytest.approx(auc)
    assert actual_ap == pytest.approx(ap)
