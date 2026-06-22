"""
JString — Implementação Python da java.lang.String (Java SE 8)
 
Referência: https://docs.oracle.com/javase/8/docs/api/java/lang/String.html
 
Decisões de Projeto:
  1. Imutabilidade: JString é imutável — todos os métodos de transformação
     retornam novas instâncias.
  2. Armazenamento interno: _value (str Python) + _chars (list[str] de code units).
  3. char[] Java: representado como list[str] de strings de comprimento 1.
  4. byte[] Java: representado como bytes ou list[int].
  5. codePoint: int Python (equivalente ao int de 32 bits Java).
  6. Nomes camelCase preservados conforme especificação Java.
  7. None tratado como NullPointerException (ValueError em Python).
  8. Charset: suporta nomes Java e Python via mapeamento interno.
  9. intern(): delegado a sys.intern() sobre a str interna.
  10. format(): suporta placeholders Java (%s, %d, %f, %b, %c, %x, %o) via
      conversão para sintaxe Python.
"""

 
from __future__ import annotations
 
import re
from typing import Optional, Union, Any, cast

# ---------------------------------------------------------------------------
# Mapeamento de charset Java → Python
# ---------------------------------------------------------------------------
_CHARSET_MAP: dict[str, str] = {
    "UTF-8": "utf-8",
    "UTF-16": "utf-16",
    "UTF-16BE": "utf-16-be",
    "UTF-16LE": "utf-16-le",
    "US-ASCII": "ascii",
    "ISO-8859-1": "latin-1",
    "ISO8859-1": "latin-1",
    "windows-1252": "cp1252",
}
 
def _resolve_charset(charset: str) -> str:
    """Resolve nome de charset Java para Python."""
    return _CHARSET_MAP.get(charset, charset)
 
 
def _to_char_list(s: str) -> list[str]:
    """Converte str Python em lista de code units UTF-16 (simulando char[] Java).
 
    Java usa UTF-16, então pares substitutos ocupam 2 posições.
    Python usa code points diretamente; aqui preservamos a semântica Java.
    """
    result: list[str] = []
    for ch in s:
        cp = ord(ch)
        if cp > 0xFFFF:
            # Suplementar: codifica como par substituto (surrogate pair)
            cp -= 0x10000
            high = 0xD800 | (cp >> 10)
            low = 0xDC00 | (cp & 0x3FF)
            result.append(chr(high))
            result.append(chr(low))
        else:
            result.append(ch)
    return result
 
 
def _from_char_list(chars: list[str]) -> str:
    """Reconstrói str Python a partir de lista de code units UTF-16."""
    result = []
    i = 0
    while i < len(chars):
        cp = ord(chars[i])
        if 0xD800 <= cp <= 0xDBFF and i + 1 < len(chars):
            low = ord(chars[i + 1])
            if 0xDC00 <= low <= 0xDFFF:
                full = 0x10000 + ((cp - 0xD800) << 10) + (low - 0xDC00)
                result.append(chr(full))
                i += 2
                continue
        result.append(chars[i])
        i += 1
    return "".join(result)

def _validate_not_none(value: object, name: str = "value") -> None:
    """Lança NullPointerException equivalente (ValueError) se None."""
    if value is None:
        raise ValueError(f"NullPointerException: {name} is null")
 
 
def _validate_index(index: int, length: int) -> None:
    """Lança StringIndexOutOfBoundsException equivalente."""
    if not (0 <= index < length):
        raise IndexError(
            f"StringIndexOutOfBoundsException: index {index}, length {length}"
        )
 
 
def _validate_range(begin: int, end: int, length: int) -> None:
    """Valida intervalo [begin, end) dentro de [0, length]."""
    if begin < 0:
        raise IndexError(f"StringIndexOutOfBoundsException: begin {begin} < 0")
    if end > length:
        raise IndexError(
            f"StringIndexOutOfBoundsException: end {end} > length {length}"
        )
    if begin > end:
        raise IndexError(
            f"StringIndexOutOfBoundsException: begin {begin} > end {end}"
        )
 

# ---------------------------------------------------------------------------
# Classe principal
# ---------------------------------------------------------------------------
 
 
class JString:
    """Implementação Python fiel à java.lang.String (Java SE 8).
 
    Todos os métodos preservam a semântica Java incluindo:
    - Indexação por code units UTF-16 (não code points)
    - Comportamento de null → ValueError (NullPointerException)
    - Retorno de novas instâncias em transformações (imutabilidade)
    """
 
    # ------------------------------------------------------------------
    # Construtores
    # ------------------------------------------------------------------
 
    def __init__(
        self,
        value: Union[str, "JString", list, bytes, None] = None,
        charset: Optional[str] = None,
        offset: Optional[int] = None,
        count: Optional[int] = None,
    ) -> None:
        """Implementa os construtores Java String.
 
        Mapeamentos:
          String()                        → JString()
          String(String original)         → JString(jstring_or_str)
          String(char[] value)            → JString(list_of_chars)
          String(char[], offset, count)   → JString(list_of_chars, offset=o, count=c)
          String(byte[] bytes)            → JString(bytes_obj)
          String(byte[], charset)         → JString(bytes_obj, charset=cs)
          String(byte[], offset, count)   → JString(bytes_obj, offset=o, count=c)
          String(StringBuilder)           → JString(str_or_jstring)
        """
        if value is None:
            self._chars: list[str] = []
        elif isinstance(value, JString):
            self._chars = list(value._chars)
        elif isinstance(value, str):
            self._chars = _to_char_list(value)
        elif isinstance(value, (bytes, bytearray)):
            cs = _resolve_charset(charset) if charset else "utf-8"
            raw = bytes(value)
            if offset is not None and count is not None:
                raw = raw[offset: offset + count]
            self._chars = _to_char_list(raw.decode(cs))
            return
        elif isinstance(value, list):
            # char[] or int[] (code points)
            if len(value) == 0:
                self._chars = []
            elif isinstance(value[0], str):
                # char[]
                chars = value
                if offset is not None and count is not None:
                    chars = value[offset: offset + count]
                self._chars = list(chars)
            elif isinstance(value[0], int):
                # int[] codePoints
                if offset is None or count is None:
                    raise ValueError("int[] codePoints requires offset and count")
                segment = value[offset: offset + count]
                self._chars = _to_char_list(
                    "".join(chr(cp) for cp in segment)
                )
            else:
                raise TypeError(
                    f"Unsupported list element type: {type(value[0])}"
                )
        else:
            raise TypeError(f"Unsupported type for JString: {type(value)}")
 
        # Para byte[] sem charset já retornou acima;
        # para demais casos, offset/count aplicam-se à lista de chars.
        if isinstance(value, list):
            pass  # já tratado acima
        elif offset is not None and count is not None and not isinstance(
            value, (bytes, bytearray)
        ):
            self._chars = self._chars[offset: offset + count]

    # ------------------------------------------------------------------
    # Propriedade interna: str Python equivalente
    # ------------------------------------------------------------------

    @property
    def _value(self) -> str:
        return _from_char_list(self._chars)

    # ------------------------------------------------------------------
    # Acesso e Tamanho
    # ------------------------------------------------------------------

    def length(self) -> int:
        """Retorna o número de code units UTF-16 (como Java)."""
        return len(self._chars)

    def isEmpty(self) -> bool:
        """Retorna True se length() == 0."""
        return len(self._chars) == 0
    
    def charAt(self, index: int) -> str:
        """Retorna o char (code unit UTF-16) na posição index.

        Lança IndexError (StringIndexOutOfBoundsException) se fora do range.
        """
        _validate_index(index, len(self._chars))
        return self._chars[index]

    def codePointAt(self, index: int) -> int:
        """Retorna o Unicode code point começando em index.

        Se index aponta para um high surrogate seguido de low surrogate,
        retorna o code point suplementar combinado.
        """
        _validate_index(index, len(self._chars))
        ch = ord(self._chars[index])
        if 0xD800 <= ch <= 0xDBFF and index + 1 < len(self._chars):
            low = ord(self._chars[index + 1])
            if 0xDC00 <= low <= 0xDFFF:
                return 0x10000 + ((ch - 0xD800) << 10) + (low - 0xDC00)
        return ch

    def codePointBefore(self, index: int) -> int:
        """Retorna o code point antes de index (índice exclusivo).

        Lança IndexError se index < 1 ou index > length().
        """
        if index < 1 or index > len(self._chars):
            raise IndexError(
                f"StringIndexOutOfBoundsException: index {index}"
            )
        ch = ord(self._chars[index - 1])
        if 0xDC00 <= ch <= 0xDFFF and index >= 2:
            high = ord(self._chars[index - 2])
            if 0xD800 <= high <= 0xDBFF:
                return 0x10000 + ((high - 0xD800) << 10) + (ch - 0xDC00)
        return ch
    
    def codePointCount(self, beginIndex: int, endIndex: int) -> int:
        """Conta code points Unicode no intervalo [beginIndex, endIndex)."""
        _validate_range(beginIndex, endIndex, len(self._chars))
        count = 0
        i = beginIndex
        while i < endIndex:
            ch = ord(self._chars[i])
            if 0xD800 <= ch <= 0xDBFF and i + 1 < endIndex:
                low = ord(self._chars[i + 1])
                if 0xDC00 <= low <= 0xDFFF:
                    i += 2
                    count += 1
                    continue
            count += 1
            i += 1
        return count
    
    def offsetByCodePoints(self, index: int, codePointOffset: int) -> int:
        """Retorna o índice deslocado por codePointOffset code points a partir de index."""
        n = len(self._chars)
        if index < 0 or index > n:
            raise IndexError(
                f"StringIndexOutOfBoundsException: index {index}"
            )
        i = index
        if codePointOffset >= 0:
            for _ in range(codePointOffset):
                if i >= n:
                    raise IndexError("offsetByCodePoints: offset out of bounds")
                ch = ord(self._chars[i])
                if 0xD800 <= ch <= 0xDBFF and i + 1 < n:
                    low = ord(self._chars[i + 1])
                    if 0xDC00 <= low <= 0xDFFF:
                        i += 2
                        continue
                i += 1
        else:
            for _ in range(-codePointOffset):
                if i <= 0:
                    raise IndexError("offsetByCodePoints: offset out of bounds")
                ch = ord(self._chars[i - 1])
                if 0xDC00 <= ch <= 0xDFFF and i >= 2:
                    high = ord(self._chars[i - 2])
                    if 0xD800 <= high <= 0xDBFF:
                        i -= 2
                        continue
                i -= 1
        return i

    def toCharArray(self) -> list[str]:
        """Retorna cópia da lista de char (code units UTF-16)."""
        return list(self._chars)

    def getChars(
        self,
        srcBegin: int,
        srcEnd: int,
        dst: list[str],
        dstBegin: int,
    ) -> None:
        """Copia chars [srcBegin, srcEnd) para dst a partir de dstBegin (in-place)."""
        _validate_range(srcBegin, srcEnd, len(self._chars))
        count = srcEnd - srcBegin
        if dstBegin < 0 or dstBegin + count > len(dst):
            raise IndexError(
                "ArrayIndexOutOfBoundsException: destination array too small"
            )
        for i in range(count):
            dst[dstBegin + i] = self._chars[srcBegin + i]
    
    def getBytes(self, charset: Optional[str] = None) -> bytes:
        """Encodes a string para bytes usando o charset fornecido (padrão: UTF-8)."""
        cs = _resolve_charset(charset) if charset else "utf-8"
        return self._value.encode(cs)
    
    # ------------------------------------------------------------------
    # Comparação
    # ------------------------------------------------------------------

    def equals(self, other: object) -> bool:
        """Compara com outro objeto. Retorna True apenas se JString com mesmo conteúdo."""
        if isinstance(other, JString):
            return self._chars == other._chars
        if isinstance(other, str):
            return self._value == other
        return False

    def equalsIgnoreCase(self, other: Optional["JString"]) -> bool:
        """Compara ignorando case (ASCII fold + Unicode fold)."""
        if other is None:
            return False
        if isinstance(other, str):
            return self._value.casefold() == other.casefold()
        return self._value.casefold() == other._value.casefold()

    def compareTo(self, other: "JString") -> int:
        """Comparação lexicográfica por code units UTF-16.

        Retorna negativo, zero ou positivo conforme Java.
        """
        _validate_not_none(other, "anotherString")
        a = self._chars
        b = other._chars if isinstance(other, JString) else _to_char_list(other)
        lim = min(len(a), len(b))
        for i in range(lim):
            diff = ord(a[i]) - ord(b[i])
            if diff != 0:
                return diff
        return len(a) - len(b)
    
    def compareToIgnoreCase(self, other: "JString") -> int:
        """Comparação lexicográfica ignorando case."""
        _validate_not_none(other, "str")
        a_str = self._value.casefold()
        b_str = (other._value if isinstance(other, JString) else other).casefold()
        a_chars = _to_char_list(a_str)
        b_chars = _to_char_list(b_str)
        lim = min(len(a_chars), len(b_chars))
        for i in range(lim):
            diff = ord(a_chars[i]) - ord(b_chars[i])
            if diff != 0:
                return diff
        return len(a_chars) - len(b_chars)

    def contentEquals(self, cs: Union[str, "JString"]) -> bool:
        """Compara conteúdo com CharSequence (str ou JString)."""
        _validate_not_none(cs, "cs")
        if isinstance(cs, JString):
            return self._value == cs._value
        return self._value == cs

    def regionMatches(
        self,
        toffset_or_ignoreCase: Union[int, bool],
        other: "JString",
        ooffset: int,
        plen: int,
        ignoreCase: Optional[bool] = None,
    ) -> bool:
        """regionMatches(int toffset, String other, int ooffset, int len)
        regionMatches(boolean ignoreCase, int toffset, String other, int ooffset, int len)
        """
        # Detectar qual sobrecarga está sendo usada
        if isinstance(toffset_or_ignoreCase, bool):
            ic = toffset_or_ignoreCase
            # neste caso: regionMatches(ignoreCase, toffset, other, ooffset, len)
            # mas a assinatura está (bool, JString, int, int) — precisamos do toffset
            # Ajuste: quando bool é passado, other é toffset, ooffset é other, plen é ooffset
            # e um 5º argumento é len. Detectamos pelo ignoreCase parameter.
            raise TypeError(
                "Para regionMatches com ignoreCase, use: "
                "regionMatches(ignoreCase, toffset, other, ooffset, plen)"
            )
        else:
            toffset = toffset_or_ignoreCase
            ic = False

        # Se ignoreCase foi passado como 5º arg, reinterpretar
        # Assinatura correta: regionMatches(bool, int, JString, int, int)
        # chamada: obj.regionMatches(True, 0, other, 0, 5)
        # → toffset_or_ignoreCase=True → detectado acima
        # Assinatura: regionMatches(int, JString, int, int)
        # → toffset_or_ignoreCase=0 (int)
        _validate_not_none(other, "other")
        other_val = other._value if isinstance(other, JString) else other

        if toffset < 0 or ooffset < 0:
            return False
        this_sub = self._value[toffset: toffset + plen]
        other_sub = other_val[ooffset: ooffset + plen]
        if len(this_sub) != plen or len(other_sub) != plen:
            return False
        if ic:
            return this_sub.casefold() == other_sub.casefold()
        return this_sub == other_sub

# ---------------------------------------------------------------------------
# Funções auxiliares internas
# ---------------------------------------------------------------------------

def _java_int(value: int) -> int:
    """Trunca para inteiro Java de 32 bits (complemento de dois)."""
    value &= 0xFFFFFFFF
    if value >= 0x80000000:
        value -= 0x100000000
    return value


def _java_float_str(value: float) -> str:
    """Formata float como Java: sem trailing zeros desnecessários mas sempre com decimal."""
    import math
    if math.isnan(value):
        return "NaN"
    if math.isinf(value):
        return "Infinity" if value > 0 else "-Infinity"
    s = repr(value)
    return s


def _java_replacement(repl: str) -> str:
    """Converte referências de grupo Java ($1, $2) para Python (\\1, \\2)."""
    return re.sub(r"\$(\d+)", r"\\\1", repl)

def _java_format(fmt: str, *args: object) -> str:
    """Processa String.format Java convertendo para str.format Python.

    Especificadores suportados: %s %d %f %b %c %x %X %o %e %E %n %%.
    Flags suportadas: -, 0, largura, precisão.
    """
    result = []
    arg_index = 0
    i = 0
    while i < len(fmt):
        if fmt[i] != "%":
            result.append(fmt[i])
            i += 1
            continue
        i += 1
        if i >= len(fmt):
            raise ValueError("Dangling % in format string")
        # Flags e largura/precisão
        flags = ""
        while i < len(fmt) and fmt[i] in "-+0 ,(":
            flags += fmt[i]
            i += 1
        width = ""
        while i < len(fmt) and fmt[i].isdigit():
            width += fmt[i]
            i += 1
        precision = ""
        if i < len(fmt) and fmt[i] == ".":
            i += 1
            while i < len(fmt) and fmt[i].isdigit():
                precision += fmt[i]
                i += 1
        if i >= len(fmt):
            raise ValueError("Incomplete format specifier")
        spec = fmt[i]
        i += 1

        if spec == "%":
            result.append("%")
            continue
        if spec == "n":
            result.append("\n")
            continue

        if arg_index >= len(args):
            raise ValueError(
                "MissingFormatArgumentException: not enough arguments"
            )
        arg = args[arg_index]
        arg_index += 1

        # Construir especificador Python
        w = width or ""
        lf = "-" if "-" in flags else ""
        zf = "0" if ("0" in flags and "-" not in flags) else ""

        if spec == "s":
            s = "null" if arg is None else str(arg)
            if precision:
                s = s[: int(precision)]
            if width:
                w_int = int(width)
                s = s.ljust(w_int) if "-" in flags else s.rjust(w_int)
            result.append(s)
        elif spec == "d":
            v_int = int(cast(Any, arg))  # v_int utilizado para inteiros
            py_fmt = f"%{lf}{zf}{w}d"
            result.append(py_fmt % v_int)
        elif spec in ("f",):
            v_float = float(cast(Any, arg))  # v_float utilizado para floats
            prec = precision or "6"
            py_fmt = f"%{lf}{zf}{w}.{prec}f"
            result.append(py_fmt % v_float)
        elif spec in ("e", "E"):
            v_float = float(cast(Any, arg))  # v_float utilizado para floats
            prec = precision or "6"
            py_fmt = f"%{lf}{zf}{w}.{prec}{spec}"
            result.append(py_fmt % v_float)
        elif spec == "b":
            if arg is None:
                result.append("false")
            elif isinstance(arg, bool):
                result.append("true" if arg else "false")
            else:
                result.append("true")  # Java: qualquer não-null não-bool → true
        elif spec == "c":
            if isinstance(arg, int):
                result.append(chr(arg))
            elif isinstance(arg, str) and len(arg) == 1:
                result.append(arg)
            else:
                raise ValueError("IllegalFormatConversionException: %c needs char")
        elif spec == "x":
            v_int = int(cast(Any, arg))
            py_fmt = f"%{lf}{zf}{w}x"
            result.append(py_fmt % v_int)
        elif spec == "X":
            v_int = int(cast(Any, arg))
            py_fmt = f"%{lf}{zf}{w}X"
            result.append(py_fmt % v_int)
        elif spec == "o":
            v_int = int(cast(Any, arg))
            py_fmt = f"%{lf}{zf}{w}o"
            result.append(py_fmt % v_int)
        else:
            raise ValueError(f"UnknownFormatConversionException: '{spec}'")

    return "".join(result)
