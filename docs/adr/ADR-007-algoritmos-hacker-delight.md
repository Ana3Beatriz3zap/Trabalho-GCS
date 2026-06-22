# ADR-007: Algoritmos Bit a Bit Baseados em Hacker's Delight

## Status

Aceito

## Contexto

`java.lang.Integer` expõe dez métodos que operam sobre a representação binária de
32 bits: `bitCount`, `highestOneBit`, `lowestOneBit`, `numberOfLeadingZeros`,
`numberOfTrailingZeros`, `reverse`, `reverseBytes`, `rotateLeft`, `rotateRight` e
`signum`.

O OpenJDK implementa esses métodos com algoritmos O(1) descritos no livro
_Hacker's Delight_ (Henry S. Warren Jr., 2ª ed., Addison-Wesley, 2012) — operações
paralelas sobre palavras de largura fixa sem laços ou com número constante de passos.

Python suporta todas as operações bit a bit necessárias (`&`, `|`, `^`, `~`, `<<`,
`>>`), mas opera sobre inteiros de precisão arbitrária. Isso cria três diferenças
críticas em relação ao Java:

1. `~x` retorna `-(x+1)`, não o complemento de N bits.
2. `x >> n` faz extensão de sinal para negativos (shift aritmético sobre precisão
   arbitrária).
3. Resultados intermediários podem exceder 32 bits — masks explícitas são necessárias.

A questão central é como implementar esses algoritmos mantendo fidelidade ao
comportamento de 32 bits e rastreabilidade ao OpenJDK.

## Alternativas Consideradas

**Laços Python simples:** até 32 iterações por chamada, O(N). Funciona, mas diverge
do comportamento do OpenJDK e ignora a intenção original dos métodos como operações
O(1) — muitas CPUs possuem instruções dedicadas (`POPCNT`, `BSR`, `BSF`, `LZCNT`).

**Conversões para string (`bin(x).count('1')`, `len(bin(n))`):** conciso e legível
para Python, mas depende de alocação de objeto intermediário por chamada, não é O(1)
puro, e semanticamente distante de operação sobre bits.

**`int.bit_count()` do Python 3.10+:** built-in, sem implementação manual. Cobre
apenas `bitCount` — os demais nove métodos não têm equivalentes built-in e
precisariam de implementação manual de qualquer forma, criando inconsistência de
abordagem. Também restringiria o projeto a Python ≥ 3.10.

**Portar os algoritmos do OpenJDK (Hacker's Delight):** fidelidade algorítmica ao
OpenJDK com adaptação das masks para garantir operação em 32 bits no Python. O(1)
com número constante de operações. Sem alocações intermediárias. Rastreável a fonte
canônica.

## Decisão

Portar os algoritmos de referência do OpenJDK para todos os dez métodos, com três
adaptações obrigatórias para Python:

1. Aplicar `_to_uint32` na entrada quando o algoritmo assume valor sem sinal de 32 bits.
2. Aplicar `_to_int32` no resultado quando o retorno deve ser inteiro com sinal.
3. Usar masks explícitas em resultados intermediários onde o Python não limita
   automaticamente a 32 bits.

Mapeamento algoritmo → referência bibliográfica:

| Método                  | Algoritmo central                                    | Referência  |
| ----------------------- | ---------------------------------------------------- | ----------- |
| `bitCount`              | Soma paralela (population count)                     | H.D. cap. 5 |
| `highestOneBit`         | Propagação de MSB por OR + isolamento                | H.D. §2-1   |
| `lowestOneBit`          | `n & (-n)` — propriedade do complemento de dois      | H.D. §2-1   |
| `numberOfLeadingZeros`  | Busca binária por halvings                           | H.D. §5-3   |
| `numberOfTrailingZeros` | NLZ aplicado ao LSB isolado                          | H.D. §5-4   |
| `reverse`               | Permutação paralela por trocas sucessivas de metades | H.D. §7-1   |
| `reverseBytes`          | Extração byte a byte e reagrupamento                 | —           |
| `rotateLeft`            | `(n << d) \| (n >> (32 - d))`, distância módulo 32   | H.D. §2-14  |
| `rotateRight`           | `rotateLeft(n, -d)`                                  | H.D. §2-14  |
| `signum`                | `(n > 0) - (n < 0)`                                  | H.D. §2-7   |

Cada método documenta o algoritmo e a referência em seu docstring.

Exemplo de adaptação — `bitCount`:

```python
@staticmethod
def bitCount(i: int) -> int:
    n = _to_uint32(i)                              # garante 32 bits sem sinal
    n = n - ((n >> 1) & 0x5555_5555)              # soma pares de bits
    n = (n & 0x3333_3333) + ((n >> 2) & 0x3333_3333)  # soma grupos de 4
    n = (n + (n >> 4)) & 0x0F0F_0F0F              # soma grupos de 8
    return ((n * 0x0101_0101) & _MASK32) >> 24     # acumula nos 8 bits mais altos
```

A mask `& _MASK32` antes do `>> 24` é adaptação Python: sem ela, a multiplicação
pode exceder 32 bits e o shift não isolaria os 8 bits esperados.

## Justificativa

A fidelidade algorítmica ao OpenJDK é o critério prioritário. Esses algoritmos foram
desenvolvidos com os mesmos requisitos: operação correta sobre inteiros de 32 bits,
O(1), sem laços. Portá-los garante que qualquer comportamento de `JInteger` é
diretamente rastreável à implementação Java de referência — essencial para um projeto
cujo propósito é replicar um contrato Java.

A legibilidade é preservada via docstrings que explicam cada passo do algoritmo,
eliminando a necessidade de inferir o mecanismo a partir das masks hexadecimais.

## Consequências

**Positivas:** comportamento bit a bit idêntico ao Java em todos os casos de borda
verificados; O(1) para todos os dez métodos; rastreável ao OpenJDK e ao livro de
referência; docstrings servem como documentação do algoritmo.

**Negativas:** masks como `0x5555_5555`, `0x3333_3333`, `0x0F0F_0F0F` são opacas
sem o contexto do algoritmo — revisão exige leitura dos docstrings ou da referência
bibliográfica; bugs sutis de port (ex: esquecer uma mask intermediária) não causam
erro imediato, apenas resultado incorreto — a suite de testes é a principal proteção.

## Revisão

Revisável para adotar built-ins Python quando equivalentes estiverem disponíveis para
todos os métodos, ou quando o projeto definir Python ≥ 3.10 como versão mínima e
novos built-ins cobrirem mais casos.
