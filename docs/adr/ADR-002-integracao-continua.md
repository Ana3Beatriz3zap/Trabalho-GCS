# ADR-002: Utilização do GitHub Actions

## Status

Aceito

## Contexto

O projeto necessita de validações automáticas para garantir a qualidade do código antes da integração de alterações.

## Alternativas Consideradas

- GitHub Actions
- GitLab CI/CD

## Decisão

Utilizar GitHub Actions como ferramenta de Integração Contínua.

## Justificativa

A solução está integrada ao GitHub e não requer infraestrutura adicional.

## Consequências

### Positivas

- Configuração simples.
- Execução automática em push e pull request.
- Fácil manutenção.

### Negativas

- Dependência da infraestrutura do GitHub.
