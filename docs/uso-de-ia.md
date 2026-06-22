# Uso de IA Generativa

## Objetivo

Este documento registra o uso de ferramentas de IA generativa durante o desenvolvimento do projeto, conforme exigido pela disciplina de Gerência de Configuração de Software.

O uso de IA teve caráter exclusivamente assistivo. Todo código, documentação e testes gerados com auxílio de IA foram revisados, adaptados e validados pelos membros da equipe antes de sua integração ao repositório.

A equipe permanece responsável por compreender integralmente os artefatos produzidos e por explicar oralmente qualquer código submetido sob sua autoria.

---

## Ferramentas Utilizadas

| Ferramenta | Finalidade |
|------------|------------|
| ChatGPT | Explicações técnicas, geração de exemplos, auxílio em implementação, documentação, testes, criação de issues e elaboração de Pull Requests |
| Claude | Apoio na implementação das classes `JInteger`, `JFloat` e `JString`, geração de testes unitários, explicação de comportamentos da API Java, sugestões de código, refatoração e validação de casos de teste |

---

# Registro de Utilização

## Registro IA-001

**Responsável:** Ana Beatriz

**Data:** 17-06-2026

**Issue:** N/A

**Classe/Módulo:** Configuração do Repositório / Processo de GCS

**Artefato(s):** N/A

**Tipo de auxílio:**

* [ ] Implementação
* [ ] Testes
* [x] Documentação
* [ ] Refatoração
* [ ] Explicação técnica

### Prompt representativo

> Gere um template de Pull Request para um projeto acadêmico de Gerência de Configuração de Software utilizando GitHub Flow. O template deve conter descrição da mudança, issue relacionada, testes realizados, arquivos alterados, impactos da mudança, observações para revisão e checklist final.

### Resultado utilizado

A IA foi utilizada para gerar uma estrutura inicial padronizada para a descrição de Pull Request da equipe. O conteúdo produzido serviu como base para uniformizar a abertura de PRs e melhorar a rastreabilidade das mudanças realizadas no projeto.

### Adaptações realizadas pela equipe

* Revisão manual do conteúdo gerado.
* Adequação ao processo definido pela disciplina.
* Ajustes para contemplar os requisitos de rastreabilidade entre issues, commits e pull requests.
* Inclusão de checklist de conformidade com os padrões do projeto.

---

## Registro IA-002

**Responsável:** Desenvolvedoras

**Data:** Durante o desenvolvimento das classes JavaLang

**Issue:** Diversas issues relacionadas à implementação das classes `JInteger`, `JFloat` e `JString`

**Classe/Módulo:** JInteger, JFloat e JString

**Método(s):**

* Diversos métodos das classes `JInteger`
* Diversos métodos das classes `JFloat`
* Diversos métodos das classes `JString`

**Tipo de auxílio:**

* [x] Implementação
* [x] Testes
* [ ] Documentação
* [x] Refatoração
* [x] Explicação técnica

### Prompt representativo

> Implemente em Python o método equivalente ao método da API Java da classe correspondente, preservando o comportamento da biblioteca padrão do Java. Gere também testes unitários cobrindo casos de sucesso, casos de borda e cenários de exceção. Considere compatibilidade com os testes existentes do projeto e aderência ao estilo já utilizado nas demais classes. Explique as decisões adotadas e apresente exemplos de uso.

### Resultado utilizado

A ferramenta Claude foi utilizada como apoio na implementação de métodos das classes `JInteger`, `JFloat` e `JString`, bem como na geração de testes unitários associados. A ferramenta forneceu sugestões de código, explicações sobre o comportamento da API Java original, tratamento de exceções, casos especiais e cenários de teste.

As respostas serviram como ponto de partida para a implementação dos métodos e para a elaboração dos testes automatizados, auxiliando na compreensão do comportamento esperado das classes equivalentes à biblioteca `java.lang`.

### Adaptações realizadas pela equipe

* Revisão integral de todo código sugerido pela IA.
* Revisão e validação de todos os testes gerados.
* Adequação das implementações à arquitetura do projeto.
* Ajustes para compatibilidade com os testes automatizados existentes.
* Inclusão de casos de teste adicionais identificados durante a revisão manual.
* Correção de inconsistências identificadas durante a validação manual.
* Padronização do estilo de código conforme as convenções adotadas pela equipe.
* Implementação de melhorias adicionais não contempladas nas sugestões originais.
* Verificação da equivalência comportamental com a documentação oficial da API Java.

### Arquivos afetados

* `javalang/jinteger.py`
* `javalang/jfloat.py`
* `javalang/jstring.py`
* `tests/test_jinteger.py`
* `tests/test_jfloat.py`
* `tests/test_jstring.py`

---

## Resumo Consolidado

| ID | Responsável | Classe/Módulo | Métodos | Tipo de Uso |
|-----|-------------|---------------|----------|-------------|
| IA-001 | Ana Beatriz | Processo de GCS / Configuração do Repositório | N/A | Documentação |
| IA-002 | Desenvolvedoras | JInteger, JFloat e JString | Diversos métodos | Implementação, Testes, Refatoração e Explicação Técnica |