import pytest
import struct
from javalang.jfloat import JFloat

def f32(v: float) -> float:
    """Round-trip through float32 (same as JFloat's internal _to_float32)."""
    return struct.unpack('>f', struct.pack('>f', v))[0]

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


# ===========================================================================
# 5. parseFloat
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestParseFloat:

    def test_parse_simple(self):
        assert JFloat.parseFloat("1.5") == f32(1.5)

    def test_parse_negative(self):
        assert JFloat.parseFloat("-3.14") == f32(-3.14)

# ===========================================================================
# 6. toString / toHexString
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestToString:

    # --- Special values ---
    def test_zero(self):
        assert JFloat(0.0).toString() == "0.0"

    def test_neg_zero(self):
        assert JFloat(-0.0).toString() == "-0.0"
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
