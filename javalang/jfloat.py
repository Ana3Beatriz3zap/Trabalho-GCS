import struct
import math

_UNSET = object()

# ---------------------------------------------------------------------------
# Private module-level helpers
# ---------------------------------------------------------------------------

def _to_float32(value: float) -> float:
    """
    Round a Python 64-bit float to IEEE 754 single-precision (32-bit).

    - NaN input  → NaN output (struct quirks avoided).
    - Overflow   → ±Infinity (matches Java's narrowing-conversion rule).
    """
    if math.isnan(value):
        return float('nan')
    try:
        return struct.unpack('>f', struct.pack('>f', value))[0]
    except (struct.error, OverflowError):
        return math.copysign(float('inf'), value)


def _float32_raw_bits(value: float) -> int:
    """Return the raw **unsigned** 32-bit integer bit-pattern of a float32."""
    return struct.unpack('>I', struct.pack('>f', value))[0]


def _to_signed32(n: int) -> int:
    """
    Reinterpret an unsigned 32-bit integer as a signed two's-complement int.

    Equivalent to Java's ``(int) unsignedValue``.
    """
    n &= 0xFFFF_FFFF
    return n - 0x1_0000_0000 if n >= 0x8000_0000 else n