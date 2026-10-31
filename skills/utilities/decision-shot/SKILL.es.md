---
name: decision-shot
version: 1.2.0
type: skill
author: Lukas Geiger + Claude
created: 2026-08-24
updated: 2026-09-18
description: "Formato de salida extremadamente breve y sustancial para UNA decisión o un grupo de decisiones, cuando el análisis subyacente ya existe (surgido en el chat, de `decide`, de `decision-briefing`, de un ticket o de un documento): contexto en 2-3 líneas, pros/contras por opción como viñetas en estilo reducido paveman/caveman, puntos de conversación, una recomendación fundamentada y una ruta/enlace al análisis completo para leerlo en detalle. Usa esta skill con \"dame esto breve con pros y contras y recomendación\", \"resumen ejecutivo de la decisión\", \"contexto breve sobre <Thema>\", \"resume la decisión X en forma corta\", /decision-shot, o cuando un resultado deba pasarse a alguien que solo necesita la esencia, no la derivación completa. NO usar para RECOPILAR muchas decisiones abiertas y consultarlas por letra: eso lo hace decision-briefing; NO usar para ANALIZAR primero una decisión: eso lo hace decide. decision-shot requiere un análisis terminado y solo comprime su presentación."
visibility: public
language: es
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: utilities
tags: [entscheidung, executive-summary, kurzform, pro-contra, talking-points, empfehlung]
status: active

dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, knappform, paveman]

provenance:
  origin: "custom"
  decision_ref: "T-20260824-673115956 (Ticket-Master, User-Auftrag 2026-08-24)"
translated_from_sha256: 26ff135e844d526543d9f5df212d36e408a427a71cc13a9e744a55abdb5ed991
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.943012+00:00"
---
<img src="banner.png" width="100%" alt="decision-shot banner">

# decision-shot

> El análisis está hecho. Lo que ahora se necesita no es una segunda
> derivación, sino la esencia más la vía de regreso a lo completo.

## Cuándo usar

- Una decisión (o un grupo estrechamente relacionado, p. ej. varias subpreguntas
  del mismo tema) ya está meditada -- en el chat, en un ticket, mediante el
  marco `decide` o en la fase 2 de `decision-briefing` -- y debe ponerse
  en segundos a disposición de alguien (el usuario, otro agente, un documento
  de traspaso).
- Palabras disparadoras: "resumido con pros y contras", "resumen ejecutivo",
  "contexto breve", "puntos de conversación al respecto", "dame esto comprimido
  con recomendación", `/decision-shot`.
- **No** con varios puntos abiertos y sin decidir que el usuario debe responder
  uno tras otro o en lote por letra -- eso es
  [decision-briefing](../decision-briefing/SKILL.md). **No** para elaborar primero una
  decisión -- eso es [decide](../decide/SKILL.md). decision-shot es solo
  PRESENTACIÓN de un análisis ya existente.

## Delimitación (resumen)

| Skill | Qué hace | Cuándo está terminado |
|---|---|---|
| `decide` | Elabora UNA decisión con un marco (matriz pro/contra, puntuación ponderada, árbol de decisión, ...) | El análisis aún falta |
| `decision-briefing` | Reúne MUCHAS decisiones abiertas de un tema, las presenta como lote A/B/C/D y recibe respuestas por letra | Varios puntos siguen sin decidir |
| `decision-shot` | Condensa UN análisis terminado (sea de donde sea) en una versión ejecutiva con enlace a la versión completa | El análisis ya existe; solo falta la presentación |
| `knappform` | Modificador general del estilo de respuesta para CADA respuesta de la sesión | Para toda la sesión, sin importar el tema |
| `paveman` | Acorta de forma determinista ARCHIVOS DE PROSA existentes (archivos de reglas/memoria) | Acorta un archivo, no la salida del chat |

`decision-shot` no compite con ninguna de las cuatro: es el FORMATO que se usa
después de `decide` o junto a `decision-briefing` en cuanto la esencia debe
transmitirse. El estilo lingüístico reducido se orienta en `knappform`/`paveman`
(ver allí la lista completa de eliminaciones), pero aquí se aplica de forma
coherente a un formato fijo de cinco partes.

## Formato (vinculante, cinco partes)

```
## <Entscheidungstitel>

**Kontext:** <2-3 Zeilen -- worum es geht, warum jetzt, was auf dem Spiel steht>

**<Option A>**
+ <staerkstes Pro-Argument>
+ <zweites Pro-Argument, nur falls es traegt>
- <staerkstes Contra-Argument>

**<Option B>**
+ <Pro>
- <Contra>
- <Contra>

**Talking Points:**
- <Punkt, der im Gespraech/in einer Mail sofort zieht>
- <Punkt, der einen typischen Einwand vorwegnimmt>

**Empfehlung:** <Option> -- <ein Satz Begruendung, keine Wiederholung der Pro-Liste>

**Vollanalyse:** <Pfad oder Link -- Ticket-Datei, Dokument, Chat-Referenz>
```

## Reglas

- **Textos para el usuario sin números/abreviaturas técnicas (forma yo, lenguaje cotidiano):**
  En el texto visible para la persona (título, contexto, opciones, puntos de conversación, recomendación) **no** aparecen abreviaturas internas, números de ticket (`T-...`), identificadores D ni rutas de archivo relativas.
  El contexto describe la situación y la acción prevista en forma yo („Propongo...“).
  Las referencias técnicas (ID de ticket, ruta exacta del archivo) aparecen únicamente en la línea final `**Vollanalyse:**` o en una tabla de referencias.
- **Las líneas son presupuesto, no objetivo.** 2-3 líneas de contexto, 2-4 viñetas por opción, 2-3 puntos de conversación, 1 frase de recomendación; lo que sobre se elimina, no se acorta y se conserva. Si una opción no cabe en 4 viñetas, no pertenece a esta skill, sino al análisis completo.
- **Estilo reducido como `knappform`/`paveman`:** sin muletillas, sin
  fórmulas vacías, sin evasivas. Las negaciones (`nicht`, `nie`, `kein`, `nur`,
  `außer`) se mantienen intactas: suprimirlas invierte la afirmación.
- **Pros/contras son viñetas, no oraciones.** `+`/`-` como prefijo, un
  pensamiento por línea, sin oraciones subordinadas.
- **Los puntos de conversación son comunicativos, no analíticos.** Responden a
  "qué digo si alguien me pregunta" -- no a "qué dice el análisis". Los duplicados
  de la lista de pros/contras indican que aún no se ha condensado.
- **La recomendación se justifica a sí misma en una frase.** Sin repetir la lista
  de pros, sin "ver arriba" -- la frase debe sostenerse sin el resto del bloque.
- **El enlace/la ruta al análisis completo es obligatorio, no opcional.** decision-shot
  no sustituye el análisis, solo lo hace fácil de encontrar. Si falta una fuente
  tangible (surgida solo oralmente en el chat, sin documento), nombra la referencia
  al chat/sesión de la forma más concreta posible (p. ej. "esta sesión, respuesta a F4")
  en lugar de dejar el campo vacío.
- **Varias decisiones relacionadas** (grupo, p. ej. varias subpreguntas de un tema):
  un bloque por decisión, separados por `---`; el contexto común se
  escribe solo una vez al principio, y únicamente si realmente vale para todas.

### Procedencia de sesión en decision-shots guardados

Si el decision-shot se guarda como artefacto nuevo, importante y duradero, el archivo termina con:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

El ID de sesión procede primero de un dato explícito de ejecución/CLI, después de un
entorno o hook autoritativo del proveedor; si faltan ambos, se escribe `unbekannt`. Nunca
adivines valores. Los subagentes usan la sesión padre. El chat rutinario, las fuentes, las políticas, `CLAUDE.md`,
los READMEs y los archivos antiguos no se sellan ni se vuelven a sellar en bloque.

## Ejemplo

```
## Wo laeuft der naechtliche Backup-Job?

**Kontext:** Ich beobachte wiederholte Ausfälle auf dem Laptop, weil das Gerät nachts
schläft. Ich schlage vor, den Job auf den Mac Studio umzuziehen, der rund um die Uhr läuft.

**Laptop (Status quo)**
+ Keine Netzwerkabhaengigkeit
- Job faellt regelmaessig aus, wenn das Geraet schlaeft
- Kein zentraler Log-Ueberblick

**Mac Studio**
+ Laeuft 24/7, keine Ausfaelle durch Schlafmodus
+ Zentrale Logs an einem Ort
- Braucht funktionierendes Tailscale/SSH als Voraussetzung

**Talking Points:**
- "Der Ausfall ist kein Bug im Skript, sondern eine Standortfrage."
- "Tailscale laeuft schon fuer andere Jobs stabil -- kein neues Risiko."

**Empfehlung:** Mac Studio -- einzige Option ohne den bekannten Schlafmodus-
Ausfall, und die Abhaengigkeit (Tailscale) ist bereits im Betrieb bewaehrt.

**Vollanalyse:** `.SYNC/MAC_STUDIO_COMPUTE_HANDOFF.md`, Abschnitt "Backup-Jobs" (Ticket T-20260620-42)
```

## Registro de cambios

### 1.2.0 (2026-09-18)
- Regla de estilo para textos de decisión comprensibles anclada (T-20260913-883789445, instrucción del usuario 2026-09-13):
  - Sin números de ticket, identificadores D ni rutas internas en el texto visible (título, contexto, puntos de conversación).
  - Contexto y recomendación en lenguaje cotidiano natural en forma yo.
  - Referencias técnicas de ticket y ruta limitadas estrictamente a la línea final del análisis completo.

### 1.1.0 (2026-09-09)
- P-018 añade el sello de sesión para decision-shots nuevos guardados que sean importantes, con
  prioridad estrecha de fuentes y exclusiones.

### 1.0.0 (2026-08-24)
- Versión inicial.
