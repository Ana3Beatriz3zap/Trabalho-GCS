# ADR-005: Conversões Numéricas com Perda — `byteValue`, `shortValue` e `floatValue`

## Status

Aceito

## Contexto

`java.lang.Integer` herda de `java.lang.Number` três métodos de conversão que
envolvem **perda de informação**:

**`byteValue()` e `shortValue()` — narrowing conversion (JLS §5.1.3):**
Descartam bits mais significativos e reinterpretam o resultado com sinal em
complemento de dois:

```java
(byte) 128    // → -128   (8 bits: trunca, reinterpreta com sinal)
(byte) 256    // → 0
(short) 32768 // → -32768
```

**`floatValue()` — widening com perda de precisão (JLS §5.1.2):**
Converte `int` para `float` IEEE 754 de 32 bits (single-precision). Valores acima
de 2²⁴ perdem precisão inteira:

```java
(float) 16777217  // → 1.6777216E7  (arredondado para float32 mais próximo)
```

Python não possui tipos de largura fixa nativos: `int` é de precisão arbitrária e
`float` é sempre 64 bits (double). Nenhuma das três conversões ocorre automaticamente.

## Alternativas Consideradas

### byteValue e shortValue

**`ctypes.c_int8` / `ctypes.c_int16`:** truncamento automático correto, mas
introduz dependência para operação solucionável com aritmética pura.

**`struct.pack/unpack`:** correto e explícito sobre o tipo, mas mais verboso do que
aritmética direta e requer pré-processamento antes do pack.

**Aritmética direta com máscara e ajuste de sinal:**
```python
def byteValue(self) -> int:
    v = self._value & 0xFF
    return v - 256 if v >= 128 else v
```
Zero dependências, explícito, testável, e consistente com `_to_int32` (ADR-002).

### floatValue

**`float(self._value)` diretamente:** simples, mas retorna double-precision — para
valores > 2²⁴, diverge do Java:
```python
float(16777217)  # → 16777217.0  (errado: Java retorna 16777216.0)
```

**`numpy.float32`:** genuinamente 32 bits, mas introduz dependência pesada para
um único método, e `numpy.float32` não é `float` Python — quebra `isinstance`.

**`ctypes.c_float(...).value`:** correto, mas dependência de `ctypes` para algo
solucionável com `struct` da biblioteca padrão.

**`struct.pack('f', ...) / unpack('f', ...)`:** serializa como IEEE 754 single
(formato `'f'`, 4 bytes), aplicando o arredondamento correto; desserializa de volta
para `float` Python (64 bits). Sem dependências extras, retorna `float` puro,
intenção explícita pelo formato `'f'`.

## Decisão

**`byteValue` e `shortValue`:** aritmética direta com máscara e ajuste de sinal,
seguindo o padrão de `_to_int32` (ADR-002):

```python
def byteValue(self) -> int:
    v = self._value & 0xFF
    return v - 256 if v >= 128 else v

def shortValue(self) -> int:
    v = self._value & 0xFFFF
    return v - 65536 if v >= 32768 else v
```

O padrão geral para N bits com sinal: truncar com `& ((1 << N) - 1)`, depois
subtrair `1 << N` se o resultado ≥ `1 << (N - 1)`.

**`floatValue`:** `struct.pack/unpack` com formato `'f'`:

```python
def floatValue(self) -> float:
    return struct.unpack('f', struct.pack('f', float(self._value)))[0]
```

O retorno é `float` Python (64 bits) com valor arredondado para single-precision,
não um `float32` genuíno — documentado como compatibilidade parcial no README.

## Justificativa

As três soluções escolhidas compartilham o mesmo critério: zero dependências extras
além da biblioteca padrão, retorno em tipos Python nativos (`int` ou `float`), e
lógica de conversão explícita e auditável. A consistência com `_to_int32` em
`byteValue`/`shortValue` torna o padrão de truncamento reconhecível em todo o módulo.

## Consequências

**Positivas:** comportamento de narrowing idêntico ao Java para todos os casos de
borda; `floatValue(16777217)` retorna `16777216.0`, idêntico ao Java; retornos em
`int` e `float` Python puros sem tipos exóticos na interface.

**Negativas:** `floatValue` retorna `float` de 64 bits com precisão de 32 bits —
a distinção é invisível ao chamador; operações subsequentes em double podem acumular
diferenças em relação a código Java que mantém o valor em `float32` durante todo o
cálculo. Se a estratégia global de tipos de largura fixa mudar (ver ADR-002),
`byteValue` e `shortValue` precisarão de atualização manual.

## Revisão

Revisável em conjunto com ADR-002 se a estratégia de simulação de tipos fixos for
alterada globalmente, ou se `numpy` for adotado por outros motivos (tornando
`numpy.float32` disponível sem custo de dependência adicional).

@Amanda
