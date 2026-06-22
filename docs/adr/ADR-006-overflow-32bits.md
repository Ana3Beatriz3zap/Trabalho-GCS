# ADR-002: Simulação de Overflow de Inteiro de 32 Bits

## Status

Aceito

## Contexto

Java armazena `int` em exatamente 32 bits com sinal (complemento de dois) e o
overflow é silencioso e definido pela especificação:

```java
Integer.MAX_VALUE + 1 == Integer.MIN_VALUE  // true
Integer.sum(Integer.MAX_VALUE, 1)           // -2147483648
```

Python usa inteiros de precisão arbitrária — `2**31 - 1 + 1` retorna `2147483648`,
não `-2147483648`. Sem intervenção explícita, qualquer operação aritmética ou
bit a bit em `JInteger` pode produzir valores fora do intervalo de 32 bits.

Isso afeta diretamente: `sum`, `max`, `min`, `rotateLeft`, `rotateRight`, `reverse`,
`reverseBytes`, `highestOneBit`, `lowestOneBit`, e o próprio construtor.

## Alternativas Consideradas

**`ctypes.c_int32`:** truncamento automático, mas requer wrapping/unwrapping
constante e introduz dependência para algo solucionável com aritmética pura.

**`numpy.int32`:** overflow automático e próximo do Java, mas introduz dependência
pesada, e `numpy.int32` não é `int` Python — quebra `isinstance` e polui a
interface pública.

**Máscara de bits + ajuste de complemento de dois:** `valor & 0xFFFF_FFFF` trunca
para 32 bits sem sinal; se o resultado ≥ `0x8000_0000`, subtrai `0x1_0000_0000`
para ajustar o sinal. Zero dependências, retorna `int` Python puro, lógica visível
e auditável.

## Decisão

Implementar duas funções auxiliares no nível de módulo, chamadas explicitamente em
todo ponto de retorno onde overflow é possível:

```python
_MASK32 = 0xFFFF_FFFF

def _to_int32(value: int) -> int:
    """Trunca para inteiro com sinal de 32 bits (complemento de dois)."""
    value &= _MASK32
    if value >= 0x8000_0000:
        value -= 0x1_0000_0000
    return value

def _to_uint32(value: int) -> int:
    """Interpreta value como inteiro sem sinal de 32 bits."""
    return value & _MASK32
```

`_to_int32` é aplicado em toda operação cujo resultado deve ser um `int` Java de
32 bits com sinal. `_to_uint32` é aplicado em métodos que interpretam o valor como
_unsigned_ antes de operar (ex: `toBinaryString`, `divideUnsigned`, operações bit
a bit).

**Isso inclui `sum`, `max` e `min`**, que herdam o comportamento de overflow
silencioso do Java — não lançam exceção nem saturam:

```python
@staticmethod
def sum(a: int, b: int) -> int:
    return _to_int32(a + b)           # MAX_VALUE + 1 → MIN_VALUE

@staticmethod
def max(a: int, b: int) -> int:
    return a if _to_int32(a) >= _to_int32(b) else b

@staticmethod
def min(a: int, b: int) -> int:
    return a if _to_int32(a) <= _to_int32(b) else b
```

`max` e `min` truncam os operandos para comparação mas retornam o argumento
original, consistente com Java onde o argumento já chega como `int` de 32 bits.

O overflow silencioso em `sum`/`max`/`min` é **comportamento especificado** (JLS
§15.18.2), não um bug. `Math.addExact` é o método Java que lança exceção em
overflow — `Integer.sum` deliberadamente não o faz.

## Justificativa

A abordagem com máscara é a mais transparente, sem dependências, e retorna `int`
Python puro em todos os casos. O custo de chamar as funções explicitamente é
aceitável e torna o comportamento auditável — qualquer revisor pode localizar
exatamente onde o truncamento ocorre. A aplicação consistente em `sum`/`max`/`min`
mantém o contrato de overflow uniforme em toda a classe.

## Consequências

**Positivas:** nenhuma dependência externa; `int` Python em todos os retornos;
lógica de complemento de dois explícita e testável; overflow idêntico ao Java em
toda a classe, incluindo `sum(MAX_VALUE, 1) == MIN_VALUE`.

**Negativas:** disciplina necessária — todo novo método deve chamar `_to_int32` ou
`_to_uint32` no retorno; a ausência não falha ruidosamente, apenas retorna valor
fora do intervalo de 32 bits. O overflow silencioso em `sum` pode surpreender
desenvolvedores Python que esperem soma matemática pura.

## Revisão

Revisável se o projeto adotar `numpy` por outros motivos — nesse caso `numpy.int32`
pode substituir `_to_int32` com overflow automático. A decisão sobre `sum`/`max`/`min`
é derivada diretamente desta e será revisada em conjunto.
