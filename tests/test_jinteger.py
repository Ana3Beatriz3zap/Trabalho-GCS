"""
Suíte de testes para os métodos de conversão numérica de JInteger:
    - byteValue()
    - shortValue()
    - intValue()
    - longValue()
    - floatValue()
"""
import pytest

from javalang.jinteger import JInteger

class TestByteValue:
    def test_dentro_do_intervalo_signed_byte(self):
        assert JInteger(100).byteValue() == 100

    def test_zero(self):
        assert JInteger(0).byteValue() == 0

    def test_127_permanece_127(self):
        assert JInteger(127).byteValue() == 127

    def test_negativo_simples(self):
        assert JInteger(-1).byteValue() == -1

    def test_negativo_129_estoura_para_127(self):
        assert JInteger(-129).byteValue() == 127

class TestShortValue:
    def test_dentro_do_intervalo_signed_short(self):
        assert JInteger(1000).shortValue() == 1000

    def test_32768_estoura_para_negativo_32768(self):
        assert JInteger(32768).shortValue() == -32768

class TestIntValue:
    def test_retorna_valor_original(self):
        assert JInteger(12345).intValue() == 12345

    def test_retorna_limite_superior_int(self):
        assert JInteger(JInteger.MAX_VALUE).intValue() == 2147483647

class TestLongValue:
    def test_retorna_valor_original(self):
        assert JInteger(500).longValue() == 500

    def test_retorna_limite_inferior_int(self):
        assert JInteger(JInteger.MIN_VALUE).longValue() == -2147483648

class TestFloatValue:
    def test_conversao_valor_simples(self):
        assert JInteger(42).floatValue() == 42.0


@pytest.mark.skip(reason="Ainda não implementado na main")
class TestDoubleValue:
    def test_conversao_valor_simples(self):
        assert JInteger(42).doubleValue() == 42.0
 
    def test_conversao_sem_perda_de_precisao_no_limite_superior(self):
        assert JInteger(JInteger.MAX_VALUE).doubleValue() == 2147483647.0

@pytest.mark.skip(reason="Ainda não implementado na main")
class TestEquals:
    def test_mesmo_valor_retorna_true(self):
        assert JInteger(5).equals(JInteger(5)) is True
        
    def test_valores_diferentes_retorna_false(self):
        assert JInteger(5).equals(JInteger(6)) is False

@pytest.mark.skip(reason="Ainda não implementado na main")
class TestCompareTo:
    def test_este_menor_que_outro_retorna_negativo(self):
        assert JInteger(1).compareTo(JInteger(2)) < 0
 
    def test_valores_iguais_retorna_zero(self):
        assert JInteger(5).compareTo(JInteger(5)) == 0