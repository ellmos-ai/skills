---
name: bewerbungsexperte
version: 1.1.0
type: expert
author: BACH Team / ellmos (standalone port)
created: 2026-01-25
updated: 2026-06-22
description: "خبير متخصص في عملية التقديم للوظائف بأكملها. يحلل إعلانات الوظائف، ويحسّن الملفات الشخصية (LinkedIn/السيرة الذاتية)، ويُنشئ خطابات تغطية مخصصة. يُولّد سير ذاتية بتنسيق ASCII من قاعدة بيانات SQLite وبنية المجلدات. تم نقل cv_generator.py بشكل مستقل -- لا حاجة إلى وقت تشغيل BACH."
standalone: true
anthropic_compatible: true
bach_compatible: true
bach_origin: true
category: utilities
tags: [bewerbung, cv, anschreiben, linkedin]
language: ar
status: active
visibility: public
dependencies: {'tools': ['cv_generator.py'], 'services': [], 'protocols': [], 'python': ['sqlite3', 'pathlib', 'argparse', 're']}
provenance: {'origin': 'bach', 'origin_path': 'system/agents/_experts/bewerbungsexperte/', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': 'None', 'local_changes_since_sync': True}
translated_from_sha256: c71218b5c90eba7666db1a407dc59752fa0e2eccd342deb8b728fba82d967e54
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="bewerbungsexperte banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.

> **English Translation** — Official English version of `bewerbungsexperte`.

# خبير التقديم للوظائف v1.1 (الألمانية)

> شريكك الاستراتيجي للخطوة المهنية القادمة.

## التفعيل

```bash
# Beispiel-CV ohne Datenbankzugriff (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --dry-run

# CV aus SQLite-Datenbank generieren (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad/zu/daten.db>

# CV in Datei speichern (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --output lebenslauf.txt

# Mit Ordner-Scan (Deutsch)
PYTHONDONTWRITEBYTECODE=1 python cv_generator.py --db <pfad> --career-path <ordner>
```


## كتالوج الخدمات

### 1. توليد السيرة الذاتية (`cv_generator.py`)
- **البيانات الشخصية:** القراءة من جدول `assistant_user_profile` (المفتاح/القيمة)
- **الخبرة المهنية:** فحص مجلد أصحاب العمل (شهادات الخبرة وعقود العمل)
- **التعليم:** فحص مجلد المؤهلات الدراسية
- **التدريب المستمر:** فحص مجلد شهادات الدورات التدريبية
- **المراجع:** من جدول `contacts` (category='beruflich')
- **التشغيل التجريبي:** بدون قاعدة بيانات -- بيانات نموذجية للاختبار

### 2. تشخيص الوظيفة
- **مطابقة الكلمات المفتاحية:** مقارنة السيرة الذاتية بمتطلبات الوظيفة (متوافق مع ATS)
- **فحص الشركة:** البحث في ثقافة الشركة والمزايا

### 3. خدمة المستندات
- **تحسين السيرة الذاتية:** تنظيم الخبرات وتركيزها
- **خطاب التغطية:** إعداد خطابات فردية ومقنعة
- **الملف الاستعراضي:** الاستشارة بشأن نماذج العمل والمراجع

## جداول قاعدة البيانات (اختيارية)

`cv_generator.py` يقرأ من هذه الجداول عند توفرها:

- `assistant_user_profile` (key TEXT, value TEXT) — البيانات الشخصية
  - الحقول: name, full_name, email, phone, address, birthday, nationality, marital_status
- `contacts` (name, organization, position, phone, email, is_active, category) — المراجع

يتم تجاهل الجداول المفقودة (أقسام فارغة في السيرة الذاتية).

## بنية المجلدات (لـ --career-path وغيره)

```
_Arbeitgeber/
  Firma_A_2020-2023/
    Arbeitsvertrag.pdf
    Arbeitszeugnis.pdf
  Firma_B_2018-2020/
    ...
_Abschluesse/
  Universitaet/
    Bachelor_Zeugnis.pdf
_Fortbildungen/
  Zertifikat_Cloud_AWS_2024.pdf
```


## خيارات سطر الأوامر

```
--db <pfad>           Pfad zur SQLite-Datenbank (Pflicht ohne --dry-run)
--output, -o          Ausgabedatei (ansonsten stdout)
--career-path         Pfad zum Arbeitgeber-Ordner
--education-path      Pfad zum Abschluesse-Ordner
--certs-path          Pfad zum Fortbildungen-Ordner
--dry-run             Beispiel-CV ohne Datenbankzugriff
```


## سير العمل: توليد السيرة الذاتية

1. **التحضير**
   - توفير قاعدة بيانات SQLite (قاعدة BACH أو قاعدة خاصة)
   - إنشاء بنية المجلدات مع المستندات (اختياري)

2. **الاختبار بدون قاعدة بيانات**
   - `python cv_generator.py --dry-run` -- يتحقق من عمل الأداة

3. **التوليد**
   - `python cv_generator.py --db <pfad> --career-path <arbeitgeber>`
   - مراجعة المخرجات وتعديلها عند الحاجة

4. **التصدير**
   - `python cv_generator.py --db <pfad> --output lebenslauf.txt`

## التبعيات

مكتبة Python القياسية فقط: `sqlite3`، `pathlib`، `argparse`، `re`، `datetime`.
لا حاجة إلى تثبيت pip، ولا استيراد وقت تشغيل BACH.

## سجل التغييرات

### 1.1.0 (2026-06-22)
- نُقل بشكل مستقل من BACH v1.0.0
- `--db <pfad>` بدلاً من مسار قاعدة البيانات الأصلية المرمّز
- أُضيف وضع `--dry-run`
- أُزيل `--scan-folders` (كان يتطلب جدول user_data_folders في BACH)
- حُيّد نص التذييل
- تم التحقق من استقلالية وقت تشغيل BACH

### 1.0.0 (2026-01-25, داخلي في BACH)
- الإصدار الأولي في BACH system/agents/_experts/bewerbungsexperte/

---
الحالة: نشط
المجال: الاستشارات المهنية
