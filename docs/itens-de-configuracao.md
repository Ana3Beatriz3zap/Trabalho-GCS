# Itens de Configuração

| Item                     | Responsável | Formato | Periodicidade de Mudança | Dependências                                            |
| ------------------------ | ----------- | ------- | ------------------------ | ------------------------------------------------------- |
| JInteger                 | Desenvolvedoras  | .py     | Frequente                | Nenhuma                                                 |
| Testes de JInteger       | Desenvolvedoras   | .py     | Frequente                | JInteger                                                |
| JFloat                   | Desenvolvedoras   | .py     | Frequente                | Nenhuma                                                 |
| Testes de JFloat         | Desenvolvedoras   | .py     | Frequente                | JFloat                                                  |
| JString                  | Desenvolvedoras   | .py     | Frequente                | Nenhuma                                                 |
| Testes de JString        | Desenvolvedoras   | .py     | Frequente                | JString                                                 |
| ADRs                     | Amanda   | .md     | Baixa                    | Nenhuma                                                 |
| README.md                | Ana Beatriz  | .md     | Média                    | ADRs, docs/adaptacoes.md                                                |
| docs/adaptacoes.md       | Desenvolvedoras   | .md     | Média                    | Nenhuma                                                 |
| .github/workflows/ci.yml | Maria Eduarda   | .yml    | Baixa                    | Testes de JInteger, Testes de JFloat, Testes de JString |
