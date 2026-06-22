# ADR-008: Mapeamento de Exceções e Integer Cache em `valueOf`

## Status

Aceito

## Contexto

Dois aspectos do contrato público de `java.lang.Integer` exigem decisões de
mapeamento para Python sem equivalente direto na linguagem:

**1. `NumberFormatException`:** Java lança esta exceção em todos os métodos de
parsing quando a entrada é inválida. Ela estende `IllegalArgumentException →
RuntimeException`. Python não possui hierarquia equivalente — a exceção mais
próxima semanticamente para "falha ao converter string em número" é `ValueError`,
que é o que `int("abc")` lança nativamente.

**2. Integer cache em `valueOf`:** O JLS §5.1.7 garante que `Integer.valueOf(i)`
retorna o **mesmo objeto** para valores em `[-128, 127]`:

```java
Integer a = Integer.valueOf(100);
Integer b = Integer.valueOf(100);
a == b;  // true — mesmo objeto garantido pela spec

Integer c = Integer.valueOf(200);
Integer d = Integer.valueOf(200);
c == d;  // false — objetos distintos fora do cache
```

Em Python, `is` corresponde à verificação de identidade de objeto. Código que
depende dessa garantia — incluindo testes — precisa que `JInteger.valueOf` replique
esse comportamento.

## Alternativas Consideradas

### NumberFormatException

**`ValueError` diretamente:** idiomático, mas perde o nome da exceção no traceback
e impossibilita captura específica sem capturar todos os `ValueError` do programa.

**`NumberFormatException(Exception)`:** nome preservado e captura específica
possível, mas código Python que captura `ValueError` (padrão para erros de
conversão) não a capturaria — quebra integração com código existente.

**`NumberFormatException(ValueError)`:** nome Java no traceback, captura específica
possível com `except NumberFormatException`, captura genérica também funciona com
`except ValueError`. Hierarquia semanticamente correta: erros de formato são
especialização de erros de valor.

### Integer Cache

**Sem cache:** mais simples, sem estado global, mas viola a garantia de identidade
da spec e quebra testes que verificam `a is b`.

**Cache pré-populado na inicialização do módulo:** sem race condition, mas custo de
256 alocações mesmo que `valueOf` nunca seja chamado.

**Cache com `dict` lazy no nível de módulo:** objetos criados sob demanda com
`object.__new__` (evita re-execução de `__init__`); fiel ao comportamento do
OpenJDK; testável.

## Decisão

**Exceções:** definir `NumberFormatException` como subclasse de `ValueError`,
declarada no nível de módulo e exportada como parte da API pública. Todo método
de parsing a lança exclusivamente — nenhum método lança `ValueError` diretamente.

```python
class NumberFormatException(ValueError):
    """Equivalente Python de java.lang.NumberFormatException."""
```

**Cache:** implementar com `dict` `_cache` no nível de módulo, lazy, usando
`object.__new__` para inserção:

```python
_cache: dict[int, JInteger] = {}

# Em valueOf:
if -128 <= parsed <= 127:
    if parsed not in _cache:
        obj = object.__new__(JInteger)
        obj._value = parsed
        _cache[parsed] = obj
    return _cache[parsed]
```

A implementação não inclui sincronização de threads — mesma omissão das
implementações de referência para contextos single-thread.

## Justificativa

`NumberFormatException(ValueError)` satisfaz simultaneamente o contrato Java (nome
preservado) e o Python (compatibilidade com `except ValueError`). É a solução de
maior compatibilidade sem custo adicional.

O cache é garantia do contrato público, não detalhe de implementação opcional.
Omiti-lo tornaria a biblioteca incompatível com código Java que depende de
identidade de objetos no intervalo `[-128, 127]`.

## Consequências

**Positivas:** tracebacks exibem `NumberFormatException`; `except ValueError` captura
a exceção; `except NumberFormatException` permite tratamento específico; `valueOf(x)
is valueOf(x)` garantido para `x in [-128, 127]`; alocações reduzidas para valores
mais comuns.

**Negativas:** a hierarquia Java completa (`NFE → IllegalArgumentException →
RuntimeException`) não é replicada. O cache usa estado global mutável — em
ambientes multithread há janela de race condition entre verificação e inserção
(sem lock), mas a garantia de identidade não é requisito em contextos concorrentes
pela própria spec Java. Testes que assumem isolamento de estado podem precisar
limpar `_cache` no `teardown`.

## Revisão

A decisão de exceções será revisada se o projeto introduzir uma hierarquia completa
de exceções Java mapeadas para Python. O cache será revisado para adicionar
`threading.Lock` se o projeto for usado em contextos multithread onde a garantia
de identidade seja crítica.

@Amanda
