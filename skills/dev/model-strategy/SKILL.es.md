---
name: model-strategy
version: 2.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-06-13
description: Orquestación multimodelo y estrategia de cambio de modelo. Selección de modelo basada en puntuación, delegación entre agentes (Gemini, Codex, Ollama), emparejamiento de asesores (advisor), disparadores de escalado, matriz de permisos y optimización de costes.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [model-switching, orchestration, multi-model, cost-optimization, routing, cross-agent, advisor]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/ing-strategie.md', 'origin_version': '2.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `model-strategy`.


# Estrategia de cambio de modelo (Model-Switching Strategy) (Español)

> Orquestación multimodelo: selección basada en puntuación, delegación entre agentes, emparejamiento de asesores, disparadores de escalado y optimización de costes.

---

## 1. Catálogo de modelos

### Claude (capaz de subagentes mediante la herramienta Agent)

```
Nivel 4 (Revisor):     Opus 4.8  — asesor, revisión matemática  [solo usuario: /model, /advisor]
Nivel 3 (Estratega):   Opus 4.6  — arquitectura, conceptos      [subagente: model:"opus"]
Nivel 3 (Creativo):    Fable 5   — textos creativos, historias  [subagente: model:"fable"]
Nivel 2 (Trabajador):  Sonnet 4.6— implementación, depuración   [subagente: model:"sonnet"]
Nivel 1 (Rápido):      Haiku 4.5 — código base, formato         [subagente: model:"haiku"]
```

### Agentes externos (scripts complementarios / SSH)

```
Nivel 2-3: Gemini 3.5 pro  — investigación, bases de datos científicas [CLI agy-companion]
Nivel 2:   Gemini 3.5 flash— investigación rápida                      [CLI agy-companion]
Nivel 2-3: Codex 5.5 (GPT) — revisión de código, generación de código [CLI codex-companion]
Nivel 2:   Codex 4.5 (GPT) — tareas de código más simples              [CLI codex-companion]
```

### Modelos locales (sin tokens, 24/7)

```
Nivel 1-2: Ollama (Qwen 3.5:35b-a3b) — nivel Haiku-a-Sonnet [<host-ollama>:11434]
           Invocación: SSH + curl http://<host-ollama>:11434/v1/chat/completions
           O: delegación a través de una API de control del sistema de agentes (si está disponible)
```

### Matriz de alcanzabilidad

| Modelo | Iniciable por LLM | Ruta de invocación | Restricciones |
|--------|-------------------|--------------------|---------------|
| Sonnet 4.6 | Sí | `Agent(model:"sonnet")` | — |
| Opus 4.6 | Sí | `Agent(model:"opus")` | — |
| Haiku 4.5 | Sí | `Agent(model:"haiku")` | — |
| Fable 5 | Sí | `Agent(model:"fable")` | — |
| Opus 4.8 | Solo como asesor | `advisor()` en sesión | el usuario debe configurar `/advisor` |
| Gemini 3.5 | Sí (Bash) | `companion-for-agy "prompt"` | solo Windows, solución alternativa stdout |
| Codex 5.5/4.5 | Sí (Bash) | `node codex-companion.mjs task "prompt"` | requiere autenticación |
| Ollama | Sí (SSH/curl) | SSH + curl a la API del host Ollama | VPN/Tailscale debe estar activo |
| Opus 4.8 como modelo principal | No | usuario: `/model opus 4.8` | solo acción del usuario |
| Fable 5 como modelo principal | No | usuario: `/model fable` | solo acción del usuario |

---

## 2. Cálculo de puntuación (Score)

```
Dimensiones (0-10):
  CLARIDAD      : ¿Qué tan unívoca es la tarea?
  COMPLEJIDAD   : ¿Cuántos componentes?
  CREATIVIDAD   : ¿Se necesitan soluciones nuevas?
  CONTEXTO      : ¿Cuánto conocimiento previo?
  CRITICIDAD    : ¿Qué tan importante es la perfección?

PUNTUACIÓN = (10 - CLARIDAD) + COMPLEJIDAD + CREATIVIDAD + CONTEXTO + CRITICIDAD
```

### Umbrales de puntuación

| Puntuación | Modelo | Ejemplos |
|------------|--------|----------|
| 0-8 | Ollama (host local) | generación de prompts, resúmenes, textos simples |
| 9-12 | Haiku | __init__.py, formato, código base |
| 13-22 | Sonnet | implementación, corrección de errores, código estándar |
| 13-22 | Gemini 3.5 | investigación, búsqueda de literatura, bases de datos científicas |
| 13-22 | Codex 5.5 | generación de código (Luau, Node.js), scripts de cálculo |
| 23-28 | Sonnet + revisión de asesor | código complejo con control de calidad |
| 23-35 | Fable 5 | textos creativos, marketing, narrativa |
| 29-40 | Opus 4.6 | arquitectura, estrategia, redacción de artículos |
| 35-50 | Opus 4.6 + asesor | demostraciones, decisiones de arquitectura, estadística |
| 40-50 | Opus 4.8 (recomendación al usuario) | demostraciones matemáticas, máximo rigor |

---

## 3. Delegación entre agentes

### ¿Qué agente externo para qué tarea?

| Tarea | Mejor agente | Razón |
|-------|--------------|-------|
| Búsqueda de literatura científica | Gemini 3.5 pro | skills nativos de OpenAlex/arXiv/PubMed |
| Revisión de código (segunda opinión) | Codex 5.5 | perspectiva independiente |
| Generación de texto simple | Ollama (host local) | sin tokens, 24/7 |
| Textos creativos, marketing | Fable 5 | salida creativa más sólida |
| Demostraciones matemáticas | Opus 4.8 (asesor) | máxima profundidad analítica |

### Exclusiones (debilidades documentadas)

- **Gemini:** NO para revisiones matemáticas o trabajo de demostración (error de dirección documentado en una revisión de demostración, 2026-06-07)
- **Codex 4.5:** solo cuando 5.5 no esté disponible; de lo contrario, siempre 5.5

### Rutas de invocación

> Reemplaza los marcadores `<host>`, `<host-ollama>`, `<ip-tailscale>`, `<usuario>` y `~/.ssh/<clave>` con tu propia infraestructura.

**Gemini (vía companion-for-agy):**
```
companion-for-agy --researcher --json --timeout 120000 "prompt de investigación"
```

**Codex (vía codex-companion):**
```
node "~/.claude/plugins/cache/openai-codex/codex/1.0.4/scripts/codex-companion.mjs" task --effort high "prompt de código"
```

**Ollama en un host remoto (vía SSH):**
```
ssh -i ~/.ssh/<clave> <usuario>@<ip-tailscale> "curl -s http://localhost:11434/v1/chat/completions -d '{\"model\":\"qwen3.5:35b-a3b\",\"messages\":[{\"role\":\"user\",\"content\":\"Prompt\"}]}'"
```

**Delegación a un sistema de agentes con herramientas (ejemplo):**
```
curl -s -X POST http://<host>:8081/api/chat -H "Content-Type: application/json" -d '{"prompt": "...", "chat_id": "claude-delegate"}'
```

---

## 4. Emparejamiento de asesores (Advisor pairing)

### Mecánica

`advisor()` es una **herramienta a nivel de sesión**: el usuario establece el modelo asesor mediante `/advisor`, no programáticamente. Esto genera los siguientes patrones de emparejamiento:

| Patrón | Cómo funciona | Cuándo usar |
|--------|---------------|-------------|
| **Asesor de sesión** | el usuario configura `/advisor opus 4.8`, el agente llama a `advisor()` | estándar para demostraciones/arquitectura |
| **Orquestador como revisor** | el modelo principal Opus revisa la salida del subagente Sonnet | el orquestador es más fuerte que el trabajador |
| **Contra-agente** | el agente A trabaja, el agente B comprueba adversariamente | verificación independiente, 2 perspectivas |
| **Recomendación al usuario** | el agente recomienda: "realiza esta tarea con opus 4.8 + asesor" | cuando la sesión actual es demasiado débil |

### ¿Cuándo recomendar un asesor?

- Demostraciones matemáticas (puntuación ≥ 35)
- Decisiones de arquitectura con consecuencias a largo plazo
- Metodología estadística / diseño de estudios
- Errores complejos después de 2+ ciclos de depuración infructuosos

### ¿Cuándo NO usar un asesor?

- Código rutinario, contenido, formato (puntuación < 23)
- Implementación de funcionalidades simples
- Tareas bien definidas y no críticas

---

## 5. Disparadores de escalado

### Ollama -> Haiku
- Requiere acceso a archivos
- Necesita análisis de código

### Haiku -> Sonnet
- Más de 2 archivos afectados
- Necesita decisión entre alternativas
- Ocurrió un error inesperado
- Se solicita operación de eliminación

### Sonnet -> Opus
- Requiere decisión de arquitectura
- Se deben integrar 3+ sistemas
- Requisitos contradictorios/pocos claros
- Necesita planificación estratégica

### Sonnet -> Gemini (lateral)
- Necesita investigación científica
- Verificación bibliográfica

### Sonnet -> Codex (lateral)
- Revisión de código como segunda opinión
- Asesor sobrecargado (revisor de respaldo)

### Opus -> Opus + asesor
- Necesita revisión de demostración
- Decisión de arquitectura crítica
- Metodología estadística

### Desescalado
- Concepto definido -> Sonnet asume la implementación
- Tarea trivial/repetitiva -> Haiku asume el control
- Solo texto, sin acceso a herramientas -> Ollama asume el control

---

## 6. Matriz de permisos

| Operación | Ollama | Haiku | Sonnet | Opus | Gemini | Codex |
|-----------|--------|-------|--------|------|--------|-------|
| Leer archivos | - | Sí | Sí | Sí | Sí* | Sí* |
| Escribir archivos | - | Sí | Sí | Sí | Sí* | Sí* |
| Eliminar archivos | - | - | Sí** | Sí | - | - |
| Comandos del sistema | - | - | Sí** | Sí | Sí* | Sí* |
| Decisiones de arquitectura | - | - | - | Sí | - | - |
| Investigación web | - | - | Sí | Sí | Sí | - |
| Llamar a advisor() | - | - | Sí | Sí | - | - |

*vía script complementario en su propio modo sandbox
**con confirmación del usuario

---

## 7. Eficiencia de costes

### Ahorro de tokens mediante enrutamiento

| Tipo de tarea | Sin enrutamiento | Con enrutamiento | Ahorro |
|---------------|------------------|------------------|--------|
| Trivial | Tokens Opus | Ollama (gratis) | 100% |
| Código base | Tokens Opus | Tokens Haiku | ~80% |
| Código estándar | Tokens Opus | Tokens Sonnet | ~50% |
| Investigación | Tokens Claude | Tokens Gemini | ~70% (presupuesto distinto) |
| Revisión de código | Tokens advisor() | Tokens Codex | ~60% (presupuesto distinto) |

---

## 8. Regla de oro

> "Opus piensa, Sonnet construye, Haiku ejecuta, Ollama ahorra. Gemini investiga, Codex revisa, Fable narra."

---

## Historial de Cambios

### 2.0.0 (2026-06-12)
- Delegación entre agentes: Gemini, Codex, Ollama (host local) como destinos de enrutamiento
- Emparejamiento de asesores: 4 patrones (asesor de sesión, orquestador como revisor, contra-agente, recomendación al usuario)
- Matriz de alcanzabilidad: documentada iniciable por LLM vs. solo usuario
- Añadido Ollama (Qwen 3.5:35b-a3b, nivel Haiku-a-Sonnet) como nivel 1-2
- Escalado lateral: Sonnet -> Gemini (investigación), Sonnet -> Codex (revisión)
- Exclusiones documentadas (Gemini no para matemáticas)
- Umbrales de puntuación extendidos a todos los modelos

### 1.0.0 (2026-03-15)
- Adaptado desde BACH v3.8.0 (ing-strategie v2.0.0)

---

*Adaptado desde BACH v3.8.0 | Ampliado con cross-agent + asesor v2.0.0*