import struct
import pytest
from javalang.jfloat import JFloat


def bits(v: float) -> int:
    """Unsigned 32-bit bit-pattern of a float32."""
    return struct.unpack('>I', struct.pack('>f', v))[0]


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
    def test_int_value_positive_truncates(self):
        assert JFloat(3.9).intValue() == 3

    def test_int_value_negative_truncates(self):
        assert JFloat(-3.9).intValue() == -3

    def test_long_value_positive(self):
        assert JFloat(3.7).longValue() == 3

    def test_byte_value_small_positive(self):
        assert JFloat(65.0).byteValue() == 65


# ===========================================================================
# 12. Edge cases and boundary values
# ===========================================================================

@pytest.mark.skip(reason="Ainda não está na main")
class TestEdgeCases:
    def test_min_value_is_subnormal(self):
        b = bits(JFloat.MIN_VALUE)
        assert (b >> 23) & 0xFF == 0       # exponent field == 0
        assert b & 0x7F_FFFF == 1          # mantissa == 1

    def test_constructor_string_hex_min_value(self):
        f = JFloat("0x0.000002p-126")
        assert f.floatValue() == JFloat.MIN_VALUE

    def test_constructor_string_hex_max_value(self):
        f = JFloat("0x1.fffffep127")
        assert f.floatValue() == JFloat.MAX_VALUE