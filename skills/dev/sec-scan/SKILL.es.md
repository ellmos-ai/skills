---
name: sec-scan
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Escaneo de seguridad, independiente del proveedor, de un repositorio propio: modelo de amenazas, división por límite de confianza, revisión dirigida por paquete (injection, authn/authz, secretos, criptografía, deserialización, rutas, SSRF, configuración, uso de dependencias vulnerables), candidatos con evidencia en findings.json y un coverage.json honesto. Modos standard y deep. Usar para 'security scan', 'revisar este repo en busca de vulnerabilidades', 'security review', 'escaneo completo', 'importar el resultado de un escáner al formato ellmos'. Incluye el adaptador para /claude-security y codex-security. Solo cambios/PR: sec-diff-scan. Refutar candidatos: sec-validate. Importar informes ajenos: sec-triage. Informe: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, scan, vulnerabilities, sast, source-to-sink, cwe]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-scan

Núcleo de la familia de seguridad ellmos. El contrato común (fases, archivos, ciclo de vida, severidad, reglas, adaptadores) está en `references/contract.md`, los esquemas en `schemas/`, el validador en `scripts/secfind.py` + `scripts/seclib.py` (solo biblioteca estándar). Este skill cita el contrato y no lo repite. Vecinos: `sec-threat-model`, `sec-diff-scan`, `sec-validate`, `sec-triage`, `sec-report`.

## Modos

- **standard:** una pasada, un modelo, una sesión.
- **deep:** varias pasadas independientes (distinto orden de paquetes, división o modelo), fusionadas por `id`. Solo tras un aviso de coste y confirmación de la persona usuaria (contrato 6.5).

## Procedimiento

1. **Objetivo y alcance:** repo, ref (SHA de commit o `working-tree`), rutas excluidas. Asignar un `scanId`. El directorio de escaneo se llama `sec-scan-<scanId>/` (contrato 1), cuelga de una carpeta base **fuera del repo** y se crea solo después del preflight.
2. **Preflight:**
   - ¿Código propio o autorizado? Si no, abortar (contrato 6.1).
   - Comprobación de bloqueo del repo y de la carpeta base del directorio de escaneo: `python <lock_scan.py> --check-dir '<path>' --json`, guardar el código de salida de inmediato. 0 = libre, 1 = bloqueado, cualquier otro (fallo, salida ilegible) = desconocido = detenerse (contrato 6.2). Llamar al intérprete de forma explícita, nunca «abrir» el script. Si `lock_scan.py` no existe en este host (sin sistema de bloqueo ellmos), buscar en su lugar `LOCK*.txt` en el repo y en sus carpetas superiores: ninguno = libre (anotarlo en el informe), uno o más = detenerse.
   - **Declarar el egress:** ¿sale código hacia un proveedor (capa de revisión alojada, modelo de terceros)? Los repos privados se quedan en la sesión local (contrato 6.6). **Declarar el coste**, y para `deep` esperar confirmación (6.5).
3. **Modelo de amenazas:** ¿existe `threatmodel.md` y está al día? Si no, ejecutar `sec-threat-model`.
4. **Formar paquetes:** dividir el repo según los límites de confianza y los puntos de entrada del modelo; por paquete, archivos y preguntas de investigación. Dividir los paquetes muy grandes en lugar de leerlos superficialmente.
5. **Revisar cada paquete** (source-to-sink: source -> transformación -> sink, leyendo también las contramedidas en la ruta):
   injection (SQL, shell, plantillas, LDAP/NoSQL), authn/authz y separación de tenants, secretos en el código, criptografía (algoritmos, aleatoriedad, gestión de claves), deserialización insegura, acceso a rutas/archivos (traversal, upload, symlinks), SSRF y open redirect, configuración insegura (debug, CORS, valores por defecto, permisos), uso de dependencias con vulnerabilidades conocidas (patrones en el código; el cotejo con advisories corresponde a `security-tech-stack-check`). No registrar hallazgos que la ruta no respalde; las sospechas sin evidencia van a `coverage.limits`, no a `findings`.
6. **Registrar un candidato:** `rule` con puntos y en minúsculas (`py.sql-injection`), `cwe` donde corresponda, `severity` y `confidence` según contrato 3, `status: candidate`, `location`, `evidence` como código/traza citados. **Enmascarar los valores secretos** (contrato 4). Derivar siempre el `id` con `python scripts/secfind.py id RULE PATH -` (fragmento por stdin), nunca a mano.
7. **Mantener la cobertura honesta:** `scanned` con profundidad `read` / `skimmed` / `pattern-only`, `notScanned` con motivo (generado, vendored, demasiado grande, binario, inalcanzable), `limits` para las limitaciones del método. `complete: true` solo cuando `notScanned` está vacío (contrato 5). `unknown` no es «seguro».
8. **Validar:** `python scripts/secfind.py validate findings.json coverage.json`, mostrar el código de salida (0/1) y la salida. Si hay errores, corregir y repetir.
9. **Cierre:** número de candidatos por severidad, estado de la cobertura, siguientes pasos (`sec-validate`, luego `sec-triage`, `sec-report`). Un escaneo parcial se informa como parcial (contrato 6.9).

## deep

Al menos dos pasadas con divisiones distintas, cada una con su propia lista de candidatos. Fusión por `id`: unir los `id` iguales (añadir evidencia; si la severidad difiere, tomar la mayor y indicar la diferencia en `description`), añadir los `id` nuevos. Cobertura = unión de las rutas leídas; `provider.model` enumera todos los modelos implicados.

## Adapter

Un escáner de proveedor existente puede encargarse de la parte de escaneo (contrato 7): **Claude** `/claude-security`, **Codex** `codex-security`. Gemini y Kimi no tienen ninguno y siguen el procedimiento anterior.

1. Ejecutar el escáner tras el preflight (paso 2); leer sus archivos de salida y mapearlos campo a campo a `findings.json` / `coverage.json`. Aquí no se presuponen los archivos ni los campos del escáner; el mapeo se construye al leer la salida real y se anota en `coverage.limits`.
2. **Todos los hallazgos empiezan como `candidate`**, incluso si el escáner los informa como confirmados. Un adaptador nunca omite la validación.
3. `provider.name` / `provider.model` tras el escaneo, `provider.engine` = nombre del escáner.
4. Tomar la cobertura del informe del escaneo. Si no la ofrece, poner `complete: false` e indicar en `notScanned` o `limits` que se desconoce la cobertura del escáner.
5. Reconstruir los `id` con `secfind.py id` para que los hallazgos coincidan con los de otras ejecuciones. Luego el paso 8.

## Límites

Sin parches, sin commits, sin escaneos de red (contrato 6.1, 6.3). Sin exploits en tiempo de ejecución; la reproducción corresponde a `sec-validate`.

## Changelog

### 0.1.0 (2026-10-31)

- Primera versión: modos standard/deep, preflight, paquetes, adaptador.
