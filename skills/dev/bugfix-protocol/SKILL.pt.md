---
name: bugfix-protocol
version: 1.0.0
type: protocol
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Protocolo sistemático de depuração em 6 fases. Abordagem estruturada para bugs com verificações rápidas, testes isolados, regra dos 20 minutos e modelo de relatório de bug."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [debugging, bugfix, protocol, python, pyqt6, systematic]
language: pt
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/bugfix-protokoll.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 5deea0b6bd5cb1acc3495ebe481c63468b2231bb09d3e15f3da8163dde433e40
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.698958+00:00"
---
<img src="banner.png" width="100%" alt="bugfix-protocol banner">

# Protocolo de Correção de Bugs: Depuração Sistemática em 6 Fases

Abordagem estruturada para bugs — da análise dos sintomas até a verificação.
Evita tentativas aleatórias e garante que as correções sejam duradouras.

---

## Visão Geral

| Fase | Nome | Objetivo | Tempo Máx. |
|------|------|----------|------------|
| 1 | Verificações Rápidas | Descartar causas óbvias | 2 min |
| 2 | Diagnóstico | Localizar a causa | 10 min |
| 3 | Teste Isolado | Tornar o bug reproduzível | 5 min |
| 4 | Correção | Correção mínima | 10 min |
| 5 | Verificação | Testar a correção + efeitos colaterais | 5 min |
| 6 | Documentação | Registrar o conhecimento | 2 min |

**Regra dos 20 minutos:** Se não houver progresso após 20 minutos → mudar de abordagem ou pedir ajuda.

---

## Fase 1: Verificações Rápidas (2 min)

Antes de se aprofundar — verifique as causas mais comuns:

### Lista de verificação

- [ ] **Erro de sintaxe?** Ler a mensagem de erro com atenção, verificar a linha
- [ ] **Erro de importação?** Módulo instalado? Nome correto? Importação circular?
- [ ] **Erro de digitação?** Nomes de variáveis/funções corretos?
- [ ] **Tipo de dado incorreto?** String em vez de int? None onde se esperava um objeto?
- [ ] **Cache desatualizado?** Excluir `__pycache__`, reiniciar
- [ ] **Ambiente incorreto?** O venv correto está ativo? Versão correta do Python?
- [ ] **Codificação?** UTF-8 vs. cp1252 (clássico do Windows)

### Ações rápidas

```bash
# Cache leeren
find . -name "__pycache__" -type d -exec rm -rf {} + 2>&1
find . -name "*.pyc" -delete 2>&1

# Imports pruefen
python -c "import modulname"

# Syntax pruefen
python -m py_compile datei.py
```

---

## Fase 2: Diagnóstico (10 min)

### Estratégia: de fora para dentro

1. **Analisar a mensagem de erro** — ler o traceback de baixo para cima
2. **Verificar as últimas alterações** — `git diff`, `git log --oneline -10`
3. **Usar ferramentas de diagnóstico** — Utilizar ferramentas de diagnóstico próprias, conforme o projeto

### Ferramentas de diagnóstico (exemplos)

Dependendo do projeto, scripts de diagnóstico especializados podem ser úteis:

| Ferramenta | Finalidade |
|------------|------------|
| `import_diagnose.py` | Analisar problemas de importação |
| `method_analyzer.py` | Verificar assinaturas de métodos |
| `env_checker.py` | Validar variáveis de ambiente/caminhos |

> **Observação:** Criar ferramentas de diagnóstico próprias conforme o projeto ou usar
> as ferramentas já existentes. O importante é a abordagem sistemática, não a
> ferramenta específica.

### Técnicas de depuração

```python
# 1. Print-Debugging (schnell aber effektiv)
print(f"DEBUG: variable={variable!r}, type={type(variable)}")

# 2. Breakpoint (interaktiv)
breakpoint()  # Python 3.7+

# 3. Traceback erweitern
import traceback
traceback.print_exc()

# 4. Logging statt Print
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug(f"State: {state!r}")
```

---

## Fase 3: Teste Isolado (5 min)

### Exemplo Mínimo Reproduzível (MRE)

Objetivo: reproduzir o bug com o mínimo de código.

```python
# test_bug.py — Minimaler Reproduktions-Test
"""
Bug: [Kurze Beschreibung]
Erwartet: [Was sollte passieren]
Tatsaechlich: [Was passiert stattdessen]
"""

# Minimaler Setup
# ... nur das Noetigste

# Bug-Ausloeser
# ... exakter Code der den Bug triggert

# Erwartetes Ergebnis
# assert result == expected, f"Got {result}"
```

### Estratégias de isolamento

1. **Novo arquivo:** reproduzir o bug em um arquivo próprio
2. **Remover dependências:** uma por vez, até o bug desaparecer
3. **Dividir ao meio:** dividir o bloco de código ao meio e verificar qual metade contém o bug
4. **Git Bisect:** `git bisect start`, `git bisect bad`, `git bisect good <commit>`

---

## Fase 4: Correção (10 min)

### Princípios

1. **Mínima:** alterar o mínimo possível
2. **Compreender:** nunca corrigir às cegas — entender POR QUE está quebrado
3. **Uma coisa só:** uma correção por commit, não vários problemas ao mesmo tempo
4. **Compatível com versões anteriores:** não quebrar funcionalidades existentes

### Padrões de correção

```python
# SCHLECHT: Symptom behandeln
try:
    result = broken_function()
except:  # Alles schlucken
    result = default_value

# GUT: Ursache beheben
def broken_function():
    if input_data is None:  # Eigentliche Ursache: None-Check fehlte
        return default_value
    return process(input_data)
```

### Categorias comuns de correção

| Categoria | Correção típica |
|-----------|-----------------|
| None/Null | Cláusula de guarda: `if x is None: return default` |
| Erro de índice | Verificação de limites: `if i < len(lst)` |
| Erro de tipo | Conversão explícita: `str(x)`, `int(x)` |
| Erro de importação | Corrigir o caminho, instalar o pacote |
| Codificação | Especificar UTF-8 explicitamente: `encoding='utf-8'` |
| Condição de corrida | Lock/Mutex, ou alterar a ordem |
| Bug de estado | Verificar a inicialização, inserir um reset |

---

## Fase 5: Verificação (5 min)

### Lista de verificação

- [ ] **Bug corrigido:** o problema original não ocorre mais
- [ ] **MRE aprovado:** o teste isolado passa
- [ ] **Sem regressão:** os testes existentes continuam passando
- [ ] **Casos limite:** entrada vazia, None, dados grandes testados
- [ ] **Ferramentas do projeto:** verificar no diretório de ferramentas do projeto se há ferramentas relevantes de teste/validação

### Comandos de teste

```bash
# Unit-Tests
python -m pytest tests/ -v

# Nur betroffene Tests
python -m pytest tests/test_modul.py -v -k "test_name"

# Type-Check
python -m mypy datei.py

# Lint
python -m flake8 datei.py
```

---

## Fase 6: Documentação (2 min)

### Modelo de relatório de bug

```markdown
## Bug-Report: [Kurztitel]

**Datum:** YYYY-MM-DD
**Schwere:** kritisch / hoch / mittel / niedrig
**Komponente:** [Modul/Datei]

### Symptom
[Was der User sieht / Fehlermeldung]

### Ursache
[Technische Root-Cause]

### Fix
[Was geaendert wurde + warum]

### Betroffene Dateien
- `datei1.py` — [Aenderung]
- `datei2.py` — [Aenderung]

### Praevention
[Wie kann dieser Bug-Typ in Zukunft vermieden werden?]
```

### Formato da mensagem de commit

```
fix: [Kurze Beschreibung des Fixes]

Ursache: [Root-Cause in einem Satz]
Fix: [Was geaendert wurde]
Test: [Wie verifiziert]
```

---

## Depuração de PyQt6 / GUI — Armadilhas comuns

> Esta seção é relevante para projetos de GUI desktop com PyQt6/PySide6.

### As 5 principais armadilhas do PyQt6

| Armadilha | Problema | Solução |
|-----------|----------|---------|
| **Desconexão de sinal-slot** | Sinal conectado, mas o handler não é executado | `print` no handler, verificar a assinatura |
| **Segurança de threads** | Atualização da GUI a partir de thread worker | `QMetaObject.invokeMethod` ou usar sinal |
| **Cascata de layout** | Widget invisível/posicionado incorretamente | `widget.show()`, verificar a hierarquia de layouts |
| **Bloqueio do event loop** | A GUI trava | Mover operações longas para QThread |
| **Coleta de lixo** | Widget desaparece de repente | Manter a referência como `self.widget` |

### Auxiliares de depuração para PyQt6

```python
# Widget-Hierarchie ausgeben
def dump_widget_tree(widget, indent=0):
    print(" " * indent + f"{widget.__class__.__name__}: {widget.objectName()}")
    for child in widget.findChildren(QWidget):
        if child.parent() == widget:
            dump_widget_tree(child, indent + 2)

# Signal-Debugging
from PyQt6.QtCore import QObject
original_connect = QObject.connect
def debug_connect(self, *args, **kwargs):
    print(f"CONNECT: {self.__class__.__name__} -> {args}")
    return original_connect(self, *args, **kwargs)
```

---

## Referência Rápida

```
BUG GEFUNDEN?
     │
     ▼
[Phase 1: Schnell-Checks]  ──── Offensichtlich? → FIX
     │
     ▼
[Phase 2: Diagnose]  ────────── Ursache klar? → Phase 4
     │
     ▼
[Phase 3: Isolierter Test]  ── Reproduzierbar? → Phase 4
     │                              │
     │                         Nicht reproduzierbar?
     │                              │
     │                         Logging einbauen,
     │                         auf erneutes Auftreten warten
     ▼
[Phase 4: Fix]  ─────────────── Minimal + verstanden
     │
     ▼
[Phase 5: Verifikation]  ────── Tests gruen? → Phase 6
     │                              │
     │                         Tests rot? → Zurueck zu Phase 4
     ▼
[Phase 6: Dokumentation]  ───── Bug-Report + Commit
```

### Regra dos 20 minutos

Se você travar por 20 minutos:

1. **Mudar de abordagem** — experimentar outra técnica de depuração
2. **Rubber Duck** — explicar o problema em voz alta (ou escrevê-lo)
3. **Pausa** — afastar-se por 5 minutos e voltar com um olhar fresco
4. **Pedir ajuda** — perguntar a um colega, Stack Overflow, documentação
5. **Recomeçar** — `git stash`, começar completamente do zero
