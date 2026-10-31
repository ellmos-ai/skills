---
name: sec-threat-model
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Crea o actualiza el modelo de amenazas de un repositorio propio (activos, límites de confianza, puntos de entrada, flujos de datos, objetivos del atacante, preguntas de investigación priorizadas) como threatmodel.md, derivado del código fuente real. Usar para 'threat model', 'superficie de ataque', 'qué debería revisar primero en este repo', antes de un escaneo de seguridad o tras un cambio de arquitectura. Funciona de forma independiente o como fase 1 de sec-scan; no encuentra vulnerabilidades por sí mismo (usar sec-scan / sec-diff-scan) y no comprueba advisories de dependencias (usar security-tech-stack-check)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, threat-model, attack-surface, trust-boundaries, review]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-threat-model

Fase 1 de la familia de seguridad ellmos (`sec-threat-model`, `sec-scan`, `sec-diff-scan`, `sec-validate`, `sec-triage`, `sec-report`). Contrato común: `sec-scan/references/contract.md` (sección 1 directorio de escaneo, sección 6 reglas). No se repite aquí.

## Reglas

- Solo código propio o expresamente autorizado (contrato 6.1). Sin acceso de red a sistemas de terceros, sin escaneos de puertos.
- El modelo se construye a partir de **código fuente leído**, no de afirmaciones del README. Lo que solo se afirma allí o no puede respaldarse con evidencia entra como `open`, nunca como hecho.
- Escribir solo en el directorio de escaneo (`<tmp>/ellmos-security/<repo>/<scanId>/`), nunca en el árbol de fuentes. Comprobar el bloqueo antes de escribir, como se describe en `sec-scan` > Preflight.

## Procedimiento

1. **Aclarar el alcance:** repo, ref (SHA de commit o `working-tree`), rutas excluidas. Leer un `threatmodel.md` existente; si lo hay, pasar al modo de actualización: solo arrastrar los cambios y anotar estado y ref.
2. **Leer la estructura:** manifiestos, archivos de build/deploy, configuración, árbol de directorios. Deducir lenguajes y frameworks a partir del código.
3. **Encontrar puntos de entrada:** rutas HTTP, argumentos de CLI, consumidores de colas/webhooks, parsers de archivos y formatos, IPC/sockets, tareas programadas, variables de entorno, puntos de carga de plugins/scripts. Para cada uno: archivo:línea y población de llamadores (anónimo, autenticado, interno).
4. **Nombrar activos:** secretos y tokens, datos personales, archivos de usuario, bases de datos, cómputo, privilegios de ejecución, reputación/cadena de suministro. Indicar la ubicación en el código, nunca el valor.
5. **Trazar límites de confianza:** donde los datos pasan de menos a más confiable (red -> proceso, usuario -> admin, tenant -> tenant, proceso -> SO/shell/BD, paquete de terceros -> código propio). Dónde reside en el código la aplicación de controles (authn/authz, validación, sandbox), o que falta.
6. **Esbozar flujos de datos:** source -> transformación -> sink para los activos y puntos de entrada más críticos (texto o Mermaid, breve). Sinks: shell, SQL, sistema de archivos, deserialización, plantillas, cliente HTTP, logs.
7. **Derivar objetivos del atacante:** por cada límite, qué quiere un atacante (ejecución de código, exfiltración de datos, escalada de privilegios, manipulación, interrupción del servicio). STRIDE solo como ayuda para pensar, no como cuadrícula obligatoria.
8. **Priorizar las preguntas de investigación:** preguntas concretas y comprobables («¿llega `user_id` de la ruta X sin comprobar a la consulta de `db.py`?»), ordenadas por impacto multiplicado por alcanzabilidad. `sec-scan` las convierte en paquetes de investigación.

## Salida: `threatmodel.md`

Secciones en este orden: **Estado** (repo, ref, fecha, rutas leídas) · **Activos** · **Límites de confianza** · **Puntos de entrada** (tabla: ruta, tipo, llamador, auth) · **Flujos de datos** · **Objetivos del atacante** · **Preguntas de investigación** (numeradas, priorizadas) · **Abierto** (supuestos, áreas sin leer, contradicciones entre documentación y código). Sin valores secretos, sin instrucciones de exploit.

## Límites del alcance

No encuentra vulnerabilidades y no asigna severidad. Un modelo con muchas entradas `open` es más honesto que uno pulido.

## Changelog

### 0.1.0 (2026-10-31)

- Primera versión como fase 1 de la familia de seguridad.
