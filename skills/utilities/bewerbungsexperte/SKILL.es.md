---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: Especialista para todo el proceso de solicitud de empleo. Analiza ofertas de empleo, optimiza perfiles (LinkedIn/CV) y genera cartas de presentación personalizadas. Genera currículums en ASCII a partir de una base de datos SQLite y una estructura de carpetas. cv_generator.py está adaptado como herramienta independiente -- no se requiere BACH-Runtime.
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

> Su socio estratégico para el próximo paso en su carrera.

## ACTIVACIÓN

```bash
# Ejemplo de CV sin acceso a base de datos (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# Generar CV desde base de datos SQLite (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <ruta/a/datos.db>

# Guardar CV en un archivo (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <ruta> --output lebenslauf.txt

# Con escaneo de carpetas (Español)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <ruta> --career-path <carpeta>
```

## CATÁLOGO DE SERVICIOS

### 1. Generación de CV (`cv_generator.py`)
- **Datos personales:** Leer de la tabla `assistant_user_profile` (clave/valor)
- **Experiencia laboral:** Escanear carpetas de empleadores (certificados, contratos)
- **Educación:** Escanear carpetas de títulos
- **Formación continua:** Escanear carpetas de certificados
- **Referencias:** De la tabla `contacts` (category='beruflich')
- **Modo de prueba (Dry-Run):** Sin base de datos -- datos de ejemplo para pruebas

### 2. Diagnóstico de la oferta de empleo
- **Coincidencia de palabras clave:** Cotejo del CV con requisitos del puesto (ATS-Safe)
- **Análisis de empresa:** Investigación sobre cultura corporativa y beneficios

### 3. Servicio de documentación
- **Optimización de CV:** Estructuración y destacado de experiencias
- **Carta de presentación:** Creación de cartas individuales y convincentes
- **Portafolio:** Asesoramiento sobre muestras de trabajo y referencias

## TABLAS DE BASE DE DATOS (opcional)

`cv_generator.py` lee de estas tablas si existen:

- `assistant_user_profile` (key TEXT, value TEXT) — Datos personales
  - Campos: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — Referencias

Las tablas que falten se ignorarán (secciones vacías en el CV).

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
--db <ruta>           Ruta a la base de datos SQLite (obligatorio sin --dry-run)
--output, -o          Archivo de salida (de lo contrario stdout)
--career-path         Ruta a la carpeta de empleadores
--education-path      Ruta a la carpeta de títulos
--certs-path          Ruta a la carpeta de certificados
--dry-run             Ejemplo de CV sin acceso a base de datos
```

## FLUJO DE TRABAJO: GENERACIÓN DE CV

1. **Preparación**
   - Proporcionar base de datos SQLite (base de datos BACH o propia)
   - Crear estructura de carpetas con documentos (opcional)

2. **Prueba sin BD**
   - `python cv_generator.py --dry-run` -- comprueba si la herramienta funciona

3. **Generación**
   - `python cv_generator.py --db <ruta> --career-path <empleador>`
   - Revisar la salida y ajustar según sea necesario

4. **Exportación**
   - `python cv_generator.py --db <ruta> --output lebenslauf.txt`

## DEPENDENCIAS

Solo biblioteca estándar de Python: `sqlite3`, `pathlib`, `argparse`, `re`, `datetime`.
No requiere instalación por pip, ni importación en el tiempo de ejecución de BACH.

## REGISTRO DE CAMBIOS

### 1.1.0 (2026-06-22)
- Adaptado como herramienta independiente desde BACH v1.0.0
- `--db <ruta>` en lugar de ruta de base de datos original prefijada
- Añadido modo `--dry-run`
- Eliminado `--scan-folders` (requería la tabla user_data_folders de BACH)
- Texto de pie de página neutralizado
- Verificada la independencia del tiempo de ejecución de BACH

### 1.0.0 (2026-01-25, interno de BACH)
- Versión inicial en BACH system/agents/_experts/bewerbungsexperte/

---
Estado: ACTIVO
Dominio: Asesoramiento profesional