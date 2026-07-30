---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Terapia Cognitivo-Conductual: modelo ABC, pensamientos automáticos, identificación de distorsiones cognitivas y registro de pensamientos.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [cbt, cognitive-restructuring, cognitive-distortions, thought-record, abc-model]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/kognitive_umstrukturierung.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `cognitive-restructuring`.


# Cognitive Restructuring (Español)

> Técnica principal de TCC: esquema ABC, identificación y modificación de pensamientos disfuncionales

See: [ETHICS.md](../ETHICS.md)

---

## Contexto

La reestructuración cognitiva es una técnica fundamental de la Terapia Cognitivo-Conductual (TCC). Ayuda a identificar pensamientos automáticos negativos, cuestionarlos y reemplazarlos por alternativas más adaptativas y útiles.

**Nota:** Esto es un apoyo, no un sustituto de la terapia profesional.
**Nunca implementar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. Modelo ABC (Ellis)

El modelo ABC explica cómo se relacionan los eventos, los pensamientos y las emociones.

```
A (Activating Event)   ->  B (Beliefs / Thoughts)  ->  C (Consequences / Feelings/Behavior)
Trigger                     Evaluation / Belief           Emotional consequence
```

**Importante:** ¡No es el evento (A) el que genera la emoción (C), sino la evaluación cognitiva (B)!

**Ejemplo:**
```
A: Boss criticizes a report in a meeting
B: "I am incompetent, everyone thinks so now"
C: Shame, withdrawal, avoiding future contributions
```

**Objetivo:** Modificar B para influir en C.

---

## 2. Identificación de Pensamientos Automáticos Negativos (PAN)

**¿Qué son los PAN?**
- Evaluaciones rápidas y automáticas en situaciones de estrés
- Percibidos a menudo como hechos, aunque son interpretaciones
- Tienden a la exageración, la generalización y la catastrofización

**Características típicas de reconocimiento:**
- Pensamiento absoluto: "siempre", "nunca", "todos", "nadie"
- Catastrofización: "Esto terminará terriblemente"
- Lectura de pensamiento: "Deben pensar que..."
- Sobregeneralización: "Esto nunca me sale bien"

**Preguntas de reconocimiento:**
- "¿Qué pasó por tu mente cuando eso sucedió?"
- "Cuando piensas en la situación, ¿qué palabras surgen?"
- "¿Qué temes que pueda pasar?"

---

## 3. Distorsiones cognitivas (Errores de pensamiento)

| Distorsión | Descripción | Ejemplo |
|------------|-------------|---------|
| Pensamiento del todo o nada | Pensamiento en blanco y negro | "Si no soy perfecto, soy un fracaso" |
| Sobregeneralización | Un solo caso = patrón general | "Esto siempre me sale mal" |
| Filtro mental | Percibir solo aspectos negativos | Enfocarse únicamente en la única crítica de un informe |
| Lectura de pensamiento | Creer saber lo que otros piensan | "Seguro que me odian" |
| Catastrofización | Asumir el peor escenario | "Esto será una catástrofe" |
| Razonamiento emocional | Emoción = realidad | "Me siento estúpido, por lo tanto soy estúpido" |
| Pensamiento de "debería/tengo que" | Reglas rígidas | "Debería ser capaz de hacer esto" |
| Personalización | Relacionar todo consigo mismo | "El mal resultado del proyecto fue mi culpa" |

---

## 4. Cuestionamiento de pensamientos (Diálogo socrático)

**Objetivo:** No refutar directamente los pensamientos, sino fomentar su examen y evaluación.

**Conjunto de preguntas:**

1. **Examinar la evidencia:**
   - "¿Qué evidencia hay a favor de esto?"
   - "¿Qué evidencia hay en contra?"

2. **Explicaciones alternativas:**
   - "¿Existen otras explicaciones para esto?"
   - "¿Cómo vería otra persona esta situación?"

3. **Evaluar las consecuencias:**
   - "¿Qué es lo peor que podría pasar? ¿Qué tan probable es?"
   - "¿Qué es lo mejor que podría pasar?"
   - "¿Cuál es el resultado más realista?"

4. **Comprobar la utilidad:**
   - "¿Me ayuda este pensamiento a alcanzar mis objetivos?"
   - "¿Qué le diría a un buen amigo que pensara de esta manera?"

---

## 5. Reestructuración cognitiva paso a paso

### Formato de registro (Registro de pensamientos)

```
SITUATION
What happened? (When? Where? Who was there?)
[Free text]

THOUGHT
What went through my mind?
Automatic thought: [...]
How much do I believe it? (0-100%): [...]%

EMOTION
What emotions did I have?
Emotion: [...]    Intensity (0-100%): [...]%

COGNITIVE DISTORTION
Which cognitive distortions are involved?
[List from table above]

EXAMINE
Evidence for: [...]
Evidence against: [...]
Alternative perspective: [...]

ALTERNATIVE THOUGHT
More balanced, realistic thought:
[...]
How much do I believe it? (0-100%): [...]%

RESULT
Emotion afterward: [...]   Intensity: [...]%
Takeaway: [...]
```

---

## 6. Activación conductual

**Complemento al trabajo cognitivo:** La modificación de la conducta respalda el cambio de pensamiento.

**Principio:** Actividades positivas -> Mejor estado de ánimo -> Pensamientos más adaptativos

**Pasos:**
1. Crear una lista de actividades agradables o significativas
2. Planificar las actividades (específicamente: cuándo, cómo, dónde)
3. Registrar la ejecución
4. Evaluar el estado de ánimo antes y después

**Ejemplos de actividades:**
- Pasear (naturaleza, aire fresco)
- Contacto con personas importantes
- Actividades creativas
- Ejercicio físico
- Cosas que antes aportaban satisfacción o placer

---

## Ética y límites

**Un asistente de IA PUEDE:**
- Explicar distorsiones cognitivas y el modelo ABC
- Formular preguntas socráticas
- Guiar registros de pensamientos
- Proporcionar psicoeducación sobre técnicas de TCC

**Un asistente de IA NO DEBE:**
- Sustituir una terapia cognitivo-conductual profesional
- Realizar diagnósticos o recomendaciones de tratamiento
- Llevar a cabo intervenciones en crisis
- Aplicar EMDR, Exposición Prolongada (PE) o Terapia de Exposición Narrativa (NET)

**En caso de crisis aguda, derivar SIEMPRE a:**
- Línea de Prevención del Suicidio y Crisis (EE. UU.): 988
- Crisis Text Line (EE. UU.): Envía HOME al 741741
- Samaritans (Reino Unido): 116 123
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

## Referencias

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*Adaptado de BACH v3.8.0 | Versión independiente*
*Fuentes: Beck (1979), Ellis (1962) — No sustituye a la terapia profesional*
