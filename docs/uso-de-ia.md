# Uso de IA Generativa

## Objetivo

Este documento registra o uso de ferramentas de IA generativa durante o desenvolvimento do projeto, conforme exigido pela disciplina de Gerência de Configuração de Software.

O uso de IA teve caráter exclusivamente assistivo. Todo código, documentação e testes gerados com auxílio de IA foram revisados, adaptados e validados pelos membros da equipe antes de sua integração ao repositório.

A equipe permanece responsável por compreender integralmente os artefatos produzidos e por explicar oralmente qualquer código submetido sob sua autoria.

---

## Ferramentas Utilizadas

| Ferramenta | Finalidade |
|------------|------------|
| ChatGPT | Explicações técnicas, documentação, elaboração de relatórios, geração de testes, criação de issues, revisão de código, auxílio na análise de compatibilidade entre Java e Python e apoio à implementação das classes do projeto |
| Claude | Análise da especificação Java SE 8, apoio à implementação das classes `JInteger`, `JFloat` e `JString`, geração de testes unitários, identificação de casos de borda, documentação de incompatibilidades, sugestões de refatoração e validação da aderência à API Java |

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

* Métodos de conversão, parsing, comparação e operações bit a bit da classe `JInteger`
* Métodos de conversão, parsing, operações IEEE 754 e comparação da classe `JFloat`
* Métodos de manipulação e comparação de strings da classe `JString`

**Tipo de auxílio:**

* [x] Implementação
* [x] Testes
* [ ] Documentação
* [x] Refatoração
* [x] Explicação técnica

### Prompt representativo

> Você é um arquiteto de software sênior especialista em Java SE 8, Python 3.12+, design de APIs, compatibilidade entre linguagens e engenharia de software.
>
> Sua missão é implementar uma biblioteca Python que replique, da forma mais fiel possível, o contrato público das classes da API Java SE 8, com base exclusivamente na documentação oficial da Oracle.
>
> A implementação deve preservar a semântica da API Java sempre que tecnicamente possível dentro das limitações da linguagem Python.
>
> O prompt especificou requisitos detalhados de:
>
> * fidelidade à API Java;
> * preservação da nomenclatura camelCase;
> * tratamento de diferenças entre Java e Python;
> * controle de overflow e representação binária;
> * robustez para casos extremos e entradas inválidas;
> * documentação de incompatibilidades;
> * geração de testes unitários com pytest;
> * análise prévia das decisões de projeto;
> * avaliação de compatibilidade dos métodos implementados.
>
> O mesmo modelo de prompt foi adaptado para cada classe implementada (`JInteger`, `JFloat` e `JString`), substituindo apenas a especificação da API correspondente.

### Resultado utilizado

As ferramentas de IA foram utilizadas como apoio técnico para:

* análise das diferenças entre as APIs Java e Python;
* identificação dos métodos previstos pela especificação oficial;
* geração de sugestões de implementação;
* explicação do comportamento esperado dos métodos da API Java;
* geração de testes unitários;
* identificação de casos de borda;
* documentação de adaptações necessárias devido às diferenças entre as linguagens;
* elaboração de análises de compatibilidade entre a implementação Python e a especificação Java.

As respostas produzidas serviram como material de apoio para estudo, validação de decisões de projeto e implementação dos métodos das classes desenvolvidas.

### Adaptações realizadas pela equipe

* Leitura e análise da documentação oficial da Oracle para validação das respostas geradas.
* Revisão integral de todo código sugerido pelas ferramentas de IA.
* Correção de inconsistências identificadas durante testes e revisão manual.
* Adequação das implementações à arquitetura definida pela equipe.
* Ajustes de compatibilidade com os testes automatizados do projeto.
* Criação de testes adicionais não contemplados pelas sugestões iniciais.
* Refatoração de código para melhorar legibilidade, manutenibilidade e aderência ao padrão do projeto.
* Validação dos comportamentos em casos extremos, incluindo overflow, operações binárias e tratamento de exceções.
* Documentação das adaptações necessárias devido às diferenças entre Java e Python.

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
