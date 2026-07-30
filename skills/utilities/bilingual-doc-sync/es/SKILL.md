---
language: es
---

> **Español** — Versión oficial en español de `bilingual-doc-sync`.

<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">

# Bilingual-Doc-Sync — Mantener sincronizadas versiones lingüísticas paralelas

## Resumen y propósito

Los documentos bilingües divergen progresivamente: la versión editada activamente crece mientras la otra queda desactualizada, hasta que la "traducción" solo lo es de nombre. Este skill convierte la verificación de sincronización en un proceso definido con una determinación previa fundamental: **¿Qué versión manda?** Sin una regla de idioma principal, cada divergencia se convierte en una decisión ad hoc y la sincronización resulta irrepetible.

## Flujo de trabajo

### 1. Evaluar inventario

- ¿Están presentes ambas (todas) las versiones lingüísticas? Si falta alguna por completo → **poner al día** (traducción completa de la versión principal, no una reescritura).
- Verificar las convenciones de nomenclatura (p. ej., `DOCUMENT.md` + `DOCUMENT.en.md` o sufijos `_de`/`_en`) y alinear las excepciones: la localizabilidad es la mitad de la sincronización.

### 2. Aclarar el idioma principal (antes de cada sincronización)

- El idioma principal es la versión en la que realmente se trabaja en el contenido (a menudo EN para artículos académicos, a menudo la lengua materna para documentación local). Prevalece en caso de conflicto.
- **Excepción de transferencia inversa:** Si la versión secundaria resuelve algo de forma demostrablemente mejor (formulación más clara, error corregido), se ADOPTA en la versión principal: primero realizar la transferencia inversa y luego sincronizar normalmente. Verificar la corrección técnica antes de adoptar una formulación "más pulida".

### 3. Verificar paralelismo

Estructura primero, luego contenido:

1. **Comparación de esquemas:** Secciones/encabezados de ambas versiones lado a lado: las secciones faltantes, adicionales o reordenadas son las divergencias principales.
2. **Muestreo por secciones** del esquema coincidente: ¿son idénticas las afirmaciones, números, referencias y ejemplos? Especialmente propensos a divergencias: changelogs, tablas, valores numéricos, bibliografías/listas de enlaces y secciones editadas recientemente.
3. **Verificar invariantes no traducibles:** Los bloques de código, identificadores, fórmulas y rutas deben ser IDÉNTICOS en ambas versiones (el código nunca se traduce).

### 4. Resolver

- Resolver divergencias en la dirección del idioma principal (o tras la transferencia inversa).
- Respetar la tipografía lingüística del idioma destino (en alemán diéresis reales ä ö ü ß, sin sustitución ae/oe/ue; convenciones de comillas).
- Actualizar metadatos: números de versión, campos de fecha, entradas del changelog en AMBAS versiones (el propio changelog es el punto de divergencia más frecuente).

### 5. Documentar

Registrar los resultados (qué era divergente, qué se adoptó, qué se transfirió de manera inversa).
Como ejecución periódica sobre un inventario: combinar con el marco de rotación (`rotation-check`) — un par de documentos por ejecución, usando el registro como memoria.

## Extensión: Auditoría de expansión (¿deberían existir MÁS idiomas?)

Además de mantener sincronizadas las versiones existentes, el mantenimiento lingüístico incluye cuestionarse si un documento/proyecto merece idiomas ADICIONALES:

1. **Evaluar la idoneidad** en lugar de traducir a ciegas: público objetivo, usabilidad internacional, presencia en tiendas/web, movilidad del contenido. No todo documento interno necesita inglés; no toda app necesita cinco idiomas.
2. **Verificar la preparación técnica:** ¿Está el objetivo preparado para archivos de idioma/versiones paralelas (estructura i18n, convención de nombres)? Si no es así, ESA es la primera tarea, no la traducción.
3. **Documentar hallazgos, no traducir masivamente de inmediato:** Las tareas concretas de traducción se añaden al archivo TODO local del proyecto; "ningún idioma adicional tiene sentido" es un resultado válido que debe registrarse.
4. **Control de calidad (QA) en versiones actualizadas:** Realizar muestreos de traducciones autogeneradas contra la versión principal (Sección 3) antes de considerarlas "presentes".

## Ejemplo y aplicación

```text
Tarea: "Comprobar si el artículo está sincronizado en DE y EN."

1. Inventario: paper_en.tex (principal) + paper_de.tex presentes.
2. Esquema: a DE le falta la nueva sección 4.2 (última revisión de EN); DE tiene un párrafo de demostración mejor en 3.1.
3. Transferencia inversa: formulación de 3.1 verificada técnicamente → adoptada en EN.
4. Puesta al día: 4.2 traducida a DE; números en Tabla 2 cotejados (DE tenía valores obsoletos); bibliografía homologada.
5. Entrada de registro: "paper-X | 2026-07-03 | de-en-sync | 3 divergencias resueltas, 1 transferencia inversa | próxima revisión tras la siguiente versión en EN".
```

## Banderas rojas (Red Flags)

| Mentalidad | Realidad |
| --- | --- |
| "Simplemente traduciré las diferencias desde cero" | Aclarar primero el idioma principal y la transferencia inversa; de lo contrario, se sobrescribirá la mejor solución. |
| "El esquema coincide, así que está sincronizado" | Los números, changelogs y referencias divergen primero: es obligatorio realizar un muestreo en profundidad. |
| "También traduciré los comentarios de código" | Los bloques de código e identificadores se mantienen idénticos en ambas versiones (en inglés). |
| "Sincronizaré todos los documentos de una sola vez" | Un par por ejecución (marco de rotación) mantiene la sincronización verificable. |

## Skills relacionados

- `rotation-check` — Marco para ejecuciones periódicas sobre un inventario de documentos.
- `workflow-extract` — Cuando esta comprobación deba configurarse como una automatización permanente.

## Historial de cambios

### 1.1.0 (2026-07-03)
- Se añadió la auditoría de expansión (evaluar idoneidad i18n, preparación técnica, QA para versiones actualizadas), integrada en lugar de un skill separado i18n-coverage-audit (decisión de desduplicación).

### 1.0.0 (2026-07-03)
- Versión inicial. Abstraído de la automatización de Codex "research-paper-de-en-synchronisationscheck", generalizado para cualquier versión lingüística paralela (artículos, READMEs, skills, textos de sitios web).
