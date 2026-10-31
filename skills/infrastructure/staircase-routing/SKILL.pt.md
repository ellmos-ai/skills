---
name: staircase-routing
version: 1.0.0
type: skill
author: Lukas Geiger + Gemini (Antigravity)
created: 2026-07-29
updated: 2026-07-29
description: "Estratégia autônoma de navegação e roteamento que percorre hierarquias de diretórios para cima e para baixo em busca de documentos-guia como CLAUDE.md, AGENTS.md, README.md e RULES.md, bem como de palavras-chave configuráveis pelo usuário. A configuração é feita por meio de staircase-config.json ou config.json. Também conhecida como Up-and-Down Routing ou Walking Bass Routing."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: false
category: infrastructure
tags: [routing, staircase-routing, up-and-down-routing, walking-bass-routing, signpost, navigation, directory-traversal]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
translated_from_sha256: 28ec74023759355f5a974506a065cb0c737455ec4d3d59d23129276e63011200
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---

<img src="banner.png" width="100%" alt="staircase-routing banner">

# Staircase-Routing (Up-and-Down / Walking Bass Routing)

A skill **Staircase-Routing**, também chamada *Up-and-Down Routing* ou *Walking Bass
Routing*, encapsula a estratégia de verificação de documentos de diretório
para agentes de IA.

Quando um agente entra em um diretório ou trabalha em um arquivo, ele usa esta
estratégia para encontrar contexto, regras e documentos-guia relevantes antes
de alterar código ou executar uma ação.

---

## 1. Padrões de documentos-guia

Por padrão, o Staircase-Routing procura estes documentos-guia:

- **Controle global e de projeto:** `CLAUDE.md`, `AGENTS.md`,
  `START.md`, `RULES.md`
- **Visão geral do projeto e tarefas:** `README.md`, `TODO.md`, `NOTIZ.md`,
  `BEWEISNOTIZ.md`
- **Palavras-chave definidas pelo usuário:** configuradas por meio de
  `staircase-config.json` ou `config.json`.

---

## 2. Algoritmo de percurso

```text
                           [ Root- / Workspace-Ebene ]
                           ┌────────────────────────┐
                           │   CLAUDE.md / RULES.md │ ◄── (Schritt 2: Root-Wegweiser lesen)
                           └───────────▲────────────┘
                                       │ (Treppe aufwärts)
                           ┌───────────┴────────────┐
                           │ Unterordner / Ziel     │ ◄── (Schritt 1: Im CWD beginnen)
                           └───────────┬────────────┘
                                       │ (Treppe abwärts)
                           ┌───────────▼────────────┐
                           │ Kind- / Modulordner    │ ◄── (Schritt 3: Untergeordnete Wegweiser finden)
                           │   module-rules.md      │
                           └────────────────────────┘
```

### Passo 1: Verificar o diretório de trabalho atual (CWD)

- Verifique o diretório do arquivo de destino ou o diretório de trabalho ativo.
- Se houver documentos-guia, leia-os imediatamente.

### Passo 2: Percorrer para cima

- Se **nenhum** documento-guia for encontrado no CWD, suba para o diretório
  pai (`..`).
- Repita esse processo progressivamente para cima até encontrar um documento-guia
  raiz (`CLAUDE.md` ou `AGENTS.md`) ou atingir o limite do workspace.
- Leia todos os documentos-guia raiz encontrados para identificar diretrizes globais e
  regras do projeto.

### Passo 3: Verificar para baixo

- A partir do diretório raiz identificado, desça para os subdiretórios
  relevantes para a tarefa.
- Encontre e leia documentos-guia especializados em nível de módulo, regras de domínio
  ou configurações de componentes.

---

## 3. Palavras-chave configuráveis pelo usuário (`staircase-config.json`)

Os agentes podem ler um `staircase-config.json` local ou global para personalizar
os documentos-guia procurados:

```json
{
  "signpost_filenames": [
    "CLAUDE.md",
    "AGENTS.md",
    "START.md",
    "RULES.md",
    "README.md",
    "TODO.md"
  ],
  "custom_buzzwords": [
    "SECURITY",
    "POLICY",
    "GOVERNANCE",
    "PIPELINE"
  ],
  "max_upward_depth": 10,
  "exclude_directories": [
    "node_modules",
    ".git",
    "__pycache__",
    "dist",
    "build",
    "archive"
  ]
}
```

---

## 4. Integração com `letter-hooker` e tarefas agendadas

`staircase-routing` está incorporado como bootloader central de verificação
prévia na skill **`letter-hooker`** e na tarefa agendada
**`antigravity-kontext-and-workflow-loader-and-divider`**. Assim, os agentes
encontram e seguem os documentos-guia antes de iniciar qualquer alteração.
