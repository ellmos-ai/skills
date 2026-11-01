---
name: sec-verify-fix
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Comprueba de forma independiente si un parche de seguridad cierra realmente la vulnerabilidad (volver a trazar la ruta source-to-sink sobre el estado parcheado, prueba negativa y de regresión), valora el riesgo de regresión y si un merge automático sería defendible (por defecto: no para critical/high). Revisión de solo lectura, no aplica nada. Disparadores: '¿el parche cierra la brecha?', 'revisar el parche', 'verificar la corrección', un hallazgo en estado fixed. No es para escribir el parche (sec-fix), ni para la revisión de código en general."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, patch, review, verification, regression]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-verify-fix banner">

# sec-verify-fix - ¿el parche cierra la brecha?

La fase «verify-fix». Contrato: `sec-scan/references/contract.md` (ciclo de vida §2, regla 7 en §6). Requiere un hallazgo con estado `fixed` y `fix.patchFile`.

## Primero la independencia

Quien revisa **no** es quien escribió el parche (regla 7): preferiblemente otro proveedor (Claude <-> Codex); si no, un subagente independiente de primer nivel con contexto limpio que reciba solo el hallazgo, el parche y el código - no el razonamiento de quien lo escribió. Si de todos modos hay que comprobarlo uno mismo, decirlo en el resultado; entonces `verifiedBy` queda vacío y el estado sigue siendo `fixed`.

## Procedimiento

1. **Aplicar el parche en una copia temporal** (nunca en el original); comprobar el bloqueo como en `sec-fix` (regla 2). Si el parche no se aplica limpiamente, eso ya es el resultado.
2. **Volver a trazar la ruta:** recorrer línea a línea, sobre el estado parcheado, la ruta source-to-sink original de `evidence`. ¿Sigue siendo alcanzable el sink? ¿Hay rutas paralelas (otros llamadores, variantes de entrada, otras codificaciones) que el parche no cubre?
3. **Prueba negativa:** una entrada mínima, no convertida en arma, que antes habría desencadenado el hallazgo debe ahora ser rechazada o neutralizada. Solo en copia temporal, solo código propio (regla 1). Si una prueba no puede ejecutarse con sentido, informarlo como «not tested».
4. **Prueba de regresión:** pruebas del proyecto antes/después; las entradas legítimas siguen funcionando. Nombrar las pruebas en rojo o no ejecutadas.
5. **Valorar el riesgo de regresión:** rutas de ejecución y llamadores afectados, contratos modificados (firmas, formatos, comportamiento ante errores), cobertura de pruebas del punto, reversibilidad (parche puro de código frente a migración de datos/configuración). Nivel low/medium/high con motivos.
6. **¿Merge automático?** sí/no con motivos. **Por defecto no para critical/high**; sí solo si la ruta está cerrada, las pruebas negativa y de regresión están en verde, el riesgo es bajo y el rollback es sencillo. Quien revisa nunca decide solo; prevalecen las reglas de merge del repo.

## Resultado

- **Cierra:** sí / parcialmente / no, nombrando el punto concreto que sigue abierto. Con «no»/«parcialmente» el estado sigue siendo `fixed` y el trabajo vuelve a `sec-fix`; el hallazgo no se descarta.
- **Con «sí»:** `status: verified`, `fix.verifiedBy: "<provider>/<model>"` y `python scripts/secfind.py validate findings.json coverage.json` (script en `sec-scan`). La argumentación, el nivel de riesgo y la recomendación de merge van en el informe para la persona usuaria; el contrato no tiene campo para ellos, así que no inventar ninguno.
- No aplica nada, no hace commit ni push (regla 3).

## Changelog

### 0.1.0 (2026-10-31)
- Versión inicial.
