"""
Testes unitários para JString (Java SE 8 String API em Python)
 
Estrutura: 2 testes por método
  - test_*_happy: fluxo feliz
  - test_*_edge:  caso de borda
"""
 
import pytest
from javalang.jstring import JString

# ===========================================================================
# Construtores
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestConstructors:
    def test_from_jstring_happy(self):
        """String(String original) a partir de JString."""
        original = JString("copy")
        copy = JString(original)
        assert copy.equals(original)
        assert copy is not original
    
    def test_from_char_list_happy(self):
        """String(char[]) a partir de lista de chars."""
        chars = ["H", "i", "!"]
        s = JString(chars)
        assert str(s) == "Hi!"

    def test_from_bytes_happy(self):
        """String(byte[]) decodifica UTF-8 por padrão."""
        b = "hello".encode("utf-8")
        s = JString(b)
        assert str(s) == "hello"
    
    def test_from_bytes_offset_count_happy(self):
        """String(byte[], offset, count) extrai sub-array."""
        b = b"abcdef"
        s = JString(b, offset=2, count=3)
        assert str(s) == "cde"

    def test_from_codepoints_happy(self):
        """String(int[] codePoints, offset, count)."""
        cps = [72, 101, 108, 108, 111]  # "Hello"
        s = JString(cps, offset=0, count=5)
        assert str(s) == "Hello"

    def test_constructor_none_raises(self):
        """Tipo inválido deve lançar TypeError."""
        with pytest.raises(TypeError):
            JString(12345)  # int puro não é suportado
 
 