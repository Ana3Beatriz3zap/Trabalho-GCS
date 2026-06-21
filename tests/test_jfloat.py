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
class TestToHexString:

    def test_one(self):
        assert JFloat.toHexString(1.0) == "0x1.0p0"

    def test_zero(self):
        assert JFloat.toHexString(0.0) == "0x0.0p0"

# ===========================================================================
# 7. Bit-level conversions
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestBitConversions:

    # --- floatToIntBits ---
    def test_float_to_int_bits_one(self):
        assert JFloat.floatToIntBits(1.0) == 0x3F80_0000

    # --- intBitsToFloat ---
    def test_int_bits_to_float_one(self):
        assert JFloat.intBitsToFloat(0x3F80_0000) == 1.0

# ===========================================================================
# 8. Comparison (compare, max, min, sum)
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestComparison:

    # --- compare ---
    def test_compare_less(self):
        assert JFloat.compare(1.0, 2.0) < 0

    # --- max ---
    def test_max_basic(self):
        assert JFloat.max(1.0, 2.0) == 2.0
        
    # --- min ---
    def test_min_basic(self):
        assert JFloat.min(1.0, 2.0) == 1.0