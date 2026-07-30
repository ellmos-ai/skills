---
language: es
---

<img src="banner.png" width="100%" alt="workflow-extract banner">

> **Español** — Versión oficial en español de `workflow-extract`.


# Workflow-Extract — Crear automatizaciones a partir de historiales de chat y automatizaciones externas

## Descripción general y propósito

Algunos flujos de trabajo no corresponden a un skill que se carga a petición, sino a una **automatización que se ejecuta de forma autónoma**: comprobaciones nocturnas, auditorías de proyectos en rotación, ejecuciones periódicas de mantenimiento. Este skill extrae dichos flujos de trabajo de dos tipos de fuentes — historiales de chat (un proceso desarrollado de forma interactiva que en el futuro debe ejecutarse sin supervisión) y prompts de automatizaciones existentes en otros sistemas (p. ej., Codex-Automations, Scheduled Tasks, flujos de n8n) — y los convierte en prompts de automatización o skills neutros con respecto al usuario y de gran robustez.

La diferencia fundamental con un proceso interactivo: una automatización **no tiene a nadie que corrija errores**. Todo aquello que el usuario haya detectado o corregido durante la sesión interactiva debe ser gestionado de forma autónoma por la propia automatización. Para esto sirven precisamente los componentes de `automation-bausteine.md`.

## Flujo de trabajo

### 1. Aclarar origen y forma de destino

| Origen | Caso típico |
| --- | --- |
| Sesión actual / Transcripción | El flujo se desarrolló de forma interactiva y debe continuar ejecutándose periódicamente |
| Automatización externa (Archivo de prompt, tarea cron, flujo n8n) | Portabilidad/abstracción hacia otro sistema o hacia la biblioteca |

Formas de destino (una o varias):

- **Prompt de automatización:** Texto de prompt independiente y neutro con respecto al usuario, utilizable en cualquier planificador (Codex-Automations, Claude `/schedule`/Cron, Scheduled Task, n8n).
- **Skill de flujo de trabajo (Workflow-Skill):** Skill en la biblioteca que describe el proceso y que el prompt de automatización solo invoca o parametriza (preferible si el mismo flujo debe aplicarse a múltiples pipelines/sistemas — fuente única de verdad).
- **Comando (Command):** Slash-command ligero para la activación manual del mismo flujo.

### 2. Extraer el núcleo del flujo de trabajo

Identificar y extraer del origen:

- **Tarea principal:** ¿Qué se comprueba, mantiene o genera? (una frase)
- **Lógica de selección:** ¿A qué se aplica la tarea? ¿Objetivo fijo o rotación sobre un conjunto (un proyecto por ejecución)?
- **Precondiciones:** ¿Qué debe leerse o comprobarse antes del trabajo (documentos raíz, registros, bloqueos/locks)?
- **Obligaciones de documentación:** ¿Dónde se escriben los resultados, logs y tareas secundarias/de seguimiento?
- **Rutas de cancelación:** ¿Cuándo finaliza la ejecución en modo solo lectura ("nada que hacer" es un resultado válido)?

En historiales de chat, evaluar además los bucles de corrección (ver `../skill-extractor/transcript-quellen.md`): Cada corrección realizada por el usuario es candidata a convertirse en una protección (guard) que la automatización necesitará por sí misma en el futuro.

### 3. Neutralizar

Siguiendo las reglas de `../skill-extractor/neutralisierung.md`: Separar la mecánica de la configuración, extraer rutas, hosts y nombres de proyectos a un bloque de configuración. Los prompts de automatización necesitan este bloque de configuración con especial urgencia porque se copian literalmente en los planificadores; los valores concretos deben ubicarse en UN solo lugar al inicio del prompt.

### 4. Añadir componentes de automatización

Contrastar el núcleo extraído con la lista de verificación de `automation-bausteine.md` y añadir los componentes faltantes — especialmente selección en rotación con registro de comprobación, idempotencia, higiene de logs, respeto a bloqueos (locks), salida en modo solo lectura e informe de cierre. Un flujo de trabajo sin estos componentes funciona en fase de pruebas pero se degrada en operación continua (verificaciones duplicadas, crecimiento desmedido de logs, colisiones con agentes paralelos).

### 5. Establecer ritmo y presupuesto

- **Vincular la frecuencia a la tasa de cambios:** Una comprobación no necesita ejecutarse con más frecuencia de la que cambia su objeto. Experiencia en flotas de automatización maduras: Muchas comprobaciones que inicialmente se ejecutaban cada hora se redujeron a frecuencia diaria/semanal; con selección en rotación, incluso un ritmo de baja frecuencia cubre toda la pipeline.
- **Ventana nocturna para tareas pesadas**, las comprobaciones cortas de solo lectura pueden ser más frecuentes.
- **Conciencia de costes:** Cada ejecución consume tokens/cómputo; una ejecución que por lo general termina en solo lectura debe determinarlo lo antes posible (leer el registro ANTES del análisis costoso).

### 6. Probar y desplegar

1. **Ejecución en seco (Dry run):** Ejecutar el prompt finalizado una vez de forma interactiva (como si fuera el planificador) y verificar: ¿Finaliza correctamente? ¿Escribe adecuadamente el registro/log? ¿Se mantiene dentro del alcance?
2. **Prueba de caso límite:** Simular una ejecución en la que no haya nada que hacer: debe finalizar en solo lectura con un registro breve en el log, sin "inventar trabajo".
3. **Desplegar:** Registrar en el planificador de destino; si es en forma de skill, almacenar además en la biblioteca y desplegar.
4. **Supervisar rutas de error:** Tras las primeras 2–3 ejecuciones reales, controlar el log/registro — las automatizaciones fallan con mayor frecuencia por desviación de rutas (el objetivo se movió) y por archivos de log desmesurados.

## Modo Fleet-Audit: auditar una flota de automatizaciones en ejecución

Para "auditar mis automatizaciones": no extraer, sino ayudar a operar el INVENTARIO EXISTENTE. A través de la fuente de automatizaciones del sistema de destino (archivos de prompt/configuración, programaciones, logs/memorias de ejecución), comprobar de forma sistemática:

1. **Detección de fallos silenciosos / No-op:** ¿La automatización se ejecuta pero ya no hace nada? (Leer memorias/logs de ejecuciones recientes: ¿solo ejecuciones en vacío, errores, rutas inactivas?)
2. **Redundancia + Rendimiento:** ¿Se solapan las automatizaciones en alcance? ¿El rendimiento (output, hallazgos resueltos) sigue siendo proporcional al consumo (tokens, ejecuciones)?
3. **Desviación (Drift):** ¿Las rutas de los prompts, convenciones y programaciones siguen ajustándose a la realidad? (Objetivos movidos, políticas modificadas, frecuencia demasiado alta para la tasa de cambios.)
4. **Cotejo con catálogo:** ¿Falta alguna automatización que debería existir (huecos en la matriz de patrones)? Las sugerencias solo deben incluirse condicionadas a aprobación (Componente 12), nunca activarse de forma autónoma.
5. **Informe de hallazgos:** Una línea por automatización (conservar | adaptar | pausar | consolidar | eliminar) + justificación; realizar cambios solo tras obtener aprobación.

## Modo Bulk: revisar inventarios de automatizaciones o múltiples transcripciones

Para "revisar todas las automatizaciones del Sistema X en busca de flujos de trabajo abstraibles" o "extraer candidatos de automatización a partir de historiales de chat antiguos":

1. **Reducción de datos como en `skill-extractor`** (Map-Reduce mediante subagentes, patrón `swarm-operations`): Un subagente por paquete que informa según la fuente: Tarea principal | Patrón (p. ej. comprobación en rotación, comprobación de salud, minería de ideas) | Elementos únicos | ¿Abstraible de forma neutra? | ¿Cubierto por un skill existente?
2. **Patrones sobre casos individuales:** Cuando muchas fuentes comparten la misma estructura base (p. ej., 40 comprobaciones en rotación), la ESTRUCTURA se convierte en un skill y los casos individuales en parametrizaciones — no en 40 skills independientes.
3. **Deduplicación frente al catálogo existente de skills/comandos**, y posteriormente presentar la lista numerada de candidatos al usuario antes de la creación masiva.

## Ejemplo y aplicación

```text
User: "Hoy probamos la verificación de citas para un artículo — a partir de ahora esto debería ejecutarse semanalmente en todos los artículos."

1. Forma de destino: Prompt de automatización para el planificador + referencia a rotation-check.
2. Núcleo: Comprobar las citas de un artículo contra fuentes originales (web/base de datos), aplicar correcciones, en caso de cambios registrar tarea de seguimiento "Re-subir" en TODO.md.
3. Neutralizar: Raíz del pipeline, rutas de registro/log → bloque de configuración.
4. Añadir componentes: Selección en rotación (un artículo por ejecución), leer registro ANTES de la selección, salida en solo lectura ("todas las fuentes ok"), higiene de logs, informe de cierre.
5. Ritmo: Semanal es suficiente (los artículos cambian lentamente); ejecución en seco + prueba de inactividad, luego al planificador.
```

## Banderas rojas (Red Flags)

| Pensamiento | Realidad |
| --- | --- |
| "El flujo funcionó en la sesión, por lo que también funcionará como automatización" | Sin el usuario faltan todos los elementos correctivos — la lista de verificación de componentes es obligatoria. |
| "Ejecutar cada hora no hace daño" | Sí hace daño: tokens, crecimiento de logs, riesgo de colisión. Vincular el ritmo a la tasa de cambios. |
| "Crearé una automatización independiente para cada variante" | Estructura compartida como skill, variantes como parámetros. |
| "No se encontró nada — buscaré otro trabajo que hacer" | La salida en modo solo lectura con un registro en el log es el resultado correcto de una ejecución en vacío. |

## Skills relacionados

- `skill-extractor` — Misma extracción, el destino es un skill invocable; comparte neutralización y fuentes de transcripción (documentado allí).
- `rotation-check` — Estructura estándar para comprobaciones en rotación de pipelines (el tipo de automatización más común); referenciar como componente en lugar de reinventar.
- `swarm-operations` — Patrón de enjambre para revisiones masivas.

## Historial de cambios

### 1.1.0 (2026-07-03)
- Modo Fleet-Audit (auditar flota de automatizaciones en ejecución: fallos silenciosos, redundancia, desviación, vacíos) — integrado en lugar de crear un skill independiente (decisión de deduplicación).
- Tres nuevos componentes en `automation-bausteine.md`: Puerta de aprobación mediante archivos centinela (12), Escalación gradual con artefacto de traspaso (13), Disciplina de notificación para monitores (14).

### 1.0.0 (2026-07-03)
- Versión inicial. Creada a partir de la abstracción del inventario de Codex-Automations (77 automatizaciones, patrón dominante de comprobación en rotación) en componentes neutros con respecto al usuario.