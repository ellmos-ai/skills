---
name: sec-triage
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Convierte hallazgos existentes (informes de escáneres, SARIF, GitHub code scanning, Dependabot, tickets) al formato findings.json de la familia de seguridad ellmos, los deduplica por id, fija severidad y prioridad según la política de seguridad del repositorio (SECURITY.md) y enlaza tickets. Solo evaluación estática. Usar para 'clasificar estos resultados de escaneo', 'priorizar alertas de Dependabot', 'importar hallazgos de code scanning', 'ordenar el backlog de hallazgos de seguridad'. Encontrar nuevas vulnerabilidades: sec-scan. Refutar o reproducir: sec-validate. Informe: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, triage, sarif, dependabot, code-scanning, prioritisation]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-triage

Fase 4 de la familia de seguridad ellmos. Contrato: `sec-scan/references/contract.md` (archivos 1, ciclo de vida 2, severidad 3, id 4, reglas 6). Validador: `sec-scan/scripts/secfind.py`. **Solo evidencia estática:** sin nuevos descubrimientos (`sec-scan`), sin validación en tiempo de ejecución (`sec-validate`).

## Entrada

Hallazgos existentes: archivos SARIF o informes de escáneres, GitHub code scanning y Dependabot (exportar mediante `gh` o desde la interfaz web; atención al egress), tickets, listas de auditoría. Si ya existe un `findings.json`, se continúa con él; si no, se crea (directorio de escaneo según contrato 1). Preflight como el paso 2 de `sec-scan` (propiedad, comprobación de bloqueo fail-closed).

## Procedimiento

1. **Mapear:** una entrada por hallazgo de origen. Normalizar `rule` a minúsculas con puntos (`py.sql-injection`; poner el identificador original de la regla y la fuente en `description`), `cwe` a partir de las etiquetas de la fuente, `location` a partir de la alerta, `severity` inicialmente tal como la indica la fuente, `status: candidate`.
2. **Asegurar la evidencia:** extracto de código de la alerta; si no, leer el punto en el archivo indicado y citarlo. Si no se puede establecer evidencia (archivo ausente, línea desplazada, alerta sin código), **no** importar el hallazgo con evidencia inventada; listarlo en `coverage.limits` como no importado, con el motivo. Enmascarar los valores secretos (contrato 4). Para alertas de dependencias: `rule` p. ej. `dep.vulnerable-dependency`, `location` = línea del manifiesto/lockfile, `evidence` = esa línea; id del advisory y versión afectada en `description`.
3. **Deduplicar:** construir el `id` con `python sec-scan/scripts/secfind.py id RULE PATH -`. Los `id` iguales (también entre varias fuentes) se fusionan en un hallazgo, listando las fuentes en `description`; si la severidad difiere, tomar la mayor y anotarlo.
4. **Leer la política:** `SECURITY.md` (definiciones de severidad, plazos, versiones soportadas, canal de notificación) y las eventuales decisiones del proyecto. Si no hay, rige el contrato 3 y el resultado lo indica.
5. **Fijar severidad y prioridad:** contrastar la severidad con la política y ajustarla con un motivo; derivar la prioridad de la severidad, la exposición y los plazos y fijarla en `priority` (`P0`-`P4`, P0 la más urgente; mapear sobre ello los niveles de la política), con el motivo en `description`.
6. **Estado:** según el validador, `triaged` exige `validatedBy.verdict == confirmed`. Los hallazgos ya validados (`validated`) pasan a `triaged`. Los hallazgos importados y aún no validados se quedan en `candidate` con severidad/prioridad fijadas y pasan a `sec-validate`. Excluir solo si la política lo contempla expresamente (p. ej. versión no soportada): `rejected` con `rejectedReason`.
7. **Tickets:** solo si la persona usuaria o la política lo exigen: `ticket_writer.py` (nunca ids elegidos a mano) o GitHub issue/borrador de advisory; las vulnerabilidades en repos públicos como borrador de advisory **privado**, no como issue público. Anotar la referencia en `ticket`. Sin valores secretos en los tickets (contrato 6.4).
8. **Cobertura:** una importación pura no escanea nada. `scanned: []`, `notScanned` con una entrada «import without own scan, repo not read» (por tanto `complete: false`), `limits` con fuentes, estado de la importación y hallazgos no importados. `provider.name` = fuente (p. ej. `github-code-scanning`), `model` = `n/a`, `engine` = herramienta de origen.
9. **Comprobar:** `python sec-scan/scripts/secfind.py validate findings.json coverage.json`, mostrar el código de salida. Luego `sec-validate` para los candidatos, `sec-report` para el informe.

## Changelog

### 0.1.0 (2026-10-31)

- Primera versión: importación, deduplicación por id, triaje según la política.
