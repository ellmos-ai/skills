---
name: project-onboarding
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Procedimento padrão para a integração de novos projetos de software: análise de funcionalidades, revisão da qualidade do código, lista de verificação de integração e criação de tarefas."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [onboarding, project, intake, analysis, checklist, code-review]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/projekt-aufnahme.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 8e49954ab15704af930d6a8e717a5fd9c0109ed1378a2421998d889d8e90d359
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.041366+00:00"
---
<img src="banner.png" width="100%" alt="project-onboarding banner">

# Procedimento padrão de integração para novos projetos de software

**Versão:** 1.0
**Data:** 2026-03-12

---

## Visão geral

Este procedimento define quais etapas devem ser executadas em pastas de software recém-descobertas antes de elas serem incluídas em um sistema de gestão de tarefas.

```
┌─────────────────────────────────────────────────────────┐
│           STANDARDAUFNAHMEVERFAHREN                     │
├─────────────────────────────────────────────────────────┤
│  1. Feature-Analyse erstellen                           │
│  2. Code-Qualitaetspruefung (Standard-Tests)            │
│  3. AUFGABEN.txt erstellen                              │
│  4. In Task-Management uebernehmen                      │
└─────────────────────────────────────────────────────────┘
```

---

## Fase 1: Análise de funcionalidades

**Objetivo:** Compreender a ferramenta, as suas funções e o estado de desenvolvimento.

**Criar arquivo:** `Feature_Analyse_<ToolName>.md`

### Modelo

```markdown
# Feature-Analyse: <ToolName>

## Kurzbeschreibung
Ein kurzer Satz der beschreibt was das Tool macht.

---

## Highlights

| Feature | Beschreibung |
|---------|-------------|
| **Feature 1** | Beschreibung |
| **Feature 2** | Beschreibung |

---

## Bewertung der Ausbaustufe

### Aktueller Stand: **<Status> (<X>%)**

Moegliche Status:
- Prototype (0-30%)
- Alpha (30-60%)
- Beta (60-85%)
- Production Ready (85-95%)
- Release (95-100%)

| Kategorie | Bewertung (1-5) | Details |
|-----------|:---------------:|---------|
| **Funktionsumfang** | 3 | |
| **UI/UX** | 3 | |
| **Stabilitaet** | 3 | |
| **Dokumentation** | 3 | |

---

## Empfohlene Erweiterungen

### Prioritaet: Hoch
1. ...

### Prioritaet: Mittel
2. ...

### Prioritaet: Niedrig
3. ...

---

## Technische Details

Framework:      <Framework>
Dateigroesse:   <X> Zeilen Python
Hauptdatei:     <main.py>

---
*Analyse erstellt: <Datum>*
```

---

## Fase 2: Verificação da qualidade do código

**Objetivo:** Garantir a qualidade técnica e identificar problemas conhecidos.

### Verificações recomendadas

| Teste | Ferramenta | Descrição |
|------|----------|--------------|
| **Codificação** | Verificador de codificação (ex.: `chardet`, `file`) | Garantir UTF-8 |
| **Análise de métodos** | Linter (ex.: `pylint`, `flake8`) | Encontrar métodos grandes |
| **Indentação** | Formatador (ex.: `black`, `autopep8`) | Verificar consistência |
| **Importações** | Verificador de importações (ex.: `isort`, `pylint`) | Encontrar importações não utilizadas |

### Pontos de verificação

- [ ] Todos os arquivos .py estão codificados em UTF-8?
- [ ] Não há métodos incomumente grandes (>100 linhas)?
- [ ] Indentação consistente (espaços vs. tabulações)?
- [ ] Importações não utilizadas removidas?
- [ ] Docstrings presentes?

### Documentar o resultado

Registrar os problemas em AUFGABEN.txt na seção "QUALITAETSPRUEFUNG".

---

## Fase 3: Criar AUFGABEN.txt

**Objetivo:** Registrar as tarefas pendentes de forma estruturada.

**Criar arquivo:** `AUFGABEN.txt` na pasta do projeto

### Modelo

```
AUFGABEN - <ToolName> V<Version>
==============================
Status: <Status>
Stand: <Datum>

OFFENE AUFGABEN:
[ ] <Aufgabe 1> - Aufwand: <NIEDRIG|MITTEL|HOCH>
[ ] <Aufgabe 2> - Aufwand: <NIEDRIG|MITTEL|HOCH>

---
ERLEDIGT (Archiv):
- <Erledigte Aufgabe> (<Version>, <Datum>)
```

### Valores de status

| Status | Significado |
|--------|-----------|
| NEU ENTDECKT | Ainda não analisado |
| ANALYSE NOETIG | Análise de funcionalidades em andamento |
| QUALITAETSPRUEFUNG | Testes de código em andamento |
| VALIDIERT & BEREIT | Pronto para funcionalidades |
| MVP | Produto Mínimo Viável |
| NUR KOMPILIEREN | Só falta compilar |
| GESPERRT | Aguardando teste/decisão do usuário |

---

## Fase 4: Integração com o sistema de gestão de tarefas

Após concluir as fases 1–3:

1. **Transferir tarefas:** Criar tarefas/issues a partir das entradas de AUFGABEN.txt
2. **Verificar:** Todas as tarefas estão categorizadas corretamente?
3. **Categorização:** Classificar o projeto na categoria adequada (Ferramenta única, Suíte, Biblioteca etc.)

### Tarefas automáticas de integração

Para novos projetos, criar as seguintes tarefas padrão:

| Tarefa | Atividade | Esforço |
|------|---------|---------|
| onb_1 | Criar análise de funcionalidades | médio |
| onb_2 | Verificação da qualidade do código | baixo |
| onb_3 | Criar AUFGABEN.txt | baixo |

As tarefas têm dependências: onb_2 depende de onb_1, onb_3 depende de onb_2.

---

## Lista de verificação rápida

```
[ ] 1. Feature_Analyse_<Name>.md erstellt
[ ] 2. Code-Qualitaetspruefung durchgefuehrt (Linter, Encoding, Imports)
[ ] 3. AUFGABEN.txt erstellt mit Status
[ ] 4. Tasks in Task-Management uebernommen
```

---

## Exemplo: Nova ferramenta "MyTool"

```bash
# 1. Feature-Analyse
# -> Feature_Analyse_MyTool.md erstellen (siehe Template)

# 2. Code-Qualitaet
pylint MyTool/main.py
flake8 MyTool/main.py
file -i MyTool/main.py  # Encoding pruefen

# 3. AUFGABEN.txt
# -> Im Tool-Ordner erstellen mit Status "QUALITAETSPRUEFUNG"

# 4. Tasks anlegen
# -> Eintraege aus AUFGABEN.txt als Issues/Tickets erfassen
```

---

*Criado: 2026-01-10 | Adaptado: 2026-03-12*
