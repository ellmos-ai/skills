---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Métodos de creatividad estructurada para la generación de ideas: SCAMPER, Seis Sombreros para Pensar, Mapas Mentales, Brainstorming Inverso, TRIZ e Ideación Rápida.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [brainstorm, creativity, ideation, scamper, six-hats, innovation]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/brainstorm.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `brainstorm`.


# Brainstorm (Español)

> Creatividad estructurada para la innovación — SCAMPER, Seis Sombreros para Pensar, Mapas Mentales, Brainstorming Inverso, TRIZ, Ideación Rápida

---

## ¿Cuándo usar?

- Se necesitan nuevas ideas
- Bloqueo creativo / estancamiento
- Búsqueda de innovación
- Resolver un problema de forma creativa

**Palabras clave de activación:** brainstorm, ideas, creative, innovative, ideation

---

## Métodos

### 1. SCAMPER

**Sustituir, Combinar, Adaptar, Modificar, Poner otros usos, Eliminar, Reorganizar/Invertir**

Mejorar sistemáticamente soluciones existentes:
- **S**ustituir: ¿Qué se puede reemplazar?
- **C**ombinar: ¿Qué se puede combinar?
- **A**daptar: ¿Qué se puede adaptar?
- **M**odificar: ¿Qué se puede cambiar?
- **P**oner otros usos: ¿Para qué más se podría utilizar?
- **E**liminar: ¿Qué se puede eliminar?
- **R**eorganizar / Invertir: ¿Qué se puede invertir o reorganizar?

---

### 2. Seis Sombreros para Pensar (Edward de Bono)

Pensar de forma sistemática desde 6 perspectivas:

- **Sombrero Blanco — Hechos:** ¿Qué información tenemos? ¿Qué falta?
- **Sombrero Rojo — Emoción:** ¿Qué transmite? Intuición, sentimiento visceral
- **Sombrero Negro — Crítica:** ¿Qué podría salir mal? Riesgos, debilidades
- **Sombrero Amarillo — Optimismo:** ¿Cuáles son las oportunidades? Mejor escenario
- **Sombrero Verde — Creatividad:** ¿Nuevas ideas? ¿Pensamiento disruptivo?
- **Sombrero Azul — Meta:** Control del proceso, resumen, siguientes pasos

**Proceso:** Definir el problema (Azul) -> Hechos (Blanco) -> Emociones (Rojo) -> Crítica (Negro) -> Positivos (Amarillo) -> Nuevas ideas (Verde) -> Resumir (Azul)

---

### 3. Mapas Mentales (Mind Mapping)

Visualizar los pensamientos de forma jerárquica:
1. Tema central
2. Ramas principales (3-7)
3. Subramas para cada categoría
4. Añadir detalles e ideas
5. Identificar conexiones

---

### 4. Brainstorming Inverso (Reverse Brainstorming)

Invertir el problema: "¿Cómo podemos empeorarlo?"

1. Invertir el problema
2. Recopilar malas ideas
3. Invertir = Buenas ideas

Especialmente eficaz cuando la generación directa de ideas se encuentra estancada.

---

### 5. TRIZ (Teoría para la Resolución de Problemas Inventivos)

Los 10 principios principales para software:
1. **Segmentación:** Dividir el monolito en módulos
2. **Extracción:** Aislar la propiedad molesta
3. **Calidad Local:** Diferentes componentes, diferentes propiedades
4. **Combinación:** Combinar funciones similares
5. **Universalidad:** Un elemento, múltiples funciones
6. **Anidamiento:** Componentes dentro de componentes
7. **Acción Previa:** Preparación por adelantado
8. **Retroalimentación:** Monitoreo y adaptación
9. **Autoservicio:** El sistema se mantiene a sí mismo
10. **Asimetría:** Diseños no simétricos

---

### 6. Ideación Rápida (Rapid Ideation)

Cantidad sobre calidad — más de 50 ideas en 20 min.

**Reglas:**
- SIN críticas durante la ideación
- Ideas DESCABELLADAS son bienvenidas
- Construir sobre las ideas de los demás
- La cantidad es lo PRIMERO

**Basado en temporizador:**
- Ronda 1 (5 min): Ideación abierta
- Ronda 2 (5 min): Variaciones
- Ronda 3 (5 min): Combinaciones
- Ronda 4 (5 min): Ideas extremas

---

## Workflow y Procedimiento

```
1. User request
2. Understand goal
3. Choose method(s)
4. Generate ideas (no criticism!)
5. Clustering
6. Feasibility/Impact matrix
7. Top 5-10 selection
8. Output + recommendation
```

---

## Historial de cambios

### 1.0.0 (2026-03-15)
- Portado desde BACH v3.8.0

---

*Portado desde BACH v3.8.0 | Versión independiente*
