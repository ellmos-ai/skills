---
language: es
---

> **Español** — Versión oficial en español de `rotation-check`.

# Rotation-Check — Un objetivo por ejecución, cobertura equitativa, memoria

## Descripción general y propósito

Quien desee revisar periódicamente una línea de producción (pipeline) con muchos proyectos (fuentes, estilo, salud, seguridad, traducciones, …) se enfrenta a un problema de distribución: revisar todos los proyectos en cada ejecución resulta demasiado costoso; sin memoria, cada ejecución revisa al azar lo mismo. El patrón de rotación resuelve ambos aspectos: **exactamente un objetivo por ejecución, selección por "el más tiempo no revisado", registro como memoria.** De este modo, incluso un ritmo poco frecuente (diario/semanal) cubre toda la pipeline a lo largo de las semanas, de forma demostrable y sin duplicar esfuerzos.

Acreditado como pilar central de un inventario consolidado de automatizaciones de producción en múltiples pipelines de proyectos.

## Componentes

### 1. Dos archivos por pipeline (crear una sola vez)

| Archivo | Contenido | Carácter |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | Una línea compacta por revisión: objetivo, fecha, tipo de revisión, resultado, siguiente paso | Vista de estado — se lee ANTES de cada selección de objetivo |
| `CHECKS-LOG.txt` | Entrada corta del historial por ejecución con detalles/evidencia | Diario — solo añadir al final (append-only) |

Ambos se ubican en la raíz de la pipeline (no en el proyecto individual), de modo que una ejecución pueda capturarlos con una sola lectura. Formato de línea del registro:

```text
| <ziel> | <YYYY-MM-DD> | <checktyp> | <ok|befund|übersprungen> | <nächster schritt> |
```

### 2. Regla de selección

1. Leer el registro y el log (obligatorio, ANTES de la selección; de lo contrario, habrá revisión duplicada).
2. Candidatos: Objetivos que nunca han sido revisados o que llevan más tiempo sin revisarse para ESTE tipo de revisión.
3. Desviar/omitir si el objetivo fue tocado recientemente por una revisión **estrechamente relacionada** (p. ej., una revisión de citas justo después de una revisión de fuentes no aporta nada) o si está bloqueado/en desarrollo activo (respetar bloqueos).
   **Tiempo de reposo entre hermanos (Sibling Cooldown):** Si ejecutas varias revisiones relacionadas sobre el mismo conjunto de objetivos (p. ej., desarrollo, búsqueda de errores y revisión de la misma pipeline), acuerda un período de gracia (valor empírico: ~24 h) en el cual un objetivo procesado por una revisión hermana no vuelva a seleccionarse — evita colisiones y cambios paralelos contradictorios.
4. Priorizar fuera de turno solo con un buen motivo (p. ej., una gran reestructuración desde la última revisión); indicar el motivo en el log.

### 3. Realizar la revisión — con salida de solo lectura

Aplicar la revisión real (libremente definible: revisión de fuentes, revisión de estilo, auditoría de seguridad, …) al ÚNICO objetivo seleccionado. Dos resultados válidos:

- **Hallazgo (Befund):** Corregir lo que encaje dentro del alcance; registrar tareas más grandes como trabajo posterior en el archivo TODO/AUFGABEN local del proyecto (la revisión no tiene que resolverlo todo por sí misma).
- **Nada que hacer:** Documentar brevemente y finalizar. Una ejecución sin cambios es un resultado, no un fracaso — en ningún caso ampliar el alcance solo para "haber encontrado algo".

### 4. Documentación

- Complementar la línea del registro (compacta), escribir la entrada del log (detalles/evidencia).
- **Higiene del log:** Si el registro/log se vuelven desordenados (valor empírico: varias cientos de líneas), mover el estado antiguo a `_archiv/`, crear un archivo nuevo y hacer referencia al predecesor en la cabecera (ruta + fecha).
- **Desviación de ruta (Path Drift):** Si una ruta esperada apunta a la nada (objetivo movido/renombrado), NO volver a crearla — corregir a través del archivo de estado/registro autoritativo de la pipeline y registrar la ruta errónea en un log de fallos.

### 5. Cadencia

Vincular la frecuencia a la tasa de cambios de lo revisado: las revisiones por rotación sobre inventarios estables funcionan bien semanalmente (un objetivo por ejecución ≈ toda la pipeline por trimestre con ~12 objetivos); revisiones de ritmo rápido (p. ej., sobre trabajo activo) diariamente. Experiencia práctica: inicialmente las revisiones horarias se redujeron casi todas a diarias/semanales — la cobertura se mantuvo, los costes cayeron.

## Plantilla de prompt (para programador/automatización)

```text
VORBEREITUNG: Lies <PIPELINE_ROOT>/<POLICY-DOKUMENTE> sowie <REGISTRY> und <LOG>.

AUFGABE: Wähle genau ein Ziel aus <ZIELMENGE>. Bevorzuge Ziele, die für den Check
"<CHECKTYP>" noch nie oder am längsten nicht geprüft wurden. Wurde ein Ziel kürzlich
von diesem oder einem eng verwandten Check geprüft oder ist es gesperrt: ausweichen
oder read-only mit Logeintrag enden.

CHECK: <konkrete Prüf-/Pflegeaufgabe und was bei Befund zu tun ist; Folgearbeiten in
die projektlokale TODO-Datei>.

Wenn keine Arbeit anfällt: kurz dokumentieren, Lauf beenden.

DOKUMENTATION: Registry-Zeile in <REGISTRY> (Ziel, Datum, Checktyp, Ergebnis, nächster
Schritt) + Verlaufseintrag in <LOG>. Bei Überlänge: alten Stand nach _archiv/ und
frische Datei mit Verweis.

ABSCHLUSS: Kurzbericht (Ziel | getan | Ergebnis | Folgeaufgaben).
```

## Banderas rojas (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "Simplemente elegiré un proyecto interesante" | Selección únicamente a través del registro — de lo contrario, sesgo hacia proyectos favoritos y puntos ciegos. |
| "Leeré el registro después de la revisión" | Antes. Es el criterio de selección, no solo el protocolo. |
| "Múltiples objetivos por ejecución logran más" | Un solo objetivo mantiene las ejecuciones cortas, idempotentes y cancelables; el volumen se consigue mediante la rotación. |
| "La ejecución sin cambios fue en vano" | Una ejecución sin cambios documentada actualiza la memoria — eso representa la mitad del valor del sistema. |

## Skills relacionadas

- `workflow-extract` — construye automatizaciones a partir de sesiones/automatizaciones externas; utiliza esta estructura como componente estándar.
- `pipeline-optimizer` — para la reestructuración arquitectónica de una pipeline (rotation-check mantiene, optimizer renova).

## Historial de cambios

### 1.1.0 (2026-07-03)
- Se añadió el tiempo de reposo entre hermanos (Sibling Cooldown) como regla de selección (anticolisión entre revisiones relacionadas sobre el mismo conjunto de objetivos; hallazgo proveniente de la clasificación completa del inventario de automatizaciones).

### 1.0.0 (2026-07-03)
- Versión inicial. Abstraído del inventario de automatización Codex (patrón de rotación en ~40 de 77 automatizaciones: revisiones de investigación/software/Roblox con CHECKED-REGISTRY/CHECKS-LOG).
