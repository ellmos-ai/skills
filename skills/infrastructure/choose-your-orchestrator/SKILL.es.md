---
name: choose-your-orchestrator
version: 1.1.0
type: skill
author: Lukas Geiger + Codex
created: 2026-08-20
updated: 2026-10-03
description: "Elige junto con el usuario, antes de un trabajo complejo con múltiples agentes, una orquestación adecuada y limitada, y genera un contrato de sesión compacto. Usa esta habilidad con /choose-your-orchestrator, cuando la combinación de orquestador, enjambre, enrutamiento de modelos o modelo de preferencias del usuario no esté clara, y antes de programas de agentes que deban fijar explícitamente las ranuras de modelos, el paralelismo, la profundidad de generación, los límites de escritura, la aceptación y la escalada."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [orchestrierung, multi-agent, delegation, routing, budget, matruschka, session-vertrag]
aliases: [choose-your-orchestrator]
language: es
status: active
visibility: public

dependencies:
  tools: []
  services: []
  protocols: [orchestrator, swarm-operations, model-strategy, decision-avatar, budgetierung]
  python: []

provenance:
  origin: custom
  origin_path: null
  origin_version: null
  origin_repo: github.com/ellmos-ai/skills
  last_sync_from_origin: null
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 0b3feaa40d5c9d5310977fbc0e9c92572c1504e201baad19e7b73c7b64e4e846
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.987703+00:00"
---
<img src="banner.png" width="100%" alt="choose-your-orchestrator banner">

# Choose Your Orchestrator

## Propósito

Aclara antes de un trabajo complejo con múltiples agentes las condiciones de contorno, recomienda la combinación más pequeña y eficaz de habilidades existentes y emite un contrato de orquestación de sesión vinculante. Carga las habilidades seleccionadas mediante el mecanismo de habilidades del entorno de ejecución actual y sigue sus instrucciones en vivo. No copies sus procedimientos en esta habilidad.

La delegación nunca amplía la autoridad. Las acciones externas o irreversibles, como publicar, enviar, eliminar, pagar o realizar cambios productivos, siguen sujetas a la aprobación del usuario, salvo que la tarea actual las autorice expresamente.

## Componentes

| Componente | Tarea en el contrato | No es su tarea |
|---|---|---|
| `orchestrator` | Paquetes de trabajo, alcances, evidencia y aceptación | Inventar la elección de modelo o el patrón de enjambre |
| `swarm-operations` | Patrón de enjambre, puerta de costes y escalonado Matruschka opcional | Paralelizar artificialmente tareas individuales |
| `model-strategy` | Ruta según capacidades y modelos, según la disponibilidad en vivo | Fijar versiones de modelos concretas o permisos |
| `clutch` | Propuesta de enrutamiento externa opcional | Autoridad exclusiva para el despacho o el alcance |
| `decision-avatar` | Señal de preferencia autorizada y opcional ante incertidumbres reversibles | Sustituir aprobaciones del usuario o ampliar la autoridad |
| `budgetierung` | Cuotas negociadas por ventana temporal para modelos/revisores/asesores caros, cuenta y verificación previa antes de las escaladas | Elegir modelos por su contenido (eso lo hace `model-strategy`) o fijar cuotas por cuenta propia |

Usa `clutch route "<kurze Aufgabenbeschreibung>" --json` solo si `clutch` está realmente disponible. Trata la respuesta JSON como una propuesta y compárala con las ranuras de ejecución disponibles, el presupuesto, las reglas del proyecto y los límites del usuario. Si `clutch` no está disponible o su salida no es legible, usa `model-strategy` y las capacidades en vivo del entorno de ejecución. No incluyas en el contrato nombres ni versiones de modelos actuales de forma fija.

## Diálogo de recomendación

### 1. Clasificar la tarea

Determina el objetivo, el tipo de tarea, los criterios de éxito, los alcances excluidos, los permisos actuales, los bloqueos existentes y los paquetes de trabajo independientes. Elige primero la propuesta de ruta más pequeña y adecuada de la tabla siguiente.

### 2. Proponer el contrato

Muestra un borrador compacto con:

1. componentes y roles,
2. ranuras de modelo/presupuesto (en ejecuciones de varias horas o con modelos escasos o caros, negócialas mediante `budgetierung` y llévalas como cuenta),
3. paralelismo máximo y profundidad de generación,
4. límites de escritura y bloqueos,
5. aceptación y evidencia,
6. escalada y preguntas al usuario,
7. límite de autoridad.

Recomienda valores concretos y nombra en una frase la compensación más importante. Pregunta solo por decisiones que cambien materialmente el resultado. Agrupa las preguntas abiertas en como máximo tres grupos claramente separados; presenta siempre la opción recomendada en primer lugar. Si todas las dimensiones ya están fijadas explícitamente, no preguntes de nuevo.

### 3. Confirmar o reducir

No inicies ningún despacho con múltiples agentes mientras haya abierta una cuestión material de presupuesto, escritura o autoridad. Si solo es incierto el beneficio del paralelismo, reduce a una ejecución individual. Una tarea explícitamente autorizada puede arrancar con los valores predeterminados seguros si no falta ninguna decisión material del usuario.

### 4. Emitir el contrato

Muestra el contrato confirmado en el chat. Si hay disponible un comando `usmc`, consulta primero su ayuda y escribe además una nota de sesión neutra en cuanto a privacidad mediante un subcomando de nota/escritura documentado allí. No inventes ningún subcomando y no guardes prompts sin procesar, secretos ni contenido privado. Sin una vía de escritura USMC disponible, el contrato del chat es el que tiene autoridad.

## Tabla de enrutamiento

| Tipo de tarea | Recomendación | Dimensionamiento predeterminado |
|---|---|---|
| Auditoría / barrido | `orchestrator` + `swarm-operations`; `model-strategy` si hay clases de capacidad distintas | áreas independientes, un pequeño grupo `parallel-chunks` o `specialist`, fusión central |
| Programa de construcción | `orchestrator` + `model-strategy`; enjambre solo para líneas realmente independientes | el jefe planifica y acepta, los workers construyen en áreas disjuntas |
| Construcción individual | Ejecución individual; opcionalmente `model-strategy` o `clutch` para la ruta | sin sobrecarga de enjambre o jerarquía |
| Operación de tickets | El sistema de tickets sigue siendo el principal; `orchestrator` complementa los contratos de trabajo y la evidencia | no sustituir el régimen existente de router/puntuación, respetar el ciclo de vida del ticket |

## Valores predeterminados seguros

Usa estos valores, salvo que el usuario, el entorno de ejecución o las reglas del proyecto establezcan algo más estricto:

- como máximo dos workers activos; empieza con uno y demuestra el beneficio del segundo,
- Matruschka desactivado, profundidad de generación máxima `0`,
- sin subagentes propios de los workers sin aprobación explícita,
- un solo escritor por repositorio o área claramente delimitada,
- reclamaciones de archivos disjuntas y bloqueos habituales del proyecto antes de cada escritura,
- el jefe/orquestador revisa por sí mismo artefactos, diferencias y pruebas,
- los informes de finalización solo valen tras la aceptación por evidencia,
- las acciones irreversibles o externas siguen sujetas a aprobación del usuario,
- las incertidumbres se agrupan en lugar de notificarse como muchas interrupciones individuales.

Activa Matruschka solo si el usuario lo confirma expresamente y el contrato indica, por nivel, la clase de modelo/capacidad, el límite de ranuras activas, las subtareas permitidas y la profundidad máxima. Cuenta los agentes activos, no solo los existentes. Incluso entonces se mantiene exactamente un escritor por área.

## Formato del contrato

```text
SESSION-ORCHESTRIERUNGSVERTRAG
Ziel und Typ: <Ergebnis; Audit/Bauprogramm/Einzelbau/Ticket-Betrieb>
Bausteine: <geladene Skills und optionale Router>
Chef: <Planung, Denkarbeit, Integration, Evidenzabnahme>
Worker-Slots: <Rolle/Fähigkeitsklasse je Slot; Budgetgrenze; Budget/Konto: <budgetierung-Konto, Pfad>>
Parallelität: <maximal aktiv>; Spawn-Tiefe: <0..N>; Matruschka: <aus/an>
Schreibgrenzen: <ein Schreiber je Bereich; Claims; Locks; negative Scopes>
Abnahme: <Artefakte, Tests, Diffs, Quellen; wer prüft>
Eskalation: <Stopps; höchstens drei gebündelte Nutzerfragen>
Autorität: <zulässige Aktionen; extern/irreversibel user-gegatet>
Persistenz: <Chat autoritativ; USMC-Notiz ja/nein und privacy-neutral>
```

## Ejemplo

```text
Auftrag: Drei unabhängige Komponenten prüfen und einen Fix integrieren.
Empfehlung: orchestrator + swarm-operations; zwei aktive Read-only-Reviewer,
danach genau ein Integrationsschreiber. Matruschka aus, Tiefe 0. Der Chef prüft
Fundstellen, Diff und Gesamttests. Push oder Veröffentlichung nur im ausdrücklich
autorisierten Scope.
Offene Frage: Ist die zweite parallele Review-Spur den zusätzlichen Verbrauch wert?
Empfehlung: ja, weil die Komponenten unabhängig sind.
```

## Condiciones de parada

Detén o reduce la orquestación si los alcances se solapan, los bloqueos no están claros, el entorno de ejecución no ofrece la ranura recomendada, el presupuesto no está confirmado o la aceptación no puede verificarse de forma independiente. Pregunta al usuario en lugar de adivinar una nueva decisión de producto, privacidad o autoridad.

## Registro de cambios

### 1.1.0 (2026-10-03)
- Se añade `budgetierung` como componente para cuotas de modelos/cuenta negociadas (tabla de componentes, ranuras de modelo/presupuesto en el diálogo de contrato, línea de formato de contrato con ranuras de workers).

### 1.0.0 (2026-08-20)
- Se introducen el diálogo de recomendación, la tabla de rutas y el contrato de sesión compacto.
- Se establecen valores predeterminados seguros para paralelismo, Matruschka, límites de escritura, evidencia y acciones externas.
- Se describe la integración opcional de `clutch` y de un modelo de preferencias autorizado, sin vinculación fija a modelos ni ampliación de la autoridad.
