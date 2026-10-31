---
name: folder-flattening
version: 1.0.0
type: tool
author: Lukas Geiger
created: 2026-03-12
updated: 2026-03-12
description: "नेस्टेड फ़ोल्डर पदानुक्रमों को सपाट, मशीन-पठनीय संरचनाओं में पुनर्गठित करें। Bash-आधारित, बुद्धिमान merge-तर्क के साथ।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [ordner, flattening, filesystem, bash, reorganisation, cleanup]
language: hi
status: active
visibility: public
dependencies:
  tools: []
  services: []
  protocols: []
  python: []
provenance:
  origin: "bach"
  origin_path: "system/skills/workflows/ordner-flattening.md"
  origin_version: "1.0.0"
  origin_repo: "github.com/ellmos-ai/bach"
  last_sync_from_origin: "2026-03-12"
  last_sync_to_origin: null
  local_changes_since_sync: true
translated_from_sha256: ecd288c18790f209ab63e3b72bc81cf748f957b27068f37a9a4999740f4392b2
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T11:49:46.928358+00:00"
---
<img src="banner.png" width="100%" alt="folder-flattening banner">

# वर्कफ़्लो: फ़ोल्डर-फ़्लैटनिंग

लक्ष्य: नेस्टेड फ़ोल्डर संरचनाओं को एक सपाट, मशीन-पठनीय संरचना में बदलना।
लाभ: क्लिक करके खोजने के बजाय डेटाबेस (Verzeichnis.db) के माध्यम से खोजना।
विषयगत रूप से उपयुक्त होने पर डुप्लिकेट की अनुमति है।

---

## चरणों का अवलोकन

| चरण | क्या होता है | स्क्रिप्ट-खंड |
|-----|-------------|--------------|
| 1 | Flatten: सभी उप-फ़ोल्डरों को एक स्तर पर लाना | `phase_flatten` |
| 2 | संक्षिप्त करना: लंबे पथ-नामों को अंतिम खंड तक छोटा करना, विरोध होने पर merge करना | `phase_shorten` |
| 3 | सफ़ाई: बहु-अंडरस्कोर (`___`) हल करना, अनुगामी `_` हटाना | `phase_cleanup_underscores` |
| 4 | समूहीकरण: संख्या-फ़ोल्डर, CD-फ़ोल्डर, छोटे नामों को संग्रह-फ़ोल्डर में डालना | `phase_group_problematic` |
| 5 | ट्रिपल-विश्लेषण: चलायमान 3-समूह, सबसे छोटा नाम merge-लक्ष्य के रूप में | `phase_tripel_merge` |
| 6 | मीडिया-प्रारूप Merge: फ़ाइल प्रकार के अनुसार फ़ोल्डरों को एकत्र करना (टेम्पलेट) | `phase_media_merge` |
| 7 | सफ़ाई: खाली फ़ोल्डर हटाना | `phase_cleanup_empty` |

---

## महत्वपूर्ण नियम

### ट्रिपल-विश्लेषण मिलान
- **सबस्ट्रिंग**: `Aufklaerung` in `Aufklaerungsbroschueren` -> merge in `Aufklaerung`
- **बहुवचन/उमलॉट**: `Raum` = `Raeume`, `Teil` = `Teile`, `Buch` = `Buecher`
- **पहला-शब्द**: `Autismus ADHS` मेल खाता है `Autismus Beruf` (समान आरंभ)

### न्यूनतम लंबाई
- बिना स्पेस वाला एक-शब्द नाम: **कम से कम 8 अक्षर** (`Hand`, `Haus`, `Form` को रोकता है)
- स्पेस वाले नाम (जैसे `ICF Katalog`): **3 अक्षरों से आरंभ ठीक है**
- इस तरह `ICF`, `ASS Frauen` आदि अनुमत रहते हैं

### Merge के बाद पुनः आरंभ
हर merge के बाद फ़ोल्डर-सूची पुनः लोड होती है और merge-लक्ष्य से दोबारा शुरू होती है।
उदाहरण के लिए `Autismus` आगे बढ़ने से पहले सभी विस्तार एकत्र कर लेता है।

---

## मीडिया-प्रारूप Merge (टेम्पलेट-प्रणाली)

चरण 6 एक टेम्पलेट-array `MEDIA_TYPES` का उपयोग करता है। हर प्रविष्टि परिभाषित करती है:
- लक्ष्य फ़ोल्डर (`_` उपसर्ग के साथ)
- फ़ाइल एक्सटेंशन जो इस प्रकार से संबंधित हैं

```bash
MEDIA_TYPES=(
    "_Audio|mp3|m4a|wav|flac|ogg|wma|aac|opus|aiff"
    "_Video|mp4|avi|mkv|mov|wmv|flv|webm|m4v|mpg|mpeg|3gp"
    "_Bilder|jpg|jpeg|png|gif|bmp|tiff|tif|webp|svg|ico|heic|heif|raw|cr2|nef"
    # Erweiterbar:
    # "_Tabellen|xlsx|xls|csv|ods"
    # "_Prasentationen|pptx|ppt|odp"
    # "_Code|py|js|ts|sh|bat|ps1"
    # "_CAD|dwg|dxf|step|stl"
    # "_3D|obj|fbx|blend|gltf|glb"
    # "_Fonts|ttf|otf|woff|woff2"
)
```

केवल वे फ़ोल्डर स्थानांतरित होते हैं जिनमें **विशेष रूप से** एक प्रकार की फ़ाइलें हों।
उप-फ़ोल्डर वाले फ़ोल्डर छोड़ दिए जाते हैं।

### नया मीडिया-प्रकार जोड़ना

`MEDIA_TYPES` array में बस एक नई पंक्ति जोड़ें:
```bash
"_Zielordner|ext1|ext2|ext3"
```

---

## निष्पादन

```bash
# Kompletter Durchlauf:
cd /pfad/zum/zielverzeichnis
bash ordner_flattening_komplett.sh

# Oder einzelne Phasen:
bash ordner_flattening_komplett.sh --phase flatten
bash ordner_flattening_komplett.sh --phase tripel
bash ordner_flattening_komplett.sh --phase media
bash ordner_flattening_komplett.sh --phase cleanup
```

---

## सत्र 26.01.2026 के अनुभवजन्य मान

- आरंभ: 206 फ़ोल्डर + 252 अलग फ़ाइलें, ~5600 नेस्टेड उप-फ़ोल्डर
- Flatten के बाद: एक स्तर पर ~2200 फ़ोल्डर
- संक्षिप्त करने + सफ़ाई के बाद: ~2005 फ़ोल्डर
- समूहीकरण के बाद (संख्याएँ, CDs): ~2005 -> संग्रह-फ़ोल्डर बनाए गए
- ट्रिपल v1 के बाद: ~1561 फ़ोल्डर
- ट्रिपल v2 के बाद (8-अक्षर नियम): आगे और कमी
- मीडिया-प्रारूप चरण: Audio/Video/Bilder-फ़ोल्डर समेकित
