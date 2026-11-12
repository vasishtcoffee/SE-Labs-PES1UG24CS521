from datetime import date
from math import isfinite
import re


COUPON = re.compile(r"([A-Z]+)-([0-9]+)", re.ASCII | re.IGNORECASE)
ISO_DATE = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}")
BASE_DATE = date(2024, 1, 1)


def split_code(code):
    """Return an uppercase prefix and integer value, or None for invalid input."""
    match = COUPON.fullmatch(code.strip()) if isinstance(code, str) else None
    if match is None:
        return None
    prefix, value = match.groups()
    try:
        return prefix.upper(), int(value)
    except ValueError:
        return None


def most_expensive(prices_csv):
    """Return the highest finite, nonnegative price, or None for invalid input."""
    if not isinstance(prices_csv, str):
        return None
    try:
        prices = [float(field) for field in prices_csv.split(",")]
    except ValueError:
        return None
    if any(not isfinite(price) or price < 0 for price in prices):
        return None
    return max(prices)


def expiry_days(date_text):
    """Return the one-based day offset from 2024-01-01, or None for invalid input."""
    if not isinstance(date_text, str):
        return None
    date_text = date_text.strip()
    if ISO_DATE.fullmatch(date_text) is None:
        return None
    try:
        expiry = date.fromisoformat(date_text)
    except ValueError:
        return None
    return (expiry - BASE_DATE).days + 1


def main():
    fields = (
        ("split_code", "Enter a coupon code (e.g. save-20): ",
         "Prefix and Value", split_code),
        ("most_expensive", "Enter item prices as CSV (e.g. 199,49.5,320): ",
         "Most Expensive Item", most_expensive),
        ("expiry_days", "Enter an expiry date as YYYY-MM-DD: ",
         "Days Since 2024", expiry_days),
    )
    for name, prompt, label, parse in fields:
        print(f"==== Running {name} ====")
        try:
            result = parse(input(prompt))
        except EOFError:
            print("Input ended.")
            return
        print(f"{label}: {result if result is not None else 'Invalid input'}")


if __name__ == "__main__":
    main()
