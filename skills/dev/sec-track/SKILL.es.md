---
name: sec-track
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-10-31
updated: 2026-10-31
description: "Hace trazables los hallazgos de seguridad validados: tras vista previa y confirmación crea un ticket (ticket_writer.py), un issue de GitHub o un borrador de security advisory (gh), comprueba antes duplicados por id de hallazgo, mantiene los secretos fuera del texto y escribe la referencia de vuelta en finding.ticket. Disparadores: 'hacer seguimiento de este hallazgo', 'ticket para SEC-...', 'crear un advisory', 'poner los hallazgos en el backlog'. Sin Linear/Jira. No es para informes técnicos (sec-report) ni para la divulgación hacia el exterior (sec-writeup)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: dev
tags: [security, tickets, tracking, github, advisory]
language: es
status: draft
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'custom', 'origin_path': null, 'origin_version': null, 'origin_repo': null, 'last_sync_from_origin': null, 'last_sync_to_origin': null, 'local_changes_since_sync': false}
---

# sec-track - hacer trazables los hallazgos

La fase «track». Contrato: `sec-scan/references/contract.md` (regla 4 secretos, regla 8 tickets en §6; campo `ticket` en §2/esquema). Solo hallazgos con estado `validated` o posterior - `candidate` no se rastrea.

## Elegir el destino

| Destino | Cuándo | Herramienta |
|---|---|---|
| Ticket en el sistema de tickets de la persona usuaria | por defecto, privado, sin efecto hacia el exterior | `ticket_writer.py` de ticket-master |
| Issue de GitHub | solo repos **privados** o simples brechas de hardening sin ruta de explotación | `gh issue create` |
| Borrador de security advisory | vulnerabilidad en un repo **público** | `gh api` (repository security advisories, borrador) |

**Repo público + hallazgo explotable: nunca un issue público** - eso sería una divulgación (egress, regla 6). Allí usar un borrador de advisory o un ticket privado. Sin Linear, sin Jira.

## Procedimiento

1. **Seleccionar:** qué hallazgos, qué destino. Uno por uno, no como ticket masivo, para que cada id tenga su propia referencia.
2. **Comprobación de duplicados por id de hallazgo** (`SEC-<12 hex>`): ¿está ya establecido `finding.ticket`? Buscar el id en los directorios de tickets; en GitHub `gh issue list --state all --search "<id>"`. Si hay coincidencia, usar la referencia existente y no crear nada nuevo.
3. **Redactar el texto:** id, título, regla/CWE, severidad, ubicación (`path:line`), impacto breve, recomendación, indicación del archivo de parche si lo hay. **Nunca un valor secreto** (regla 4): solo la ubicación. Sin más detalle de exploit que el necesario.
4. **Mostrar una vista previa y esperar confirmación.** Solo entonces crear - los tickets, issues y advisories tienen efecto hacia el exterior o no se pueden retirar.
5. **Crear:**
   - Ticket (nunca elegir IDs a mano, regla 8): `python <ticket-master>/lib/ticket_writer.py --title "<SEC-id> <título>" --body "<texto>" --project <proyecto> --priority <nivel>`; la CLI imprime la ruta del archivo de ticket creado. La documentación del módulo dice a veces `--urgency`; la CLI en sí conoce `--priority` - leer `--help` antes de usarla.
   - Issue: `gh issue create --repo <owner/repo> --title ... --body-file <archivo>`.
   - Advisory: borrador mediante la interfaz REST de GitHub para repository security advisories (`gh api`); comprobar los campos exactos en la documentación de GitHub antes de usarlo (abierto, aquí no está fijado). Dejarlo como borrador, no publicarlo.
6. **Escribir la referencia de vuelta:** `finding.ticket` = ruta/id del ticket, `owner/repo#nr` o enlace del advisory; después `python scripts/secfind.py validate findings.json coverage.json` (script en `sec-scan`).

## Changelog

### 0.1.0 (2026-10-31)
- Versión inicial.
