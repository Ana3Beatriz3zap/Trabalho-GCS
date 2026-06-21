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

class TestCompareUnsigned:
    def test_menos_um_e_maior_que_qualquer_positivo_como_unsigned(self):
        assert JInteger.compareUnsigned(-1, 1) > 0
 
    def test_valores_iguais_retorna_zero(self):
        assert JInteger.compareUnsigned(-1, -1) == 0

class TestDivideUnsigned:
    def test_divisao_simples(self):
        assert JInteger.divideUnsigned(10, 3) == 3
    
    def test_dividendo_negativo_interpretado_como_unsigned(self):
        assert JInteger.divideUnsigned(-1, 2) == JInteger.MAX_VALUE
 
class TestRemainderUnsigned:
    def test_resto_simples(self):
        assert JInteger.remainderUnsigned(10, 3) == 1
 
    def test_dividendo_negativo_interpretado_como_unsigned(self):
        assert JInteger.remainderUnsigned(-1, 2) == 1
 
class TestParseInt:
    def test_string_decimal_simples(self):
        assert JInteger.parseInt("473") == 473