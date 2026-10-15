---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "Reestruturar hierarquias de pastas aninhadas em estruturas planas e legíveis por máquina. Baseado em Bash, com lógica de mesclagem inteligente."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [ordner, flattening, filesystem, bash, reorganisation, cleanup]
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
  origin_path: "system/skills/workflows/ordner-flattening.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ecd288c18790f209ab63e3b72bc81cf748f957b27068f37a9a4999740f4392b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.387946+00:00"
---
<img src="banner.png" width="100%" alt="folder-flattening banner">

# Fluxo de trabalho: Achatamento de pastas

Objetivo: Converter estruturas de pastas aninhadas em uma estrutura plana e legível por máquina.
Vantagem: Não é mais necessário navegar clicando, mas pesquisar por meio de banco de dados (Verzeichnis.db).
Duplicatas são permitidas quando fizer sentido tematicamente.

---

## Visão geral das fases

| Fase | O que acontece | Seção do script |
|------|----------------|-----------------|
| 1 | Achatar: Mover todas as subpastas para um único nível | `phase_flatten` |
| 2 | Encurtar: Reduzir nomes de caminho longos ao último segmento, mesclando em caso de conflitos | `phase_shorten` |
| 3 | Limpar: Resolver sublinhados múltiplos (`___`) e remover `_` finais | `phase_cleanup_underscores` |
| 4 | Agrupar: Pastas numéricas, pastas de CD e nomes curtos em pastas coletivas | `phase_group_problematic` |
| 5 | Análise de tripletos: Grupos deslizantes de 3, nome mais curto como destino da mesclagem | `phase_tripel_merge` |
| 6 | Mesclagem por formato de mídia: Agrupar pastas por tipo de arquivo (modelo) | `phase_media_merge` |
| 7 | Organizar: Excluir pastas vazias | `phase_cleanup_empty` |

---

## Regras importantes

### Correspondência na análise de tripletos
- **Substring**: `Aufklaerung` em `Aufklaerungsbroschueren` -> mesclar em `Aufklaerung`
- **Plural/Umlaut**: `Raum` = `Raeume`, `Teil` = `Teile`, `Buch` = `Buecher`
- **Primeira palavra**: `Autismus ADHS` corresponde a `Autismus Beruf` (mesmo início)

### Comprimento mínimo
- Nome de uma palavra sem espaços: **no mínimo 8 caracteres** (evita `Hand`, `Haus`, `Form`)
- Com espaços (p. ex. `ICF Katalog`): **a partir de 3 caracteres é aceitável**
- Assim, `ICF`, `ASS Frauen` etc. continuam permitidos

### Reinício após a mesclagem
Após cada mesclagem, a lista de pastas é recarregada e o processo recomeça no destino da mesclagem.
Assim, por exemplo, `Autismus` reúne todas as extensões antes de prosseguir.

---

## Mesclagem por formato de mídia (sistema de modelos)

A fase 6 usa um array de modelos `MEDIA_TYPES`. Cada entrada define:
- Pasta de destino (com o prefixo `_`)
- Extensões de arquivo que pertencem a esse tipo

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Bilder|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Erweiterbar:
    # "_Tabellen|xlsx|xls|csv|ods"
    # "_Prasentationen|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

Somente pastas que contenham **exclusivamente** arquivos de um tipo são movidas.
Pastas com subpastas são ignoradas.

### Adicionar um novo tipo de mídia

Basta acrescentar uma nova linha ao array `MEDIA_TYPES`:
```bash
"_Zielordner|ext1|ext2|ext3"
```

---

## Execução

```bash
# Kompletter Durchlauf:
cd /pfad/zum/zielverzeichnis
bash ordner_flattening_komplett.sh

# Oder einzelne Phasen:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## Valores empíricos da sessão de 26.01.2026

- Início: 206 pastas + 252 arquivos soltos, ~5600 subpastas aninhadas
- Após o achatamento: ~2200 pastas em um único nível
- Após encurtar + limpar: ~2005 pastas
- Após agrupar (números, CDs): ~2005 -> pasta coletiva criada
- Após tripletos v1: ~1561 pastas
- Após tripletos v2 (regra de 8 caracteres): redução adicional
- Fase de formato de mídia: pastas de Áudio/Vídeo/Imagens consolidadas
