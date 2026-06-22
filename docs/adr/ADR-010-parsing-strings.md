# ADR-008: Parsing de Strings — Prefixos de Base em `decode` e Tratamento de Radix

## Status

Aceito

## Contexto

Dois aspectos do parsing de strings em `java.lang.Integer` exigem decisões
explícitas sobre como lidar com a entrada:

**1. Prefixos de base em `decode`**

`Integer.decode(String nm)` aceita três bases com notações distintas:

```text
Decimal      → sem prefixo           "42", "-42", "+42"
Hexadecimal  → prefixo "0x" ou "0X"  "0x1F", "0X1F"
Hexadecimal  → prefixo "#"           "#1F"
Octal        → prefixo "0"           "017"
```

O sinal (`+` ou `-`) precede o prefixo de base. A string `"0"` isolada é zero
decimal, não prefixo octal. Python possui `int(s, 0)` que detecta base
automaticamente, mas não reconhece o prefixo `#` e aceita `0o`/`0b` (Python 3)
que Java rejeita com `NumberFormatException`.

**2. Comportamento de radix inválido**

A especificação define comportamentos **assimétricos** dependendo do grupo de método:

```java
// Formatação — radix inválido → fallback silencioso para 10
Integer.toString(255, 1)   // → "255"  (não lança exceção)
Integer.toString(255, 37)  // → "255"

// Parsing — radix inválido → NumberFormatException
Integer.parseInt("10", 1)   // lança NumberFormatException
Integer.parseInt("10", 37)  // lança NumberFormatException
```

> _"If the radix is smaller than Character.MIN_RADIX or larger than
> Character.MAX_RADIX, then the radix 10 is used instead."_ — Javadoc de `toString`
>
> _"Throws NumberFormatException if the radix is either smaller than
> Character.MIN_RADIX or larger than Character.MAX_RADIX."_ — Javadoc de `parseInt`

Um único validador de radix não serve para os dois grupos.

## Alternativas Consideradas

### decode — uso de `int(s, 0)`

`int("0x1F", 0)` e `int("017", 0)` funcionam, mas `int("#1F", 0)` lança
`ValueError`. Pré-processar `#` para `0x` antes de chamar `int(s, 0)` é possível,
mas a partir desse ponto o controle sobre o parsing já foi assumido manualmente —
e o custo de implementar o parser completo torna-se marginal. Além disso, `int(s, 0)`
aceita `"0o17"` e `"0b101"` (Python 3) que Java rejeita, o que introduz divergência
silenciosa.

### radix — validador único (sempre estrito ou sempre silencioso)

**Sempre estrito:** `toString(255, 1)` lançaria exceção onde Java retorna `"255"` —
viola a spec de formatação.

**Sempre silencioso:** `parseInt("10", 37)` retornaria `10` onde Java lança exceção
— encobre erros de programação que deveriam ser detectados.

## Decisão

**`decode` — parser manual sequencial:**

```python
@staticmethod
def decode(nm):
    # 1. Verificar None ou vazio → NumberFormatException
    # 2. Detectar sinal ('-' ou '+')
    # 3. Detectar prefixo:
    #    - "0x" / "0X" → radix 16, avança 2
    #    - "#"          → radix 16, avança 1
    #    - "0" + dígito → radix 8,  avança 1
    #    - caso contrário → radix 10
    # 4. Extrair dígitos; vazio → NumberFormatException
    # 5. int(dígitos, radix) — ValueError capturado como NumberFormatException
    # 6. Aplicar sinal e verificar intervalo [-2³¹, 2³¹-1]
    # 7. Retornar JInteger.valueOf(value)
```

A condição de octal usa `len(s) > idx + 1` para garantir que `"0"` isolado seja
decimal zero, não prefixo octal sem dígitos.

**Radix — dois validadores separados:**

```python
_MIN_RADIX = 2
_MAX_RADIX = 36

def _check_radix_silent(radix: int) -> int:
    """Formatação: retorna radix ou 10 se inválido."""
    return radix if _MIN_RADIX <= radix <= _MAX_RADIX else 10

def _check_radix_strict(radix: int) -> None:
    """Parsing: lança NumberFormatException se radix inválido."""
    if not (_MIN_RADIX <= radix <= _MAX_RADIX):
        raise NumberFormatException(
            f"radix {radix} fora do intervalo [{_MIN_RADIX}, {_MAX_RADIX}]"
        )
```

Regra de aplicação:

| Método                          | Validador             |
| ------------------------------- | --------------------- |
| `toString(int, int)`            | `_check_radix_silent` |
| `toUnsignedString(int, int)`    | `_check_radix_silent` |
| `parseInt(String, int)`         | `_check_radix_strict` |
| `parseUnsignedInt(String, int)` | `_check_radix_strict` |

## Justificativa

O parser manual em `decode` é necessário pelo prefixo `#` e pela rejeição de
`0o`/`0b`. Uma vez que pré-processamento de qualquer natureza é obrigatório,
implementar o parser completo produz código mais claro, testável e fiel à spec do
que encadear `int(s, 0)` com tratamentos especiais.

A assimetria de radix existe na especificação e deve ser replicada: formatação
degrada graciosamente (radix inválido → usa decimal), parsing falha explicitamente
(radix inválido → o chamador precisa saber que a string foi rejeitada). Dois
validadores com nomes descritivos tornam essa escolha explícita e auditável em
cada ponto de uso.

## Consequências

**Positivas:** `decode("#1F")` funciona; `decode("0o17")` lança `NumberFormatException`
(prefixo Python não suportado); `decode("0")` retorna zero decimal; `toString(255, 1)`
retorna `"255"`; `parseInt("10", 37)` lança `NumberFormatException`. Cada caso de
borda é testável isoladamente.

**Negativas:** dois validadores com nomes similares (`_check_radix_silent` vs
`_check_radix_strict`) exigem atenção ao implementar novos métodos que aceitem
radix — usar o validador errado produz comportamento silenciosamente divergente
da spec.

## Revisão

A decisão do parser manual será revisada se Python introduzir suporte nativo ao
prefixo `#` em `int(s, 0)`. A decisão dos dois validadores é derivada diretamente
da spec Java e só será revisada se a spec mudar.
