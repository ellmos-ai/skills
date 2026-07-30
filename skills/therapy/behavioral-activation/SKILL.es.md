---
name: behavioral-activation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Activación conductual para la depresión: romper el círculo vicioso, registro de actividades, planificación semanal y actividades basadas en valores.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [behavioral-activation, depression, activity, weekly-plan, values]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/verhaltensaktivierung.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `behavioral-activation`.


# Activación Conductual (Español)

> Planificación de actividades, diario de estado de ánimo y actividad, y selección de actividades basadas en valores: contrarrestrar el círculo vicioso de la inactividad y el bajo estado de ánimo

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

La Activación Conductual (AC) es una intervención basada en evidencia de la terapia de conducta para el tratamiento de la depresión. Se basa en la premisa de que la depresión conduce al aislamiento y la inactividad, lo que empeora aún más el estado de ánimo (círculo vicioso). Mediante la construcción programada de actividades positivas, se rompe este ciclo.

Evidencia: La activación conductual es eficaz como terapia independiente y es equivalente a la terapia cognitiva (Dimidjian et al. 2006, estudio COBRA de Richards et al. 2016). Recomendada como intervención de primera línea para la depresión leve a moderada (Guías NICE).

**Nota:** Esto es un apoyo, no un sustituto de la terapia profesional.
Para la depresión grave o ideas suicidas, recomiende SIEMPRE ayuda profesional.
**Nunca aplicar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. El Modelo de Activación Conductual para la Depresión

### El Círculo Vicioso

```
Situación desencadenante (pérdida, estrés, cambio)
        |
        v
Bajo estado de ánimo, falta de energía
        |
        v
Aislamiento, evitación, inactividad
        |
        v
Menos experiencias positivas, aislamiento social
        |
        v
Estado de ánimo aún más bajo
        |
        v
Aún más aislamiento... (espiral descendente)
```

### El Contra-Principio

```
Actividad dirigida (incluso con baja motivación)
        |
        v
Experiencia positiva / sensación de logro / conexión
        |
        v
Leve mejora del estado de ánimo
        |
        v
Algo más de energía y motivación
        |
        v
Más actividades... (espiral ascendente)
```

**Principio fundamental:** No espere a que llegue la motivación: la acción crea la motivación.
"Actúe primero, sienta después." (No: "Sienta primero, luego actúe.")

---

## 2. Diario de Estado de Ánimo y Actividad

### Objetivo
Hacer visibles las conexiones entre las actividades y el estado de ánimo. Reconocer qué actividades mejoran el estado de ánimo y cuáles lo empeoran.

### Formato del Diario

```
DIARIO DE ESTADO DE ÁNIMO Y ACTIVIDAD

Fecha: [...]

| Hora  | Actividad | Estado de ánimo (0-10) | Disfrute (0-10) | Importancia (0-10) |
|-------|-----------|------------------------|-----------------|--------------------|
| 07:00 | Levantarse, desayunar | 3 | 2 | 5 |
| 08:00 | Trabajo: correos electrónicos | 4 | 1 | 6 |
| 10:00 | Paseo | 6 | 5 | 4 |
| 12:00 | Almuerzo con un compañero | 7 | 6 | 7 |
| 14:00 | Trabajo: proyecto | 5 | 3 | 7 |
| 18:00 | Ver la televisión (solo) | 3 | 2 | 1 |
| 20:00 | Llamada telefónica con un amigo | 6 | 5 | 8 |

Promedio diario del estado de ánimo: [...]
Mejor actividad de hoy: [...]
Reflexión/Aprendizaje: [...]
```

### Revisión Semanal

**Preguntas guía:**
- ¿Qué actividades elevan regularmente mi estado de ánimo?
- ¿Qué actividades bajan mi estado de ánimo?
- ¿Hay momentos del día que sean particularmente difíciles?
- ¿Cuánto tiempo dedico a actividades agradables frente a desagradables?
- ¿Qué actividades he estado evitando?

---

## 3. Planificación de Actividades

### Paso 1: Crear lista de actividades

Reunir tres categorías de actividades:

**A) Actividades Agradables (placer, disfrute)**
- Naturaleza: Pasear, parque, bosque
- Social: Reunirse con amigos, llamadas, cocinar juntos
- Creativo: Música, pintura, escritura, manualidades
- Físico: Deporte, yoga, baile, natación
- Disfrute: Cocinar la comida favorita, leer un libro, escuchar música
- Relajación: Tomar un baño, meditación, ejercicios de respiración

**B) Actividades Necesarias (estructura, autocuidado)**
- Hogar: Limpiar, cocinar, hacer compras
- Cuidado personal: Ducharse, vestirse, lavarse los dientes
- Administración: Facturas, citas, papeleo
- Salud: Citas médicas, medicación, nutrición

**C) Actividades Basadas en Valores (sentido, significado)**
- Ver la sección 4 a continuación

### Paso 2: Crear el plan semanal

```
PLAN SEMANAL

| Día | Mañana | Mediodía | Tarde | Noche |
|-----|--------|----------|-------|-------|
| Lun | [...]  | [...]    | [...] | [...] |
| Mar | [...]  | [...]    | [...] | [...] |
| Mié | [...]  | [...]    | [...] | [...] |
| Jue | [...]  | [...]    | [...] | [...] |
| Vie | [...]  | [...]    | [...] | [...] |
| Sáb | [...]  | [...]    | [...] | [...] |
| Dom | [...]  | [...]    | [...] | [...] |
```

### Reglas de Planificación
1. **Comience poco a poco:** No planifique todo el día, sino 1-2 actividades por día
2. **Mezcle:** Agradables + necesarias + basadas en valores
3. **Específico:** "Martes 3:00 PM paseo en el parque" en lugar de "Moverme más"
4. **Realista:** Alcanzable incluso con poca energía
5. **Flexible:** El plan es una guía, no una obligación
6. **Gradual:** Para energía muy baja: mini-pasos (5 minutos es suficiente)

### Manejo de Obstáculos

| Obstáculo | Estrategia |
|-----------|------------|
| "No tengo energía" | Reducir la actividad a 5 minutos |
| "No tengo ganas" | Recordatorio: la motivación llega a través de la acción |
| "De nada servirá" | Experimento: probar y medir el estado de ánimo después |
| "No puedo hacerlo solo" | Involucrar a alguien (compromiso) |
| "No tengo tiempo" | Integrar pequeñas actividades (usar escaleras, 5 min de descanso fuera) |

---

## 4. Selección de Actividades Basadas en Valores

### Principio
Las actividades que se alinean con los valores personales generan un bienestar sostenible, a diferencia del mero placer que se desvanece rápidamente.

### Dominios de Vida y Valores

```
BRÚJULA DE VALORES

Relaciones:            ¿Qué tipo de pareja/amigo/familiar quiero ser?
Trabajo/Educación:     ¿Qué es importante para mí respecto a mi trabajo?
Ocio:                  ¿Cómo quiero pasar mi tiempo libre?
Salud:                 ¿Cómo quiero tratar a mi cuerpo?
Comunidad:             ¿Qué contribución quiero hacer?
Personal:              ¿Qué tipo de persona quiero ser?
```

### Mapeo de Valores y Actividades

**Ejemplo:**

| Valor | Actividad | Frecuencia |
|-------|-----------|------------|
| Conexión | Llamar a un amigo | 2 veces por semana |
| Salud | Paseo de 20 min | Diario |
| Creatividad | Tocar la guitarra | 1 vez por semana |
| Solidaridad | Ayudar al vecino con las compras | 1 vez por semana |
| Aprendizaje | 15 min de lectura de no ficción | 3 veces por semana |

### Valores vs. Metas
- **Valor:** Una dirección hacia la que quiere moverse (ej. "ser una pareja afectuosa")
- **Meta:** Un punto final alcanzable (ej. "planificar la celebración del aniversario")
- Los valores nunca se pueden "marcar como completados": proporcionan una orientación continua

---

## 5. Medición del Progreso

### Revisión Semanal

```
REVISIÓN SEMANAL

Semana: [Fecha]
Actividades planificadas: [Número]
Actividades completadas: [Número]
Estado de ánimo promedio: [0-10]

Lo que fue bien: [...]
Lo que fue difícil: [...]
Aprendizaje de la semana: [...]
Plan para la próxima semana: [...]
```

### Seguimiento a Largo Plazo
- Observar las tendencias del estado de ánimo a lo largo de las semanas
- Reconocer la conexión entre el nivel de actividad y el estado de ánimo
- Hacer visibles los éxitos (incluso los pequeños)

---

## Ética y Límites

**Un asistente de IA puede:**
- Guiar a través del diario y la planificación de actividades
- Sugerir actividades (nunca prescribir)
- Documentar datos del estado de ánimo y reflejar patrones
- Acompañar la reflexión sobre valores
- Reconocer pequeños progresos

**Un asistente de IA NO debe:**
- Ser el único apoyo para la depresión grave
- Hacer recomendaciones sobre medicación
- Evaluar la suicidabilidad
- Realizar diagnósticos
- Garantizar que la activación conductual sea suficiente

**Importante:** Para la depresión grave (falta persistente de impulso, pensamientos suicidas, incapacidad para manejar la vida diaria), la ayuda profesional es imprescindible. La activación conductual es un complemento, no un sustituto.

**En caso de crisis aguda, SIEMPRE derivar a:**
- 988 Suicide & Crisis Lifeline (EE. UU.): 988
- Crisis Text Line (EE. UU.): Envíe HOME al 741741
- Samaritans (Reino Unido): 116 123
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

*Adaptado de BACH v3.8.0 | Versión independiente*
*Fuentes: Martell et al. (2010), Dimidjian et al. (2006), Richards et al. (2016) — No es terapia profesional*