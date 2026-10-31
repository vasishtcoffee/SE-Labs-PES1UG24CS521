"""Branch-coverage tests for the supplied coupon_validator.py.

Run from the Lab6 directory:
    coverage run --branch --source=coupon_validator -m pytest BranchCoverageTest_coupon_validator.py
    coverage report -m

The cap-exceeded branch in best_discount is not naturally reachable with the
provided coupon rules. A monkeypatch is used to exercise that defensive branch.
"""

import pytest
import coupon_validator
from coupon_validator import best_discount, coupon_discount, is_expired


@pytest.mark.parametrize(
    "code,total,is_new_user,day,expected",
    [
        ("WELCOME10", 100, True, "mon", 10.0),       # new-user condition True
        ("WELCOME10", 100, False, "mon", 0),         # new-user condition False
        ("WEEKEND20", 500, True, "sat", 100.0),      # weekend, minimum met
        ("WEEKEND20", 499, True, "sun", 50),         # weekend, minimum not met
        ("WEEKEND20", 500, True, "fri", 0),          # not a weekend
        ("FLAT100", 301, True, "mon", 100),          # total > 300
        ("FLAT100", 300, True, "mon", 0),            # total <= 300
        ("NOT_A_COUPON", 100, True, "mon", 0),       # unknown coupon
    ],
)
def test_coupon_discount_decision_branches(code, total, is_new_user, day, expected):
    assert coupon_discount(code, total, is_new_user, day) == expected


@pytest.mark.parametrize("total", [0, -100])
def test_non_positive_cart_branch(total):
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("NOT_A_COUPON", total, False, "mon")


def test_best_discount_empty_list_exercises_zero_loop_iterations():
    assert best_discount([], 100, False, "mon") == 0


def test_best_discount_loop_and_best_value_branches():
    # First result is greater than zero; the next result ties the best value.
    assert best_discount(["FLAT100", "WELCOME10"], 1000, True, "mon") == 100


def test_best_discount_cap_comparison_false():
    assert best_discount(["WELCOME10"], 100, True, "mon") == 10


def test_best_discount_cap_comparison_true(monkeypatch):
    # Force a defensive path that cannot be reached using the supplied coupons.
    monkeypatch.setattr(coupon_validator, "coupon_discount", lambda *args: 80)
    assert coupon_validator.best_discount(["FORCED"], 100, False, "mon") == 40


@pytest.mark.parametrize(
    "today,start,days_valid,expected",
    [
        (5, 1, 0, True),    # non-positive validity
        (5, 1, 4, False),   # elapsed equals validity
        (6, 1, 4, True),    # elapsed exceeds validity
        (1, 5, 4, False),   # date difference is negative
    ],
)
def test_expiry_decision_branches(today, start, days_valid, expected):
    assert is_expired(today, start, days_valid) is expected
