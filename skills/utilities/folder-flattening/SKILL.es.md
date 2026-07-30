---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Reestructura jerarquías de carpetas anidadas en diseños planos y legibles por máquina. Basado en Bash con lógica de fusión inteligente.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [folder, flattening, filesystem, bash, reorganization, cleanup]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ordner-flattening.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `folder-flattening`.

# Flujo de trabajo: Folder Flattening

Objetivo: Convertir estructuras de carpetas anidadas en una estructura plana y legible por máquina.
Ventaja: No más navegación manual por directorios — búsqueda mediante base de datos (`Verzeichnis.db`) en su lugar.
Se permiten duplicados cuando tengan sentido temático.

---

## Descripción general de las fases

| Fase | Qué sucede | Sección del script |
|-------|-------------|----------------|
| 1 | Aplanar (Flatten): Mover todas las subcarpetas a un solo nivel | `phase_flatten` |
| 2 | Acortar (Shorten): Truncar nombres de ruta largos al último segmento, fusionar en caso de conflicto | `phase_shorten` |
| 3 | Limpieza: Resolver guiones bajos múltiples (`___`), eliminar `_` final | `phase_cleanup_underscores` |
| 4 | Agrupar: Mover carpetas numéricas, carpetas de CD y nombres cortos a carpetas de colección | `phase_group_problematic` |
| 5 | Análisis de tripletes: Grupos deslizantes de 3, el nombre más corto como destino de fusión | `phase_tripel_merge` |
| 6 | Fusión por formato de medios: Consolidar carpetas según el tipo de archivo (plantilla) | `phase_media_merge` |
| 7 | Limpieza: Eliminar carpetas vacías | `phase_cleanup_empty` |

---

## Reglas importantes

### Coincidencia en el análisis de tripletes
- **Subcadena**: `Education` en `EducationalBrochures` -> fusionar en `Education`
- **Plural/Umlaut**: `Room` = `Rooms`, `Part` = `Parts`, `Book` = `Books`
- **Primera palabra**: `Autism ADHD` coincide con `Autism Career` (mismo inicio)

### Longitud mínima
- Nombre de una sola palabra sin espacios: **al menos 8 caracteres** (evita `Hand`, `House`, `Form`)
- Con espacios (p. ej., `ICF Catalog`): **a partir de 3 caracteres OK**
- Esto permite mantener `ICF`, `ASD Women`, etc.

### Reinicio tras la fusión
Tras cada fusión, la lista de carpetas se vuelve a cargar y se reinicia en el destino de la fusión.
De este modo, por ejemplo, `Autism` recopila todas las extensiones antes de continuar.

---

## Fusión por formato de medios (Sistema de plantillas)

La Fase 6 utiliza un arreglo de plantilla `MEDIA_TYPES`. Cada entrada define:
- Carpeta de destino (con prefijo `_`)
- Extensiones de archivo pertenecientes a este tipo

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Images|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Extensible:
    # "_Spreadsheets|xlsx|xls|csv|ods"
    # "_Presentations|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

Solo se mueven las carpetas que contienen **exclusivamente** archivos de un tipo.
Las carpetas con subcarpetas se omiten.

### Añadir un nuevo tipo de medio

Simplemente añada una nueva línea al arreglo `MEDIA_TYPES`:
```bash
"_TargetFolder|ext1|ext2|ext3"
```

---

## Ejecución

```bash
# Complete run:
cd /path/to/target/directory
bash ordner_flattening_komplett.sh

# Or individual phases:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## Valores de experiencia (Sesión 2026-01-26)

- Inicio: 206 carpetas + 252 archivos sueltos, ~5600 subcarpetas anidadas
- Tras aplanar: ~2200 carpetas en un solo nivel
- Tras acortar y limpiar: ~2005 carpetas
- Tras agrupar (números, CDs): ~2005 -> carpetas de colección creadas
- Tras triplete v1: ~1561 carpetas
- Tras triplete v2 (regla de 8 caracteres): reducción adicional
- Fase de formato de medios: Carpetas de audio/video/imágenes consolidadas