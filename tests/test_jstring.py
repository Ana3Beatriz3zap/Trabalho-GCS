"""
Testes unitários para JString (Java SE 8 String API em Python)
 
Estrutura: 2 testes por método
  - test_*_happy: fluxo feliz
  - test_*_edge:  caso de borda
"""
# mypy: ignore-errors
import pytest
from javalang.jstring import JString

# ===========================================================================
# Construtores
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestConstructors:
 
    def test_default_constructor_happy(self):
        """String() cria string vazia."""
        s = JString()
        assert s.length() == 0
        assert str(s) == ""
     
    def test_default_constructor_edge_isEmpty(self):
        """String() deve ser isEmpty()."""
        assert JString().isEmpty() is True
 
    def test_from_str_happy(self):
        """String(String) copia o conteúdo."""
        s = JString("Python")
        assert str(s) == "Python"
    
    def test_from_jstring_happy(self):
        """String(String original) a partir de JString."""
        original = JString("copy")
        copy = JString(original)
        assert copy.equals(original)
        assert copy is not original

     
    def test_from_jstring_edge_empty(self):
        """Cópia de JString vazio."""
        original = JString()
        copy = JString(original)
        assert copy.isEmpty()

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
 
 
 