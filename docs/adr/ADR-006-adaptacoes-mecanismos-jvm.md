# ADR-006: Adaptações por Limitações de Mecanismos JVM — `TYPE` e `getInteger`

## Status

Aceito

## Contexto

Dois membros da API `java.lang.Integer` dependem de mecanismos internos da JVM que
não possuem equivalente direto em Python:

**`Integer.TYPE`** depende do sistema de reflexão Java, que distingue o tipo
primitivo `int` do tipo wrapper `Integer`:

```java
Integer.TYPE  // Class<Integer> para o primitivo int
              // distinto de Integer.class (o wrapper)
```

Essa distinção é usada em reflexão para verificar se um parâmetro de método é do
tipo primitivo `int` ou do tipo objeto `Integer`:

```java
method.getParameterTypes()[0] == Integer.TYPE   // true para (int x)
method.getParameterTypes()[0] == Integer.class  // true para (Integer x)
```

Python não possui tipos primitivos. Tudo é objeto. Não existe distinção entre
tipo primitivo e wrapper, nem um objeto `Class` com identidade separável por
contexto.

**`getInteger(String nm)`** lê propriedades do sistema via `System.getProperty`,
subsistema próprio da JVM configurável pela flag `-D` na linha de comando:

```bash
java -Dporta.http=8080 MinhaClasse
```

```java
Integer.getInteger("porta.http")        // → 8080
Integer.getInteger("inexistente", 42)   // → 42 (fallback)
```

Python não possui `System.getProperty`. Os mecanismos disponíveis para configuração
de processo são `os.environ`, `sys.argv`, arquivos de configuração, ou módulos
específicos como `configparser`.

## Alternativas Consideradas

### `Integer.TYPE`

**Omitir a constante:** `JInteger.TYPE` lançaria `AttributeError`. Viola o princípio
de expor toda a superfície pública.

**`TYPE = None`:** evita `AttributeError`, mas `None` não é utilizável para
verificação de tipo e não comunica nenhuma informação semântica.

**`TYPE = int`:** o tipo Python `int` é o análogo semântico mais próximo ao tipo
primitivo Java `int`. `isinstance(42, JInteger.TYPE)` funciona; `JInteger.TYPE is int`
é proposição significativa; compatível com type hints e `isinstance`.

**`TYPE = "int"` (string):** comunicativo mas inutilizável programaticamente.

### `getInteger`

**Não implementar:** `JInteger.getInteger` lançaria `AttributeError`. Viola o
princípio de expor toda a superfície pública.

**Dicionário configurável `JInteger._properties`:** controlável, sem dependência
do ambiente, mas requer população manual — nenhum mecanismo externo alimenta o
dicionário automaticamente. Mais distante do comportamento Java.

**`os.environ`:** variáveis de ambiente são configuradas fora do processo e lidas
em runtime — análogo semântico mais próximo de `System.getProperty`. Comportamento
de fallback, decode e tratamento de erro permanecem fiéis à spec. Testável com
`monkeypatch.setenv` no pytest.

**`sys.argv` parseado:** mais próximo de flags de linha de comando, mas colide com
o uso normal de `sys.argv` pela aplicação hospedeira e requer parsing manual.

## Decisão

**`TYPE`:** definir como o tipo Python `int`:

```python
TYPE: type = int
```

A impossibilidade de replicar a semântica de reflexão Java é documentada no README
e no docstring do módulo. A constante é declarada junto às demais (`MAX_VALUE`,
`MIN_VALUE`, `SIZE`, `BYTES`).

**`getInteger`:** implementar lendo `os.environ.get(nm)`, com comportamento de
fallback e decode fiéis à especificação:

```python
@staticmethod
def getInteger(nm, val=None):
    if nm is None or len(nm) == 0:
        return JInteger.valueOf(val) if isinstance(val, int) else val
    raw = os.environ.get(nm)
    if raw is None:
        return JInteger.valueOf(val) if isinstance(val, int) else val
    try:
        return JInteger.decode(raw)
    except NumberFormatException:
        return JInteger.valueOf(val) if isinstance(val, int) else val
```

A diferença de fonte de dados (`os.environ` vs `System.getProperty`) é documentada
no README na seção de incompatibilidades.

## Justificativa

Em ambos os casos, a estratégia é escolher o análogo semântico mais próximo
disponível em Python, documentar a diferença com clareza, e não inventar mecanismos
que simulem a JVM de forma opaca.

`int` para `TYPE` e `os.environ` para `getInteger` são as alternativas que preservam
o maior valor prático para o chamador: `JInteger.TYPE` é utilizável em `isinstance`
e type hints; `getInteger` é testável e permite migração de código Java que usa
`-D` substituindo por variáveis de ambiente.

## Consequências

**Positivas:** `JInteger.TYPE` retorna valor utilizável; `isinstance(42, JInteger.TYPE)`
funciona; `getInteger` é implementado e testável via `monkeypatch.setenv`; comportamento
de fallback e decode idênticos ao Java.

**Negativas:** `JInteger.TYPE is int` e `JInteger is int` são igualmente `False` —
a distinção primitivo/wrapper de Java não existe em Python; código que usa `TYPE`
para reflexão Java genuína não tem caminho de migração direto. Propriedades Java com
ponto no nome (`porta.http`) precisam ser definidas como variáveis de ambiente com
o mesmo nome — válido em Unix, mas incomum. `System.setProperty` não tem equivalente
direto — `os.environ` pode ser modificado em Python, mas altera o ambiente do
processo inteiro.

## Revisão

`TYPE` será revisado se o projeto introduzir type tokens ou metaclasses que
permitam distinguir `JInteger` (wrapper) de `int` (primitivo) de forma programática.
`getInteger` será revisado para suportar fonte de dados configurável
(`JInteger.set_properties_source(callable)`) se o projeto precisar integrar com
sistemas de configuração distintos de `os.environ`.
