# ADR-013: Modelo de Contrato, Despacho Dinâmico e Nomenclatura da API Pública

## Status

Aceito

## Contexto

A especificação Java SE 8 impõe restrições estruturais de contrato que conflitam diretamente com o modelo de dados e a sintaxe do Python. Primeiramente, métodos como `isNaN`, `isInfinite`, `toString` e `hashCode` atuam simultaneamente como estáticos e de instância, enquanto o Python sobrescreve definições homônimas dentro de uma classe. Segundo, a classe Java implementa três sobrecargas de construtores distintas (`float`, `double`, `String`), funcionalidade não suportada nativamente em Python. Terceiro, o Java utiliza as exceções controladas `NullPointerException`, `NumberFormatException` e `ClassCastException`, que carecem de correspondência direta na hierarquia nativa do Python. Quarto, a convenção padrão do Java exige o formato `camelCase` para a assinatura pública (`floatToIntBits`), violando o guia de estilo PEP 8 (`snake_case`). Por fim, chamadas estáticas vazias ou malformadas precisam ser interceptadas de forma limpa antes de processarem valores nulos.

## Decisão

Adotaremos uma arquitetura de API unificada baseada em despacho dinâmico por tipo em tempo de execução, mapeamento idiomático e estrita aderência ao contrato nominal do Java:

1. **Nomenclatura:** Todos os identificadores públicos manterão o padrão `camelCase` idêntico ao Java, restringindo o uso de `snake_case` com prefixo `_` exclusivamente para rotinas internas e privadas do módulo.
2. **Métodos de Uso Duplo e Sentinela:** Os métodos serão declarados sem decoradores de escopo. Um objeto sentinela de identidade única e imutável (`_UNSET = object()`) será atribuído como valor padrão ao parâmetro `self_or_v`. Através do protocolo de descritores e checagem de tipo via `isinstance`, o método discriminará dinamicamente se a chamada partiu de uma instância ou de um contexto estático, gerando um erro explícito `TypeError` caso nenhum argumento válido seja fornecido.
3. **Construtor Unificado e Exceções:** Forneceremos um único método `__init__` que intercepta os tipos aceitos (`float`, `int`, `str`, `JFloat`), delegando as operações internas para métodos auxiliares dedicados (como `parseFloat`). Desvios de dados serão tratados mapeando as exceções Java diretamente para as exceções mais próximas e idiomáticas do ecossistema Python: `NullPointerException` e `NumberFormatException` serão unificadas e lançadas como `ValueError`, enquanto `ClassCastException` será convertida em um `TypeError` padrão.

```python
_UNSET = object()

class JFloat:
    def __init__(self, value):
        if isinstance(value, JFloat):         self._value = value._value
        elif isinstance(value, str):          self._value = JFloat.parseFloat(value)
        elif isinstance(value, (int, float)): self._value = _to_float32(float(value))
        else: raise TypeError("Tipo inválido no construtor")

    def isNaN(self_or_v=_UNSET):
        if self_or_v is _UNSET:
            raise TypeError("isNaN() requer uma instância de JFloat ou um argumento numérico")
        if isinstance(self_or_v, JFloat):
            return math.isnan(self_or_v._value)
        return math.isnan(_to_float32(float(self_or_v)))
```

## Consequências

- **Positivo:** A superfície da API pública torna-se um espelho 100% idêntico à especificação oficial do Java SE 8, permitindo o porte mecânico e direto de códigos fonte e testes unitários. A integração com estruturas de controle do Python (`except ValueError`) flui de forma nativa e sem a necessidade de injeção de classes proprietárias ou metaprogramação complexa.
- **Negativo:** Ocorre uma quebra deliberada das diretrizes de estilo da PEP 8, forçando o uso de supressões locais (`# type: ignore[override]`) em linters e ferramentas de análise estática como o `mypy`, visto que as assinaturas dinâmicas obscurecem o uso convencional de type hints. A unificação de erros sob `ValueError` remove a distinção precisa entre ponteiros nulos e falhas de parsing de strings, exigindo uma documentação interna rigorosa nos testes da aplicação.
