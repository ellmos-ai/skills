---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "Compose une musique de fond synchronisée avec la vidéo à partir d'un JSON de scénario, par synthèse de forme d'onde locale (numpy + ffmpeg). Styles : Chiptune, Ambient, Electronic. Déterministe, hors ligne, sans service cloud."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: fr
status: stable
visibility: public
dependencies:
  tools: [ffmpeg]
  services: []
  protocols: []
  python: [numpy]
provenance:
  origin: local-reconstruction
  origin_license: MIT
  notes: >
    Verfahren rekonstruiert aus einem video-synchronisierten Score, komponiert
    für ein 179,5-s-Erklärvideo (5 Musikabschnitte aus 7 Story-Akten
    gemappt). Kanonische Engine: ai-media-editor-Repo, tools/compose_music.py
    (github.com/ellmos-ai/ai-media-editor). Eine eigenständige Kopie liegt
    hier für Offline-Nutzung bei.
translated_from_sha256: 4920ef9c05d0ed853c0ddf7723ca56bac953af15b025feb2f32bdbc8c446fc23
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Scénario → Partition

Compose une partition de fond qui suit l'arc dramatique d'une vidéo, entièrement en local : synthèse de forme d'onde avec numpy (oscillateurs, ADSR, superposition de couches, réverbération par délai) + ffmpeg pour l'encodage MP3. Aucun échantillon, aucun matériel MIDI, aucune API cloud.

## Quand l'utiliser

- Une vidéo ou un podcast a besoin d'une musique de fond dont les moments clés coïncident exactement avec des horodatages (ouverture, creux de tension, section dynamique (driving), apogée, outro).
- Une partition déterministe et re-rendable est nécessaire (même graine → même audio).
- Les styles chiptune, ambient ou electronic sont acceptables.

## Quand NE PAS l'utiliser (limites honnêtes de genre)

La synthèse de forme d'onde peut fournir des lits de fond **chiptune, ambient et electronic**. Avec son synthétiseur intégré, elle ne peut **pas** fournir de pop, de rock, de musique classique ou de musique de film orchestrale — mais l'arrangement est indépendant du moteur sonore : voir « Au-delà de la synthèse de forme d'onde » ci-dessous pour rendre la même composition via des SoundFonts, des bibliothèques orchestrales ou une génération externe.

## La méthode : Scénario → Partition

Reconstruite comme dans la partition de référence (179,5 s, do mineur) :

1. **Associer les actes du scénario à des sections musicales.** Les actes qui partagent un état émotionnel fusionnent en une seule section (référence : 7 actes → 5 sections ; les actes 1 à 3 formaient une seule ouverture calme de 62 s). Chaque section reçoit un `start`/`end` exact en secondes.
2. **Attribuer émotion et intensité à chaque section.**
   - *L'émotion* choisit la progression d'accords (degrés de gamme, exemple mineur) : `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III · `driving` i–VII–VI–V · `epic` iv–V–VI–i (le V est majeur (mineur harmonique)).
   - *L'intensité* (0–1) pilote la sensation de tempo (BPM), le nombre de couches et la montée de volume. Les couches entrent à certains seuils : pads toujours → cloches éparses (<0,3) → arpège (≥0,25) → basse (≥0,4) → lead (≥0,45) → batterie (≥0,5) → extras drive (≥0,65) → doublement d'octave des pads (≥0,85).
3. **Placer les événements spéciaux sur la chronologie.**
   - `damp` : atténuation gaussienne du volume — `1 - depth · exp(-((t-T)²)/(2σ²))`. Référence : profondeur 0,5, σ 1 s à T=84 s, sur le temps fort parlé « Two databases. Same cluster. » (~1:24).
   - `climax` : fenêtre temporelle forçant la superposition complète, le volume de crête et les pads doublés en octave (référence : 154–170 s = 2:34–2:50, au moment de la transition 2D→3D).
   - `outro` : à partir de son début, batterie/basse/lead disparaissent et les cloches descendent à 20 % (référence : 170–179,5 s, carte générique de fin).
4. **Assembler.** Lissage en cosinus surélevé aux frontières de section (~2,5 s), fondu d'entrée/sortie global, réverbération à délai avec rétroaction (100 ms, decay 0,25), drive tanh + normalisation de crête à un niveau de fond (masterisation de référence mesurée : moyenne ≈ −22 dB, max ≈ −1,6 dB).
5. **Rester sous la voix off.** Les sections marquées « background » plafonnent leur montée de volume ; la partition est un lit, non une mélodie principale.

## Utilisation

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Sorties : `score.wav` (stéréo 16 bits 44,1 kHz), `score.mp3` (192k, nécessite ffmpeg dans le PATH ; sinon ignoré avec avertissement), `score.notes.json` (le journal d'arrangement/de notes : chaque note placée avec temps, couche, hauteur MIDI, durée, vélocité) et `score.mid` — un véritable **fichier MIDI standard** (type 1 : piste de tempo avec un événement de tempo par section, piste de notes avec indications de programme GM par style, batterie sur le canal GM 10). Écrit sans dépendance ; pretty_midi/mido non nécessaires.

Déterminisme : même scénario + même `seed` → WAV identique octet par octet.

## Référence du JSON de scénario

```json
{
  "title": "my-score",
  "duration": 179.5,
  "bpm": 100,
  "key": "C",
  "mode": "minor",
  "style": "chiptune",
  "seed": 42,
  "fade_in": 3.0,
  "fade_out": 5.0,
  "crossfade": 2.5,
  "peak": 0.85,
  "drive": 2.0,
  "reverb": {"delay_ms": 100, "decay": 0.25},
  "sections": [
    {"start": 0.0, "end": 62.0, "emotion": "calm", "intensity": 0.18, "bpm": 60,
     "comment": "optional note"},
    {"start": 62.0, "end": 88.0, "emotion": "tense", "intensity": 0.4, "bpm": 72}
  ],
  "events": [
    {"type": "damp", "time": 84.0, "depth": 0.5, "width": 1.0},
    {"type": "climax", "start": 154.0, "end": 170.0},
    {"type": "outro", "start": 170.0}
  ]
}
```

- `duration` (obligatoire, secondes), `sections` (obligatoire, ≥1, trié, sans chevauchement, dans la durée).
- Champs de section : `start`, `end` (obligatoires) ; `emotion` ∈ calm | tense | alive | driving | epic | outro ; `intensity` 0–1 (défaut selon l'émotion) ; `bpm` (défaut : `bpm` global) ; `melody` (liste MIDI optionnelle, cyclique ; sinon une marche aléatoire initialisée par graine (seed) sur les degrés de gamme est générée).
- `key` : nom de note (C, C#, Db, …), `mode` : minor | major.
- `style` : chiptune | ambient | electronic (voir ci-dessous).
- Événement `damp` : `time` (s), `depth` 0–1, `width` = σ en secondes.
- Valeurs par défaut des fondus/fondus enchaînés/crête/drive/réverbération comme indiqué ci-dessus ; tous optionnels.

Exemple complet calculé (la reconstruction de la vidéo de référence) : [`example-storyline.json`](example-storyline.json) — rend une partition de 179,5 s correspondant au niveau master de l'original (moyenne ≈ −22 dB, max ≈ −1,6 dB).

## Préréglages de style

| Style | Lead | Basse/Arpège | Batterie | Caractère |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | basse triangle, arpèges square rapides | Kick/Hat/Snare à base de bruit | Console rétro, guidé par l'arpège (le style de référence) |
| `ambient` | triangle/sine doux | arpèges lents, pads à attaque longue | seulement à intensité ≥ 0,75 | épuré, centré sur les cloches, sensation de réverbération large |
| `electronic` | sawtooth + detune + sub | basse puissante, arpèges saw | kit complet | lit entraînant proche de l'EDM |

## Au-delà de la synthèse de forme d'onde : meilleurs moteurs sonores

Le plafond de genre mentionné concerne le **moteur sonore, non la composition**. La méthode Scénario→Partition produit un arrangement indépendant du moteur ; le synthétiseur numpy fourni n'est que le moteur hors ligne gratuit par défaut. Chaque exécution écrit en plus un fichier MIDI standard (`<out>.mid`) — à rendre avec de meilleurs instruments :

- **Voie A — SoundFont (recommandée : locale, gratuite, sans cloud).** Installer FluidSynth (fluidsynth.org, Windows : `winget install FluidSynth`) plus un SoundFont GM gratuit (GeneralUser GS de S. Christian Collins, ou MuseScore_General.sf2). Puis : `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3 via ffmpeg. Cela débloque les sons de groupe pop/rock, le piano et des cordes simples.
- **Voie B — Orchestre/film.** Bibliothèques orchestrales gratuites : VSCO 2 Community Edition, Soni Musicae, Salamander Grand Piano. Meilleures cordes/cuivres, plus épiques. Remarque honnête : l'articulation et l'humanisation (variation de vélocité, legato, courbes de dynamique) comptent plus que le jeu d'échantillons — et une véritable épopée de film exige en plus une maturité d'arrangement ; un seul moteur ne suffit pas.
- **Voie C — génération IA externe (Suno, etc.).** Possible, mais soulève des questions de confidentialité/droits — uniquement avec l'accord explicite de l'utilisateur, jamais par défaut.

Prévu mais **pas encore implémenté** : une option `humanize` dans le moteur (gigue de vélocité/timing par note), afin que le rendu par échantillons ne sonne pas mécanique (marqué TODO dans la docstring du moteur).

## Limites

- Les commentaires de scénario en anglais et en allemand ne posent pas de problème ; les clés/valeurs sont fixes en anglais.
- Les durées très courtes (< ~10 s) fonctionnent mais compriment la dramaturgie (les fondus et fondus enchaînés sont automatiquement plafonnés à 20 % de la durée / 50 % de la section la plus courte).
- Le journal de notes (`*.notes.json`) est le jeu de données adapté à l'analyse ; le fichier `*.mid` est le format d'échange pour DAW/moteurs SoundFont (les numéros de programme GM sont des indications de style grossières — à remapper selon le goût).
