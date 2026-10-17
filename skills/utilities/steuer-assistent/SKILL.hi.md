---
name: steuer-assistent
version: 0.1.0
type: skill
author: Lukas Geiger
created: 2026-07-23
updated: 2026-07-23
description: "यह स्टैंडअलोन मॉड्यूल steuer-assistent की ओर संकेत करता है: जर्मन कर्मचारी आय-संबंधी व्यय (Werbungskosten) के लिए एक स्थानीय, ऑफ़लाइन-प्रथम रसीद वर्कशीट -- रिकॉर्ड करें, सेंट-सटीक योग करें, निजी ZIP निर्यात करें। इस स्किल का उपयोग तब करें जब Werbungskosten की रसीदें संरचित तरीके से तैयार की जानी हों -- एक स्पष्ट सीमा के साथ: यह कर सलाह नहीं है, कोई कटौती-योग्यता जाँच नहीं है, और कोई कर रिटर्न नहीं बनाया या जमा किया जाता (वह ELSTER या स्वीकृत सॉफ़्टवेयर के माध्यम से होता है)।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance: {'origin': 'external', 'origin_repo': 'https://github.com/ellmos-ai/steuer-assistent', 'origin_path': 'SKILL.md, steuer_assistent/ (CLI module)', 'origin_version': None, 'last_sync_from_origin': '2026-07-23', 'last_sync_to_origin': None, 'local_changes_since_sync': False}
category: utilities
tags: [tax, germany, receipts, finance, wrapper, pointer-skill]
language: hi
status: active
visibility: public
translated_from_sha256: 0beb350be5741675f21d27461094e9908be7de7c209e659bed7b55ab374c1bb3
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:45.272925+00:00"
---
<img src="banner.png" width="100%" alt="steuer-assistent banner">

# steuer-assistent -- Verweis-Skill

यह स्किल एक **हल्का संदर्भ (Wrapper)** है जो स्वतंत्र, सार्वजनिक मॉड्यूल-रिपॉज़िटरी
[`ellmos-ai/steuer-assistent`](https://github.com/ellmos-ai/steuer-assistent)
(MIT-लाइसेंस, सार्वजनिक) की ओर इंगित करता है। वास्तविक स्किल वहीं रहती है -- यह
रिपॉज़िटरी केवल इंस्टॉलेशन का लिंक और दस्तावेज़ीकरण देती है।

## मॉड्यूल क्या करता है

`steuer-assistent` स्व-वर्गीकृत Werbungskosten-रसीदों (कर्मचारी-Werbungskosten) के लिए एक छोटा, ऑफ़लाइन-प्रथम Python-मॉड्यूल है:

- रसीदें दर्ज करें (श्रेणी, राशि, तारीख, वैकल्पिक नोट)।
- दर्ज Werbungskosten को वर्ष के अनुसार सेंट-सटीक रूप से जोड़ें।
- एक निजी, गैर-आधिकारिक ZIP कार्य-दस्तावेज़ निर्यात करें (CSV + सारांश + गैर-आधिकारिकता का संकेत, बिना रसीद-फ़ाइलों के)।
- स्थानीय स्टोर (डिफ़ॉल्ट `%USERPROFILE%\.steuer-assistent\steuer.db`), कोई नेटवर्क एक्सेस नहीं, कोई क्लाउड अपलोड नहीं, किसी बाहरी डेटाबेस तक पहुँच नहीं।

## सीमाएँ (महत्वपूर्ण)

- **कोई कर सलाह नहीं।** यह मॉड्यूल न तो व्यक्तिगत मदों की कर-कटौती-योग्यता की जाँच करता है और न ही कर रिटर्न बनाता या जमा करता है।
- आधिकारिक इलेक्ट्रॉनिक जमा केवल ELSTER या उसके लिए स्वीकृत सॉफ़्टवेयर के माध्यम से होता है -- इस मॉड्यूल के माध्यम से नहीं।
- दायरा: कर्मचारी Werbungskosten के लिए निजी कार्य-दस्तावेज़; व्यापार- या व्यावसायिक व्यय की कोई रिकॉर्डिंग नहीं।

## इंस्टॉलेशन (सामान्य, स्थानीय ठोस पथों के बिना)

1. मॉड्यूल क्लोन करें:
   ```bash
   git clone https://github.com/ellmos-ai/steuer-assistent.git <klon-pfad>
   ```
2. मॉड्यूल इंस्टॉल करें और जाँचें:
   ```bash
   cd <klon-pfad>
   python -m pip install -e .
   python -B -m pytest tests -q -p no:cacheprovider
   ```
3. `<klon-pfad>/SKILL.md` को अपने स्किल-वातावरण में लें (जैसे
   `~/.claude/skills/steuer-assistent/`)। किसी संस्करित स्किल-वातावरण में वास्तविक स्थानीय पथ
   या होस्टनाम कमिट न करें।
4. आवश्यकता होने पर स्टोर-पथ को `STEUER_ASSISTENT_DB=<pfad>` या
   `--store <pfad>` के माध्यम से समायोजित करें; डिफ़ॉल्ट उपयोगकर्ता-निर्देशिका है।
5. CLI-कमांड, गोपनीयता और सीमाओं का विवरण: मॉड्यूल-रेपो के README में देखें।

## इस संदर्भ-स्किल की उत्पत्ति

यह रैपर 2026-07-23 को `ellmos-ai/skills`-रिपॉज़िटरी के लिए एक showcase-प्रविष्टि के रूप में तैयार किया गया था। **कोई कोड-दोहराव नहीं** होता -- रखरखाव और संस्करण-नियंत्रण केवल मॉड्यूल-रेपो `ellmos-ai/steuer-assistent` में रहते हैं।

## Changelog

### 0.1.0 (2026-07-23)
- `ellmos-ai/steuer-assistent` पर प्रारंभिक संदर्भ-स्किल।
