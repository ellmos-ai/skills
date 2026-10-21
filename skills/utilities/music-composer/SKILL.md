---
name: music-composer
version: 1.1.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-10-18
description: >
  Komponiert video-synchronisierte Hintergrundmusik per lokaler Synthese
  (numpy + scipy, ffmpeg optional). Empfohlen: der Partitur-Modus
  (handgeschriebene Partitur auf der Sprachzeitachse, feste Pegelstufen ohne
  Ducking, Neuheitsbeleg gegen Vorgängerstücke). Daneben der schnelle
  Storyline-Modus als Skizze (Chiptune, Ambient, Electronic). Deterministisch,
  offline, keine Samples, kein Cloud-Dienst.
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, partitur, chiptune, ambient, electronic, video-sync, waveform-synthesis, fm-synthesis, loudness]
language: de
status: stable
visibility: public
dependencies:
  tools: [ffmpeg]
  services: []
  protocols: []
  python: [numpy, scipy]
provenance:
  origin: local-reconstruction
  origin_license: MIT
  notes: >
    Storyline-Modus: Verfahren rekonstruiert aus einem video-synchronisierten
    Score, komponiert für ein 179,5-s-Erklärvideo (5 Musikabschnitte aus 7
    Story-Akten gemappt). Kanonische Engine: ai-media-editor-Repo,
    tools/compose_music.py (github.com/ellmos-ai/ai-media-editor). Eine
    eigenständige Kopie liegt hier für Offline-Nutzung bei. Partitur-Modus
    (score/): aus der Vertonung eines Demovideos verallgemeinert (handgeschriebene
    Partitur, eigene Synthese, Pegelstufen aus der Messung); Projektdaten wurden
    entfernt, Beispiel-Sprachkarte und Beispielpartitur sind neutral.
---

<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Partitur → Score (empfohlen) und Storyline → Score (Skizze)

Komponiert Hintergrundmusik für Video oder Podcast, vollständig lokal: eigene
Synthese mit numpy/scipy (FM-Blech, Modal-Marimba/-Glockenspiel,
Karplus-Strong-Pizzicato, Chip-Wellen, Perkussion, synthetischer Hall), keine
Samples, keine MIDI-Hardware, keine Cloud-API. Zwei Modi:

| | Partitur-Modus (`score/`) | Storyline-Modus (`compose_music.py`) |
|---|---|---|
| Rolle | **Empfohlen für Videomusik** | Schneller Skizzenmodus |
| Eingabe | Sprachkarte (JSON) + handgeschriebene Partitur (Python) | Storyline-JSON (Abschnitte, Emotion, Intensität) |
| Aufbau | Akkorde je Takt, ausgeschriebene Melodiephrasen, Begleitfiguren je Szene | Schablone: Akkordfolge je Emotion, Vier-Ton-Figuren aus geseedetem Random Walk |
| Zeitachse | Die Stimme: Szenenschnitt = Abschnittswechsel = Takt-Eins | Zeitstempel der Abschnitte |
| Pegel | Feste Stufe je Sprechfenster und Pause, aus der Messung abgeleitet, kein Ducking | Lautstärkerampe je Abschnitt, Peak-Normalisierung |
| Abhängigkeiten | numpy, scipy (ffmpeg nur als optionale Gegenprobe) | numpy (ffmpeg nur für MP3) |
| Grenze | Die Partitur muss geschrieben werden | Gleiche Schablone → über Projekte hinweg klingt es wie derselbe Song (siehe „Storyline-Modus") |

## Wann nutzen

- **Partitur-Modus:** Videomusik, die als eigenständiges Stück wahrgenommen
  werden soll: Melodie in den Sprechpausen, Begleitung unter der Stimme,
  Pegel nach Vorgabe, Variantenvergleich mit Belegen.
- **Storyline-Modus:** Ein schneller, deterministischer Score-Entwurf, der
  Story-Beats auf Zeitstempeln trifft (Opening, Spannungstal, Drive-Abschnitt,
  Klimax, Outro); Chiptune-, Ambient- oder Electronic-Stile sind akzeptabel.

## Wann NICHT nutzen (ehrliche Genre-Grenzen)

Waveform-Synthese kann **Chiptune-, Ambient- und Electronic**-Hintergrundbetten
liefern, im Partitur-Modus zusätzlich Blechmarsch sowie Marimba-, Flöten- und
Glockenspiel-Stücke. Mit dem eingebauten Synth gibt es **kein Pop, Rock, Klassik
oder Orchester-Filmmusik** — aber das Arrangement ist Backend-neutral: siehe
„Jenseits der Waveform-Synthese" unten.

# Partitur-Modus (empfohlen)

Eine echte, durchkomponierte Partitur statt einer Schablone: Der Agent schreibt
Akkorde je Takt und die Melodiephrasen von Hand (Python-Daten), `score/`
setzt sie in Noten, Audio, MIDI und Pegelmessung um.

## Ablauf

Alle Pfade relativ zu diesem Skill-Ordner.

```bash
# 1. Sprachkarte aus Narrationsclips bauen (oder von Hand schreiben, Schema unten)
python score/timeline.py --timeline timeline.json --narration-dir clips/ -o speech-map.json [--extend-last-scene 2.0]

# 2. Taktraster / Spotting-Sheet: Takte je Szene, Startzeit, Sprache (#) und Pause (.) je Schlag
python score/grid.py --speech-map speech-map.json --bpm 116 --beats-per-bar 2

# 3. Partitur schreiben (Vorlage: score/examples/march.py), in Sekunden prüfen - schreibt nichts
python score/build.py --speech-map speech-map.json --variant my_score.py --check

# 4. Bauen; Zielordner muss neu oder leer sein, sonst Abbruch
python score/build.py --speech-map speech-map.json --variant my_score.py --out out/v1 \
    --narration-dir clips/ --compare earlier/notes.json other.notes.json

# 5. Prüfen: Formate/Länge/MIDI, Pianoroll + Spektrogramm als PNG
python score/check.py out/v1 --duration 180.6
python score/viz.py out/v1 --speech-map speech-map.json
```

Ohne Narration läuft der Bau trotzdem (`--narration-dir` weglassen): Dann gilt
die Sprache als bereits auf −16 LUFS, und es entsteht keine `preview-mix.wav`.
Komplettes Beispiel mit der neutralen Beispielkarte (42 s, vier Szenen, Marsch
in B-Dur, 2/4):

```bash
python score/build.py --speech-map score/examples/speech-map.json \
    --variant score/examples/march.py --out out/march
```

Ausgaben je Bau (alles in `--out`):

| Datei | Inhalt |
|---|---|
| `music.wav` | Musik allein, 48 kHz, Stereo, 24 bit, volle Länge, feste Pegelstufen eingerechnet |
| `preview-mix.wav` | Narration + Musik, auf −16 LUFS normiert, ≤ −1,5 dBTP (nur mit `--narration-dir`) |
| `score.mid` | Standard-MIDI-Datei (Typ 1, Tempo- und Taktart-Spur, GM-Programme) |
| `score.json`, `notes.json` | Partitur- und Noten-Ledger (jede Note mit Zeit, Takt, Schlag, Stimme, Velocity) |
| `levels.json` | Pegelstufen und Messungen je Abschnitt (eigener BS.1770-Messer, ffmpeg-Gegenprobe wenn vorhanden) |
| `novelty.json` | Neuheitsbeleg (Intervall-n-Gramme der Melodie gegen `--compare`) |
| `ARRANGEMENT.md` | Idee, Motiv, Harmonik, Besetzung, Abschnitte, Pegel, Neuheit (Texte aus `DOC` der Partitur) |
| `qa/pianoroll.png`, `qa/spectrogram.png` | von `viz.py`: Noten über den Sprechfenstern, Spektrum mit 1–4-kHz-Markern |

Der Lauf ist deterministisch (feste Rauschschlüssel). Werkzeuge in `score/`:

| Datei | Aufgabe |
|---|---|
| `timeline.py` | Sprachkarte aus Szenen-Timeline und Narrationsclips bauen, laden, prüfen |
| `grid.py` | Taktraster je Szene und Spotting-Sheet |
| `engine.py` | Partitur → Noten → Audio/MIDI, Pegelstufen, BS.1770-Messer, Begrenzer |
| `synth.py` | Klangerzeuger (siehe unten), synthetischer Hall |
| `build.py` | Ein Stück vollständig bauen, Ledger, Neuheitsbeleg, `ARRANGEMENT.md` |
| `check.py`, `viz.py` | Abnahmeprüfung (ohne ffmpeg), Pianoroll und Spektrogramm |
| `analyze_ref.py` | Grobanalyse einer Referenzaufnahme (Tempo, Tonvorrat), nur zum Vergleich |
| `examples/` | Neutrale Beispiel-Sprachkarte und Beispielpartitur `march.py` |

## Die Sprachkarte: die Stimme ist die Zeitachse

`speech-map.json` (Beispiel: `score/examples/speech-map.json`):

```json
{"duration": 42.0,
 "scenes": [{"id": "intro", "start": 0.0, "end": 8.3}, {"id": "problem", "start": 8.3, "end": 19.2}],
 "voices": [{"id": "v1_intro", "clip_start": 0.7, "clip_dur": 4.7, "speech_start": 0.8, "speech_end": 5.2}],
 "pauses": [{"start": 5.2, "end": 9.05, "len": 3.85, "before": "v2_problem"}]}
```

- `scenes`: lückenlos, die letzte endet bei `duration`; eine Szene = ein Abschnitt der Partitur (Bildschnitt = Abschnittswechsel).
- `voices`: Sprechfenster (erstes bis letztes hörbares Wort je Narrationsclip); `clip_start`/`clip_dur` platzieren den Clip für die Mischung (`<voice id>.wav` in `--narration-dir`, 48 kHz).
- `pauses` (optional, wird aus den Sprechfenstern abgeleitet): Lücken zwischen den Fenstern; `before` ist die Id der nächsten Stimme, `"END"` für die Lücke nach dem letzten Wort.
- `timeline.py` erzeugt die Karte aus `timeline.json` (`{"duration", "scenes": [{"id","start","duration"}], "voices": [{"id","start"}]}`) und den Clips; Sprechfenster = Aktivitätsschwelle −50 dBFS. `--extend-last-scene` verlängert die Schlussszene (z. B. längere Endkarte).

`grid.py` legt je Szene ganze Takte an und biegt das Tempo je Szene minimal
(die Abweichung steht im Raster), damit **jeder Schnitt auf eine Eins fällt**;
ein Rest wird als kurzer Schlusstakt vor dem Schnitt notiert. Die Partitur
muss je Szene genau so viele Akkordtakte haben, wie das Raster ausweist.

## Partitur schreiben

Eine Partitur ist eine Python-Datei mit `SCORE` (und optional `DOC` für
`ARRANGEMENT.md`). Das vollständige Formatwörterbuch steht im Kopfkommentar von
[`score/examples/march.py`](score/examples/march.py); Kurzfassung:

| Baustein | Syntax |
|---|---|
| Akkordtafel `chords` | Takte mit `\|` getrennt, je Takt Akkordsymbole (`Bb`, `Gm`, `Cm7`, `F7`, `Fsus4`, `Ebmaj7`, `Bb/D`); Längen in Schlägen: `Cm7:1 F7:1` |
| Phrase `(Stimme, "Takt:Schlag", "Töne", Velocity)` | `Bb4:.5` Ton mit Länge in Schlägen, `r:.5` Pause, `\|` Taktstrich (wird geprüft), `g:A4` Vorschlag, `D5<` Rückwärts-Hüllkurve, `F5~:1` Triller, `Bb5*:2` klingt aus (Schlussakkord), `x`/`X` Schlag weich/hart (Perkussion) |
| Begleitfigur `default_parts` / `parts` | `dict(inst=…, pattern=[(Versatz, Länge, Spec, Velocity)], range=(tief, hoch), voices=3, when="speech"\|"pause", bars=(von, bis), drum=True, guide=True)`; Spec: `R` Grundton, `5`/`3`/`7`, `app` chromatische Annäherung, `v` Akkordlage, `a0`… Arpeggio, `+12` Oktave |
| Stimmen `instruments` | `dict(fn=synth.…, opt={…}, pan, send, gain, fg=True, drum=<GM-Note>, program=<GM-Programm>)`; `fg=True` kennzeichnet Melodiestimmen |

Klangerzeuger in `score/synth.py`: `chip_pulse`, `chip_tri`, `chip_hat`,
`chip_snare`, `chip_kick` (8-Bit); `marimba`, `glock`, `pizz`
(Karplus-Strong), `flute` (auch Okarina), `shaker`, `woodblock`, `framedrum`
(akustisch anmutend); `fm_brass`, `fm_bell`, `snare`, `bdrum`, `cymbal`
(Blech und Marsch). Neue Stimmen: eine Funktion `f(freq, dur, vel, bright, …)`
(Perkussion `f(vel, bright)`) in `synth.py` ergänzen.

## Regeln für gute Videomusik

- **Zwei bis drei Varianten** schreiben und über Charakter und Besetzung
  streuen (andere Tonart, anderer Takt, anderes Leitmotiv, andere Stimmen),
  statt an einer Fassung zu iterieren. Beispiele für die Streuung: 8-Bit-Quest-Thema
  in D-Dur/4/4 (Puls- und Dreieckswellen), gemütlicher 6/8-Dorfplatz in F-Dur
  (Marimba, Zupfbass, Flöte), leichter B-Dur-Marsch (FM-Blech, Tuba, Snare);
  als Beispielpartitur liegt nur der Marsch bei. Je Variante eine eigene
  Partitur-Datei und ein eigener Ausgabeordner.
- **Stimme als Zeitachse:** Szenenwechsel im Bild = Abschnittswechsel in der
  Musik; das Motiv wird **in den Sprechpausen** ausgespielt (Intro, Titelkarte,
  Szenenübergänge, Ende), nicht unter der Stimme. Pausen ab 1,3 s zählen als
  Vordergrund; Melodiestimmen (`fg=True`) dürfen nicht länger als 0,12 s in ein
  Wort ragen (`build.py` meldet jede Überschneidung).
- **Begleitlage unter Sprache:** mittlere Lage (z. B. MIDI 53–67), wenige
  Obertöne (`bright_speech` je Begleitfigur, Standard 0,3), Bett aus Umpa,
  Nachschlägen, gehaltenen Akkorden oder einer leisen Gegenstimme
  (`guide=True`); das Band 1–4 kHz bleibt weitgehend frei. Nachmessen:
  `levels.json` → `midband_1_4khz_share_pct.under_speech` (möglichst nahe 0).
- **Schluss:** Nach dem letzten Wort Motiv oder Kadenz, dann ein Schlussakkord
  (`Bb5*:2`), der frei ausklingt; die Begleitung endet im Takt davor
  (`bars=(1, <Takt vor dem Schlussakkord>)`).
- **Neu schreiben statt wiederverwenden:** Melodie und Akkordfolge je Projekt
  neu komponieren; eine übernommene Schablone ist der Grund, warum Stücke „wie
  derselbe Song" klingen.
- **Rein synthetisch:** keine fremden Samples, keine SoundFonts, keine
  Downloads, kein Musik-KI-Dienst, keine Zitate bekannter Melodien. Das hält
  das Stück eigenständig und die Rechtefrage trivial.

## Pegel ohne Ducking

Feste Verstärkung je Abschnitt statt Sidechain oder Carving:

- **Bett unter Sprache:** etwa 20 LU unter der Sprache, ≈ −36 LUFS (±2) bei
  −16 LUFS Gesamtmischung.
- **Vordergrund in Pausen ohne Sprache:** höchstens −24 LUFS (Ziel −24,5 LUFS
  ab 3 s Pause). Kürzere Übergangspausen liegen 2,5 dB je fehlender Sekunde
  tiefer (höchstens 4 dB), damit es zwischen zwei Sätzen nicht pumpt; der
  Schlussakkord nach dem letzten Wort bekommt die volle Stufe.
- **Rampen enden vor dem ersten Wort:** hoch höchstens 0,35 s nach Sprechende,
  herunter höchstens 0,8 s und 0,1 s vor dem nächsten Wort; die Einblendung
  dauert bis zu 0,55 s und endet 0,08 s vor dem ersten Wort. Der Schlussklang
  klingt auf fester Stufe aus (nur 0,15 s Klickschutz am Ende).
- **Wie:** Jede Stufe wird aus der gemessenen Musik abgeleitet
  (`Verstärkung = Ziel − LUFS`), dreimal mit den Rampen nachgemessen und
  nachgeregelt; die Gesamtmischung wird danach linear auf −16 LUFS gebracht.
  Ein Look-ahead-Begrenzer (Ceiling −1,6 dB) greift nur, wenn der True Peak
  −1,5 dBTP überschreitet, und fasst dann nur Sprachspitzen an. `levels.json`
  und `ARRANGEMENT.md` weisen jede Stufe und Messung aus.

## Neuheitsbeleg

Mit `--compare` (die `notes.json` früherer Stücke, auch die `*.notes.json` des
Storyline-Modus) vergleicht `build.py` die Melodie (`SCORE["melody"]`, Standard:
alle `fg`-Stimmen) mit jeder Tonhöhenspur jedes Vorgängerstücks über
Intervall-3-, -4- und -5-Gramme und zählt die gemeinsamen. Das Ergebnis steht in
`novelty.json` und `ARRANGEMENT.md`. Anhaltspunkt: wenige gemeinsame 4-Gramme
und keine gemeinsamen 5-Gramme, dazu eine andere Rhythmusvielfalt (verschiedene
Tondauern), belegen ein neues Stück; viele gemeinsame 4-/5-Gramme heißen: neu
schreiben.

## Prüfen: Hörproben und Mischung

- **Hörproben nur als eingefrorene Kopie abspielen.** Eine Hörprobe wurde
  einmal während des Abspielens überschrieben und rauschte hörbar. Deshalb
  bricht `build.py` ab, wenn der Zielordner nicht leer ist; abgespielt wird nur
  eine Kopie, und jeder neue Bau geht in einen neuen Ordner (`out/v2`).
- **Mischung gegen eine Referenz wellenformgenau prüfen, nicht nur per LUFS.**
  Gleiche Lautheit beweist nicht, dass die Wellenform stimmt: Ein
  ffmpeg-`alimiter` ohne `latency=1` verschob die Wellenform um die Attack-Zeit
  (Korrelation −0,17 statt 0,99999), die LUFS blieben gleich. Prüfung:

  ```python
  import numpy as np
  from scipy.io import wavfile
  (_, a), (_, b) = wavfile.read("mix.wav"), wavfile.read("reference.wav")
  n = min(len(a), len(b))
  print(np.corrcoef(a[:n].astype(float).ravel(), b[:n].astype(float).ravel())[0, 1])  # erwartet ~0.99999
  ```

- **Kein Abhören durch den Agenten:** Ein Agent belegt die Stücke durch Messung,
  Pianoroll und Spektrogramm; ob sie gefallen, entscheidet das Anhören der
  `preview-mix.wav` (einzeln, nacheinander, gegen das Video im zweiten Player).
- `check.py` dekodiert jede WAV vollständig, prüft Format und Länge und liest
  die MIDI-Datei; es braucht kein ffmpeg.

## Grenzen des Partitur-Modus

- Die Partitur entsteht von Hand. Das kostet Zeit und braucht Musikverstand; die
  Engine nimmt nur das Setzen und Messen ab.
- Klangfarbe: reine FM-Blechsynthese wirkt schneller künstlich als Holz und
  Glas; ob eine Variante überzeugt, zeigt erst die Hörprobe.
- Alle Stücke teilen `synth.py` und die Raster-/Pegellogik. Für eine Reihe
  von Stücken Besetzung und Klangfarbe ändern, nicht nur Töne.
- Das Raster ist an ganze Schläge je Szene gebunden; Szenen von nur wenigen
  Schlägen erlauben kaum Phrasen.

# Storyline-Modus (Skizze)

Der schnelle Modus: eine Storyline-JSON-Datei, ein Lauf, ein Score. Gut für
Entwürfe und Platzhalter, **nicht** für Musik, die als eigenständiges Stück
gelten soll.

> **Dokumentierte Grenze:** Der Storyline-Modus baut jedes Stück aus derselben
> Schablone (feste Akkordfolge je Emotion, Vier-Ton-Figuren aus einem geseedeten
> Random Walk, dieselben Wellenform-Stimmen). Wechselt man nur Seed, Tonart,
> Tempo oder Stil, bleibt das Grundmuster erkennbar: Über mehrere Projekte oder
> Videofassungen hinweg klingt es wie derselbe Song in Varianten (in einem
> Projekt wurde genau das nach drei Fassungen bemängelt). Ursache ist die
> Schablone, nicht der Seed. Dafür gibt es den Partitur-Modus.

## Das Verfahren: Storyline → Score

So rekonstruiert wie im Referenz-Score (179,5 s, c-Moll):

1. **Story-Akte auf Musikabschnitte mappen.** Akte, die einen emotionalen
   Zustand teilen, verschmelzen zu einem Abschnitt (Referenz: 7 Akte →
   5 Abschnitte; Akte 1–3 bildeten ein einziges 62-s-ruhiges Opening). Jeder
   Abschnitt bekommt exaktes `start`/`end` in Sekunden.
2. **Emotion + Intensität je Abschnitt zuweisen.**
   - *Emotion* wählt die Akkordfolge (Skalenstufen, Moll-Beispiel):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V ist harmonisch-Moll-Dur).
   - *Intensität* (0–1) treibt Tempo-Gefühl (BPM), Layer-Anzahl und
     Lautstärke-Rampe. Layer treten bei Schwellen bei: Pads immer → spärliche
     Glocken (<0,3) → Arp (≥0,25) → Bass (≥0,4) → Lead (≥0,45) →
     Drums (≥0,5) → Drive-Extras (≥0,65) → Pad-Oktavverdopplung (≥0,85).
3. **Spezielle Events auf der Zeitachse platzieren.**
   - `damp`: Gauß'sche Lautstärke-Duck — `1 - depth · exp(-((t-T)²)/(2σ²))`.
     Referenz: depth 0,5, σ 1 s bei T=84 s, auf dem gesprochenen Beat
     "Two databases. Same cluster." (~1:24).
   - `climax`: Zeitfenster, das volles Layering, Spitzenlautstärke,
     oktavverdoppelte Pads erzwingt (Referenz: 154–170 s = 2:34–2:50, beim
     2D→3D-Morph).
   - `outro`: ab seinem Start fallen Drums/Bass/Lead weg und Glocken faden
     auf 20 % (Referenz: 170–179,5 s, Abspannkarte).
4. **Verkleben.** Raised-Cosine-Glättung an Abschnittsgrenzen (~2,5 s),
   globaler Fade-in/-out, Feedback-Delay-Reverb (100 ms, Decay 0,25),
   Tanh-Drive + Peak-Normalisierung auf ein Hintergrundniveau (gemessener
   Referenz-Master: Mittel ≈ −22 dB, Max ≈ −1,6 dB).
5. **Hinter dem Voiceover bleiben.** Als "background" markierte Abschnitte
   deckeln ihre Lautstärke-Rampe; der Score ist ein Bett, kein Lead.

## Nutzung

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Ausgabe: `score.wav` (Stereo 16-bit 44,1 kHz), `score.mp3` (192k, braucht
ffmpeg im PATH; sonst mit Warnung übersprungen), `score.notes.json` (das
Arrangement-/Noten-Log: jede platzierte Note mit Zeit, Layer, MIDI-Pitch,
Dauer, Velocity) und `score.mid` — eine echte **Standard-MIDI-Datei** (Typ 1:
Tempo-Spur mit einem Tempo-Event je Abschnitt, Noten-Spur mit
GM-Programm-Hinweisen je Stil, Drums auf GM-Kanal 10). Abhängigkeitsfrei
geschrieben; kein pretty_midi/mido nötig.

Determinismus: gleiche Storyline + gleicher `seed` → byte-identisches WAV.

## Storyline-JSON-Referenz

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

- `duration` (Pflicht, Sekunden), `sections` (Pflicht, ≥1, sortiert,
  überlappungsfrei, innerhalb der Dauer).
- Abschnitts-Felder: `start`, `end` (Pflicht); `emotion` ∈ calm | tense |
  alive | driving | epic | outro; `intensity` 0–1 (Standard je Emotion);
  `bpm` (Standard: globales `bpm`); `melody` (optionale MIDI-Liste, zyklisch;
  sonst wird ein geseedeter Random Walk über Skalentöne erzeugt).
- `key`: Notenname (C, C#, Db, …), `mode`: minor | major.
- `style`: chiptune | ambient | electronic (siehe unten).
- Event `damp`: `time` (s), `depth` 0–1, `width` = σ in Sekunden.
- Standardwerte für Fades/Crossfade/Peak/Drive/Reverb wie oben gezeigt;
  alle optional.

Vollständiges durchgerechnetes Beispiel (die Rekonstruktion des
Referenzvideos): [`example-storyline.json`](example-storyline.json) —
rendert einen 179,5-s-Score, der dem Master-Level des Originals entspricht
(Mittel ≈ −22 dB, Max ≈ −1,6 dB).

## Stil-Presets

| Stil | Lead | Bass/Arp | Drums | Charakter |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle bass, schnelle square arps | Noise-basierter Kick/Hat/Snare | Retro-Konsole, arpeggio-getrieben (der Referenzstil) |
| `ambient` | weiches triangle/sine | langsame Arps, Long-Attack-Pads | erst ab Intensität ≥ 0,75 | spärlich, glocken-fokussiert, breites Reverb-Gefühl |
| `electronic` | sawtooth + detune + sub | druckvoller Bass, saw Arps | volles Kit | treibendes EDM-nahes Bett |

# Jenseits der Waveform-Synthese: bessere Sound-Backends

Die genannte Genre-Decke ist das **Sound-Backend, nicht die Komposition**.
Beide Modi erzeugen ein Backend-neutrales Arrangement; der mitgelieferte
numpy-Synth ist nur der kostenlose Offline-Standard-Renderer. Jeder Lauf
schreibt zusätzlich eine Standard-MIDI-Datei (`<out>.mid` bzw. `score.mid`) —
über bessere Instrumente rendern (der Partitur-Modus bleibt standardmäßig rein
synthetisch, siehe oben; dieser Abschnitt gilt nur, wenn ausdrücklich ein anderes
Klangbild gewünscht ist):

- **Pfad A — SoundFont (empfohlen: lokal, kostenlos, keine Cloud).**
  FluidSynth installieren (fluidsynth.org, Windows: `winget install FluidSynth`)
  plus ein kostenloses GM-SoundFont (GeneralUser GS von S. Christian Collins,
  oder MuseScore_General.sf2). Dann:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3
  über ffmpeg. Das schaltet Pop-/Rock-Band-Sounds, Klavier, einfache
  Streicher frei.
- **Pfad B — Orchester/Film.** Kostenlose Orchester-Bibliotheken: VSCO 2
  Community Edition, Soni Musicae, Salamander Grand Piano. Bessere
  Streicher/Blechbläser, epischer. Ehrlicher Hinweis: Artikulation und
  Humanisierung (Velocity-Variation, Legato, Dynamik-Kurven) zählen mehr
  als der Sample-Satz — und echte Filmscore-Epik braucht zusätzlich
  Arrangement-Reife; ein Backend allein reicht nicht.
- **Pfad C — externe KI-Generierung (Suno u. a.).** Möglich, wirft aber
  Datenschutz-/Rechtefragen auf — nur nach ausdrücklicher Nutzerfreigabe,
  niemals als Standard.

Geplant, aber **noch nicht implementiert**: eine `humanize`-Option in der
Engine (Velocity-/Timing-Jitter je Note), damit sample-basiertes Rendern
nicht mechanisch klingt (als TODO im Engine-Docstring markiert).

## Grenzen

- Englische und deutsche Storyline-Kommentare sind unproblematisch;
  Keys/Values sind fest englisch.
- Sehr kurze Dauern (< ~10 s) funktionieren, stauchen aber die Dramaturgie
  (Fades und Crossfades werden automatisch auf 20 % der Dauer / 50 % des
  kürzesten Abschnitts gedeckelt).
- Das Noten-Log (`*.notes.json`) ist der analysefreundliche Datensatz; die
  `*.mid`-Datei ist das Austauschformat für DAWs/SoundFont-Renderer
  (GM-Programmnummern sind grobe Stil-Hinweise — nach Geschmack remappen).

## Changelog

### 1.1.0 (2026-10-18)

- Neu: Partitur-Modus (`score/`) als empfohlener Weg für Videomusik: Sprachkarte
  (`timeline.py`), Taktraster (`grid.py`), Partitur → Noten/Audio/MIDI
  (`engine.py`, `synth.py`), Bau mit festen Pegelstufen ohne Ducking und
  Neuheitsbeleg (`build.py`), Prüfwerkzeuge (`check.py`, `viz.py`,
  `analyze_ref.py`), neutrale Beispielkarte und Beispielpartitur (Marsch),
  Test (`tests/test_score_mode.py`).
- Storyline-Modus (`compose_music.py`) unverändert, jetzt als Skizzenmodus
  mit dokumentierter Grenze gekennzeichnet.
- Abhängigkeit `scipy` ergänzt (nur Partitur-Modus).

### 1.0.0 (2026-07-31)

- Erstfassung: Storyline-Modus (`compose_music.py`).
