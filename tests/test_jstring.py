 """
Testes unitários para JString (Java SE 8 String API em Python)
 
Estrutura: 2 testes por método
  - test_*_happy: fluxo feliz
  - test_*_edge:  caso de borda
"""
 
import pytest
from javalang.jstring import JString
# ===========================================================================
# Acesso e Tamanho
# ===========================================================================
 
class TestAccessAndSize:
  
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