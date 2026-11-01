---
name: sec-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Genera, SOLO a petición expresa, un parche de seguridad mínimo para un hallazgo confirmado (estado validated o triaged) - en una copia de trabajo o worktree, nunca en el original, como patches/<id>.diff sin aplicarlo, sin commit ni push. Disparadores: 'corregir este hallazgo', 'parche para SEC-...', 'cerrar esta vulnerabilidad'. No es para la corrección de errores ordinarios (usar bugfix-protocol), ni para juzgar un parche (sec-verify-fix), ni para encontrar problemas (sec-scan)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, fix, remediation]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-fix banner">

# sec-fix - parche de seguridad mínimo

La fase «fix» de la familia de seguridad ellmos. Contrato: `sec-scan/references/contract.md` (directorio §1, ciclo de vida §2, reglas §6). Aquí solo se describe la aplicación.

## Cuándo (y cuándo no)

- **Solo a petición expresa.** Un escaneo o una validación nunca desencadenan por sí solos una corrección.
- **Solo hallazgos con estado `validated` o `triaged`.** `candidate` pasa antes por `sec-validate`; `rejected` se queda como está.
- Error ordinario sin relación con la seguridad: `bugfix-protocol`. Si un parche existente es bueno: `sec-verify-fix`. Una causa estructural detrás de varios hallazgos: `sec-hardening`.

## Procedimiento

1. **Leer el hallazgo y su entorno:** `findings.json` (hallazgo, `evidence`, `recommendation`), el archivo afectado y los llamadores del punto. Corregir la causa, no el síntoma en un único sitio de llamada; si varios llamadores usan la misma función insegura, parchear el punto común.
2. **Comprobar el bloqueo (contrato §6 regla 2):** `lock_scan.py --check-dir <repo> --json`; exit 0 = libre, 1 = bloqueado, cualquier otro = desconocido = detenerse; en un host sin `lock_scan.py`, buscar en su lugar `LOCK*.txt` en el repo y en sus carpetas superiores (ninguno = libre, en otro caso detenerse). No tocar nunca `LOCK.user.*`.
3. **Copia de trabajo:** copia temporal o `git worktree` en una carpeta fuera del original. No se escribe nada en el original.
4. **Medir la línea base:** ejecutar una vez las pruebas del proyecto antes del parche y anotar el resultado (verde/rojo, cantidad). Si no hay pruebas, decirlo - no inventarlas.
5. **Parchear de forma mínima:** el cambio más pequeño que cierre la ruta source-to-sink (validación, parametrización, allowlist, escaping en el lugar correcto). Sin refactorización, sin correcciones de estilo, sin nuevas dependencias sin necesidad. Una prueba de regresión para el hallazgo forma parte del parche si el proyecto tiene pruebas.
6. **Volver a medir:** repetir las pruebas; informar con honestidad del antes/después, incluidas las pruebas en rojo y las que no se ejecutaron.
7. **Guardar el parche:** `git diff` de la copia de trabajo a `patches/<id>.diff` en el directorio de escaneo; comprobar con `git apply --check` contra el estado de destino (no cambia nada).
8. **Actualizar el hallazgo:** `status: fixed`, `fix.patchFile: patches/<id>.diff`; después `python scripts/secfind.py validate findings.json coverage.json` (el script está en `sec-scan`).

## Límites

- **Sin aplicar, sin commit, sin push (regla 3).** Eso requiere una orden directa de la persona usuaria.
- **Hallazgos de secretos:** el valor antiguo aparece necesariamente en las líneas `-` del diff. Mantener el parche en local en el directorio de escaneo, nunca en un ticket, chat o informe; antes rotar el secreto en el proveedor (regla 4). Abierto: si un diff enmascarado sería aplicable de forma útil - no inventarlo.
- Quien escribe el parche no lo revisa: `sec-verify-fix` con otro revisor (regla 7).
- Aviso de coste al corregir muchos hallazgos a la vez (regla 5); tratarlos en serie.

## Changelog

### 0.1.0 (2026-10-31)
- Versión inicial.
