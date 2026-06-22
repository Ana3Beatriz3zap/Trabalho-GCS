# 📌 Auditoria de Controle de Mudanças

## 📝 Objetivo da Auditoria

Esta auditoria tem como objetivo verificar o processo de controle de mudanças do projeto, garantindo que todas as alterações relevantes possam ser rastreadas desde sua solicitação (issue) até sua integração na branch principal (`main`), incluindo branches, commits e Pull Requests.

---

## 🔍 Escopo da Análise

Foram analisados os seguintes artefatos do repositório:

- Issues criadas durante o desenvolvimento
- Branches associadas às implementações
- Commits realizados nas branches
- Pull Requests utilizados para integração
- Histórico de merge na branch `main`

---

## 🔗 Rastreabilidade de Mudanças

### 📌 Cadeia de rastreabilidade identificada

O projeto segue uma cadeia estruturada de controle de mudanças:

**Issue → Branch → Commits → Pull Request → Merge na main**

---

### 🧩 Exemplo de rastreabilidade (padrão adotado)

Para cada mudança relevante, o fluxo seguiu o padrão:

- Uma **issue** foi criada para descrever a necessidade da alteração
- Uma **branch específica** foi criada a partir da `main`
- O desenvolvimento ocorreu por meio de **commits semânticos**
- Um **Pull Request (PR)** foi aberto vinculando a branch à issue
- Após revisão e CI verde, o PR foi **mergeado na `main`**

---

## 🏷️ Verificação de Issues e Pull Requests

Foi identificado que o projeto mantém associação entre issues e Pull Requests através de:

- Referências no título ou descrição do PR
- Uso de palavras-chave como `Closes`, `Fixes` ou `Resolves`
- Histórico de PRs vinculados a funcionalidades específicas

**Resultado:** Conforme.

---

## 🏷️ Utilização de Labels

Foi verificado o uso de labels para organização das issues e Pull Requests.

Exemplos de categorização:

- `feature`
- `release`
- `documentation`
- `refactor`
- `decision`
- `configuration`
- `tests`
- `refactor`
- `goodfirst issue`
- `bug`

As labels auxiliaram na classificação e priorização das mudanças.

**Resultado:** Conforme.

---

## 🎯 Utilização de Milestones

Foi identificado o uso de milestones para agrupamento de entregas relacionadas a versões do projeto.


- `SETUP`
- `JInteger`
- `JFloat`
- `JString`
- `Auditoria`

As milestones ajudaram a organizar o progresso do projeto por versões.

**Resultado:** Conforme.

---

## 👤 Atribuição de Responsáveis

As issues e Pull Requests possuem atribuição de responsáveis, garantindo clareza sobre:

- Quem executou cada mudança
- Quem revisou cada Pull Request
- Responsabilidade individual por entregas

**Resultado:** Conforme.

---


## 📊 Avaliação da Rastreabilidade

| Elemento | Status |
|----------|--------|
| Issues vinculadas | ✅ Conforme |
| Branches relacionadas | ✅ Conforme |
| Commits rastreáveis | ✅ Conforme |
| Pull Requests vinculados | ✅ Conforme |
| Uso de labels | ✅ Conforme |
| Uso de milestones | ✅ Conforme |
| Responsáveis atribuídos | ✅ Conforme |

---

## ✅ Conclusão

O projeto apresenta uma cadeia consistente de rastreabilidade entre issues, branches, commits e Pull Requests.

Todas as mudanças relevantes seguem um fluxo estruturado, permitindo auditoria clara do ciclo completo de desenvolvimento, desde a solicitação da alteração até sua integração na branch principal.

**Status da Auditoria:** Aprovada ✅