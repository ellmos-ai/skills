---
name: pingpong
version: 1.1.0
type: protocol
author: Lukas Geiger, OpenAI Codex
created: 2026-08-03
updated: 2026-09-13
description: "एक सीमित अवधि के लिए, सत्र-बद्ध रेडियो स्टेशन चलाता है, जो एक साझा रूप से सिंक्रोनाइज़ किए गए फ़ोल्डर के माध्यम से संचालित होता है। ListenSync व्यवस्थित रूप से कार्यों और नई जानकारी के लिए स्कैन करता है; WriteSync डेल्टा और रसीदें भेजता है। PingPong, Dosentelefon, ListenSync, WriteSync, Sync-Listener, Auftragswache, News-Scan या Goal-/Loop-निगरानी के लिए उपयोग करें।"
# Kompatibilität
standalone: false
anthropic_compatible: true
bach_compatible: false
bach_origin: false

# Kategorisierung
category: infrastructure
tags: [pingpong, sync, listener, goal, loop, cadence, filecommander]
language: hi
status: active
visibility: public

# Abhängigkeiten
dependencies:
  tools: [ellmos-filecommander]
  services: []
  protocols: [shared-folder-sync]
  python: []

roles:
  - id: pingpong
    label: PingPong
    prompt: skills/infrastructure/pingpong/SKILL.en.md
    request: Read and follow the PingPong protocol for the requested mode and duration.
    modes: [ListenSync, WriteSync]
    providers: [codex, claude]

# Provenance
provenance:
  origin: "custom"
  origin_path: "local-skill/pingpong"
  origin_version: "1.0.0"
  origin_repo: null
  last_sync_from_origin: "2026-08-04"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: 6f644ddfdc91c21a6250f7af08b78211b2949ad989b2e2f9104d71bed1ef062b
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:43.405620+00:00"
---
<img src="banner.png" width="100%" alt="pingpong banner">

# PingPong

दो या अधिक सिस्टमों को एक साझा Sync-फ़ोल्डर के माध्यम से रेडियो स्टेशनों के रूप में चलाएँ। फ़ंक्शनल अनुबंध को प्रदाता-तटस्थ रखें; केवल जारी रखने वाला एडेप्टर भिन्न होता है।

## मोड तय करें

- ListenSync: प्रति होस्ट ठीक एक व्यवस्थित Listener। वह स्कैन करता है, उपयुक्त कार्य स्वीकार करता है और उत्तर मिलने पर WriteSync भी चलाता है।
- WriteSync: प्रत्येक सक्रिय अभिनेता अपने प्रासंगिक डेल्टा, कार्य, नई जानकारी और रसीदें भेज सकता है। यह मोड कोई Listener शुरू नहीं करता।
- यदि मोड नहीं दिया गया है, तो ListenSync का उपयोग करें।

## भागीदारी स्पष्ट करें (STATE और CALL)

रन-अनुबंध से पहले दो-चरणीय जाँच तय करती है कि वास्तव में कोई पहुँच में है या नहीं। `scripts/pingpong_runtime.py check --slot <slot> --sync-root <pfad>` ठीक तीन मानों के साथ उत्तर देता है: Exit 0 `call-for-me` (सक्रिय करें और एक एजेंट स्पॉन करें), Exit 1 `idle` (मैं स्वयं सक्रिय हूँ, निष्क्रिय करें), Exit 3 `check-failed` (अपठनीय, इसे कभी निष्क्रियता न मानें)। भागीदारी के लिए STATE और CALL एक साथ आवश्यक हैं; जो कॉल बुलाता है, वह उद्देश्य पूरा होने पर उसे समाप्त करता है, अन्यथा वह समाप्त हो जाता है। पूर्ण नियम references/protocol.md में हैं।

## रन-अनुबंध तय करें

1. डिफ़ॉल्ट रूप से 24h उपयोग करें। सापेक्ष अवधियाँ जैसे 15m, 2h, 3d या एक निरपेक्ष ISO-8601 समाप्ति-समय भी स्वीकार करें।
2. स्थानीय प्रारंभ-समय मापें और expires_at को तारीख, समय और समय-क्षेत्र के साथ बताएँ।
3. 15 मिनट से शुरू करें। references/protocol.md की कैडेंस का उपयोग करें, जब तक उपयोगकर्ता कोई स्थिर कैडेंस न माँगे।
4. लक्ष्य-पूर्ति को इस प्रकार परिभाषित करें: समाप्ति-समय पहुँच गया, FileCommander का अंतिम स्कैन प्रमाणित, तब तक पहचाने गए सभी उपयुक्त इनपुट संसाधित या सटीक रूप से अवरुद्ध और दस्तावेज़ित, State अद्यतन और अपना Scheduler समाप्त।
5. FileCommander-प्रमाण के बिना न स्कैन और न लक्ष्य-पूर्ति का दावा करें।

## प्रदाता-एडेप्टर का उपयोग करें

### Codex

पहले स्कैन से पहले पूर्ण रन-अनुबंध और expires_at के साथ एक स्थायी Goal स्पष्ट रूप से बनाएँ। प्रत्येक जारी रखने पर ठीक एक पूर्ण स्कैन-चक्र चलाएँ। खाली या सफल एकल चक्र के बाद Goal समाप्त न करें। उसके बाद वास्तव में next_scan_at तक प्रतीक्षा करें, उदाहरण के लिए:

    python "<skill-root>/scripts/pingpong_runtime.py" wait --until "<next_scan_at>"

समाप्ति-समय पर अंतिम चक्र चलाएँ। Goal को केवल सफलता-मानदंड पूरा होने पर पूर्ण चिह्नित करें।

### Claude Code

कार्य को /loop <Kadenz> $pingpong के रूप में शुरू करें। यदि Skill पहले से किसी निर्धारित रन से आ रहा है, तो दूसरा Loop न बनाएँ। कैडेंस बदलने पर केवल अपना Cron-Job बदलें। अंतिम चक्र के बाद उसे हटा दें।

## चक्र चलाएँ

references/protocol.md को पूरा पढ़ें और वहाँ वर्णित ठीक एक स्कैन-, संसाधन- और State-चक्र चलाएँ। Sync-फ़ोल्डर की हर पहुँच के लिए ellmos FileCommander उपयोग करें। केवल एक Shell-Listing, Scheduler-प्रविष्टि या फ़ाइलनाम स्कैन-प्रमाण नहीं है।

निष्क्रियता में कोई काम न गढ़ें। संक्षेप में रिपोर्ट करें: स्कैन-समय, पढ़ी गई Freshness-फ़ाइलें, वर्तमान कैडेंस, empty_runs, next_scan_at और expires_at।

## WriteSync चलाएँ

केवल अपने सिस्टम-स्लॉट या स्पष्ट रूप से वैश्विक चैनल में लिखें। प्रेषक, प्राप्तकर्ता, समय, संदर्भ, कार्रवाई, परिणाम, खुले बिंदु और वांछित कैडेंस बताएँ। ओवरराइट के बजाय Merge करें; कोई Credentials नहीं; Locks का सम्मान करें। लिखने के बाद FileCommander से कैनोनिकल फ़ाइल वापस पढ़ें।

## Changelog

### 1.1.0 (2026-09-13)

- होस्ट-संबंधित भागीदारी-चिह्न STATE (फ़ील्ड `pingpong` में `agents/registry/<slot>.state.json`) और समाप्त होने वाली संबोधित CALL-फ़ाइलें `call-<von>-to-<an|all>.txt` जोड़ी गईं; `pingpong_runtime.py` इसके लिए `state`, `call` और दो-चरणीय जाँच `check` को तीन-मान परिणाम के साथ जानता है। पुराने `pull-` नाम संक्रमण के लिए अभी भी पढ़े जाते हैं। T-20260830-425388998 का कार्यान्वयन उपयोगकर्ता के निर्णय 2026-09-11 के अनुसार (सबसे छोटा कटौती: केवल STATE, CALL और समाप्ति)।

### 1.0.1 (2026-09-09)

- वैकल्पिक Modul-v2-Rollenvertrag के अनुसार घोषणात्मक भूमिका-मेटाडेटा जोड़ा गया; कोई तटस्थ Starter भूमिका घोषित नहीं करता। मौजूदा प्रोटोकॉल-पहचान और Discovery-पथ बने रहते हैं।

### 1.0.0 (2026-08-04)

- Codex-Goal- और Claude-Loop-एडेप्टर के साथ प्रदाता-तटस्थ ListenSync-/WriteSync-अनुबंध।
- FileCommander-प्रमाण, Freshness-Guard, अनुकूली कैडेंस और निरपेक्ष समाप्ति-शर्त जोड़ी गई।
