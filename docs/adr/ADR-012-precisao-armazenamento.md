# ADR-012: Estratégia de Precisão de Dados e Inicialização de Constantes Binárias em JFloat

## Status

Aceito

## Contexto

O tipo `float` na linguagem Java segue rigidamente a especificação IEEE 754 de **32 bits** (precisão simples), enquanto o tipo `float` do Python nativo é mapeado para a especificação de **64 bits** (precisão dupla). Sem um mecanismo explícito de coerção e truncamento, qualquer operação simulada ou valor armazenado reteria a precisão de 64 bits, quebrando o contrato e gerando resultados numéricos divergentes do comportamento da JVM (onde a operação `1.1f + 2.2f` resulta em um valor binário diferente de `1.1 + 2.2` no interpretador Python). Adicionalmente, constantes públicas críticas estabelecidas pela especificação Java SE 8, como `MAX_VALUE` (`3.4028235e38`), `MIN_VALUE` (`1.4e-45`) e `MIN_NORMAL` (`1.17549435e-38`), não possuem representações literais decimais exatas em Python de 64 bits, gerando desvios e potenciais erros de arredondamento se definidas puramente por aproximação textual decimal.

## Decisão

Unificaremos o controle de precisão e a inicialização de constantes por meio da manipulação direta de pacotes de bytes da biblioteca padrão `struct`. Toda entrada numérica recebida no construtor ou por meio de métodos estáticos passará obrigatoriamente por um ciclo de _round-trip_ de conversão binária utilizando a formatação de precisão simples em Big-Endian (`'>f'`), delegando ao hardware o arredondamento IEEE 754 correto:

```python
def _to_float32(value: float) -> float:
    return struct.unpack('>f', struct.pack('>f', value))[0]
```

Para garantir a exatidão absoluta exigida pelo contrato Java, as constantes de classe não serão definidas por literais decimais. Elas serão derivadas e inicializadas diretamente a partir de seus padrões de bits hexadecimais nativos de 32 bits fornecidos pela especificação da JAVADOC, convertidos pelo mesmo motor binário:

```python
MAX_VALUE  = _bits_to_float32(0x7F7F_FFFF)
MIN_VALUE  = _bits_to_float32(0x0000_0001)
MIN_NORMAL = _bits_to_float32(0x0080_0000)
```

## Consequências

- **Positivo:** Precisão de 32 bits (float32) garantida em toda a superfície pública da biblioteca, eliminando quaisquer discrepâncias de cálculo com o Java nativo. A verificação bit a bit das constantes (`JFloat.floatToIntBits(JFloat.MAX_VALUE) == 0x7F7FFFFF`) torna-se deterministicamente correta e portável, sem dependências externas.
- **Negativo:** Introdução de um leve _overhead_ computacional decorrente dos múltiplos ciclos de `pack`/`unpack` em loops numéricos de alta frequência. Além disso, o Python colapsa múltiplos padrões de bits NaN após o empacotamento para um padrão único (`0x7fc00000`), e a legibilidade visual das constantes em hexadecimal exige documentação complementar via comentários para melhor compreensão humana.
