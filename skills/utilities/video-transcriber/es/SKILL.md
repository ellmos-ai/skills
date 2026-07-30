---
name: video-transcriber
version: 1.1.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-06-20
description: Obtiene transcripciones (subtítulos) y metadatos de fuentes de video en línea y los emite en Markdown, JSON o texto plano. Actualmente compatible: YouTube. Prefiere subtítulos creados manualmente y recurre a los generados automáticamente.

standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: es
status: active
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

> **Español** — Versión oficial en español de `video-transcriber`.


# Video Transcriber (Español)

Obtiene transcripciones (subtítulos) y metadatos (título, canal, fecha, reproducciones,
descripción) de videos en línea. Prefiere subtítulos creados manualmente y recurre
a los generados automáticamente como alternativa. Salida en Markdown, JSON o texto plano.

Fuente actualmente compatible: **YouTube** (youtube.com, youtu.be, youtube-nocookie.com).

Para videos, utilice esta herramienta en lugar de resumir el contenido manualmente:
la transcripción es la fuente confiable.

> **Aviso:** Esta herramienta no está afiliada, respaldada ni patrocinada por
> YouTube o Google. El uso es bajo la propia responsabilidad del usuario. Los usuarios son únicamente
> responsables de cumplir con los términos de servicio de la plataforma respectiva
> y la ley de derechos de autor aplicable. Sin elusión de DRM, paywalls o restricciones
> de acceso. Sin raspado masivo. Sin redistribución de transcripciones protegidas por derechos
> de autor sin el consentimiento del titular de los derechos.

## Dependencias y licencias

```bash
pip install youtube-transcript-api   # transcripciones (requerido) — licencia MIT
pip install yt-dlp                   # metadatos (opcional, fallback: noembed) — Unlicense (Dominio Público)
```

## Uso

> **Nota sobre Windows:** Establezca siempre `PYTHONIOENCODING=utf-8`, de lo contrario, las diéresis y los
> caracteres especiales se romperán en la salida (codificación cp1252).

```bash
# Predeterminado: Markdown con marcas de tiempo
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Elegir formato de salida
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# Guardar en archivo
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Idiomas preferidos (predeterminado: de en)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### Opciones

| Opción | Efecto |
|--------|--------|
| `--format markdown\|json\|plain` | Formato de salida (predeterminado: markdown) |
| `--output, -o <file>` | Escribir en archivo en lugar de stdout |
| `--lang <codes...>` | Idiomas de subtítulos preferidos (predeterminado: de en) |
| `--meta-only` | Solo metadatos, sin transcripción |
| `--transcript-only` | Solo transcripción, sin metadatos |
| `--no-timestamps` | Transcripción sin marcas de tiempo |
| `--no-meta` | Más rápido: omitir metadatos de yt-dlp |

### Como librería de Python

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)
```

## Casos de uso típicos

- Investigación: hacer que el contenido de video sea citable como texto
- Análisis de fuentes: examinar la argumentación/metáforas en presentaciones
- Resúmenes: transcripción como una base confiable en lugar de alucinación

## Límites

- Solo funciona si el video tiene subtítulos (manuales o automáticos)
- Los subtítulos automáticos pueden contener errores de reconocimiento
- Sin descarga de audio, sin reconocimiento de voz integrado

## Historial de cambios

### 1.1.0 (2026-06-20)
- Renombrado de `yt-transcriber` → `video-transcriber` (Política de marca de YouTube:
  "yt" es una abreviatura explícitamente prohibida; consulte RECHTSCHECK_2026-06-20.md)
- Script: `yt_transcriber.py` → `video_transcriber.py`
- Exención de responsabilidad y licencias de dependencias añadidas (responsabilidad del usuario, ToS, sin respaldo)
- YouTube se menciona descriptivamente solo como una fuente, no como un componente de nombre/marca
- Wrapper de compatibilidad hacia atrás `yt_transcriber.py` retenido en la ruta anterior

### 1.0.0 (2026-06-12)
- SKILL.md añadido (la herramienta ya existía como script + README)
- Script v1.0.0: transcripción + metadatos, 3 formatos de salida, preferencias de idioma
