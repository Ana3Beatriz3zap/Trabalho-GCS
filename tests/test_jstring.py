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

