---
language: es
---

<img src="banner.png" width="100%" alt="bilingual-doc-sync banner">

> **Español** — Versión oficial en español de `bilingual-doc-sync`.



# Bilingual-Doc-Sync — Mantener sincronizadas las versiones lingüísticas paralelas (Español)

## Descripción general y propósito

Los documentos bilingües divergen gradualmente: la versión que se edita activamente crece, mientras que la otra queda desfasada, hasta que la "traducción" solo lo es de nombre. Esta habilidad convierte la verificación de sincronización en un proceso definido con una regla previa decisiva: **¿qué versión es la principal?** Sin una regla de idioma principal, cada divergencia se convierte en una decisión caso por caso y la comparación resulta irrepetible.

## Proceso

### 1. Determinar el estado del inventario

- ¿Están presentes ambas (o todas) las versiones lingüísticas? Si falta alguna por completo → **actualizar/igualar** (traducción completa de la versión principal, no una nueva redacción).
- Comprobar la convención de nombres (p. ej., `DOCUMENTO.md` + `DOCUMENTO.en.md` o sufijos `_de`/`_en`) y unificar las desviaciones: la capacidad de localización es la mitad de la sincronización.

### 2. Aclarar el idioma principal (antes de cada sincronización)

- El idioma principal (o leitsprache) es la versión en la que se trabaja en cuanto a contenido (en artículos académicos suele ser EN, en documentación local suele ser la lengua materna). Prevalece en caso de contradicción.
- **Excepción de transferencia inversa:** Si la versión secundaria resuelve algo de manera demostrablemente mejor (formulación más clara, error corregido), se ADOPTA en la versión principal: primero realizar la transferencia inversa y luego sincronizar normalmente. Verificar la corrección técnica antes de adoptar una formulación "más bonita".

### 3. Comprobar la paralelidad

Estructura primero, luego el contenido:

1. **Comparación de la estructura:** Secciones y encabezados de ambas versiones lado a lado; las secciones faltantes, adicionales o reordenadas constituyen las divergencias más notorias.
2. **Muestreo por secciones** de la estructura coincidente: ¿Son idénticas las afirmaciones, números, referencias y ejemplos? Especialmente propensos a divergencias: registros de cambios (changelogs), tablas, valores numéricos, listas de referencias/enlaces y secciones editadas recientemente.
3. **Comprobar invariantes no traducibles:** Los bloques de código, identificadores, fórmulas y rutas deben ser IDÉNTICOS en ambas versiones (el código nunca se traduce).

### 4. Resolver divergencias

- Resolver las divergencias en dirección al idioma principal (o tras la transferencia inversa).
- Respetar la tipografía lingüística del idioma de destino (en español, uso correcto de tildes, signos de apertura `¿` `¡`, convenciones de comillas).
- Actualizar metadatos: números de versión, campos de fecha y entradas de changelog en AMBAS versiones (el propio changelog es el punto de divergencia más frecuente).

### 5. Documentar

Registrar el resultado (qué era divergente, qué se adoptó y qué se transfirió de forma inversa).
Como ejecución periódica sobre un conjunto de documentos: combinar con la estructura de rotación (`rotation-check`) — un documento (o par) por ejecución, usando el registro como memoria.

## Extensión: Auditoría de expansión (¿deberían existir MÁS idiomas?)

Además de mantener sincronizadas las versiones existentes, la gestión lingüística incluye evaluar si un documento o proyecto merece idiomas ADICIONALES:

1. **Evaluar la idoneidad** en lugar de traducir a ciegas: público objetivo, usabilidad internacional, presencia en tiendas/web, movilidad del contenido. No todo documento interno necesita inglés; no toda aplicación necesita cinco idiomas.
2. **Comprobar la preparación técnica:** ¿Está el objetivo preparado para archivos de idioma/versiones paralelas (estructura i18n, convención de nombres)? Si no, ESA es la primera tarea, no la traducción.
3. **Documentar el hallazgo, no realizar traducciones masivas de inmediato:** Asignar tareas de traducción concretas al archivo TODO local del proyecto; la conclusión "ningún otro idioma es necesario" es un resultado válido que debe registrarse.
4. **Control de calidad en versiones actualizadas:** Comprobar aleatoriamente las traducciones autogeneradas contra la versión principal (Sección 3) antes de considerarlas "existentes".

## Ejemplo y aplicación

```text
Encargo: "Comprueba si el artículo está sincronizado en DE y EN."

1. Inventario: paper_en.tex (principal) + paper_de.tex presentes.
2. Estructura: A DE le falta la nueva sección 4.2 (última revisión de EN); DE tiene un
   párrafo de demostración mejor en 3.1.
3. Transferencia inversa: Formulación de 3.1 verificada técnicamente → adoptada en EN.
4. Actualización: 4.2 traducido a DE; números en la Tabla 2 cotejados (DE tenía
   valores desfasados); bibliografía igualada.
5. Entrada en registro: "paper-X | 2026-07-03 | de-en-sync | 3 divergencias resueltas,
   1 transferencia inversa | próxima revisión tras la siguiente versión de EN".
```

## Red Flags (Señales de advertencia)

| Pensamiento | Realidad |
| --- | --- |
| "Simplemente traduciré las diferencias desde cero" | Aclarar primero el idioma principal y la transferencia inversa — de lo contrario, se sobrescribirá la mejor solución. |
| "La estructura coincide, por lo tanto está sincronizado" | Los números, changelogs y referencias divergen primero — es obligatorio hacer muestreos en profundidad. |
| "También traduciré los comentarios del código" | Los bloques de código y los identificadores permanecen idénticos en ambas versiones (en inglés). |
| "Sincronizaré todos los documentos de una sola vez" | Un par por ejecución (usando la estructura de rotación) mantiene la comparación verificable. |

## Habilidades relacionadas

- `rotation-check` — Estructura para ejecuciones periódicas sobre un fondo de documentos.
- `workflow-extract` — Si esta comprobación se va a configurar como una automatización permanente.

## Registro de cambios

### 1.1.0 (2026-07-03)
- Se añadió la auditoría de expansión (evaluar idoneidad i18n, preparación técnica, control de calidad para versiones actualizadas) — integrada en lugar de crear un skill independiente i18n-coverage-audit (decisión de desduplicación).

### 1.0.0 (2026-07-03)
- Versión inicial. Abstraído de la automatización Codex "research-paper-de-en-synchronisationscheck", generalizado para cualquier par de versiones lingüísticas paralelas (artículos, READMEs, skills, textos web).