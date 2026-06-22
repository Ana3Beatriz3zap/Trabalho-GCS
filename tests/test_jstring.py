"""
Testes unitários para JString (Java SE 8 String API em Python)
 
Estrutura: 2 testes por método
  - test_*_happy: fluxo feliz
  - test_*_edge:  caso de borda
"""
 
import pytest
from javalang.jstring import JString
# ===========================================================================
# Busca
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestSearch:
    def test_indexOf_char_happy(self):
        """indexOf(int ch) encontra primeira ocorrência."""
        s = JString("hello")
        assert s.indexOf(ord("l")) == 2

    def test_lastIndexOf_char_happy(self):
        """lastIndexOf(int ch) retorna última posição."""
        s = JString("hello")
        assert s.lastIndexOf(ord("l")) == 3

    def test_contains_happy(self):
        """contains retorna True quando substring existe."""
        s = JString("Hello World")
        assert s.contains(JString("World")) is True
 