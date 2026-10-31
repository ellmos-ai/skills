---
name: decision-path
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "Genera, a partir de un inventario de decisiones abiertas y cerradas, un grafo de dependencias en ASCII estructurado (máximo 100 columnas) para el terminal. Evalúa los nodos según cinco criterios fijos: razonable, recomendado, propio del usuario (dirección y confianza de decision-avatar por separado), compatible y contradictorio; las aristas llevan el tipo de relación y el estado de la evidencia. Detecta sin contemplaciones bloqueos, desbloqueos, secuencias y recomendaciones contradictorias. Usa esta skill con \"qué decisiones dependen unas de otras\", \"grafo de dependencias de las decisiones\", \"visualizar la ruta de decisión\", \"revisar contradicciones entre decisiones\", \"orden de las resoluciones\", /decision-path. NO la uses para inventariar decisiones por primera vez: eso lo hace decision-briefing; NO la uses para agrupar el concepto general recomendado para su aprobación: eso lo hace decision-draw; NO para bloques individuales compactos de cinco puntos con opciones y pro/contra: eso lo hace decision-shot; NO para la consideración de un caso individual con marcos de trabajo: eso lo hace decide."
visibility: public
language: es
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, abhaengigkeiten, ascii-graph, decision-path, visualisierung, routing, widerspruchs-erkennung]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-draw, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: 68422f7ca7043f158883734f79aadf21f8830b6238588a896255dccd8abc952a
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T14:40:54.042972+00:00"
---
<img src="banner.png" width="100%" alt="decision-path banner">

# decision-path — Grafo de dependencias en ASCII de decisiones abiertas

> Las decisiones no se toman en el vacío. Lo que, aislado, parece razonable
> a menudo bloquea trabajos posteriores, requiere etapas previas incompletas
> o anula contratos de protección existentes. decision-path hace visibles en
> el terminal las causalidades, secuencias y contradicciones.

---

## Cuándo usarla

- Hay un inventario de decisiones abiertas (de [decision-briefing](../decision-briefing/SKILL.md) fase 1, de un contexto de sesión o de una plantilla de decisiones) que debe estructurarse.
- Hay que aclarar qué decisiones pueden tomarse de inmediato (nodos raíz) y cuáles dependen de condiciones previas o de bloqueos externos.
- Se necesita una visión general de qué recomendaciones armonizan entre sí y dónde dos resoluciones se contradicen lógica u organizativamente.
- Palabras desencadenantes: `/decision-path`, "qué decisiones dependen unas de otras", "grafo de dependencias de las decisiones", "visualizar la ruta de decisión", "árbol de decisiones ASCII", "contradicciones entre decisiones", "revisar causalidades".
- **No** usarla:
  - Para capturar e inventariar por primera vez preguntas abiertas: eso lo hace [decision-briefing](../decision-briefing/SKILL.md) fase 1.
  - Para agrupar las variantes recomendadas en una imagen global coherente para su aprobación: eso lo hace [decision-draw](../decision-draw/SKILL.md).
  - Para bloques compactos de cinco puntos por decisión con opciones y pro/contra por opción: eso lo hace [decision-shot](../decision-shot/SKILL.md).
  - Para la elaboración metódica de una sola pregunta compleja (puntuación ponderada, escenarios): eso lo hace [decide](../decide/SKILL.md).

---

## Delimitación dentro de la familia de decisiones

| Skill | Tarea | Entrada | Salida |
|---|---|---|---|
| `decide` | Elabora **una sola** decisión metódicamente | Criterios, opciones | Matriz de evaluación, decisión individual |
| `decision-briefing` | **Descompone muchas** decisiones abiertas en preguntas individuales con opciones | Lista de puntos abiertos | Briefing numerado A/B/C/D, marcas gruesas, registro |
| `decision-path` | **Valida y visualiza causalidades y contradicciones** entre muchas decisiones | Marcas gruesas del briefing / registro | Grafo de dependencias ASCII con 5 valoraciones por nodo y estado de aristas |
| `decision-draw` | **Agrupa las recomendaciones en una imagen global** para su aprobación como conjunto | Paquete de `decision-path` | Concepto, interacción (solo variante recomendada), retrotransferencia |
| `decision-shot` | Comprime **análisis terminados** a lo esencial (1 decisión o un grupo reducido) | 1 pregunta analizada o grupo | Resumen de cinco partes con opciones, pro/contra y enlace al análisis completo |
| `decision-avatar` | Proporciona el **modelado de preferencias del usuario** | Contexto, resoluciones previas | Valoración de confianza 🟢 / 🟡 / 🔴 |

### Contrato y competencia frente a decision-briefing

`decision-briefing` fase 1 ya identifica de forma aproximada dependencias y secuencias al leer el material (por ejemplo, a partir de palabras clave como "Después automáticamente:", bloqueos o referencias a tickets). `decision-path` no deduce de nuevo esa estructura en silencio, sino que se basa directamente en estas marcas gruesas:

1. **decision-briefing aporta las marcas gruesas:** Proporciona el inventario bruto de decisiones abiertas y sus primeras señales de acoplamiento.
2. **decision-path valida, evalúa y visualiza:** Contrasta las señales con el estado real de la evidencia, separa aristas confirmadas de aristas supuestas, asigna las cinco valoraciones por nodo y detecta sin contemplaciones las colisiones con compuertas.
3. **Retroalimentación ante discrepancias:** Si `decision-path` encuentra una dependencia que falta en el briefing o estaba incompleta, nunca la incorpora en silencio, sino que la devuelve como nota de corrección al briefing.

---

## Las cinco valoraciones por nodo (y estado de evidencia de las aristas)

Las cinco dimensiones `[S E U Z W]` valoran los **nodos** (las decisiones pendientes o cerradas en el contexto sistémico). Las aristas llevan su tipo de relación semántica (por ejemplo, desbloquea, bloquea, presupone) y su estado de evidencia (confirmado frente a supuesto).

Cada nodo del grafo lleva una línea de valoración compacta con exactamente cinco dimensiones:

```
[S+ E:<Option> U<Richtung><Konfidenz> Z+ W-]
```

1. **razonable (`S`)** — Solidez técnica y arquitectónica:
   - `S+`: La solución es robusta, resuelve un problema real y evita complejidad innecesaria.
   - `S~`: Parcialmente razonable, pero conlleva riesgos de mantenimiento o de proceso.
   - `S-`: Solución aparente, activismo o callejón sin salida conocido (p. ej., un filtro aplicado en la palanca equivocada).

2. **recomendado (`E`)** — La recomendación de acción concreta y basada en hechos:
   - `E:<Option>`: Opción clara (p. ej., `E:A`, `E:B`, `E:klaeren`, `E:Schritt1`).
   - `E-`: No es posible recomendar (por ejemplo, por falta de hechos o por una cuestión de principio real).

3. **propio del usuario (`U`)** — Coincidencia con la forma de trabajar y las reglas del usuario (mediante `decision-avatar`):
   Codifica por separado la **dirección** (¿encaja la opción con la forma de trabajar?) y la **seguridad de la evidencia / confianza**:
   - **Dirección (primer carácter tras U):**
     - `+`: Propio del usuario — coincide con decisiones históricamente documentadas, directrices (`CLAUDE.md`, políticas) o preferencias explícitas del usuario.
     - `~`: Neutral / abierto — no se puede acreditar una dirección de preferencia marcada.
     - `-`: Ajeno al usuario — rompe con la forma de trabajo habitual o con los patrones previos del usuario.
   - **Seguridad de la evidencia / confianza (segundo carácter):**
     - En el grafo ASCII puro:
       - `!`: Alta / confirmada (en prosa: 🟢 acreditado).
       - `~`: Media / plausible (en prosa: 🟡 decisión de valoración, requiere la ponderación del usuario).
       - `?`: Baja / no confirmada (en prosa: 🔴 terreno nuevo, cuestión de principio). **¡Escalar en lugar de adivinar!**
   - *Ejemplos:* `U+!` (propio del usuario y acreditado), `U+~` (propio del usuario, pero asunto de ponderación), `U-!` (acreditado pero ajeno al usuario), `U~?` (abierto, sin indicación → escalar).

4. **compatible (`Z`)** — Encaje suave, estilístico y arquitectónico con los nodos vecinos:
   - `Z+`: Encaja sin fisuras en estilo y arquitectura; forma un conjunto coherente sin fricción.
   - `Z~`: Ligera fricción estilística o esfuerzo organizativo adicional, pero funcionalmente compatible.
   - `Z-`: Roza de forma notable con el conjunto del sistema (p. ej., proliferación de configuraciones, acoplamiento deficiente, ruptura de paradigma), pero aún no vulnera ninguna regla estricta.

5. **contradictorio (`W`)** — Contradicción dura y vulneración de reglas o compuertas (**salida más importante — ¡alarma!**):
   - `W-`: Sin contradicciones con otras recomendaciones, directrices vinculantes ni compuertas de protección activas.
   - `W+`: **Colisión dura / ¡alarma!** Anula otra recomendación, vulnera una política vinculante (`CLAUDE.md`, P-00x) o ignora una compuerta de protección activa. Los nodos en colisión deben figurar siempre en la sección `WIDERSPRUECHE` con causa y vía de resolución.

---

## Tipos de arista y reglas de derivación

Las dependencias se derivan **estrictamente de los textos fuente**, nunca se inventan de forma especulativa. Las aristas llevan su tipo de relación y su estado de evidencia:

| Señal en el texto | Tipo de arista | Notación | Significado |
|---|---|---|---|
| "Después automáticamente: …", "libera", "posibilita" | Desbloquea | `+-->` | La decisión de destino solo se puede ejecutar cuando se resuelve la de origen (confirmado) |
| "bloquea", "impide", "la compuerta de protección se aplica" | Bloquea | `=>` | El destino está bloqueado mientras no se resuelva el origen |
| "presupone", "requiere antes", "condición previa" | Presupone | `-->` | El destino exige cronológica y lógicamente la decisión de origen |
| "decisión posterior", "paso 2 después" | Secuencia | `-->` | Paso lógico posterior a la ejecución |
| "refutado por medición", "superado", "carece de objeto" | Invalida | `--X-->` | El conocimiento de origen vuelve obsoleta la partida de destino |
| Mismo ID de decisión, mismo ID de ticket o mismo sistema sin prueba textual | Supuesto | `?-->` | Acoplamiento plausible sin prueba causal explícita (no acreditado) |

> **Regla para aristas no acreditadas:**
> Cuando no existe en el texto una prueba causal explícita, la arista se marca como supuesta (`?-->`), nunca como hecho confirmado. Cuando no está acreditada ninguna relación, los nodos aparecen uno junto a otro sin conexión.

---

## Requisitos de formato para el grafo ASCII

1. **Monoespaciado y apto para terminal:** Ancho máximo de línea **100 columnas**. Nada de tablas anchas que se partan en el terminal.
2. **Juego de caracteres y pureza:** ASCII puro. Dentro del bloque de código del grafo no pueden aparecer emojis (🟢🟡🔴); las confianzas se codifican allí exclusivamente con caracteres ASCII (`!`, `~`, `?`).
3. **IDs de nodo:** Únicamente abreviaturas existentes (`PD-A`, `MD-A`, `BH-A`, `VM-A`, `QR-A`, `CL-A`, `MO-A`, `D-001`, `732597768`). ¡Nunca inventar IDs nuevos! Si falta una abreviatura, se usa el número de posición. Los pasos internos de seguimiento se registran como anotaciones sin numerar `(...)` junto a la arista.
4. **Estructura por niveles:**
   - `EBENE 0 - haengt an nichts`: Nodos raíz, decisiones desbloqueadas, palancas externas.
   - `EBENE 1 - haengt an genau einer`: Decisiones consecuentes directas.
   - `EBENE 2 - haengt an mehreren / tiefe Kette`: Nodos con dependencias múltiples o posteriores.
   - `WIDERSPRUECHE`: Contradicciones duras, colisiones con compuertas y recomendaciones inconsistentes (`W+`).
   - `LEGENDE`: Componente obligatorio de cada grafo. Todo carácter estructural usado en el grafo (`|`, `=Option`, `(...)`, flechas de arista) debe aparecer en la leyenda y quedar explicado.
5. **Proyección Mermaid opcional:** Puede añadirse, si es necesario, como bloque de código adicional (`mermaid`) cuando no suponga esfuerzo extra. El grafo ASCII sigue siendo la salida principal vinculante.

---

## Ejemplo (extracto piloto: Ticket-Master 2026-09-13)

Extracto real de la plantilla de decisiones del Ticket-Master (`732597768`, `MO-A`, `CL-A`, `QR-A`, `387521104`, `CL-B`):

```
====================================================================================================
DECISION-PATH: ABHAENGIGKEITSGRAPH (Pilot Ticket-Master 2026-09-13)
====================================================================================================

EBENE 0 - haengt an nichts (Wurzelentscheidungen & externe Blocker)
  [732597768] GitHub-Billing klaeren                        [S+ E:klaeren U+! Z+ W-]
      |  schaltet frei
      +--> [MO-A] Welle 2 freigeben                         [S+ E:A       U+~ Z+ W-]

  [CL-A] clutch Admin-Merge PR #6 & PR #8                   [S+ E:A       U+! Z+ W-]
      |  blockiert durch: [Gate "1 Approving Review" (Self-Approval unmoeglich)]
      --> (Folgeentscheidung: Branchschutz auf 0 oder Bot anpassen)

  [QR-A] Queue-Rename Junction (_TICKETS -> TICKETS)        [S+ E:B       U+! Z+ W-]
      +--> [387521104] Nachtfenster faehrt                  (belegt: nur unter B)

  [CL-B] Review-Gate-Pilot: Mac-Signierschluessel           [S+ E:Schritt1 U+~ Z+ W-]
      --> (Folgeschritte 2-4: Modell-Automatisierung nach Schluessel-Bereitstellung)

EBENE 1 - haengt an genau einer Vorbedingung
  [MO-A] Welle 2 freigeben                                  [S+ E:A       U+~ Z+ W-]
      |  setzt voraus: [732597768] (Billing geklaert, Remote-CI-Gates wieder aktiv)
      |  setzt voraus: [Gate PRIVATE.txt "gruenes Remote-CI"]
      --> (Folgeschritt: Sichtbarkeit schalten bleibt reine Nutzerhandlung)

EBENE 2 - haengt an mehreren / tiefe Kette
  [387521104] Nachtfenster Migration autonom fahren         [S+ E:B       U+! Z+ W-]
      |  setzt voraus: [QR-A]=B (NTFS-Junction gesetzt)
      |  setzt voraus: (Junction auf dem zweiten Host per Transfer-Ticket gesetzt -
      |                  Ticketnummer in der Vorlage nicht genannt)

----------------------------------------------------------------------------------------------------
WIDERSPRUECHE & GATE-KOLLISIONEN
----------------------------------------------------------------------------------------------------
  [MO-A]=B  X  [Gate PRIVATE.txt "gruenes Remote-CI"]
               Konflikt: Option B wuerde Welle 2 rein auf lokaler Testbasis freigeben,
               obwohl zwei Modulvertraege ausdruecklich gruenes Remote-CI fordern.
               Aufloesung: Empfehlung A erzwingt erst [732597768] (Billing), heilt Kollision.

  [CL-A]=StatusQuo  X  [Gate "1 Approving Review" (Self-Approval unmoeglich)]
               Konflikt: master verlangt 1 Review, einziges Repo-Konto ist lukisch.
               Aufloesung: Empfehlung A (Admin-Merge) bricht Blockade legitim auf.

----------------------------------------------------------------------------------------------------
LEGENDE & BEWERTUNGSSCHLUESSEL
----------------------------------------------------------------------------------------------------
  Kanten & Struktur:
    +-->   schaltet frei (Kausalitaet im Quelltext belegt)
    =>     blockiert / verhindert (Gate oder externer Blocker)
    -->    setzt voraus / Reihenfolge (Vorbedingung oder Folgeschritt)
    ?-->   vermutete Abhaengigkeit (Koppelung plausibel, aber unbelegt)
    --X--> entwertet / ueberholt (macht Zielposten obsolet)
    X      Widerspruch / Kollision (Gate- oder Regelverletzung)
    |      vertikaler Verbindungsstrang / Attribut-Zuordnung
    [ID]   Entscheidungsknoten (Kuerzel oder Postennummer aus Vorlage)
    [Gate]  externes Gate / Regel / Vertrag - KEIN Entscheidungsknoten
    =Opt   spezifische Option eines Knotens (z. B. [MO-A]=B)
    (...)  unnummerierte Kanten-Annotation / Folgeschritt (keine neue ID)

  Knoten-Status [S E U Z W]:
    S: Sinnvoll      (+ tragfaehig / ~ mit Vorbehalt / - ungeeignet)
    E: Empfohlen     (A, B, C, klaeren, Schritt1, - keine Empfehlung)
    U: Usertypisch   (Richtung: + typisch / ~ neutral / - untypisch;
                      Konfidenz: ! gesichert / ~ Abwaegung / ? Eskalation)
                      [! = belegt (Prosa gruen), ~ = Nutzerabwaegung (Prosa gelb),
                       ? = ungesichert / Eskalation (Prosa rot)]
    Z: Zusammenpass. (+ harmoniert stilistisch / ~ Reibung / - Architektur-Bruch)
    W: Widerspruch   (- widerspruchsfrei / + harte Kollision mit Gate oder Regel)
====================================================================================================
```

---

## Lo que decision-path NO hace

1. **No toma decisiones:** La skill ofrece una cartografía transparente de la situación. La capacidad de decidir sigue en manos del usuario.
2. **No elabora opciones:** La skill no debate variantes nuevas ni catálogos de criterios; eso corresponde a [decide](../decide/SKILL.md) o [decision-briefing](../decision-briefing/SKILL.md).
3. **No escribe en el registro:** El grafo no modifica archivos de registro ni de tickets. La actualización tras una decisión la realiza [decision-briefing](../decision-briefing/SKILL.md) fase 4 o el mecanismo de retrotransferencia de [decision-draw](../decision-draw/SKILL.md).
4. **No usa abreviaturas crípticas en el texto dirigido al usuario:** Cuando se explican al usuario los resultados del grafo, rige la regla de estilo vinculante (T-20260913-883789445): 2–4 frases en lenguaje cotidiano en primera persona (situación, "Hago …", alternativa de respaldo). Las etiquetas de los nodos usan títulos cortos legibles. Los identificadores técnicos y los números de ticket van a una tabla de anexo.

---

## Procedencia de la sesión

Cuando el grafo de dependencias se guarda como artefacto de análisis duradero, el documento termina con:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Prioridad de fuentes: indicación explícita de ejecución o CLI; después, entorno o hook del proveedor autorizado; en caso contrario, `unbekannt`.
- Los subagentes heredan el ID de sesión de la sesión padre.
- El chat rutinario y las salidas temporales de terminal no reciben sello.

---

## Registro de cambios

### 1.1.0 (2026-09-18)
- Regla de estilo para textos de decisión comprensibles anclada (T-20260913-883789445, instrucción del usuario 2026-09-13):
  - Explicaciones al usuario en primera persona natural, sin avalancha de números.
  - Títulos cortos legibles para los nodos del grafo de terminal.
  - Asignación técnica (números de ticket / D) trasladada a una tabla de anexo.

### 1.0.0 (2026-09-13)
- Versión inicial basada en el encargo del usuario T-20260913-107991667.
- Clave de valoración de cinco partes por nodo (razonable, recomendado, propio del usuario con dirección y confianza separadas mediante `decision-avatar`, compatible, contradictorio); las aristas llevan tipo de relación y estado de evidencia.
- Contrato vinculante con `decision-briefing`: el briefing aporta las marcas gruesas, decision-path valida y visualiza; retroalimentación ante discrepancias.
- Delimitación clara frente a `decision-shot` en cuanto al formato de salida (cinco partes compactas con opciones y pro/contra).
- Corrección de la estructura causal: CL-A en la compuerta de aprobación en lugar de facturación; eliminación de IDs inventados a favor de anotaciones de arista sin numerar.
- Especificación ASCII coherente (máx. 100 columnas) con notación de arista unificada `--X-->`, leyenda estructural completa y código del grafo libre de emojis.
