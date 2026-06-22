import pytest
from jstring import JString, _java_int, _to_char_list
 

# ===========================================================================
# Acesso e Tamanho
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestAccessAndSize:
     
    def test_isEmpty_happy(self, empty):
        """isEmpty() retorna True para string vazia."""
        assert empty.isEmpty() is True

    def test_charAt_happy(self, hello):
        """charAt(0) retorna primeiro char."""
        assert hello.charAt(0) == "H"

    def test_codePointAt_happy(self):
        """codePointAt retorna code point BMP."""
        s = JString("A")
        assert s.codePointAt(0) == 65

    def test_codePointBefore_happy(self):
        """codePointBefore(1) retorna code point do primeiro char."""
        s = JString("Z")
        assert s.codePointBefore(1) == 90  # ord('Z')

    def test_codePointCount_happy(self):
        """codePointCount de string BMP conta 1:1."""
        s = JString("hello")
        assert s.codePointCount(0, 5) == 5
        
    def test_offsetByCodePoints_happy(self):
        """offsetByCodePoints avança N code points."""
        s = JString("abcde")
        assert s.offsetByCodePoints(0, 3) == 3

