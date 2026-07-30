---
name: game-design
version: 1.0.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-06-17
description: Cómo funciona el desarrollo de videojuegos como proceso: roles, subtareas, flujos de trabajo y descripciones de roles, especialmente (pero no únicamente) para Roblox. Usa esta skill cuando se trate de la ORGANIZACIÓN del desarrollo de juegos en lugar de código concreto: ¿Qué roles existen (Creative Director, Engineer, Artist, Polish/Audio, Business, QA-Tester, Game Critic)? ¿Quién hace qué subtarea? ¿Cómo es una cadena de desarrollo (concepto → backend → frontend → polish → test)? ¿Cómo se escribe un Game Design Document / KONZEPT.md? ¿Cómo se reparten el juego varios agentes (de IA)? Activar también con "planificar un nuevo juego", "crear Game Design Document", "qué roles necesito para mi juego", "flujo de trabajo de desarrollo de un juego", "quién prueba el juego", "estructurar una idea de juego", "género/monetización en Roblox".
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: game-dev
tags: [game-design, roblox, rollen, workflow, gdd, konzept, monetarisierung, qa, gamedev]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': '~/.claude/skills/game-design/', 'origin_version': '1.0.0', 'origin_repo': None, 'last_sync_from_origin': None, 'last_sync_to_origin': None, 'local_changes_since_sync': False}
---

<img src="banner.png" width="100%" alt="game-design banner">

> **Español** — Versión oficial en español de `game-design`.


# Game Design — Roles, Subtareas y Flujos de Trabajo

## Descripción general y propósito

El desarrollo de videojuegos es un trabajo en equipo compuesto por disciplinas claramente separadas, incluso cuando una sola persona o un solo agente de IA asume varias de ellas. Esta skill proporciona el **modelo organizativo**: qué roles existen, qué subtareas les corresponden, en qué orden interactúan y cómo plasmar un juego como concepto (GDD). Para el "cómo" *técnico*, consulta `/rojo` (sincronización), `/rbx-studio` (editor/assets) y la meta-skill `/rbx-dev` (arquitectura).

Usa esta skill al planificar un nuevo juego, al dividir el trabajo (también entre varios agentes de IA) y al redactar/revisar un Game Design Document.

## Los Roles (5 de desarrollo + 2 de pruebas)

Una distribución de roles probada y compacta. Descripciones completas con todas las subtareas: [`references/roles-and-workflows.md`](references/roles-and-workflows.md).

| Rol | Enfoque | Subtareas principales |
| --- | --- | --- |
| **Creative Director** | QUÉ & POR QUÉ & para QUIÉN | GDD/KONZEPT, diseño y balanceo de mecánicas, priorización/sprints, historia, flujo de UX |
| **Engineer** | CÓMO (técnico) | Código de servidor/cliente/compartido, bucle de juego, redes/remotes, DevOps (Rojo, build), corrección de errores |
| **Artist** | cómo se ve el mundo | Construcción del mundo/niveles, iluminación y atmósfera, partículas, búsqueda de assets (incl. análisis de malware) |
| **Polish / Audio** | cómo se siente y suena | SFX/música/ambiente, animaciones, ajuste fino de UI/UX, "juice" (vibración de pantalla, hit-stop), feedback |
| **Business** | orientado al exterior | Página de la tienda, icono/miniatura, monetización (gamepass/productos/pase), analíticas, comunidad |
| **QA-Tester** | ¿es técnicamente correcto? | Escaneo de errores en código, pruebas de juego + revisión de consola, informes reproducibles, regresión, rendimiento |
| **Game Critic** | ¿es divertido? | Primera impresión e impresión a largo plazo desde la perspectiva del jugador, evaluación honesta (diversión, claridad, imparcialidad), sugerencias |

**Regla básica:** El desarrollo y las pruebas son roles **separados**; lo ideal es que sean personas o agentes distintos. Quien escribe código no lo prueba de forma objetiva. El Game Critic puede ser exigente.

## Flujos de Trabajo y Procedimiento

El trabajo fluye como una cadena de rol en rol. Los patrones más importantes:

**Cadena estándar de funciones:**
```
Creative Director (plans feature) → Engineer (backend) → Artist (frontend/assets)
→ Polish/Audio (sound + fine-tuning) → QA-Tester (technical test)
→ Game Critic (player perspective) → Creative Director (feedback → next iteration)
```

**Cadena de solución rápida:** QA-Tester (bug) → Engineer (fix) → QA-Tester (verifies).

**Cadena de assets:** Artist (store search) → Artist (malware scan) → Artist (integrate) → QA (visual).

**Cadena de polish:** Game Critic (weakness) → Polish/Audio → Artist → Game Critic (re-check).

**Human-in-the-loop:** [agent chain] → human tester → Creative Director (feedback) → [chain].

Cada iteración debe dejar un breve historial de cambios. Condición de parada: presupuesto de tiempo alcanzado **o** objetivo de calidad cumplido.

### Pruebas basadas en personas (Persona-based testing)

Un juego solo sobrevive si jugadores muy diversos pueden adaptarse a él. Por lo tanto, realiza pruebas (también simuladas por agentes) desde varias **personas** en lugar de solo desde tu propia perspectiva, variando por edad, experiencia, plataforma (PC/móvil/tablet/consola), capacidad de atención, idioma y accesibilidad. Ejemplos: un niño de 9 años en una tablet que solo quiere pulsar botones; un jugador de 12 años en PC que busca el meta; un principiante mayor de 60 años que necesita botones grandes.
Las pruebas de personas deben realizarse **a ciegas** (el probador no conoce la intención del diseño).

## Game Design Document (KONZEPT.md)

Registra cada juego en un GDD conciso — plantilla: [`assets/KONZEPT_template.md`](assets/KONZEPT_template.md). Estructura mínima:

- **Visión** — 1–2 frases: ¿Qué es el juego?
- **Género / referencia** — clasificación + títulos de referencia.
- **Mecánicas principales** — **máx. 3–4** (el enfoque fuerza la calidad).
- **Gameplay loop** — el bucle minuto a minuto del jugador.
- **Modos de juego / formatos de tiempo** — si procede.
- **Monetización** — gamepasses, productos de desarrollador, pase de batalla, tienda.
- **Tecnología** — stack (Rojo/frameworks), arquitectura general.
- **Próximos pasos** — lista de verificación de implementación.
- **Errores conocidos / tareas pendientes**.

## División del trabajo multi-agente

Varios agentes de IA (o humano+IA) pueden dividirse un juego — dos modos:

- **Swarm (Enjambre)** — misma tarea, diferentes áreas (p. ej., tres agentes balancean cada uno un sistema).
- **Team (Equipo)** — diferentes roles, coordinados entre sí (Engineer + Artist + Polish en paralelo en una función, coordinados por el Creative Director).

Demostrado en la práctica: **nunca** asignes el desarrollo y las pruebas al mismo agente; establece prompts fijos por rol (system prompt = descripción del rol); cada iteración de la cadena termina con un historial de cambios + informe de prueba; el humano se mantiene como el filtro de calidad.

## Contexto de mercado específico de Roblox (orientación)

Conocimiento de la plataforma en el que se basa el trabajo conceptual para Roblox (sin garantía, solo reglas generales):

- **Géneros rentables:** Simulator, RPG, Tycoon, Horror, Obby — escalado y esfuerzo muy diferentes.
- **Nichos desatendidos (mayor riesgo, menor competencia):** estrategia real/RTS-lite, juegos deportivos de alta calidad, cozy/simulador de vida, puzle/escape cooperativo, auto-battler.
- **Reglas de oro de monetización:** (1) LiveOps es obligatorio (actualizaciones cada 2–4 semanas), (2) la monetización debe *apoyar* el juego, no bloquearlo, (3) el diseño social (intercambio, cooperativo) es infraestructura, (4) mobile-first (más del 50 % juega en teléfonos), (5) la idoneidad para creadores de contenido (YouTube/TikTok) es marketing.

> Para obtener cifras de mercado actuales y fiables, investiga en lugar de estimar; los puntos anteriores son heurísticas estables, no datos en vivo.

## Lecturas adicionales

- Skills hermanas: `/rojo`, `/rbx-studio`; meta-skill `/rbx-dev` (patrones de arquitectura, estructura del proyecto, lecciones de Luau).
- Pipeline de referencia (si está disponible): `<your Roblox project pipeline>` (`AGENT_ROLES.md`, `GUIDE.md`, `IDEAS.md`, análisis de mercado).

## Registro de cambios

### 1.0.0 (2026-06-17)
- Versión inicial. Marco genérico de roles y flujos de trabajo, extraído de `.ROBLOX/AGENT_ROLES.md` y `GUIDE.md`, neutral para el usuario (sin portafolio específico del proyecto).