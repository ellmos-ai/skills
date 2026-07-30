---
name: pmr-autogenic-training
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Relajación Muscular Progresiva (PMR) según Jacobson y Entrenamiento Autógeno según Schultz. Formas cortas y versiones completas.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [pmr, autogenic-training, relaxation, jacobson, schultz, muscle-relaxation]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/pmr_autogenes_training.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `pmr-autogenic-training`.


# Relajación Muscular Progresiva y Entrenamiento Autógeno

> Técnicas de relajación de base corporal según Jacobson y Schultz

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

La Relajación Muscular Progresiva (PMR, Jacobson 1929) y el Entrenamiento Autógeno (AT, Schultz 1932) son las dos técnicas de relajación más investigadas científicamente. Ambas actúan mediante la influencia consciente en el sistema nervioso autónomo y pueden aprenderse como métodos de autoayuda sin supervisión terapéutica.

**Nota:** Esto es un soporte y no sustituye a la terapia profesional.
**Nunca implementar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET)

---

## 1. Relajación Muscular Progresiva (PMR) según Jacobson

### Principio Básico

Tensión y liberación sistemáticas de grupos musculares. A través del contraste entre la tensión y la relajación, el cuerpo aprende una relajación más profunda que la posible en su estado habitual.

**Mecanismo:** Tensión muscular -> liberación consciente -> activación parasimpática -> reducción de la frecuencia cardíaca, presión arterial y tono muscular

### 1.1 Forma Larga: 16 Grupos Musculares

| N.º | Grupo Muscular | Tensión |
|----|-------------|---------|
| 1 | Mano/antebrazo derecho | Apretar el puño |
| 2 | Brazo derecho | Tensar el bíceps |
| 3 | Mano/antebrazo izquierdo | Apretar el puño |
| 4 | Brazo izquierdo | Tensar el bíceps |
| 5 | Frente | Levantar las cejas |
| 6 | Zona media del rostro | Cerrar los ojos con fuerza, arrugar la nariz |
| 7 | Zona inferior del rostro | Apretar los dientes, estirar las comisuras de los labios |
| 8 | Cuello | Presionar la barbilla contra el pecho (contrapresión) |
| 9 | Pecho/hombros | Elevar los hombros, inspirar profundamente |
| 10 | Abdomen | Tensar la musculatura abdominal |
| 11 | Zona lumbar | Arquear ligeramente la espalda |
| 12 | Muslo derecho | Levantar ligeramente la pierna |
| 13 | Pantorrilla derecha | Tirar del pie hacia la espinilla |
| 14 | Pie derecho | Doblar los dedos del pie hacia abajo |
| 15 | Muslo izquierdo | Levantar ligeramente la pierna |
| 16 | Pantorrilla/pie izquierdo | Tirar del pie hacia arriba, doblar los dedos |

**Procedimiento por grupo muscular:**
1. Dirigir la atención al grupo muscular
2. Tensar: 5-7 segundos (aproximadamente el 70% de la fuerza máxima)
3. Soltar: Relajar de forma abrupta
4. Observar: 20-30 segundos, percibir la relajación
5. Siguiente grupo muscular

### 1.2 Forma Corta: 7 Grupos Musculares

Para practicantes experimentados o cuando el tiempo es limitado:

| N.º | Combinación | Tensión |
|----|------------|---------|
| 1 | Ambos brazos | Apretar puños, doblar brazos |
| 2 | Rostro completo | Mueca: fruncir el ceño, cerrar ojos, abrir bien la boca |
| 3 | Cuello/hombros | Subir hombros hacia las orejas |
| 4 | Pecho/abdomen | Inhalar, tensar el abdomen |
| 5 | Espalda | Juntar escápulas, arco ligero |
| 6 | Ambos muslos | Levantar ligeramente las piernas |
| 7 | Ambas pantorrillas/pies | Tirar de los pies hacia arriba |

### 1.3 Técnica de Evocación / Recuerdo (Avanzado)

Tras varias semanas de práctica: Relajación de los grupos musculares ÚNICAMENTE mediante la imaginación (sin tensión física real). El cuerpo ha acondicionado la respuesta de relajación.

---

## 2. Entrenamiento Autógeno (AT) según Schultz

### Principio Básico

Autorrelajación concentrativa mediante autosugestión formularia. El practicante induce un estado de relajación profunda a través de frases guía repetidas (conmutación autonómica).

**Mecanismo:** Concentración en fórmulas -> respuesta ideomotora -> cambios físicos reales (flujo sanguíneo, calor, calma)

### 2.1 Los 6 Ejercicios Básicos (Grado Inferior)

| Ejercicio | Fórmula | Objetivo |
|----------|---------|------|
| 1. Pesadez | "Mi brazo derecho es muy pesado" | Relajación muscular |
| 2. Calor | "Mi brazo derecho está muy caliente" | Vasodilatación, flujo sanguíneo |
| 3. Corazón | "Mi corazón late de forma tranquila y constante" | Regulación cardíaca |
| 4. Respiración | "Mi respiración es tranquila y constante" | Regulación respiratoria |
| 5. Plexo solar | "Mi plexo solar irradia calor" | Relajación de órganos abdominales |
| 6. Frente | "Mi frente está agradablemente fresca" | Claridad mental |

**Progresión:** Gradual a lo largo de 6-8 semanas. Añadir un nuevo ejercicio cada semana.

### 2.2 Procedimiento de la Sesión

```
1. Postura básica: Postura del cochero, posición en sillón o acostado
2. Apertura: Cerrar los ojos, "Estoy completamente tranquilo/a"
3. Repetir mentalmente las fórmulas (6 veces cada una, lentamente):
   - "Mi brazo derecho es muy pesado" (6x)
   - "Mi brazo derecho está muy caliente" (6x)
   - [fórmulas adicionales según el nivel de práctica]
4. Fórmula de descanso intermedia: "Estoy completamente tranquilo/a"
5. Retorno / Cancelación (Recall): Tensar fuertemente los brazos, respirar hondo, abrir los ojos
   IMPORTANTE: Nunca omitir el retorno (excepto antes de dormirse)
```

### 2.3 Plan de Aprendizaje

| Semana | Ejercicio | Duración |
|------|----------|----------|
| 1-2 | Ejercicio de pesadez | 5 min |
| 3-4 | Pesadez + Calor | 8 min |
| 5-6 | Pesadez + Calor + Corazón + Respiración | 12 min |
| 7-8 | Los 6 ejercicios básicos | 15 min |

---

## 3. PMR vs. AT: Guía de Decisión

| Criterio | PMR | AT |
|-----------|-----|-----|
| Aprendizaje | Fácil, de eficacia inmediata | Requiere práctica (4-8 semanas) |
| Actividad física | Sí (tensión) | No (solo imaginación) |
| Para tensión muscular | Muy adecuado | Moderadamente adecuado |
| Para inquietud interior | Bueno | Muy bueno |
| Para problemas de sueño | Bueno | Muy bueno |
| Utilizable en cualquier lugar | Limitado (requiere movimiento) | Sí (discreto) |
| Para niños | Desde aprox. los 8 años | Desde aprox. los 10 años |

---

## 4. Contraindicaciones

**PMR:**
- Lesiones musculares agudas o inflamación
- Espasticidad grave
- Epilepsia (la tensión puede desencadenar crisis, poco frecuente)

**AT:**
- Psicosis aguda
- Depresión grave (riesgo de introspección excesiva)
- Arritmia cardíaca (omitir el ejercicio del corazón)
- Trastornos disociativos
- Hipotensión grave (posibles problemas circulatorios)

**Ambos métodos:**
- Interrumpir inmediatamente si se producen flashbacks traumáticos
- No sustituye al tratamiento médico o psicoterapéutico

---

## Seguimiento del Progreso

- Nivel de tensión antes/después del ejercicio (escala 0-10)
- ¿Qué grupos musculares estaban especialmente tensos?
- AT: ¿Qué fórmulas son ya efectivas y cuáles aún no?
- Regularidad: Objetivo 1 vez al día, al menos 4 veces por semana

**En caso de crisis aguda, acudir SIEMPRE a:**
- 988 Línea de Crisis y Suicidio (EE. UU.): 988
- Crisis Text Line (EE. UU.): Enviar HOME al 741741
- Samaritans (Reino Unido): 116 123
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE / España)

---

*Portado de BACH v3.8.0 | Versión Independiente*
*Fuentes: Jacobson (1929), Schultz (1932) — No es terapia profesional*
