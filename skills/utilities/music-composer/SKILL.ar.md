---
name: music-composer
version: 1.0.0
type: tool
author: ellmos contributors
created: 2026-07-31
updated: 2026-07-31
description: "يؤلف موسيقى خلفية متزامنة مع الفيديو من ملف JSON للحبكة، عبر تخليق الموجات محليًا (numpy + ffmpeg). الأنماط: Chiptune وAmbient وElectronic. حتمي، يعمل دون اتصال، ولا يعتمد على أي خدمة سحابية."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: utilities
tags: [music, audio, score, composition, chiptune, ambient, electronic, video-sync, waveform-synthesis]
language: ar
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
translated_at: "2026-10-15T22:17:49.701000+00:00"
---
<img src="banner.png" width="100%" alt="music-composer banner">

# music-composer — من الحبكة (Storyline) إلى المقطوعة (Score)

يؤلف مقطوعة خلفية تتبع القوس الدرامي لفيديو، بالكامل محليًا: تخليق موجات عبر numpy (مذبذبات، وADSR، وتراكب الطبقات، وصدى التأخير) مع ffmpeg لترميز MP3. لا عينات صوتية، ولا أجهزة MIDI، ولا واجهة برمجة تطبيقات سحابية.

## متى يُستخدم

- يحتاج فيديو أو بودكاست إلى موسيقى خلفية تتطابق نقاط القصة فيها تمامًا مع الطوابع الزمنية (المقدمة، ووادي التوتر، ومقطع الدفع، والذروة، والخاتمة).
- يُحتاج إلى مقطوعة حتمية يمكن إعادة عرضها (البذرة نفسها → الصوت نفسه).
- أنماط Chiptune أو Ambient أو Electronic مقبولة.

## متى لا يُستخدم (حدود الأنماط بصراحة)

يمكن لتخليق الموجات أن يوفر خلفيات من نوع **Chiptune وAmbient وElectronic**. لكنه لا يستطيع، بالمُخلِّق المدمج فيه، توفير **Pop أو Rock أو الموسيقى الكلاسيكية أو موسيقى الأفلام الأوركسترالية**. غير أن الترتيب الموسيقي مستقل عن الواجهة الخلفية: انظر "ما وراء تخليق الموجات" أدناه، لعرض التأليف نفسه عبر SoundFonts أو مكتبات الأوركسترا أو التوليد الخارجي.

## الإجراء: من الحبكة (Storyline) إلى المقطوعة (Score)

أُعيد بناؤه على هذا النحو في المقطوعة المرجعية (179,5 ثانية، دو صغير):

1. **ربط فصول القصة بأقسام الموسيقى.** الفصول التي تشترك في حالة عاطفية واحدة تندمج في قسم واحد (المرجع: 7 فصول ← 5 أقسام؛ شكّلت الفصول 1–3 مقدمةً هادئةً واحدةً مدتها 62 ثانية). يُحدَّد لكل قسم `start`/`end` بدقة بالثواني.
2. **تعيين الشعور والشدة لكل قسم.**
   - *الشعور* يختار تسلسل الكوردات (درجات السلم، مثال من المقام الصغير):
     `calm` i–VI–III–VII · `tense` iv–i–V–i · `alive` VI–VII–i–III ·
     `driving` i–VII–VI–V · `epic` iv–V–VI–i (V هي درجة كبيرة في المقام الصغير الهارموني).
   - *الشدة* (0–1) تحدد إحساس السرعة (BPM) وعدد الطبقات ومنحنى تصاعد الصوت. تظهر الطبقات عند العتبات: الوسائد الصوتية دائمًا ← أجراس متفرقة (<0,3) ← أربيجيو (≥0,25) ← باس (≥0,4) ← لحن رئيسي (≥0,45) ← طبول (≥0,5) ← عناصر الدفع (≥0,65) ← مضاعفة الوسائد بالأوكتاف (≥0,85).
3. **وضع الأحداث الخاصة على المحور الزمني.**
   - `damp`: خفض الصوت (Ducking) الغاوسي — `1 - depth · exp(-((t-T)²)/(2σ²))`. المرجع: depth = 0,5، وσ = 1 ثانية عند T = 84 ثانية، على النبضة المنطوقة "قاعدتا بيانات. نفس العنقود." (~1:24).
   - `climax`: نافذة زمنية تفرض التراكب الكامل للطبقات وأقصى مستوى صوت والوسائد المضاعفة بالأوكتاف (المرجع: 154–170 ثانية = 2:34–2:50، عند تحوّل 2D→3D).
   - `outro`: منذ بدايته تتوقف الطبول والباس واللحن الرئيسي، وتخفت الأجراس إلى 20 % (المرجع: 170–179,5 ثانية، بطاقة الختام).
4. **الدمج.** تنعيم Raised-Cosine عند حدود الأقسام (~2,5 ثانية)، وتلاشٍ عام للدخول والخروج، وصدى تأخير بتغذية راجعة (100 ms، وتلاشٍ 0,25)، وتشويه Tanh مع تطبيع الذروة إلى مستوى خلفية (الماستر المرجعي المقاس: المتوسط ≈ −22 dB، والأقصى ≈ −1,6 dB).
5. **البقاء خلف التعليق الصوتي.** الأقسام الموسومة بـ "background" تحدّ من منحنى تصاعد صوتها؛ فالمقطوعة فراش، لا لحن رئيسي.

## الاستخدام

```bash
# Mitgelieferte eigenständige Kopie (dieser Skill-Ordner):
python compose_music.py storyline.json -o out/score
python compose_music.py --init       # gibt eine Storyline-Vorlage aus
python compose_music.py --selftest   # 3-s-Render + Verifikation

# Kanonische Engine (bevorzugt, wenn das Repo verfügbar ist):
python <ai-media-editor>/tools/compose_music.py storyline.json -o out/score
```


المخرجات: `score.wav` (ستيريو 16 بت، 44,1 kHz)، و`score.mp3` (192k، يحتاج ffmpeg في PATH، وإلا يُتخطى مع تحذير)، و`score.notes.json` (سجل الترتيب والنوتات: كل نوتة موضوعة مع الزمن والطبقة ودرجة MIDI (Pitch) والمدة والسرعة (Velocity))، و`score.mid` — **ملف MIDI قياسي** حقيقي (النوع 1: مسار تمبو فيه حدث تمبو واحد لكل قسم، ومسار نوتات مع تلميحات برامج GM لكل نمط، والطبول على قناة GM رقم 10). مكتوب دون أي تبعيات؛ لا حاجة إلى pretty_midi أو mido.

الحتمية: الحبكة نفسها + `seed` نفسه → ملف WAV متطابق بايتًا ببايت.

## مرجع JSON الخاص بالحبكة (Storyline-JSON)

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

- `duration` (إلزامي، بالثواني)، و`sections` (إلزامي، ≥1، مرتب، بلا تداخل، ضمن المدة).
- حقول القسم: `start`، و`end` (إلزامية)؛ `emotion` ∈ calm | tense | alive | driving | epic | outro؛ `intensity` من 0 إلى 1 (القيمة الافتراضية حسب الشعور)؛ `bpm` (الافتراضي: `bpm` العام)؛ `melody` (قائمة MIDI اختيارية، دورية؛ وإلا يُنشأ مسار عشوائي (Random Walk) مُهيَّأ ببذرة عبر درجات السلم).
- `key`: اسم النوتة (C، C#، Db، …)، و`mode`: minor | major.
- `style`: chiptune | ambient | electronic (انظر أدناه).
- الحدث `damp`: `time` (ثانية)، و`depth` من 0 إلى 1، و`width` = σ بالثواني.
- القيم الافتراضية للتلاشي والتلاشي المتقاطع والذروة والدفع والصدى كما هو موضح أعلاه؛ وكلها اختيارية.

مثال كامل محسوب (إعادة بناء الفيديو المرجعي): [`example-storyline.json`](example-storyline.json) — يعرض مقطوعة مدتها 179,5 ثانية تطابق مستوى ماستر الأصل (المتوسط ≈ −22 dB، والأقصى ≈ −1,6 dB).

## إعدادات الأنماط المسبقة

| النمط | اللحن الرئيسي | الباس/الأربيجيو | الطبول | الطابع |
|---|---|---|---|---|
| `chiptune` | square + detune + triangle | باس triangle، وأربيجيو square سريع | ركلة/هاي-هات/سنير قائمة على الضوضاء | كونسول retro، يقوده الأربيجيو (النمط المرجعي) |
| `ambient` | triangle/sine ناعم | أربيجيو بطيء، ووسائد ذات هجوم طويل | فقط من شدة ≥ 0,75 | متفرق، يركز على الأجراس، وإحساس صدى واسع |
| `electronic` | sawtooth + detune + sub | باس قوي، وأربيجيو saw | الطقم الكامل | فراش دافع قريب من EDM |

## ما وراء تخليق الموجات: واجهات صوتية خلفية أفضل

إن سقف الأنماط المذكور هو **الواجهة الصوتية الخلفية، لا التأليف**. إجراء Storyline→Score ينتج ترتيبًا مستقلًا عن الواجهة الخلفية؛ ومُخلِّق numpy المرفق هو فقط عارض الأوفلاين المجاني الافتراضي. كل تشغيل يكتب أيضًا ملف MIDI قياسيًا (`<out>.mid`) — للعرض عبر آلات أفضل:

- **المسار A — SoundFont (موصى به: محلي، مجاني، بلا سحابة).** ثبّت FluidSynth (fluidsynth.org، وعلى Windows: `winget install FluidSynth`) مع SoundFont مجاني بمعيار GM (GeneralUser GS من S. Christian Collins، أو MuseScore_General.sf2). ثم: `fluidsynth -ni soundfont.sf2 score.mid -F score_sf.wav -r 44100` → MP3 عبر ffmpeg. وهذا يفتح أصوات فرق البوب والروك، والبيانو، والوتريات البسيطة.
- **المسار B — الأوركسترا/الفيلم.** مكتبات أوركسترالية مجانية: VSCO 2 Community Edition، وSoni Musicae، وSalamander Grand Piano. وترات ونحاسيات أفضل، وأكثر ملحمية. تنويه صريح: النطق الموسيقي (Articulation) والأنسنة (تنوع السرعة Velocity، وLegato، ومنحنيات الديناميكية) أهم من مجموعة العينات، والملحمية الحقيقية لموسيقى الأفلام تحتاج أيضًا إلى نضج في الترتيب؛ فالواجهة الخلفية وحدها لا تكفي.
- **المسار C — توليد خارجي بالذكاء الاصطناعي (Suno وغيره).** ممكن، لكنه يثير أسئلة الخصوصية والحقوق، فلا يُستخدم إلا بعد موافقة صريحة من المستخدم، ولا يُعتمد أبدًا كخيار افتراضي.

مخطط له، لكنه **لم يُنفَّذ بعد**: خيار `humanize` في المحرك (ارتعاش السرعة والتوقيت لكل نوتة)، حتى لا يبدو العرض المعتمد على العينات آليًا (ومُعلَّم كـ TODO في docstring المحرك).

## الحدود

- تعليقات الحبكة بالإنجليزية والألمانية لا إشكال فيها؛ أما المفاتيح والقيم فهي إنجليزية ثابتة.
- المدد القصيرة جدًا (< ~10 ثوانٍ) تعمل، لكنها تضغط الدراما (يُحدّ التلاشي والتلاشي المتقاطع تلقائيًا عند 20 % من المدة / 50 % من أقصر قسم).
- سجل النوتات (`*.notes.json`) هو مجموعة البيانات الملائمة للتحليل، وملف `*.mid` هو تنسيق التبادل لبرامج DAW ومُعرِّضات SoundFont (أرقام برامج GM تلميحات أسلوبية تقريبية، فأعد تعيينها حسب الذوق).
