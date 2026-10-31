---
name: batch-file-ops
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Operações em lote com arquivos (excluir, mover, copiar, listar) usando padrões glob. Ferramenta de linha de comando para operações eficientes no sistema de arquivos. Sem dependências."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [batch, file-ops, glob, cli, filesystem, cleanup]
language: pt
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/tools/batch_file_ops.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6fd8057d502337926d541fe4b66208c94e661e7d8c83fe0a4847094e90c5e024
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.371367+00:00"
---
<img src="banner.png" width="100%" alt="batch-file-ops banner">

# batch_file_ops - Operações em lote com arquivos

Ferramenta de linha de comando para operações em lote eficientes em arquivos, com padrões glob.
Suporta: delete, move, copy, list. Zero dependências (apenas a biblioteca padrão do Python).

---

## Ações

| Ação | Descrição |
|--------|-------------|
| `delete` | Excluir arquivos conforme o padrão |
| `move` | Mover arquivos conforme o padrão |
| `copy` | Copiar arquivos conforme o padrão |
| `list` | Listar arquivos conforme o padrão |

## Uso da CLI

```bash
python batch_file_ops.py <aktion> <quelle> [<ziel>] --pattern "<glob>" [--dry-run] [--recursive]
```

### Argumentos

| Argumento | Descrição |
|----------|-------------|
| `aktion` | `delete`, `move`, `copy` ou `list` |
| `quelle` | Pasta de origem |
| `ziel` | Pasta de destino (somente para `move` e `copy`) |
| `--pattern`, `-p` | Padrão glob (por ex., `*.py`, `TOOLS_*.py`) - Padrão: `*` |
| `--dry-run`, `-n` | Apenas exibir, sem alterar nada |
| `--recursive`, `-r` | Pesquisar recursivamente em subpastas |

---

## Exemplos

```bash
# Alle Python-Dateien in einem Ordner auflisten
python batch_file_ops.py list /pfad/zum/ordner --pattern "*.py"

# Alle .tmp Dateien loeschen (erst Dry-Run!)
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp" --dry-run
python batch_file_ops.py delete /pfad/zum/ordner --pattern "*.tmp"

# Dateien verschieben
python batch_file_ops.py move /quelle /ziel --pattern "*.txt"

# Dateien kopieren (rekursiv)
python batch_file_ops.py copy /quelle /ziel --pattern "*.md" --recursive

# Pattern-Beispiele
python batch_file_ops.py delete /pfad --pattern "TOOLS_*.py"
python batch_file_ops.py list /pfad --pattern "backup_202?-*"
```

---

## Observações

- **Simulação primeiro:** Com `delete` e `move`, use sempre antes `--dry-run`
- **Padrões glob:** Utiliza `pathlib.glob()` / `pathlib.rglob()` do Python
- **Compatível com Windows:** Codificação de saída UTF-8 automática
- **Somente arquivos:** Pastas são ignoradas (apenas arquivos são processados)
