from __future__ import annotations
from typing import Optional

# ---------------------------------------------------------------------------
# Sentinela para distinguir "argumento não fornecido" de None válido
# ---------------------------------------------------------------------------

_MISSING = object()

# ---------------------------------------------------------------------------
# Exceção equivalente a java.lang.NumberFormatException
# ---------------------------------------------------------------------------


class NumberFormatException(ValueError):
    """
    Equivalente Python de java.lang.NumberFormatException.

    Subclasse de ValueError para manter compatibilidade com código s
    que captura ValueError, permitindo também captura específica desta exceção.
    """


# ---------------------------------------------------------------------------
# Helpers internos de 32 bits — não fazem parte da API pública
# ---------------------------------------------------------------------------

_MASK32    = 0xFFFF_FFFF
_MIN_RADIX = 2
_MAX_RADIX = 36
_DIGITS    = '0123456789abcdefghijklmnopqrstuvwxyz'


def _to_int32(value: int) -> int:
    """Trunca para inteiro com sinal de 32 bits (complemento de dois)."""
    value &= _MASK32
    if value >= 0x8000_0000:
        value -= 0x1_0000_0000
    return value


def _to_uint32(value: int) -> int:
    """Interpreta value como inteiro sem sinal de 32 bits."""
    return value & _MASK32


def _check_radix_silent(radix: int) -> int:
    """Retorna radix válido ou 10 — comportamento Java para toString/toUnsignedString."""
    return radix if _MIN_RADIX <= radix <= _MAX_RADIX else 10


def _check_radix_strict(radix: int) -> None:
    """Lança NumberFormatException se radix fora de [2, 36] — usado em parseInt."""
    if not (_MIN_RADIX <= radix <= _MAX_RADIX):
        raise NumberFormatException(
            f"radix {radix} fora do intervalo [{_MIN_RADIX}, {_MAX_RADIX}]"
        )


def _parse_signed_core(s: Optional[str], radix: int) -> int:
    """
    Núcleo de parseInt: analisa string como inteiro com sinal no radix dado.
    Lança NumberFormatException para qualquer entrada inválida.
    """
    if s is None or len(s) == 0:
        raise NumberFormatException("Argumento nulo ou string vazia")
    _check_radix_strict(radix)

    negative = False
    idx = 0
    if s[0] == '-':
        negative = True
        idx = 1
    elif s[0] == '+':
        idx = 1

    if idx >= len(s):
        raise NumberFormatException(f'Para string: "{s}"')

    try:
        magnitude = int(s[idx:], radix)
    except ValueError:
        raise NumberFormatException(f'Para string: "{s}"')

    value = -magnitude if negative else magnitude

    if value < -(2**31) or value > (2**31 - 1):
        raise NumberFormatException(
            f'Valor fora do intervalo [-2147483648, 2147483647]: "{s}"'
        )
    return value


def _int_to_str(i: int, radix: int) -> str:
    """
    Converte inteiro com sinal para string no radix dado.
    Núcleo compartilhado de toString(int) e toString(int, int).
    """
    radix = _check_radix_silent(radix)
    i = _to_int32(i)
    if i == 0:
        return '0'
    sign = ''
    if i < 0:
        sign = '-'
        i = -i
    digits: list[str] = []
    while i:
        digits.append(_DIGITS[i % radix])
        i //= radix
    return sign + ''.join(reversed(digits))


def _uint_to_str(i: int, radix: int) -> str:
    """
    Converte inteiro sem sinal de 32 bits para string no radix dado.
    Núcleo compartilhado de toUnsignedString, toBinaryString,
    toOctalString e toHexString.
    """
    radix = _check_radix_silent(radix)
    u = _to_uint32(i)
    if u == 0:
        return '0'
    digits: list[str] = []
    while u:
        digits.append(_DIGITS[u % radix])
        u //= radix
    return ''.join(reversed(digits))


class JInteger:
    """
    Equivalente Python de java.lang.Integer (Java SE 8).

    Encapsula um inteiro de 32 bits com sinal e expõe toda a API pública
    da especificação Java, incluindo constantes, construtores, métodos de
    instância e métodos estáticos, com nomes camelCase preservados.

    Sobrecargas Java resolvidas por _DualMethod (contexto instância/classe)
    e por parâmetros sentinela _MISSING (aridade variável).

    Exemplos
    --------
     n = JInteger(42)
     n.intValue()
     42
     n.toString()          # instância, zero args
    '42'
     JInteger.toString(255, 16)   # estático, dois args
    'ff'
     n.hashCode()          # instância
    42
     JInteger.hashCode(255)       # estático Java 8+
    255
     JInteger.parseInt("-FF", 16)
    -255
     JInteger.toBinaryString(-1)
    '11111111111111111111111111111111'
    """

    # ------------------------------------------------------------------
    # Formatação por base — métodos estáticos
    # ------------------------------------------------------------------

    @staticmethod
    def toString(i: int, radix: int = 10) -> str:
        """
        Converte o inteiro i para string no radix especificado.

        Equivalente a Integer.toString(int i) / Integer.toString(int i, int radix).
        Se radix estiver fora de [2, 36], usa 10 (comportamento Java).

        Exemplos
        --------
        >>> JInteger.toString(255, 16)
        'ff'
        >>> JInteger.toString(-255, 16)
        '-ff'
        >>> JInteger.toString(0)
        '0'
        """
        if not isinstance(i, int) or isinstance(i, bool):
            raise TypeError(f"toString requer int, recebeu {type(i).__name__}")
        return _int_to_str(i, radix)

    @staticmethod
    def toBinaryString(i: int) -> str:
        """
        Retorna representação binária do inteiro como unsigned de 32 bits.

        Equivalente a Integer.toBinaryString(int i).

        Exemplos
        --------
        >>> JInteger.toBinaryString(-1)
        '11111111111111111111111111111111'
        >>> JInteger.toBinaryString(4)
        '100'
        """
        return _uint_to_str(i, 2)

    @staticmethod
    def toHexString(i: int) -> str:
        """
        Retorna representação hexadecimal do inteiro como unsigned de 32 bits.

        Equivalente a Integer.toHexString(int i).

        Exemplos
        --------
        >>> JInteger.toHexString(255)
        'ff'
        >>> JInteger.toHexString(-1)
        'ffffffff'
        """
        return _uint_to_str(i, 16)

    @staticmethod
    def toOctalString(i: int) -> str:
        """
        Retorna representação octal do inteiro como unsigned de 32 bits.

        Equivalente a Integer.toOctalString(int i).

        Exemplos
        --------
        >>> JInteger.toOctalString(-1)
        '37777777777'
        >>> JInteger.toOctalString(8)
        '10'
        """
        return _uint_to_str(i, 8)

    @staticmethod
    def toUnsignedString(i: int, radix: int = 10) -> str:
        """
        Retorna representação em string do inteiro como valor sem sinal de 32 bits.

        Equivalente a:
            Integer.toUnsignedString(int i)
            Integer.toUnsignedString(int i, int radix)

        Se radix fora de [2, 36], usa 10.

        Exemplos
        --------
        >>> JInteger.toUnsignedString(-1)
        '4294967295'
        >>> JInteger.toUnsignedString(-1, 16)
        'ffffffff'
        """
        return _uint_to_str(i, radix)

    # ------------------------------------------------------------------
    # Constantes de classe
    # ------------------------------------------------------------------

    MAX_VALUE: int  = 2**31 - 1    # 2147483647
    MIN_VALUE: int  = -(2**31)     # -2147483648
    SIZE:      int  = 32           # número de bits em um int Java
    BYTES:     int  = 4            # número de bytes em um int Java

    # Java expõe Integer.TYPE como Class<Integer> via reflexão para o tipo
    # primitivo 'int'. Python não possui tipos primitivos nem reflexão
    # equivalente. O análogo semântico mais próximo é o tipo `int` do Python.
    TYPE: type = int