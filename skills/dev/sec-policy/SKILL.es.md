---
name: sec-policy
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Define, revisa o actualiza el SECURITY.md de un repo (alcance, áreas excluidas, propiedades de seguridad exigidas, canal de notificación, plazos de respuesta, versiones soportadas) y contrasta sus afirmaciones con el código real. La política es la base de sec-triage. Disparadores: 'crear/revisar SECURITY.md', 'política de seguridad', 'qué cuenta aquí como vulnerabilidad', 'definir el canal de notificación'. No es para hallazgos (sec-scan) ni para informes de divulgación (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, policy, security-md, disclosure]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-policy - definir y revisar SECURITY.md

La política dice qué cuenta como vulnerabilidad en este repo. `sec-triage` valora los hallazgos frente a ella (contrato `sec-scan/references/contract.md` §2: `triaged` = severidad y prioridad decididas según la política). Sin política, el triaje adivina.

## Contenido de un SECURITY.md

| Sección | Pregunta a la que responde |
|---|---|
| Versiones soportadas | ¿qué versiones reciben correcciones de seguridad? |
| Alcance | ¿qué componentes, interfaces, despliegues se contemplan? |
| Excluido | ¿qué no cuenta expresamente (código de pruebas, ejemplos, limitaciones conocidas, ataques que requieren acceso al sistema anfitrión)? |
| Propiedades de seguridad exigidas | ¿qué debe garantizar el proyecto (p. ej. «sin secretos en el repo», «la entrada de red se valida», «los plugins se ejecutan sin acceso a archivos fuera de X»)? El triaje mide frente a esto. |
| Canal de notificación | dónde notificar: marcador `<security-contact>`; o el private vulnerability reporting de GitHub si está activado en el repo. **No inventar una dirección.** |
| Plazos de respuesta | acuse de recibo, valoración, objetivo de corrección - los valores los aporta quien mantiene, no el skill; marcar las sugerencias como tales. |
| Divulgación | coordinada, plazos de quien mantiene; remitir a `sec-writeup`. |

## Procedimiento

1. **Leer lo existente:** `SECURITY.md` actual, README, archivos de dependencias y build, estructura del código (puntos de entrada, auth, acceso a archivos, red, mecanismos de plugins).
2. **Afirmación frente a evidencia:** contrastar cada promesa de la política («toda la entrada se valida», «sin telemetría», «se mantienen las versiones X.y») con el código o los releases. Una contradicción es un hallazgo (`sec-scan`) o una corrección de la política, nunca se ignora en silencio. Lo que no se puede comprobar: marcarlo como no verificado.
3. **Borrador o diff:** nuevo SECURITY.md o una propuesta de cambio con puntos abiertos (marcadores `<...>`) para decisiones de quien mantiene. Si falta una respuesta, preguntar en lugar de adivinar.
4. **Ubicación:** borrador en el chat o en el directorio de escaneo. El repo solo se escribe por orden directa de la persona usuaria (comprobar el bloqueo, regla 2; sin commit/push, regla 3). El archivo nunca contiene secretos, rutas del host ni contactos privados (regla 4).

## Fronteras

Propuestas técnicas de hardening: `sec-hardening`. Comprobar si un repo está listo para su publicación: `repo-publish-check`.

## Changelog

### 0.1.0 (2026-10-31)
- Versión inicial.
