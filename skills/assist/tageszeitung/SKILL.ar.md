---
name: tageszeitung
version: 0.1.0
type: assist
author: ellmos-ai
created: 2026-06-22
updated: 2026-06-22
description: "ينشئ صحيفة يومية مخصّصة من خلاصات RSS ومصادر الويب. مُنقولة من نظام أخبار BACH (news.py + newspaper_generator.py). متجر SQLite خاص (بدون Origin-DB). feedparser اختياري — احتياطي XML عبر المكتبة القياسية. تصدير PDF عبر Edge Headless (msedge.exe)."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: assist
tags: [zeitung, news, rss, feed, pdf, tageszeitung]
language: ar
status: stable
visibility: public
dependencies: {'tools': [{'name': 'msedge.exe', 'optional': True, 'purpose': 'HTML → PDF (Edge Headless); without Edge: HTML output only'}], 'services': [], 'protocols': [], 'python': [{'name': 'feedparser', 'optional': True, 'install': 'pip install feedparser', 'purpose': 'RSS parsing (main backend). Fallback: defusedxml → regex'}, {'name': 'defusedxml', 'optional': True, 'install': 'pip install defusedxml', 'purpose': 'XXE-safe XML parser as fallback when feedparser is missing. Without defusedxml a regex fallback is used (no ET.fromstring on network data).'}]}
provenance: {'origin': 'bach-port', 'origin_path': 'BACH/system/hub/news.py + hub/_services/newspaper/newspaper_generator.py', 'origin_version': 'news.py v1.x, newspaper_generator.py v1.x', 'origin_repo': 'ellmos-ai/bach (privat)', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'notes': 'Schema (news_sources + news_items) 1:1 aus BACH news.py portiert. BaseHandler-Abhängigkeit entfernt. Origin-DB-Pfad entfernt. DB-Pfad konfigurierbar. newspaper_generator.py-Logik (HTML-Render + Edge-PDF) userneutral übernommen.\n'}
translated_from_sha256: e42d847ea203fa764315a96678ddf6b5814633dd363b9ee8f9fbf87a4af5cce8
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="tageszeitung banner">

## الغرض

جلب المقالات من خلاصات RSS ومصادر الويب المُعدّة، وفرزها حسب الفئات، وعرضها كصحيفة يومية بصيغة HTML/PDF. تُخزَّن المقالات محليًا في `tageszeitung/store.db` وتُوسَم بأنها مقروءة.

---

## المشغّل

| العبارة | الإجراء |
|---|---|
| „Erstell meine Tageszeitung" / «أنشئ صحيفتي اليومية» | جلب المقالات + عرض PDF |
| „Tageszeitung für heute" / «صحيفة اليوم» | عرض صحيفة اليوم |
| „Füge Feed hinzu [URL]" / «أضف خلاصة [URL]» | تسجيل مصدر RSS |
| „Zeig meine Quellen" / «اعرض مصادري» | عرض قائمة المصادر |
| „Fetch News" / «اجلب الأخبار» | جلب جميع المصادر (بدون عرض) |

---

## سير العمل

1. **فحص المصادر**: قراءة جميع المصادر النشطة من `news_sources`.
2. **الجلب**: RSS عبر feedparser (أو احتياطي xml.etree)، والويب عبر urllib.
3. **إزالة التكرار**: يمنع UNIQUE(source_id, url) تكرار المقالات.
4. **العرض**: تجميع المقالات غير المقروءة حسب الفئة ← HTML ← PDF.
5. **التسليم**: وضع ملفات HTML/PDF في مجلد الإخراج (مسار قابل للتهيئة).

---

## نقطة الدخول عبر سطر الأوامر

```bash
# Quelle hinzufügen
python tageszeitung_core.py add-source "Heise" rss https://www.heise.de/rss/heise-atom.xml --category tech

# Alle Quellen abrufen
python tageszeitung_core.py fetch

# Tageszeitung rendern (HTML + PDF wenn Edge verfügbar)
python tageszeitung_core.py render [--date 2026-06-22] [--out /pfad/]

# Quellen auflisten
python tageszeitung_core.py sources

# Ungelesene Artikel
python tageszeitung_core.py items [--limit 50] [--category tech]

# Artikel als gelesen markieren
python tageszeitung_core.py read <item_id>

# Alternativer Store (z.B. für Tests)
python tageszeitung_core.py --store /tmp/t.db sources --dry-run
```

---

## المتجر

| الخاصية | القيمة |
|---|---|
| النوع | SQLite |
| المسار (الافتراضي) | `skills/assist/tageszeitung/store.db` |
| التجاوز | `--store <pfad>` أو المتغير البيئي `TAGESZEITUNG_STORE` |
| الجداول | `news_sources`، `news_items` |

### المخطط (مُنقول من news.py في BACH)

```sql
CREATE TABLE IF NOT EXISTS news_sources (
    id           TEXT PRIMARY KEY,
    name         TEXT NOT NULL,
    type         TEXT NOT NULL DEFAULT 'rss',  -- rss | web
    url          TEXT NOT NULL UNIQUE,
    category     TEXT DEFAULT 'Allgemein',
    schedule     TEXT DEFAULT 'daily',
    is_active    INTEGER DEFAULT 1,
    last_fetched TEXT,
    fetch_count  INTEGER DEFAULT 0,
    error_count  INTEGER DEFAULT 0,
    last_error   TEXT,
    created_at   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS news_items (
    id           TEXT PRIMARY KEY,
    source_id    TEXT NOT NULL REFERENCES news_sources(id),
    title        TEXT NOT NULL,
    content      TEXT,
    summary      TEXT,
    url          TEXT,
    author       TEXT,
    published_at TEXT,
    fetched_at   TEXT NOT NULL,
    is_read      INTEGER DEFAULT 0,
    category     TEXT,
    UNIQUE(source_id, url)
);
```

---

## مبادئ التشغيل

- يُفضَّل feedparser؛ وبدونه يُستخدم احتياطي xml.etree لخلاصات RSS 2.0 البسيطة.
- يتطلب إنشاء PDF وجود `msedge.exe` في مسار النظام PATH أو المتغير البيئي `MSEDGE_PATH`. وبدون Edge يُنشأ HTML فقط.
- الحد الأقصى للمقالات لكل فئة: قابل للتهيئة عبر `assist/prefs.json` (`tageszeitung_max_per_category`، والافتراضي: 5).

---

## الخصوصية

- تبقى محتويات المقالات محليًا في `store.db`.
- لا توجد خدمات تحليل خارجية — تُستدعى فقط مصادر RSS/الويب المُعدّة.

---

## الموارد ذات الصلة

- BACH `hub/news.py` — Origin (للقراءة فقط)
- BACH `hub/_services/newspaper/newspaper_generator.py` — Origin (للقراءة فقط)

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 0.1.0 | 2026-06-22 | إنشاء أولي — نقل مخطط BACH، متجر خاص، feedparser اختياري |
