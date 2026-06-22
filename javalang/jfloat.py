import struct
import math
from typing import Union

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


def _bits_to_float32(bits: int) -> float:
    """Reconstruct the float32 whose bit-pattern is the given unsigned 32-bit int."""
    return struct.unpack('>f', struct.pack('>I', bits & 0xFFFF_FFFF))[0]


class JFloat:
    """
    Python implementation of ``java.lang.Float`` (Java SE 8).

    ``https://docs.oracle.com/javase/8/docs/api/java/lang/Float.html``

    Values are internally stored as IEEE 754 **32-bit** single-precision
    floats, enforced at construction time and in every static factory method
    via ``struct`` pack/unpack.

    Dual-use methods
    ~~~~~~~~~~~~~~~~
    ``isNaN``, ``isInfinite``, ``toString``, and ``hashCode`` work both as
    instance methods and as class-level (static) functions::

        # Instance usage
        f = JFloat(1.0)
        f.isNaN()          # → False
        f.toString()       # → "1.0"

        # Static usage
        JFloat.isNaN(float('nan'))   # → True
        JFloat.toString(1.0)         # → "1.0"
    """

    # ------------------------------------------------------------------
    # Class constants
    # ------------------------------------------------------------------

    MAX_VALUE: float = _bits_to_float32(0x7F7F_FFFF)
    """Largest positive finite float32 ≈ 3.4028235E38."""

    MIN_VALUE: float = _bits_to_float32(0x0000_0001)
    """Smallest positive *nonzero* float32 (subnormal) ≈ 1.4E-45.
    Note: this value is *positive*, unlike ``Integer.MIN_VALUE``."""

    MIN_NORMAL: float = _bits_to_float32(0x0080_0000)
    """Smallest positive *normalized* float32 ≈ 1.17549435E-38."""

    POSITIVE_INFINITY: float = float('inf')
    NEGATIVE_INFINITY: float = float('-inf')
    NaN: float = float('nan')

    MAX_EXPONENT: int = 127
    """Maximum unbiased exponent for a finite normalized float32."""

    MIN_EXPONENT: int = -126
    """Minimum unbiased exponent for a finite normalized float32."""

    SIZE: int = 32
    """Number of bits in the IEEE 754 single-precision format."""

    BYTES: int = 4
    """Number of bytes in the IEEE 754 single-precision format."""

    TYPE: type = float
    """
    Closest Python equivalent to Java's ``Float.TYPE`` (``Class<float>``).

    Java exposes the reflective ``Class`` object for the primitive ``float``
    type via ``Float.TYPE``.  Python has no primitive types or runtime class
    reflection; the built-in ``float`` type is the nearest conceptual
    equivalent, despite being 64-bit rather than 32-bit.
    """

    # ------------------------------------------------------------------
    # Constructor
    # ------------------------------------------------------------------

    def __init__(self, value: Union[float, int, str, 'JFloat']) -> None:
        """
        Construct a JFloat from a numeric or string value.

        Mirrors Java's three constructors::

            Float(float value)   – pass any Python ``float`` or ``int``
            Float(double value)  – identical in Python (no distinct double)
            Float(String s)      – pass a ``str``; parsed via ``parseFloat()``

        Args:
            value: ``float``, ``int``, ``str``, or another ``JFloat``.

        Raises:
            TypeError:  if *value* is not a supported type.
            ValueError: if *value* is a ``str`` that cannot be parsed
                        (Java equivalent: ``NumberFormatException``).
        """
        if isinstance(value, JFloat):
            self._value: float = value._value
        elif isinstance(value, str):
            self._value = JFloat.parseFloat(value)
        elif isinstance(value, (int, float)):
            self._value = _to_float32(float(value))
        else:
            raise TypeError(
                f"JFloat() requires float, int, str, or JFloat, "
                f"not '{type(value).__name__}'"
            )
        

    # ------------------------------------------------------------------
    # Static — parsing & value factories
    # ------------------------------------------------------------------

    @staticmethod
    def parseFloat(s: str) -> float:
        """
        Parse a string as a float32 value.

        Java: ``static float parseFloat(String s)``

        Accepted formats:

        * Named literals (case-sensitive): ``"NaN"``, ``"Infinity"``,
          ``"+Infinity"``, ``"-Infinity"``
        * Decimal: ``"1.5"``, ``"-3.14"``, ``"1.5e3"``, ``"1.5E-3"``
        * Hexadecimal float: ``"0x1.8p0"``, ``"0x1.8P-1"``
        * Leading/trailing whitespace is stripped.

        Args:
            s: the string to parse.

        Raises:
            ValueError: if *s* is ``None`` or cannot be parsed
                        (Java: ``NullPointerException`` / ``NumberFormatException``).
        """
        if s is None:
            raise ValueError(
                "null input (Java equivalent: NullPointerException)"
            )
        s = s.strip()
        if not s:
            raise ValueError(
                "empty string cannot be parsed as float "
                "(Java equivalent: NumberFormatException)"
            )

        # Java-specified named literals (exact case, per the Java spec)
        if s == "NaN":
            return float('nan')
        if s in ("Infinity", "+Infinity"):
            return float('inf')
        if s == "-Infinity":
            return float('-inf')

        # Hexadecimal floating-point (Java supports 0x… format in parseFloat)
        lower = s.lower()
        if '0x' in lower:
            try:
                return _to_float32(float.fromhex(s))
            except ValueError:
                raise ValueError(
                    f"Cannot parse '{s}' as float "
                    f"(Java equivalent: NumberFormatException)"
                )

        # Decimal floating-point (Python float() handles all standard forms)
        try:
            return _to_float32(float(s))
        except ValueError:
            raise ValueError(
                f"Cannot parse '{s}' as float "
                f"(Java equivalent: NumberFormatException)"
            )

    # ------------------------------------------------------------------
    # Dual-use methods  (instance call: obj.m()  OR  static call: JFloat.m(v))
    # ------------------------------------------------------------------

    def toString(self_or_f: Union['JFloat', float] = _UNSET) -> str:  # type: ignore[override]
        """
        Return a Java-style string for this value or for the given float.

        Instance: ``obj.toString()``         → string for *obj*'s value
        Static:   ``JFloat.toString(f)``     → string for the float32 *f*

        Java: ``String toString()`` / ``static String toString(float f)``

        Examples::

            JFloat(1.0).toString()   → "1.0"
            JFloat.toString(0.1)     → "0.1"
            JFloat.toString(1e8)     → "1.0E8"
        """
        if self_or_f is _UNSET:
            raise TypeError(
                "toString() requires a JFloat instance or a float argument"
            )
        if isinstance(self_or_f, JFloat):
            return _java_float_str(self_or_f._value)
        return _java_float_str(_to_float32(float(self_or_f)))

    def hashCode(self_or_v: Union['JFloat', float] = _UNSET) -> int:  # type: ignore[override]
        """
        Return the hash code (= ``floatToIntBits(value)``).

        Instance: ``obj.hashCode()``          → hash for *obj*'s value
        Static:   ``JFloat.hashCode(v)``      → hash for the float32 *v*

        Java: ``int hashCode()`` / ``static int hashCode(float value)``
        """
        if self_or_v is _UNSET:
            raise TypeError(
                "hashCode() requires a JFloat instance or a float argument"
            )
        if isinstance(self_or_v, JFloat):
            return JFloat.floatToIntBits(self_or_v._value)
        return JFloat.floatToIntBits(_to_float32(float(self_or_v)))
