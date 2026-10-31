---
name: video-transcriber
version: 1.2.0
type: tool
author: Lukas Geiger
created: 2026-04-04
updated: 2026-08-24
description: "جلب نصوص الفيديو (الترجمات المصاحبة) والبيانات الوصفية من مصادر الفيديو عبر الإنترنت، وإخراجها بصيغة Markdown أو JSON أو نص عادي. المصدر المدعوم حاليًا: YouTube. يُفضَّل الترجمات المنشأة يدويًا، ويُعتمد على الترجمات المولَّدة تلقائيًا عند عدم توفرها."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [video, transcript, subtitles, metadata, research, youtube]
language: ar
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['youtube-transcript-api', 'yt-dlp']}
provenance: {'origin': 'bach', 'origin_path': 'system/tools/youtube_extractor.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-04-04', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: caf55e3434119acd935dad208f5461f7a08e72d34b595314abd52b58469cd299
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.164575+00:00"
---
<img src="banner.png" width="100%" alt="video-transcriber banner">

# مُحوِّل نصوص الفيديو

يجلب النصوص (الترجمات المصاحبة) والبيانات الوصفية (العنوان، والقناة، والتاريخ، وعدد المشاهدات،
والوصف) من مقاطع الفيديو عبر الإنترنت. يُفضَّل الترجمات المنشأة يدويًا، مع الرجوع إلى الترجمات
المولَّدة تلقائيًا عند عدم توفرها. تكون المخرجات بصيغة Markdown أو JSON أو نص عادي.

إذا لم يُرجع المسار الأساسي (`youtube-transcript-api`) أي نتيجة، يتدخل تلقائيًا مسار ثانٍ عبر
البيانات الوصفية لـ yt-dlp. يقرأ هذا المسار مسار الترجمة فقط، وهو المسار الذي تسلّمه المنصة
أصلًا لتشغيل الفيديو، **دون تنزيل أي فيديو أو صوت**. ويظهر المسار الذي تم استخدامه في الحقل
`source` ضمن مخرجات JSON، وكذلك على stderr.

لكل لغة مطلوبة، يعطي المسار الثانوي الأولوية للمسارات اليدوية المطابقة تمامًا أو للغة الأساسية،
قبل المسارات المولَّدة تلقائيًا المطابقة تمامًا أو للغة الأساسية؛ أما أي مسار آخر فيأتي لاحقًا.
ولا يؤدي تعذر قراءة مسار JSON3 إلى إيقاف الجلب ما دام هناك مرشح آخر متاح.

المصدر المدعوم حاليًا: **YouTube** (youtube.com وyoutu.be وyoutube-nocookie.com).

لمقاطع الفيديو، استخدم هذه الأداة بدلًا من تلخيص المحتوى يدويًا، فالنص المفرَّغ هو المصدر الموثوق.

> **تنبيه:** هذه الأداة غير مرتبطة بـ YouTube أو Google، ولا تحظى بدعمهما أو اعتمادهما. يتم
> الاستخدام على مسؤولية المستخدم وحده. المستخدمون مسؤولون بأنفسهم عن الالتزام بشروط الاستخدام
> الخاصة بالمنصة المعنية وبقانون حقوق المؤلف المعمول به. يُمنع تجاوز إدارة الحقوق الرقمية (DRM)
> أو الاشتراكات المدفوعة أو قيود الوصول؛ ويُمنع الجمع الآلي الواسع النطاق للبيانات؛ ويُمنع إعادة نشر النصوص
> المحمية دون موافقة أصحاب الحقوق.

## التبعيات والتراخيص

```bash
pip install youtube-transcript-api   # Transkripte (Pflicht) — MIT-Lizenz
pip install yt-dlp                   # Metadaten (optional, Fallback: noembed) — Unlicense (Public Domain)
```

## الاستخدام

> **ملاحظة لنظام Windows:** اضبط دائمًا `PYTHONIOENCODING=utf-8`، وإلا ستتعطل الحروف المميزة
> والرموز الخاصة في المخرجات (ترميز cp1252).

```bash
# Standard: Markdown mit Timestamps
PYTHONIOENCODING=utf-8 python video_transcriber.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Ausgabeformat waehlen
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --format markdown|json|plain

# In Datei speichern
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o transcript.md

# Sprachen bevorzugen (Default: de en)
PYTHONIOENCODING=utf-8 python video_transcriber.py URL --lang de en fr
```

### الخيارات

| الخيار | الأثر |
|--------|-------|
| `--format markdown\|json\|plain` | صيغة الإخراج (الافتراضي: markdown) |
| `--output, -o <datei>` | الكتابة إلى ملف بدلًا من stdout |
| `--lang <codes...>` | لغات الترجمة المفضلة (الافتراضي: de en) |
| `--meta-only` | البيانات الوصفية فقط، دون نص |
| `--transcript-only` | النص فقط، دون بيانات وصفية |
| `--no-timestamps` | النص دون الطوابع الزمنية |
| `--no-meta` | أسرع: تخطَّ البيانات الوصفية من yt-dlp |
| `--allow-empty-transcript` | اعتبر النص الفارغ نجاحًا (الخروج 0 بدلًا من 3) |

### رموز الخروج

النص الفارغ **ليس** نجاحًا. قبل الإصدار 1.2.0، كان هذا الحال ينتهي بالخروج 0: يُكتب ملف
الإخراج، ومصفوفة المقاطع فارغة، وكان كل برنامج آلي يستدعي الأداة يعدّ ذلك ناجحًا. هذا الفشل
الصامت هو العيب الحقيقي الذي أزاله الإصدار 1.2.0.

| الرمز | المعنى |
|-------|--------|
| `0` | نجاح — يوجد نص، أو `--meta-only`، أو `--allow-empty-transcript` |
| `1` | عنوان URL أو معرّف فيديو غير صالح |
| `2` | خطأ في الاستدعاء (تُصدره argparse، مثل خيار غير معروف) |
| `3` | لم يُستلم أي نص — المساران فارغان |

يبقى `2` محجوزًا لـ argparse، حتى يمكن التمييز بين خطأ مطبعي في الاستدعاء
وفيديو لا يحتوي على ترجمات.

```bash
# In Skripten
PYTHONIOENCODING=utf-8 python video_transcriber.py URL -o out.md || {
  code=$?
  [ "$code" -eq 3 ] && echo "Video hat keine Untertitel" || echo "Fehler: $code"
}
```

### كمكتبة Python

```python
from video_transcriber import extract_video_id, fetch_metadata, fetch_transcript, format_markdown

video_id = extract_video_id("https://www.youtube.com/watch?v=VIDEO_ID")
meta = fetch_metadata(video_id)
transcript = fetch_transcript(video_id, languages=["de", "en"])
output = format_markdown(meta, transcript)

# Immer pruefen -- fetch_transcript wirft nicht, es meldet:
if not transcript["segments"]:
    raise RuntimeError(transcript["error"])
print(transcript["source"])  # "youtube_transcript_api" oder "yt-dlp"
```

المساران قابلان للاستدعاء منفصلين: `fetch_transcript_primary()` (المسار الأساسي
`youtube-transcript-api` فقط) و`fetch_transcript_ytdlp()` (المسار البديل فقط). تربط `fetch_transcript()`
بينهما وتضمن الحقول `segments` و`language` و`is_generated`
و`full_text` و`source`، وفي حالة الخطأ الحقل `error`.

## حالات الاستخدام الشائعة

- البحث: الاستفادة من محتوى الفيديو كنص قابل للاستشهاد
- تحليل المصادر: دراسة الحجج والاستعارات في المحاضرات
- الملخصات: اتخاذ النص المفرَّغ أساسًا موثوقًا بدلًا من الاختلاق

## القيود

- تعمل الأداة فقط إذا كان للفيديو ترجمات (يدوية أو تلقائية)
- قد تحتوي الترجمات التلقائية على أخطاء في التعرف على الكلام
- لا يوجد تنزيل للصوت، ولا تعرّف مستقل على الكلام؛ حتى المسار البديل يحمّل
  مسار الترجمة فقط، ولا يحمّل الفيديو أو الصوت أبدًا
- يحتاج المسار البديل إلى مسار JSON3؛ فإذا لم تقدّم المنصة سوى صيغ أخرى، ينتهي التشغيل
  بالخروج 3 بدلًا من إخراج جزئي

## سجل التغييرات

### 1.2.0 (2026-08-24)
- **دلالات الخروج:** ينتهي النص الفارغ بالخروج `3` بدلًا من أن يمر بصمت
  بالخروج `0`. صار عنوان URL غير الصالح `1` كثابت مسمّى. يبقى
  `--meta-only` ناجحًا لأنه لا يُتوقع فيه نص.
- **خيار جديد `--allow-empty-transcript`:** يعتبر النص الفارغ نجاحًا عن قصد — لمن يستدعون
  الأداة ويعاملون الترجمات كأمر اختياري.
- **مسار الترجمة البديل عبر yt-dlp:** يتدخل متى لم ينتج المسار الأساسي أي مقاطع
  (لا عند الاستثناء فقط). يستخدم `extract_info(download=False)`
  ويقرأ عنوان URL للترجمة فقط — لا فيديو، ولا صوت، ولا تجاوز لقيود الوصول.
- **تشديد اختيار اللغة:** يُعثر على مسارات `de-orig`/`de-DE` عند استخدام `--lang de`
  (مطابقة اللغة الأساسية). تبقى الترجمات اليدوية مقدَّمة على التلقائية.
- **الحقل `source`** في النتيجة: `youtube_transcript_api` أو `yt-dlp`.
- اختبارات الانحدار: 29 اختبارًا باستجابات محاكاة (UTF-8، والصيغ الثلاث للإخراج،
  ورموز الخروج، واختيار اللغة، وتحليل JSON3).

### 1.1.0 (2026-06-20)
- أعيدت التسمية من `yt-transcriber` إلى `video-transcriber` (إرشادات علامة YouTube التجارية:
  „yt" اختصار محظور صراحةً؛ التوصية: RECHTSCHECK_2026-06-20.md)
- السكربت: من `yt_transcriber.py` إلى `video_transcriber.py`
- إضافة التنبيه وتراخيص التبعيات (مسؤولية المستخدم، وشروط الخدمة، وعدم الاعتماد)
- ذُكرت YouTube الآن كمصدر وصفي فقط، لا كجزء من الاسم أو العلامة التجارية
- أُبقي الغلاف المتوافق مع الإصدارات السابقة `yt_transcriber.py` على المسار القديم

### 1.0.0 (2026-06-12)
- أُضيف ملف SKILL.md (كانت الأداة موجودة كسكربت وREADME من قبل)
- السكربت الإصدار 1.0.0: نص + بيانات وصفية، و3 صيغ إخراج، وتفضيلات لغوية
