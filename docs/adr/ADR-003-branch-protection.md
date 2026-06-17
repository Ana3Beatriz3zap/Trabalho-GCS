# ADR-003: Proteção da Branch Main

## Status

Aceito

## Contexto

É necessário evitar alterações diretas na branch principal do projeto.

## Alternativas Consideradas

- Permitir push direto.
- Utilizar Pull Requests com aprovação obrigatória.

## Decisão

Todas as alterações deverão ser integradas por meio de Pull Requests.

## Justificativa

A revisão reduz riscos de erros e aumenta a rastreabilidade das mudanças.

## Consequências

### Positivas

- Maior controle das alterações.
- Histórico de revisões.
- Melhor colaboração da equipe.

### Negativas

- Processo de integração ligeiramente mais demorado
