---
name: sec-diff-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Escaneo de seguridad de un cambio en lugar del repositorio completo: PR, commit, diff de rama o parche del árbol de trabajo. Revisa las líneas modificadas junto con sus llamadores y llamados, busca regresiones de patrones conocidos y escribe candidatos en findings.json más un coverage.json que lista los archivos del diff y de contexto. Usar para 'security review de este PR', 'revisar este diff en busca de vulnerabilidades', 'echar un vistazo antes del merge', '¿este cambio abrió algo?'. Escaneo del repo completo: sec-scan. Refutar candidatos: sec-validate. Informe: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, diff, pull-request, regression, review]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-diff-scan

Como `sec-scan`, pero el alcance es un **cambio**. Contrato, formatos de archivo y reglas: `sec-scan/references/contract.md`; esquemas y validador en `sec-scan/schemas/` y `sec-scan/scripts/`. El preflight (propiedad, comprobación de bloqueo, egress, coste), la construcción de candidatos (`id` mediante `secfind.py id`, enmascarar secretos) y la validación funcionan como en `sec-scan` > Procedimiento. Aquí solo se enumeran las diferencias.

## Determinar el alcance

Una de estas fuentes, siempre con el punto de comparación exacto:

- PR: commit base y head del PR (en local `git diff <base>...<head>`, o traer el PR con `gh`; atención al egress).
- Commit(s) o rama: `git diff <base>...<branch>`.
- Árbol de trabajo: `git diff` y `git diff --staged` más los archivos sin seguimiento.

`findings.json` > `target.ref` = commit head (o `working-tree`), `target.scope` = los archivos del diff. Si el diff está vacío, abortar y decirlo.

## Procedimiento (en lugar de los pasos 3-5 de sec-scan)

1. **Leer el diff**, no solo los hunks: cada archivo modificado en el contexto de la función afectada.
2. **Incorporar contexto:** llamadores de las funciones modificadas (¿quién aporta las entradas?), llamados (¿hacia dónde fluyen los datos?), configuración y pruebas que documentan supuestos. Usar `threatmodel.md` si existe; si no, determinar uno mismo, brevemente, solo los límites de confianza afectados (sin modelo completo; eso es `sec-threat-model`).
3. **Preguntas de revisión para cambios:**
   - ¿Nuevos puntos de entrada o nuevos sinks (shell, SQL, sistema de archivos, deserialización, cliente HTTP)?
   - ¿Se eliminó, debilitó o eludió una comprobación (decorador de autenticación, validación, escaping, comprobación de permisos)?
   - Regresión de patrones conocidos: la misma clase de error que en hallazgos anteriores o en otra parte del repo (valores de `rule` de un `findings.json` existente, si lo hay).
   - ¿Nueva dependencia o versión cambiada en el manifiesto/lockfile; secretos o tokens en el cambio; más aperturas de configuración (CORS, debug, permisos)?
4. **Informar un hallazgo solo si la ruta alcanza realmente el punto modificado o afectado.** Fallos preexistentes en el contexto sin relación con el cambio: registrarlos con su severidad real según el contrato 3 e indicar en `description` «preexistente, no introducido por este cambio» (sin rebajarlos a `info`) o, si no se han verificado, nombrarlos solo en `coverage.limits`; no son objeto del diff.

## Cobertura

`coverage.json`: `scanned` = los archivos del diff (profundidad normalmente `read`) **y** los archivos de contexto leídos adicionalmente, `notScanned` = archivos del diff que no se leyeron (binarios, generados, demasiado grandes), con motivo. `limits` indica: «solo el cambio, el resto del repo no se escaneó». `complete` sigue el contrato 5. Un escaneo de diff limpio no dice nada sobre el repositorio.

## Límites del alcance

Sin escaneo del repo completo (`sec-scan`), sin comprobación en tiempo de ejecución (`sec-validate`), sin corrección. Salida: `findings.json`, `coverage.json`, código de salida de `secfind.py validate`.

## Changelog

### 0.1.0 (2026-10-31)

- Primera versión: alcance de cambio, incorporación de contexto, preguntas de regresión.
