# ADR-016: Gerenciamento de Memória, Ciclo de Vida e Abordagem de Objetos para PyFloat

## Status

Aceito

## Contexto

O tipo `float` do Python mapeia-se internamente para o tipo primitivo `double` da linguagem C (64 bits, IEEE 754), mas opera sob a semântica de um objeto imutável gerenciado por contagem de referências (_Reference Counting_), sendo destruído imediatamente ao sair de escopo. No ambiente da JVM, implementar a classe `PyFloat` exige a criação de uma estrutura de objeto completa. Isso impõe duas grandes limitações: o aumento drástico do consumo de memória (_footprint_) devido aos cabeçalhos de objeto da JVM (Object Headers) e uma severa pressão sobre o Garbage Collector (como G1 ou ZGC), causada pela criação em massa de instâncias de `PyFloat` temporárias em operações aritméticas encadeadas (ex: `a + b + c + d`).

## Decisão

Implementaremos a classe `PyFloat` como uma estrutura estritamente imutável que encapsula um primitivo `double` do Java (`private final double value;`). Para mitigar o impacto de alocação de memória e aliviar o Garbage Collector, adotaremos o padrão de projeto _Flyweight_ por meio de um cache interno estático para valores altamente recorrentes (como `0.0`, `1.0`, `-1.0`), semelhante ao mecanismo de pequenos inteiros/floats do CPython. Além disso, em trechos de código que realizem processamentos matemáticos intensivos em lote, a lógica deverá extrair os valores primitivos, executar as computações de forma pura na pilha (_Stack_) e envelopar o resultado em um objeto `PyFloat` apenas na entrega final do dado.

## Consequências

- **Positivo:** Preservamos fielmente a semântica de imutabilidade e o modelo de dados unificado do Python, reduzindo o desperdício de memória em aplicações típicas que reutilizam valores numéricos neutros e unitários.
- **Negativo:** Operações de computação numérica massiva (_number crunching_) sofrerão uma degradação inevitável de desempenho e maior consumo de memória se comparadas ao uso de arrays primitivos nativos do Java (`double[]`), decorrente da alocação de instâncias não-viciadas na Eden Space.
