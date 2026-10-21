---
name: textproduction
version: 2.0.0
type: expert
author: ellmos
created: 2026-06-22
updated: 2026-09-27
description: "এআই-সহায়তায় পাঠ্য নির্মাণ তিনটি উপ-দক্ষতায়: সাধারণ পাঠ্য (ব্লগপোস্ট, সোশ্যাল, নিউজলেটার, কপি, ই-মেইল, প্রতিবেদন), বর্ণনামূলক গল্প (স্ক্রিপ্ট, ছোটগল্প, RPG, বিশ্বনির্মাণ) এবং PR-যোগাযোগ (প্রেস রিলিজ, অবস্থানপত্র) স্থানীয় LaTeX-PDF কম্পাইলারসহ। কোনো বাহ্যিক সেবা বাধ্যতামূলক নয়।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true

category: production
tags: [text, blogpost, social-media, newsletter, marketing, email, bericht, copy,
       story, drehbuch, rpg, weltenbau, pressemitteilung, positionspapier, pr, latex]
language: bn
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

# পাঠ্য উৎপাদন — রাউটার (Deutsch)

এই দক্ষতা সমস্ত পাঠ্য উৎপাদন রূপ অন্তর্ভুক্ত করে। এটি উপযুক্ত উপ-দক্ষতায় পরিচালিত করে — উপফোল্ডারের বিস্তারিত নির্দেশনা পড়ুন।

## রাউটিং সারণি

| উপ-দক্ষতা | ট্রিগার-উদাহরণ | বিস্তারিত নির্দেশনা |
|---|---|---|
| **text** | „Schreib einen Blogpost", „5 LinkedIn-Posts", „Newsletter", „Produktbeschreibung", „Formelle E-Mail", „Fasse X zusammen", „একটি ব্লগপোস্ট লিখুন", „৫টি LinkedIn-পোস্ট লিখুন", „নিউজলেটার তৈরি করুন", „পণ্যের বিবরণ লিখুন", „আনুষ্ঠানিক ই-মেইল লিখুন", „X সংক্ষেপে সারসংক্ষেপ করুন" | `text/WORKFLOW.md` |
| **storys** | „Schreib ein Drehbuch", „Kurzgeschichte", „RPG-Abenteuer erstellen", „Character Sheet", „Weltenbau", „একটি চিত্রনাট্য লিখুন", „ছোটগল্প লিখুন", „RPG-অ্যাডভেঞ্চার তৈরি করুন", „ক্যারেক্টার শিট", „বিশ্বনির্মাণ" | `storys/WORKFLOW.md` |
| **pr** | „Pressemitteilung verfassen", „Positionspapier", „PR-Paket", „PDF generieren", „প্রেস রিলিজ লিখুন", „অবস্থানপত্র তৈরি করুন", „PR-প্যাকেজ তৈরি করুন", „PDF তৈরি করুন" | `pr/WORKFLOW.md` (+ `pr/press_compiler.py`) |

## কর্মপ্রবাহ ও পদ্ধতি

```
1. Nutzerwunsch → Routing-Tabelle oben → passenden Teilskill bestimmen.
2. Detail-Anleitung im Unterordner lesen (WORKFLOW.md).
3. Prompt-Muster auswaehlen, Platzhalter fuellen, Text generieren.
4. Qualitaetspruefung (je Teilskill angegeben).
```


## নোট

- **ব্যবহারকারী-নিরপেক্ষ:** দক্ষতায় কোনো ব্যক্তিগত তথ্য, API-Keys বা অ্যাকাউন্ট তথ্য নেই।
  কনফিগারেশন (স্বর, অক্ষর-সীমা, PR-এর যোগাযোগ তথ্য) ব্যবহারকারীর দায়িত্ব।
- **PR-Tool:** `pr/press_compiler.py` LaTeX (pdflatex/xelatex) এর মাধ্যমে প্রেস রিলিজ ও অবস্থানপত্র PDF-এ কম্পাইল করে। একবারের সেটআপ: `pr/config.example.json`-কে `pr/config.json`-এ কপি করুন এবং যোগাযোগ তথ্য লিখুন।
- ঐচ্ছিক শৈলী-অপ্টিমাইজেশন: DeepL Write (মাসে 500,000 অক্ষর পর্যন্ত বিনামূল্যে)।

## পরিবর্তন লগ

### 2.0.0 (2026-06-22)
- রাউটার-প্যাটার্নে পুনর্গঠন: SKILL.md = সূচনা + রাউটিং সারণি।
- তিনটি উপ-দক্ষতা: text/ (6 পাঠ্য-ধরন), storys/ (4 বর্ণনামূলক ফরম্যাট),
  pr/ (প্রেস রিলিজ + অবস্থানপত্র + LaTeX-PDF কম্পাইলার)।
- press_compiler.py + LaTeX-Templates + config.example.json ai-media-editor/production/pr/ থেকে এখানে স্থানান্তরিত (SSOT)।
- সম্পর্কিত-দক্ষতার রেফারেন্স অভ্যন্তরীণ উপ-দক্ষতা পথে হালনাগাদ।

### 1.0.0 (2026-06-22)
- প্রাথমিক সংস্করণ। ai-media-editor/production/text/WORKFLOW.md থেকে পৃথক করা।
- উৎস: BACH agents/_experts/textproduction/ (MIT)।
