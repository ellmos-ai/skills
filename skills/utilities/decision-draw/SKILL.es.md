---
name: decision-draw
version: 1.1.0
type: skill
author: Lukas Geiger + agy
created: 2026-09-13
updated: 2026-09-18
description: "Condensa decisiones abiertas agrupadas en UN concepto general coherente y basado en prosa, a partir de todas las variantes recomendadas. Muestra cómo se interrelacionan concretamente los subsistemas tras la implementación, en lugar de obligar al usuario a responder docenas de preguntas aisladas. El usuario acepta la imagen en su conjunto o da correcciones dirigidas, que se traducen automáticamente en decisiones individuales y se reescriben en el registro mediante la fase 4 de decision-briefing. Usa esta habilidad con frases como \"¿cómo se vería todo si aceptáramos todo?\", \"dibújame la imagen completa\", \"concepto general de las decisiones\", \"decision draw\", /decision-draw, \"¿cómo encajan los sistemas entre sí?\". NO la uses si se quieren discutir alternativas por cada punto individual; eso lo hace decision-briefing. NO para el grafo de dependencias; eso lo hace decision-path. NO para bloques estructurados individuales con opciones y pros/contras (incluso en grupos estrechamente relacionados); eso lo hace decision-shot. NO para derivar una decisión individual; eso lo hace decide."
visibility: public
language: es
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [entscheidung, konzeptbild, gesamtabnahme, buendelung, zusammenspiel, ruecktransfer, workflow]
status: active
dependencies:
  tools: []
  services: []
  modules: [decide, decision-briefing, decision-path, decision-shot, decision-avatar]
provenance:
  origin: "custom"
  decision_ref: "T-20260913-107991667 (Ticket-Master, Nutzerauftrag 2026-09-13)"
translated_from_sha256: da661fa325502ab0dfae6d6655d70650457d6ac1ff27ca5f0ce6289c375ef2c8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:42.485190+00:00"
---
<img src="banner.png" width="100%" alt="decision-draw banner">

# decision-draw — Imagen general y aceptación de decisiones agrupadas

> Cuando hay cinco o diez decisiones pendientes, es fácil perder de vista el sistema que se está creando entre las opciones de detalle. decision-draw no describe las alternativas, sino el conjunto funcionando: ¿cómo trabajan juntos los sistemas si se aceptan todas las recomendaciones? El usuario acepta la imagen en su conjunto o la corrige de forma dirigida.

---

## Cuándo usarlo

- Varias decisiones relacionadas (de [decision-briefing](../decision-briefing/SKILL.md) o de una plantilla de decisiones) no deben tratarse como un catálogo tedioso de preguntas individuales.
- El usuario quiere ver, antes de decidir, cómo interactuarán realmente los componentes en el uso cotidiano tras la implementación.
- Del grafo de dependencias ([decision-path](../decision-path/SKILL.md)) se ha identificado un bloque de decisiones estrechamente acopladas que puede aceptarse como unidad funcional.
- Palabras desencadenantes: `/decision-draw`, "¿cómo se vería todo si aceptáramos todo?", "dibújame la imagen completa", "concepto general de las decisiones", "decision draw", "¿cómo encajan entonces los sistemas?", "imagen para la aceptación global".
- **No** usarlo:
  - Si el usuario quiere sopesar opciones individuales por pregunta y elegir por letra (A/B/C): eso lo hace [decision-briefing](../decision-briefing/SKILL.md).
  - Para el puro análisis causal y de bloqueos en la terminal: eso lo hace [decision-path](../decision-path/SKILL.md).
  - Para la ponderación aislada de opciones en bloques individuales de 5 partes (contexto, pros/contras por opción, recomendación) para preguntas individuales o grupos estrechamente relacionados: eso lo hace [decision-shot](../decision-shot/SKILL.md).
  - Para la elaboración metódica de una única cuestión fundamental abierta: eso lo hace [decide](../decide/SKILL.md).

---

## Delimitación dentro de la familia de decisiones

| Habilidad | Enfoque UX | Postura ante las opciones | Forma de aceptación |
|---|---|---|---|
| `decision-briefing` | **Descompone** en preguntas individuales | Muestra todas las opciones A/B/C/D | Códigos de letra (`1A 2C 3B`) |
| `decision-path` | **Estructura** las causalidades | Evalúa las opciones en el grafo | Diagnóstico en la terminal (ASCII) |
| `decision-draw` | **Imagen objetivo coherente** (agrupa decisiones interconectadas) | Describe **solo la variante recomendada** (las alternativas están enlazadas) | Aceptación global o frase de corrección |
| `decision-shot` | **Bloques individuales estructurados** (para preguntas individuales o grupos estrechos) | Muestra opciones con 2–4 pros/contras | Decisión ejecutiva / aceptación individual |
| `decide` | **Elabora** el caso individual | Matriz de evaluación (criterios) | Recomendación analítica |

> **Regla central:**
> `decision-draw` describe **exclusivamente la variante recomendada**. Las alternativas descartadas no han desaparecido: están documentadas en [decision-briefing](../decision-briefing/SKILL.md), [decision-shot](../decision-shot/SKILL.md) o en los tickets enlazados, y se referencian en el encabezado. Un draw sin esta referencia quitaría al usuario la elección, en lugar de facilitársela.

---

## Regla de estilo vinculante: textos para el usuario sin códigos ni números

> **Instrucción canónica del usuario (comentario del 2026-09-13 / ticket T-20260913-883789445):**
> *"Los decision draws me resultan demasiado técnicos, tiene que ser sin número; tú los conoces en segundo plano o los usas para redactar el texto [...]."*

1. **Sin códigos técnicos en el texto visible para el usuario:**
   En el texto visible para las personas (paquete, concepto, interacción, implementación, consulta) **no** aparecen códigos internos (como `BH-A`, `MD-A`, `HA-A`, `PRA`), números de ticket (`T-2026...`), números D (`D-2026...`), rutas relativas, hashes de Git ni valores de medición.
2. **2–4 frases en lenguaje cotidiano y en primera persona por cada punto:**
   Cada punto del paquete se formula según la tríada:
   - *Situación:* ¿cuál es el punto de partida actual?
   - *"Hago …":* ¿qué planeo concretamente / cuál es mi recomendación de acción?
   - *Plan B:* ¿qué pasa si esto fracasa o qué decide el usuario después?
   *(Ejemplo: "Hermes solo admite tareas en inglés. Lo reporto a Hermes como issue y para nosotros construyo una solución alternativa. Ahora mismo hay sesiones anteriores que no se pueden usar. Intento volver a hacerlas utilizables. Si no funciona, te doy una muestra aleatoria de 10 sesiones y la resumo, así puedes decidir si merece la pena rescatarlas.")*
3. **Títulos en lenguaje claro para orientarse:**
   Cada punto lleva un título comprensible en lenguaje claro (p. ej., *"Backend de modelos como núcleo propio"*, *"Claves de despliegue seguras en el Mac"*). El usuario interactúa a través de ese título o da una aceptación global.
4. **Asignación técnica exclusivamente en el anexo:**
   La correspondencia entre título en lenguaje claro, código interno, ID de ticket y estado en el registro se realiza **exclusivamente en una tabla anexa final** al término del documento. Solo allí actúan los analizadores automáticos y los mecanismos de reescritura del registro.

---

## Estructura vinculante (ocho partes)

Un `decision-draw` completo sigue sin excepción esta estructura:

### 1. Paquete y alcance (en lenguaje claro)
Resumen de los puntos agrupados en lenguaje cotidiano (primera persona, 2–4 frases por punto, sin IDs ni códigos en el texto).

### 2. Concepto
El estado objetivo deseado como texto coherente en prosa:
- ¿Qué panorama de sistemas o qué flujo de trabajo surge si todas las recomendaciones se implementan exactamente así?
- Sin contraposición de opciones, sin convivencia de subjuntivos ("se podría también").
- Indicativo claro y preciso: así funciona el sistema en el estado objetivo.

### 3. Interacción
El núcleo funcional de la habilidad:
- ¿Cómo se entrelazan realmente las partes decididas **después** de la implementación?
- Presentación preferentemente a lo largo de un flujo concreto de principio a fin, en lugar de una mera lista de componentes.
- Hace tangibles los flujos de datos, las interfaces y las responsabilidades.

### 4. Implementación
El orden concreto de realización:
- ¿Qué ocurre realmente en la práctica?
- Toma directamente la lógica de aristas y dependencias de [decision-path](../decision-path/SKILL.md).
- Las líneas de trabajo independientes se presentan honestamente como paralelas (no se inventan cadenas causales artificiales; un paquete puede constar de varias líneas paralelas). Los órdenes solo se afirman donde existen dependencias o plazos documentados.
- Nombra puertas de control, pasos de migración y verificaciones.

### 5. Lo que esta imagen no cubre
Protección frente a una falsa completitud:
- ¿Qué cuestiones marginales, puntos abiertos o confianzas 🔴 quedan deliberadamente fuera?
- ¿Dónde están los límites de interfaz con los sistemas vecinos?
- Una imagen que calla sus bordes genera una falsa sensación de seguridad.

### 6. Aceptación
La interacción con el usuario:
- El usuario revisa la imagen en su conjunto.
- Opción de respuesta 1: **aceptación global expresa** ("Así está bien", "Aceptado", "Implementémoslo así"). Solo en este caso se registran como decididos todos los puntos del paquete.
- Opción de respuesta 2: **corrección mediante título en lenguaje claro o en lenguaje cotidiano** ("En el despliegue en el Mac mejor sin reinicio automático", "Aplacemos de momento el VersicherungsManager"). Conduce a la descomposición en decisiones individuales; todos los puntos no corregidos siguen abiertos.

### 7. Retorno
La traducción sistemática de las correcciones del usuario en decisiones individuales:
- **Sin contabilización automática:** solo con aceptación global expresa se registran los puntos no modificados. Una corrección parcial **no** es una aceptación global.
- **Aislamiento en las correcciones:** si llega una corrección, se descompone en decisiones individuales; todos los demás puntos del paquete permanecen estrictamente **abiertos** (en el registro de origen / la plantilla) hasta que el usuario acepte la imagen depurada en su conjunto o confirme los puntos restantes uno a uno.
- **Tabla obligatoria del retorno:** cada respuesta de corrección genera necesariamente una tabla de evaluación estructurada con cuatro columnas (corrección original, códigos afectados, estado del efecto dominó, ambigüedades abiertas).
- **Vía de escritura exclusiva mediante la fase 4:** `decision-draw` **no** tiene vía de escritura propia en el registro. El registro se realiza **exclusivamente** mediante el procedimiento estandarizado de la fase 4 de [decision-briefing](../decision-briefing/SKILL.md).

### 8. Anexo: tabla técnica de referencia (solo para registro y auditoría)
Tabla compacta al final del documento con:
`| Klartext-Titel | Internes Kürzel / ID | Ticket-Referenz | Unterstellte Empfehlung | Konfidenz | Link / Details |`

---

## Ejemplo (extracto piloto: Ticket-Master 2026-09-13 — BACH y conjunto de sistemas)

```markdown
# DECISION-DRAW: BACH-Kernverbund & Betriebsintegrität

## 1. Bündel und Umfang

- **Modell-Backend als eigenes Herzstück:** Die Modellzuteilung ist aktuell eng mit dem Monolithen verzahnt. Ich lagere das Backend als eigenständiges Kernmodul aus, damit Rechte und Budgets unabhängig geprüft werden. Scheitert ein externer Dienst, schaltet das System automatisch auf das lokale Reservemodell zurück.
- **Sichere Deploy-Schlüssel auf dem Mac:** Auf dem Mac laufen Dauerprozesse, die bei harten Updates unsauber abbrechen können. Ich richte einen lesenden Schlüssel und ein Meldeskript ein, das Aktualisierungen anzeigt, ohne laufende Dienste abzuschießen. Sollte ein Dienst dennoch hängen, meldet der Watcher das direkt an die Betriebsübersicht.
- **Einheitliche Konfigurations-Sollwerte:** Die beiden Hauptrechner nutzen teilweise unterschiedliche Spracheinstellungen. Ich gleiche die Konfigurationen über das gemeinsame Sync-Verzeichnis an, lasse dem Laptop aber ausreichend Spielraum für mobile Tests.
- **Feste Zeitzone im VersicherungsManager:** Datumsberechnungen bei Fristen hängen bisher vom Betriebssystem ab. Ich verankere eine feste Zeitzone in den Anwendungseinstellungen, damit Fristen überall auf die Minute genau übereinstimmen.
- **Öffentliche Bereitstellung der USMC-Dokumentation:** Die Modul-Dokumentation ist im Webauftritt noch als privat markiert und löst Prüfwarnungen aus. Ich korrigiere die Sichtbarkeit auf öffentlich, damit der nächtliche Seiten-Bau ohne Fehler durchläuft.

---

## 2. Konzept

Wir etablieren ein sauberes, entkoppeltes Multi-Host-System, bei dem das Modell-Backend
als eigenständiges Kernmodul `agents-heart` betrieben wird. Rechte und Budgets liegen
strukturiert in einer SQLite-Datenbank, während Zuteilungsentscheidungen zweistufig
fallen: BACH ermittelt fachlich fundiert die Kandidatenmenge, clutch wählt darin
preis- und kapazitätsoptimal das finale Modell.

Auf dem Mac Studio laufen die 24/7-Dienste geschützt und stabil über einen read-only
Deploy-Key; Updates ziehen automatisch ein, benachrichtigen den Operator bei laufenden
Diensten aber sanft, statt Hintergrundprozesse hart abzuschießen. Konfigurationen
dürfen dort bewusst hostspezifisch auf Leistung abgestimmt sein, während app-weite
Einstellungen (wie Zeitzonen im VersicherungsManager nach dem bewährten routinika-Muster)
deterministisch fest verdrahtet sind. USMC bleibt der kanonische öffentliche
Memory-Baustein und behält seinen festen Platz im Webauftritt.

---

## 3. Zusammenspiel

Die fünf Posten bilden keine serielle Kausalkette, sondern stellen modular entkoppelte Bausteine der täglichen Betriebsintegrität dar, die im Gesamtsystem parallel ineinandergreifen:

- **Kernarchitektur & Modell-Routing (`BH-A`):** Das Modul `agents-heart` entkoppelt die Modellzuteilung. Trifft eine Aufgabe ein, ermittelt BACH fachbezogen die Kandidatenmenge und clutch wählt kosten- und kapazitätsoptimal das Modell.
- **Host-Konfiguration & Deploy-Integrität (`CF-A`, `MD-A`):** Während auf dem Laptop und der Workstation konsistente Reasoning-Stufen gelten (`CF-A`; hostabhängige Modelle bleiben transparent), betreibt der Mac Studio seine persistenten Hintergrundprozesse unter validierten Einstellungen. Bei Aktualisierungen zieht der Mac den Code via Read-only Deploy-Key (`MD-A`); der GUI-Server startet neu, während langlebige 24/7-Dienste den Update-Bedarf sanft an das Dashboard melden.
- **Domänen-Persistenz & Fristen (`VM-A`):** Applikationen wie der VersicherungsManager schreiben Fristen und Deadlines gegen eine app-weite `settings`-Tabelle nach routinika-Muster. Zeitrechnungen und Deadline-Projektionen operieren über alle Profile hinweg deterministisch auf derselben IANA-Zeitzone.
- **Öffentlicher Auftritt (`PD-A`):** Der nächtliche Seiten-Builder validiert den Zustand der Repositories. USMC wird mit korrigierter `public`-Deklaration fehlerfrei publiziert, ohne Warnungen in den Sicherheits-Gates auszulösen.

---

## 4. Umsetzung

Da die Vorlage für diese fünf Posten im Abhängigkeitsgraphen ([decision-path](../decision-path/SKILL.md)) keine serielle Kette vorgibt, erfolgt die Umsetzung ehrlich in vier voneinander unabhängigen, parallelen Arbeitssträngen (Ausweg a: parallele Stränge statt erfundener Kausalität). Eine sequenzielle Reihenfolge gilt nur dort, wo externe Fristen oder interne Schritte belegt sind:

- **Strang A (Termingebunden — Frist 2026-09-14):**
  1. USMC-Metadaten auf `public` nachziehen (`PD-A`); Draft-PR #2 verwerfen. Duldet wegen des nächtlichen Builder-Laufs keinen Aufschub, ist technisch jedoch von allen anderen Strängen unabhängig.
- **Strang B (Host-Konfiguration & Mac-Deploy — parallel ausführbar):**
  1. B1: Sollwerte in `.SYNC` festschreiben (`CF-A`), Reasoning-Stufe `high` für beide Hosts synchronisieren.
  2. B2 (unabhängig von B1): Read-only Deploy-Key auf Mac Studio hinterlegen und Pull-and-Report-Skript einrichten (`MD-A`).
- **Strang C (Domänen-Datenbank — parallel ausführbar):**
  1. Migration der app-weiten `settings`-Tabelle im VersicherungsManager nach routinika-Vorbild implementieren (`VM-A`), um die saubere Basis für den nachgelagerten Publisher-Bau zu schaffen.
- **Strang D (Architektur-Herauslösung — interner Mehrstufenplan):**
  1. D1: SQLite-Schema für Rollen und Budgets in `agents-heart` anlegen (`BH-A` E1).
  2. D2: Backend-Katalog als Python-Modul ausgründen (`BH-A` E3) und clutch-Seam für Zuteilung binden (`BH-A` E2).
  3. D3: Modul `agents-heart` final herauslösen und anbinden (`BH-A` E5, E6).

---

## 5. Was dieses Bild nicht abdeckt

- **Task-Claiming Race Condition:** Der Integritätsfehler bei doppeltem Task-Claim läuft
  in einem separaten Hotfix-Ticket und ist nicht Teil dieser Freigabe.
- **Cockpit-Frontend:** Das Monitoring-Cockpit (`BH-A` E4) wird bewusst noch nicht gebaut,
  solange das Backend nicht produktiv meldet.
- **Sichtbarkeitsschaltung nach außen:** Reine Bereitstellung von Code schaltet keine
  neuen Repos public; die finale Freigabe bleibt dem Nutzer vorbehalten.

---

## 6. Abnahme

Du kannst diesen Systemverbund als Ganzes abnehmen oder in Alltagssprache korrigieren:

- **Ausdrückliche Gesamtabnahme:** „Passt so, genau so umsetzen.“ (Nur dies führt zur Verbuchung aller Posten).
- **Korrektur-Beispiele:**
  - *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* (Mehrfachtreffer)
  - *„BH-A E5 lieber ocean-heart nennen statt agents-heart.“*
  - *„VM-A erst mal vertagen, der Publisher hat noch Zeit.“*

---

## 7. Rücktransfer

Wird das Gesamtbild abgenommen oder korrigiert, übersetzt der Skill die Rückmeldung:

### Fall A: Ausdrückliche Gesamtabnahme
Nimmt der Nutzer das Gesamtbild ausdrücklich als Ganzes ab (z. B. *„Passt so, genau so umsetzen“*):
- Alle fünf Posten (`BH-A: 1A/2A/3A/4B/5A/6A`, `MD-A: A1`, `CF-A: 1C/2B/3B`, `VM-A: A`, `PD-A: A`) werden als GETROFFEN an [decision-briefing](../decision-briefing/SKILL.md) Phase 4 übergeben.
- Phase 4 übernimmt die Eintragung ins Register `DECIDED-AND-DONE.md` und aktualisiert die fünf Quelltickets.

### Fall B: Teilkorrektur mit Mehrfachtreffer
Gibt der Nutzer eine inhaltliche Korrektur ein, z. B.:
> *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“*

**1. Strukturierte Rücktransfer-Tabelle:**

| Originalkorrektur (Wortlaut des Nutzers) | Betroffene Kürzel | Domino-Status (welche abhängigen Knoten kippen dadurch) | Offene Mehrdeutigkeiten |
|---|---|---|---|
| *„Keine hostspezifischen Sonderwege auf dem Mac: MD-A braucht volles Schreibrecht (A2) für direkte Pushes, und CF-A soll alle Konfigurationen strikt an die Workstation angleichen (Gruppe 1=A, 2=A).“* | `MD-A`, `CF-A` *(Mehrfachtreffer: 1 Aussage bewegt 2 Posten)* | **`MD-A`:** Kippt von A1 auf A2. Erfordert SSH-Write-Key auf Mac Studio, Push-Rechte im GitHub-Repo `bach` und Sicherheitsprüfung des LaunchAgents.<br>**`CF-A`:** Gruppe 1 kippt von C auf A (Laptop-Claude-Desktop wird restriktiver). Gruppe 2 kippt von B auf A (`codex.model` wird starr angeglichen). Gruppe 3 bleibt B (`high`), da bereits synchron. | **`CF-A` Gruppe 1:** Nutzer verlangt Angleichung an Workstation (1=A) — Rückfrage nötig, ob die bisher bewusste Freizügigkeit auf dem Laptop wirklich entzogen werden soll.<br>**`MD-A`:** Unklar, ob Write-Key für alle Repos oder nur für `bach` gelten soll. |

**2. Status der unberührten Posten (Schutz vor ungefragtem Mitbuchen):**
- Die unveränderten Posten `BH-A`, `VM-A` und `PD-A` werden **nicht** gebucht!
- Sie verbleiben im Status **OFFEN** (`PENDING`) in der Vorlage bzw. im Register `TO-DECIDE-USER.txt`.
- Eine Teilkorrektur ist **keine** Gesamtabnahme. Erst wenn das nach Korrektur aktualisierte Gesamtbild vom Nutzer als Ganzes abgenommen wird oder die verbleibenden Punkte einzeln bestätigt werden, dürfen sie verbucht werden.

**3. Buchungsweg:**
- `decision-draw` besitzt keinen eigenen Schreibmechanismus.
- Übergeben wird an **[decision-briefing](../decision-briefing/SKILL.md) Phase 4** nur, was die Tabelle als eindeutig ausweist: `CF-A` Gruppe 2 = A und Gruppe 3 = B.
- **Nicht** übergeben werden `MD-A` und `CF-A` Gruppe 1 — für beide steht in der Spalte *Offene Mehrdeutigkeiten* eine Rückfrage. Eine Mehrdeutigkeit, die man vor der Buchung klären wollte, darf man nicht in derselben Runde als geklärt verbuchen.
- Phase 4 trägt die eindeutigen Teile mit Begründung in Ticket `T-20260913-947070291.txt` ein und aktualisiert `DECIDED-AND-DONE.md`. Ticket `T-20260913-799464688.txt` (`MD-A`) bleibt offen, bis die Rückfrage beantwortet ist.

---

## 8. Anhang: Technische Referenztabelle (nur für Buchung & Audit)

| Klartext-Titel | Internes Kürzel | Ticket / Quelle | Unterstellte Empfehlung | Konfidenz | Link / Details |
|---|---|---|---|---|---|
| Modell-Backend als eigenes Herzstück | `BH-A` | `T-20260913-896336887` | 1A / 2A / 3A / 4B / 5A / 6A | 🟢 | `docs/MODELL-BACKEND-KONZEPT_2026-09-13.md` |
| Sichere Deploy-Schlüssel auf dem Mac | `MD-A` | `T-20260913-799464688` | A1 + Skript (nur Melden für 24/7) | 🟢 | Ticket `T-20260913-799464688.txt` |
| Einheitliche Konfigurations-Sollwerte | `CF-A` | `T-20260913-947070291` | 1C (begründet) / 2B (hostabh.) / 3B (high) | 🟢 / 🟡 | Ticket `T-20260913-947070291.<HOST>.txt` |
| Feste Zeitzone im VersicherungsManager | `VM-A` | `T-20260906-496406575` | A (app-weite settings wie routinika) | 🟢 | Ticket `T-20260906-496406575.<HOST>.txt` |
| Öffentliche Bereitstellung der USMC-Dokumentation | `PD-A` | `T-20260913-609930207` | A (auf public nachziehen, Status quo) | 🟢 | Ticket `T-20260913-609930207.txt` |
```

---

## Reglas para la práctica

1. **Sin subjuntivo en el concepto:** describe el sistema global como si ya estuviera realizado. El usuario quiere claridad sobre el resultado, no eventualidades teóricas.
2. **Causalidad antes que cronología:** el orden en la sección *Implementación* sigue los niveles del grafo de dependencias de [decision-path](../decision-path/SKILL.md). Las líneas independientes se presentan honestamente como paralelas y no se doblan en una cadena causal artificial.
3. **Verificación explícita de efecto dominó en el retorno:** una corrección del usuario nunca debe registrarse de forma aislada sin comprobar si nodos dependientes del grafo quedan invalidados o afectados.
4. **Sin contabilización automática en correcciones parciales:** solo con aceptación global expresa se registran los puntos no modificados. En cada corrección parcial, todos los puntos no afectados permanecen estrictamente abiertos hasta que la imagen general se vuelva a liberar o los puntos se confirmen individualmente.
5. **Vía de escritura exclusiva mediante la fase 4:** `decision-draw` no tiene vía de escritura propia en el registro. Los registros se realizan sin excepción mediante la fase 4 de [decision-briefing](../decision-briefing/SKILL.md).
6. **Respeta los contratos del registro:** los registros siempre siguen las reglas del registro de decisiones (sin renumerar IDs, códigos de registro unívocos, destino canónico `DECIDED-AND-DONE.md`).
7. **Textos para el usuario sin números ni códigos técnicos:** en el texto visible para las personas no aparecen IDs, códigos, rutas ni números de ticket. Cada punto se formula en primera persona y lenguaje comprensible; todos los identificadores van a la tabla anexa.

---

## Procedencia de la sesión

Si un decision-draw se guarda como documento conceptual permanente, termina con:

`session: <session-id> | <agent>@<host> | YYYY-MM-DD`

- Prioridad de fuentes: indicación explícita de tiempo de ejecución o CLI; después, entorno o hook de proveedor autoritativo; si no, `unbekannt`.
- Los subagentes heredan el ID de sesión de la sesión padre.
- Las plantillas puras de chat no reciben sello.

---

## Registro de cambios

### 1.1.0 (2026-09-18)
- Regla de estilo para textos de decisión orientados al usuario anclada (T-20260913-883789445, instrucción del usuario del 2026-09-13):
  - Sin códigos técnicos, números de ticket o D, rutas ni valores de medición en el texto visible para el usuario.
  - 2–4 frases en lenguaje cotidiano y primera persona (situación, "Hago …", plan B) por punto.
  - Títulos claros y descriptivos para la identificación y la aceptación.
  - La asignación técnica (códigos, ID de ticket, estado de registro) se traslada estrictamente a la tabla anexa final (sección 8).

### 1.0.1 (2026-09-13)
- Revisión posterior:
  - Contrato de retorno endurecido: sin contabilización automática en correcciones parciales; los puntos no afectados permanecen estrictamente abiertos hasta la aceptación global.
  - Tabla obligatoria de retorno con 4 columnas (corrección original, códigos afectados, estado del efecto dominó, ambigüedades abiertas) introducida.
  - Coincidencias múltiples demostradas en el ejemplo (una corrección del usuario mueve `MD-A` y `CF-A` a la vez).
  - Vía de escritura exclusiva mediante la fase 4 de `decision-briefing` anclada en el contrato y en el ejemplo.
  - Error de suposición de cadena causal en el ejemplo corregido: los puntos independientes se presentan honestamente como cuatro líneas de trabajo paralelas (solución a).
  - Delimitación respecto de `decision-shot` precisada mediante el formato de salida (bloques individuales estructurados con pros/contras frente a imagen objetivo coherente con aceptación global).

### 1.0.0 (2026-09-13)
- Versión inicial basada en el encargo del usuario T-20260913-107991667.
- Estructura vinculante de siete partes (paquete, concepto, interacción, implementación, límites, aceptación, retorno).
- Lógica de agrupación basada en `decision-path` y puente de reescritura hacia la fase 4 de `decision-briefing`.
