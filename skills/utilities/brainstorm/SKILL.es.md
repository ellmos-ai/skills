---
name: brainstorm
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: Métodos de creatividad estructurada para la generación de ideas: SCAMPER, Seis Sombreros para Pensar, Mapa Mental, Lluvia de Ideas Inversa, TRIZ e Ideación Rápida.

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

<img src="banner.png" width="100%" alt="brainstorm banner">

> **Español** — Versión oficial en español de `brainstorm`.


# Brainstorm (Español)

> Creatividad estructurada para la innovación — SCAMPER, Seis Sombreros, Mapas Mentales, Lluvia de Ideas Inversa, TRIZ, Ideación Rápida

---

## ¿Cuándo usarlo?

- Se necesitan nuevas ideas
- Bloqueo creativo / estancamiento
- Se busca innovación
- Resolver un problema de forma creativa

**Palabras clave desencadenantes:** brainstorm, ideas, creativo, innovador, ideación

---

## Métodos

### 1. SCAMPER

**Sustituir, Combinar, Adaptar, Modificar, Dar otro uso, Eliminar, Invertir**

Mejorar sistemáticamente las soluciones existentes:
- **S**ustituir: ¿Qué se puede reemplazar?
- **C**ombinar: ¿Qué se puede combinar?
- **A**daptar: ¿Qué se puede adaptar?
- **M**odificar: ¿Qué se puede cambiar?
- **P**oner en otro uso: ¿Para qué más se podría utilizar?
- **E**liminar: ¿Qué se puede quitar?
- **R**evertir/Invertir: ¿Qué se puede invertir?

---

### 2. Seis Sombreros para Pensar (Edward de Bono)

Pensar sistemáticamente a través de 6 perspectivas:

- **Sombrero Blanco — Hechos:** ¿Qué información tenemos? ¿Qué falta?
- **Sombrero Rojo — Emoción:** ¿Cómo se siente? Intuición, corazonada
- **Sombrero Negro — Crítica:** ¿Qué podría salir mal? Riesgos, puntos débiles
- **Sombrero Amarillo — Optimismo:** ¿Cuáles son las oportunidades? Mejor escenario
- **Sombrero Verde — Creatividad:** ¿Nuevas ideas? ¿Pensamiento fuera de la caja?
- **Sombrero Azul — Meta:** Control del proceso, resumen, siguientes pasos

**Proceso:** Definir problema (Azul) -> Hechos (Blanco) -> Emociones (Rojo) -> Crítica (Negro) -> Positivos (Amarillo) -> Nuevas ideas (Verde) -> Resumir (Azul)

---

### 3. Mapa Mental (Mind Mapping)

Visualizar pensamientos de forma jerárquica:
1. Tema central
2. Ramas principales (3-7)
3. Subramas para cada categoría
4. Añadir detalles e ideas
5. Identificar conexiones

---

### 4. Lluvia de Ideas Inversa (Reverse Brainstorming)

Invertir el problema: "¿Cómo hacemos para empeorarlo?"

1. Invertir el problema
2. Recopilar malas ideas
3. Invertir = Buenas ideas

Especialmente eficaz cuando la ideación directa está estancada.

---

### 5. TRIZ (Teoría para la Resolución de Problemas Inventivos)

Los 10 principios principales para software:
1. **Segmentación:** Dividir un monolito en módulos
2. **Extracción:** Aislar la propiedad perturbadora
3. **Calidad local:** Diferentes componentes, diferentes propiedades
4. **Fusión:** Combinar funciones similares
5. **Universalidad:** Un elemento, múltiples funciones
6. **Anidamiento:** Componentes dentro de componentes
7. **Acción preliminar:** Preparación por adelantado
8. **Retroalimentación:** Monitoreo y adaptación
9. **Auto-servicio:** El sistema se mantiene a sí mismo
10. **Asimetría:** Diseños no simétricos

---

### 6. Ideación Rápida (Rapid Ideation)

Cantidad sobre calidad — más de 50 ideas en 20 minutos.

**Reglas:**
- SIN críticas durante la ideación
- Ideas CURIOSAS/SALVAJES bienvenidas
- Construir sobre las ideas de otros
- Cantidad PRIMERO

**Basado en temporizador:**
- Ronda 1 (5 min): Ideación abierta
- Ronda 2 (5 min): Variaciones
- Ronda 3 (5 min): Combinaciones
- Ronda 4 (5 min): Ideas extremas

---

## Flujo de trabajo y procedimiento

```
1. Solicitud del usuario
2. Comprender el objetivo
3. Elegir método(s)
4. Generar ideas (¡sin críticas!)
5. Agrupación (Clustering)
6. Matriz de factibilidad/impacto
7. Selección de las mejores 5-10
8. Salida + recomendación
```

---

## Registro de cambios

### 1.0.0 (2026-03-15)
- Adaptado desde BACH v3.8.0

---

*Adaptado desde BACH v3.8.0 | Versión independiente*