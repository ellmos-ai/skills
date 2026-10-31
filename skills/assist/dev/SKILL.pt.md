---
name: dev
version: 0.1.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-06-22
description: "Assistente de desenvolvedor (sucessor do ATI). Fornece uma visão geral rápida do projeto por meio de uma varredura headless e encaminha para as ferramentas de codificação disponíveis: CodeCommander MCP (análise/refatoração/diagnóstico) e o módulo ellmos-code-tools. Apenas roteamento de ferramentas + varredura, sem armazenamento próprio."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [dev, coding, projekt-scan, ati, codecommander]
language: pt
status: active
visibility: public
dependencies: {'tools': ['dev_core.py'], 'services': [], 'protocols': [], 'python': ['pathlib'], 'external': ['codecommander-mcp', 'ellmos-code-tools']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/ati/ + system/agents/entwickler/', 'origin_version': 'n/a', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: e0c349589cfe3b0cf418f3deb24b7fb097d45ef52358ad19a4958a96d7f5a0ef
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:35:20.792687+00:00"
---
<img src="banner.png" width="100%" alt="dev banner">

# Dev — Assistente de Desenvolvedor (ATI)

Fornece uma visão geral e, em seguida, encaminha para as ferramentas adequadas.

## Finalidade

Sucessor do agente ATI/entwickler do BACH. Duas tarefas:
1. **Varredura do projeto** (headless, stdlib): visão geral rápida e econômica em tokens da
   estrutura, das linguagens e dos marcadores de build de um projeto — antes que uma análise custosa seja executada.
2. **Roteamento de ferramentas:** encaminha para as ferramentas de codificação existentes, em vez de duplicá-las.

## Gatilhos

| Entrada do usuário | Ação |
|---|---|
| „Dê-me uma visão geral do projeto X" | `dev_core.py scan <pfad>` |
| „O que é este projeto / qual é a stack?" | `dev_core.py scan <pfad>` |
| „Analise este arquivo / refatore" | → CodeCommander-MCP |
| „Gere/verifique código Python" | → CodeCommander-MCP / ellmos-code-tools |

## Cenário de ferramentas (destinos de roteamento)

- **CodeCommander-MCP** (`.AI/.MCP/ellmos-codecommander-mcp`): `cc_analyze_code`,
  `cc_analyze_methods`, `cc_extract_classes`, `cc_diagnose_imports`,
  `cc_runtime_import_diagnose`, `cc_generate_python_code`, `cc_check_indentation` e outras.
- **ellmos-code-tools** (`.AI/.MODULES/ellmos-code-tools`): ferramentas de desenvolvimento CLI (edição estrutural, contexto pycutter, analisador de métodos).
- **FileCommander-MCP**: operações de arquivos/diretórios sobre árvores grandes.

## Entrada CLI (dev_core.py)

```bash
python dev_core.py scan .              # aktuelles Projekt
python dev_core.py scan /pfad/projekt  # Struktur + Sprachen + Marker
```

Detecta, entre outros: Python (pyproject/requirements/setup), Node/TypeScript, Rust, Go,
Java, Roblox (Rojo), Docker, repositório Git.

## Armazenamento

Sem armazenamento. Apenas varredura + roteamento.

## Postura

Recomendamos CodeCommander/ellmos-code-tools como ferramentas de codificação, mas estamos abertos
a outras (por exemplo ruff/pylint/eslint), caso o usuário prefira.

## Privacidade

- `dev_core.py` lê apenas nomes de arquivos/diretórios (estrutura), sem conteúdo e sem upload.
- São ignorados, entre outros, `.git`, `node_modules`, `.venv`, `__pycache__`.

## Recursos relacionados

- `assist/AGENTS.md` — roteador guarda-chuva
- `.AI/.MCP/ellmos-codecommander-mcp` · `.AI/.MODULES/ellmos-code-tools`

## Registro de alterações

### 0.1.0 (2026-06-22)
- Versão inicial. Sucessor do ATI/entwickler: varredura headless do projeto (stdlib) +
  roteamento para CodeCommander-MCP / ellmos-code-tools. Neutro quanto ao usuário, sem armazenamento.
