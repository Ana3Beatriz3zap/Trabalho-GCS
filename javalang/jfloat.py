import struct


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