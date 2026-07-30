---
name: cognitive-restructuring
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Terapia Cognitivo-Conductual: Modelo ABC, pensamientos automáticos, identificación de distorsiones cognitivas y registros de pensamientos.
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


# Reestructuración Cognitiva (Español)

> Técnica central de la TCC: Esquema ABC, identificación y modificación de pensamientos disfuncionales

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

La reestructuración cognitiva es una técnica fundamental de la Terapia Cognitivo-Conductual (TCC). Ayuda a identificar pensamientos automáticos negativos, cuestionarlos y reemplazarlos por alternativas más adaptativas y útiles.

**Nota:** Esto es un apoyo, no un sustituto de la terapia profesional.
**Nunca aplicar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. El Modelo ABC (Ellis)

El modelo ABC explica cómo se relacionan los acontecimientos, los pensamientos y los sentimientos.

```
A (Acontecimiento Activador) -> B (Creencias / Pensamientos) -> C (Consecuencias / Sentimientos/Conducta)
Desencadenante                   Evaluación / Creencia            Consecuencia emocional
```

**Importante:** ¡No es el acontecimiento (A) el que crea la emoción (C), sino la evaluación o interpretación (B)!

**Ejemplo:**
```
A: El jefe critica un informe en una reunión
B: "Soy incompetente, ahora todos lo piensan"
C: Vergüenza, aislamiento, evitar futuras contribuciones
```

**Objetivo:** Modificar B para influir positivamente en C.

---

## 2. Identificación de Pensamientos Automáticos Negativos (PANs)

**¿Qué son los PANs?**
- Evaluaciones rápidas y automáticas en situaciones de estrés
- A menudo se perciben como hechos reales, aunque son interpretaciones
- Tienden a la exageración, la generalización y la catastrofización

**Características típicas de reconocimiento:**
- Pensamiento absoluto: "siempre", "nunca", "todos", "nadie"
- Catastrofización: "Esto terminará terriblemente"
- Lectura de mente: "Seguro están pensando que..."
- Sobregeneralización: "Esto nunca me sale bien"

**Preguntas para identificarlos:**
- "¿Qué pasó por tu mente cuando ocurrió eso?"
- "Cuando piensas en la situación, ¿qué palabras surgen?"
- "¿Qué temes que pueda pasar?"

---

## 3. Distorsiones Cognitivas (Sesgos Cognitivos)

| Distorsión | Descripción | Ejemplo |
|------------|-------------|---------|
| Todo o nada | Pensamiento en blanco y negro | "Si no soy perfecto, soy un fracaso" |
| Sobregeneralización | Un solo caso = patrón general | "Esto siempre me sale mal" |
| Filtro mental | Percibir únicamente lo negativo | Centrarse en la única crítica dentro de un elogio |
| Lectura de mente | Creer saber lo que otros piensan | "De seguro me odian" |
| Catastrofización | Asumir el peor escenario posible | "Esto va a ser una catástrofe" |
| Razonamiento emocional | Sentimiento = realidad | "Me siento estúpido, por lo tanto lo soy" |
| Pensamiento de "debería/tengo que" | Reglas rígidas e inflexibles | "Debería ser capaz de hacer esto" |
| Personalización | Relacionarlo todo consigo mismo | "El fracaso del proyecto fue mi culpa" |

---

## 4. Cuestionamiento de Pensamientos (Debate Socrático)

**Objetivo:** No refutar los pensamientos directamente, sino fomentar el examen crítico.

**Conjunto de preguntas:**

1. **Examinar la evidencia:**
   - "¿Qué evidencia hay a favor de este pensamiento?"
   - "¿Qué evidencia hay en contra?"

2. **Explicaciones alternativas:**
   - "¿Existen otras explicaciones para esto?"
   - "¿Cómo vería esta situación otra persona?"

3. **Evaluar consecuencias:**
   - "¿Qué es lo peor que podría pasar? ¿Qué tan probable es?"
   - "¿Qué es lo mejor que podría pasar?"
   - "¿Cuál es el resultado más realista?"

4. **Comprobar la utilidad:**
   - "¿Me ayuda este pensamiento a alcanzar mis objetivos?"
   - "¿Qué le diría a un buen amigo que pensara de esta manera?"

---

## 5. Reestructuración Cognitiva Paso a Paso

### Formato de Registro (Registro de Pensamientos)

```
SITUACIÓN
¿Qué sucedió? (¿Cuándo? ¿Dónde? ¿Quién estaba allí?)
[Texto libre]

PENSAMIENTO
¿Qué pasó por mi mente?
Pensamiento automático: [...]
¿Cuánto lo creo? (0-100%): [...]%

EMOCIÓN
¿Qué emociones sentí?
Emoción: [...]    Intensidad (0-100%): [...]%

DISTORSIÓN COGNITIVA
¿Qué distorsiones cognitivas están presentes?
[Lista de la tabla anterior]

EXAMINAR
Evidencia a favor: [...]
Evidencia en contra: [...]
Perspectiva alternativa: [...]

PENSAMIENTO ALTERNATIVO
Pensamiento más equilibrado y realista:
[...]
¿Cuánto lo creo? (0-100%): [...]%

RESULTADO
Emoción posterior: [...]   Intensidad: [...]%
Aprendizaje/Conclusión: [...]
```

---

## 6. Activación Conductual

**Complemento al trabajo cognitivo:** Modificar la conducta apoya el cambio de pensamiento.

**Principio:** Actividades positivas -> Mejor estado de ánimo -> Pensamientos más útiles

**Pasos:**
1. Crear una lista de actividades agradables/significativas
2. Planificar actividades (específicamente: cuándo, cómo, dónde)
3. Registrar la realización
4. Calificar el estado de ánimo antes y después

**Ejemplos de actividades:**
- Paseo (naturaleza, aire fresco)
- Contacto con personas importantes
- Actividades creativas
- Ejercicio físico
- Cosas que solían brindar alegría

---

## Ética y Límites

**Un asistente de IA puede:**
- Explicar las distorsiones cognitivas y el modelo ABC
- Formular preguntas socráticas
- Guiar registros de pensamientos
- Proporcionar psicoeducación sobre técnicas de TCC

**Un asistente de IA NO debe:**
- Reemplazar la terapia cognitivo-conductual profesional
- Realizar diagnósticos o recomendaciones de tratamiento
- Llevar a cabo intervención en crisis
- Aplicar EMDR, Exposición Prolongada (PE) o Terapia de Exposición Narrativa (NET)

**En caso de crisis aguda, SIEMPRE derivar a:**
- 988 Suicide & Crisis Lifeline (EE. UU.): 988
- Crisis Text Line (EE. UU.): Envíe HOME al 741741
- Samaritans (Reino Unido): 116 123
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

## Referencias

- Beck, A. T. (1979). *Cognitive Therapy and the Emotional Disorders.* Penguin Books.
- Ellis, A. (1962). *Reason and Emotion in Psychotherapy.* Lyle Stuart.

---

*Adaptado de BACH v3.8.0 | Versión independiente*
*Fuentes: Beck (1979), Ellis (1962) — No es terapia profesional*