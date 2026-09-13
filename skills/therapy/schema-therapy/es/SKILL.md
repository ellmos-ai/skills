---
name: schema-therapy
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Terapia de Esquemas según Jeffrey Young: Esquemas, modos, concepto del niño interior y estilos de afrontamiento — presentado psicoeducativamente.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [schema-therapy, modes, inner-child, coping-styles, personality]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/schematherapie.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="schema-therapy banner">

> **Español** — Versión oficial en español de `schema-therapy`.


# Schema Therapy (Español)

> Fundamentos de la Terapia de Esquemas según Jeffrey Young: Esquemas, modos, concepto del niño interior y estilos de afrontamiento — presentado psicoeducativamente

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

La Terapia de Esquemas fue desarrollada por Jeffrey E. Young a partir de la década de 1990 como una extensión de la terapia cognitivo-conductual. Integra elementos de la TCC, la teoría del apego, la terapia Gestalt y enfoques psicodinámicos.

Evidencia: La Terapia de Esquemas cuenta con un sólido respaldo empírico, particularmente para los trastornos de la personalidad (Giesen-Bloo et al. 2006, Masley et al. 2012). En Alemania, está reconocida como un método dentro de la terapia de conducta.

**Nota:** Esto es psicoeducación, no un sustituto de la terapia profesional.
**Nunca implementar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. Esquemas Inadaptados Tempranos

### Principio
Los esquemas son patrones emocionales y cognitivos profundamente arraigados que se desarrollan en la infancia a través de necesidades núcleo no satisfechas. Influyen en cómo percibimos el mundo, a nosotros mismos y a los demás.

### Las Cinco Necesidades Núcleo (según Young)

| Necesidad Núcleo | Al no satisfacerse, puede derivar en |
|------------------|---------------------------------------|
| Apego seguro | Abandono, desconfianza |
| Autonomía y competencia | Dependencia, miedo al fracaso |
| Límites realistas | Derecho / Grandiosidad, insuficiente autocontrol |
| Libertad para expresar necesidades | Subyugación, autosacrificio |
| Espontaneidad y juego | Normas inalcanzables, carácter punitivo |

### Los 18 Esquemas — Visión General (5 Dominios)

**Dominio 1: Desconexión y Rechazo**
- Abandono / Inestabilidad
- Desconfianza / Abuso
- Privación Emocional
- Imperfección / Vergüenza
- Aislamiento Social

**Dominio 2: Autonomía y Desempeño Deteriorados**
- Dependencia / Incompetencia
- Vulnerabilidad al Daño
- Apego Excesivo / Autoconcepto No Desarrollado
- Fracaso

**Dominio 3: Límites Deteriorados**
- Derecho / Grandiosidad
- Insuficiente Autocontrol

**Dominio 4: Orientación hacia los Demás**
- Subyugación
- Autosacrificio
- Búsqueda de Aprobación

**Dominio 5: Hipervigilancia e Inhibición**
- Negativismo / Pesimismo
- Inhibición Emocional
- Normas Inalcanzables
- Castigo / Carácter Punitivo

### Preguntas de Reflexión para Reconocer Esquemas
- "¿Qué creencias sobre ti mismo vuelven a surgir una y otra vez?"
- "¿En qué situaciones reaccionas de manera especialmente intensa a nivel emocional?"
- "¿Notas patrones que se repiten a lo largo de diferentes relaciones?"
- "¿Qué necesidades pudieron no haberse satisfecho suficientemente en tu infancia?"

---

## 2. El Modelo de Modos

### Principio
Los modos son estados emocionales momentáneos activados por los esquemas. El modelo de modos ayuda a comprender y categorizar diferentes "partes internas".

### Las Cuatro Categorías de Modos

**Modos Niño:**
- *Niño Vulnerable:* Se siente triste, solo, ansioso, abrumado
- *Niño Airado:* Con rabia por necesidades no satisfechas
- *Niño Impulsivo:* Actúa sin pensar, busca gratificación inmediata
- *Niño Feliz:* Se siente seguro, amado, espontáneo

**Modos Padre Inadaptado:**
- *Padre Punitivo:* Voz interior que critica, castiga, desvaloriza
- *Padre Exigente:* Voz interior que exige perfección y rendimiento

**Modos de Afrontamiento Inadaptados:**
- *Rendido Complaciente:* Cede, se adapta en exceso
- *Protector Distanciado:* Adormece emociones, se retira, se distrae
- *Sobrecompensador:* Domina, controla, ataca

**Adulto Sano:**
- Puede percibir necesidades y satisfacerlas adecuadamente
- Establece límites saludables
- Consuela y calma al niño vulnerable
- Limita los modos padre excesivos

### Ejercicio: Reconocer Modos en la Vida Cotidiana

```
Situación: ______________
¿Qué modo estoy sintiendo en este momento?
  [ ] Niño Vulnerable — "Me siento pequeño e indefenso"
  [ ] Niño Airado — "¡Eso no es justo!"
  [ ] Padre Punitivo — "No eres lo suficientemente bueno"
  [ ] Padre Exigente — "Debes hacer más"
  [ ] Protector Distanciado — "No quiero pensar en esto"
  [ ] Sobrecompensador — "Ya les enseñaré"
  [ ] Adulto Sano — "¿Qué necesito realmente en este momento?"
```

---

## 3. Trabajo con el Niño Interior (Psicoeducativo)

### Principio
El trabajo con el niño interior en Terapia de Esquemas busca desarrollar una actitud interna de cuidado hacia las propias partes vulnerables.

**ATENCIÓN:** El trabajo profundo con el niño interior corresponde a la supervisión terapéutica profesional.

### Ejercicio de Reflexión: Carta al Niño Interior

```
Escribe una breve carta a tu yo más joven:
1. ¿Qué habrías necesitado en aquel momento?
2. ¿Qué le dirías a ese niño hoy?
3. ¿Qué consuelo le ofrecerías?
```

### Preguntas de Reflexión
- "Cuando piensas en esa situación, ¿cuántos años sientes que tienes por dentro?"
- "¿Qué te habría dicho un adulto afectuoso en aquel momento?"
- "¿Qué necesidades de tu niño interior no están siendo satisfechas actualmente?"

---

## 4. Comprensión de los Estilos de Afrontamiento

### Los Tres Patrones Básicos

| Estilo de Afrontamiento | Estrategia | Ejemplo |
|-------------------------|------------|---------|
| Sumisión / Rendición | Aceptar el esquema, someterse | "Así soy yo, no puedo cambiarlo" |
| Evitación | No querer sentir el esquema | Distracción, consumo de sustancias, exceso de trabajo |
| Sobrecompensación | Vivir lo opuesto al esquema | Perfeccionismo en lugar de sentirse como un fracaso |

### Preguntas de Reflexión
- "Cuando estás bajo presión, ¿tiendes a someterte, huir o luchar?"
- "¿Cuáles de tus hábitos podrían ser estrategias de evitación?"
- "¿Hay áreas en las que haces lo contrario de lo que realmente sientes?"

---

## Ética y Límites

**Un asistente de IA puede:**
- Explicar esquemas y modos como conceptos
- Formular preguntas de reflexión para la autoexploración
- Presentar estilos de afrontamiento como psicoeducación
- Guiar ejercicios sencillos y escritos de reflexión sobre el niño interior

**Un asistente de IA NO debe:**
- Diagnosticar o atribuir esquemas
- Realizar trabajo de sillas ni ejercicios vivenciales/experienciales
- Ofrecer reparentalización (reparenting limitado)
- Procesar experiencias traumáticas de la infancia
- Sustituir la terapia de modos de esquema

**En caso de crisis aguda, SIEMPRE derivar a:**
- Teléfono de la Esperanza (ES): 717 003 717 / Línea 024 de atención a la conducta suicida
- Línea de Crisis y Prevención del Suicidio (US en español): 988
- Samaritans (UK): 116 123
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

## Referencias

- Young, J. E., Klosko, J. S. & Weishaar, M. E. (2003). *Schema Therapy: A Practitioner's Guide.* Guilford Press.
- Giesen-Bloo, J. et al. (2006). Outpatient Psychotherapy for Borderline Personality Disorder. *Archives of General Psychiatry*, 63(6), 649-658.
- Roediger, E. (2011). *Praxis der Schematherapie.* Schattauer.

---

*Portado de BACH v3.8.0 | Versión independiente*
*Fuentes: Young et al. (2003), Giesen-Bloo et al. (2006), Roediger (2011) — No es terapia profesional*
