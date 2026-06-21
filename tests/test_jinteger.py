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
class TestParseUnsignedInt:
    def test_string_decimal_simples(self):
        assert JInteger.parseUnsignedInt("ff", 16) == 255
 
    def test_valor_acima_de_max_value_retorna_negativo(self):
        assert JInteger.parseUnsignedInt("4294967295") == -1

class TestValueOf:
    def test_valor_a_partir_de_string_com_radix(self):
        assert JInteger.valueOf("ff", 16).intValue() == 255
    
    def test_cache_retorna_mesma_instancia_no_intervalo_128(self):
        assert JInteger.valueOf(-128) is JInteger.valueOf(-128)

class TestDecode:
    def test_string_hexadecimal_com_prefixo_0x(self):
        assert JInteger.decode("0xFF").intValue() == 255
 
    def test_string_octal_negativa(self):
        assert JInteger.decode("-017").intValue() == -15

class TestSum:
    def test_soma_simples(self):
        assert JInteger.sum(2, 3) == 5
 
    def test_overflow_estoura_para_min_value(self):
        assert JInteger.sum(JInteger.MAX_VALUE, 1) == JInteger.MIN_VALUE

class TestMax:
    def test_segundo_argumento_maior(self):
        assert JInteger.max(2, 3) == 3

    def test_comparacao_entre_negativos(self):
        assert JInteger.max(-5, -1) == -1

class TestMin:
    def test_primeiro_argumento_menor(self):
        assert JInteger.min(2, 3) == 2
 
    def test_comparacao_entre_negativos(self):
        assert JInteger.min(-5, -1) == -5
  
class TestCompare:
    def test_x_menor_que_y_retorna_negativo(self):
        assert JInteger.compare(1, 2) < 0
class TestNumberOfLeadingZeros:
    def test_valor_um_tem_31_zeros_a_esquerda(self):
        assert JInteger.numberOfLeadingZeros(1) == 31
 
    def test_zero_retorna_32(self):
        assert JInteger.numberOfLeadingZeros(0) == 32

class TestNumberOfTrailingZeros:
    def test_valor_oito_tem_3_zeros_a_direita(self):
        assert JInteger.numberOfTrailingZeros(8) == 3

    def test_zero_retorna_32(self):
        assert JInteger.numberOfTrailingZeros(0) == 32

class TestReverse:
    def test_bit_unico_vai_para_extremo_oposto(self):
        assert JInteger.reverse(1) == JInteger.MIN_VALUE
 
    def test_reverse_de_reverse_retorna_valor_original(self):
        assert JInteger.reverse(JInteger.reverse(42)) == 42
        
class TestSignum:
    def test_valor_positivo(self):
        assert JInteger.signum(42) == 1
 
class TestRotateRight:
    def test_rotacao_simples(self):
        assert JInteger.rotateRight(1, 1) == JInteger.MIN_VALUE
 
    def test_distancia_multipla_de_32_e_noop(self):
        assert JInteger.rotateRight(42, 32) == 42
 
 
class TestBitCount:
    def test_valor_positivo_simples(self):
        assert JInteger.bitCount(7) == 3

    def test_todos_os_bits_setados(self):
        assert JInteger.bitCount(-1) == 32

class TestHighestOneBit:
    def test_valor_positivo_simples(self):
        assert JInteger.highestOneBit(10) == 8
 
    def test_bit_31_setado_retorna_min_value(self):
        assert JInteger.highestOneBit(-1) == JInteger.MIN_VALUE

class TestLowestOneBit:
    def test_valor_positivo_simples(self):
        assert JInteger.lowestOneBit(12) == 4

class TestToUnsignedString:
    def test_valor_positivo_simples(self):
        assert JInteger.toUnsignedString(5) == '5'
 
    def test_negativo_em_radix_16(self):
        assert JInteger.toUnsignedString(-1, 16) == 'ffffffff'


class TestReverseBytes:
    def test_valor_simples(self):
        assert JInteger.reverseBytes(0x12345678) == 0x78563412

    def test_zero_permanece_zero(self):
        assert JInteger.reverseBytes(0) == 0
    
class TestRotateLeft:
    def test_rotacao_simples(self):
        assert JInteger.rotateLeft(1, 1) == 2
 
    def test_bit_de_sinal_rotaciona_para_lsb(self):
        assert JInteger.rotateLeft(JInteger.MIN_VALUE, 1) == 1
        
    def test_distancia_multipla_de_32_e_noop(self):
        assert JInteger.rotateLeft(42, 32) == 42
