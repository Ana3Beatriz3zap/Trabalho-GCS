import pytest
from javalang.jfloat import JFloat

# ===========================================================================
# 2. Constructors
# ===========================================================================

@pytest.mark.skip(reason="Ainda não está na main")
class TestConstructors:
    def test_float_constructor(self):
        assert JFloat(1.5).floatValue() == 1.5

    def test_string_constructor_nan(self):
        assert JFloat("NaN").isNaN()

    def test_string_constructor_negative_infinity(self):
        f = JFloat("-Infinity")
        assert f.isInfinite() and f.floatValue() < 0

# ===========================================================================
# 3. Narrowing/widening conversions
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestConversions:
    # --- intValue ---
    def test_int_value_positive_truncates(self):
        assert JFloat(3.9).intValue() == 3
    
    def test_int_value_negative_truncates(self):
        assert JFloat(-3.9).intValue() == -3
    
    # --- longValue ---
    def test_long_value_positive(self):
        assert JFloat(3.7).longValue() == 3
    
    # --- byteValue ---
    def test_byte_value_small_positive(self):
        assert JFloat(65.0).byteValue() == 65
    
    def test_byte_value_wraps_positive(self):
        # 200 & 0xFF = 200 → 200 - 256 = -56
        assert JFloat(200.0).byteValue() == -56
    
    # --- shortValue ---

    def test_short_value_normal(self):
        assert JFloat(32767.0).shortValue() == 32767

    def test_short_value_wraps(self):
        assert JFloat(32768.0).shortValue() == -32768
    
    # --- floatValue / doubleValue ---

    def test_float_value(self):
        assert JFloat(1.5).floatValue() == 1.5

    def test_double_value(self):
        assert JFloat(1.5).doubleValue() == 1.5

# ===========================================================================
# 4. IEEE 754 checks
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestIEEEChecks:

    # --- isNaN (instance) ---
    def test_is_nan_instance_true(self):
        assert JFloat(float('nan')).isNaN() is True
    
    def test_is_nan_instance_false(self):
        assert JFloat(1.0).isNaN() is False
