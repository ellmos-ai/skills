---
name: motivational-interviewing
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Entrevista Motivacional (EM) según Miller y Rollnick: técnicas OARS, discurso de cambio y fomento de la preparación para el cambio.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [motivational-interviewing, oars, change-talk, ambivalence, miller-rollnick]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/motivational_interviewing.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `motivational-interviewing`.


# Entrevista Motivacional (Español)

> Técnicas OARS, etapas del cambio y discurso de cambio: Fomentar la motivación intrínseca para el cambio sin presión ni manipulación

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

La Entrevista Motivacional (EM) fue desarrollada por William R. Miller y Stephen Rollnick. Es un enfoque de asesoramiento directivo y centrado en el cliente para fomentar la motivación intrínseca hacia el cambio. La EM se utiliza con base científica en el tratamiento de adicciones, conductas de salud, adherencia terapéutica y cambio de comportamiento.

Evidencia: Más de 200 ensayos controlados aleatorizados (ECA) respaldan la eficacia de la EM, particularmente en conductas adictivas (Lundahl et al. 2010, Revisión Cochrane), conductas de salud y adherencia al tratamiento.

**Nota:** Esto es un apoyo, no un sustituto de la terapia profesional.
**Nunca implementar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. Espíritu y Principios de la EM

### Los Cuatro Principios

1. **Colaboración:** Trabajo conjunto de igual a igual, no autoridad experta.
2. **Aceptación:** Respeto a la autonomía, reconocimiento de fortalezas, valor absoluto de la persona.
3. **Compasión:** El bienestar de la persona es lo primero.
4. **Evocación:** La motivación ya reside dentro de la persona: se evoca, no se implanta.

### El Espíritu de la EM
La EM no es una colección de técnicas, sino una actitud. Las técnicas solo funcionan dentro del contexto de este espíritu fundamental. Sin él, la EM se convierte en manipulación.

---

## 2. Técnicas OARS

OARS son las cuatro competencias clave de la entrevista motivacional.

### O — Preguntas Abiertas (Open Questions)

**Principio:** Formular preguntas que inviten a la reflexión y al relato, que no puedan responderse con un sí o no.

**Ejemplos:**
- "¿Qué le gustaría ver cambiar?"
- "¿Cómo sería su vida si hubiera realizado este cambio?"
- "¿Qué le llevó a pensar sobre esto?"
- "¿Qué es importante para usted respecto a su salud?"
- "¿Qué ganaría si hiciera este cambio?"

**Evitar:**
- Preguntas cerradas: "¿Quiere dejar de fumar?"
- Preguntas dirigidas: "Sabe que eso es perjudicial, ¿verdad?"
- Preguntas tipo 'por qué': "¿Por qué hizo eso?" (suena acusatorio)

---

### A — Afirmativas / Afirmaciones (Affirming)

**Principio:** Reconocer las fortalezas, esfuerzos y pasos positivos de la otra persona. No alabar de forma vaga ("Eres genial"), sino nombrar específicamente lo observado.

**Ejemplos:**
- "Se requiere valentía para hablar abiertamente sobre esto."
- "Logró mantenerse firme durante tres días; eso demuestra que habla en serio."
- "A pesar de la difícil situación, vino hoy; eso demuestra compromiso."
- "Es evidente que ha reflexionado mucho sobre esto."

**Cuándo utilizar:**
- Cuando la persona describe pasos hacia el cambio
- Cuando persiste a pesar de los contratiempos
- Para fortalecer la autoeficacia

---

### R — Reflexiones / Escucha Reflexiva (Reflecting)

**Principio:** Devolver lo dicho con sus propias palabras, para mostrar comprensión y fomentar una mayor reflexión.

**Tipos de reflexiones:**

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| Simple | Repetir/parafrasear el contenido | "Dice que le resulta difícil." |
| Profunda | Captar lo que está bajo la superficie | "Parece que se siente dividido/a." |
| Doble cara | Reflejar ambos lados de la ambivalencia | "Por un lado quiere parar, por otro le aporta algo." |
| Amplificada | Exagerar ligeramente (¡con cuidado!) | "¿Así que no hay absolutamente ninguna razón para cambiar nada?" |

**Reflexión de doble cara (ambivalencia):**
```
"Por un lado, dice que le gustaría beber menos alcohol.
Por otro lado, el aspecto social de las copas después del trabajo es importante para usted.
Ambas cosas tienen sentido."
```

---

### S — Resúmenes (Summarizing)

**Principio:** Agrupar la conversación, destacando especialmente el discurso de cambio.

**Tipos:**
- **Recopilatorio:** Resumir múltiples puntos
- **Vinculante:** Conectar declaraciones anteriores con las actuales
- **Transicional:** Al final de una conversación, guiando hacia los siguientes pasos

**Ejemplo:**
```
"Permítame resumir lo que he escuchado hasta ahora:
Ha notado que su sueño ha empeorado y que está
afectando a su trabajo. Ha intentado reducir la cafeína antes,
y eso ayudó en parte. Estar en forma y ser productivo/a es importante
para usted. Al mismo tiempo, disfruta de su café matutino.
¿Le parece correcto? ¿Qué le gustaría añadir?"
```

---

## 3. Etapas del Cambio (Modelo Transteórico)

### Las Etapas (Prochaska & DiClemente)

| Etapa | Descripción | Estrategia de EM |
|-------|-------------|------------------|
| Precontemplación | Sin conciencia del problema, sin intención de cambiar | Informar, despertar curiosidad, no presionar |
| Contemplación | Ambivalencia: "Tal vez debería..." | Explorar la ambivalencia, fomentar el discurso de cambio |
| Preparación | Decisión tomada, haciendo planes | Apoyar la planificación, fortalecer la confianza |
| Acción | Implementando activamente el cambio | Afirmar, trabajar a través de los obstáculos |
| Mantenimiento | Estabilizando el cambio | Prevención de recaídas, reconocer los éxitos |
| Recaída | Retorno al comportamiento anterior | Normalizar, volver a motivar, aprender de la experiencia |

**Importante:** La recaída no es un fracaso, sino parte del proceso de cambio.

### Reconocer la Etapa

**Preguntas guía:**
- "¿Ha pensado en cambiar algo?" (Precontemplation vs. Contemplation)
- "¿Qué habla a favor y qué en contra?" (Exploración de la ambivalencia)
- "¿Tiene ideas concretas sobre cómo lo abordaría?" (Preparation)
- "¿Qué ha intentado ya?" (Experiencia de acción)

---

## 4. Reconocer y Fortalecer el Discurso de Cambio

### ¿Qué es el Discurso de Cambio (Change Talk)?

El discurso de cambio consiste en declaraciones de la persona que se orientan hacia el cambio. La EM busca incrementar el discurso de cambio y no reforzar el discurso de mantenimiento (sostenimiento del statu quo).

### Marco DARN-CAT

**Discurso de cambio preparatorio (DARN):**
- **D**eseo (Desire): "Me gustaría..."
- **A**ptitud / Capacidad (Ability): "Podría..."
- **R**azones (Reasons): "Sería mejor porque..."
- **N**ecesidad (Need): "Necesito cambiar algo..."

**Discurso de cambio movilizador (CAT):**
- **C**ompromiso (Commitment): "Lo haré..."
- **A**ctivación (Activation): "Estoy listo/a para..."
- **T**omar pasos (Taking Steps): "Ya he..."

### Fomentar el Discurso de Cambio

**Estrategias:**
1. **Hacer preguntas abiertas:**
   - "¿Qué ganaría si algo cambiara?"
   - "¿Qué le da confianza de que podría lograrlo?"

2. **Escala de importancia y confianza:**
   - "¿Qué tan importante es este cambio para usted en una escala del 0 al 10?"
   - "¿Qué tan confiado/a está de poder manejarlo?"
   - "¿Por qué un 5 y no un 2?" (fortalece la motivación existente)

3. **Explorar extremos:**
   - "¿Qué podría pasar en el peor de los casos si nada cambia?"
   - "¿Qué sería lo mejor que podría pasar si lo cambiara?"

4. **Mirar hacia atrás y mirar hacia adelante:**
   - "¿Cómo eran las cosas antes de que surgiera este problema?"
   - "¿Dónde se ve dentro de cinco años si todo sigue igual?"

---

## 5. Manejo de la Resistencia

### La Resistencia como Señal

En la EM, la "resistencia" se interpreta como una señal de que el asesor va demasiado rápido o no respeta adecuadamente la autonomía de la persona.

### Estrategias

| Situación | Respuesta |
|-----------|-----------|
| "No tengo ningún problema" | Aceptar, no discutir, mostrar curiosidad |
| "Usted no me entiende" | Reflejar: "Ser comprendido/a es importante para usted" |
| "Eso no funcionará de todos modos" | Explorar éxitos pasados, fortalecer la confianza |
| La persona se enoja | Desacelerar, enfatizar la autonomía, reflejar con empatía |

**Regla de oro:** Nunca discutir contra la resistencia. Fluya con la resistencia (rodar con la resistencia), no empuje contra ella.

---

## Ética y Límites

**Un asistente de IA PUEDE:**
- Utilizar técnicas OARS para fomentar la reflexión
- Reconocer y reflejar el discurso de cambio
- Proporcionar información sobre los procesos de cambio
- Explorar respetuosamente la ambivalencia

**Un asistente de IA NO DEBE:**
- Forzar o manipular el cambio
- Tomar decisiones por la persona
- Realizar terapia de adicciones o apoyo para el abandono/abstinencia
- Utilizar amenazas o apelaciones al miedo
- Socavar la autonomía de la persona

**Principio fundamental:** La persona decide. Un asistente de IA apoya el proceso de reflexión.

**En caso de crisis aguda, SIEMPRE derivar a:**
- 988 Suicide & Crisis Lifeline (EE. UU.): 988
- Crisis Text Line (EE. UU.): Envía HOME al 741741
- Samaritans (Reino Unido): 116 123
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

*Adaptado de BACH v3.8.0 | Versión independiente*
*Fuentes: Miller & Rollnick (2013), Prochaska & DiClemente (1983), Lundahl et al. (2010) — No es terapia profesional*
