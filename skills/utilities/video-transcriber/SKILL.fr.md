---
name: video-transcriber
version: 1.2.1
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-11-22
description: "Utilisez cette compétence lorsque des transcriptions, sous-titres ou métadonnées de vidéos en ligne doivent être téléchargés (par ex. 'transcrire vidéo YouTube', 'télécharger sous-titres', /video-transcriber). Extrait sous-titres manuels et automatiques en Markdown, JSON ou texte ; ne PAS utiliser pour la transcription audio locale via Whisper (assist/transkription)."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: fr
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
---

<img src="banner.png" width="100%" alt="video-transcriber banner">

> **Français** — Version française officielle de la compétence `video-transcriber`.

# Video-Transkriber — Transcripteur vidéo

Récupère les transcriptions (sous-titres) et métadonnées (titre, chaîne, date, vues, description) de vidéos en ligne. Privilégie les sous-titres créés manuellement, avec repli sur les sous-titres générés automatiquement. Sortie en Markdown, JSON ou texte brut.

Si la voie principale (`youtube-transcript-api`) ne renvoie rien, une seconde voie via les métadonnées `yt-dlp` prend automatiquement le relais. Elle lit exclusivement la piste de sous-titres que la plateforme fournit déjà pour la lecture — **aucun téléchargement vidéo ou audio**. La voie ayant abouti est indiquée dans le champ `source` de la sortie JSON et sur `stderr`.

Pour chaque langue souhaitée, le repli donne priorité aux pistes manuelles exactes puis de base avant les pistes automatiques exactes puis de base ; toute autre piste ne vient qu'après. Une piste JSON3 illisible n'interrompt pas la récupération tant qu'une autre piste candidate reste disponible.

Source actuellement prise en charge : **YouTube** (`youtube.com`, `youtu.be`, `youtube-nocookie.com`).

Pour les vidéos, utiliser cet outil plutôt que de résumer le contenu manuellement — la transcription constitue la source fiable.

> **Remarque :** Cet outil n'est ni affilié à YouTube ou Google, ni soutenu ou approuvé par eux. L'utilisation s'effectue sous votre propre responsabilité. Les utilisateurs sont eux-mêmes responsables du respect des conditions d'utilisation de chaque plateforme et du droit d'auteur applicable. Aucun contournement de DRM, de paywalls ou de restrictions d'accès ; aucune collecte de données de masse ; aucune republication de transcriptions protégées sans l'accord des ayants droit.

## Dépendances et licences

```bash
pip install youtube-transcript-api   # Transcriptions (obligatoire) — Licence MIT
pip install yt-dlp                   # Métadonnées (optionnel, repli : noembed) — Unlicense (Domaine public)
```

## Utilisation

> **Remarque Windows :** Toujours définir `PYTHONIOENCODING=utf-8`, sinon les accents et caractères spéciaux cassent dans la sortie (encodage cp1252).

```bash
# Par défaut : Markdown avec horodatages
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Choisir le format de sortie
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# Enregistrer dans un fichier
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Préférer des langues (par défaut : de en)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### Options

| Option | Effet |
|--------|-------|
| `--format markdown\|json\|plain` | Format de sortie (par défaut : markdown) |
| `--output, -o <fichier>` | Écrire dans un fichier au lieu de `stdout` |
| `--lang <codes...>` | Langues de sous-titres préférées (par défaut : `de en`) |
| `--meta-only` | Uniquement les métadonnées, sans transcription |
| `--transcript-only` | Uniquement la transcription, sans métadonnées |
| `--no-timestamps` | Transcription sans horodatages |
| `--no-meta` | Plus rapide : ignorer les métadonnées `yt-dlp` |
| `--allow-empty-transcript` | Considérer une transcription vide comme un succès (Exit 0 au lieu de 3) |

### Codes de sortie

Une transcription vide n'est **pas** un succès. Avant la version 1.2.0, ce cas se terminait avec le code 0 : le fichier de sortie était écrit, le tableau de segments était vide, et tout automate appelant considérait l'opération réussie. Cet échec silencieux est précisément le défaut corrigé par la version 1.2.0.

| Code | Signification |
|------|---------------|
| `0` | Succès — transcription présente, ou `--meta-only`, ou `--allow-empty-transcript` |
| `1` | URL ou ID vidéo invalide |
| `2` | Erreur d'appel (attribuée par `argparse`, par ex. option inconnue) |
| `3` | Aucune transcription obtenue — les deux voies sont vides |

Le code `2` reste réservé à `argparse` afin qu'une faute de frappe lors de l'appel demeure distincte d'une vidéo sans sous-titres.

```bash
# Dans des scripts
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o out.md || {
  code=$?
  [ "$code" -eq 3 ] && echo "La vidéo n'a pas de sous-titres" || echo "Erreur : $code"
}
```

### En tant que bibliothèque Python

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)

# Toujours vérifier -- fetch_transcript ne lève pas d'exception, il signale :
if not transcript["segments"]:
    raise RuntimeError(transcript["error"])
print(transcript["source"])  # "youtube_transcript_api" ou "yt-dlp"
```

Les deux voies peuvent être appelées séparément : `fetch_transcript_primary()` (uniquement `youtube-transcript-api`) et `fetch_transcript_ytdlp()` (uniquement la voie de secours). `fetch_transcript()` les enchaîne et garantit les champs `segments`, `language`, `is_generated`, `full_text`, `source` et, en cas d'erreur, `error`.

## Cas d'usage typiques

- Recherche documentaire : exploiter des contenus vidéo sous forme textuelle citable
- Analyse de sources : examiner l'argumentation et les métaphores dans des conférences
- Résumés : utiliser la transcription comme base fiable plutôt que d'halluciner

## Limites

- Ne fonctionne que si la vidéo possède des sous-titres (manuels ou automatiques)
- Les sous-titres automatiques peuvent contenir des erreurs de reconnaissance
- Aucun téléchargement audio, aucune reconnaissance vocale propre — même la voie de secours ne charge que la piste de sous-titres, jamais la vidéo ni l'audio
- La voie de secours nécessite une piste JSON3 ; si la plateforme ne fournit que d'autres formats, l'exécution se termine par le code 3 plutôt que par une sortie partielle

## Journal des modifications

### 1.2.1 (2026-11-22)
- Indication de langue corrigée

### 1.2.0 (2026-08-24)
- **Sémantique de sortie :** Une transcription vide se termine avec le code `3` au lieu de `0` silencieusement. Une URL invalide renvoie désormais `1` via une constante nommée. `--meta-only` reste un succès car aucune transcription n'y est attendue.
- **Nouvelle option `--allow-empty-transcript` :** traite délibérément une transcription vide comme un succès — pour les appelants qui considèrent les sous-titres comme optionnels.
- **Repli sous-titres `yt-dlp` :** s'enclenche dès que la voie principale ne fournit aucun segment (pas seulement en cas d'exception). Utilise `extract_info(download=False)` et ne lit que l'URL des sous-titres — pas de vidéo, pas d'audio, aucun contournement des restrictions d'accès.
- **Sélection de langue durcie :** `de-orig`/`de-DE` sont trouvés pour `--lang de` (correspondance sur la langue de base). Les sous-titres manuels restent prioritaires sur les automatiques.
- **Champ `source`** dans le résultat : `youtube_transcript_api` ou `yt-dlp`.
- Tests de régression : 29 tests avec réponses simulées (UTF-8, les trois formats de sortie, codes de sortie, choix de langue, analyse JSON3).

### 1.1.0 (2026-06-20)
- Renommé de `yt-transcriber` → `video-transcriber` (directive de marque YouTube : « yt » est une abréviation explicitement interdite ; recommandation : `RECHTSCHECK_2026-06-20.md`)
- Script : `yt_transcriber.py` → `video_transcriber.py`
- Ajout de l'avertissement et des licences des dépendances (responsabilité utilisateur, conditions d'utilisation, absence d'approbation officielle)
- YouTube uniquement mentionné comme indication descriptive de source, plus comme élément de nom ou de marque
- Conservation du wrapper de rétrocompatibilité `yt_transcriber.py` à l'ancien emplacement

### 1.0.0 (2026-06-12)
- Ajout de `SKILL.md` (l'outil existait déjà sous forme de script + README)
- Script v1.0.0 : transcription + métadonnées, 3 formats de sortie, préférences de langue
