"""
test_jfloat.py
==============
Pytest test suite for JFloat — Python implementation of java.lang.Float (Java SE 8).

Run with:
    pytest test_jfloat.py -v
"""

import math
import struct
import pytest
#from jfloat import JFloat

@pytest.mark.skip(reason="Desativado temporariamente")
class TestConversions:
    # --- intValue ---

    def test_int_value_positive_truncates(self):
        assert JFloat(3.9).intValue() == 3

    def test_int_value_negative_truncates(self):
        assert JFloat(-3.9).intValue() == -3

    def test_int_value_nan_is_zero(self):
        assert JFloat(float('nan')).intValue() == 0

    def test_int_value_pos_inf_is_max(self):
        assert JFloat(float('inf')).intValue() == 2_147_483_647

    def test_int_value_neg_inf_is_min(self):
        assert JFloat(float('-inf')).intValue() == -2_147_483_648

    def test_int_value_large_overflow(self):
        # 3e38 far exceeds Integer.MAX_VALUE → saturate
        assert JFloat(3e38).intValue() == 2_147_483_647

    def test_int_value_negative_overflow(self):
        assert JFloat(-3e38).intValue() == -2_147_483_648

    def test_int_value_zero(self):
        assert JFloat(0.0).intValue() == 0

    # --- longValue ---

    def test_long_value_positive(self):
        assert JFloat(3.7).longValue() == 3

    def test_long_value_nan_is_zero(self):
        assert JFloat(float('nan')).longValue() == 0

    def test_long_value_pos_inf(self):
        assert JFloat(float('inf')).longValue() == 9_223_372_036_854_775_807

    def test_long_value_neg_inf(self):
        assert JFloat(float('-inf')).longValue() == -9_223_372_036_854_775_808

    # --- byteValue ---

    def test_byte_value_small_positive(self):
        assert JFloat(65.0).byteValue() == 65

    def test_byte_value_wraps_positive(self):
        # 200 & 0xFF = 200 → 200 - 256 = -56
        assert JFloat(200.0).byteValue() == -56

    def test_byte_value_negative_one(self):
        assert JFloat(-1.0).byteValue() == -1

    def test_byte_value_max_byte(self):
        assert JFloat(127.0).byteValue() == 127

    def test_byte_value_min_byte(self):
        assert JFloat(128.0).byteValue() == -128

    # --- shortValue ---

    def test_short_value_normal(self):
        assert JFloat(32767.0).shortValue() == 32767

    def test_short_value_wraps(self):
        assert JFloat(32768.0).shortValue() == -32768

    def test_short_value_negative(self):
        assert JFloat(-1.0).shortValue() == -1

    # --- floatValue / doubleValue ---

    def test_float_value(self):
        assert JFloat(1.5).floatValue() == 1.5

    def test_double_value(self):
        assert JFloat(1.5).doubleValue() == 1.5

# ===========================================================================
# 4. IEEE 754 checks
# ===========================================================================

class TestIEEEChecks:

    # --- isNaN (instance) ---
    def test_is_nan_instance_true(self):
        assert JFloat(float('nan')).isNaN() is True

    def test_is_nan_instance_false(self):
        assert JFloat(1.0).isNaN() is False

    def test_is_nan_instance_infinity_false(self):
        assert JFloat(float('inf')).isNaN() is False
