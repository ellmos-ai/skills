---
name: backup
version: 1.0.0
type: skill
author: User
created: 2026-08-24
updated: 2026-08-24
description: "फ़ाइलों को योजना बनाकर, दर्पण (mirror) बनाकर, सत्यापित करके, पुनर्स्थापित करके या संग्रहीत करके स्पष्ट रूप से fail-closed mac-backup कोर के माध्यम से संभालता है। इसका उपयोग उपयोगकर्ता के अपने होस्ट-पार-होस्ट बैकअप जॉब्स के लिए करें; सामान्य क्लाउड सिंक्रोनाइज़ेशन या आकस्मिक फ़ाइल कॉपी के लिए नहीं।"
visibility: public
language: hi
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: false
provenance:
  origin: "custom"
  origin_repo: "github.com/ellmos-ai/mac-backup"
  last_sync_from_origin: "2026-08-24"
  last_sync_to_origin: null
  local_changes_since_sync: false
translated_from_sha256: c50a9f8b557b5e4baa08f880f28ba234c8f56974e644ce57147bde5311a02ad6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:02.365030+00:00"
---
<img src="banner.png" width="100%" alt="backup banner">

# बैकअप

स्थापित `mac-backup`-CLI को एकमात्र ट्रांसफ़र कार्यान्वयन के रूप में उपयोग करें। प्रवाह को कच्चे
`scp`, `rsync`, SSHFS, Explorer क्रियाओं या तदर्थ हटाने से दोबारा न बनाएँ।

## अनुरोध को रूट करें

- एक सामान्य "बैकअप" अनुरोध का अर्थ `mirror` है; स्रोत अछूता रहता है।
- `archive` का अर्थ स्रोत की सफ़ाई है और यह एक अलग, विनाशकारी इरादा है। इसे कभी भी
  "backup", "बैकअप", "copy", "कॉपी", "free some space" या "कुछ जगह खाली करो" से न निकालें।
- `restore` एक नए गंतव्य पर लिखता है और कभी चुपचाप अधिलेखित नहीं करता।
- यदि कोई सत्यापित job JSON मौजूद नहीं है, तो एक job प्रस्ताव तैयार करें और `init-target` या
  ट्रांसफ़र से पहले रुकें।

## निष्पादन

1. job पढ़ें और `mac-backup plan <job> --json` चलाएँ।
2. सत्यापित करें कि लौटाई गई स्रोत श्रेणी, फ़ाइल गणना, बाइट गणना, गंतव्य volume ID,
   एन्क्रिप्शन स्थिति और होस्ट fingerprint अनुरोध और वर्तमान डिवाइस साक्ष्य से मेल खाते हैं।
3. Mirror के लिए `mac-backup mirror <job> --json` चलाएँ, फिर `mac-backup verify <job> --json`।
4. Restore के लिए एक नया, निरपेक्ष गंतव्य उपयोग करें और कमांड के manifest परिणाम के माध्यम से
   पुनर्स्थापित फ़ाइलों को सत्यापित करें।
5. Archive के लिए `--confirm-delete` केवल तभी पास करें जब उपयोगकर्ता ने स्रोत हटाने का स्पष्ट
   अनुरोध किया हो और सत्यापित योजना इसी स्रोत का नाम ले। नीति द्वारा अवरोध सही परिणाम है; कभी भी
   `target_encryption_required`, `source_class_unknown_cleanup_blocked`, `onedrive_dehydrate_not_implemented`, किसी lock, किसी पहचान
   विसंगति या किसी लापता anchor को बायपास न करें।

`init-target` विशेषाधिकार प्राप्त सेटअप है, नियमित निष्पादन नहीं। इसके लिए volume ID और
एन्क्रिप्शन हेतु स्वतंत्र रूप से प्राप्त ऑपरेटिंग सिस्टम साक्ष्य आवश्यक है; प्रस्तावित job से
कॉपी किया गया मान साक्ष्य नहीं है।

गंतव्य verify और वास्तविक restore परीक्षण दोनों पास होने से पहले कभी यह दावा न करें कि mirror एक
पूर्ण बैकअप है। Tickets, Git और OneDrive से गोपनीय जानकारी, वास्तविक job फ़ाइलें, स्थानीय anchors
और उपयोगकर्ता फ़ाइल नाम बाहर रखें।

## Changelog

### 1.0.0 (2026-08-24)
- `~/.claude/skills/backup/` deployment master की तटस्थ प्रति, वर्गीकृत लाइब्रेरी में शामिल की गई। Sync अंतराल
  का कारण: Skill तैनात था, पर `skills/<category>/` के अंतर्गत उसकी कोई स्रोत प्रविष्टि नहीं थी, इसलिए
  `skill_sync.py status` उसे केवल `NUR-ZIEL` (केवल गंतव्य) के रूप में रिपोर्ट करता था और
  `catalog.py`/`build_public_registry.py` (जो केवल `skills/` स्कैन करते हैं) उसे कभी नहीं देख
  पाते थे — इसलिए deployment प्रति चाहे कैसे भी संपादित की जाए, वह सार्वजनिक registry या
  `SKILLS-MAP.md` तक कभी नहीं पहुँच सकता था।
