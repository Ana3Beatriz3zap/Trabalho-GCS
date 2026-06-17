"""
Testes Unitários escritos com base no contrato JInteger 
"""

import pytest

from jtypes.jinteger import JInteger


class TestJInteger:
    # --- CONSTANTES ---

    # impl:test
    def test_max_value(self):
        assert JInteger.MAX_VALUE == 2**31 - 1

    # impl:test
    def test_min_value(self):
        assert JInteger.MIN_VALUE == -(2**31)

    # impl:test
    def test_size_em_bits(self):
        assert JInteger.SIZE == 32

    # impl:test
    def test_bytes(self):
        assert JInteger.BYTES == 4

    # --- CONSTRUTOR E CONVERSAO ---

    # impl:test
    def test_construtor_com_int_dentro_do_range(self):
        assert JInteger(42).intValue() == 42

    # impl:test
    def test_construtor_aplica_wraparound_acima_do_max(self):
        assert JInteger(JInteger.MAX_VALUE + 1).intValue() == JInteger.MIN_VALUE

    # impl:test
    def test_construtor_aplica_wraparound_abaixo_do_min(self):
        assert JInteger(JInteger.MIN_VALUE - 1).intValue() == JInteger.MAX_VALUE

    # impl:test
    def test_construtor_com_string_numerica(self):
        assert JInteger("123").intValue() == 123

    # impl:test
    def test_construtor_com_string_invalida_lanca_erro(self):
        with pytest.raises(ValueError):
            JInteger("abc")

    # impl:test
    def test_byte_value_trunca_e_faz_sign_extend(self):
        # 300 em binario ultrapassa 1 byte; deve truncar como (byte) 300 em Java == 44
        assert JInteger(300).byteValue() == 44

    # impl:test
    def test_short_value_trunca_16_bits(self):
        # 70000 truncado para short (16 bits com sinal) == 4464 em Java
        assert JInteger(70000).shortValue() == 4464

    # impl:test
    def test_long_value_preserva_o_valor(self):
        assert JInteger(123).longValue() == 123

    # impl:test
    def test_float_value_e_double_value(self):
        numero = JInteger(10)
        assert numero.floatValue() == 10.0
        assert numero.doubleValue() == 10.0

    # impl:test
    def test_str_representa_valor_decimal(self):
        assert str(JInteger(-7)) == "-7"

    # impl:test
    def test_hash_eh_consistente_para_mesmo_valor(self):
        assert hash(JInteger(5)) == hash(JInteger(5))

    # impl:test
    def test_equals_compara_por_valor(self):
        assert JInteger(5) == JInteger(5)
        assert JInteger(5) != JInteger(6)

    # impl:test
    def test_equals_com_tipo_diferente_retorna_false(self):
        assert (JInteger(5) == "5") is False

    # impl:test
    def test_compare_to_menor_igual_maior(self):
        assert JInteger(1).compareTo(JInteger(2)) < 0
        assert JInteger(2).compareTo(JInteger(2)) == 0
        assert JInteger(3).compareTo(JInteger(2)) > 0

    # --- PARSING ---

    # impl:test
    def test_parse_int_decimal_positivo(self):
        assert JInteger.parseInt("42") == 42

    # impl:test
    def test_parse_int_decimal_negativo(self):
        assert JInteger.parseInt("-17") == -17

    # impl:test
    def test_parse_int_string_invalida_lanca_value_error(self):
        with pytest.raises(ValueError):
            JInteger.parseInt("12a")

    # impl:test
    def test_parse_int_com_radix_binario(self):
        assert JInteger.parseInt("1010", 2) == 10

    # impl:test
    def test_parse_int_com_radix_hexadecimal(self):
        assert JInteger.parseInt("ff", 16) == 255

    # impl:test
    def test_parse_unsigned_int_aceita_valor_acima_do_max_value(self):
        # 4294967295 = 2^32 - 1, maior que JInteger.MAX_VALUE, mas valido como unsigned
        assert JInteger.parseUnsignedInt("4294967295") == -1

    # impl:test
    def test_parse_unsigned_int_com_radix(self):
        assert JInteger.parseUnsignedInt("ffffffff", 16) == -1

    # --- VALUE_OF E DECODE ---

    # impl:test
    def test_value_of_a_partir_de_int(self):
        resultado = JInteger.valueOf(7)
        assert isinstance(resultado, JInteger)
        assert resultado.intValue() == 7

    # impl:test
    def test_value_of_a_partir_de_string(self):
        assert JInteger.valueOf("99").intValue() == 99

    # impl:test
    def test_value_of_a_partir_de_string_com_radix(self):
        assert JInteger.valueOf("101", 2).intValue() == 5

    # impl:test
    def test_decode_string_decimal(self):
        assert JInteger.decode("123").intValue() == 123

    # impl:test
    def test_decode_string_hexadecimal_com_prefixo_0x(self):
        assert JInteger.decode("0x1A").intValue() == 26

    # impl:test
    def test_decode_string_octal_com_prefixo_zero(self):
        assert JInteger.decode("017").intValue() == 15

    # impl:test
    def test_decode_string_negativa_hexadecimal(self):
        assert JInteger.decode("-0x1A").intValue() == -26

    # --- FORMATACAO POR BASE ---

    # impl:test
    def test_to_string_decimal_padrao(self):
        assert JInteger.toString(42) == "42"

    # impl:test
    def test_to_string_negativo_decimal(self):
        assert JInteger.toString(-42) == "-42"

    # impl:test
    def test_to_string_com_radix_binario(self):
        assert JInteger.toString(10, 2) == "1010"

    # impl:test
    def test_to_string_com_radix_hexadecimal(self):
        assert JInteger.toString(255, 16) == "ff"

    # impl:test
    def test_to_binary_string_de_valor_positivo(self):
        assert JInteger.toBinaryString(10) == "1010"

    # impl:test
    def test_to_binary_string_de_valor_negativo_usa_32_bits(self):
        # -1 em complemento de dois de 32 bits = 32 uns
        assert JInteger.toBinaryString(-1) == "1" * 32

    # impl:test
    def test_to_octal_string_de_valor_positivo(self):
        assert JInteger.toOctalString(8) == "10"

    # impl:test
    def test_to_hex_string_de_valor_positivo(self):
        assert JInteger.toHexString(255) == "ff"

    # impl:test
    def test_to_hex_string_de_valor_negativo_usa_32_bits(self):
        assert JInteger.toHexString(-1) == "ffffffff"

    # impl:test
    def test_to_unsigned_string_decimal(self):
        assert JInteger.toUnsignedString(-1) == "4294967295"

    # impl:test
    def test_to_unsigned_string_com_radix(self):
        assert JInteger.toUnsignedString(-1, 16) == "ffffffff"

    # --- OPERACOES BIT A BIT ---

    # impl:test
    def test_bit_count_de_valor_positivo(self):
        assert JInteger.bitCount(7) == 3  # 0b111

    # impl:test
    def test_bit_count_de_zero(self):
        assert JInteger.bitCount(0) == 0

    # impl:test
    def test_highest_one_bit(self):
        assert JInteger.highestOneBit(10) == 8  # 0b1010 -> 0b1000

    # impl:test
    def test_lowest_one_bit(self):
        assert JInteger.lowestOneBit(12) == 4  # 0b1100 -> 0b0100

    # impl:test
    def test_number_of_leading_zeros_de_valor_pequeno(self):
        assert JInteger.numberOfLeadingZeros(1) == 31

    # impl:test
    def test_number_of_trailing_zeros_de_valor_par(self):
        assert JInteger.numberOfTrailingZeros(8) == 3  # 0b1000

    # impl:test
    def test_reverse_inverte_a_ordem_dos_32_bits(self):
        # 1 (...0001) revertido vira o bit mais significativo ligado
        assert JInteger.reverse(1) == JInteger.MIN_VALUE

    # impl:test
    def test_reverse_bytes_inverte_a_ordem_dos_4_bytes(self):
        assert JInteger.reverseBytes(0x12345678) == 0x78563412

    # impl:test
    def test_rotate_left(self):
        assert JInteger.rotateLeft(1, 1) == 2

    # impl:test
    def test_rotate_right(self):
        assert JInteger.rotateRight(2, 1) == 1

    # impl:test
    def test_signum_positivo_negativo_zero(self):
        assert JInteger.signum(10) == 1
        assert JInteger.signum(-10) == -1
        assert JInteger.signum(0) == 0

    # --- ARITMETICA ESTATICA ---

    # impl:test
    def test_sum_simples(self):
        assert JInteger.sum(2, 3) == 5

    # impl:test
    def test_sum_com_overflow_aplica_wraparound(self):
        assert JInteger.sum(JInteger.MAX_VALUE, 1) == JInteger.MIN_VALUE

    # impl:test
    def test_max_retorna_o_maior(self):
        assert JInteger.max(3, 7) == 7

    # impl:test
    def test_min_retorna_o_menor(self):
        assert JInteger.min(3, 7) == 3

    # impl:test
    def test_compare_negativo_zero_positivo(self):
        assert JInteger.compare(1, 2) < 0
        assert JInteger.compare(2, 2) == 0
        assert JInteger.compare(3, 2) > 0

    # impl:test
    def test_compare_unsigned_trata_negativo_como_valor_alto(self):
        # -1 como unsigned (4294967295) e maior que 1
        assert JInteger.compareUnsigned(-1, 1) > 0

    # impl:test
    def test_divide_unsigned_com_operandos_positivos(self):
        assert JInteger.divideUnsigned(10, 3) == 3

    # impl:test
    def test_divide_unsigned_trata_dividendo_negativo_como_unsigned(self):
        # -1 (0xFFFFFFFF = 4294967295) dividido por 2 (unsigned) = 2147483647
        assert JInteger.divideUnsigned(-1, 2) == 2147483647

    # impl:test
    def test_divide_unsigned_por_zero_lanca_erro(self):
        with pytest.raises(ZeroDivisionError):
            JInteger.divideUnsigned(10, 0)

    # impl:test
    def test_remainder_unsigned_com_operandos_positivos(self):
        assert JInteger.remainderUnsigned(10, 3) == 1

    # impl:test
    def test_remainder_unsigned_trata_dividendo_negativo_como_unsigned(self):
        # -1 (4294967295) % 2 (unsigned) = 1
        assert JInteger.remainderUnsigned(-1, 2) == 1