"""Tests for tiny-rfc-3339's validator.

Tests are organized by the RFC 3339 grammar production they cover. All cases
are deterministic literals — no wall-clock time is used.
"""

import unittest

from tiny_rfc_3339 import is_rfc3339


class TestRFC3339Validator(unittest.TestCase):
    def test_canonical_utc(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05Z"))

    def test_lowercase_t_and_z(self):
        self.assertTrue(is_rfc3339("2025-01-02t15:04:05z"))

    def test_positive_offset(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05+02:00"))

    def test_negative_offset(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05-08:00"))

    def test_zero_offset(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05+00:00"))

    def test_fractional_seconds_short(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05.5Z"))

    def test_fractional_seconds_long(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05.123456789Z"))

    def test_fractional_seconds_with_offset(self):
        self.assertTrue(is_rfc3339("2025-01-02T15:04:05.123+02:00"))

    def test_boundary_dates(self):
        self.assertTrue(is_rfc3339("2025-01-01T00:00:00Z"))
        self.assertTrue(is_rfc3339("2025-12-31T23:59:59Z"))

    def test_invalid_date_only(self):
        self.assertFalse(is_rfc3339("2025-01-02"))

    def test_invalid_missing_offset(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:05"))

    def test_invalid_space_separator(self):
        self.assertFalse(is_rfc3339("2025-01-02 15:04:05Z"))

    def test_invalid_trailing_chars(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:05Zextra"))

    def test_invalid_empty_string(self):
        self.assertFalse(is_rfc3339(""))

    def test_invalid_non_string(self):
        self.assertFalse(is_rfc3339(None))
        self.assertFalse(is_rfc3339(12345))

    def test_invalid_month_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-13-02T15:04:05Z"))
        self.assertFalse(is_rfc3339("2025-00-02T15:04:05Z"))

    def test_invalid_day_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-01-32T15:04:05Z"))
        self.assertFalse(is_rfc3339("2025-01-00T15:04:05Z"))

    def test_invalid_hour_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-01-02T24:00:00Z"))

    def test_invalid_minute_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:60:00Z"))

    def test_invalid_second_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:60Z"))

    def test_invalid_offset_hour_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:05+24:00"))

    def test_invalid_offset_minute_out_of_range(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:05+02:60"))

    def test_invalid_offset_missing_colon(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:05+0200"))

    def test_invalid_fraction_without_digits(self):
        self.assertFalse(is_rfc3339("2025-01-02T15:04:05.Z"))

    def test_invalid_non_digit_in_date(self):
        self.assertFalse(is_rfc3339("20a5-01-02T15:04:05Z"))


if __name__ == "__main__":
    unittest.main()
