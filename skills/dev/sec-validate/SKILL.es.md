---
name: sec-validate
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Intenta REFUTAR cada candidato de findings.json: trazar la ruta source-to-sink, comprobar alcanzabilidad y contramedidas, calibrar la severidad, reproducir en local donde sea seguro. Establece validatedBy (confirmed/refuted/uncertain) y el estado validated o rejected con motivo. Usar para 'verificar los hallazgos', 'descartar falsos positivos', '¿es realmente explotable?', 'segunda comprobación independiente del escaneo'. Quien valida debería ser un proveedor distinto del que encontró el hallazgo. Encontrar nuevos problemas: sec-scan. Clasificar informes ajenos: sec-triage. Informe: sec-report."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, validation, false-positives, exploitability, review]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-validate

Fase 3 de la familia de seguridad ellmos. Contrato: `sec-scan/references/contract.md` (ciclo de vida 2, severidad 3, reglas 6). Validador: `sec-scan/scripts/secfind.py`. Postura: **refutar, no confirmar.** Un candidato cuenta como `validated` solo cuando fracasa el intento de refutarlo.

## Entrada e independencia

- Entrada: `findings.json` + `coverage.json` de un escaneo, candidatos con `status: candidate` (o una selección de `id` indicada por la persona usuaria).
- **Validador independiente (contrato 6.7):** preferiblemente un proveedor distinto del `provider.name` del escaneo (Claude <-> Codex). Sin él: un subagente independiente de la clase de modelo superior que **no** lea de antemano el razonamiento de quien encontró el hallazgo; dejarlo anotado en el resultado. Varios proveedores o un fan-out: estimar primero el coste y avisar a la persona usuaria (6.5). Si el código va a un proveedor externo, declarar el egress (6.6).
- Preflight como el paso 2 de `sec-scan` (propiedad, comprobación de bloqueo, fail-closed).

## Por candidato

1. **Leerlo de nuevo:** leer uno mismo el código en `location`; usar la `evidence` de quien lo encontró solo como pista.
2. **Trazar la ruta:** source -> transformaciones -> sink, cada paso con archivo:línea. Una cadena rota es motivo de refutación.
3. **Alcanzabilidad:** ¿qué ruta, llamador o autenticación lleva hasta allí? El código muerto, el código de pruebas, las rutas solo para administradores y los llamadores internos reducen la severidad o refutan.
4. **Buscar contramedidas:** validación, escaping, consultas parametrizadas, protección del framework, configuración, comprobaciones previas, permisos. También en otros lugares (middleware, wrappers).
5. **Nombrar las precondiciones del atacante** (anónimo, cuenta, acceso local, configuración específica).
6. **Reproducir si es seguro:** solo en una copia local o entorno de pruebas, con datos sintéticos y servicios simulados; p. ej. una prueba unitaria dirigida o una llamada a la función con una entrada de ataque. **Nunca** contra sistemas de terceros o de producción, sin acceso de red saliente, sin secretos reales, sin destrucción. Si no puede reproducirse con seguridad, basta el argumento estático y se permite el veredicto `uncertain`.
7. **Calibrar la severidad** según contrato 3 (alcanzabilidad por impacto); restablecer `confidence`. Registrar un cambio como «severidad antigua -> nueva: motivo» en `description`.
8. **Escribir el veredicto:**

| Veredicto | Consecuencia en `findings.json` |
|---|---|
| `confirmed` | `status: validated`, `validatedBy: {provider, model, verdict: confirmed}`; ruta y eventual repro en `description`; añadir `impact` y `recommendation` |
| `refuted` | `status: rejected`, `rejectedReason` que nombre la contramedida concreta o la ruptura de la cadena, `validatedBy.verdict: refuted` |
| `uncertain` | `status` sigue en `candidate`, `validatedBy.verdict: uncertain`, `description` indica qué falta para decidir |

`validatedBy.provider` / `.model` son los del **validador**, no los de quien encontró el hallazgo. El mismo proveedor que el del hallazgo dispara la advertencia del validador «validated by the same provider»; permanece visible y no se suprime.

## Cierre

`python sec-scan/scripts/secfind.py validate findings.json coverage.json`, mostrar el código de salida. Resumen: número por veredicto, cambios de severidad, `uncertain` abiertos. Continuar con `sec-triage` (hallazgos validados) y `sec-report`. Sin valores secretos en `description` ni en la salida de la repro (contrato 6.4). Sin parches, sin commit.

## Changelog

### 0.1.0 (2026-10-31)

- Primera versión: procedimiento de refutación, mapeo de veredictos, independencia.
