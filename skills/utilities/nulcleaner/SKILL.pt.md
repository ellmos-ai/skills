---
name: nulcleaner
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Encontra e exclui arquivos NUL reservados do Windows, criados pelo uso de /dev/null no Git Bash. Sem interface gráfica ou com GUI."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [windows, nul, cleanup, git-bash, filesystem]
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
  origin_path: "system/tools/nulcleaner.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 684d3a24e9aa64d125877cb5f27fc613d89bcf44a2f5e213ea1b65d91cc44a39
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.033613+00:00"
---
<img src="banner.png" width="100%" alt="nulcleaner banner">

# nulcleaner - Limpeza de arquivos NUL do Windows

## O problema

Quando `/dev/null` é usado em comandos no Git Bash sob Windows (por exemplo, `> /dev/null`),
em vez de um redirecionamento para o nada, é criado um arquivo real chamado **`nul`** no diretório
atual. O Windows reserva "NUL" como nome de dispositivo, por isso esses arquivos não podem ser
excluídos normalmente.

Esta ferramenta encontra e exclui esses arquivos NUL usando o caminho UNC estendido (`\\?\`).

---

## Modos

| Modo | Descrição |
|-------|-------------|
| `scan` | Pesquisa recursivamente um diretório por arquivos NUL |
| `delete` | Encontra e exclui arquivos NUL |
| `gui` | Interface gráfica com seleção de arquivos |

---

## Uso da CLI

```bash
# Nur scannen (zeigt gefundene NUL-Dateien)
python nulcleaner.py scan /pfad/zum/verzeichnis

# Scannen und loeschen
python nulcleaner.py delete /pfad/zum/verzeichnis

# GUI-Modus starten
python nulcleaner.py gui
```

---

## API headless (para integração)

A ferramenta também oferece uma API em Python para operação headless:

```python
from nulcleaner import clean_nul_files_headless

result = clean_nul_files_headless("/pfad/zum/verzeichnis", verbose=True)
print(f"Gefunden: {result['found']}, Geloescht: {result['deleted']}")
```

**Retorno:** `{'found': int, 'deleted': int, 'errors': list}`

---

## Detalhes técnicos

- Usa o caminho UNC estendido (`\\?\`) para excluir nomes de arquivo reservados pelo Windows
- Varredura recursiva com `os.walk()`
- GUI com tkinter (sem dependências externas)
- Funciona apenas no Windows (onde o problema ocorre)

---

## Prevenção

O ideal é evitar `/dev/null` no Git Bash. Em vez disso:
- Simplesmente omita a saída
- Use `2>&1` para redirecionar o stderr
- Em scripts de shell, atente-se à compatibilidade com o Windows
