---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Registro local y privado de datos médicos: diagnósticos, historial de síntomas y planes de examen. Sin origen BACH: diseño personalizado con su propio almacenamiento SQLite. Estrictamente local, sin transferencia a la nube.

standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: es
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
---

> **Español** — Versión oficial en español de `medizin-daten`.


## Descripción general y propósito

Registra de forma segura y local datos médicos personales: diagnósticos (código CIE-10 opcional), historial de síntomas con series de fechas y planes de examen. Todos los datos permanecen exclusivamente locales en `medizin-daten/store.db`.

El skill no reemplaza la consulta médica y no realiza declaraciones médicas; es un cuaderno estructurado para datos personales de salud.

---

## Disparadores (Triggers)

| Frase | Acción |
|---|---|
| "Record a diagnosis" / "Registrar un diagnóstico" | Crear nuevo diagnóstico |
| "Add diagnosis [name]" / "Añadir diagnóstico [nombre]" | Crear diagnóstico con nombre |
| "Symptom history" / "Historial de síntomas" | Registrar síntomas de hoy |
| "Record symptom [name]" / "Registrar síntoma [nombre]" | Registrar un solo síntoma |
| "Examination plan" / "Plan de exámenes" | Mostrar próximas citas/exámenes |
| "Add appointment" / "Añadir cita" | Registrar cita de examen |
| "Show my diagnoses" / "Mostrar mis diagnósticos" | Mostrar lista de diagnósticos |

---

## Flujo de trabajo y procedimiento

1. **Detectar modo**: diagnóstico / síntoma / plan de examen
2. **Estructurar entrada**: fecha, nombre, notas, código CIE-10 opcional
3. **Guardar**: en `store.db` (local, sin acceso a red)
4. **Salida**: resumen legible para el contexto del LLM

---

## Punto de entrada CLI

```bash
# Create diagnosis (Deutsch)
python medizin_daten_core.py add-diagnosis "Hypertension" [--icd I10] [--note "note"]

# List diagnoses (Deutsch)
python medizin_daten_core.py diagnoses

# Record symptom (Deutsch)
python medizin_daten_core.py add-symptom "Headache" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptom history for a name (Deutsch)
python medizin_daten_core.py symptom-history "Headache" [--limit 30]

# Plan examination (Deutsch)
python medizin_daten_core.py add-exam "Blood count" [--date 2026-07-01] [--note "fasting"]

# Upcoming examinations (Deutsch)
python medizin_daten_core.py exams [--upcoming]

# Alternative store (e.g. for tests) (Deutsch)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## Almacenamiento (Store)

| Propiedad | Valor |
|---|---|
| Tipo | SQLite |
| Ruta (por defecto) | `skills/assist/medizin-daten/store.db` |
| Sobrescribir | `--store <ruta>` o var. de entorno `MEDIZIN_STORE` |
| Tablas | `diagnoses`, `symptoms`, `examination_plans` |

### Esquema (Schema)

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (short: 8 hex)
    name        TEXT NOT NULL,        -- name (e.g. "Hypertension")
    icd_code    TEXT,                 -- ICD-10 code optional (e.g. "I10")
    onset_date  TEXT,                 -- onset (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- free-text note
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    name         TEXT NOT NULL,       -- name (e.g. "Headache")
    severity     INTEGER,             -- 1–10 scale (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 timestamp
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: assignment
    exam_name    TEXT NOT NULL,       -- examination name
    planned_date TEXT,                -- planned date (ISO-8601)
    done_date    TEXT,                -- completed on (NULL = pending)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## Enfoque y principios

- Sin recomendaciones médicas ni diagnósticos por parte del skill.
- Los códigos CIE-10 se almacenan como texto libre: sin validación con bases de datos externas.
- La escala de gravedad 1–10 es subjetiva del usuario.
- Siempre se permiten valores faltantes (fecha, gravedad): se aplica el principio de cuaderno de notas.

---

## Privacidad (Privacy Gate)

> **ADVERTENCIA: Los datos médicos son especialmente sensibles.**

- `store.db` contiene datos de salud altamente sensibles: **nunca confirmarlo en Git (commit)**.
- **Sin acceso a la red**: todas las operaciones se ejecutan de forma totalmente local.
- **Sin compartir** con servicios externos, sin sincronización con backends en la nube.
- Recomendación de copia de seguridad: copia de seguridad local cifrada (p. ej., `age`/`gpg`).
- El skill comprueba al iniciarse si `store.db` está fuera del sistema de archivos local y emite una advertencia si la ruta está en una carpeta de sincronización (OneDrive, etc.).
- `~/.gitignore_global` o el `.gitignore` local deben excluir `store.db`.

---

## Recursos relacionados

- Skill `assist/gesundheit`: asistencia médica general (no datos médicos)
- MediPlaner (`tools/module-installer` → `mediplaner`): gestión de medicamentos (programa independiente)

---

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-06-22 | Creación inicial: diseño personalizado, puerta de privacidad, esquema de 3 tablas |