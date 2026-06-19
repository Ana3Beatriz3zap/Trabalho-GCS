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

    Subclasse de ValueError para manter compatibilidade com código Python
    que captura ValueError, permitendo também captura específica desta exceção.
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

    # ------------------------------------------------------------------
    # Métodos estáticos — parsing
    # ------------------------------------------------------------------

    @staticmethod
    def parseInt(s: Optional[str], radix: int = 10) -> int:
        """
        Parseia a string como inteiro com sinal no radix dado.

        Equivalente a:
            Integer.parseInt(String s)           — radix = 10
            Integer.parseInt(String s, int radix)

        A string pode ter '+' ou '-' como primeiro caractere.
        Radix deve estar em [2, 36]; fora disso lança NumberFormatException.

        Exceções
        --------
        NumberFormatException
            String nula, vazia, com caracteres inválidos para o radix,
            radix fora de [2, 36], ou valor fora de [-2147483648, 2147483647].

        Exemplos
        --------
        >>> JInteger.parseInt("473")
        473
        >>> JInteger.parseInt("-FF", 16)
        -255
        >>> JInteger.parseInt("Kona", 27)
        411787
        """
        return _parse_signed_core(s, radix)

    @staticmethod
    def parseUnsignedInt(s: Optional[str], radix: int = 10) -> int:
        """
        Parseia a string como inteiro sem sinal no radix dado.

        Valores entre 2^31 e 2^32-1 (maiores que MAX_VALUE) são retornados
        como inteiros negativos de 32 bits com sinal — comportamento Java.

        Equivalente a:
            Integer.parseUnsignedInt(String s)
            Integer.parseUnsignedInt(String s, int radix)

        Exceções
        --------
        NumberFormatException
            String nula, vazia, com sinal negativo, valor > 4294967295,
            radix fora de [2, 36], ou caracteres inválidos.

        Exemplos
        --------
        >>> JInteger.parseUnsignedInt("4294967295")
        -1
        >>> JInteger.parseUnsignedInt("ff", 16)
        255
        """
        if s is None or len(s) == 0:
            raise NumberFormatException("Argumento nulo ou string vazia")
        _check_radix_strict(radix)

        idx = 0
        if s[0] == '+':
            idx = 1
        elif s[0] == '-':
            raise NumberFormatException(
                f'parseUnsignedInt não aceita sinal negativo: "{s}"'
            )

        if idx >= len(s):
            raise NumberFormatException(f'Para string: "{s}"')

        try:
            value = int(s[idx:], radix)
        except ValueError:
            raise NumberFormatException(f'Para string: "{s}"')

        if value < 0 or value > 0xFFFF_FFFF:
            raise NumberFormatException(
                f'Valor fora do intervalo unsigned [0, 4294967295]: "{s}"'
            )

        return _to_int32(value)

    # ------------------------------------------------------------------
    # valueOf — aridade 1 ou 2, despacho por tipo do primeiro argumento
    # ------------------------------------------------------------------

    @staticmethod
    def valueOf(value: Union[int, str], radix: int = 10) -> 'JInteger':
        """
        Retorna um JInteger representando o valor especificado.

        Equivalente a:
            Integer.valueOf(int i)
            Integer.valueOf(String s)         — radix implícito 10
            Integer.valueOf(String s, int radix)

        Implementa o Integer cache Java: para valores em [-128, 127] retorna
        sempre o mesmo objeto (identidade garantida por especificação).

        Parâmetros
        ----------
        value : int | str
            int → usado diretamente (truncado para 32 bits).
            str → parseado com parseInt(value, radix).
        radix : int
            Base numérica, usada apenas quando value é str. Default 10.

        Exemplos
        --------
        >>> JInteger.valueOf(42).intValue()
        42
        >>> JInteger.valueOf("ff", 16).intValue()
        255
        >>> JInteger.valueOf(-128) is JInteger.valueOf(-128)
        True
        """
        if isinstance(value, str):
            parsed = _parse_signed_core(value, radix)
        elif isinstance(value, int) and not isinstance(value, bool):
            parsed = _to_int32(value)
        else:
            raise TypeError(
                f"valueOf requer int ou str, recebeu {type(value).__name__}"
            )

        # Integer cache [-128, 127]
        if -128 <= parsed <= 127:
            if parsed not in _cache:
                obj = object.__new__(JInteger)
                obj._value = parsed
                _cache[parsed] = obj
            return _cache[parsed]

        return JInteger(parsed)