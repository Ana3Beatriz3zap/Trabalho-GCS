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
import sys
import unicodedata
from typing import List, Optional, Union

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
 