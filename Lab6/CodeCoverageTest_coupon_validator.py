"""Line-coverage tests for the supplied coupon_validator.py.

Run from the Lab6 directory:
    coverage run --source=coupon_validator -m pytest CodeCoverageTest_coupon_validator.py
    coverage report -m
"""

import pytest

from coupon_validator import best_discount, coupon_discount, is_expired


@pytest.mark.parametrize(
    "code,total,is_new_user,day,expected",
    [
        ("WELCOME10", 200, True, "mon", 20.0),
        ("WELCOME10", 200, False, "mon", 0),
        ("WEEKEND20", 600, True, "sat", 120.0),
        ("WEEKEND20", 200, False, "sun", 50),
        ("WEEKEND20", 600, False, "mon", 0),
        ("FLAT100", 301, True, "mon", 100),
        ("FLAT100", 300, True, "mon", 0),
        ("UNKNOWN", 200, True, "mon", 0),
    ],
)
def test_coupon_discount_paths(code, total, is_new_user, day, expected):
    assert coupon_discount(code, total, is_new_user, day) == expected


@pytest.mark.parametrize("total", [0, -1])
def test_coupon_discount_rejects_non_positive_cart(total):
    with pytest.raises(ValueError, match="empty cart"):
        coupon_discount("WELCOME10", total, True, "mon")


def test_best_discount_selects_highest_coupon():
    assert best_discount(["WELCOME10", "FLAT100"], 1000, True, "mon") == 100


def test_best_discount_with_no_matching_coupon():
    assert best_discount(["UNKNOWN"], 1000, False, "mon") == 0


def test_best_discount_with_empty_coupon_list():
    assert best_discount([], 1000, False, "mon") == 0


def test_is_expired_with_non_positive_validity():
    assert is_expired(10, 5, 0) is True


def test_is_expired_after_validity_period():
    assert is_expired(11, 5, 5) is True


def test_is_not_expired_at_validity_boundary():
    assert is_expired(10, 5, 5) is False
