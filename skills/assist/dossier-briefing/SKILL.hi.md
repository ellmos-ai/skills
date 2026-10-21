---
name: dossier-briefing
version: 1.0.0
type: assist
author: ellmos-ai
created: 2026-07-23
updated: 2026-08-23
category: assist
description: "किसी विषय या व्यक्ति के लिए संरचित शोध-ब्रीफ़िंग को Markdown ढाँचे के रूप में उत्पन्न करता है (stdout या फ़ाइल)। कोई स्थायी स्टोर नहीं।"
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
language: hi
visibility: public
translated_from_sha256: dbe880eee63e64ccec3db2527c516d0aace0924b5b7a8137e36639ad7136c356
translator: "claude-haiku-5-5; revision:gpt-6-sol"
translated_at: "2026-10-15T11:46:14.336931+00:00"
---
<img src="banner.png" width="100%" alt="dossier-briefing banner">

# डोज़ियर-ब्रीफ़िंग

**किसी विषय या व्यक्ति पर संरचित शोध-ब्रीफ़िंग**

---

## अवलोकन

किसी भी विषय (व्यक्ति, कंपनी, घटना, अवधारणा) पर एक खाली, संरचित Markdown-ब्रीफ़िंग उत्पन्न करता है। यह ढाँचा `research-agent` या `web-reading` के साथ आगे की शोध के लिए आधार का काम करता है।

---

## ट्रिगर

| वाक्यांश | कार्रवाई |
|---|---|
| „मैरी क्यूरी पर एक ब्रीफ़िंग बनाओ" | ढाँचा: व्यक्ति, प्रकार=person |
| „OpenAI पर एक डोज़ियर बनाओ" | ढाँचा: कंपनी, प्रकार=organization |
| „क्वांटम कंप्यूटिंग विषय पर एक ब्रीफ़िंग बनाओ" | ढाँचा: विषय, प्रकार=topic |
| „COP30 पर एक शोध-ब्रीफ़िंग तैयार करो" | ढाँचा: घटना, प्रकार=event |

---

## कार्यप्रवाह

1. **विषय का नाम तय करें:** उपयोगकर्ता के इनपुट से ब्रीफ़िंग का नाम/शीर्षक निकालें।
2. **प्रकार पहचानें:** person, organization, topic, event (या unspecified)।
3. **ढाँचा बनाएँ:** सभी प्रासंगिक अनुभागों के साथ Markdown उत्पन्न करें।
4. **आउटपुट:** stdout पर, या वैकल्पिक रूप से फ़ाइल में लिखें (`-o datei.md`)।
5. **शोध शुरू करें:** ढाँचे को `research-agent` या `web-reading` को सौंपें,
   ताकि गायब अनुभाग भरे जा सकें।

---

## CLI

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

## ब्रीफ़िंग-प्रकार और अनुभाग

| प्रकार | अनुभाग |
|---|---|
| `person` | बुनियादी डेटा, जीवन-वृत्त/पृष्ठभूमि, कार्य और योगदान, स्रोत, नोट्स |
| `organization` | प्रोफ़ाइल, इतिहास, उत्पाद/सेवाएँ, प्रमुख व्यक्ति, स्रोत, नोट्स |
| `topic` | अवलोकन, पृष्ठभूमि/संदर्भ, वर्तमान विकास, प्रमुख स्रोत, खुले प्रश्न, नोट्स |
| `event` | मुख्य तथ्य, सम्बद्ध पक्ष, घटनाक्रम/पृष्ठभूमि, महत्त्व, स्रोत, नोट्स |
| `unspecified` | अवलोकन, पृष्ठभूमि, विवरण, स्रोत, नोट्स |

---

## स्टोर

कोई स्थायी स्टोर नहीं। ढाँचा केवल आउटपुट किया जाता है (stdout या फ़ाइल),
किसी डेटाबेस में संग्रहीत नहीं किया जाता।

---

## दृष्टिकोण

- हमेशा स्पष्ट करें कि ढाँचा खाली है और शोध द्वारा भरा जाना चाहिए।
- सामग्री का कभी आविष्कार या कल्पना न करें — केवल संरचना प्रदान करें।
- प्रकार अस्पष्ट होने पर पूछें या `unspecified` का उपयोग करें।

---

## गोपनीयता

कोई नेटवर्क पहुँच नहीं। कोई स्टोर नहीं। केवल स्थानीय प्रसंस्करण।

---

## सम्बद्ध संसाधन

- `research-agent` — शोध-परिणामों से ब्रीफ़िंग ढाँचे को भरता है
- `web-reading` — वेबपेज पढ़ता है और ब्रीफ़िंग के लिए सामग्री निकालता है

---

## परिवर्तन-लॉग

| संस्करण | तिथि | परिवर्तन |
|---|---|---|
| 1.0.0 | 2026-06-22 | BACH dossier_generator.py v1.0.0 से बनाया गया; स्टोर हटाया गया, सामान्यीकृत किया गया |
