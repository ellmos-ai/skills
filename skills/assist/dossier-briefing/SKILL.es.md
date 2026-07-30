---
name: dossier-briefing
version: 1.0.0
category: assist
description: Genera un informe estructurado de investigación para un tema o persona como una plantilla Markdown (stdout o archivo). Sin almacenamiento persistente.
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: es
---

> **Español** — Versión oficial en español de `dossier-briefing`.


# Dossier-Briefing (Español)

**Informe estructurado de investigación para un tema o persona**

---

## Visión general y propósito

Genera un informe Markdown vacío y estructurado para cualquier sujeto
(persona, empresa, evento, concepto). La plantilla sirve como punto de partida para
investigaciones posteriores con `research-agent` o `web-reading`.

---

## Disparadores

| Frase | Acción |
|---|---|
| "Crear un informe sobre Marie Curie" | Plantilla: persona, type=person |
| "Dossier sobre OpenAI" | Plantilla: empresa, type=organization |
| "Informe sobre computación cuántica" | Plantilla: tema, type=topic |
| "Preparar un informe de investigación sobre la COP30" | Plantilla: evento, type=event |

---

## Flujo de trabajo y procedimiento

1. **Identificar el sujeto:** Extraer el nombre/título del informe a partir de la entrada del usuario.
2. **Detectar el tipo:** person, organization, topic, event (o unspecified).
3. **Generar la plantilla:** Crear el Markdown con todas las secciones relevantes.
4. **Salida:** stdout o opcionalmente escribir en un archivo (`-o file.md`).
5. **Iniciar investigación:** Entregar la plantilla a `research-agent` o `web-reading`
   para completar las secciones faltantes.

---

## CLI

```bash
# Briefing to stdout (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# Write to file (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Topic briefing (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantum computing" --typ topic

# Event (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Without type (generic) (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "My topic"

# Help (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```

---

## Tipos de informe y secciones

| Tipo | Secciones |
|---|---|
| `person` | Datos básicos, biografía/antecedentes, trabajo y contribuciones, fuentes, notas |
| `organization` | Perfil, historia, productos/servicios, personas clave, fuentes, notas |
| `topic` | Visión general, antecedentes/contexto, desarrollos actuales, fuentes clave, preguntas abiertas, notas |
| `event` | Datos clave, participantes, antecedentes/cronología, importancia, fuentes, notas |
| `unspecified` | Visión general, antecedentes, detalles, fuentes, notas |

---

## Almacenamiento

Sin almacenamiento persistente. La plantilla solo se emite como salida (stdout o archivo),
no se guarda en una base de datos.

---

## Actitud y directrices

- Enfatizar siempre que la plantilla está vacía y debe completarse mediante investigación.
- Nunca inventar contenido ni alucinar: solo proporcionar la estructura.
- Preguntar si el tipo no está claro o usar `unspecified`.

---

## Privacidad

Sin acceso a la red. Sin almacenamiento. Procesamiento puramente local.

---

## Recursos relacionados

- `research-agent`: completa la plantilla del informe con los resultados de la investigación
- `web-reading`: lee páginas web y extrae contenido para el informe

---

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 1.0.0 | 2026-06-22 | Creado a partir de dossier_generator.py de BACH v1.0.0; almacenamiento eliminado, generalizado |