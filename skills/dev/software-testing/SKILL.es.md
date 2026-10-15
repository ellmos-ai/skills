---
name: software-testing
version: 1.0.1
type: knowledge-protocol
author: Lukas Geiger
created: 2026-08-22
updated: 2026-08-22
description: "Asesor de estrategia de pruebas para proyectos de software — elige los niveles de prueba adecuados (unitarias/integración/sistema/aceptación), los tipos de prueba (funcionales, no funcionales, relacionadas con cambios) y las técnicas de diseño de pruebas (clases de equivalencia, valores límite, tablas de decisión, exploratorias) para la situación concreta y la fase de SDLC/CI, incluyendo pirámide de pruebas, puertas de CI/CD, Shift-Left y buenas prácticas. Usa esta skill SIEMPRE que haya que escribir, planificar, priorizar o evaluar pruebas — con \"escribe pruebas\", \"estrategia de pruebas\", \"plan de pruebas\", \"concepto de pruebas\", \"qué/cómo debo probar\", \"qué pruebas faltan\", \"mejorar la cobertura de pruebas\", \"poner en marcha QA\", preguntas sobre pruebas de regresión/smoke/sanity/carga/estrés/seguridad o al configurar un pipeline de pruebas — incluso cuando \"prueba\" aparezca solo de paso. Delimitación — para el propio ciclo TDD usa superpowers:test-driven-development, para el diagnóstico de errores bugfix-protocol, para la búsqueda sistemática de errores bugsweep."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [testing, teststrategie, qa, unit-test, integration, regression, testpyramide, shift-left, ci-cd, istqb]
language: es
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'claude-code-recherche', 'origin_version': '1.0.0', 'created_from': 'Online-Recherche 2026-08-22 (ISTQB-Systematik, Testpyramide, Agile Testing Quadrants, moderne Verfahren); Quellen siehe testarten-katalog.md'}
translated_from_sha256: 85a9672454c8df2d2e0dfd1a87d5468a7ebc030e45a1fa2843f361bba80c8b80
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:44.041978+00:00"
---
<img src="banner.png" width="100%" alt="software-testing banner">

# Pruebas de software: estrategia de pruebas y selección de pruebas

Esta skill responde a la pregunta **«¿Qué pruebas necesito aquí, ahora, y para qué?»**, de forma sistemática y no a ojo. Proporciona la lógica de decisión; el catálogo completo de todos los tipos de prueba, técnicas y definiciones se encuentra en
`testarten-katalog.md` en la misma carpeta (para preguntas de detalle, consúltalo allí).

---

## 1. Marco de orden: pensar en tres dimensiones

Antes de planificar o escribir pruebas, ubica la tarea en tres ejes (ISTQB). Quien solo lleva «una lista de pruebas» mezcla los ejes y planifica con lagunas:

| Eje | Pregunta | Manifestaciones |
|---|---|---|
| **Nivel de prueba** | ¿En qué nivel? | Unitario → Integración → Sistema → Aceptación |
| **Tipo de prueba** | ¿Qué propiedad? | funcional / no funcional / basado en la estructura / relacionado con cambios |
| **Técnica de prueba** | ¿Cómo surgen los casos de prueba? | Caja negra / Caja blanca / basada en la experiencia |

Transversalmente: **estático** (revisiones, análisis estático — sin ejecución, detección de errores más temprana y económica) frente a **dinámico** (el código se ejecuta).

---

## 2. Enrutador de situaciones: ¿qué se tiene?

Elige el punto de partida según la situación concreta:

| Situación | Procedimiento |
|---|---|
| **Construir una nueva funcionalidad** | Aclarar los criterios de aceptación ANTES del código (mentalidad ATDD/BDD). Pruebas unitarias en paralelo a la implementación (clases de equivalencia + valores límite). Prueba de integración para nuevas interfaces. Un E2E de camino feliz, no más. |
| **Corregir un error** | Primero una prueba que reproduzca el error (rojo), luego la corrección (verde) = **re-test**. Después **regresión** del entorno. El diagnóstico en sí → `bugfix-protocol`. |
| **Refactorización** | NINGUNA prueba nueva de funcionalidad — la suite existente es la red de seguridad. Antes comprobar si la suite cubre realmente el comportamiento (dado el caso, completar con pruebas de caracterización). Cobertura/mutación como indicador de lagunas. |
| **Código heredado sin pruebas** | No empezar con pruebas unitarias de cada función. Primero pruebas de caracterización a nivel de sistema/API que fijen el comportamiento actual; al tocar partes concretas, añadir después pruebas unitarias. |
| **API / microservicios** | Centrarse en pruebas de API a nivel de servicio (nivel medio de la pirámide). Con equipos o despliegues separados: **Contract Testing** (p. ej. Pact) en lugar de pruebas de integración compartidas en staging. |
| **Preparar un release** | Orden: smoke (¿build estable?) → regresión completa → pruebas no funcionales (carga, seguridad) → UAT/aceptación → smoke sobre el candidato a release. |
| **Preocupación por el rendimiento** | Definir primero un objetivo medible (p. ej. «P95 < 300 ms con 1.000 usuarios»), si no ninguna prueba es evaluable. Prueba de carga = carga normal, prueba de estrés = punto de rotura y recuperación. Entorno cercano a producción obligatorio. |
| **Montar un pipeline de pruebas** | Implementar las puertas de CI/CD del apartado 4; empezar con unitarias + lint en cada commit y ampliar por etapas. |
| **Escribir una estrategia de pruebas/concepto de pruebas** | Estructura a lo largo de los 3 ejes + mapeo por fases (apartado 4) + priorización basada en riesgo (apartado 6, punto 10). |

---

## 3. Niveles de prueba: objeto, objetivo, momento

| Nivel | Comprueba | Cuándo | Regla práctica |
|---|---|---|---|
| **Unidad/componente** | Función/clase individual aislada (mocks/stubs) | Durante la implementación, cada commit | Base amplia de la pirámide; rápida (< segundos), determinista |
| **Integración** | Interacción, interfaces, conexión con BD | Tras las pruebas unitarias, en cada merge | Integrar de forma incremental (Top-Down/Bottom-Up), nunca Big Bang en sistemas grandes |
| **Sistema** | Sistema completo frente a requisitos técnicos | En cuanto exista un build integrado | Funcional Y no funcional; testers independientes valiosos |
| **Aceptación** | Expectativa de negocio, uso real | Última etapa antes del go-live | UAT por parte del área especializada; no olvidar lo operativo (backup/despliegue/monitorización); dado el caso alfa/beta |

**Pirámide de pruebas** como proporción: muchas pruebas unitarias, pruebas de integración/API específicas, pocas E2E (regla orientativa ~70/20/10 como punto de partida — ajustar según el origen real de los errores). Una pirámide invertida (muchas pruebas de UI) = lenta + inestable → evitar.

---

## 4. Mapeo por fases: ¿cuándo se prueba qué?

### Puertas de CI/CD (mapeo estándar moderno)

| Etapa del pipeline | Puerta |
|---|---|
| Cada commit | Pruebas unitarias, linters, análisis estático (segundos–minutos) |
| Pull Request | Revisión de código, SAST/SCA, pruebas de componente selectivas |
| Merge | Pruebas de integración/API/contrato, smoke en el entorno de pruebas |
| Nightly / pre-release | Regresión completa, E2E, pruebas de rendimiento/carga, DAST |
| Candidato a release | Smoke en staging, UAT, aceptación |
| Producción (Shift-Right) | Monitorización/observabilidad, canary/blue-green, feature flags, dado el caso experimentos de caos |

**Presupuestos de tiempo y reglas de bloqueo (valores orientativos de la práctica):**

- **Commit hasta feedback < 10 minutos** para la vía rápida (lint + unitarias + pruebas de integración críticas); pipeline completo hasta staging **< 30–45 minutos**; regresión completa nightly o antes del release. Un ciclo de retroalimentación más lento se acaba eludiendo.
- **Bloqueante frente a informativa:** las puertas unitarias, de integración y smoke SIEMPRE bloquean (si hay rojo, no hay merge/despliegue). Las etapas nightly (regresión, carga, DAST) informan mediante ticket/corrección, pero no bloquean cada commit. Tras el despliegue en producción: smoke + monitorización — si hay rojo, rollback + incidente.
- **Punto de transferencia:** el commit (git push) separa el inner loop (local: TDD, unitarias, iteración rápida) del outer loop (pipeline compartido con puertas). Lo que pueda trasladarse al inner loop se detecta allí de la forma más económica (Shift-Left).

### Clásico (modelo V): diseñar pruebas al especificar

Requisitos ↔ prueba de aceptación · Diseño del sistema ↔ prueba de sistema · Arquitectura ↔ prueba de integración · Código ↔ prueba unitaria. Idea central: las pruebas de un nivel se diseñan **al crear la especificación correspondiente** — no al final. Las revisiones de requisitos/diseños (prueba estática) son la detección de errores más temprana de todas.

### Cuadrantes de Agile Testing (matriz de planificación de sprints)

Q1 unitarias/TDD + Q2 pruebas de historias/BDD se ejecutan de forma continua y **previenen** errores; Q3 exploratorias/usabilidad/UAT + Q4 rendimiento/seguridad **evalúan** el producto, en cuanto exista suficiente producto. Detalles en el catálogo.

---

## 5. Elegir la técnica de diseño de pruebas

| Si la base de pruebas … | … entonces técnica |
|---|---|
| tiene rangos de entrada/conjuntos de valores | **Clases de equivalencia** (un representante por clase) + **análisis de valores límite** (en y justo más allá de cada límite: para 5–50 probar 4, 5, 50, 51) — el equipamiento básico para casi toda prueba unitaria |
| tiene reglas de negocio complejas/combinaciones de condiciones | **Prueba con tabla de decisión** |
| tiene estados y transiciones (flujo de trabajo, sesión, dispositivo) | **Prueba de transición de estados** (probar también las transiciones prohibidas) |
| describe flujos de usuario | **Prueba de casos de uso/escenarios** incl. rutas de error y excepción |
| hay código y se quiere medir la cobertura | **Cobertura de sentencias/ramas** — como indicador de lagunas, no como objetivo (100 % de cobertura ≠ correcto) |
| es poco clara o incompleta, o el tiempo escasea | **Pruebas exploratorias** (sesiones con límite de tiempo y charter) + **error guessing** (nulo, cadena vacía, caracteres especiales, zonas horarias, condiciones de carrera) |

Primero los procedimientos sistemáticos; las técnicas basadas en la experiencia, de forma deliberada, **como complemento** — encuentran lo que los scripts pasan por alto.

---

## 6. Buenas prácticas (lista de comprobación al planificar/revisar pruebas)

1. **Shift-Left:** revisiones + análisis estático desde la fase de requisitos — cuanto más tarde se detecte un error, más caro (regla empírica difundida según Boehm; la dirección es indiscutible, los factores exactos son controvertidos).
2. **Respetar la pirámide de pruebas** — E2E con moderación, base unitaria amplia.
3. **Automatizar lo que se repite** (smoke, regresión, API, unitarias) y anclarlo en las puertas de CI/CD; reservar capacidad manual para exploratorias + usabilidad.
4. **Diseñar los casos de prueba de forma sistemática** (apartado 5), no ad hoc.
5. **Hacer medibles los requisitos no funcionales** — sin un valor numérico objetivo no hay prueba de rendimiento/carga evaluable.
6. **Re-test ≠ regresión:** primero confirmar la corrección, luego los efectos colaterales. Orden smoke → sanity/re-test → regresión.
7. **Tratar de inmediato las pruebas inestables (flaky)** — ponerlas en cuarentena, corregir la causa o eliminarlas; las suites inestables destruyen la confianza en el pipeline.
8. **Gestionar datos y entornos de prueba:** reproducibles (contenedores/IaC), cercanos a producción, datos anonimizados o sintéticos.
9. **Medir la calidad de las propias pruebas:** cobertura como indicador de lagunas; **mutation testing** allí donde las cifras de cobertura podrían engañar.
10. **Priorizar según el riesgo:** profundidad de las pruebas según impacto del fallo × probabilidad de error — no distribuida por igual.
11. **La calidad es tarea del equipo** (enfoque de equipo completo): integrar a los testers pronto en los requisitos; BDD/ATDD como vehículo común con el área especializada.
12. **No olvidar el Shift-Right:** monitorización, canary, feature flags; chaos engineering solo con una observabilidad madura.

---

## 7. Procedimientos modernos — cuándo usarlos adicionalmente

| Procedimiento | Usar cuando … |
|---|---|
| **Contract Testing** (Pact) | Microservicios con despliegues/equipos separados |
| **Mutation Testing** (Stryker, PIT, mutmut) | Haya que evaluar la calidad de una suite de pruebas existente |
| **Property-Based Testing** (Hypothesis, fast-check) | Existan invariantes («ordenado es idempotente») y se teman casos límite |
| **Fuzzing** | Parsers, deserialización, entradas críticas para la seguridad |
| **Chaos Engineering** | Sistemas distribuidos + observabilidad madura + rollbacks limpios |

---

## Skills vecinas (no duplicar)

- **`superpowers:test-driven-development`** — el ciclo concreto red-green-refactor al escribir código.
- **`bugfix-protocol`** — diagnóstico de 6 fases de un error concreto.
- **`bugsweep`** — recorrido sistemático de búsqueda de errores sobre una base de código.
- **`dev-cycle`** — ciclo completo de 8 fases (a partir de su v1.2.0: las pruebas se diseñan en las fases 1/3/5, se escriben en la fase 6 y se ejecutan en la fase 7; esta skill completa QUÉ pruebas deben ejecutarse dónde).

## Referencia

Catálogo completo (todos los niveles de prueba, tipos de prueba incl. tabla detallada de no funcionales, todas las técnicas de diseño, Agile Quadrants, estático/dinámico, modelo V, fuentes):
→ `testarten-katalog.md` (en la misma carpeta)

Mapa visual general — fases, ciclos de retroalimentación, roles y puertas de prueba como «esquema de circuito del desarrollo de software» (hoja BL-5 = integración de pruebas, BL-2 = cadencias del ciclo de retroalimentación):
→ `../dev-cycle/SCHALTPLAN-SOFTWAREENTWICKLUNG.html` (abrir en el navegador)

---

## Registro de cambios

### 1.0.1 (2026-08-22)
- Presupuestos de tiempo y reglas de bloqueo para las puertas de CI/CD añadidos (< 10 min vía rápida, < 30–45 min pipeline; bloqueante frente a informativa; rollback tras rojo en producción), así como el commit como punto de transferencia inner/outer loop
- Referencia a la hoja de esquema en la skill dev-cycle; delimitación con dev-cycle ajustada a su v1.2.0 (Shift-Left: diseñar 1/3/5, escribir 6, ejecutar 7)

### 1.0.0 (2026-08-22)
- Versión inicial a partir de investigación en línea (sistemática ISTQB, pirámide de pruebas, Agile Testing Quadrants, puertas de CI/CD, procedimientos modernos)
