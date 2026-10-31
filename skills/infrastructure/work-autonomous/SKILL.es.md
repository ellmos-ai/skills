---
name: work-autonomous
version: 1.5.1
type: protocol
author: Lukas Geiger + Claude
created: 2026-08-15
updated: 2026-09-09
description: "Condición de terminación para bucles autónomos: seguir trabajando de forma independiente en la medida de lo posible Y terminar un bucle solo cuando esté acreditado que ya no existe ninguna tarea ejecutable de forma autónoma. La mera impresión de \"no queda nada por hacer\" NO basta: activa una cadena de comprobación de cuatro pasos (think/decide, _CONTROL/_DECISIONS, Gardener/USMC, decision-avatar/BYUM), que primero debe GANAR nuevas tareas antes de que el bucle pueda terminar. Cada paso de la cadena informa found/empty/unavailable en lugar de un resultado binario: \"exhausted\" solo se aplica si TODAS las fuentes eran realmente consultables; si al menos una fuente está unavailable, la skill informa \"blind\" en lugar de \"exhausted\" y no afirma nada no comprobado. Usa esta skill con /work-autonomous, /waafap, \"sigue trabajando de forma autónoma hasta que no quede nada por hacer\", como condición de objetivo dentro de un /loop, o cuando haya que comprobar si realmente ya no queda trabajo autónomo antes de terminar un bucle o una sesión."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [autonomy, loop, goal, workflow, decision, exhaustion-check, guard, ticket-master]
language: es
status: active
visibility: public
aliases: [waafap, work-autonomous-as-far-as-possible]

dependencies:
  tools: []
  services: []
  protocols: [think, decide, decision-avatar]
  python: []

provenance:
  origin: "custom"
  origin_path: null
  origin_version: null
  origin_repo: "github.com/ellmos-ai/skills"
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: a8ee248e73bb81d9af36df2f3e82719bed0f31e89005ab64c35f4e236b15600c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.428121+00:00"
---
<img src="banner.png" width="100%" alt="work-autonomous banner">

# work-autonomous — Terminar el bucle solo cuando esté acreditado que no quedan tareas autónomas

## Propósito

Esta skill cumple dos funciones a la vez:

1. **Seguir trabajando de forma autónoma en la medida de lo posible** — trabajo normal de sesión, nada especial.
2. **Terminar un bucle solo cuando se HAYA DEMOSTRADO** que no existe ninguna tarea ejecutable de forma autónoma. La sospecha de "ahora mismo no encuentro nada que hacer" **no** es motivo de terminación — es el **desencadenante** de una cadena de comprobación que primero intenta **ganar** nuevas tareas. Solo cuando esa cadena permanece totalmente sin resultados, la terminación se considera acreditada.

**Deliberadamente sin `/goal` integrado:** la skill es utilizable de forma independiente (p. ej., directamente como invocación `/work-autonomous` dentro de una sesión normal) y también como condición dentro de una construcción de bucle superior: `/loop` normal, y después nombrar solo esta skill como objetivo. El objetivo queda entonces, en sentido figurado: *"Termina el bucle cuando no queden tareas autónomas — y mientras tanto sigue trabajando de forma autónoma en la medida de lo posible."* La skill en sí no invoca ninguna construcción `/goal`; solo proporciona la señal de terminación inequívoca que tal construcción puede leer (véase "Señal de terminación" más abajo).

## Modelo operativo — dos niveles

### Nivel 1 — Trabajo normal (cada tick)

#### Puerta de admisión TICKET-MASTER (prioridad sobre todo lo demás en este nivel)

**Solo relevante si hay un sistema de tickets (`_TICKETS/`) en el contexto** — las sesiones sin sistema de tickets omiten esta puerta sin más; la skill sigue siendo utilizable de forma independiente sin ningún sistema de tickets (véase "Propósito" arriba). Si procede, primero hay que comprobar si `INBOX/` — incluidas las entradas informales aún no llevadas al formato de ticket — está completamente formalizado y clasificado. Si no lo está, eso cuenta como trabajo autónomo encontrado (formalizar/clasificar es trabajo administrativo sin decisión del usuario, véase la delimitación más abajo) — se realiza, el tick termina y no se entra en el Nivel 2, como con cualquier otra fuente del Nivel 1.

**Mientras la INBOX esté abierta, NO puede surgir ninguna `NO_WORK`, señal de agotamiento (`exhausted`/`blind`), STOP de guard ni ninguna otra señal de terminación.** Solo cuando la admisión esté completamente clasificada pueden comprobarse `ACTIONABLE`, `BLOCKED` desbloqueados y `WAITING` vencidos (abajo) — y, después, si procede, el Nivel 2.

*Caso de prueba:* un bucle empezó la comprobación de agotamiento tras procesar `ACTIONABLE`, mientras seguían llegando nuevos tickets `INBOX`, dos de ellos con prioridad P1. Sin esta puerta, el bucle habría informado `exhausted`/`blind` aunque la entrada seguía abierta — exactamente lo que impide la puerta.

Después, buscar con normalidad más trabajo ejecutable de forma autónoma (véase la delimitación más abajo) y realizarlo: tickets `ACTIONABLE` abiertos, tickets `BLOCKED` desbloqueados, tickets `WAITING` vencidos, puntos `TODO.md`/`AUFGABEN.txt` abiertos en proyectos sin dependencia del usuario, comprobaciones rutinarias/de higiene vencidas según la política local, trabajo iniciado pero no terminado de la última sesión (USMC `working`), **ejecuciones `tidy-up` vencidas del proyecto activo** (adición 1.3.0, 2026-08-19 — véase la skill `tidy-up`: pasada de Tasksolver+Writer+Maintainer sobre la carpeta del proyecto en la que la sesión estaba trabajando; la vencimiento lo comprueba `tidy-up` por sí misma mediante su propio registro USMC ligero, véase su sección "Relación con work-autonomous").

→ **Encontrado y realizado:** informar brevemente del resultado, el tick termina, el bucle sigue con normalidad. NO se entra en el Nivel 2 — ninguno de los cuatro pasos de comprobación costosos es necesario mientras haya trabajo visible.

### Nivel 2 — Comprobación de agotamiento (solo ante la sospecha de "no queda nada por hacer")

Solo cuando el Nivel 1 **no** encuentra nada autónomo, surge la sospecha. Esa sospecha por sí sola no basta. Ahora se ejecuta **obligatoriamente** la siguiente cadena para intentar **ganar** nuevas tareas.

#### Autoconocimiento (antes de la cadena, no después)

Antes de consultar nada: la skill declara QUÉ fuentes necesita para su juicio. Cuatro necesidades (`grounding_seed.self_knowledge.Need`, si `grounding-seed` está instalado — en caso contrario, la misma lista vale como simple declaración sin vinculación a biblioteca):

| Rol | Paso de la cadena | Qué hay detrás |
|---|---|---|
| `decisions.ledger` | 2 | registro central de decisiones |
| `memory.organic` | 3 | Gardener (`find()`/`put()`) |
| `memory.curated` | 3 | USMC (`facts`/`lessons`/`working`/`context`) |
| `user.model` | 4 | decision-avatar / BYUM |

**`/think` + `/decide` (paso 1) es deliberadamente NO una fuente declarada.** Es el propio paso analítico del modelo, no un sistema externo que pudiera ser alcanzable o no — siempre está "disponible" en el sentido de esta distinción. Solo los pasos 2–4 pueden volverse `unavailable`.

Herramienta opcional y comprobable para la pura cuestión de localización (found/unavailable, todavía SIN comprobación de contenido): `scripts/exhaustion_check.py` en la carpeta de esta skill. Usa `grounding_seed.resolve()` + `status_from_resolution()` para `decisions.ledger`/`user.model` (allí existe un proveedor `source-resolver` real), comprueba `memory.organic`/`memory.curated` **siempre** directamente mediante alcanzabilidad CLI (`gardener`/`usmc` en PATH) — para estos dos roles, hasta el 2026-08-15 no había ningún proveedor `source-resolver` registrado; consultarlos a través del resolver solo habría devuelto `unavailable`, independientemente de si Gardener/USMC estaban realmente instalados. Funciona igual con y sin `grounding-seed` instalado.

**Actualización 2026-08-25 (K3=C, `T-20260825-342866657`):** la laguna está cerrada — `source-resolver` registra ahora `memory.organic` (Gardener) y `memory.curated` (USMC) como roles de nivel 1, ambos con la misma comprobación de presencia CLI (`shutil.which("gardener")`/`shutil.which("usmc")`) que este script venía codificando por su cuenta. `exhaustion_check.py`, por tanto, NO se ha reconvertido de inmediato (sin pérdida funcional, la comprobación existente sigue siendo correcta) — en la próxima pasada de cuidado de la skill, el paso 3 puede pasar a `source_resolver.resolve("memory.organic"/"memory.curated")`, análogamente al paso 2 (`decisions.ledger`), en lugar de mantener la comprobación CLI por duplicado.

#### Los cuatro pasos de la cadena — cada uno informa found | empty | unavailable

Cada paso se ejecuta en dos fases: primero **localización** (¿conozco realmente un lugar alcanzable?), y después — solo si se ha localizado — **comprobación de contenido** (el modelo lee efectivamente, con sus propias herramientas, si hay algo nuevo allí). Una fuente que no pudo localizarse NUNCA se comprueba en su contenido — cuenta como `unavailable`, no como `empty`.

1. **`/think` + `/decide`** aplicados a la pregunta: "¿De verdad no queda trabajo autónomo ejecutable, o se me está pasando algo?" — análisis estructurado en lugar de intuición. No tiene estado found/empty/unavailable (véase arriba, no es una fuente).
2. **`decisions.ledger`** — localización mediante `source_resolver.resolve("decisions.ledger")` / `grounding_seed.resolve(...)`, si está instalado; si no, la ruta de respaldo conocida (`_control-center/_CONTROL/_DECISIONS/`, cadena `TO-DECIDE-USER*.txt`, `TO-DECIDE-USER-<HOST>.txt` propia del host, `DECIDED-AND-DONE.md`). Localizado → leer el contenido: ¿se han tomado recientemente decisiones que desbloqueen trabajo antes bloqueado o pendiente de aprobación? Hallazgo → `found`. Leído, nada nuevo → `empty`. No localizable (falta el resolver Y no existe la ruta de respaldo) → `unavailable`.
3. **`memory.organic` (Gardener) + `memory.curated` (USMC)** — dos fuentes separadas, un solo paso de la cadena. Localización: CLI en PATH (`gardener`/`usmc`), véase el autoconocimiento arriba. Alcanzable → leer el contenido (`find()`/`recall()` o `usmc facts|lessons|working|context`): puntos abiertos de la memoria de trabajo, lecciones con un seguimiento pendiente, hechos que apunten a trabajo ejecutable pasado por alto (es justo el lugar donde sesiones anteriores dejan puntos sin terminar — campo `RESUME:`, entradas `note` abiertas). Hallazgo → `found`. Leído, nada nuevo → `empty`. CLI no en PATH → `unavailable`.
4. **`user.model` (decision-avatar/BYUM)** — localización como en `decisions.ledger` (resolver o ruta de respaldo `_control-center/_CONTROL/_USER-MIND/`). Localizado → comprobar el contenido: ¿existe un patrón acreditado según el cual el usuario quisiera ver una acción concreta realizada de forma autónoma en este punto? Solo cuenta como `found` con confianza suficiente (🟢/🟡) — 🔴 cuenta como `empty`, no como tarea ganada, sino como punto abierto para el paso "Resto solo del usuario" más abajo. No localizable → `unavailable`.

**"Exhausted" solo puede informarse si las CUATRO fuentes (pasos 2–4, tres pasos, cuatro roles) pudieron consultarse de verdad — es decir, `found` o `empty`, sin una sola `unavailable`.** Eso corresponde a `grounding_seed.self_knowledge.GroundingReport.all_answerable()`. Si al menos un rol es `unavailable`, NO aplica "exhausted", sino la señal propia "blind" (véase la señal de terminación más abajo) — el bucle termina igualmente (de todos modos no puede consultar nada), pero ya no afirma haber comprobado lo que no pudo comprobar.

Si cualquier paso encuentra trabajo nuevo → volver al Nivel 1, realizar el trabajo, y poner el estado de guard (véase abajo) en "found" en lugar de "exhausted"/"blind".

### Caso especial: restos solo del usuario

Si la cadena **no** encuentra ya ninguna tarea **autónoma**, pero hay tickets `USER/*` o puntos `_DECISIONS` sin decidir abiertos, eso sigue siendo un STOP para la autonomía — aunque no significa "nada que hacer", sino "nada que hacer *de forma autónoma*". Estos puntos se presentan según la regla de bucle autónomo como un único envío **agrupado** desde `ticket-master` (una sola plantilla de resumen, no avisos individuales), no se preguntan uno a uno. La señal de terminación distingue expresamente este caso de la auténtica falta de trabajo.

## Delimitación — ¿qué cuenta como "ejecutable de forma autónoma"?

Referencia: categorías `ticket-master` (`.AI/.MODULES/.CONTROL/ticket-master/docs/CATEGORIES.de.md`).

| Caso | ¿Autónomo? | Motivo |
|---|---|---|
| `INBOX/` incluidas las entradas informales, bajo TICKET-MASTER (antes de la clasificación) | **Sí, con prioridad** | Formalizar/clasificar es trabajo administrativo sin decisión del usuario — va antes que `ACTIONABLE`/`BLOCKED`/`WAITING` y bloquea hasta entonces cualquier señal de terminación (véase la puerta de admisión arriba). |
| Ticket `ACTIONABLE` | **Sí** | Sin bloqueo, sin dependencia del usuario — por definición. |
| `BLOCKED/*` (host-receipt, foreign-state, lock, quota, dependency) | No, mientras el bloqueo no haya desaparecido **empíricamente** | Está permitida una nueva comprobación periódica (bucle autónomo), "existente" no basta como prueba — hace falta evidencia. |
| `WAITING/*` (scheduled, review-due, marker) antes de la fecha/marcador | No | Ligado a un plazo. |
| `WAITING/*` tras cumplirse la fecha/marcador | **Sí** | Condición cumplida → pasa a `ACTIONABLE`. |
| `USER/*` (decision, data, freigabe, hardware, session) | **Nunca autónomo** | Requiere necesariamente decisión, datos, aprobación, hardware o sesión del usuario. Presentar agrupado, véase arriba. |
| `PARKED/*` (skip, backlog, until-trigger) | No, salvo encargo o disparador explícito | Pospuesto a propósito, sin nueva comprobación automática. |
| Puntos `TODO.md`/`AUFGABEN.txt` abiertos sin nota de aprobación/decisión | **Sí** | Registro de proyecto, trabajo normal. |
| Comprobaciones rutinarias/de higiene vencidas (enfriamiento cumplido, sin bloqueo) | **Sí** | Mantenimiento habitual según la política local. |
| Áreas bloqueadas por `LOCK.user.*` | **Nunca** | Bloqueo del usuario — solo el usuario lo levanta, véase LOCK-SYSTEM. |
| Pasos irreversibles/con efecto externo sin liberación de política (subida a Zenodo, push a ramas juzgadas/protegidas, decisión de gasto en servidor más allá del umbral del portátil, borrado definitivo sin vista previa) | **No** | Requiere liberación/decisión, aunque sea técnicamente ejecutable. |
| Sesión que solo puede iniciarse por GUI/login (p. ej., tarea de Claude Desktop, login interactivo, acción física de hardware) | **Nunca** | "Sesión que solo el usuario puede iniciar" — ningún bucle puede asumirla. |

Regla general: es autónomo lo que puede completarse **sin** decisión, aprobación, datos, hardware o sesión del usuario Y que no requiere una acción irreversible/con efecto externo sin liberación de política documentada.

## Guard contra bucles infinitos (obligatorio)

**Problema:** sin freno, la cadena de cuatro pasos se ejecutaría por completo en cada nueva comprobación, aunque desde la última pasada sin resultados no haya cambiado nada — costoso e inútil, sobre todo si la skill se invoca repetidamente (bucle, tarea programada, nueva invocación manual poco después de la anterior).

**El estado se persiste en USMC** (el estado de proceso pertenece en este sistema allí, no en archivos Markdown):

```bash
# Zustand lesen (nach Tag work-autonomous-guard filtern)
usmc --agent <agent> working --limit 20

# Zustand nach einem Kettendurchlauf schreiben
usmc --agent <agent> note "work-autonomous-guard: result=<exhausted|blind|found> fingerprint=<FP> at=<ISO-Zeit>" \
  --type context --priority 3 --tags "work-autonomous-guard,<projekt-slug>"
```

**La huella se compone de DOS elementos — la situación Y la alcanzabilidad:**

1. **Elemento de situación** (como hasta ahora): número/IDs de tickets `ACTIONABLE` abiertos, mtime de la cadena `_DECISIONS` (`TO-DECIDE-USER*.txt`, `DECIDED-AND-DONE.md`), número de entradas `working` nuevas de USMC desde la última pasada de la cadena.
2. **Elemento de disponibilidad (nuevo, obligatorio desde 1.2.0):** la tupla ordenada de los roles que en ese momento se informaron como `unavailable` en la comprobación de autoconocimiento (`exhaustion_check.availability_fingerprint_component()`), p. ej. `("memory.organic",)` o `()`.

**Por qué el segundo elemento es obligatorio — "si no, el guard hereda la laguna":** sin él, la huella (elemento 1) depende, entre otros, del mtime de la cadena `_DECISIONS`. Si esa cadena falta por completo en un sistema, esa parte de la huella es constante para siempre — un `exhausted`/`blind` establecido erróneamente nunca volvería a comprobarse, aunque más tarde se instalara `source-resolver` o se creara `_control-center/_CONTROL/_DECISIONS/`. El elemento de disponibilidad soluciona precisamente eso: si cambia QUÉ roles están unavailable (aparece o desaparece una fuente), la huella cambia automáticamente — el guard lo detecta en la siguiente invocación y vuelve a ejecutar la cadena. Es un "trasplante" en el sentido de la metáfora de grounding (T-20260815-371628859): un cambio de entorno dispara una nueva búsqueda sin que nadie tenga que reiniciar el guard manualmente.

**Secuencia antes de cada pasada de la cadena:**

```
guard = letzten "work-autonomous-guard"-Eintrag aus USMC lesen
wenn guard existiert
   und guard.result in ("exhausted", "blind")
   und (jetzt - guard.timestamp) < GUARD_INTERVAL   (Default: 15 Minuten)
   und fingerprint(jetzt) == guard.fingerprint:      # Lage- UND Verfügbarkeits-Baustein
       → Kette NICHT erneut fahren.
       → guard.result == "exhausted":
           Melden: "Weiterhin keine autonome Arbeit — unverändert seit {guard.timestamp}.
                    Kein neuer Trigger. STOP (Guard aktiv, exhausted unchanged since …)."
       → guard.result == "blind":
           Melden: "Weiterhin blind (Quellen nicht verfügbar) — unverändert seit {guard.timestamp}.
                    STOP (Guard aktiv, blind unchanged since …)."
sonst:
       → Kette vollständig fahren (Selbstkenntnis-Prüfung + alle vier Kettenschritte).
       → Neuen Guard-Zustand schreiben (timestamp=jetzt, fingerprint=fingerprint(jetzt),
         result=exhausted|blind|found).
       → alle vier Quellen befragbar UND alle empty → exhausted → STOP (belegt).
       → mindestens eine Quelle unavailable → blind → STOP (nicht belegt, nur unerreichbar).
       → mindestens eine Quelle liefert einen Treffer → found → zurück zu Ebene 1, Arbeit erledigen.
```

Una única pasada completamente ejecutada de la cadena, en la que las CUATRO fuentes eran consultables y NINGUNA devolvió un hallazgo, basta como prueba de "ya no hay tareas autónomas" (regla del ticket: "solo cuando TODOS los pasos de una pasada permanecen sin resultados" — sin resultados aquí significa expresamente `empty`, no `unavailable`). El guard no impide la comprobación en sí, sino solo la **nueva comprobación repetida e inalterada** en invocaciones seguidas — y ello por separado para `exhausted` Y para `blind`, sin confundirlas nunca.

`GUARD_INTERVAL` es configurable (por defecto 15 minutos) — en entornos muy tranquilos (nuevos tickets/decisiones poco frecuentes) puede elegirse más, en entornos muy activos, menos.

## Señal de terminación

Cada pasada termina con **una** línea única y localizable con grep, para que una construcción `/loop` envolvente o una futura construcción `/goal` pueda leer de ella si debe seguir:

```
WORK-AUTONOMOUS: CONTINUE                                          — Ebene 1 hat Arbeit erledigt, Loop läuft weiter.
WORK-AUTONOMOUS: STOP (exhausted)                                  — alle vier Quellen befragt, alle empty. Belegt: keine Arbeit mehr.
WORK-AUTONOMOUS: STOP (blind, N/4 Quellen nicht verfuegbar: <rollen>) — mind. eine Quelle unavailable. NICHT belegt — nur nicht prüfbar.
WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since …)         — Guard aktiv, weiterhin exhausted, kein neuer Trigger.
WORK-AUTONOMOUS: STOP (guard, blind unchanged since …)             — Guard aktiv, weiterhin blind, keine Quelle neu verfügbar geworden.
WORK-AUTONOMOUS: STOP (user-only)                                  — nur USER/*-Reste offen, gebündelt vorgelegt.
```

`CONTINUE` es la única señal en la que un bucle superior debe lanzar otro tick. Todas las variantes `STOP` son la terminación acreditada — incluida la justificación de qué caso se da.

**La diferencia entre `exhausted` y `blind` es esencial para el usuario, no cosmética:** `exhausted` significa "he comprobado todo lo que había que comprobar — el trabajo está terminado". `blind` significa "me falta infraestructura para comprobar en absoluto — eso no es un estado de trabajo, sino una laguna". Una construcción `/loop`/`/goal` que trate ambos igual (el bucle termina de todas formas) no debe INFORMAR de ellos de la misma manera al usuario — de lo contrario desaparecería justo la información que exigió T-20260815-205101335.

## Relación con otras skills

- **`think`/`decide`** — aportan el análisis/decisión estructurados del paso 1 de la cadena. Aquí se invocan como componente, no se reinventan.
- **`decision-avatar`** (esta skill, neutral respecto al usuario) — aporta el paso 4 de la cadena. En sistemas con un perfil concreto y autorizado, eso corresponde a `user-model` + `build-your-users-mind`.
- **`orchestrator`** — regula CÓMO se delega en subagentes y cómo se verifica su informe de finalización. `work-autonomous` regula CUÁNDO se deja de buscar; ambas son combinables (el orquestador puede aparecer como parte del trabajo realizado en el Nivel 1).
- **`bugsweep`** — un ejemplo de otro protocolo de búsqueda autolimitado (escalada por duplicación en lugar de cadena de cuatro pasos). `work-autonomous` es más genérico: no solo comprueba código en busca de errores, sino cualquier fuente de trabajo autónomo.
- **Categorías de tickets (`ticket-master`)** — aportan el vocabulario de "ejecutable de forma autónoma" (véase la tabla de delimitación) y la plantilla para el bucle autónomo (nueva comprobación BLOCKED, agrupación USER, arrastre de plazos WAITING, estancamiento PARKED).
- **`tidy-up`** (desde 1.3.0) — aporta una fuente adicional de nivel 1: la pasada única de Tasksolver+Writer+Maintainer para la carpeta del proyecto que se está trabajando. Comprueba su propio vencimiento mediante un registro USMC ligero (sin el guard de cuatro pasos de aquí) — `work-autonomous` solo la invoca como una de varias fuentes del nivel 1, sin duplicar su lógica.

## Ejemplo de flujo

```
Tick 1: ACTIONABLE-Ticket T-... gefunden → erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 2: Kein ACTIONABLE-Ticket mehr, kein offener TODO-Punkt.
        → Ebene 2: Selbstkenntnis + Kette 1–4 läuft.
        → Schritt 2 (decisions.ledger): verortet, DECIDED-AND-DONE.md hat einen neuen Eintrag
          seit 10 Min. → found, daraus resultiert eine neue autonome Aufgabe.
        → Guard: result=found geschrieben. Aufgabe erledigt. WORK-AUTONOMOUS: CONTINUE
Tick 3: Wieder nichts sichtbar. Voll ausgestattetes System (Gardener, USMC, _DECISIONS, BYUM alle da).
        → Ebene 2: alle vier Quellen verortet UND befragt, alle vier empty.
        → Guard: result=exhausted, fingerprint=FP1 (Lage + Verfügbarkeit ()), timestamp=T1.
        → WORK-AUTONOMOUS: STOP (exhausted)
Tick 4 (2 Minuten später, z. B. durch erneuten Loop-Trigger):
        → Guard: result=exhausted, fingerprint(jetzt)==FP1, (jetzt-T1) < 15 Min.
        → Kette NICHT erneut gefahren.
        → WORK-AUTONOMOUS: STOP (guard, exhausted unchanged since T1)

Gegenbeispiel — System OHNE Gardener/USMC (der Kernfall aus T-20260815-205101335):
Tick 1: Nichts sichtbar. Selbstkenntnis-Prüfung: decisions.ledger verortet (leer, empty),
        memory.organic/memory.curated NICHT verortet (CLI fehlt) → unavailable,
        user.model verortet (empty).
        → nicht alle vier Quellen befragbar → KEIN exhausted.
        → Guard: result=blind, fingerprint=FP2 (Verfügbarkeit ("memory.curated","memory.organic")).
        → WORK-AUTONOMOUS: STOP (blind, 2/4 Quellen nicht verfuegbar: memory.organic, memory.curated)
Tick 2 (Nutzer installiert grounding-seed + usmc auf diesem System):
        → Selbstkenntnis-Prüfung: memory.curated jetzt verortet (CLI auf PATH) → Verfügbarkeits-
          Baustein ändert sich zu ("memory.organic",) → fingerprint(jetzt) != FP2.
        → Guard erkennt Änderung, Kette läuft neu (Verpflanzung) — ohne dass jemand den Guard
          manuell zurückgesetzt hätte.
```

## Registro de cambios

### 1.5.1 (2026-09-09)
- T-20260909-282509082: El respaldo documentado para `decisions.ledger` y `user.model` sigue la mudanza confirmada del Control Center a `_CONTROL/_DECISIONS` y `_CONTROL/_USER-MIND`. La prioridad del resolver y el comportamiento fail-closed siguen sin cambios.

### 1.5.0 (2026-09-09)
- P-018: Los informes de trabajo, handoffs y receipts importantes recién creados y guardados de forma duradera terminan con `session: <session-id> | <agent>@<host> | YYYY-MM-DD`. La prioridad de fuentes es primero la indicación explícita en tiempo de ejecución/CLI, después el entorno/hook autoritativo del proveedor y por último `unbekannt`; los valores nunca se adivinan y los subagentes usan la sesión padre. El chat rutinario, las fuentes, las políticas, `CLAUDE.md`, los READMEs y los archivos antiguos quedan excluidos de estampado global o retroactivo.

### 1.4.0 (2026-09-03)
- Adición mínimamente invasiva del ticket T-20260902-729068782: nueva **puerta de admisión TICKET-MASTER** en el Nivel 1 (prioridad sobre `ACTIONABLE`/`BLOCKED`/`WAITING`) — solo relevante si un sistema de tickets forma parte del contexto. Mientras `INBOX/` (incluidas las entradas informales) no esté completamente clasificado, no puede surgir ningún `NO_WORK`/señal de agotamiento/STOP de guard. Caso de prueba: un bucle empezó la comprobación de agotamiento mientras `INBOX` aún tenía entradas abiertas (entre ellas dos tickets P1). La cadena de cuatro pasos de agotamiento, el guard y la usabilidad fuera de TICKET-MASTER siguen sin cambios — la puerta actúa exclusivamente en el Nivel 1 y solo bajo TICKET-MASTER.
- Nueva función auxiliar probada `scripts/exhaustion_check.py::intake_gate_blocks_stop()` + pruebas de regresión en `tests/test_exhaustion_check.py` (de comportamiento: la puerta bloquea con la INBOX abierta, libera con la INBOX vacía).

### 1.3.0 (2026-08-19)
- Adición mínimamente invasiva del ticket T-20260819-461890468 (nueva skill `tidy-up`): el Nivel 1 recibe una fuente adicional e independiente — "ejecuciones `tidy-up` vencidas del proyecto activo" (pasada de Tasksolver+Writer+Maintainer, véase la skill `tidy-up`). Sin nuevo paso de la cadena, sin cambios en el Nivel 2/guard/señal de terminación — `tidy-up` comprueba su vencimiento por sí misma mediante un registro USMC ligero y aquí solo se referencia como otra fuente del Nivel 1, análogamente a las ya existentes (tickets, TODO/AUFGABEN, comprobaciones rutinarias, USMC `working`). Así, los puntos `tidy-up` cuentan como tarea autónoma a ejecutar en el sentido de una construcción `/goal` que combina `/work-autonomous` + `/tidy-up` (caso de uso central del ticket). Sin intervención en la cadena de cuatro pasos de agotamiento ni en el guard — el Nivel 2 sigue sin cambios.

### 1.2.0 (2026-08-15)
- Retrofit del ticket T-20260815-205101335 (encargo de revisión: "comprueba si la solución sostiene en conexión con la metáfora de grounding", hallazgo en la skill entregada: sostenía en tres puntos, pero NO en la distinción "consultado y vacío" frente a "no pudo consultarse en absoluto" — la cadena informaba `STOP (exhausted)` también en sistemas sin Gardener/USMC/`_DECISIONS`, sin haberlo comprobado nunca. Primer caso real de uso de `grounding-seed`, ticket T-20260815-371628859).
- **Autoconocimiento añadido:** cuatro necesidades declaradas (`decisions.ledger`, `memory.organic`, `memory.curated`, `user.model`) antes de la cadena, en lugar de buscar a ciegas en cuatro ubicaciones fijas.
- **Cada paso de la cadena (2–4) informa found | empty | unavailable** en lugar de un resultado binario — en dos fases: primero localización (`grounding-seed`/`source-resolver` para `decisions.ledger`/`user.model`, comprobación CLI directa para `memory.organic`/`memory.curated`, que aún no tienen proveedor `source-resolver`), comprobación de contenido solo si la localización tuvo éxito.
- **`exhausted` solo vale si las cuatro fuentes fueron realmente consultables** (todas found/empty, ninguna unavailable). Nueva señal distinguible `STOP (blind, N/4 Quellen nicht
  verfuegbar: …)` para el caso de que al menos una fuente no fuera alcanzable — el bucle termina igualmente, pero ya no afirma un resultado comprobado.
- **Huella del guard ampliada con un elemento de disponibilidad** (tupla ordenada de los roles actualmente unavailable). Corrige la observación de seguimiento "el guard hereda la laguna": sin este elemento, un `exhausted`/`blind` establecido erróneamente seguiría valiendo para siempre si la cadena `_DECISIONS` falta por completo (el componente existente de la huella es entonces constante). Con el elemento, una fuente recién disponible dispara automáticamente una nueva pasada de la cadena (trasplante en el sentido de la metáfora de grounding).
- Nuevo script auxiliar probado `scripts/exhaustion_check.py` (+ `tests/test_exhaustion_check.py`, 11 pruebas, ambos modos comprobados: con y sin `grounding-seed` instalado) — proporciona de forma determinista la comprobación de autoconocimiento/localización, para que la skill no tenga que adivinarla en cada ejecución. Sigue siendo opcional: la skill sigue siendo principalmente un protocolo que un modelo sigue con sus propias herramientas.
- Dependencia: `grounding_seed.self_knowledge.assess()`/`status_from_resolution()` desde `grounding-seed` 0.2.0 — las versiones anteriores de `grounding-seed` (0.1.0) tenían un error de categorías (`not_found` se convertía erróneamente en `empty`), que habría vuelto a difuminar justo la distinción corregida aquí. Sin `grounding-seed` instalado, el respaldo documentado funciona igual.

### 1.1.0 (2026-08-15)
- Retrofit de referencia del ticket T-20260815-385400870: el paso 2 (registro de decisiones) resuelve ahora su ubicación a través del rol `decisions.ledger` (`source_resolver.resolve(...)`, módulo `source-resolver`), en lugar de tenerla cableada, con respaldo documentado a la ruta anterior si el resolver no está instalado. Comportamiento funcional sin cambios.

### 1.0.0 (2026-08-15)
- Versión inicial del ticket T-20260815-522639345: modelo operativo de dos niveles, cadena de comprobación de cuatro pasos, tabla de delimitación según las categorías `ticket-master`, guard contra bucles infinitos respaldado por USMC y señal de terminación inequívoca para construcciones `/loop`/`/goal`.
