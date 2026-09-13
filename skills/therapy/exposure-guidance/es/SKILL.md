---
name: exposure-guidance
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Exposición graduada para trastornos de ansiedad: Jerarquía de miedo, escala SUDs, planificación y orientación de la exposición. Solo psicoeducación, no ejecución.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [exposure, anxiety, phobia, suds, graded, behavioral-therapy]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/exposition_begleitung.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="exposure-guidance banner">

> **Español** — Versión oficial en español de `exposure-guidance`.


# Exposure Guidance (Español)

> Jerarquía de miedo, escala SUDs, exposición graduada y habituación: Planificación y orientación — la exposición real solo con un terapeuta

See: [ETHICS.md](../ETHICS.md)

---

## Contexto

La exposición (terapia de confrontación) es uno de los métodos más eficaces en la terapia cognitivo-conductual (TCC) para trastornos de ansiedad, fobias, trastorno obsesivo-compulsivo (TOC) y TEPT. Se basa en los principios de habituación y extinción: al enfrentarse repetidamente a una situación desencadenante de ansiedad, la respuesta de ansiedad disminuye con el tiempo.

Evidencia: La terapia de exposición es el tratamiento estándar de oro para fobias específicas, ansiedad social, trastorno de pánico y agorafobia (Guías NICE, Bandelow et al. 2014, Guía S3 de Trastornos de Ansiedad). Los tamaños del efecto se encuentran entre los más altos en la investigación psicoterapéutica.

**IMPORTANTE:** Esta habilidad apoya la PLANIFICACIÓN de ejercicios de exposición y transmite la comprensión de los mecanismos. La EJECUCIÓN de la exposición debe realizarse bajo la guía de un terapeuta cualificado.
**Nunca aplicar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. Comprensión de los mecanismos

### Habituación

```
HABITUACIÓN: Adaptación mediante confrontación repetida

Nivel de ansiedad
100 |  *
    | * *
 80 |*   *
    |     *
 60 |      *
    |       *
 40 |        *
    |         *  *
 20 |          **  * *
    |                  * * * * * *
  0 |________________________________
    Tiempo (durante la exposición)

La ansiedad aumenta inicialmente, alcanza un pico
y luego disminuye por sí sola SIN huida ni evitación.

Experiencia clave: "La ansiedad pasa, incluso cuando
permanezco en la situación."
```

### Extinción (Nuevo aprendizaje)

```
EXTINCIÓN: Las nuevas experiencias sobrescriben las viejas asociaciones de miedo

Experiencia previa: Perro -> Peligro -> Miedo -> Huida
Nueva experiencia: Perro -> Sin peligro -> El miedo disminuye -> Estoy a salvo

La asociación previa no se borra, sino que se superpone con nuevas
experiencias. Por lo tanto, el miedo puede regresar en ciertos
contextos (renovación, restablecimiento), lo cual es NORMAL.
```

### Por qué la evitación mantiene el problema

```
EL CÍRCULO VICIOSO DE LA EVITACIÓN:

Situación desencadenante de ansiedad
        |
        v
La ansiedad aumenta (desagradable)
        |
        v
Evitación / huida
        |
        v
Alivio a corto plazo (la ansiedad disminuye de inmediato)
        |
        v
Refuerzo de la ansiedad a largo plazo
("La situación SÍ es peligrosa, menos mal que hui")
        |
        v
La próxima vez: Aún más ansiedad, aún más evitación
```

---

## 2. La escala SUDs

### Unidades Subjetivas de Malestar (0-100)

```
ESCALA SUDs (Unidades Subjetivas de Malestar / Subjective Units of Distress)

  0  Completamente relajado, sin ansiedad
 10  Tensión mínima, apenas perceptible
 20  Leve malestar, fácilmente tolerable
 30  Perceptiblemente desagradable, pero controlable
 40  Ansiedad notable, aún capaz de funcionar
 50  Ansiedad moderada, exigente pero manejable
 60  Ansiedad fuerte, claro impulso de evitar
 70  Ansiedad muy fuerte, difícil de soportar
 80  Ansiedad intensa, al límite de la tolerancia
 90  Ansiedad extrema, sensación de pánico
100  Ansiedad máxima, el peor malestar imaginable
```

### Uso de la escala SUDs

**Antes de la exposición:**
- Ansiedad estimada en la situación planificada (valor esperado)

**Durante la exposición:**
- Evaluar el valor de SUDs actual cada 5 minutos
- Documentar la evolución (ascendente, descendente, fluctuante)

**Después de la exposición:**
- ¿Valor de SUDs más alto? ¿Valor final? ¿Qué tan rápido disminuyó la ansiedad?
- ¿Fue tan malo como se esperaba?

---

## 3. Creación de una jerarquía de miedo

### Principio

Una jerarquía de miedo clasifica las situaciones desencadenantes de ansiedad de menor a mayor nivel de malestar. La exposición comienza con situaciones sencillas y aumenta paso a paso.

### Ejemplo: Fobia a los perros

```
JERARQUÍA DE MIEDO: Fobia a los perros

SUDs | Situación
-----|--------------------------------------------------
 10  | Mirar la foto de un perro
 15  | Ver un video de perros jugando
 25  | Hablar sobre experiencias propias con perros
 30  | Observar a un perro pequeño desde 10 metros de distancia
 40  | Observar a un perro pequeño desde 5 metros de distancia
 50  | Estar junto a un perro pequeño con correa (2 metros)
 55  | Tocar a un perro pequeño con correa (sujetado por su dueño)
 60  | Observar a un perro mediano desde 5 metros
 65  | Sentarse junto a un perro mediano con correa
 70  | Acariciar a un perro mediano
 75  | Pasar caminando cerca de un perro sin correa (en un parque)
 80  | Estar a solas en una habitación con un perro tranquilo
 85  | Acariciar a un perro grande
 90  | Estar en un parque con varios perros sin correa
 95  | Darle de comer a un perro
100  | Dejar que un perro desconocido corra hacia uno
```

### Plantilla para completar

```
MI JERARQUÍA DE MIEDO

Tema de ansiedad: [...]

SUDs | Situación
-----|--------------------------------------------------
     | [...]
     | [...]
     | [...]
     | [...]
     | [...]
```

---

## 4. Tipos de exposición

### Exposición graduada (In Vivo)

**Principio:** Confrontación paso a paso con situaciones reales, comenzando en valores bajos de SUDs.

### Inundación (Flooding)

**Principio:** Confrontación directa con situaciones altamente generadoras de ansiedad durante períodos prolongados. Únicamente bajo supervisión terapéutica. NO debe ser guiada por un asistente de IA (solo explicada).

### Exposición In Sensu (Imaginaria)

**Principio:** Experimentar situaciones desencadenantes de ansiedad en la imaginación. Útil como preparación para la exposición real.

### Exposición interoceptiva

**Principio:** Inducir deliberadamente síntomas físicos de ansiedad (p. ej., taquicardia mediante ejercicio, mareo mediante giros). ÚNICAMENTE bajo supervisión terapéutica.

---

## 5. Planificación guiada de la exposición

### Protocolo de preparación

```
PROTOCOLO DE PLANIFICACIÓN DE LA EXPOSICIÓN

Fecha: [...]
Terapeuta informado: [ ] Sí  [ ] No (¡OBLIGATORIO!)

Tema de ansiedad: [...]
Situación elegida: [...]
Valor de SUDs esperado: [...]
Nivel en la jerarquía: [...]

¿Qué haré exactamente?: [...]
Dónde: [...]
Cuándo: [...]
Durante cuánto tiempo: [...]
Solo o acompañado: [...]

Mi mayor temor: [...]
Qué sucederá en la realidad: [...]

Plan de emergencia (si SUDs > 90 o disociación):
1. Anclaje / Grounding (técnica 5-4-3-2-1)
2. Ejercicio de respiración (respiración cuadrada / box breathing)
3. [Llamar a persona de confianza]: Tel. [...]
4. Abandonar la situación de forma ordenada (sin huida presa del pánico)
```

### Protocolo posterior a la sesión (Debriefing)

```
EVALUACIÓN POST-EXPOSICIÓN (DEBRIEFING)

Fecha: [...]
Situación: [...]

SUDs previo (expectativa): [...]
SUDs valor más alto durante: [...]
SUDs al finalizar: [...]

Tiempo que permanecí en la situación: [...]
¿Ocurrió habituación?: [ ] Sí  [ ] Parcial  [ ] No

Lo que aprendí: [...]
¿Fue tan malo como temía?: [ ] Peor  [ ] Como esperaba  [ ] Menos malo

Lo que quiero hacer diferente la próxima vez: [...]
Siguiente nivel: [...]
```

---

## 6. Notas de seguridad y criterios de interrupción

### Requisitos previos para la exposición

```
LISTA DE COMPROBACIÓN ANTES DE INICIAR LA EXPOSICIÓN:

[ ] Hay un terapeuta cualificado involucrado
[ ] Existe una estabilización previa suficiente
[ ] La jerarquía de miedo está creada y discutida
[ ] El plan de emergencia está preparado
[ ] La persona comprende el mecanismo (habituación)
[ ] Ausencia de suicidalidad aguda
[ ] Sin síntomas psicóticos no controlados
[ ] Sin trastorno disociativo grave (sin acompañamiento terapéutico)
[ ] Sin intoxicación aguda por sustancias
[ ] La persona ha dado su consentimiento voluntario (¡sin exposición forzada!)
```

### Criterios de interrupción

```
INTERRUMPIR LA EXPOSICIÓN SI:

- Ocurre disociación (la persona está "ausente", no responde)
- Ataque de pánico con pérdida de control
- La persona desea explícitamente parar (¡respetar la autonomía!)
- Síntomas físicos: dolor en el pecho, dificultad respiratoria, desmayo
- Pensamientos suicidas durante la exposición
- La situación se vuelve objetivamente insegura

EN CASO DE INTERRUPCIÓN:
1. Anclaje / Grounding y estabilización (5-4-3-2-1, ejercicio de respiración)
2. Asegurar que la persona esté orientada y estable
3. Analizar la experiencia (qué sucedió, qué se aprendió)
4. Ningún reproche ("Deberías haberte quedado")
5. Planificar el siguiente paso con el terapeuta
```

---

## Ética y límites

**Un asistente de IA PUEDE:**
- Explicar los principios de la exposición (psicoeducación)
- Elaborar jerarquías de miedo conjuntamente
- Explicar y utilizar la escala SUDs
- Apoyar la planificación de la exposición (cumplimentar protocolos)
- Documentar la evaluación posterior (debriefing)
- Proporcionar información de seguridad
- Motivar y normalizar ("La ansiedad durante la exposición es esperada y normal")

**Un asistente de IA NO DEBE:**
- Guiar o llevar a cabo la exposición de forma independiente
- Guiar la inundación / flooding (SOLO el terapeuta)
- Guiar la exposición interoceptiva (SOLO el terapeuta)
- Realizar exposición prolongada para el TEPT
- Acompañar la exposición en casos de disociación grave
- Presionar para realizar la exposición ("Tienes que enfrentarlo")
- Garantizar resultados
- Realizar diagnósticos o elaborar planes de tratamiento
- Hacer recomendaciones relacionadas con medicación

**LÍMITE ESPECIALMENTE ESTRICTO:** El asistente de IA planifica y explica. La exposición real se lleva a cabo bajo la guía de un terapeuta cualificado. Ante cualquier solicitud de ejecución: derivar a un profesional. La exposición sin apoyo profesional puede intensificar la ansiedad y re-traumatizar.

**En caso de crisis aguda, derivar SIEMPRE a:**
- 988 Suicide & Crisis Lifeline (EE. UU.): 988
- Crisis Text Line (EE. UU.): Envía HOME al 741741
- Samaritans (Reino Unido): 116 123
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

*Adaptado de BACH v3.8.0 | Versión independiente*
*Fuentes: Foa & Kozak (1986), Craske et al. (2014), Bandelow et al. (2014), Guía S3 de Trastornos de Ansiedad (2014) — No es terapia profesional*
