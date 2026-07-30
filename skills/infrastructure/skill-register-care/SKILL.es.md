---
name: skill-register-care
version: 0.1.0
type: skill
author: Lukas Geiger + Claude
created: 2026-06-17
updated: 2026-07-30
description: >
  Habilidad de mantenimiento que mantiene consistente el registro de habilidades compuesto por tres partes
  (catálogos code-skill-index, índice de habilidades, mapa de familias/enrutamiento SKILL-MAP). Utiliza esta
  habilidad para una verificación de desvío entre el inventario real y el registro documentado: notificar entradas
  faltantes o sobrantes, corregir recuentos, establecer fecha de actualización. Activar también ante solicitudes de
  "mantener registro de habilidades", "actualizar índice", "verificar desvío de registro", "¿qué habilidades faltan en el mapa?".

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false

category: infrastructure
tags: [skills, register, index, drift, pflege, meta]
language: es
status: active

dependencies:
  tools: []
  services: []
  protocols: [skill-explorer, code-skill-index]
  python: []

provenance:
  origin: "custom"
  origin_path: "~/.claude/skills/skill-register-care/"
  origin_version: "0.1.0"
---

<img src="banner.png" width="100%" alt="skill-register-care banner">
# Mantenimiento del Registro de Habilidades (Skill-Register-Care)

## Propósito

Mantiene el **registro** libre de desviaciones. El registro consta de tres artefactos interconectados — nunca crear un cuarto, siempre ampliar estos tres:

- `~/.claude/skills/code-skill-index/references/catalog-*.md` (catálogos de categoría)
- el índice de habilidades (lista maestra)
- `<USER_HOME>\OneDrive\.USR\SKILL-MAP.md` (mapa de familias y enrutamiento)

## Procedimiento de verificación de desvío (Drift-Check)

1. **Obtener estado actual:**
   ```bash
   PYTHONIOENCODING=utf-8 python ~/.claude/skills/skill-explorer/scripts/inventory_skills.py \
       --out ~/.skill-inventory.json --pretty
   ```
   Solo las habilidades con `source=user` son relevantes para el registro (las de plugins/externas quedan fuera).
2. **Leer estado objetivo:** los tres artefactos del registro.
3. **Calcular la diferencia:**
   - **Faltante** (en inventario, no en el registro) → agregar.
   - **Huérfana** (en el registro, ya no en inventario) → marcar/eliminar.
   - **Discrepancia en recuento** (p. ej., "18 habilidades" ya no es correcto) → corregir la cifra.
4. **Agregar entradas:** por cada nueva habilidad, una línea en el `catalog-<kategorie>.md` correspondiente, una línea en el índice de habilidades (+ fecha en encabezado) y —si hay una familia nueva o modificada— una sección en `SKILL-MAP.md`.
5. **Establecer la fecha de actualización** en todos los archivos modificados con la fecha actual.

## Snippet de ayuda (listar habilidades de usuario faltantes)

```bash
PYTHONIOENCODING=utf-8 python -c "
import json
inv=json.load(open('<USER_HOME>/.skill-inventory.json',encoding='utf-8'))
print('\n'.join(s['dir'] for s in inv['skills'] if s['source']=='user'))
"
```
Cotejar la salida con los artefactos del registro (manualmente o mediante grep).

## Reglas estrictas

- **No crear un cuarto registro** — ampliar únicamente estos tres.
- Solo las habilidades creadas por el usuario pertenecen al registro; las de terceros siguen la ruta externa.
- No adivinar fechas — establecer la fecha actual.

## Registro de cambios

### 0.1.0 (2026-06-17)
- Versión inicial. Creada por el modo de auditoría (P2). Motivo: en la auditoría del 2026-06-17 faltaban ~10 habilidades del usuario en la SKILL-MAP (swarm-operations, model-strategy, agents-bridge, mcp-config-sync, system-onboarding, update-cli-docs, migrate-rename, plugin-system + familias de terapia y desarrollo de juegos).
