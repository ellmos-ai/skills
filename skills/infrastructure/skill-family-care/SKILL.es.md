---
name: skill-family-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Habilidad de mantenimiento que mantiene actualizadas las familias de habilidades sin ejecutar la auditoría
  completa de skill-explorer. Utiliza esta habilidad cuando asignes una nueva habilidad a la familia correcta,
  actualices un enrutador de encabezado de familia tras un cambio o elimines un enrutador huérfano. Activar
  también ante solicitudes de "mantener familias", "asignar nueva habilidad a una familia", "actualizar enrutador",
  "establecer/eliminar encabezado de familia".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, familien, pflege, routing, meta]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-family-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-family-care banner">
# Mantenimiento de Familias de Habilidades (Skill-Family-Care)

## Propósito

Mantiene actualizadas las **familias** de habilidades — sin ejecutar el ciclo completo de auditoría de `skill-explorer`. Diseñado según el principio de instalador (sub-habilidad ligera en lugar de un monolito). Hace referencia a los scripts de `skill-explorer` sin duplicarlos.

## Fuentes (no duplicar)

- **Lista de familias:** `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (mapa canónico de familias y enrutamiento).
- **Inventario (estado actual):** `skill-explorer/scripts/inventory_skills.py`.
- **Establecer/Eliminar enrutador:** `skill-explorer/scripts/inject_family_header.py`.
- **Configuración (familias enlazadas):** `~/.claude/skills/skill-explorer/config.json`.

## Tareas

### A — Asignar una nueva habilidad a una familia
1. Obtener de nuevo el inventario:
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
2. Elegir la familia adecuada de `SKILL-MAP.md` (Ejes: Fase/Amplitud/Rigidez/Impacto/Materia prima).
3. Registrar la habilidad como miembro en `config.json` (`families[<fam>].members`) y en `SKILL-MAP.md`.

### B — Actualizar el enrutador de encabezado tras un cambio de familia
```bash
PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inject_family_header.py \
    --family <Familie> --skills s1,s2,s3 --router "<Wegweiser>" --inventory ~/.skill-inventory.json
```
- Idempotente: se reemplaza cualquier bloque existente de la misma familia.
- Solo se modifican las habilidades de tipo `editable`/`source=user` (bloqueo de seguridad dentro del script).

### C — Eliminar enrutador huérfano
Mismo script con `--remove` (sin necesidad de `--router`).

## Reglas estrictas

- **Inspección ≠ Mutación:** solo las habilidades del usuario reciben encabezados. Nunca modificar habilidades de plugins o externas.
- Después de cada cambio, actualizar `config.json` (`families[*].linked`, `updated`).
- No copiar contenidos del mapa de familias en las habilidades individuales; solo inyectar el bloque de señalización.

## Registro de cambios

### 0.1.0 (2026-06-17)
- Versión inicial. Creada por el modo de auditoría (P1).
