---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: Especialista para todo el proceso de solicitud de empleo. Analiza ofertas de trabajo, optimiza perfiles (LinkedIn/CV) y genera cartas de presentación personalizadas. Genera CVs en ASCII a partir de una base de datos SQLite y una estructura de carpetas. cv_generator.py está adaptado de forma independiente -- no requiere la ejecución de BACH.
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: es
status: active
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `bewerbungsexperte`.


<img src="banner.png" width="100%" alt="bewerbungsexperte banner">
# BEWERBUNGSEXPERTE v1.1 (Español)

> Tu socio estratégico para el siguiente paso en tu carrera.

## ACTIVACIÓN

```bash
# Ejemplo de CV sin acceso a base de datos (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# Generar CV desde base de datos SQLite (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# Guardar CV en un archivo (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# Con escaneo de carpetas (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```

## CATÁLOGO DE SERVICIOS

### 1. Generación de CV (`cv_generator.py`)
- **Datos personales:** Lectura desde la tabla `assistant_user_profile` (clave/valor)
- **Experiencia laboral:** Escaneo de la carpeta del empleador (certificados, contratos)
- **Educación:** Escaneo de la carpeta de títulos/titulaciones
- **Formación continua:** Escaneo de la carpeta de certificados
- **Referencias:** Desde la tabla `contacts` (category='beruflich')
- **Modo de prueba (Dry-Run):** Sin base de datos -- datos de ejemplo para pruebas

### 2. Diagnóstico de la oferta de trabajo
- **Coincidencia de palabras clave (Keyword-Matching):** Comparación del CV con los requisitos del puesto (compatible con ATS)
- **Análisis de la empresa:** Investigación sobre cultura empresarial y beneficios

### 3. Servicio de documentos de solicitud
- **Optimización de CV:** Estructuración y destacado de experiencias
- **Carta de presentación:** Creación de cartas personalizadas y convincentes
- **Portafolio:** Asesoramiento sobre muestras de trabajo y referencias

## TABLAS DE BASE DE DATOS (opcional)

`cv_generator.py` lee de estas tablas si están presentes:

- `assistant_user_profile` (key TEXT, value TEXT) — Datos personales
  - Campos: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — Referencias

Las tablas faltantes se ignoran (secciones vacías en el CV).

## ESTRUCTURA DE CARPETAS (para --career-path etc.)

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```

## OPCIONES DE CLI

```
--db <pfad>           Ruta a la base de datos SQLite (obligatorio sin --dry-run)
--output, -o          Archivo de salida (de lo contrario stdout)
--career-path         Ruta a la carpeta del empleador
--education-path      Ruta a la carpeta de títulos/estudios
--certs-path          Ruta a la carpeta de certificados
--dry-run             CV de ejemplo sin acceso a la base de datos
```

## FLUJO DE TRABAJO: GENERACIÓN DE CV

1. **Preparación**
   - Proporcionar base de datos SQLite (BD de BACH o propia)
   - Crear estructura de carpetas con documentos (opcional)

2. **Prueba sin BD**
   - `python cv_generator.py --dry-run` -- comprueba si la herramienta funciona

3. **Generación**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - Revisar la salida y ajustar si es necesario

4. **Exportación**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## DEPENDENCIAS

Solo biblioteca estándar de Python (Stdlib): `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
No requiere instalación por pip, sin importación del entorno de ejecución de BACH.

## REGISTRO DE CAMBIOS

### 1.1.0 (2026-06-22)
- Adaptado de forma independiente desde BACH v1.0.0
- `--db <pfad>` en lugar de la ruta a la BD de origen hardcodeada
- Añadido el modo `--dry-run`
- Eliminado `--scan-folders` (requería la tabla user_data_folders de BACH)
- Texto del pie de página neutralizado
- Verificada la independencia del entorno de ejecución de BACH

### 1.0.0 (2026-01-25, BACH interno)
- Versión inicial en BACH system/agents/_experts/bewerbungsexperte/

---
Estado: ACTIVO
Dominio: Asesoría profesional
