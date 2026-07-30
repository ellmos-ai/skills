---
name: trauma-psychoeducation
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: Psicoeducación en trauma: Definición de trauma, reacciones normales, ventana de tolerancia, manejo de desencadenantes (triggers) y autocuidado.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: therapy
tags: [trauma, psychoeducation, window-of-tolerance, trigger, self-care, ptsd]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/therapie/trauma_psychoedukation.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-12', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `trauma-psychoeducation`.


# Psicoeducación en Trauma

> Conocimiento sobre el trauma, las secuelas traumáticas y la ventana de tolerancia: Comprender reacciones normales ante eventos anormales — psicoeducación pura, NO procesamiento de trauma.

Ver: [ETHICS.md](../ETHICS.md)

---

## Contexto

La psicoeducación sobre el trauma ayuda a las personas afectadas a entender y contextualizar sus reacciones. Saber que síntomas como los flashbacks, la hiperactivación o la evitación son respuestas NORMALES ante eventos ANORMALES resulta reconfortante y reduce la culpa y la vergüenza.

Evidencia: La psicoeducación es un componente reconocido de la terapia de trauma (Flatten et al. 2011, Guía de práctica clínica S3 TEPT). Como intervención aislada resulta insuficiente, pero incrementa la motivación terapéutica y alivia los síntomas.

**IMPORTANTE:** Esta habilidad transmite exclusivamente CONOCIMIENTO sobre el trauma. NO realiza procesamiento de trauma, NO explora recuerdos dolorosos ni solicita detalles del trauma.
**Nunca implementar:** EMDR, Exposición Prolongada (PE), Terapia de Exposición Narrativa (NET).

---

## 1. ¿Qué es el Trauma?

### Definición

Un trauma es un evento que supera la capacidad de afrontamiento de una persona y va acompañado de experiencias de impotencia, pérdida de control y/o temor a la muerte. No es el evento en sí lo que define el trauma, sino la vivencia subjetiva del individuo.

### Tipos de Trauma

| Tipo | Descripción | Ejemplos |
|------|-------------|----------|
| Tipo I (Trauma único) | Evento único e inesperado | Accidente, agresión física, desastre natural |
| Tipo II (Trauma complejo) | Traumatización repetida y prolongada | Abuso infantil, negligencia, guerra |
| Trauma accidental | Eventos fortuitos o impredecibles | Accidente de tráfico, incendio, accidente laboral |
| Trauma interpersonal | Causado intencionadamente por humanos | Violencia, abuso, tortura |
| Trauma secundario | Por presenciar o acompañar la vivencia | Profesiones de ayuda, familiares |

### Lo que NO es Trauma (Diferenciación)

No todo evento doloroso o estresante es un trauma en sentido clínico:
- Ruptura amorosa, pérdida de empleo, discusiones: estresantes, pero habitualmente no son traumas.
- Acoso (bullying): puede ser traumatizante (especialmente en la infancia), pero no constituye trauma automáticamente.
- La evaluación y vivencia individual determinan el impacto, no solo la categoría del evento.

---

## 2. Reacciones Normales ante Eventos Anormales

### Los Tres Patrones de Respuesta

```
HIPERACTIVACIÓN (Hyperarousal)
- Estado de alerta constante y tensión física
- Respuesta de sobresalto exagerada
- Trastornos del sueño
- Irritabilidad, explosiones de ira
- Dificultades de concentración

REEXPERIMENTACIÓN (Intrusión)
- Flashbacks (recuerdos intrusivos con vivencia de realidad)
- Pesadillas recurrentes
- Recuerdos angustiantes que emergen súbitamente
- Reacciones fisiológicas al recordar (taquicardia, sudoración)

EVITACIÓN Y EMBOTAMIENTO (Constricción)
- Evitación de lugares, personas o situaciones relacionadas
- Embotamiento emocional o insensibilidad
- Aislamiento y distanciamiento social
- Sensación de extrañamiento o alienación
- Pérdida de interés y anhedonia
```

### Mensaje Clave para las Personas Afectadas

```
"Estas reacciones son respuestas NORMALES ante eventos ANORMALES.

Tu cuerpo y tu mente están intentando protegerte.
La hipervigilancia te protege de un nuevo peligro.
Los recuerdos intentan procesar lo que ocurrió.
La evitación te protege de verte abrumado/a.

No estás 'loco/a'. No eres 'débil'.
Tu sistema nervioso está respondiendo tal y como está programado
para responder ante una amenaza extrema."
```

### Línea Temporal del Curso Clínico

```
EVOLUCIÓN TRAS UN EVENTO TRAUMÁTICO

0-4 semanas:  Reacción de Estrés Agudo (NORMAL)
              - Shock, embotamiento, inquietud
              - Alteraciones del sueño, sobresaltos
              - Flashbacks, pesadillas
              - En la mayoría de personas: Recuperación espontánea

4+ semanas:   Si los síntomas persisten: Posible TEPT
              - Se recomienda evaluación profesional
              - La intervención temprana mejora el pronóstico

Meses-Años:   Posible cronificación
              - La terapia es eficaz incluso tras mucho tiempo
              - "Nunca es tarde para buscar ayuda"
```

---

## 3. La Ventana de Tolerancia (Dan Siegel)

### El Modelo

```
            ________________________________________________
           |                                                |
           |   POR ENCIMA DE LA VENTANA: Hiperactivación     |
           |   Pánico, ira, sobreactivación, flashbacks     |
           |   Taquicardia, sudoración, temblores           |
           |   Respuesta de "Lucha o Huida"                 |
           |________________________________________________|
           |                                                |
           |   VENTANA DE TOLERANCIA                        |
           |                                                |
           |   Aquí podemos:                                |
           |   - Pensar y sentir al mismo tiempo            |
           |   - Procesar información                       |
           |   - Mantener relaciones saludables             |
           |   - Resolver problemas                         |
           |   - Aprender y crecer                          |
           |________________________________________________|
           |                                                |
           |   POR DEBAJO DE LA VENTANA: Hipoactivación     |
           |   Parálisis (freeze), embotamiento, disociación|
           |   Falta de energía, vacío, desconexión         |
           |   Reflejo de "Hacerse el muerto"               |
           |________________________________________________|
```

### ¿Qué Significa Esto?

- **Dentro de la ventana:** Podemos regular el estrés y funcionar adecuadamente.
- **Por encima de la ventana:** Exceso de activación; el cuerpo está en modo de alarma.
- **Por debajo de la ventana:** Defecto de activación; el cuerpo se apaga o desconecta.

### El Trauma y la Ventana de Tolerancia

```
ANTES del trauma:          TRAS el trauma (sin tratar):

|_______________|         |_____|
|               |         |     |  <- La ventana se ha ESTRECHADO
|    VENTANA    |         | V.  |
|    (amplia)   |         |     |
|_______________|         |_____|

Incluso estímulos pequeños pueden provocar la salida de la ventana
tras sufrir un trauma (desencadenantes o triggers).

OBJETIVO de la terapia: AMPLIAR nuevamente la ventana.
```

### Comprensión de los Desencadenantes (Triggers)

```
Los DESENCADENANTES son estímulos que recuerdan el trauma y ponen
al sistema nervioso en modo de alarma, a menudo de forma inconsciente.

Los desencadenantes pueden ser:
- Sonidos (estruendos, gritos, cierta música)
- Olores (humo, perfume, alcohol)
- Imágenes (noticias, películas, lugares)
- Sensaciones corporales (opresión, tacto, dolor)
- Fechas del calendario (aniversarios)
- Situaciones relacionales (discusiones, pérdida de control)

Los desencadenantes NO son una debilidad. Son señales de advertencia
almacenadas por el sistema nervioso. En terapia se aprende a
reconocer los desencadenantes y a regular el sistema nervioso.
```

---

## 4. Estrategias de Autocuidado

### Garantizar Necesidades Básicas

```
LISTA DE VERIFICACIÓN DE NECESIDADES BÁSICAS

[ ] Sueño: Horarios regulares, al menos 7 horas
[ ] Nutrición: Comidas regulares, hidratación suficiente
[ ] Ejercicio: Al menos 20 minutos diarios (un paseo es suficiente)
[ ] Contactos sociales: Al menos una persona de confianza
[ ] Seguridad: Sentirse a salvo en el propio entorno
[ ] Estructura: Rutina diaria con puntos de anclaje fijos
```

### Estrategias de Autocuidado en la Vida Diaria

**Físico:**
- Ejercicio regular (reduce hormonas de estrés)
- Ejercicios de respiración
- Sueño suficiente (mantener higiene del sueño)
- Reducir cafeína y alcohol (amplifican hiperactivación y embotamiento)

**Social:**
- Contar con personas de confianza (no es necesario hablar del trauma)
- Evitar el aislamiento (incluso pequeños contactos ayudan)
- Aprender a poner límites (permitirse decir "no")
- Aceptar apoyo

**Emocional:**
- Nombrar las emociones (sin juzgarlas)
- Utilizar técnicas de estabilización (5-4-3-2-1, lugar seguro)
- Llevar un diario reflexivo (opcional, no forzar)
- Buscar expresión creativa (pintura, música, escritura)

**Cognitivo:**
- Informarse (psicoeducación)
- Cuestionar la culpa propia ("No fue mi culpa")
- Contrastar con la realidad las interpretaciones catastrofistas
- Tener paciencia con uno mismo (la recuperación requiere tiempo)

---

## 5. Búsqueda de Ayuda Profesional

### ¿Cuándo está Indicada la Ayuda Profesional?

```
LA AYUDA PROFESIONAL ESTÁ INDICADA CUANDO:

- Los síntomas persisten durante más de 4 semanas
- Los síntomas empeoran en lugar de mejorar
- La vida cotidiana se ve gravemente interferida (trabajo, relaciones)
- Los flashbacks o pesadillas ocurren con mucha frecuencia
- Las conductas de evitación restringen severamente la vida
- Se recurre al consumo de sustancias como estrategia de afrontamiento
- Aparecen pensamientos suicidas o autolesiones
- Existe la sensación de: "No puedo manejar esto solo/a"
```

### Recursos de Ayuda

```
AYUDA INMEDIATA:
- 988 Suicide & Crisis Lifeline (EE. UU.): 988 (24/7, gratuito)
- Crisis Text Line (EE. UU.): Enviar HOME al 741741
- Teléfono de la Esperanza (España): 717 003 717
- Teléfono contra el Suicidio (España): 024
- Telefonseelsorge (Alemania): 0800 111 0 111 / 0800 111 0 222 (24/7, gratuito)
- Servicios de emergencia: 911 (EE. UU.) / 112 (España y UE)

ESPECIALIZADOS EN TRAUMA:
- Unidades de Salud Mental y Centros de Atención a Víctimas
- Líneas de atención a víctimas de violencia sexual / doméstica

BÚSQUEDA DE TERAPEUTA:
- Colegios Oficiales de Psicología / Directorios de profesionales
- Importante: Buscar profesionales especializados en "Terapia de Trauma" / "TEPT"
```

---

## 6. Preguntas Frecuentes (FAQ)

### "¿Estoy traumatizado/a ahora?"

No todas las personas que viven un evento estresante desarrollan un trastorno relacionado con el trauma. La mayoría de las personas se recuperan de forma espontánea en pocas semanas. Determinar si existe TEPT corresponde exclusivamente a un profesional de la salud mental.

### "¿Tengo que hablar obligatoriamente de lo ocurrido?"

No. Forzarse a hablar puede resultar perjudicial. Algunas personas se benefician de hablar de ello y otras no. No hay una obligación. En terapia, el momento adecuado se decide conjuntamente.

### "¿Por qué reacciono así si ocurrió hace mucho tiempo?"

Los recuerdos traumáticos se almacenan de forma diferente a los recuerdos ordinarios. Pueden reactivarse por desencadenantes y sentirse como si el evento estuviera ocurriendo AHORA. El cerebro no distingue entre "entonces" y "ahora". La terapia ayuda a "reordenar" estos recuerdos.

### "¿Soy débil por no poder superar esto por mi cuenta?"

No. Buscar ayuda es un signo de fortaleza. La terapia de trauma es altamente eficaz: la mayoría de las personas mejoran significativamente con apoyo profesional.

---

## Ética y Límites

**Un asistente de IA puede:**
- Transmitir conocimiento sobre el trauma y sus secuelas (psicoeducación)
- Normalizar las reacciones y brindar alivio
- Explicar el modelo de la ventana de tolerancia
- Sugerir estrategias de autocuidado
- Derivar a ayuda profesional
- Ofrecer técnicas de estabilización

**Un asistente de IA NO debe:**
- Realizar procesamiento de trauma (EMDR, exposición, NET, IRRT)
- Solicitar ni explorar detalles del evento traumático
- Procesar el contenido de flashbacks (solo estabilizar)
- Diagnosticar TEPT u otros trastornos relacionados con trauma
- Evaluar el riesgo suicida
- Hacer recomendaciones farmacológicas
- Emitir juicios sobre culpa o responsabilidad
- "Trabajar" o "procesar" recuerdos
- Hacer preguntas inductivas ("¿No será que...?")

**LÍMITE ESPECIALMENTE STRICTO:** El procesamiento del trauma debe estar exclusivamente en manos de terapeutas de trauma capacitados. Esta habilidad ofrece únicamente psicoeducación y estabilización. Ante cualquier forma de exploración de trauma: DETENERSE y derivar a un profesional.

**En caso de crisis aguda, SIEMPRE derivar a:**
- Línea de Prevención del Suicidio y Crisis (EE. UU.): 988
- Crisis Text Line (EE. UU.): Enviar HOME al 741741
- Línea 024 de Atención a la Conducta Suicida (España): 024
- Teléfono de la Esperanza (España): 717 003 717
- Telefonseelsorge (DE): 0800 111 0 111 / 0800 111 0 222
- Servicios de emergencia: 911 (EE. UU.) / 112 (UE)

---

*Adaptado de BACH v3.8.0 | Versión independiente*
*Fuentes: Flatten et al. (2011), Siegel (2012), Reddemann (2001), Guía S3 TEPT (2019) — No es terapia profesional*