# ADR-015: Estratégia Unificada de Formatação de Strings de Ponto Flutuante

## Status

Aceito

## Contexto

O Python adota o algoritmo de David Gay (a partir da versão 3.1) para assegurar que a conversão de um float para string gere a menor representação decimal possível que garanta um "round-trip" perfeito (ou seja, `float(repr(x)) == x`). Além disso, o método `float.hex()` do Python produz strings hexadecimais padronizadas na norma IEEE 754 com diretrizes muito específicas quanto à formatação de prefixos, sinais no expoente e preenchimento de zeros à esquerda/direita. O ecossistema Java possui os métodos nativos `Double.toString()` e `Double.toHexString()`. Embora ambos sejam matematicamente corretos, suas saídas de texto diferem sutilmente da formatação padrão esperada pelas suites de teste e usuários do CPython.

## Decisão

Adotaremos os motores nativos do Java (`Double.toString()` e `Double.toHexString()`) como base de conversão de alto desempenho, mas aplicaremos uma camada de pós-processamento textual obrigatória. Para strings normais (`__str__` e `__repr__`), caso a saída do Java divirja das regras de compressão do Python, interceptaremos o fluxo usando formatadores explícitos como `String.format("%.17g")`. Para strings hexadecimais, utilizaremos manipulação manual de strings (como substrings e substituições via regex) sobre o resultado do `Double.toHexString()` para ajustar os prefixos, o sinal do expoente e o preenchimento de zeros, alinhando a saída perfeitamente ao formato do `float.hex()`.

## Consequências

- **Positivo:** Alcançamos compatibilidade visual e semântica absoluta com o interpretador oficial do Python para exibições textuais e representações hexadecimais.
- **Negativo:** A conversão de ponto flutuante para texto torna-se consideravelmente mais lenta que a chamada nativa direta do Java, introduzindo alocações adicionais de memória Heap para objetos de string temporários durante o pós-processamento.
