# ADR-012: Sobrecarga de Métodos Simulada via Descritor `_DualMethod`

## Status

Aceito

## Contexto

Java resolve sobrecargas em tempo de compilação por tipo e aridade. Dois métodos
com o mesmo nome coexistem em `java.lang.Integer` simultaneamente como método de
instância e como método estático:

```java
String toString()                        // instância, zero args
static String toString(int i)            // estático, um arg
static String toString(int i, int radix) // estático, dois args

int hashCode()                           // instância, zero args
static int hashCode(int value)           // estático, um arg (Java 8+)
```

Python não tem sobrecarga. O namespace de uma classe é um dicionário: o segundo
método com o mesmo nome sobrescreve o primeiro. Uma tentativa prévia de resolver
isso com `@staticmethod` + parâmetro opcional resultou em `JInteger(42).toString()`
chamando o método estático e recebendo `i=None`, lançando `TypeError` em vez de
retornar `"42"`. Renomear os estáticos para `toStringStatic`/`hashCodeStatic`
violava a fidelidade à API Java e gerou inconsistência documentada.

## Alternativas Consideradas

**Parâmetro sentinela `_MISSING`:** um único método tenta detectar o contexto pelo
tipo do primeiro argumento. Frágil: não é possível distinguir
`JInteger(42).toString()` de `JInteger.toString(42)` sem introspecção de tipo que
contamina a lógica de negócio. Type hints ficam impossíveis de expressar.

**Nomes distintos (`toStringStatic`, `hashCodeStatic`):** simples, sem mecanismo
especial, mas quebra a fidelidade à API Java — já foi tentado e gerou inconsistência.

**`functools.singledispatch`:** despacha por tipo do primeiro argumento, não por
contexto de acesso (instância vs. classe). Não resolve `toString()` com zero
argumentos vs. `toString(int)` com um argumento do mesmo tipo.

**Descritor Python (`__get__`):** controla como o atributo é acessado dependendo
do contexto. Quando `obj is None`, o acesso é via classe → retorna função estática.
Quando `obj` é uma instância, retorna bound method. É o mesmo mecanismo que o
Python usa internamente para `@property`, `@staticmethod` e `@classmethod`.

## Decisão

Implementar o descritor `_DualMethod` no nível de módulo e associá-lo aos dois
métodos afetados:

```python
class _DualMethod:
    def __init__(self, instance_fn, static_fn):
        self._instance_fn = instance_fn
        self._static_fn   = static_fn

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self._static_fn          # acesso via classe → estático
        def bound(*args, **kwargs):
            return self._instance_fn(obj, *args, **kwargs)
        return bound                        # acesso via instância → bound method

# Dentro de JInteger:
toString = _DualMethod(_toString_instance, _toString_static)
hashCode = _DualMethod(_hashCode_instance, _hashCode_static)
```

Demais métodos com aridade variável (ex.: `parseInt(s)` vs `parseInt(s, radix)`)
continuam usando parâmetros opcionais com valores padrão — não há conflito de
contexto pois todos são estáticos.

## Justificativa

O protocolo de descritores é o mecanismo correto do Python para controlar acesso
a atributos e é a base dos próprios decoradores `@property`, `@staticmethod` e
`@classmethod`. Usá-lo aqui é idiomático no nível de metaprogramação, ainda que
incomum em código de aplicação. O resultado do ponto de vista do chamador é API
idêntica à Java:

```python
JInteger(42).toString()       # instância → "42"
JInteger.toString(255, 16)    # estático  → "ff"
JInteger(42).hashCode()       # instância → 42
JInteger.hashCode(42)         # estático  → 42
```

## Consequências

**Positivas:** API idêntica à Java sem nenhum nome alternativo; type hints corretos
em cada função privada; cada variante é testável isoladamente.

**Negativas:** `_toString_instance`, `_toString_static`, `_hashCode_instance` e
`_hashCode_static` aparecem no namespace da classe com prefixo `_`; `help(JInteger.toString)`
exibe a docstring do estático (acesso via classe), não da instância; desenvolvedores
sem familiaridade com descritores precisarão de contexto para entender o mecanismo.

## Revisão

Revisável se outros métodos da API exigirem o mesmo tratamento, caso em que
`_DualMethod` pode ser generalizado ou substituído por solução baseada em metaclasse.
