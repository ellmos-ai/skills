---
name: medizin-daten
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "التقاط محلي وخاص للبيانات الطبية: التشخيصات وتاريخ الأعراض وخطط الفحص. ليس له أصل في BACH — تصميم مخصص مع مخزن SQLite خاص به. محلي بصرامة، دون نقل إلى السحابة."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [medizin, diagnose, symptome, gesundheit, privat, lokal]
language: ar
status: stable
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin. Skill vollständig neu konzipiert. Kein bestehendes Implementierungs-Vorbild im Ökosystem gefunden.\n'}
translated_from_sha256: b345b47fc6f0ea659604ac06a0d5bda40fadb7770d2f3b2899ce95ccb9ee463c
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.977053+00:00"
---
<img src="banner.png" width="100%" alt="medizin-daten banner">

## الغرض

جمع البيانات الصحية الشخصية بأمان ومحليًا: التشخيصات (رمز ICD-10 اختياري)، وتسلسلات الأعراض بتواريخها، وخطط الفحوصات. تبقى جميع البيانات محصورة محليًا في `medizin-daten/store.db`.

لا تحل المهارة محل الاستشارة الطبية ولا تُدلي بأي تصريحات طبية — إنها دفتر ملاحظات منظم لبيانات الصحة الشخصية.

---

## المحفزات

| العبارة | الإجراء |
|---|---|
| „تسجيل تشخيص" | إنشاء تشخيص جديد |
| „إضافة تشخيص [الاسم]" | إنشاء تشخيص مسمّى |
| „تسلسل الأعراض" | تسجيل أعراض اليوم |
| „تسجيل عرض [الاسم]" | إدخال عرض واحد |
| „خطة الفحوصات" | عرض المواعيد/الفحوصات التالية |
| „إضافة موعد" | إدخال موعد فحص |
| „أرني تشخيصاتي" | إخراج قائمة التشخيصات |

---

## سير العمل

1. **التعرف على الوضع**: تشخيص / عرض / خطة فحوصات
2. **تنظيم المدخلات**: التاريخ، التسمية، الملاحظات، رمز ICD-10 الاختياري
3. **الحفظ**: في `store.db` (محليًا، دون وصول إلى الشبكة)
4. **الإخراج**: ملخص مقروء لسياق LLM

---

## نقطة دخول سطر الأوامر

```bash
# Diagnose anlegen
python medizin_daten_core.py add-diagnosis "Hypertonie" [--icd I10] [--note "Anmerkung"]

# Diagnosen auflisten
python medizin_daten_core.py diagnoses

# Symptom erfassen
python medizin_daten_core.py add-symptom "Kopfschmerzen" [--severity 7] [--date 2026-06-22] [--note "..."]

# Symptomverlauf für eine Bezeichnung
python medizin_daten_core.py symptom-history "Kopfschmerzen" [--limit 30]

# Untersuchung planen
python medizin_daten_core.py add-exam "Blutbild" [--date 2026-07-01] [--note "nüchtern"]

# Anstehende Untersuchungen
python medizin_daten_core.py exams [--upcoming]

# Alternativer Store (z.B. für Tests)
python medizin_daten_core.py --store /tmp/med_test.db diagnoses --dry-run
```

---

## المخزن

| الخاصية | القيمة |
|---|---|
| النوع | SQLite |
| المسار (الافتراضي) | `skills/assist/medizin-daten/store.db` |
| التجاوز | `--store <pfad>` أو متغير البيئة `MEDIZIN_STORE` |
| الجداول | `diagnoses`، `symptoms`، `examination_plans` |

### المخطط

```sql
CREATE TABLE IF NOT EXISTS diagnoses (
    id          TEXT PRIMARY KEY,     -- UUID (kurz: 8 Hex)
    name        TEXT NOT NULL,        -- Bezeichnung (z.B. "Hypertonie")
    icd_code    TEXT,                 -- ICD-10-Code optional (z.B. "I10")
    onset_date  TEXT,                 -- Beginn (ISO-8601, optional)
    status      TEXT DEFAULT 'aktiv', -- aktiv | remission | abgeschlossen
    note        TEXT,                 -- Freitext-Notiz
    created_at  TEXT NOT NULL,
    updated_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS symptoms (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    name         TEXT NOT NULL,       -- Bezeichnung (z.B. "Kopfschmerzen")
    severity     INTEGER,             -- 1–10 Skala (optional)
    recorded_at  TEXT NOT NULL,       -- ISO-8601 Zeitstempel
    note         TEXT
);

CREATE TABLE IF NOT EXISTS examination_plans (
    id           TEXT PRIMARY KEY,
    diagnosis_id TEXT REFERENCES diagnoses(id),  -- optional: Zuordnung
    exam_name    TEXT NOT NULL,       -- Untersuchungsbezeichnung
    planned_date TEXT,                -- Geplantes Datum (ISO-8601)
    done_date    TEXT,                -- Durchgeführt am (NULL = ausstehend)
    note         TEXT,
    created_at   TEXT NOT NULL
);
```

---

## المنهجية

- لا توصيات طبية، ولا تشخيص من قبل المهارة.
- تُخزَّن رموز ICD-10 كنص حر — دون تحقق مقابل قاعدة بيانات خارجية.
- مقياس الشدة من 1 إلى 10 ذاتي وفق تقدير المستخدم.
- القيم المفقودة (التاريخ، درجة الشدة) مسموح بها دائمًا — فمبدأ دفتر الملاحظات ساري.

---

## الخصوصية (بوابة الخصوصية)

> **تحذير: البيانات الطبية تستحق حماية خاصة.**

- `store.db` يحتوي على بيانات صحية شديدة الحساسية — **لا تُودِع في Git مطلقًا**.
- **لا وصول إلى الشبكة** — تعمل جميع العمليات محليًا بالكامل.
- **لا نقل** إلى خدمات خارجية، ولا مزامنة مع خوادم سحابية.
- توصية النسخ الاحتياطي: نسخة محلية مشفّرة (مثل `age`/`gpg`).
- تتحقق المهارة عند البدء مما إذا كان `store.db` خارج نظام الملفات المحلي،
  وتُصدر تحذيرًا إذا كان المسار داخل مجلد مزامنة (OneDrive أو غيره).
- ينبغي أن يستثني `~/.gitignore_global` أو `.gitignore` المحلي `store.db`.

---

## الموارد ذات الصلة

- المهارة `assist/gesundheit` — مساعدة صحية عامة (ليست بيانات طبية)
- MediPlaner (`tools/module-installer` ← `mediplaner`) — إدارة الأدوية (برنامج منفصل)

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 0.1.0 | 2026-06-22 | الإنشاء الأولي — تصميم خاص، بوابة الخصوصية، مخطط من ثلاثة جداول |
