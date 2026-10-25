---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "Compõe música de fundo sincronizada com vídeo a partir de um JSON de storyline, por síntese de forma de onda local (numpy + ffmpeg). Estilos: Chiptune, Ambient, Electronic. Determinístico, offline, sem serviço em nuvem."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: pt
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
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

Compõe uma partitura de fundo que segue o arco dramatúrgico de um
vídeo, totalmente localmente: síntese de forma de onda com numpy (osciladores,
ADSR, camadas, reverb de atraso) + ffmpeg para a codificação MP3. Sem samples,
sem hardware MIDI, sem API em nuvem.

## Quando usar

- Um vídeo/podcast precisa de música de fundo que acompanhe os beats da história
  exatamente nos marcos de tempo (abertura, vale de tensão, seção de drive,
  clímax, encerramento (outro).
- É necessária uma partitura determinística e renderizável de novo (mesma
  semente → mesmo áudio).
- Estilos chiptune, ambient ou electronic são aceitáveis.

## Quando NÃO usar (limites honestos de gênero)

A síntese de forma de onda pode entregar bases de fundo **chiptune, ambient e
electronic**. Com o sintetizador embutido, ela **não** pode entregar **pop, rock,
música clássica ou trilha orquestral de cinema** — mas o arranjo é neutro quanto
ao backend: veja "Além da síntese de forma de onda" abaixo, para renderizar a
mesma composição com SoundFonts, bibliotecas orquestrais ou geração externa.

## O procedimento: Storyline → Score

Reconstruído assim como na partitura de referência (179,5 s, dó menor):

1. **Mapear os atos da história em seções musicais.** Atos que compartilham um
   estado emocional se fundem em uma seção (referência: 7 atos → 5 seções;
   os atos 1–3 formaram uma única abertura calma de 62 s). Cada seção recebe
   `start`/`end` exatos em segundos.
2. **Atribuir emoção + intensidade por seção.**
   - *Emoção* escolhe a progressão de acordes (graus da escala, exemplo menor):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V é maior na menor harmônica).
   - *Intensidade* (0–1) controla a sensação de andamento (BPM), o número de
     camadas e a rampa de volume. As camadas entram em limiares: pads sempre →
     sinos esparsos (<0,3) → arp (≥0,25) → baixo (≥0,4) → lead (≥0,45) →
     bateria (≥0,5) → extras de drive (≥0,65) → duplicação de pads em oitava (≥0,85).
3. **Posicionar eventos especiais na linha do tempo.**
   - `damp`: redução de volume gaussiana — `1 - depth · exp(-((t-T)²)/(2σ²))`.
     Referência: profundidade 0,5, σ 1 s em T=84 s, sobre o beat falado
     "Two databases. Same cluster." (~1:24).
   - `climax`: janela de tempo que força camadas completas, pico de volume
     e pads com oitava dobrada (referência: 154–170 s = 2:34–2:50, na
     transição 2D→3D).
   - `outro`: a partir do seu início, bateria/baixo/lead saem e os sinos
     caem para 20 % (referência: 170–179,5 s, cartão de créditos).
4. **Juntar tudo.** Suavização raised-cosine nas fronteiras de seção (~2,5 s),
   fade-in/fade-out global, reverb de atraso com realimentação (100 ms, decaimento 0,25),
   drive tanh + normalização de pico para um nível de fundo (master de referência
   medido: média ≈ −22 dB, máximo ≈ −1,6 dB).
5. **Ficar atrás da narração.** Seções marcadas como "background" limitam sua
   rampa de volume; a partitura é uma cama, não um lead.

## Uso

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Saída: `score.wav` (estéreo 16 bits 44,1 kHz), `score.mp3` (192k, requer
ffmpeg no PATH; caso contrário é ignorado com aviso), `score.notes.json` (o log de
arranjo/notas: cada nota colocada com tempo, camada, pitch MIDI,
duração, velocidade) e `score.mid` — um **arquivo Standard MIDI** real (tipo 1:
trilha de tempo com um evento de tempo por seção, trilha de notas com
indicações de programa GM por estilo, bateria no canal GM 10). Escrito sem
dependências; não é necessário pretty_midi/mido.

Determinismo: mesma storyline + mesmo `seed` → WAV byte a byte idêntico.

## Referência do JSON de storyline

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

- `duration` (obrigatório, segundos), `sections` (obrigatório, ≥1, ordenadas,
  sem sobreposição, dentro da duração).
- Campos da seção: `start`, `end` (obrigatórios); `emotion` ∈ calm | tense |
  alive | driving | epic | outro; `intensity` 0–1 (padrão por emoção);
  `bpm` (padrão: `bpm` global); `melody` (lista MIDI opcional, cíclica;
  caso contrário é gerado um passeio aleatório semeado sobre os tons da escala).
- `key`: nome da nota (C, C#, Db, …), `mode`: minor | major.
- `style`: chiptune | ambient | electronic (veja abaixo).
- Evento `damp`: `time` (s), `depth` 0–1, `width` = σ em segundos.
- Valores padrão para fades/crossfade/pico/drive/reverb como mostrado acima;
  todos opcionais.

Exemplo completo calculado (a reconstrução do
vídeo de referência): [`example-storyline.json`](example-storyline.json) —
renderiza uma partitura de 179,5 s que corresponde ao nível de master do original
(média ≈ −22 dB, máximo ≈ −1,6 dB).

## Presets de estilo

| Estilo | Lead | Baixo/Arp | Bateria | Caráter |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | baixo triangle, arps square rápidos | Kick/hat/snare baseados em ruído | Console retrô, guiado por arpejos (o estilo de referência) |
| `ambient` | triangle/sine suave | arps lentos, pads de ataque longo | só a partir de intensidade ≥ 0,75 | esparso, focado em sinos, sensação de reverb ampla |
| `electronic` | sawtooth + detune + sub | baixo potente, arps saw | kit completo | base impulsionante próxima do EDM |

## Além da síntese de forma de onda: backends de som melhores

O teto de gênero mencionado é o **backend de som, não a composição**.
O procedimento storyline→score produz um arranjo neutro quanto ao backend;
o sintetizador numpy incluído é apenas o renderizador offline padrão gratuito.
Cada execução também grava um arquivo Standard MIDI (`<out>.mid`) —
renderize com instrumentos melhores:

- **Caminho A — SoundFont (recomendado: local, gratuito, sem nuvem).**
  Instale o FluidSynth (fluidsynth.org, Windows: `winget install FluidSynth`)
  mais um SoundFont GM gratuito (GeneralUser GS de S. Christian Collins,
  ou MuseScore_General.sf2). Depois:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3
  via ffmpeg. Isso libera sons de banda pop/rock, piano e cordas simples.
- **Caminho B — Orquestra/cinema.** Bibliotecas orquestrais gratuitas: VSCO 2
  Community Edition, Soni Musicae, Salamander Grand Piano. Cordas/metais
  melhores, mais épicos. Observação honesta: articulação e humanização (variação de
  velocidade, legato, curvas de dinâmica) importam mais que o conjunto de samples —
  e a épica de trilha de cinema real exige também maturidade de arranjo;
  um backend sozinho não basta.
- **Caminho C — geração externa por IA (Suno etc.).** Possível, mas levanta
  questões de privacidade/direitos — somente com aprovação explícita do usuário,
  nunca como padrão.

Planejado, mas **ainda não implementado**: uma opção `humanize` no
motor (jitter de velocidade/timing por nota), para que a renderização baseada em samples
não soe mecânica (marcado como TODO na docstring do motor).

## Limites

- Comentários de storyline em inglês e alemão não são problemáticos;
  chaves/valores são fixos em inglês.
- Durações muito curtas (< ~10 s) funcionam, mas comprimem a dramaturgia
  (fades e crossfades são limitados automaticamente a 20 % da duração / 50 % da
  seção mais curta).
- O log de notas (`*.notes.json`) é o conjunto de dados voltado para análise; o
  arquivo `*.mid` é o formato de troca para DAWs/renderizadores SoundFont
  (os números de programa GM são indicações grosseiras de estilo — remapeie conforme o gosto).
