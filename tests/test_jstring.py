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

    def test_startsWith_happy(self):
        """startsWith retorna True para prefixo correto."""
        s = JString("Hello")
        assert s.startsWith(JString("He")) is True

    def test_endsWith_happy(self):
        """endsWith retorna True para sufixo correto."""
        s = JString("Hello World")
        assert s.endsWith(JString("World")) is True
 
import pytest
from javalang.jstring import JString
# ===========================================================================
# Transformação
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestTransformation:
    def test_substring_happy(self):
        """substring(beginIndex) retorna do índice ao fim."""
        s = JString("Hello World")
        assert str(s.substring(6)) == "World"

    def test_subSequence_happy(self):
        """subSequence equivale a substring(begin, end)."""
        s = JString("Hello")
        assert str(s.subSequence(1, 4)) == "ell"

    def test_concat_happy(self):
        """concat junta duas strings."""
        a = JString("Hello, ")
        b = JString("World!")
        assert str(a.concat(b)) == "Hello, World!"

# ===========================================================================
# Expressões Regulares
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestRegex:
    def test_matches_happy(self):
        """matches retorna True quando string casa completamente com regex."""
        s = JString("12345")
        assert s.matches(r"\d+") is True

    def test_replaceFirst_happy(self):
        """replaceFirst substitui apenas a primeira ocorrência."""
        s = JString("aaa")
        assert str(s.replaceFirst("a", "b")) == "baa"

# ===========================================================================
# Métodos Estáticos
# ===========================================================================
@pytest.mark.skip(reason="Ainda não está na main")
class TestStaticMethods:
    def test_valueOf_int_happy(self):
        """valueOf(int) converte inteiro."""
        assert str(JString.valueOf(42)) == "42"
    
    def test_valueOf_float_happy(self):
        """valueOf(float) converte float."""
        result = str(JString.valueOf(3.14))
        assert "3.14" in result
