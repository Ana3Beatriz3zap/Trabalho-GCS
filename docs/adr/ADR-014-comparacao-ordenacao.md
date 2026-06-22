# ADR-014: Comparação, Ordenação e Tratamento de Sinais de Bits em PyFloat

## Status

Aceito

## Contexto

No Python, a comparação de ponto flutuante possui regras estritas tanto para a representação binária exata em memória quanto para a ordenação de valores limites. Para operações de hash ou identidades estritas, é essencial distinguir comportamentos específicos de representação binária (onde `0.0` e `-0.0` possuem mapeamentos distintos). Além disso, funções como `max(0.0, -0.0)` e `min()` no Python tratam ambos os valores como logicamente equivalentes, mas preservam a ordem do primeiro argumento fornecido em caso de empate. No Java nativo, o operador `==` considera `0.0 == -0.0`, enquanto métodos utilitários como `Math.max(0.0, -0.0)` ou `Double.compare()` aplicam rigidamente a norma IEEE 754 de forma que `0.0` é estritamente maior que `-0.0`, violando o comportamento de preservação de ordem do interpretador CPython.

## Decisão

Combinaremos a extração direta de bits com uma lógica de fluxo de controle customizada para as operações de ordenação e igualdade. Utilizaremos `Double.doubleToRawLongBits()` associado a operações bit a bit (como XOR) para implementar comparações de identidade binária e geração de `__hash__()`. Para os métodos de extremos como `__max__` e `__min__`, rejeitaremos o uso direto do `Math.max` do Java. Em vez disso, implementaremos uma verificação manual baseada em condicionais: quando houver equivalência lógica de valor (como o cenário de `0.0` e `-0.0`), o método retornará exatamente a referência ou valor do primeiro operando avaliado, replicando fielmente o comportamento nativo do Python.

## Consequências

- **Positivo:** Garantimos compatibilidade bit a bit com o CPython para verificação de identidade e tabelas de espalhamento, além de total aderência aos casos de borda (_edge cases_) na ordenação de zeros sinalizados.
- **Negativo:** O código em Java torna-se mais verboso, e a impossibilidade de delegar diretamente para as rotinas altamente otimizadas da JVM (`Math.max`) introduz um leve custo computacional devido às checagens manuais por fluxo de controle.
