---
name: compare-race
version: 1.0.0
type: pointer
author: Lukas Geiger
created: 2026-08-16
updated: 2026-08-16
description: "ये स्किल तब उपयोग करें जब उपयोगकर्ता एक ही प्रॉम्प्ट कई LLMs को भेजना और उनके उत्तरों की तुलना करना चाहता है - क्रमिक रूप से (स्टॉपवॉच, हर लेन की साफ़ समय-माप) या समानांतर रूप से (सच्ची दौड़), हर मॉडल के लिए वैकल्पिक दोहराव के साथ, जिसमें शुरुआती मॉडल ही जज के रूप में गुणवत्ता, शुद्धता, पूर्णता, निर्देश-निष्ठा और विलंबता के आधार पर उत्तरों का मूल्यांकन करता है (समय केवल एक आयाम है)। /compare-race, 'model race', 'vergleiche modelle', 'gleicher prompt an mehrere modelle', 'मॉडल रेस', 'मॉडलों की तुलना करो', 'एक ही प्रॉम्प्ट कई मॉडलों को' पर ट्रिगर होता है।"
standalone: true
anthropic_compatible: true
bach_compatible: false
category: dev
tags: [model-comparison, race, benchmark, multi-agent, judge, workflow]
language: hi
status: active
visibility: public
pointer: {'module_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race', 'prompt_de': 'prompts/RACE-STARTER.de.md', 'prompt_en': 'prompts/RACE-STARTER.en.md', 'config': 'config/compare-race.config.example.json', 'repo': 'github.com/ellmos-ai/compare-race'}
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': ['system-auditor'], 'optional_tools': [{'name': 'coma', 'path': '.AI/.MODULES/.ORCHESTRATION/coma/', 'python_module': 'coma', 'usage': 'Ausfuehrungsschicht fuer compare-race run (Spawn/Polling/Dateiprotokoll)', 'note': 'Optional. Ohne coma laeuft der modellmanuelle Weg: Spuren selbst ausfuehren und mit compare-race record einreichen.'}]}
provenance: {'origin': 'module', 'origin_path': '<HOME>/OneDrive/.TOPICS/.AI/.MODULES/.ORCHESTRATION/compare-race/prompts/RACE-STARTER.de.md', 'origin_version': '0.1.0', 'last_sync_from_origin': '2026-08-16', 'last_sync_to_origin': 'None', 'local_changes_since_sync': False}
translated_from_sha256: eef2d1e681ca3ed6c7fe63a8a36535632cf48a7b990fd8d944c8ef42ea046750
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:28:49.872870+00:00"
---
<img src="banner.png" width="100%" alt="compare-race banner">

# compare-race — पॉइंटर-स्किल (जर्मन)

> **यह स्किल केवल एक पॉइंटर है। सत्य का स्रोत मॉड्यूल है।**

## मॉड्यूल-पथ

```
<HOME>\OneDrive\.TOPICS\.AI\.MODULES\.ORCHESTRATION\compare-race\
```

रेपो: [github.com/ellmos-ai/compare-race](https://github.com/ellmos-ai/compare-race)

## एजेंट के लिए निर्देश

1. मॉड्यूल-फ़ोल्डर में रोल-प्रॉम्प्ट **`prompts/RACE-STARTER.de.md`** पढ़ें और उसका पालन करें।
   आप RACE-STARTER हैं — और डिफ़ॉल्ट रूप से **Judge** भी (उपयोगकर्ता का निर्णय
   2026-08-16)।
2. कॉन्फ़िग जाँचें (`compare-race config`; होस्ट-कॉन्फ़िग `~/.compare-race/` के अंतर्गत)।
   मोड चुनें: `sequential` = स्टॉपवॉच (हर स्पर्धा-लेन की साफ़ एकल माप) ·
   `parallel` = सच्ची दौड़। **स्टॉपवॉच केवल एक उपमा है** — समय गुणवत्ता, शुद्धता, पूर्णता, निर्देश-निष्ठा और लागत के अंतर्गत एक आयाम है।
3. दौड़ शुरू करें (`compare-race run --prompt-file …`); बिना coma के मॉडल-मैन्युअल
   मार्ग `compare-race record` के माध्यम से अपनाएँ।
4. Judge के रूप में, रेस-फ़ोल्डर की `RACE.md` में रूब्रिक भरें — हर RUN-फ़ाइल स्वयं पढ़ें; यदि अपना मॉडल भी भाग ले रहा हो तो पक्षपात का उल्लेख करें।
5. अक्ष-अनुशासन: कारण केवल तभी आरोपित करें जब ठीक एक अक्ष बदल रहा हो
   (model = दौड़ · run = विचरण · time = मॉडल-ड्रिफ़्ट)।

## कोटा-चेतावनी

दौड़ें **हर** शामिल कोटा (claude/codex/agy/kimi) पर खर्च होती हैं। बड़ी दौड़ों
(कई लेनें × दोहराव) से पहले उपयोगकर्ता से पूछें।
