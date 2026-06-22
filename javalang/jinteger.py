from __future__ import annotations
from typing import Optional, Union
import struct

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

    # ------------------------------------------------------------------
    # Construtor
    # ------------------------------------------------------------------

    def __init__(self, value: Union[int, str]) -> None:
        """
        Constrói um JInteger a partir de um int ou de uma String decimal.

        Equivalente a:
            Integer(int value)   — armazena o valor truncado para 32 bits.
            Integer(String s)    — parseia como parseInt(s, 10).

        Parâmetros
        ----------
        value : int | str
            int → truncado para 32 bits com sinal (overflow silencioso).
            str → parseado como inteiro decimal com sinal.

        Exceções
        --------
        NumberFormatException
            Se value for str inválida ou fora do intervalo de 32 bits.
        TypeError
            Se value não for int (exceto bool) nem str.
        """
        if isinstance(value, str):
            self._value: int = _parse_signed_core(value, 10)
        elif isinstance(value, int) and not isinstance(value, bool):
            self._value = _to_int32(value)
        else:
            raise TypeError(
                f"JInteger requer int ou str, recebeu {type(value).__name__}"
            )

    # ------------------------------------------------------------------
    # Conversões numéricas de instância (Number subclass equivalents)
    # ------------------------------------------------------------------

    def byteValue(self) -> int:
        """
        Retorna o valor como byte — narrowing para 8 bits com sinal.

        Equivale ao cast (byte) do Java: os 8 bits menos significativos
        são reinterpretados com sinal (complemento de dois).

        Retorno: int no intervalo [-128, 127].
        """
        v = self._value & 0xFF
        return v - 256 if v >= 128 else v

    def shortValue(self) -> int:
        """
        Retorna o valor como short — narrowing para 16 bits com sinal.

        Retorno: int no intervalo [-32768, 32767].
        """
        v = self._value & 0xFFFF
        return v - 65536 if v >= 32768 else v

    def intValue(self) -> int:
        """Retorna o valor como int de 32 bits com sinal. Sem perda de informação."""
        return self._value

    def longValue(self) -> int:
        """
        Retorna o valor como long — widening, sem perda de informação.

        Python não distingue int de long; retorna int Python que cobre
        todo o intervalo de long Java (64 bits).
        """
        return self._value

    def floatValue(self) -> float:
        """
        Retorna o valor como float IEEE 754 de 32 bits — possível perda de precisão.

        Usa struct para simular a arredondamento exato de single-precision Java.
        Python float é 64 bits nativamente; a conversão via struct garante que
        o valor retornado é o float32 mais próximo, como faria a JVM.
        """
        return struct.unpack('f', struct.pack('f', float(self._value)))[0]
    
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

    toString = _DualMethod(_toString_instance, _toString_static)

    # ------------------------------------------------------------------
    # hashCode — descritor _DualMethod
    #
    # Java SE 8 adicionou uma sobrecarga estática:
    #   instância : int hashCode()                → retorna this.value
    #   estático  : static int hashCode(int value) → retorna value
    #
    # O descritor despacha:
    #   JInteger(42).hashCode()    → _hashCode_instance(self)  → 42
    #   JInteger.hashCode(42)      → _hashCode_static(42)      → 42
    # ------------------------------------------------------------------

    @staticmethod
    def _hashCode_static(value: int) -> int:
        """
        Retorna o hash code para o valor int dado.

        Equivalente a Integer.hashCode(int value) — método estático Java 8+.
        Em Java, hashCode de int é o próprio valor; aqui aplicamos truncamento
        de 32 bits para consistência.

        Exemplos
        --------
        >>> JInteger.hashCode(42)
        42
        >>> JInteger.hashCode(-1)
        -1
        """
        return _to_int32(value)

    hashCode = _DualMethod(_hashCode_instance, _hashCode_static)
    
    @staticmethod
    def reverseBytes(i: int) -> int:
        """
        Inverte a ordem dos 4 bytes, mantendo os bits dentro de cada byte.

        Algoritmo: extração byte a byte e reagrupamento na ordem inversa.
        Equivale a trocar endianness de um inteiro de 32 bits.

        Equivalente a Integer.reverseBytes(int i).

        Exemplos
        --------
        >>> hex(JInteger.reverseBytes(0x12345678))
        '0x78563412'
        """
        n = _to_uint32(i)
        b0 = (n >> 24) & 0xFF
        b1 = (n >> 16) & 0xFF
        b2 = (n >>  8) & 0xFF
        b3 =  n        & 0xFF
        return _to_int32((b3 << 24) | (b2 << 16) | (b1 << 8) | b0)

    @staticmethod
    def rotateLeft(i: int, distance: int) -> int:
        """
        Rotaciona os bits de i à esquerda por distance posições.

        Bits que saem pela esquerda reentram pela direita.
        Apenas os 5 bits menos significativos de distance são usados
        (módulo 32) — comportamento definido pela especificação Java.
        Distâncias negativas equivalem a rotateRight.

        Equivalente a Integer.rotateLeft(int i, int distance).

        Exemplos
        --------
        >>> JInteger.rotateLeft(1, 1)
        2
        >>> JInteger.rotateLeft(-2147483648, 1)    # MIN_VALUE → 1
        1
        >>> JInteger.rotateLeft(42, 32)            # noop
        42
        """
        distance &= 0x1F   # módulo 32; trata negativo e > 32 automaticamente
        if distance == 0:
            return _to_int32(i)
        n = _to_uint32(i)
        return _to_int32(((n << distance) | (n >> (32 - distance))) & _MASK32)

    @staticmethod
    def rotateRight(i: int, distance: int) -> int:
        """
        Rotaciona os bits de i à direita por distance posições.

        Equivalente a Integer.rotateRight(int i, int distance).
        Implementado como rotateLeft(i, 32 - distance & 0x1F).

        Exemplos
        --------
        >>> JInteger.rotateRight(1, 1)
        -2147483648
        >>> JInteger.rotateRight(42, 32)           # noop
        42
        """
        return JInteger.rotateLeft(i, -distance)
    
    @staticmethod
    def signum(i: int) -> int:
        """
        Retorna o sinal do inteiro: -1, 0 ou +1.

        Equivalente a Integer.signum(int i).

        Exemplos
        --------
        >>> JInteger.signum(-100)
        -1
        >>> JInteger.signum(0)
        0
        >>> JInteger.signum(42)
        1
        """
        i = _to_int32(i)
        return (i > 0) - (i < 0)
    
    @staticmethod
    def sum(a: int, b: int) -> int:
        """
        Soma dois inteiros com comportamento de overflow Java (silencioso).

        MAX_VALUE + 1 == MIN_VALUE, exatamente como em Java.

        Equivalente a Integer.sum(int a, int b).

        Exemplos
        --------
        >>> JInteger.sum(2147483647, 1)
        -2147483648
        """
        return _to_int32(a + b)

    @staticmethod
    def max(a: int, b: int) -> int:
        """
        Retorna o maior entre dois inteiros de 32 bits com sinal.

        Equivalente a Integer.max(int a, int b).
        """
        return a if _to_int32(a) >= _to_int32(b) else b

    @staticmethod
    def min(a: int, b: int) -> int:
        """
        Retorna o menor entre dois inteiros de 32 bits com sinal.

        Equivalente a Integer.min(int a, int b).
        """
        return a if _to_int32(a) <= _to_int32(b) else b
    
    @staticmethod
    def compare(x: int, y: int) -> int:
        """
        Compara numericamente dois inteiros de 32 bits com sinal.

        Retorna: 0 se iguais, valor negativo se x < y, positivo se x > y.

        Equivalente a Integer.compare(int x, int y).
        """
        x, y = _to_int32(x), _to_int32(y)
        return (x > y) - (x < y)

    @staticmethod
    def compareUnsigned(x: int, y: int) -> int:
        """
        Compara dois inteiros de 32 bits como valores sem sinal.

        -1 é interpretado como 4294967295 (maior que qualquer valor positivo).

        Equivalente a Integer.compareUnsigned(int x, int y).

        Exemplos
        --------
        >>> JInteger.compareUnsigned(-1, 1)    # 0xFFFFFFFF > 1
        1
        >>> JInteger.compareUnsigned(-1, -1)
        0
        """
        ux, uy = _to_uint32(x), _to_uint32(y)
        return (ux > uy) - (ux < uy)

    @staticmethod
    def divideUnsigned(dividend: int, divisor: int) -> int:
        """
        Divisão inteira tratando ambos os operandos como unsigned de 32 bits.

        Equivalente a Integer.divideUnsigned(int dividend, int divisor).

        Exceções
        --------
        ZeroDivisionError
            Se divisor for zero.

        Exemplos
        --------
        >>> JInteger.divideUnsigned(-1, 2)    # 4294967295 // 2
        2147483647
        """
        return _to_int32(_to_uint32(dividend) // _to_uint32(divisor))

    
    @staticmethod
    def remainderUnsigned(dividend: int, divisor: int) -> int:
        """
        Resto da divisão inteira tratando ambos os operandos como unsigned de 32 bits.

        Equivalente a Integer.remainderUnsigned(int dividend, int divisor).

        Exceções
        --------
        ZeroDivisionError
            Se divisor for zero.

        Exemplos
        --------
        >>> JInteger.remainderUnsigned(-1, 2)    # 4294967295 % 2
        1
        """
        return _to_int32(_to_uint32(dividend) % _to_uint32(divisor))

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
    
    # ------------------------------------------------------------------
    # decode
    # ------------------------------------------------------------------

    @staticmethod
    def decode(nm: Optional[str]) -> 'JInteger':
        """
        Decodifica uma String para JInteger aceitando decimal, hex e octal.

        Formatos aceitos (sinal '+'/'-' opcional antes do prefixo):
            decimal      → "42", "-42", "+42"
            hexadecimal  → "0x1F", "0X1F", "#1F"
            octal        → "017"

        Equivalente a Integer.decode(String nm).

        Exceções
        --------
        NumberFormatException
            nm nulo, vazio, formato inválido, ou valor fora de [-2^31, 2^31-1].

        Exemplos
        --------
        >>> JInteger.decode("0xFF").intValue()
        255
        >>> JInteger.decode("-017").intValue()
        -15
        """
        if nm is None or len(nm) == 0:
            raise NumberFormatException("decode: argumento nulo ou string vazia")

        s = nm.strip()
        if not s:
            raise NumberFormatException("decode: string em branco")

        negative = False
        idx = 0
        if s[0] == '-':
            negative = True
            idx = 1
        elif s[0] == '+':
            idx = 1

        radix = 10
        if s[idx:idx + 2].lower() == '0x':
            radix = 16
            idx += 2
        elif s[idx:idx + 1] == '#':
            radix = 16
            idx += 1
        elif s[idx:idx + 1] == '0' and len(s) > idx + 1:
            radix = 8
            idx += 1

        digits = s[idx:]
        if not digits:
            raise NumberFormatException(f'decode: sem dígitos em "{nm}"')

        try:
            magnitude = int(digits, radix)
        except ValueError:
            raise NumberFormatException(f'decode: "{nm}" não é um inteiro válido')

        value = -magnitude if negative else magnitude

        if value < -(2**31) or value > (2**31 - 1):
            raise NumberFormatException(f'decode: valor fora do intervalo: "{nm}"')

        return JInteger.valueOf(value)
    
    @staticmethod
    def bitCount(i: int) -> int:
        """
        Conta os bits 1 na representação de 32 bits (population count / popcount).

        Algoritmo: Hacker's Delight cap. 5 — soma paralela em pares de bits.
        Complexidade: O(1) com 5 operações de redução.

        Equivalente a Integer.bitCount(int i).

        Exemplos
        --------
        >>> JInteger.bitCount(-1)
        32
        >>> JInteger.bitCount(7)
        3
        >>> JInteger.bitCount(0)
        0
        """
        n = _to_uint32(i)
        # Soma pares de bits adjacentes em paralelo
        n = n - ((n >> 1) & 0x5555_5555)
        # Soma grupos de 4 bits
        n = (n & 0x3333_3333) + ((n >> 2) & 0x3333_3333)
        # Soma grupos de 8 bits; máscara elimina overflow interno
        n = (n + (n >> 4)) & 0x0F0F_0F0F
        # Multiplica para acumular nos 8 bits mais altos; shift extrai resultado
        return ((n * 0x0101_0101) & _MASK32) >> 24

    @staticmethod
    def highestOneBit(i: int) -> int:
        """
        Retorna um valor com apenas o bit 1 mais significativo de i.

        Retorna 0 se i == 0; retorna MIN_VALUE se o bit 31 estiver setado.

        Algoritmo: propaga o bit mais alto progressivamente para baixo via OR,
        depois isola o topo com (i XOR i>>1) equivalente a (i - i>>1).

        Equivalente a Integer.highestOneBit(int i).

        Exemplos
        --------
        >>> JInteger.highestOneBit(10)    # 0b1010 → 0b1000
        8
        >>> JInteger.highestOneBit(-1)    # MSB de 0xFFFFFFFF = bit 31
        -2147483648
        >>> JInteger.highestOneBit(0)
        0
        """
        n = _to_uint32(i)
        n |= (n >> 1)
        n |= (n >> 2)
        n |= (n >> 4)
        n |= (n >> 8)
        n |= (n >> 16)
        return _to_int32(n - (n >> 1))

    @staticmethod
    def lowestOneBit(i: int) -> int:
        """
        Retorna um valor com apenas o bit 1 menos significativo de i.

        Retorna 0 se i == 0.

        Algoritmo: n & (-n) isola o bit menos significativo em complemento
        de dois — propriedade fundamental do two's complement.

        Equivalente a Integer.lowestOneBit(int i).

        Exemplos
        --------
        >>> JInteger.lowestOneBit(12)    # 0b1100 → 0b0100
        4
        >>> JInteger.lowestOneBit(-12)   # same LSB
        4
        """
        u = _to_uint32(i)
        return _to_int32(u & (-u & _MASK32))

    @staticmethod
    def numberOfLeadingZeros(i: int) -> int:
        """
        Conta zeros à esquerda do bit 1 mais alto na representação de 32 bits.

        Retorna 32 se i == 0.

        Algoritmo: busca binária por halvings (Hacker's Delight §5-3).
        Em cada passo, testa se os n bits mais altos são todos zero;
        se sim, descarta a metade inferior e acumula o contador.

        Equivalente a Integer.numberOfLeadingZeros(int i).

        Exemplos
        --------
        >>> JInteger.numberOfLeadingZeros(0)
        32
        >>> JInteger.numberOfLeadingZeros(1)
        31
        >>> JInteger.numberOfLeadingZeros(-1)    # bit 31 setado
        0
        """
        n = _to_uint32(i)
        if n == 0:
            return 32
        count = 0
        if n <= 0x0000_FFFF: 
            count += 16; n <<= 16  # noqa: E702
        if n <= 0x00FF_FFFF: 
            count += 8;  n <<= 8   # noqa: E702
        if n <= 0x0FFF_FFFF: 
            count += 4;  n <<= 4   # noqa: E702
        if n <= 0x3FFF_FFFF: 
            count += 2;  n <<= 2   # noqa: E702
        if n <= 0x7FFF_FFFF: 
            count += 1              # noqa: E702
        return count

    @staticmethod
    def numberOfTrailingZeros(i: int) -> int:
        """
        Conta zeros à direita do bit 1 menos significativo na representação de 32 bits.

        Retorna 32 se i == 0.

        Algoritmo: isola o LSB com n & (-n), depois aplica numberOfLeadingZeros
        e ajusta: NTZ(n) = 31 - NLZ(lowestOneBit(n)).

        Equivalente a Integer.numberOfTrailingZeros(int i).

        Exemplos
        --------
        >>> JInteger.numberOfTrailingZeros(0)
        32
        >>> JInteger.numberOfTrailingZeros(8)    # 0b1000
        3
        >>> JInteger.numberOfTrailingZeros(1)
        0
        """
        n = _to_uint32(i)
        if n == 0:
            return 32
        low = n & (-n & _MASK32)
        return 31 - JInteger.numberOfLeadingZeros(low)

    @staticmethod
    def reverse(i: int) -> int:
        """
        Inverte a ordem de todos os 32 bits.

        Algoritmo: permutação paralela por trocas de metades sucessivas
        (Hacker's Delight §7-1). Cinco passos de complexidade O(1):
          passo 1: troca bits vizinhos (granularidade 1)
          passo 2: troca pares  (granularidade 2)
          passo 3: troca nibbles (granularidade 4)
          passo 4: troca bytes  (granularidade 8)
          passo 5: troca half-words (granularidade 16)

        Equivalente a Integer.reverse(int i).

        Exemplos
        --------
        >>> JInteger.reverse(1)       # 0x00000001 → 0x80000000
        -2147483648
        >>> JInteger.reverse(JInteger.reverse(42)) == 42
        True
        """
        n = _to_uint32(i)
        n = ((n & 0x5555_5555) << 1)  | ((n >> 1)  & 0x5555_5555)
        n = ((n & 0x3333_3333) << 2)  | ((n >> 2)  & 0x3333_3333)
        n = ((n & 0x0F0F_0F0F) << 4)  | ((n >> 4)  & 0x0F0F_0F0F)
        n = ((n & 0x00FF_00FF) << 8)  | ((n >> 8)  & 0x00FF_00FF)
        n = ((n & 0x0000_FFFF) << 16) | ((n >> 16) & 0x0000_FFFF)
        return _to_int32(n & _MASK32)
