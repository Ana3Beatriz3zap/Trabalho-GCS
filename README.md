# 📌 Ementa do Trabalho

---

## 🧾 Descrição Geral

A equipe deve implementar em **Python** as classes `String`, `Integer` e `Float` da especificação **Java SE 8**, replicando o contrato público (construtores, métodos de instância e métodos estáticos), com as adaptações necessárias à linguagem Python.

Métodos que não puderem ser implementados por limitações da linguagem ou da plataforma devem ser **explicitamente documentados no `README.md`**, com justificativa técnica.

A entrega será avaliada não apenas pelo código, mas principalmente pelo **processo de Gerência de Configuração de Software (GCS)** adotado no repositório.

---

## 🎯 Objetivos do Trabalho

Ao final do projeto, a equipe deverá demonstrar domínio prático sobre:

### 📘 Especificação como contrato
- Leitura de documentação oficial (Javadoc)
- Tradução da especificação para Python
- Preservação de semântica e comportamento

---

### 🔁 Controle de versão distribuído
- Uso intensivo de Git
- Branches por feature
- Commits semânticos
- Uso adequado de rebase quando necessário
- Resolução consciente de conflitos

---

### 🔄 Controle de mudanças
- Toda alteração não trivial deve iniciar em uma issue
- Implementação via pull request
- Revisão por pares obrigatória
- Merge apenas após aprovação documentada

---

### 🏷️ Baselines e versionamento semântico
- Uso de tags para releases
- Definição de marcos por classe implementada
- Organização incremental do projeto

---

### 📊 Auditoria e relatórios
- Geração de relatórios de status por baseline
- Evidências de evolução do sistema
- Explicação clara do histórico de mudanças
- Demonstração da integridade do repositório

---

## 🧠 Princípio Orientador

> O código é o pretexto; a prática de GCS é o objeto da avaliação.

Uma classe perfeitamente implementada em um repositório desorganizado tem menor valor do que uma implementação parcial em um repositório que demonstra disciplina, rastreabilidade e maturidade no processo.

---

## 📊 Papéis da Equipe

| Papel | Atribuições | Responsável |
|------|-------------|-------------|
| **Mantenedor** | Cria o repositório, configura proteção de branch, aprova merges na main, cria releases e tags. Garante a integridade das baselines. | Ana Beatriz |
| **Gerente de Configuração** | Mantém atualizados os documentos de itens de configuração, ADRs e adaptações. Conduz a auditoria interna ao final. | Amanda Beatriz |
| **Engenheiro de Qualidade** | Configura e mantém a CI, garante cobertura mínima de testes, revisa PRs sob a ótica de qualidade e regressão. | Maria Eduarda Gonçalves|
| **Desenvolvedores** | Implementam as classes. Cada aluno é responsável por pelo menos um conjunto de métodos formalmente atribuído via issue. | Ana Beatriz, Amanda Beatriz, Ana Clara Ottoni, Isabela Lopes, Maria Eduarda Gonçalves, Nahie Herradon|
| **Relator** | Produz relatórios de status a cada baseline e o relatório final. Sintetiza o trabalho da equipe para apresentação e gravação do vídeo. | Isabela Lopes |

---
## 7.2 Baseline JInteger

A Baseline JInteger marcou a conclusão da implementação da classe `JInteger`, baseada na especificação da classe `java.lang.Integer` do Java SE 8.

Durante esta etapa foram criadas e rastreadas issues para cada conjunto de funcionalidades previstas na especificação. O desenvolvimento foi realizado em branches específicas, com integração por meio de pull requests revisados pela equipe.

### Funcionalidades implementadas

- Construtores da classe.
- Métodos de conversão entre tipos numéricos.
- Métodos de comparação.
- Métodos utilitários estáticos.
- Operações de manipulação e representação de valores inteiros.
- Tratamento de casos especiais e validações previstas na especificação.

### Evidências de GCS

- Criação de issues para rastreamento das funcionalidades.
- Desenvolvimento em branches dedicadas.
- Histórico de commits semânticos.
- Revisões realizadas via pull requests.
- Integração controlada na branch principal.

### Status

A implementação da classe JInteger encontra-se concluída. Os testes automatizados foram desenvolvidos, executados e aprovados, consolidando esta baseline como uma entrega estável do projeto.

---

## 7.3 Baseline JFloat

A Baseline JFloat teve como objetivo implementar a classe `JFloat`, reproduzindo o comportamento da classe `java.lang.Float` do Java SE 8.

As funcionalidades foram organizadas em issues e desenvolvidas de forma incremental, seguindo o fluxo definido para o projeto.

### Funcionalidades implementadas

- Construtores da classe.
- Métodos de conversão de tipos.
- Métodos de comparação.
- Operações envolvendo valores de ponto flutuante.
- Tratamento de valores especiais, como NaN e infinito.
- Métodos estáticos previstos na especificação.

### Evidências de GCS

- Funcionalidades documentadas por meio de issues.
- Desenvolvimento realizado em branches específicas.
- Integração por pull requests.
- Revisões de código realizadas pela equipe.
- Registro completo das alterações por meio de commits semânticos.

### Status

A implementação da classe JFloat encontra-se concluída. A suíte de testes foi desenvolvida e encontra-se disponível no repositório. Alguns testes permanecem temporariamente desativados, aguardando ativação durante a fase final de integração e validação do projeto.

---

## 7.4 Baseline JString

A Baseline JString corresponde ao desenvolvimento da classe `JString`, baseada na especificação da classe `java.lang.String` do Java SE 8.

Por se tratar da classe mais extensa do projeto, o desenvolvimento foi dividido em grupos de funcionalidades organizados por issues.

### Funcionalidades previstas

- Construtores.
- Métodos de acesso e tamanho.
- Métodos de comparação.
- Métodos de busca.
- Métodos de transformação de texto.
- Operações com expressões regulares.
- Métodos estáticos utilitários.

### Situação atual

Até o momento foram criadas as issues necessárias para organizar o desenvolvimento da classe e parte significativa das funcionalidades já foi implementada.

As implementações realizadas encontram-se distribuídas em pull requests que estão em processo de revisão e integração.

### Evidências de GCS

- Planejamento das funcionalidades através de issues.
- Desenvolvimento em branches específicas.
- Utilização de pull requests para integração.
- Registro das alterações por meio de commits semânticos.
- Rastreabilidade entre requisitos, implementação e revisão.

### Status

A classe JString encontra-se em desenvolvimento. As funcionalidades principais já possuem implementação parcial ou completa, porém ainda existem atividades de integração, revisão e validação pendentes antes da consolidação definitiva desta baseline.
