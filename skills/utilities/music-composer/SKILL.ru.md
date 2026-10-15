---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "Создаёт видеосинхронизированную фоновую музыку из storyline-JSON с помощью локального синтеза волновых форм (numpy + ffmpeg). Стили: Chiptune, Ambient, Electronic. Детерминированно, офлайн, без облачного сервиса."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: ru
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
translated_at: "2026-10-15T12:49:15.481627+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — Storyline → Score

Сочиняет фоновый score, который следует драматургической дуге
видео, полностью локально: синтез волновых форм на numpy (осцилляторы,
ADSR, наслоение, delay-реверберация) + ffmpeg для кодирования MP3.
Никаких сэмплов, никакого MIDI-оборудования, никакого облачного API.

## Когда использовать

- Видео/подкасту нужна фоновая музыка, которая точно попадает в story-биты
  по временным меткам (открытие, спад напряжения, драйв-секция, кульминация,
  финал).
- Нужен детерминированный, заново рендеримый score (тот же seed → то же аудио).
- Допустимы стили chiptune, ambient или electronic.

## Когда НЕ использовать (честные границы жанров)

Синтез волновых форм может дать фоновые подложки в стилях **chiptune, ambient и electronic**.
Встроенным синтезатором он **не может** дать **поп, рок, классику или
оркестровую киномузыку** — но аранжировка не зависит от бэкенда:
см. «За пределами синтеза волновых форм» ниже, чтобы отрендерить ту же композицию
через SoundFont, оркестровые библиотеки или внешнюю генерацию.

## Метод: Storyline → Score

Так же, как восстановлен эталонный score (179,5 с, до минор):

1. **Сопоставить акты истории с музыкальными секциями.** Акты, которые разделяют
   эмоциональное состояние, объединяются в одну секцию (эталон: 7 актов →
   5 секций; акты 1–3 образовали одно 62-секундное спокойное открытие). Каждой секции
   присваиваются точные `start`/`end` в секундах.
2. **Назначить эмоцию и интенсивность каждой секции.**
   - *Эмоция* выбирает аккордовую последовательность (ступени лада, пример для минора):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V — мажорное у гармонического минора).
   - *Интенсивность* (0–1) задаёт ощущение темпа (BPM), количество слоёв и
     нарастание громкости. Слои появляются при пороговых значениях: пэды всегда → разреженные колокольчики (<0,3) → арп (≥0,25) → бас (≥0,4) → лид (≥0,45) →
     ударные (≥0,5) → драйв-дополнения (≥0,65) → удвоение пэдов на октаву (≥0,85).
3. **Разместить специальные события на временной шкале.**
   - `damp`: гауссово приглушение громкости — `1 - depth · exp(-((t-T)²)/(2σ²))`.
     Эталон: depth 0,5, σ 1 с при T=84 с, на озвученном ударе
     «Two databases. Same cluster.» (~1:24).
   - `climax`: временное окно, которое принудительно задаёт полное наслоение, пиковую громкость,
     пэды, удвоенные на октаву (эталон: 154–170 с = 2:34–2:50, на морфинге 2D→3D).
   - `outro`: с его начала ударные, бас и лид отключаются, а колокольчики
     затухают до 20 % (эталон: 170–179,5 с, карточка титров).
4. **Склеить.** Raised-cosine сглаживание на границах секций (~2,5 с),
   глобальные fade-in/-out, feedback-delay-реверберация (100 мс, decay 0,25),
   tanh-драйв + пиковая нормализация до уровня подложки (измеренный
   эталонный мастер: среднее ≈ −22 дБ, максимум ≈ −1,6 дБ).
5. **Оставаться под закадровым голосом.** Секции, помеченные как «background», ограничивают
   свою громкостную кривую; score — это подложка, а не лид.

## Использование

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```

Вывод: `score.wav` (стерео 16 бит 44,1 кГц), `score.mp3` (192k, требует
ffmpeg в PATH; иначе пропускается с предупреждением), `score.notes.json` (журнал
аранжировки/нот: каждая размещённая нота с временем, слоем, MIDI-питчем,
длительностью, velocity) и `score.mid` — настоящий **стандартный MIDI-файл** (тип 1:
дорожка темпа с одним событием темпа на секцию, нотная дорожка с
подсказками программы GM для каждого стиля, ударные на GM-канале 10). Записывается без зависимостей;
pretty_midi/mido не нужны.

Детерминизм: тот же storyline + тот же `seed` → побайтово идентичный WAV.

## Справка по storyline-JSON

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

- `duration` (обязательно, секунды), `sections` (обязательно, ≥1, отсортировано,
  без перекрытий, внутри длительности).
- Поля секции: `start`, `end` (обязательны); `emotion` ∈ calm | tense |
  alive | driving | epic | outro; `intensity` 0–1 (по умолчанию для эмоции);
  `bpm` (по умолчанию: глобальный `bpm`); `melody` (необязательный список MIDI, циклический;
  иначе генерируется случайное блуждание с seed по ступеням лада).
- `key`: название ноты (C, C#, Db, …), `mode`: minor | major.
- `style`: chiptune | ambient | electronic (см. ниже).
- Событие `damp`: `time` (с), `depth` 0–1, `width` = σ в секундах.
- Значения по умолчанию для fade/crossfade/peak/drive/reverb такие, как показано выше;
  все необязательны.

Полный просчитанный пример (восстановление
эталонного видео): [`example-storyline.json`](example-storyline.json) —
рендерит 179,5-секундный score, соответствующий уровню мастера оригинала
(среднее ≈ −22 дБ, максимум ≈ −1,6 дБ).

## Пресеты стилей

| Стиль | Лид | Бас/Арп | Ударные | Характер |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | triangle-бас, быстрые square-арпы | Kick/Hat/Snare на основе шума | Ретро-консоль, арпеджио-ориентированный (эталонный стиль) |
| `ambient` | мягкий triangle/sine | медленные арпы, пэды с долгой атакой | только при интенсивности ≥ 0,75 | разреженный, ориентированный на колокольчики, широкое ощущение реверберации |
| `electronic` | sawtooth + detune + sub | мощный бас, saw-арпы | полный набор | драйвовая подложка, близкая к EDM |

## За пределами синтеза волновых форм: лучшие звуковые бэкенды

Указанный жанровый потолок относится к **звуковому бэкенду, а не к композиции**.
Процесс storyline→score создаёт аранжировку, не зависящую от бэкенда;
поставляемый numpy-синтезатор — лишь бесплатный офлайн-рендерер по умолчанию.
Каждый запуск дополнительно записывает стандартный MIDI-файл (`<out>.mid`) —
рендерите его через лучшие инструменты:

- **Путь A — SoundFont (рекомендуется: локально, бесплатно, без облака).**
  Установите FluidSynth (fluidsynth.org, Windows: `winget install FluidSynth`)
  и бесплатный GM-SoundFont (GeneralUser GS от S. Christian Collins
  или MuseScore_General.sf2). Затем:
  `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3
  через ffmpeg. Это открывает поп-/рок-групповые звуки, фортепиано, простые
  струнные.
- **Путь B — Оркестр/кино.** Бесплатные оркестровые библиотеки: VSCO 2
  Community Edition, Soni Musicae, Salamander Grand Piano. Лучшие
  струнные/медные, более эпичные. Честное замечание: артикуляция и
  humanization (вариация velocity, legato, кривые динамики) важнее,
  чем набор сэмплов — а настоящей эпике киномузыки нужна ещё и зрелость
  аранжировки; одного бэкенда недостаточно.
- **Путь C — внешняя генерация ИИ (Suno и др.).** Возможно, но возникают вопросы
  приватности и прав — только после явного согласия пользователя,
  никогда по умолчанию.

Запланировано, но **ещё не реализовано**: опция `humanize` в
движке (джиттер velocity/тайминга на каждую ноту), чтобы рендеринг на основе сэмплов
не звучал механически (помечено как TODO в docstring движка).

## Ограничения

- Комментарии в storyline на английском и немецком языках не создают проблем;
  ключи/значения фиксированы на английском.
- Очень короткие длительности (< ~10 с) работают, но сжимают драматургию
  (fade и crossfade автоматически ограничиваются 20 % длительности / 50 % самой короткой секции).
- Журнал нот (`*.notes.json`) — удобный для анализа набор данных; файл
  `*.mid` — формат обмена для DAW/рендереров SoundFont
  (номера программ GM — грубые подсказки по стилю; при желании переназначьте по вкусу).
