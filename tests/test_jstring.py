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
 