# ADR-005: Estrutura Mínima Esperada do Repositório

## Status

Aceito

## Contexto

Com o início do desenvolvimento do projeto `javalang-py`, que implementará as classes `JInteger`, `JFloat` e `JString` em Python, é essencial estabelecer uma organização padronizada para o código-fonte, testes, documentação e fluxos de trabalho (CI/CD). A ausência de um padrão estrutural nas fases iniciais pode gerar desorganização, dificultar a integração contínua e atrasar a adaptação de novos contribuidores ou revisores. Tornou-se necessário definir um esqueleto de diretórios que atenda às boas práticas e seja facilmente compreendido por toda a equipe.

## Alternativas Consideradas

### Estrutura plana (todos os arquivos na raiz)

Consiste em manter o código fonte, testes e documentação no mesmo nível do diretório. Facilita a criação inicial, porém mistura contextos distintos, tornando a navegação e a manutenção insustentáveis à medida que o projeto cresce.

### Uso do padrão `src/` (layout `src/javalang/`)

Consiste em encapsular o código da aplicação dentro de uma pasta `src/`. É uma excelente prática no ecossistema Python para evitar erros de importação durante os testes locais, mas adiciona um nível extra de aninhamento que a equipe pode considerar desnecessário para o escopo e tamanho atual deste projeto.

### Adoção de uma estrutura modular base com pacotes na raiz

Estabelece pastas distintas para o pacote da aplicação (`javalang/`), testes separados na raiz (`tests/`), documentação centralizada (`docs/`) e padronização das ferramentas do GitHub (`.github/`). Equilibra perfeitamente a organização conceitual sem adicionar complexidade excessiva.

## Decisão

Foi definida a adoção da estrutura modular base como a arquitetura mínima de diretórios do repositório. A estrutura inicial esperada é a seguinte:

```text
javalang-py/
├── README.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── .gitignore
├── pyproject.toml
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── feature.md
│   │   ├── bug.md
│   │   └── decision.md
│   └── pull_request_template.md
├── javalang/
│   ├── __init__.py
│   ├── jstring.py
│   ├── jinteger.py
│   └── jfloat.py
├── tests/
│   ├── test_jstring.py
│   ├── test_jinteger.py
│   ├── test_jfloat.py
│   └── test_interop.py
└── docs/
    ├── itens-de-configuracao.md
    ├── adaptacoes.md
    ├── adr/
    │   ├── 0001-nomenclatura-classes.md
    │   ├── 0002-modelo-ramificacao.md
    │   └── 0003-tratamento-locale.md
    ├── relatorios/
    │   ├── status-v0.1.md
    │   ├── status-v0.2.md
    │   └── status-v1.0.md
    ├── auditoria.md
    └── auditoria-cruzada.md
```

### Justificativa

A organização escolhida segrega claramente as diferentes responsabilidades do repositório, seguindo convenções consolidadas no desenvolvimento de software moderno:

- Separação de Contextos: O código de produção (javalang/) fica isolado do código de verificação (tests/), o que facilita a execução do pytest e métricas de cobertura.
- Integração e Padronização: O diretório .github/ centraliza a automação (CI/CD) e garante que as contribuições (Issues e Pull Requests) sigam templates predefinidos, reduzindo o atrito na comunicação da equipe.
- Gestão de Conhecimento: O diretório docs/ fornece um local centralizado para o histórico de decisões (ADRs), itens de configuração e relatórios de auditoria e status. Isso garante rastreabilidade total do projeto.
- Gerenciamento de Dependências: O uso do pyproject.toml na raiz moderniza a gestão de dependências e empacotamento, seguindo as diretrizes atuais do ecossistema Python (PEP 518).

Esta estrutura é considerada a "mínima esperada", fornecendo um alicerce sólido que permite escalabilidade e flexibilidade.

## Consequências

### Positivas

- Ambiente de desenvolvimento altamente organizado desde o primeiro dia.
- Redução do atrito cognitivo para novos desenvolvedores entenderem onde cada arquivo deve ser criado.
- Processos de CI/CD, revisão de código e relatórios já possuem seus locais adequados, facilitando a automação.
- Facilidade em rastrear decisões arquiteturais passadas (via docs/adr/).

### Negativas

- Exige disciplina e rigor da equipe para respeitar os diretórios e não criar arquivos soltos na raiz ou em locais inapropriados.
- Qualquer alteração arquitetural nesta base exigirá a criação de uma nova ADR justificando a adaptação.

## Revisão

Esta estrutura é adaptável. Esta decisão poderá ser revisada e expandida futuramente caso surja a necessidade de novos módulos, ferramentas de linting/formatação (que alterem a configuração raiz) ou mudanças nas políticas de empacotamento, devendo qualquer desvio ser documentado através de uma nova ADR.
