# ADR-004: Ordem de Implementação das Classes

## Status

Aceito

## Contexto

O projeto contempla a implementação das classes JInteger, JFloat e JString, juntamente com suas respectivas suítes de testes. Como o desenvolvimento será conduzido de forma incremental e controlado por meio de Pull Requests, tornou-se necessário definir uma estratégia para a sequência de implementação desses módulos.

## Alternativas Consideradas

### Implementar as classes em ordem aleatória

Permite que cada integrante escolha livremente qual classe desenvolver primeiro, porém dificulta o planejamento e a previsibilidade das entregas.

### Implementar as classes em paralelo

Possibilita maior distribuição de tarefas entre os membros da equipe, mas aumenta a complexidade de coordenação, revisão e integração das alterações.

### Implementar por ordem crescente de complexidade

Inicia pelos módulos mais simples e evolui gradualmente para os mais complexos, permitindo aprendizado progressivo e entregas frequentes.

## Decisão

Foi definida a seguinte ordem de implementação:

1. JInteger
2. JFloat
3. JString

## Justificativa

A sequência escolhida foi planejada para maximizar a produtividade da equipe e reduzir riscos durante o desenvolvimento.

A implementação terá início com JInteger, considerada a classe de menor complexidade e com maior densidade de métodos estáticos. Essa escolha permite estabelecer rapidamente o fluxo de desenvolvimento, testes, revisão e integração, favorecendo a criação de Pull Requests frequentes e a validação antecipada do processo de trabalho.

Na sequência, será implementada JFloat, que apresenta complexidade intermediária e possibilita consolidar as práticas adotadas na etapa anterior.

Por fim, será desenvolvida JString, a classe mais abrangente do projeto. Nesse momento, a equipe já terá adquirido experiência com o fluxo de desenvolvimento, revisão de código e integração contínua, reduzindo os riscos associados à implementação do módulo mais complexo.

## Consequências

### Positivas

- Entregas incrementais desde as primeiras etapas do projeto.
- Maior frequência de Pull Requests nas fases iniciais.
- Redução dos riscos relacionados aos módulos mais complexos.
- Aprendizado gradual e contínuo do fluxo de trabalho.
- Validação antecipada dos processos de revisão de código e integração contínua.

### Negativas

- Funcionalidades relacionadas à classe JString estarão disponíveis apenas nas etapas finais do desenvolvimento.
- Possível concentração de esforço em um módulo mais complexo ao final do cronograma.

## Revisão

Esta decisão poderá ser revisada caso sejam identificadas novas dependências técnicas ou restrições que justifiquem a alteração da ordem de implementação definida
