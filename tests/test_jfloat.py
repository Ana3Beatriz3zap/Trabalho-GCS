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

@pytest.mark.skip(reason="Ainda não está na main")
class TestComparison:
    # --- sum ---
    def test_sum_basic(self):
        assert JFloat.sum(1.0, 2.0) == 3.0

# ===========================================================================
# 9. equals, hashCode, compareTo
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestObjectContract:
    # --- equals ---

    def test_equals_same_value(self):
        assert JFloat(1.0).equals(JFloat(1.0))

    # --- hashCode ---

    def test_hash_code_equals_float_to_int_bits(self):
        f = JFloat(1.5)
        assert f.hashCode() == JFloat.floatToIntBits(1.5)


    # --- compareTo ---

    def test_compare_to_less(self):
        assert JFloat(1.0).compareTo(JFloat(2.0)) < 0