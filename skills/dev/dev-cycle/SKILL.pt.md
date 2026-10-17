---
name: dev-cycle
version: 1.2.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-08-22
description: "Ciclo de desenvolvimento de 8 fases: solicitações de funcionalidades, estado atual, planejamento funcional, frontend, planejamento do backend, código do backend, testes, casos de uso. Estrutura iterativa para o desenvolvimento sistemático de software."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [development, dev-cycle, phases, workflow, systematic, iterative]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/dev-zyklus.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 3d82b648971c28906aeabf5b953a28ac162897503581e5cb5a6af8d9f0b1ae8f
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.126617+00:00"
---
<img src="banner.png" width="100%" alt="dev-cycle banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

# Ciclo de Desenvolvimento (Dev Cycle) (Deutsch)

> **Objetivo:** Processo estruturado desde a solicitação de funcionalidade até o sistema validado.
> Todo desenvolvimento passa por estas 8 fases.

> 📐 **Anexo:** `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` —
> „esquema elétrico do desenvolvimento de software" legível por humanos (HTML, abrir no navegador):
> mapa geral pesquisado de fases, circuitos de controle, papéis, cadeias de processos e portões de teste
> (pesquisa na web 08/2026), no qual este ciclo de 8 fases se insere.

---

## Visão geral e finalidade

```
  +--------------------------------------------------------------+
  |                    DEVELOPMENT CYCLE                           |
  +--------------------------------------------------------------+
  |                                                                |
  |  Phase 1   Feature Requests (functional requirements)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 2   Check Current State (What already exists?)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 3   Functional Planning                                 |
  |            (Workflows, Agents, Experts, Skills, Services)      |
  |     |                                                          |
  |     v                                                          |
  |  Phase 4   Implement Functional Frontend                       |
  |            (Skill files, workflow markdown, agent profiles)     |
  |     |                                                          |
  |     v                                                          |
  |  Phase 5   Plan and Align Backend                              |
  |            (CLI handlers, DB schema, API endpoints)            |
  |     |                                                          |
  |     v                                                          |
  |  Phase 6   Implement Backend Tasks                             |
  |            (Python code, tools, DB migrations)                 |
  |     |                                                          |
  |     v                                                          |
  |  Phase 7   Test Execution, Review Gate and Bugfixes           |
  |            (B/O/E tests, bugfix protocol, code review)          |
  |     |                                                          |
  |     v                                                          |
  |  Phase 8   Functional and Feature Test: USE CASES              |
  |            (End-to-end validation from user perspective)        |
  |                                                                |
  +--------------------------------------------------------------+

  Core principles throughout:
  - Functional description first (before code)
  - CLI First (everything controllable via terminal)
  - Clear separation of user data and system data
  - Shift-Left: tests are DESIGNED early (phases 1/3/5) and WRITTEN
    with the code (phase 6) - phase 7 only EXECUTES them
```


---

## Fase 1: Solicitações de Funcionalidades (Requisitos Funcionais)

**O que:** Coletar e formular os requisitos funcionais.

**Entrada:**
- Desejos, ideias e problemas dos usuários
- Sugestões de parceiros (assistentes LLM)
- Insights de casos de uso (ciclo de realimentação!)

**Saída:**
- Tarefas no sistema de tarefas (por exemplo, como issue, ticket ou lista de TODO)
- Os requisitos descrevem O QUE é desejado, não COMO
- Cada requisito traz critérios de aceitação testáveis (Shift-Left: eles se tornam
  os casos de uso da Fase 8 e a lista de verificação de aceitação)

**Regras:**
- Formular sempre os requisitos de forma funcional ("O usuário pode fazer X")
- Não de forma técnica ("Implementar endpoint REST para X")
- Usar os casos de uso como fonte de requisitos (Fase 8 -> Fase 1)

---

## Fase 2: Verificar o Estado Atual

**O que:** Inventariar a funcionalidade existente.

**Lista de verificação:**
```
  [ ] Search existing tools/scripts
  [ ] Check documentation/help on the topic
  [ ] Check existing skills/agents/services
  [ ] Check DB schema (if relevant)
  [ ] Check use cases - has something similar been tested?
```


**Saída:**
- Documentação do que existe, do que falta e do que precisa ser estendido
- Evitar duplicações

---

## Fase 3: Planejamento Funcional

**O que:** Planejar no nível funcional — NÃO escrever código imediatamente.

**Níveis de planejamento:**

| Nível | Pergunta | Artefato |
|-------|----------|----------|
| Workflow | QUANDO/COMO é feita a coordenação? | workflows/*.md |
| Agente | QUEM executa? | agents/*.txt |
| Especialista | QUEM possui o conhecimento de domínio? | experts/*/ |
| Skill | O QUE é feito? | skills/*.md |
| Serviço | COMO é feito tecnicamente? | services/*/ |

**Regras:**
- Pensar primeiro funcionalmente, depois tecnicamente
- Shift-Left: para cada nível de planejamento, planejar também sua VERIFICAÇÃO — requisito →
  critério de aceitação, serviço/interface → teste de integração, unidade → teste unitário
  (seleção de nível e técnica de teste: [software-testing](../software-testing/SKILL.md))
- Workflows descrevem processos, não detalhes de implementação
- Cada agente precisa de um perfil claro
- Serviços devem funcionar sem dados do usuário

---

## Fase 4: Implementar o Frontend Funcional

**O que:** Criar arquivos de skills, markdown de workflows e perfis de agentes.

O "frontend" aqui é a camada de descrição funcional:
- Arquivos de workflow (.md)
- Perfis de agentes (.txt)
- Conhecimento de especialistas
- Descrições de serviços
- Arquivos de ajuda

**Saída:**
- Todas as descrições funcionais existem
- Um parceiro LLM consegue ler e compreender o workflow
- A camada funcional está totalmente documentada

---

## Fase 5: Planejar e Alinhar o Backend

**O que:** Alinhar a arquitetura técnica ao frontend funcional.

**Áreas de planejamento:**

| Área | Pergunta | Localização |
|------|----------|-------------|
| Handlers de CLI | Quais comandos? | handlers/*.py |
| Esquema de BD | Quais tabelas/colunas? | schema/*.sql |
| Endpoints de API | Quais endpoints de GUI? | server.py |
| Ferramentas | Quais scripts Python? | tools/*.py |

**Saída:**
- Plano técnico alinhado ao frontend funcional
- Projeto do esquema de BD
- Estrutura dos comandos de CLI

---

## Fase 6: Implementar as Tarefas do Backend

**O que:** Escrever código Python, migrações de BD e handlers de CLI.

**Lista de verificação (por tarefa):**
```
  [ ] Unit tests written (TDD: test before code) and green locally?
  [ ] Works without user data (empty DB)?
  [ ] CLI command available?
  [ ] Input can come from files/folders?
  [ ] Output goes to structured DB?
  [ ] Scan/import is repeatable (idempotent)?
  [ ] No hardcoded path?
  [ ] Tool registered and documented?
  [ ] Help file created?
```


---

## Fase 7: Execução de Testes, Portão de Revisão e Correções de Bugs

**O que:** Garantir a correção técnica. Os testes foram PROJETADOS nas fases 1/3/5 e
ESCRITOS na fase 6 (Shift-Left) — a fase 7 os EXECUTA em portões escalonados e bloqueantes:
testes rápidos a cada commit, testes custosos (regressão completa, E2E, carga) à noite
ou antes do lançamento. Mapeamento de portões e seleção de testes: [software-testing](../software-testing/SKILL.md).

**Tipos de teste (B/O/E):**

| Tipo | Perspectiva | Descrição |
|------|-------------|-----------|
| Testes B | Externa/Automatizada | Testes automatizados, CI/CD |
| Testes O | Funcional (Entrada->Saída) | Verificação funcional manual |
| Testes E | Subjetiva/Experiência | Avaliação de UX, ergonomia |

**Portão de revisão (antes da Fase 8):**
- Revisão de código por um segundo par de olhos (colega, agente revisor ou consultor)
- Nada entra na validação de casos de uso sem revisão
- Os achados da revisão retornam à Fase 6 como solicitações de mudança

**Sobre bugs:**
- Aplicar o protocolo de correção de bugs
- Respeitar a regra dos 20 minutos (mudar de abordagem após 20 min)
- Documentar as lições aprendidas

---

## Fase 8: Teste Funcional e de Funcionalidades - CASOS DE USO

**O que:** Validação de ponta a ponta na perspectiva do usuário.

**Os casos de uso servem AMBAS as finalidades:**
1. **Indicadores de funcionalidade** - O que é desejado? O que deveria ser possível?
2. **Cenários de teste** - Realmente funciona do início ao fim?

**Formato do caso de uso:**
```
  USECASE_NNN: Short Title

  PRECONDITION: What must be in place?
  INPUT:        What does the user enter / what data?
  EXPECTED:     What should the result be?
  TESTS:        Which components are tested?
```


**Ciclo de realimentação:**
- Casos de uso com falha -> novas tarefas na Fase 1
- Casos de uso bem-sucedidos -> funcionalidades validadas
- Novas ideias de casos de uso -> registrar como tarefas

---

## Resumo: O Ciclo

```
  Phase 8 (Use Cases)
       |
       | New requirements / bugs
       v
  Phase 1 (Feature Requests)  -->  Phase 2 (Current State)
       ^                                    |
       |                                    v
  Phase 7 (Tests/Bugs)         Phase 3 (Functional Planning)
       ^                                    |
       |                                    v
  Phase 6 (Backend Code)       Phase 4 (Functional Frontend)
       ^                                    |
       |                                    v
       +──────────────────── Phase 5 (Backend Planning)
```

O ciclo é um laço: os casos de uso validam as funcionalidades e, ao mesmo tempo,
geram novos requisitos.

---

## Circuitos de controle (Regelkreise)

O ciclo de 8 fases é o circuito de controle EXTERNO. Dentro dele, laços mais rápidos
funcionam simultaneamente — quanto mais interno o laço, mais rápido o seu ritmo e mais
barata a correção:

| Laço | Ritmo | Onde no ciclo |
|------|-------|---------------|
| TDD (Red–Green–Refactor) | segundos–minutos | dentro da Fase 6 |
| Execução de testes / portões de CI | < 10 min por commit | Fase 7 → Fase 6 em caso de falha |
| Portão de revisão (4 olhos) | horas | entre a Fase 7 e a Fase 8 |
| Laço de correção de bugs | horas | Fase 7 → Fase 6 (protocolo de correção) |
| Laço de casos de uso | por ciclo | Fase 8 → Fase 1 |
| Realimentação operacional | contínua | monitoramento/incidentes → Fase 1 |

Regra prática: manter o tempo entre commit e retorno abaixo de 10 minutos — um laço lento
acaba sendo contornado. Mapa visual de todos os laços com tempos: anexado
`SCHALTPLAN-SOFTWAREENTWICKLUNG.html`, folha BL-2.

---

## Skills específicas por fase

| Fase | Skill especializada | Gatilho |
|------|---------------------|---------|
| Fases 1-3 | Bootstrapper de projeto (se disponível) | Criar um novo projeto (greenfield) |
| Fase 2 | [project-onboarding](../project-onboarding/SKILL.en.md) | Assumir um projeto existente |
| Fases 2-3 | [docs-analysis](../docs-analysis/SKILL.en.md) | Verificar documentos de requisitos contra o código |
| Fases 5-6 | [pipeline-optimizer](../pipeline-optimizer/SKILL.en.md) | Renovar estruturas existentes |
| Fase 7 | [bugfix-protocol](../bugfix-protocol/SKILL.en.md) | Depuração sistemática em 6 fases |
| Fases 7-8 | [bugsweep](../bugsweep/SKILL.en.md) | Varredura convergente de bugs antes de um lançamento |
| Fases 1, 3, 7 | [software-testing](../software-testing/SKILL.md) | Escolher níveis, tipos e técnicas de teste; mapeamento de portões de CI/CD |
| Após a Fase 8 | [github-repo-care](../github-repo-care/SKILL.en.md) | Lançamento: publicar e manter o repositório |

Se a sua coleção de skills tiver um índice de skills, pesquise nele por outras skills específicas por fase.

---

## Registro de alterações

### 1.2.0 (2026-08-22)
- Shift-Left ancorado (alinhamento com a pesquisa e o esquema do anexo): critérios de aceitação como
  saída da Fase 1, projeto de testes por nível de planejamento na Fase 3, testes unitários (TDD) como primeiro
  item da lista de verificação da Fase 6; Fase 7 renomeada para „Execução de Testes, Portão de Revisão e
  Correções de Bugs" — os testes são executados ali, não apenas escritos
- Portão de revisão (princípio dos 4 olhos) como passo explícito antes da Fase 8
- Nova seção „Circuitos de controle (Regelkreise)" com tempos de ciclo (TDD, CI, revisão,
  correção de bugs, casos de uso, operação)
- Tabela de skills por fase ampliada: software-testing (fases 1/3/7), github-repo-care
  (após a Fase 8); referências a software-testing na Fase 3 e na Fase 7

### 1.1.1 (2026-08-22)
- Anexo `SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (mapa geral legível por humanos: fases,
  circuitos de controle, papéis, cadeias de processos, portões de teste — síntese de uma pesquisa na web 08/2026)
  mais referência no cabeçalho do arquivo

### 1.1.0 (2026-06-13)
- Nova tabela „Skills específicas por fase" com referências a project-onboarding, docs-analysis, pipeline-optimizer, bugfix-protocol e bugsweep

### 1.0.0 (2026-03-12)
- Portado do BACH (dev-zyklus v1.0.0)

---

*Criado: 2026-01-28 | Portado: 2026-03-12*
