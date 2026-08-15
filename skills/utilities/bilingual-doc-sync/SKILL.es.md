---
name: bilingual-doc-sync
version: 1.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-07-03
updated: 2026-07-30
description: >
  Mantener sincronizadas las versiones lingüísticas paralelas de un documento (Paper DE/EN, README + README_de,
  SKILL.md + SKILL.en.md, textos de sitios web): actualizar la versión faltante,
  verificar el paralelismo de secciones, resolver divergencias, con una regla clara de idioma principal y
  transferencia inversa controlada cuando la versión secundaria resuelve algo mejor. Utilice esta habilidad
  al preguntar "¿están sincronizados DE y EN?", "actualiza la versión en inglés/alemán",
  "la traducción está desactualizada", en artículos/README/skills bilingües, o como un
  chequeo periódico de un inventario de documentos. También incluye la auditoría de expansión:
  evaluar si un proyecto/documento merece idiomas ADICIONALES (idoneidad i18n por
  público objetivo, preparación técnica, sin traducción masiva a ciegas).

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [übersetzung, zweisprachig, synchronisation, paper, readme, i18n, dokumentation]
language: es
status: active

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
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
---

<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">
# Bilingual-Doc-Sync — Sincronización de Versiones Lingüísticas Paralelas

## Propósito

Los documentos mantenidos en varios idiomas divergen sutilmente con el tiempo: la versión editada activamente
crece mientras la otra queda obsoleta, hasta que la "traducción" es cierta solo de nombre. Esta
habilidad convierte la verificación de sincronización en un flujo de trabajo definido con una decisión previa
crucial: **¿Qué versión es la principal?** Sin una regla de idioma principal, cada divergencia
se convierte en un debate caso por caso y la alineación deja de ser repetible.

## Flujo de Trabajo

### 1. Comprobación de Inventario

- ¿Están presentes ambas (o todas) las versiones lingüísticas? Si falta una por completo → **actualizar** (traducción
  completa de la versión principal, no una reescritura).
- Comprobar las convenciones de nomenclatura (ej. `DOCUMENTO.md` + `DOCUMENTO.en.md` o sufijos `_de`/`_en`)
  y alinear las desviaciones — la descubribilidad es la mitad de la sincronización.

### 2. Aclarar el Idioma Principal (antes de cada alineación)

- El idioma principal es la versión en la que se realiza principalmente el trabajo de contenido (a menudo EN en artículos científicos,
  idioma nativo en documentación local). Prevalece en caso de conflicto.
- **Excepción de transferencia inversa:** Si la versión secundaria resuelve algo demostrablemente mejor (redacción más clara,
  error corregido), se ADOPTA en la versión principal: transferir primero, luego
  sincronizar normalmente. Verificar la corrección técnica antes de adoptar una redacción "más bonita".

### 3. Verificar el Paralelismo

Estructura primero, luego contenido:

1. **Comparación de esquemas:** Secciones/encabezados de ambas versiones lado a lado:
   secciones faltantes, adicionales o reordenadas representan divergencias mayores.
2. **Muestreo sección por sección** del esquema coincidente: ¿las afirmaciones, números,
   referencias cruzadas y ejemplos son idénticos? Especialmente propensos a divergencias: changelogs, tablas,
   valores numéricos, listas de bibliografía/enlaces, secciones editadas recientemente.
3. **Comprobar invariantes no traducibles:** Bloques de código, identificadores, fórmulas y rutas
   deben ser IDÉNTICOS en ambas versiones (el código nunca se traduce).

### 4. Resolver Divergencias

- Resolver divergencias en dirección al idioma principal (o tras la transferencia inversa).
- Respetar la tipografía del idioma de destino (ej. convenciones de comillas).
- Actualizar metadatos: números de versión, campos de fecha, entradas del changelog en AMBAS
  versiones (el changelog en sí es el punto de divergencia más frecuente).

### 5. Documentar Resultados

Registrar los hallazgos (qué era divergente, qué se adoptó, qué se transfirió de vuelta).
Para una ejecución periódica sobre un inventario: combinar con la estructura de rotación
(`rotation-check`) — un par de documentos por ejecución, utilizando el registro como memoria.

## Extensión: Auditoría de Expansión (¿Deberían existir MÁS idiomas?)

Además de mantener sincronizadas las versiones existentes, el mantenimiento lingüístico implica preguntarse si un
documento/proyecto merece idiomas ADICIONALES:

1. **Evaluar la idoneidad** en lugar de traducir a ciegas: público objetivo, utilidad internacional,
   presencia en tiendas/web, portabilidad del contenido. No todo documento interno necesita inglés;
   no toda aplicación necesita cinco idiomas.
2. **Comprobar la preparación técnica:** ¿Está el sistema de destino preparado para archivos de idioma / versiones
   paralelas (estructura i18n, convención de nombres)? Si no es así, ESA es la primera
   tarea, no la traducción.
3. **Documentar hallazgos, no traducir masivamente de inmediato:** Colocar tareas de traducción concretas
   en el archivo TODO local del proyecto; "ningún otro idioma tiene sentido" es un resultado válido
   y digno de registrar.
4. **Control de calidad en versiones añadidas:** Realizar un muestreo de traducciones autogeneradas
   frente a la versión principal (Sección 3) antes de considerarlas "presentes".

## Ejemplo

```text
Tarea: "Comprobar si el artículo está sincronizado en DE y EN."

1. Inventario: paper_en.tex (principal) + paper_de.tex presentes.
2. Esquema: a DE le falta la nueva sección 4.2 (última revisión EN); DE tiene un
   mejor párrafo de demostración en 3.1.
3. Transferencia inversa: redacción de 3.1 verificada técnicamente → adoptada en EN.
4. Actualización: 4.2 traducido a DE; números en la Tabla 2 reconciliados (DE tenía
   valores obsoletos); bibliografía alineada de forma idéntica.
5. Entrada de registro: "paper-X | 2026-07-03 | de-en-sync | 3 divergencias resueltas,
   1 transferencia inversa | próxima comprobación tras la siguiente revisión EN".
```

## Banderas Red (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "Traduciré las diferencias de nuevo rápidamente" | Aclarar idioma principal + transferencia inversa primero — de lo contrario la mejor solución se sobrescribe. |
| "El esquema coincide, así que está sincronizado" | Números, changelogs y referencias divergen primero — el muestreo profundo es obligatorio. |
| "Traduciré los comentarios de código también" | Los bloques de código e identificadores permanecen idénticos en ambas versiones (inglés). |
| "Sincronizaré todos los documentos de una vez" | Un par por ejecución (estructura de rotación) mantiene la alineación verificable. |

## Habilidades Relacionadas

- `rotation-check` — Estructura para ejecuciones periódicas sobre un inventario de documentos.
- `workflow-extract` — Cuando esta comprobación deba configurarse como una automatización permanente.

## Registro de Cambios (Changelog)

### 1.1.0 (2026-07-03)
- Se añadió la auditoría de expansión (evaluar idoneidad i18n, preparación técnica, control de calidad para
  versiones añadidas) — integrada en lugar de una habilidad independiente i18n-coverage-audit
  (decisión de desduplicación).

### 1.0.0 (2026-07-03)
- Versión inicial. Abstraída de la automatización Codex
  "research-paper-de-en-synchronisationscheck", generalizada para cualquier versión lingüística
  paralela (artículos, README, habilidades, textos web).
