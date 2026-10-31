---
name: encoding-fix
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Reparação de mojibake para UTF-8 codificado duas/três vezes. Corrige interpretações incorretas de Windows cp1252/Latin-1. Sem dependências."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [encoding, utf-8, mojibake, windows, cp1252, text-repair]
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
  origin_path: "system/tools/encoding_fix.py"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c637d841765295aae889df92b106b3dfa66071f13ab32be04e1d1cfe21520d56
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:47.120221+00:00"
---
<img src="banner.png" width="100%" alt="encoding-fix banner">

# Correção de Codificação

Repara mojibake (UTF-8 codificado duas/três vezes) causado por uma interpretação incorreta como Windows cp1252/Latin-1. Zero dependências — apenas a biblioteca padrão do Python.

## Problema Típico

```
"ue" (U+00FC) → UTF-8 \xc3\xbc → als cp1252 gelesen → "Ã¼"
```

## Utilização

### Como Biblioteca
```python
from encoding_fix import sanitize_outbound

clean = sanitize_outbound("WÃ¼rge")  # → "Würge"
```

### Saída de Subprocesso
```python
from encoding_fix import sanitize_subprocess_output

text = sanitize_subprocess_output(process.stdout)
```

### CLI
```bash
python encoding_fix.py "WÃ¼rge"    # Einzelnen String prüfen
python encoding_fix.py              # Selbst-Test
```

## Funcionalidades

- **Idempotente:** Texto já corretamente codificado não é alterado
- **Até 3 rodadas:** Repara também strings codificadas três vezes
- **Decodificador de subprocesso:** Fallback UTF-8/cp1252 para a saída de processos
- **Zero dependências:** Apenas a biblioteca padrão do Python

## Registo de Alterações

### 1.0.0 (2026-03-12)
- Portado de BACH system/tools/encoding_fix.py
