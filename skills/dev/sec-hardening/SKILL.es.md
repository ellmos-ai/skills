---
name: sec-hardening
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Deriva propuestas estructurales de hardening a partir de hallazgos, informes de incidentes o evaluaciones en lugar de parches puntuales: agrupar causas raíz, imagen de arquitectura antes/después (ASCII), alternativas con sus compromisos (esfuerzo, riesgo, efecto), orden de implementación, evidencia por propuesta. Entrega un documento y no cambia código. Disparadores: 'cómo reforzamos esto de raíz', 'por qué siguen apareciendo hallazgos como este', 'hacer más segura la arquitectura', 'plan de acción a partir del incidente'. No es para corregir un único hallazgo (sec-fix) ni para la defensa aguda (protection-shield)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, hardening, architecture, root-cause]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-hardening banner">

# sec-hardening - estructural en lugar de pieza a pieza

Cuando los hallazgos de la misma clase reaparecen una y otra vez, la causa suele estar en la estructura (sin validación central, límite de confianza sin comprobar, secretos en el código). Este skill propone cambios a ese nivel. Contrato: `sec-scan/references/contract.md` (hallazgos §1/§2, regla 4 secretos, regla 5 coste).

## Entrada

`findings.json` (idealmente `validated` o posterior), informes de incidentes, evaluaciones, `threatmodel.md` y conocimiento del código. Sin propuestas sin una entrada respaldada por evidencia; marcar los supuestos como tales.

## Procedimiento

1. **Agrupar causas raíz:** agrupar los hallazgos por raíz, no por archivo: p. ej. «cada ruta construye el SQL por su cuenta», «la comprobación de acceso se repite en cada handler», «la configuración contiene secretos». Nombrar los ids de hallazgo por grupo.
2. **Esbozar la arquitectura actual** como imagen ASCII: límites de confianza, flujo de datos, dónde se realiza (o no) hoy la comprobación.
3. **Opciones por causa** (al menos dos, incluida «solo parches individuales»): descripción, **esfuerzo**, **riesgo de implementación** (regresiones, migración), **efecto** (qué clase de hallazgo desaparece, cuál permanece), dependencias. En forma de tabla.
4. **Recomendación** por causa con justificación y una **imagen objetivo** (ASCII) junto a la actual.
5. **Orden:** qué primero porque cierra varios hallazgos a la vez o es requisito previo; qué puede esperar. Pasos intermedios que puedan entregarse por separado.
6. **Evidencia por propuesta:** ids de hallazgo, ubicaciones en el código (`path:line`), mediciones. Una propuesta sin evidencia se marca como hipótesis. Sin cifras de esfuerzo en tiempo inventadas; solo relativas (small/medium/large) o aportadas por la persona usuaria.

## Salida

Un documento (p. ej. `hardening.md` en el directorio de escaneo, o en el chat), secciones: punto de partida, causas, imágenes actual/objetivo, opciones, recomendación, orden, preguntas abiertas. **No cambia código**, no crea parches y no hace commit de nada (regla 3); los pasos individuales se ejecutan mediante `sec-fix` o el desarrollo normal. Sin valores secretos en el documento (regla 4).

## Changelog

### 0.1.0 (2026-10-31)
- Versión inicial.
