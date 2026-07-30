---
name: migrate-rename
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Renombrado evolutivo de archivos con archivos wrapper. Permite renombrar sin interrupciones drásticas: las referencias se actualizan orgánicamente con el uso.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="migrate-rename banner">

> **Español** — Versión oficial en español de `migrate-rename`.


# Renombrado de archivos con Wrappers (Migración Evolutiva) (Español)

> Permite renombrar archivos SIN interrupciones drásticas. Las referencias se actualizan orgánicamente mediante el uso diario.

---

## Principio: Migración Evolutiva

```
ANTES:                           DESPUÉS:
old_file.md                      new_file.md (renombrado)
   |                                |
   +-- Referencia A                 +-- old_file.md (wrapper)
   +-- Referencia B                        |
   +-- Referencia C                        +-- Tabla de registro
                                           +-- Instrucciones
                                           +-- Enlace a new_file.md
```

Cuando alguien accede a la ruta antigua:
1. Llega al archivo wrapper
2. Añade una entrada al registro
3. Corrige la referencia que le llevó allí
4. Continúa hacia el archivo real

---

## Paso a paso

### 1. Renombrar el archivo

```bash
mv old_file.md new_file.md
```

### 2. Crear archivo Wrapper

Crea `old_file.md` con el siguiente contenido:

```markdown
# OLD_FILE.md - REDIRIGIDO (Español)

**Estado:** Este archivo ha sido renombrado a `new_file.md`

---

## Registro de migración

| Fecha | Quién | Origen | ¿Referencia corregida? |
|-------|-------|--------|-----------------------|
| AAAA-MM-DD | [Nombre] | Migración inicial | n/a (wrapper creado) |

---

## Instrucciones

1. **Deja una entrada en el registro** (en la tabla superior)
2. **Comprueba el origen**: ¿Qué te envió aquí?
3. **Corrige la referencia**: Cambia `old_file.md` -> `new_file.md`
4. **Ve al archivo real**: [new_file.md](new_file.md)

---

**Archivo de destino:** [new_file.md](new_file.md)
```

### 3. Corregir inmediatamente referencias críticas
- Archivos de ayuda (documentación principal)
- Referencias de prompts del sistema
- Código CLI que usa directamente la ruta

### 4. Migrar referencias restantes evolutivamente
El resto se corrige automáticamente a través del uso.

---

## ¿Cuándo usar el método Wrapper?

**SÍ - Wrapper útil:**
- Muchas referencias potenciales
- El archivo es referenciado por varios socios/herramientas
- No es un archivo de sistema crítico

**NO - Cambiar todo directamente:**
- Pocas referencias conocidas
- Archivos críticos del sistema (configuración, esquema BD)
- Rutas críticas para el rendimiento

---

## Limpieza

Después de aproximadamente 30 días o cuando el registro no muestre nuevas entradas:
1. Mover el archivo wrapper a `_archive/deprecated/`
2. O eliminarlo completamente (si no hay más entradas)

---

## Historial de Cambios

### 1.0.0 (2026-03-15)
- Adaptado desde BACH v3.8.0

---

*Adaptado desde BACH v3.8.0 | Versión independiente*