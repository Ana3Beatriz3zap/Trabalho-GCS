"""
Suíte de testes para os métodos de conversão numérica de JInteger:
    - byteValue()
    - shortValue()
    - intValue()
    - longValue()
    - floatValue()
"""
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
