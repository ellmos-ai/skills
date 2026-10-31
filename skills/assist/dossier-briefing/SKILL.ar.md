---
name: dossier-briefing
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "يُنشئ هذا الأداة إحاطةً بحثيةً منظّمةً عن موضوع أو شخص في صورة هيكل Markdown (على الشاشة أو في ملف). لا يوجد مخزن دائم."
tags: [briefing, dossier, recherche, markdown, research]
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
languages: [de, en]
dependencies: {'python': ['datetime', 'pathlib', 'textwrap']}
runtime: python3
entry_point: dossier_briefing_core.py
provenance: {'origin': 'BACH persoenlicher-assistent', 'origin_path': 'system/agents/persoenlicher-assistent/tools/dossier_generator.py', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'origin_license': 'MIT', 'last_sync_from_origin': '2026-06-22', 'last_sync_to_origin': None, 'local_changes_since_sync': 'Alle Origin-DB-Abhaengigkeiten entfernt (create_dossier, update_dossier, DOSSIERS_DIR, DossierGenerator-Klasse mit DB-Methoden). Nur _create_markdown-Logik portiert und verallgemeinert (Person→Subjekt). Kein Store. One-Shot-Scaffold-Generator. Headless, nur Stdlib.\n'}
language: ar
visibility: public
translated_from_sha256: dbe880eee63e64ccec3db2527c516d0aace0924b5b7a8137e36639ad7136c356
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:32:11.631321+00:00"
---
<img src="banner.png" width="100%" alt="dossier-briefing banner">

# Dossier-Briefing

**إحاطة بحثية منظّمة حول موضوع أو شخص**

---

## نظرة عامة

يُنشئ هذا الأداة إحاطةً فارغةً ومنظّمةً بصيغة Markdown حول أي موضوع (شخص، أو شركة، أو حدث، أو مفهوم). ويُستخدم الهيكل نقطةَ انطلاقٍ لبحثٍ لاحقٍ باستخدام `research-agent` أو `web-reading`.

---

## المحفّزات

| العبارة | الإجراء |
|---|---|
| «أنشئ إحاطةً عن ماري كوري» | هيكل: شخص، النوع=person |
| «ملف عن OpenAI» | هيكل: شركة، النوع=organization |
| «إحاطة حول موضوع الحوسبة الكمومية» | هيكل: موضوع، النوع=topic |
| «جهّز إحاطة بحثية عن COP30» | هيكل: حدث، النوع=event |

---

## سير العمل

1. **تحديد الموضوع:** استخراج اسم الإحاطة أو عنوانها من إدخال المستخدم.
2. **تحديد النوع:** person، أو organization، أو topic، أو event (أو unspecified).
3. **إنشاء الهيكل:** توليد Markdown يتضمن جميع الأقسام ذات الصلة.
4. **الإخراج:** على الشاشة (stdout) أو اختيارياً في ملف (`-o datei.md`).
5. **بدء البحث:** تمرير الهيكل إلى `research-agent` أو `web-reading`
   لملء الأقسام الناقصة.

---

## واجهة سطر الأوامر

```bash
# Briefing zu stdout
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Marie Curie" --typ person

# In Datei schreiben
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "OpenAI" --typ organization -o briefing_openai.md

# Themen-Briefing
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Quantencomputing" --typ topic

# Ereignis
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "COP30" --typ event

# Ohne Typ-Angabe (generisch)
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py "Mein Thema"

# Hilfe
PYTHONDONTWRITEBYTECODE=1 python dossier_briefing_core.py --help
```


---

## أنواع الإحاطات والأقسام

| النوع | الأقسام |
|---|---|
| `person` | البيانات الأساسية، السيرة/الخلفية، الأعمال والإسهامات، المصادر، ملاحظات |
| `organization` | الملف التعريفي، التاريخ، المنتجات/الخدمات، الشخصيات الرئيسة، المصادر، ملاحظات |
| `topic` | نظرة عامة، الخلفية/السياق، التطورات الراهنة، المصادر الرئيسة، أسئلة مفتوحة، ملاحظات |
| `event` | الحقائق الأساسية، المشاركون، التسلسل/الخلفية، الأهمية، المصادر، ملاحظات |
| `unspecified` | نظرة عامة، الخلفية، التفاصيل، المصادر، ملاحظات |

---

## المخزن

لا يوجد مخزن دائم. يُخرَج الهيكل فقط (على الشاشة أو في ملف)،
ولا يُحفظ في قاعدة بيانات.

---

## المنهجية

- التأكيد دائماً على أن الهيكل فارغ ويجب ملؤه عن طريق البحث.
- عدم اختلاق المحتوى أو تخمينه؛ تقديم البنية فقط.
- عند غموض النوع، يُسأل المستخدم أو تُستخدم `unspecified`.

---

## حماية البيانات

لا يوجد وصول إلى الشبكة. لا يوجد مخزن. معالجة محلية بالكامل.

---

## موارد ذات صلة

- `research-agent` — يملأ هيكل الإحاطة بنتائج البحث
- `web-reading` — يقرأ صفحات الويب ويستخرج المحتوى للإحاطة

---

## سجل التغييرات

| الإصدار | التاريخ | التغيير |
|---|---|---|
| 1.0.0 | 2026-06-22 | أُنشئ من BACH dossier_generator.py v1.0.0؛ أُزيل المخزن وعُمّم |
