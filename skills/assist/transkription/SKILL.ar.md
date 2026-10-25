---
name: transkription
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "يحوّل ملفات الصوت والفيديو إلى نص. يستخدم Whisper (openai-whisper) أو Vosk (دون اتصال بالإنترنت) كخلفية اختيارية — ويُكتشف كلاهما عبر فحص الوجود. بدون خلفية: وضع العنصر النائب بمخرجات وهمية (تشغيل تجريبي)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [transkription, audio, speech-to-text, whisper, vosk, offline]
language: ar
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': [{'name': 'openai-whisper', 'optional': True, 'install': 'pip install openai-whisper', 'purpose': 'STT backend option 1 (cloud/local model)'}, {'name': 'vosk', 'optional': True, 'install': 'pip install vosk', 'purpose': 'STT backend option 2 (fully offline)'}]}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein direkter BACH-Origin vorhanden (transkriptions-service existiert nicht als Datei in BACH/system). Skill neu konzipiert. voice_stt.py aus BACH/hub/_services/voice/ hat das Backend-Muster inspiriert (optionale Imports mit Verfügbarkeits-Flags), wurde aber nicht direkt portiert.\n'}
translated_from_sha256: a65e028046b1d74694d3835cfe35daeab1bc4f0f259665d6e5a8647fd0fff859
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="transkription banner">

## الغرض

تحويل ملفات الصوت/الفيديو إلى نص — محليًا، دون الحاجة إلى السحابة. تكتشف المهارة بنفسها ما إذا كان Whisper أو Vosk مثبتًا، ويختار أفضل خلفية متاحة. بدون خلفية تعمل في وضع التشغيل التجريبي وتعيد نصًا عنصرًا نائبًا، بحيث يعمل سير العمل دائمًا.

تُخزَّن النصوص المفرّغة محليًا في `transkription/store.db` ويمكن الاستعلام عنها.

---

## المشغّلات

| العبارة | الإجراء |
|---|---|
| „Transkribiere diese Audio" / فرّغ هذا الملف الصوتي | تفريغ ملف الصوت |
| „Transkribiere [Datei]" / فرّغ [الملف] | تفريغ الملف المسمّى |
| „Zeig meine Transkripte" / أظهر نصوصي المفرّغة | عرض قائمة النصوص المفرّغة الأخيرة |
| „Suche Transkript [Begriff]" / ابحث في النصوص المفرّغة عن [المصطلح] | البحث النصي الكامل في النصوص المفرّغة |
| „Exportiere Transkript [ID]" / صدّر النص المفرّغ [ID] | تصدير النص المفرّغ كملف TXT |

---

## سير العمل

1. **فحص الخلفية**: التحقق مما إذا كان `whisper` أو `vosk` قابلًا للاستيراد.
2. **فحص الملف**: يجب أن يكون ملف الإدخال موجودًا (صوت: wav وmp3 وm4a وogg وflac؛ فيديو: mp4 وmkv وwebm — الاستخراج عبر ffmpeg).
3. **التفريغ**: استدعاء الخلفية والحصول على النص الخام.
4. **الحفظ**: تخزين النتيجة مع البيانات الوصفية (الملف، المدة، اللغة، الخلفية، الطابع الزمني) في `store.db`.
5. **المخرجات**: إعادة النص؛ ويمكن اختياريًا تصديره بصيغة `.txt`.

---

## نقطة الدخول عبر سطر الأوامر

```bash
# Datei transkribieren
python transkription_core.py transcribe audio.wav

# Mit expliziter Sprache
python transkription_core.py transcribe audio.mp3 --lang de

# Dry-Run (kein Backend nötig)
python transkription_core.py transcribe audio.wav --dry-run

# Transkripte auflisten
python transkription_core.py list [--limit 20]

# Volltextsuche
python transkription_core.py search "Begriff"

# Exportieren
python transkription_core.py export <id> [--out datei.txt]

# Backend-Check
python transkription_core.py check

# Alternativer Store-Pfad (z.B. für Tests)
python transkription_core.py --store /tmp/test.db transcribe audio.wav --dry-run
```

---

## المخزن

| الخاصية | القيمة |
|---|---|
| النوع | SQLite |
| المسار (الافتراضي) | `skills/assist/transkription/store.db` |
| التجاوز | `--store <pfad>` أو المتغير البيئي `TRANSKRIPTION_STORE` |
| الجداول | `transcripts` |

### المخطط `transcripts`

```sql
CREATE TABLE IF NOT EXISTS transcripts (
    id          TEXT PRIMARY KEY,  -- UUID (kurz: 8 Hex)
    file_path   TEXT NOT NULL,     -- Originalpfad der Audiodatei
    file_name   TEXT NOT NULL,     -- Dateiname (ohne Pfad, für Anzeige)
    text        TEXT NOT NULL,     -- Transkribierter Text
    language    TEXT,              -- Sprache (z.B. "de", "en")
    backend     TEXT,              -- "whisper" | "vosk" | "dry-run"
    duration_s  REAL,              -- Dauer in Sekunden (wenn bekannt)
    created_at  TEXT NOT NULL,     -- ISO-8601 Timestamp
    tags        TEXT               -- Komma-getrennte Tags (optional)
);
```

---

## المبادئ

- بدون خلفية مثبتة تعمل المهارة في وضع التشغيل التجريبي (نص توضيحي).
- يُفضَّل Whisper على Vosk (جودة أفضل للغة الألمانية).
- يمكن تحديد الاختيار بين Whisper وVosk عبر `assist/prefs.json` (`transkription_backend: "whisper"|"vosk"|"auto"`).
- يجب تثبيت ffmpeg بشكل منفصل لاستخراج الصوت من الفيديو، وهو غير مضمّن في المهارة.

---

## الخصوصية

- **تبقى جميع النصوص المفرّغة محلية** — لا نقل إلى السحابة ما لم يُستخدم وضع Whisper عبر الإنترنت.
- يمكن تشغيل Whisper محليًا (نموذج tiny/base/medium) أو عبر واجهة OpenAI البرمجية.
  يُستخدم النموذج المحلي افتراضيًا.
- يحتوي `store.db` على محتوى محادثات قد يكون حساسًا — **لا ترفعه إلى Git**.
- التوصية: إضافة `store.db` إلى `.gitignore`.

---

## الموارد ذات الصلة

- BACH `hub/_services/voice/voice_stt.py` — أنماط الخلفية (إلهام، للقراءة فقط)
- المهارة `utilities/yt-transcriber` — تفريغ YouTube (مهارة منفصلة، ليست نسخة مكررة: خاصة بـYouTube)
- `tools/module-installer/module_installer.py` — يحتوي السجل على whisper وvosk

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 0.1.0 | 2026-06-22 | الإنشاء الأولي — مخزن SQLite خاص، فحص وجود Whisper/Vosk |
