from datetime import date, timedelta
from math import isfinite
import string

from hypothesis import given, strategies as st

from coupon_validator import expiry_days, most_expensive, split_code


non_text = st.none() | st.booleans() | st.integers() | st.binary()
mixed_inputs = st.text() | non_text


@given(mixed_inputs)
def test_split_code_returns_valid_shape_or_none(value):
    result = split_code(value)
    if result is not None:
        prefix, amount = result
        assert prefix.isascii() and prefix.isalpha() and prefix.isupper()
        assert type(amount) is int and amount >= 0


@given(st.text(alphabet=string.ascii_letters, min_size=1),
       st.integers(min_value=0, max_value=10**20))
def test_split_code_normalizes_valid_codes(prefix, amount):
    assert split_code(f"  {prefix}-{amount}  ") == (prefix.upper(), amount)


@given(non_text | st.text(alphabet=string.ascii_letters))
def test_split_code_rejects_inputs_without_a_value(value):
    assert split_code(value) is None


@given(mixed_inputs)
def test_most_expensive_returns_valid_price_or_none(value):
    result = most_expensive(value)
    assert result is None or (isinstance(result, float) and isfinite(result) and result >= 0)


@given(st.lists(st.integers(min_value=0, max_value=10**8), min_size=1))
def test_most_expensive_matches_cart_maximum(cents):
    csv = ",".join(f"{price / 100:.2f}" for price in cents)
    assert most_expensive(csv) == max(cents) / 100


@given(non_text | st.sampled_from(["", "1,,2", "1,nan", "1,inf", "1,-2"]))
def test_most_expensive_rejects_invalid_cart(value):
    assert most_expensive(value) is None


@given(mixed_inputs)
def test_expiry_days_returns_integer_or_none(value):
    result = expiry_days(value)
    assert result is None or type(result) is int


@given(st.integers(min_value=-365, max_value=3650))
def test_expiry_days_counts_calendar_days(offset):
    expiry = date(2024, 1, 1) + timedelta(days=offset)
    assert expiry_days(expiry.isoformat()) == offset + 1


@given(non_text | st.sampled_from(["", "2024-02-30", "2025-02-29", "2024-2-01"]))
def test_expiry_days_rejects_invalid_dates(value):
    assert expiry_days(value) is None
