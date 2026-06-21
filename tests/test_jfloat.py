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

# ===========================================================================
# 4. IEEE 754 checks
# ===========================================================================

@pytest.mark.skip(reason="Ainda não está na main")
class TestIEEEChecks:
    # --- isInfinite (instance) ---
    def test_is_infinite_instance_pos(self):
        assert JFloat(float('inf')).isInfinite() is True

    # --- isInfinite (static) ---
    def test_is_infinite_static_true(self):
        assert JFloat.isInfinite(float('inf')) is True

    # --- isFinite (static only) ---
    def test_is_finite_normal(self):
        assert JFloat.isFinite(1.0) is True