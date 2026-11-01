---
name: sec-report
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Genera el informe de seguridad report.md (agrupado por severidad, sección de cobertura con lagunas, hallazgos rechazados por separado, resumen sin edulcorar) y findings.sarif (SARIF 2.1.0) a partir de findings.json y coverage.json mediante el script render_report.py. Usar para 'redactar el informe de seguridad', 'resumir el resultado del escaneo', 'exportar SARIF', 'informe para code scanning'. Aborta con datos inválidos; un escaneo parcial se informa como parcial. Nuevos hallazgos: sec-scan / sec-diff-scan. Verificar: sec-validate. Clasificar: sec-triage."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, report, sarif, coverage, findings]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-report banner">

# sec-report

Fase final de la familia de seguridad ellmos. Contrato: `sec-scan/references/contract.md` (archivos 1, severidad 3, cobertura 5, reglas 6). El script importa `seclib` de la carpeta hermana `sec-scan/scripts` (en el repo `skills/dev/` y en un despliegue plano `~/.claude/skills/`; ambas carpetas deben estar una junto a la otra). Solo biblioteca estándar.

## Uso

```
python scripts/render_report.py FINDINGS COVERAGE OUTDIR [--lang de|en]
```

Llamar al intérprete de forma explícita. `OUTDIR` es el directorio de escaneo; comprobar antes el bloqueo como en el paso 2 de `sec-scan` (fail-closed). Resultado: `OUTDIR/report.md` y `OUTDIR/findings.sarif`. Códigos de salida: 0 = escrito, 1 = entrada ilegible o inválida (**no** se escribe nada), 2 = uso incorrecto. Mostrar el código de salida y la salida. El idioma por defecto del informe es el alemán; usar `--lang en` para inglés.

## Comportamiento

- **Valida primero** (`seclib.validate_findings`). Los errores se listan y no se genera ningún informe a partir de datos rotos. Corregir antes la causa (`sec-scan`, `sec-validate`) y volver a renderizar.
- **report.md:** cabecera (objetivo, ref, escáner) · resumen · advertencias · hallazgos por severidad (de critical a info) con ubicación, confianza, estado, validador, evidencia, descripción, impacto, recomendación, ticket · **hallazgos rechazados por separado** con motivo · cobertura (escaneado con profundidad, no escaneado con motivo, límites).
- **Honestidad (contrato 5, 6.9):** `complete: false` aparece al principio del todo como «PARTIAL SCAN». Sin hallazgos y con cobertura incompleta se lee «NOT a clean result». Solo «No findings with complete coverage» puede leerse como un resultado limpio. Las advertencias, como el mismo proveedor para quien encuentra y quien valida, aparecen en el informe.
- **findings.sarif:** SARIF 2.1.0 mediante `seclib.to_sarif`; los hallazgos rechazados permanecen en el log como `suppressions`. Utilizable directamente como carga de code scanning. Subirlo es una publicación hacia el exterior y requiere una orden de la persona usuaria.

## Antes de entregarlo

Releer el informe: sin valores secretos (el validador solo detecta patrones comunes; contrato 6.4), solo ubicaciones. Los informes en sistemas de tickets y chats, igualmente sin valores. Las vulnerabilidades en repos públicos van por el canal de notificación privado (SECURITY.md), no por un issue público.

## Prueba

`python -m pytest tests -q -p no:cacheprovider` en la carpeta del skill (informe, SARIF, escaneo parcial, evidencia con backticks, caso negativo sin salida).

## Changelog

### 0.1.0 (2026-10-31)

- Primera versión con `render_report.py`: report.md y findings.sarif a partir de datos validados.
