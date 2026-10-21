---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "Compone música de fondo sincronizada con el video a partir de un JSON de storyline mediante síntesis de forma de onda local (numpy + ffmpeg). Estilos: Chiptune, Ambient, Electronic. Determinista, sin conexión, sin servicio en la nube."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: es
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
translated_at: "2026-10-15T11:49:45.560323+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

Compone una partitura de fondo que sigue el arco dramático de un video,
completamente en local: síntesis de forma de onda con numpy (osciladores,
ADSR, superposición de capas, reverberación con retardo) + ffmpeg para la
codificación MP3. Sin muestras, sin hardware MIDI, sin API en la nube.

## Cuándo usarlo

- Un video/podcast necesita música de fondo que coincida exactamente con los
  momentos de la historia en marcas de tiempo (apertura, valle de tensión,
  sección de impulso, clímax, cierre).
- Se necesita una partitura determinista que pueda volver a renderizarse
  (misma semilla → mismo audio).
- Son aceptables los estilos Chiptune, Ambient o Electronic.

## Cuándo NO usarlo (límites honestos de género)

La síntesis de forma de onda puede producir bases de fondo **Chiptune, Ambient
y Electronic**. Con su sintetizador integrado **no puede producir Pop, Rock,
música clásica ni música de cine orquestal**, pero el arreglo es neutral
respecto al backend: consulta "Más allá de la síntesis de forma de onda" más
abajo para renderizar la misma composición con SoundFonts, bibliotecas
orquestales o generación externa.

## El procedimiento: Storyline → Score

Reconstruido como en la partitura de referencia (179,5 s, do menor):

1. **Asignar los actos de la historia a secciones musicales.** Los actos que
   comparten un estado emocional se fusionan en una sola sección (referencia:
   7 actos → 5 secciones; los actos 1–3 formaron una única apertura tranquila
   de 62 s). Cada sección recibe `start`/`end` exactos en segundos.
2. **Asignar emoción e intensidad a cada sección.**
   - *Emoción* elige la progresión de acordes (grados de escala, ejemplo menor):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V es la dominante de la menor armónica).
   - *Intensidad* (0–1) controla la sensación de tempo (BPM), el número de
     capas y la rampa de volumen. Las capas entran en los umbrales: pads
     siempre → campanas escasas (<0,3) → arpegio (≥0,25) → bajo (≥0,4) → lead
     (≥0,45) → batería (≥0,5) → extras de impulso (≥0,65) → duplicación de
     pads a la octava (≥0,85).
3. **Colocar eventos especiales en la línea de tiempo.**
   - `damp`: atenuación gaussiana del volumen — `1 - depth · exp(-((t-T)²)/(2σ²))`.
     Referencia: profundidad 0,5, σ 1 s en T=84 s, sobre el golpe hablado
     "Two databases. Same cluster." (~1:24).
   - `climax`: ventana temporal que fuerza superposición completa, volumen
     máximo y pads duplicados a la octava (referencia: 154–170 s = 2:34–2:50,
     durante la transición 2D→3D).
   - `outro`: desde su inicio, batería/bajo/lead desaparecen y las campanas
     se atenúan al 20 % (referencia: 170–179,5 s, tarjeta de créditos).
4. **Unir.** Suavizado de coseno elevado en los límites de sección (~2,5 s),
   fundido global de entrada y salida, reverberación con retardo realimentado
   (100 ms, decaimiento 0,25), drive tanh + normalización de pico a un nivel de
   fondo (master de referencia medido: media ≈ −22 dB, máx ≈ −1,6 dB).
5. **Mantenerse detrás de la voz en off.** Las secciones marcadas como
   "background" limitan su rampa de volumen; la partitura es una base, no un
   protagonista.

## Uso

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Salida: `score.wav` (estéreo 16 bits 44,1 kHz), `score.mp3` (192k, requiere
ffmpeg en el PATH; si no, se omite con una advertencia), `score.notes.json` (el registro de
arreglo/notas: cada nota colocada con tiempo, capa, tono MIDI, duración,
velocidad) y `score.mid` — un **archivo MIDI estándar** real (tipo 1: pista de
tempo con un evento de tempo por sección, pista de notas con indicaciones de
programa GM por estilo, batería en el canal GM 10). Se escribe sin
dependencias; no necesita pretty_midi ni mido.

Determinismo: misma storyline + mismo `seed` → WAV idéntico byte a byte.

## Referencia del JSON de storyline

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

- `duration` (obligatorio, segundos), `sections` (obligatorio, ≥1, ordenadas,
  sin solapamientos, dentro de la duración).
- Campos de sección: `start`, `end` (obligatorios); `emotion` ∈ calm | tense |
  alive | driving | epic | outro; `intensity` 0–1 (por defecto según la emoción);
  `bpm` (por defecto: `bpm` global); `melody` (lista MIDI opcional, cíclica;
  si no, se genera un paseo aleatorio con semilla sobre tonos de la escala).
- `key`: nombre de nota (C, C#, Db, …), `mode`: minor | major.
- `style`: chiptune | ambient | electronic (ver abajo).
- Evento `damp`: `time` (s), `depth` 0–1, `width` = σ en segundos.
- Los valores por defecto para fundidos/crossfade/pico/drive/reverberación son
  los mostrados arriba; todos son opcionales.

Ejemplo completo calculado (la reconstrucción del video de referencia):
[`example-storyline.json`](example-storyline.json) — renderiza una partitura de
179,5 s que coincide con el nivel master del original (media ≈ −22 dB,
máx ≈ −1,6 dB).

## Presets de estilo

| Estilo | Lead | Bajo/Arpegio | Batería | Carácter |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | bajo triangle, arpegios square rápidos | Kick/Hat/Snare basados en ruido | Consola retro, impulsado por arpegios (el estilo de referencia) |
| `ambient` | triangle/sine suave | arpegios lentos, pads de ataque largo | solo con intensidad ≥ 0,75 | escaso, centrado en campanas, sensación de reverberación amplia |
| `electronic` | sawtooth + detune + sub | bajo con pegada, arpegios saw | kit completo | base impulsiva cercana al EDM |

## Más allá de la síntesis de forma de onda: mejores backends de sonido

El techo de género mencionado corresponde al **backend de sonido, no a la
composición**. El procedimiento Storyline→Score produce un arreglo neutral
respecto al backend; el sintetizador numpy incluido es solo el renderizador
estándar gratuito sin conexión. Cada ejecución también escribe un archivo
MIDI estándar (`<out>.mid`), que puedes renderizar con instrumentos mejores:

- **Vía A — SoundFont (recomendada: local, gratuita, sin nube).**
  Instala FluidSynth (fluidsynth.org; Windows: `winget install FluidSynth`) más un
  SoundFont GM gratuito (GeneralUser GS de S. Christian Collins, o
  MuseScore_General.sf2). Después:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3
  mediante ffmpeg. Así se habilitan sonidos de banda pop/rock, piano y
  cuerdas sencillas.
- **Vía B — Orquesta/cine.** Bibliotecas orquestales gratuitas: VSCO 2
  Community Edition, Soni Musicae, Salamander Grand Piano. Cuerdas y metales
  mejores, más épicos. Aviso honesto: la articulación y la humanización
  (variación de velocidad, legato, curvas de dinámica) importan más que el
  conjunto de muestras, y la épica de una partitura de cine real también
  requiere madurez de arreglo; un backend por sí solo no basta.
- **Vía C — generación externa con IA (Suno u otros).** Es posible, pero
  plantea cuestiones de privacidad y derechos; solo con autorización
  explícita del usuario, nunca como opción por defecto.

Previsto, pero **aún no implementado**: una opción `humanize` en el motor
(variación de velocidad/tiempo por nota) para que el renderizado basado en
muestras no suene mecánico (marcado como TODO en la documentación del motor).

## Límites

- Los comentarios de storyline en inglés y alemán no suponen problema; las
  claves y los valores son fijos en inglés.
- Duraciones muy cortas (< ~10 s) funcionan, pero comprimen la dramaturgia
  (los fundidos y crossfades se limitan automáticamente al 20 % de la duración
  / al 50 % de la sección más corta).
- El registro de notas (`*.notes.json`) es el conjunto de datos apto para análisis; el
  archivo `*.mid` es el formato de intercambio para DAWs y renderizadores SoundFont
  (los números de programa GM son pistas de estilo aproximadas; reasígnalos
  según tu gusto).
