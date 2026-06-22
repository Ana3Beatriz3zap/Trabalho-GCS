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

    def test_contentEquals_happy(self):
        """contentEquals com str Python equivalente."""
        assert JString("hello").contentEquals("hello")
    
    def test_regionMatches_happy(self):
        """regionMatches encontra sub-região correta."""
        s = JString("Hello World")
        other = JString("World")
        assert s.regionMatches(6, other, 0, 5) is True

    def test_hashCode_happy(self):
        """hashCode de 'hello' deve corresponder ao valor Java."""
        # Java: "hello".hashCode() == 99162322
        assert JString("hello").hashCode() == 99162322