---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: Transcribe archivos de audio/video a texto. Utiliza Whisper (openai-whisper) o Vosk (offline) como backend opcional; ambos se detectan mediante comprobación de presencia. Sin backend: modo marcador de posición con salida simulada (dry-run).
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: es
status: stable
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
---

> **Español** — Versión oficial en español de `transkription`.


## Descripción general y propósito

Convierte archivos de audio/video a texto, localmente y sin acceso obligatorio a la nube. El skill detecta automáticamente si Whisper o Vosk están instalados y selecciona el mejor backend disponible. Sin un backend, se ejecuta en modo de prueba (dry-run) y devuelve un texto de reemplazo, por lo que el flujo de trabajo siempre funciona.

Las transcripciones se almacenan localmente en `transkription/store.db` y se pueden consultar.

---

## Activadores

| Frase | Acción |
|---|---|
| "Transcribe this audio" | Transcribir archivo de audio |
| "Transcribe [file]" | Transcribir archivo especificado |
| "Show my transcripts" | Listar las últimas transcripciones |
| "Search transcript [term]" | Búsqueda de texto completo en transcripciones |
| "Export transcript [ID]" | Exportar transcripción como TXT |

---

## Flujo de trabajo y procedimiento

1. **Comprobación de backend**: Verificar si `whisper` o `vosk` se pueden importar.
2. **Comprobación de archivo**: El archivo de entrada debe existir (audio: wav, mp3, m4a, ogg, flac; video: mp4, mkv, webm — extracción a través de ffmpeg).
3. **Transcripción**: Llamar al backend y obtener el texto sin formato.
4. **Guardar**: Almacenar el resultado con metadatos (archivo, duración, idioma, backend, marca de tiempo) en `store.db`.
5. **Salida**: Devolver texto; opcionalmente exportar como `.txt`.

---

## Punto de entrada CLI

```bash
# Transcribe file (Deutsch)
python transkription_core.py transcribe audio.wav

# With explicit language (Deutsch)
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-run (no backend required) (Deutsch)
python transkription_core.py transcribe audio.wav --dry-run

# List transcripts (Deutsch)
python transkription_core.py list [--limit 20]

# Full-text search (Deutsch)
python transkription_core.py search "term"

# Export (Deutsch)
python transkription_core.py export <id> [--out file.txt]

# Backend check (Deutsch)
python transkription_core.py check

# Alternative store path (e.g. for tests) (Deutsch)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## Almacenamiento

| Propiedad | Valor |
|---|---|
| Tipo | SQLite |
| Ruta (predeterminada) | `skills/assist/transkription/store.db` |
| Sobrescribir | `--store <path>` o variable de entorno `TRANSKRIPTION_STORE` |
| Tablas | `transcripts` |

### Esquema `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (short: 8 hex)
    file_path   TEXT NOT NULL,     -- original path of audio file
    file_name   TEXT NOT NULL,     -- filename (without path, for display)
    text        TEXT NOT NULL,     -- transcribed text
    language    TEXT,              -- language (e.g. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- duration in seconds (if known)
    created_at  TEXT NOT NULL,     -- ISO-8601 timestamp
    tags        TEXT               -- comma-separated tags (optional)
);
```

---

## Comportamiento y principios

- Sin un backend instalado, el skill funciona en modo dry-run (texto de demostración).
- Se prefiere Whisper sobre Vosk (mejor calidad en alemán).
- La elección entre Whisper y Vosk se puede configurar mediante `assist/prefs.json` (`transkription_backend: "whisper"|"vosk"|"auto"`).
- ffmpeg para la extracción de video se requiere por separado y no está incluido en el skill.

---

## Privacidad

- **Todas las transcripciones permanecen locales**: sin transferencia a la nube sin el modo en línea de Whisper.
- Whisper se puede usar localmente (modelo tiny/base/medium) o mediante la API de OpenAI. Por defecto se utiliza el modelo local.
- `store.db` puede contener contenido confidencial de conversaciones — **no confirmar en Git**.
- Recomendación: añadir `store.db` a `.gitignore`.

---

## Recursos relacionados

- BACH `hub/_services/voice/voice_stt.py` — patrón de backend (inspiración, solo lectura)
- Skill `utilities/yt-transcriber` — transcripción de YouTube (skill independiente, no es un duplicado: específico para YT)
- `tools/module-installer/module_installer.py` — el registro contiene whisper + vosk

---

## Historial de cambios

| Versión | Fecha | Cambio |
|---|---|---|
| 0.1.0 | 2026-06-22 | Creación inicial — almacenamiento SQLite propio, comprobación de presencia de Whisper/Vosk |