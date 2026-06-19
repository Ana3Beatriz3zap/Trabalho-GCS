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

    def _uint_to_str(i: int, radix: int) -> str:
        """
        Converte inteiro sem sinal de 32 bits para string no radix dado.
        Núcleo compartilhado de toUnsignedString(int) e toUnsignedString(int, int).
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

# ---------------------------------------------------------------------------
# Descritor _DualMethod — despacho por contexto (instância vs. classe)
# ---------------------------------------------------------------------------


class _DualMethod:
    """
    Descritor que implementa sobrecarga de contexto Java em Python.

    Em Java, ``Integer.toString()`` (instância, zero args) e
    ``Integer.toString(int i)`` / ``Integer.toString(int i, int radix)``
    (métodos estáticos) coexistem com o mesmo nome porque o compilador
    resolve a sobrecarga em tempo de compilação por tipo e aridade.

    Python não tem esse mecanismo; quando se declara um @staticmethod após
    um método de instância com o mesmo nome, o último simplesmente sobrescreve
    o primeiro no namespace da classe.

    Este descritor resolve o problema em runtime:
    - ``obj.método(...)``   → chama ``instance_fn(obj, ...)``
    - ``Classe.método(...)`` → chama ``static_fn(...)``

    Uso dentro da classe:
        nome = _DualMethod(instance_fn, static_fn)
    """

    def __init__(self, instance_fn, static_fn):
        self._instance_fn = instance_fn
        self._static_fn   = static_fn
        # Herda a documentação do método de instância por convenção.
        self.__doc__  = instance_fn.__doc__
        self.__name__ = instance_fn.__name__

    def __set_name__(self, owner, name):
        self.__name__ = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            # Acesso via classe: Classe.método → retorna o callable estático
            return self._static_fn
        # Acesso via instância: obj.método → retorna bound method de instância
        def bound(*args, **kwargs):
            return self._instance_fn(obj, *args, **kwargs)
        bound.__doc__  = self._instance_fn.__doc__
        bound.__name__ = self.__name__
        return bound


# ---------------------------------------------------------------------------
# Cache interno — Integer cache Java [-128, 127]
# ---------------------------------------------------------------------------

_cache: dict[int, 'JInteger'] = {}

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

    def doubleValue(self) -> float:
        """
        Retorna o valor como double IEEE 754 de 64 bits — sem perda de precisão.

        Python float é de 64 bits (double), equivalente direto ao double Java.
        """
        return float(self._value)

    # ------------------------------------------------------------------
    # Métodos de instância — Object / Comparable
    # ------------------------------------------------------------------

    def _toString_instance(self) -> str:
        """
        Retorna representação decimal com sinal deste JInteger.

        Equivalente a Integer.toString() de instância Java.
        Chamado via JInteger(x).toString() — sem argumentos.
        """
        return _int_to_str(self._value, 10)

    def _hashCode_instance(self) -> int:
        """
        Retorna o hash code deste JInteger.

        Em Java, Integer.hashCode() retorna o próprio valor int.
        Chamado via JInteger(x).hashCode() — sem argumentos.
        """
        return self._value
    
    def equals(self, obj: object) -> bool:
        """
        Compara este objeto com outro pelo valor.

        Retorna True se e somente se obj é um JInteger com o mesmo valor.
        Equivalente a Integer.equals(Object).
        """
        if not isinstance(obj, JInteger):
            return False
        return self._value == obj._value

    def compareTo(self, anotherInteger: 'JInteger') -> int:
        """
        Compara numericamente este JInteger com outro.

        Retorna: 0 se iguais, negativo se este < outro, positivo se este > outro.
        Equivalente a Integer.compareTo(Integer).
        """
        if not isinstance(anotherInteger, JInteger):
            raise TypeError("compareTo requer um JInteger")
        return JInteger.compare(self._value, anotherInteger._value)

    # ------------------------------------------------------------------
    # toString — descritor _DualMethod
    #
    # Java tem DOIS métodos com o mesmo nome:
    #   instância : String toString()
    #   estático  : static String toString(int i)
    #               static String toString(int i, int radix)
    #
    # O descritor despacha:
    #   JInteger(42).toString()        → _toString_instance(self)   → "42"
    #   JInteger.toString(42)          → _toString_static(42)       → "42"
    #   JInteger.toString(255, 16)     → _toString_static(255, 16)  → "ff"
    # ------------------------------------------------------------------

    @staticmethod
    def _toString_static(i: int, radix: int = 10) -> str:
        """
        Converte o inteiro i para string no radix especificado.

        Equivalente a:
            Integer.toString(int i)
            Integer.toString(int i, int radix)

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