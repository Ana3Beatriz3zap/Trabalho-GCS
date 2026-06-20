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

def _float_compare_key(bits_signed: int) -> int:
    """
    Transform a *signed* ``floatToIntBits`` value into an integer that
    preserves IEEE 754 total ordering under ordinary Python ``<``/``>``
    comparison.

    IEEE 754 floats are laid out so that:
    * Positive values: unsigned bit-pattern order == mathematical order.
    * Negative values: unsigned bit-pattern order is **reversed** relative
      to mathematical order (larger magnitude → larger unsigned bits, but
      should map to a *smaller* ordered integer).

    Fix: XOR the lower 31 bits of negative bit-patterns.  This inverts their
    relative ordering while keeping them below all positive bit-patterns.

    Examples (signed)::

        -0.0  → 0x80000000 → XOR → -1          (just below +0.0 = 0)
        -1.0  → 0xBF800000 → XOR → -1065156609  (correct position)
        -2.0  → 0xC0000000 → XOR → -1073741825  (less than -1.0 ✓)
        +0.0  → 0x00000000 → unchanged → 0
        NaN   → 0x7fc00000 → unchanged → 2143289344 (greatest)
    """
    if bits_signed < 0:
        return bits_signed ^ 0x7FFF_FFFF
    return bits_signed


def _java_float_str(f32: float) -> str:
    """
    Format a float32 value exactly as Java's ``Float.toString(float)`` would.

    Rules (from the Java SE 8 specification):

    * ``NaN``       → ``"NaN"``
    * ``±Infinity`` → ``"Infinity"`` / ``"-Infinity"``
    * ``±0.0``      → ``"0.0"``     / ``"-0.0"``
    * Decimal notation when the base-10 exponent *e* satisfies -3 ≤ e ≤ 6;
      scientific notation (capital ``E``, no leading zeros, no ``+`` sign for
      positive exponents) otherwise.
    * Minimum number of digits that uniquely identifies the float32 value
      (i.e., round-trips through ``parseFloat`` back to the same float32).

    Note: for a handful of subnormal values the shortest round-trip string
    produced here may differ from the JDK's exact output by one digit (e.g.,
    ``"1.0E-45"`` vs ``"1.4E-45"`` for ``Float.MIN_VALUE``).  Both strings
    parse to the same float32.  See README for details.
    """
    if math.isnan(f32):
        return "NaN"
    if math.isinf(f32):
        return "Infinity" if f32 > 0 else "-Infinity"

    sign = "-" if math.copysign(1.0, f32) < 0 else ""
    val = abs(f32)

    if val == 0.0:
        return sign + "0.0"

    # Obtain the base-10 exponent via Python's scientific formatter to avoid
    # log10 precision errors with float32 values near powers of 10.
    exp_i = int(f"{val:.0e}".split('e')[1])
    use_sci = exp_i < -3 or exp_i >= 7

    if use_sci:
        # Iterate digits-after-decimal (0 = 1 sig-fig) until round-trip passes.
        for prec in range(0, 9):
            candidate = f"{val:.{prec}e}"
            try:
                if _to_float32(float(candidate)) == val:
                    mantissa, e_part = candidate.split('e')
                    if '.' not in mantissa:
                        mantissa += '.0'
                    return f"{sign}{mantissa}E{int(e_part)}"
            except (ValueError, OverflowError):
                pass
    else:
        # Iterate decimal places (0, 1, 2 …) until round-trip passes.
        for d in range(0, 9):
            candidate = f"{val:.{d}f}"
            try:
                if _to_float32(float(candidate)) == val:
                    if '.' not in candidate:
                        candidate += '.0'
                    return sign + candidate
            except (ValueError, OverflowError):
                pass

    # Safety fallback — should be unreachable for any valid float32 value.
    return sign + repr(val)