"""
Testes unitários para JString (Java SE 8 String API em Python)
 
Estrutura: 2 testes por método
  - test_*_happy: fluxo feliz
  - test_*_edge:  caso de borda
"""
 
import pytest
from javalang.jstring import JString
# ===========================================================================
# Comparação
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestComparison:
     
    def test_equals_happy(self):
        """equals retorna True para mesma string."""
        assert JString("abc").equals(JString("abc"))

    def test_equalsIgnoreCase_happy(self):
        """equalsIgnoreCase ignora maiúsculas/minúsculas."""
        assert JString("Hello").equalsIgnoreCase(JString("HELLO"))
  
    def test_compareTo_happy(self):
        """compareTo retorna 0 para strings iguais."""
        assert JString("abc").compareTo(JString("abc")) == 0