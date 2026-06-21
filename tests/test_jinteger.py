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


@pytest.mark.skip(reason="Ainda não está na main")
class TestToString:
    def test_instancia_sem_argumentos(self):
        assert JInteger(42).toString() == '42'
 
    def test_estatico_com_radix(self):
        assert JInteger.toString(255, 16) == 'ff'
 
 
@pytest.mark.skip(reason="Ainda não está na main")
class TestHashCode:
    def test_instancia_sem_argumentos(self):
        assert JInteger(42).hashCode() == 42

    def test_estatico_com_valor_negativo(self):
        assert JInteger.hashCode(-1) == -1
 