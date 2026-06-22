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