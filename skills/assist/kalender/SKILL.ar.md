---
name: kalender
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "مهارة تقويم مع اختيار الواجهة الخلفية حسب تفضيل المستخدم (العلامة 3). الافتراضي: مخزن SQLite محلي. اختياري: Google Calendar MCP أو Routinika أو UpToday كواجهة خلفية — يُتحكم بها عبر assist/prefs.json. وفي حال عدم وجود تفضيل يسأل نموذج اللغة المستخدم تفاعلياً."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
category: assist
tags: [kalender, termine, events, ics, google-calendar, routinika]
language: ar
status: stable
visibility: public
dependencies: {'tools': [], 'services': [{'name': 'Google Calendar MCP', 'optional': True, 'purpose': 'Backend option when kalender_backend=google in prefs.json'}], 'protocols': [{'name': 'ICS / iCalendar', 'optional': True, 'purpose': 'Import/export of appointments (RFC 5545 subset)'}], 'python': []}
provenance: {'origin': 'eigenentwurf', 'origin_path': '', 'origin_version': '', 'origin_repo': '', 'origin_license': 'MIT', 'last_sync_from_origin': '', 'notes': 'Kein BACH-Origin gefunden (kein kalender-Service in BACH/system/). Skill vollständig neu konzipiert mit Flag-3-Logik (user-adaptive backend). ICS-Felder angelehnt an RFC 5545, kein externer ICS-Parser benötigt.\n'}
translated_from_sha256: 3dd9e7b8d86095d63dd54e3d9c4c3b825eef0dd3affffd992b54bbc8a03cdd7e
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.378053+00:00"
---
<img src="banner.png" width="100%" alt="kalender banner">

## الغرض

تسجيل المواعيد والاستعلام عنها وإدارتها — مع واجهة خلفية قابلة للاختيار. تعمل النواة (`kalender_core.py`) دائماً بـ**مخزن SQLite المحلي** كخيار افتراضي. يختار نموذج اللغة عند الحاجة واجهة خلفية بديلة استناداً إلى `assist/prefs.json`.

**العلامة 3 — اختيار الواجهة الخلفية:**

| `kalender_backend` في prefs.json | السلوك |
|---|---|
| `local` (الافتراضي) | مخزن SQLite في مجلد المهارة هذا |
| `google` | Google-Calendar-MCP (مسار نموذج اللغة فقط، وليس في core.py) |
| `routinika` | تقويم Routinika عبر module-installer (غير مُنفَّذ في الإصدار 0.1) |
| `uptoday` | تقويم UpToday عبر module-installer (غير مُنفَّذ في الإصدار 0.1) |
| غير مُعيَّنة | يسأل نموذج اللغة المستخدم تفاعلياً عن الواجهة الخلفية المفضلة |

> `kalender_core.py` يُنفِّذ حصرياً الواجهة الخلفية `local`.
> Google-Calendar-MCP والواجهات الخلفية الأخرى يتحكم بها نموذج اللغة، وتُوثَّق
> في SKILL.md وليس في النواة.

---

## المحفزات

| العبارة | الإجراء |
|---|---|
| „أضف موعدًا" | تسجيل موعد جديد |
| „ما المواعيد اليوم؟" | الاستعلام عن مواعيد اليوم |
| „ما المواعيد هذا الأسبوع؟" | نظرة عامة على 7 أيام |
| „موعد [العنوان] في [التاريخ]" | إنشاء موعد بتاريخ |
| „جميع المواعيد في [الشهر]" | نظرة شهرية |
| „احذف الموعد [ID]" | حذف موعد |
| „صدّر المواعيد" | تصدير ICS لجميع المواعيد أو لموعد محدد |

---

## سير العمل

1. **فحص الواجهة الخلفية**: قراءة `assist/prefs.json` ← `kalender_backend`.
2. **دون تفضيل**: يسأل نموذج اللغة المستخدم: تقويم محلي، أم Google Calendar، أم غيره؟
3. **الواجهة المحلية**: core.py — إنشاء/استعلام/حذف الموعد في مخزن SQLite.
4. **واجهة Google**: يستدعي نموذج اللغة Google-Calendar-MCP مباشرةً (لا يشارك core.py).
5. **المخرجات**: قائمة مواعيد مقروءة أو تأكيد.

---

## نقطة الدخول عبر سطر الأوامر

```bash
# Termin anlegen
python kalender_core.py add "Zahnarzt" --date 2026-07-01 --time 10:00 [--duration 60] [--location "Praxis Dr. X"]

# Heutige Termine
python kalender_core.py today

# Wochenübersicht
python kalender_core.py week [--from 2026-06-22]

# Monatsübersicht
python kalender_core.py month [--month 2026-07]

# Alle Termine (optional mit Suchbegriff)
python kalender_core.py list [--search "Zahnarzt"] [--limit 50]

# Termin löschen
python kalender_core.py delete <id>

# ICS-Export
python kalender_core.py export [--id <id>] [--out kalender.ics]

# Backend-Check
python kalender_core.py check-backend

# Alternativer Store (z.B. für Tests)
python kalender_core.py --store /tmp/kal_test.db today --dry-run
```

---

## المخزن

| الخاصية | القيمة |
|---|---|
| النوع | SQLite (الواجهة المحلية) |
| المسار (الافتراضي) | `skills/assist/kalender/store.db` |
| التجاوز | `--store <pfad>` أو المتغير البيئي `KALENDER_STORE` |
| الجداول | `events` |

### المخطط

```sql
CREATE TABLE IF NOT EXISTS events (
    id           TEXT PRIMARY KEY,      -- UUID (kurz: 8 Hex)
    title        TEXT NOT NULL,         -- Termin-Bezeichnung
    date         TEXT NOT NULL,         -- ISO-Datum YYYY-MM-DD
    time         TEXT,                  -- HH:MM (optional)
    duration_min INTEGER,               -- Dauer in Minuten (optional)
    location     TEXT,                  -- Ort (optional)
    description  TEXT,                  -- Notiz/Beschreibung
    recurrence   TEXT,                  -- ICS RRULE (optional, z.B. "FREQ=WEEKLY")
    ics_uid      TEXT UNIQUE,           -- ICS UID für Import/Export
    created_at   TEXT NOT NULL,
    updated_at   TEXT NOT NULL
);
```

---

## المنهجية

- تُنفِّذ النواة فقط الواجهة الخلفية `local` — خفيفة الوزن، بلا تبعيات خارجية.
- يُنتج تصدير ICS مجموعة فرعية صالحة من RFC 5545 (VCALENDAR + VEVENT)، قابلة للاستيراد في جميع تطبيقات التقويم الشائعة.
- استيراد ICS (التحليل) غير مُنفَّذ بعد في الإصدار 0.1 — مخطط له في الإصدار 0.2.
- تُخزَّن قواعد التكرار (`recurrence`/RRULE) لكنها لا تُفسَّر — التفسير مُخطَّط له في الإصدار 0.2.

---

## حماية البيانات

- تبقى المواعيد المحلية في `store.db` — لا وصول إلى الشبكة في النواة.
- في مسار الواجهة الخلفية لـ Google Calendar تُعالج Google-Calendar-MCP البيانات — وتسري سياسات خصوصية Google.
- لا يُرفع `store.db` إلى Git (يُوصى بـ `.gitignore`).

---

## موارد ذات صلة

- Google-Calendar-MCP (`mcp__claude_ai_Google_Calendar__*`) — واجهة خلفية بديلة يتحكم بها نموذج اللغة
- المهارة `assist/haushalt-manager` — تكامل Routinika (نمط فحص الحضور)
- `tools/module-installer/module_installer.py` — لتكامل الواجهات الخلفية المستقبلية Routinika/UpToday

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 0.1.0 | 2026-06-22 | إنشاء أولي — منطق العلامة 3، والواجهة المحلية، وتصدير ICS |
