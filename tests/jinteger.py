"""
Suíte de testes para os métodos de conversão numérica de JInteger:
    - byteValue()
    - shortValue()
    - intValue()
    - longValue()
    - floatValue()
"""
class TestByteValue:
    def test_dentro_do_intervalo_signed_byte(self):
        assert JInteger(100).byteValue() == 100
 
    def test_zero(self):
        assert JInteger(0).byteValue() == 0
 
    def test_127_permanece_127(self):
        assert JInteger(127).byteValue() == 127