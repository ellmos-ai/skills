---
language: es
---

> **Español** — Versión oficial en español de `rotation-check`.


# Rotation-Check — un objetivo por ejecución, cobertura justa, memoria (Español)

## Visión general y propósito

Quien desee revisar periódicamente un pipeline con muchos proyectos (fuentes, estilo, salud, seguridad, traducciones, …), se enfrenta a un problema de distribución: revisar todos los proyectos en cada ejecución es demasiado costoso; sin memoria, cada ejecución revisa lo mismo al azar. El patrón de rotación resuelve ambos problemas: **exactamente un objetivo por ejecución, selección basada en "el que lleva más tiempo sin revisar", registry como memoria.** De este modo, incluso un ritmo infrecuente (diario/semanal) cubre todo el pipeline a lo largo de las semanas, de forma comprobable y sin duplicar trabajo.

Demostrado como la columna vertebral de un conjunto consolidado de automatizaciones de producción a través de múltiples pipelines de proyectos.

## Componentes

### 1. Dos archivos por pipeline (crear una sola vez)

| Archivo | Contenido | Carácter |
| --- | --- | --- |
| `CHECKED-REGISTRY.md` | Una línea compacta por revisión: objetivo, fecha, tipo de check, resultado, siguiente paso | Resumen de estado — se lee ANTES de cada selección de objetivo |
| `CHECKS-LOG.txt` | Entrada de historial corta por ejecución con detalles/evidencia | Diario — solo anexar (append-only) |

Ambos se ubican en la raíz del pipeline (no en el proyecto individual) para que una ejecución pueda capturarlos con una sola lectura. Formato de línea en la registry:

```text
| <objetivo> | <YYYY-MM-DD> | <tipo_de_check> | <ok|hallazgo|omitido> | <siguiente_paso> |
```

### 2. Regla de selección

1. Leer la registry y el log (obligatorio, ANTES de la selección — de lo contrario habrá revisión duplicada).
2. Candidatos: Objetivos que NUNCA hayan sido revisados o lleven MÁS TIEMPO sin revisarse para ESTE tipo de check.
3. Desviar si el objetivo fue abordado recientemente por un check **estrechamente relacionado** (ej. un check de citas inmediatamente después de un check de fuentes no aporta nada) o si está bloqueado/en edición actualmente (respetar los bloqueos/locks).
   **Tiempo de reposo entre checks hermanos (Sibling Cooldown):** Si ejecutas múltiples checks relacionados sobre el mismo conjunto de objetivos (ej. desarrollo, búsqueda de errores y revisión del mismo pipeline), acuerda un tiempo de espera (valor empírico: ~24 h) durante el cual un objetivo procesado por un check hermano no vuelva a ser seleccionado — evita colisiones y cambios paralelos contradictorios.
4. Adelantar fuera de turno solo con una buena razón (ej. gran revisión desde el último check) — indicar la razón en el log.

### 3. Realizar el check — con salida de solo lectura (Read-only Exit)

Aplicar el check en sí (definible libremente: check de fuentes, check de estilo, auditoría de seguridad, …) al ÚNICO objetivo seleccionado. Dos salidas válidas:

- **Hallazgo:** corregir lo que quepa dentro del alcance; lo que sea mayor registrarlo como tarea posterior en el archivo TODO/TAREAS local del proyecto (el check no tiene que resolver todo por sí mismo).
- **Nada que hacer:** documentar brevemente y finalizar. Una ejecución sin hallazgos es un resultado, no un fracaso — en ningún caso se debe ampliar el alcance solo para "haber encontrado algo".

### 4. Documentar

- Agregar la línea en la registry (compacta), escribir la entrada en el log (detalles/evidencia).
- **Higiene del log:** Si la registry/log se vuelven confusos (valor empírico: varias cientos de líneas), mover el estado antiguo a `_archiv/`, crear un archivo nuevo y hacer referencia al anterior en el encabezado (ruta + fecha).
- **Desviación de rutas (Path Drift):** Si una ruta esperada apunta al vacío (objetivo movido/renombrado), NO la crees de nuevo — corrígela mediante el archivo de estado/registry definitivo del pipeline y registra la ruta errónea en un log de fallos.

### 5. Ritmo / Cadencia

Vincular la frecuencia a la tasa de cambios de lo revisado: Los checks de rotación sobre conjuntos estables funcionan bien semanalmente (un objetivo por ejecución ≈ todo el pipeline por trimestre para ~12 objetivos); checks de ritmo rápido (ej. sobre trabajo activo) diariamente. Experiencia práctica: al principio casi todos los checks horarios se redujeron a diarios/semanales — la cobertura se mantuvo y los costos cayeron.

## Plantilla de Prompt (para Programador/Automatización)

```text
PREPARACIÓN: Lee <PIPELINE_ROOT>/<POLÍTICAS> así como <REGISTRY> y <LOG>.

TAREA: Selecciona exactamente un objetivo de <CONJUNTO_OBJETIVOS>. Prioriza los objetivos que NUNCA hayan sido revisados o lleven MÁS TIEMPO sin revisarse para el check "<TIPO_CHECK>". Si un objetivo fue revisado recientemente por este u otro check estrechamente relacionado o está bloqueado: desviar o finalizar en modo lectura (read-only) con una entrada en el log.

CHECK: <tarea concreta de revisión/mantenimiento y qué hacer en caso de hallazgos; registrar tareas posteriores en el archivo TODO local del proyecto>.

Si no hay trabajo pendiente: documentar brevemente y finalizar la ejecución.

DOCUMENTACIÓN: Línea en la registry en <REGISTRY> (objetivo, fecha, tipo de check, resultado, siguiente paso) + entrada de historial en <LOG>. En caso de longitud excesiva: mover estado antiguo a _archiv/ y crear archivo nuevo con referencia.

FINALIZACIÓN: Informe breve (Objetivo | realizado | resultado | tareas posteriores).
```

## Banderas Rojas (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "Simplemente elegiré un proyecto interesante" | La selección se realiza ÚNICAMENTE mediante la registry — de lo contrario habrá sesgo de proyecto favorito y puntos ciegos. |
| "Leeré la registry después del check" | Léela ANTES. Es el criterio de selección, no solo el protocolo. |
| "Múltiples objetivos por ejecución rinden más" | Un solo objetivo mantiene las ejecuciones cortas, idempotentes y cancelables; la cantidad se logra mediante la rotación. |
| "La ejecución sin hallazgos fue en vano" | Una ejecución sin hallazgos documentada actualiza la memoria — ese es el 50% del valor del sistema. |

## Habilidades Relacionadas

- `workflow-extract` — construye automatizaciones a partir de sesiones/automatizaciones externas; utiliza esta estructura como componente estándar.
- `pipeline-optimizer` — para la reestructuración de un pipeline (Rotation-Check mantiene, Optimizer renueva).

## Historial de Cambios

### 1.1.0 (2026-07-03)
- Se añadió el tiempo de reposo entre hermanos (Sibling Cooldown) como regla de selección (prevención de colisiones entre checks relacionados sobre el mismo conjunto de objetivos; hallazgo de la clasificación completa del inventario de automatización).

### 1.0.0 (2026-07-03)
- Versión inicial. Abstraído del inventario de automatizaciones de Codex (patrón de rotación en ~40 de 77 automatizaciones: checks de investigación/software/Roblox con CHECKED-REGISTRY/CHECKS-LOG).