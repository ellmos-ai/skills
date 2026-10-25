---
name: textproduction
version: 2.0.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-09-27
description: "إنتاج نصوص بمساعدة الذكاء الاصطناعي في ثلاث مهارات فرعية: النصوص العامة (منشور مدونة، وسائل التواصل الاجتماعي، النشرة الإخبارية، النص الإعلاني، البريد الإلكتروني، التقرير)، والقصص السردية (السيناريو، القصة القصيرة، لعب الأدوار RPG، بناء العوالم) والتواصل الإعلامي (البيان الصحفي، ورقة الموقف) مع مترجم LaTeX محلي لإنتاج ملفات PDF. لا تلزم أي خدمة خارجية."
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: production
tags: [text, blogpost, social-media, newsletter, marketing, email, bericht, copy,
       story, drehbuch, rpg, weltenbau, pressemitteilung, positionspapier, pr, latex]
language: ar
status: active
visibility: public

dependencies:
  tools: [pr/press_compiler.py]
  services: []
  protocols: []
  python: []

provenance:
  origin: "bach"
  origin_path: "system/agents/_experts/textproduction/ + system/agents/_experts/press/"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  origin_license: "MIT"
  last_sync_from_origin: "2026-06-22"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: 0ecf524b5455a0991d20fb17dfd48892eaf544f75453f005c4bfa0dc63bdc03f
translator: "claude-haiku-5-5"
translated_at: "2026-10-16T03:22:33.152218+00:00"
---
<img src="banner.png" width="100%" alt="textproduction banner">

> **Deutsch** — Offizielle Deutsch-Version / Documento Oficial en Deutsch.


> **English Translation** — Official English version of `textproduction`.


# إنتاج النصوص — الموجّه (العربية)

تغطي هذه المهارة جميع أشكال إنتاج النصوص. وهي تحيل إلى المهارة الفرعية المناسبة — اقرأ الإرشادات التفصيلية في المجلد الفرعي.

## جدول التوجيه

| المهارة الفرعية | أمثلة على المحفّزات | الإرشادات التفصيلية |
|---|---|---|
| **text** | „Schreib einen Blogpost", „5 LinkedIn-Posts", „Newsletter", „Produktbeschreibung", „Formelle E-Mail", „Fasse X zusammen"، «اكتب منشور مدونة»، «5 منشورات لينكدإن»، «نشرة إخبارية»، «وصف منتج»، «بريد إلكتروني رسمي»، «لخّص X» | `text/WORKFLOW.md` |
| **storys** | „Schreib ein Drehbuch", „Kurzgeschichte", „RPG-Abenteuer erstellen", „Character Sheet", „Weltenbau"، «اكتب سيناريو»، «قصة قصيرة»، «إنشاء مغامرة RPG»، «ورقة شخصية»، «بناء العوالم» | `storys/WORKFLOW.md` |
| **pr** | „Pressemitteilung verfassen", „Positionspapier", „PR-Paket", „PDF generieren"، «صياغة بيان صحفي»، «ورقة موقف»، «حزمة تواصل إعلامي»، «إنشاء ملف PDF» | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## سير العمل والنهج

```
1. Nutzerwunsch → Routing-Tabelle oben → passenden Teilskill bestimmen.
2. Detail-Anleitung im Unterordner lesen (WORKFLOW.md).
3. Prompt-Muster auswaehlen, Platzhalter fuellen, Text generieren.
4. Qualitaetspruefung (je Teilskill angegeben).
```


## ملاحظات

- **محايدة للمستخدم:** لا توجد بيانات شخصية أو مفاتيح API أو بيانات حسابات في المهارة.
  يتولى المستخدم الإعدادات (النبرة، حدود عدد الأحرف، بيانات الاتصال لأغراض التواصل الإعلامي).
- **أداة التواصل الإعلامي:** يقوم `pr/press_compiler.py` بتجميع البيانات الصحفية وأوراق المواقف إلى ملفات PDF عبر LaTeX (pdflatex/xelatex). الإعداد لمرة واحدة: انسخ `pr/config.example.json` إلى `pr/config.json` وأدخل بيانات الاتصال.
- تحسين الأسلوب اختياري: DeepL Write (مجاني حتى 500,000 حرف شهريًا).

## سجل التغييرات

### 2.0.0 (2026-06-22)
- إعادة الهيكلة وفق نمط الموجّه: SKILL.md = نقطة الدخول + جدول التوجيه.
- ثلاث مهارات فرعية: text/ (6 أنواع نصية)، storys/ (4 تنسيقات سردية)،
  pr/ (البيان الصحفي + ورقة الموقف + مترجم LaTeX إلى PDF).
- نقل press_compiler.py + قوالب LaTeX + config.example.json من
  ai-media-editor/production/pr/ إلى هنا (المصدر الواحد للحقيقة SSOT).
- تحديث مراجع المهارات ذات الصلة إلى مسارات المهارات الفرعية الداخلية.

### 1.0.0 (2026-06-22)
- الإصدار الأولي. مُستخرج من ai-media-editor/production/text/WORKFLOW.md.
- المصدر: BACH agents/_experts/textproduction/ (MIT).
