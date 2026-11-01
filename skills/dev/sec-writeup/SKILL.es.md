---
name: sec-writeup
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Convierte notas, PoC y hallazgos en un informe de vulnerabilidad autocontenido y revisado con escepticismo para la divulgación coordinada: versiones afectadas, pasos de reproducción, impacto, corrección, cronología. PoC mínimo (sin exploit convertido en arma), secretos redactados, cada afirmación respaldada por evidencia o marcada como no verificada. Disparadores: 'redactar la divulgación', 'informe de vulnerabilidad', 'texto del advisory', 'notificar a quien mantiene el proyecto'. No es para el informe interno de escaneo (sec-report) ni para el ticket (sec-track)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, disclosure, writeup, advisory, reporting]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

<img src="banner.png" width="100%" alt="sec-writeup banner">

# sec-writeup - informe de vulnerabilidad para la divulgación

Un informe legible sin conocimientos previos y reproducible por alguien que no conoce el fallo. Contrato: `sec-scan/references/contract.md` (regla 1 código propio, regla 4 secretos, regla 6 egress, regla 9 informar con fidelidad).

## Procedimiento

1. **Reunir el material en bruto:** hallazgo (`findings.json`), notas, PoC, parche. Solo vulnerabilidades en código propio o expresamente autorizado (regla 1).
2. **Comprobar con escepticismo antes de escribir:** intentar uno mismo refutar cada afirmación central («alcanzable sin autenticación», «ejecución remota de código», «afecta a todas las versiones»). Después marcar cada afirmación como **evidenced** (con evidencia: ubicación en el código, salida de pruebas, commit) o **unverified** (marcada como tal en el texto). La severidad solo en la escala del contrato (§3); una cifra CVSS o un identificador CVE solo si los aporta la persona usuaria - nunca inventarlos.
3. **Determinar las versiones afectadas a partir del historial** (introducción mediante `git log -S`/`git blame`, corrección mediante commit/tag), no estimarlas; indicar como abierto un límite incierto.
4. **Estructurar el informe:** resumen (2-3 frases) · componente y versiones afectados · requisitos previos del atacante · pasos de reproducción · impacto (concreto, no exagerado) · corrección/workaround · cronología · créditos/contacto.
5. **PoC mínimo:** solo lo que necesita quien mantiene para reproducir (entrada + comportamiento erróneo esperado). Sin exploit convertido en arma, sin sistemas objetivo, sin persistencia. En caso de duda, describir en lugar de adjuntar código.
6. **Redactar:** eliminar secretos, nombres de host, rutas internas y datos personales; los hallazgos muestran solo la ubicación, nunca el valor (regla 4). Un secreto expuesto se rota en el proveedor.
7. **Cronología solo con fechas reales** (descubrimiento, notificación, acuse de recibo, corrección). El plazo de divulgación lo fija la persona usuaria o `SECURITY.md` (`sec-policy`), no el skill.
8. **Entrega:** el borrador se queda con la persona usuaria. El envío (correo, advisory, plataforma) tiene efecto hacia el exterior y requiere su aprobación expresa (regla 6); para repos públicos preferir un borrador de advisory o el canal de notificación privado.

## Changelog

### 0.1.0 (2026-10-31)
- Versión inicial.
