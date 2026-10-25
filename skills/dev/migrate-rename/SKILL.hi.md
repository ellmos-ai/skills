---
name: migrate-rename
version: 1.1.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-09-06
description: "विकासवादी फ़ाइल-नामबदली रैपर फ़ाइलों के साथ, और पूरे फ़ोल्डर/फ़ाइल स्थानांतरण के लिए संक्षिप्त MOVED-स्टब मानक। बिना कठोर टूटन के नामबदली संभव बनाता है — संदर्भ उपयोग के माध्यम से स्वाभाविक रूप से अद्यतन होते हैं।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: dev
tags: [migration, renaming, wrapper, evolutionary, refactoring]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/workflows/migrate-rename.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 16d2b6f4499cdc4c454bcd8244fff5811ae232e7703095f43a59eb663238d837
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:03.139962+00:00"
---
<img src="banner.png" width="100%" alt="migrate-rename banner">

# फ़ाइल-नामबदली रैपर के साथ (विकासवादी माइग्रेशन)

> कठोर टूटन के बिना फ़ाइल-नामबदली की अनुमति देता है। संदर्भ दैनिक उपयोग के माध्यम से स्वाभाविक रूप से अद्यतन होते हैं।

---

## सिद्धांत: विकासवादी माइग्रेशन

```
VORHER:                          NACHHER:
alte_datei.md                    neue_datei.md (umbenannt)
   |                                |
   +-- Verweis A                    +-- alte_datei.md (Wrapper)
   +-- Verweis B                           |
   +-- Verweis C                           +-- Log-Tabelle
                                           +-- Anleitung
                                           +-- Link zu neue_datei.md
```

जो पुराने पथ को कॉल करता है:
1. रैपर फ़ाइल पर पहुँचता है
2. स्वयं को लॉग में दर्ज करता है
3. उस संदर्भ को सुधारता है जिसने उसे भेजा था
4. वास्तविक फ़ाइल पर जाता है

---

## चरण-दर-चरण

### 1. फ़ाइल का नाम बदलें

```bash
mv alte_datei.md neue_datei.md
```

### 2. रैपर फ़ाइल बनाएँ

`alte_datei.md` को निम्नलिखित सामग्री के साथ बनाएँ:

```markdown
# ALTE_DATEI.md - UMGELEITET

**Status:** Diese Datei wurde umbenannt zu `neue_datei.md`

---

## Migration-Log

| Datum | Wer | Herkunft | Verweis korrigiert? |
|-------|-----|----------|---------------------|
| YYYY-MM-DD | [Name] | Initiale Migration | n/a (Wrapper erstellt) |

---

## Anleitung

1. **Log-Eintrag hinterlassen** (oben in Tabelle)
2. **Herkunft pruefen**: Was hat dich hierher geschickt?
3. **Verweis korrigieren**: Aendere `alte_datei.md` -> `neue_datei.md`
4. **Zur eigentlichen Datei gehen**: `neue_datei.md`

---

**Zieldatei:** `neue_datei.md`
```

### 3. महत्वपूर्ण संदर्भ तुरंत सुधारें
- सहायता-फ़ाइलें (प्राथमिक दस्तावेज़ीकरण)
- सिस्टम-प्रॉम्प्ट संदर्भ
- CLI-कोड जो पथ को सीधे उपयोग करता है

### 4. शेष संदर्भ विकासवादी रूप से माइग्रेट करें
बाकी उपयोग के समय स्वचालित रूप से सुधार दिए जाते हैं।

---

## रैपर-विधि कब उपयोग करें?

**हाँ - रैपर उपयोगी है:**
- कई संभावित संदर्भ
- फ़ाइल विभिन्न साझेदारों/टूल्स द्वारा संदर्भित होती है
- कोई महत्वपूर्ण सिस्टम-फ़ाइल नहीं

**नहीं - सीधे सभी बदलें:**
- कुछ, ज्ञात संदर्भ
- महत्वपूर्ण सिस्टम-फ़ाइलें (config, DB-स्कीमा)
- प्रदर्शन-महत्वपूर्ण पथ

---

## MOVED-स्टब के साथ फ़ोल्डर-/फ़ाइल-स्थानांतरण

> 2026-09-06 को औपचारिक रूप दिया गया (टिकट T-20260906-688261413)। मिसाल स्वतःस्फूर्त रूप से बनी थी
> `.ELLMOS.MIGRATED.md` (2026-08-11) और `_control-center/_CONTROL`-स्टब्स (2026-09-06) पर।

ऊपर के रैपर से अलग स्थिति: यहाँ **पूरा फ़ोल्डर** या **कई सक्रिय संदर्भों के बिना फ़ाइल** एक नए स्थान पर पूरी तरह
स्थानांतरित होती है (समेकन, नामबदली, पाइपलाइन-पुनर्गठन)। कोई माइग्रेशन-लॉग नहीं, "संदर्भ सुधारें" नहीं — केवल एक संक्षिप्त
पॉइंटर, जो बताता है: अब यह यहाँ है।

**ऊपर की रैपर-प्रक्रिया से अंतर:**

| | रैपर (ऊपर चरण 1-4) | MOVED-स्टब |
|---|---|---|
| उपयोग | एकल फ़ाइल, कई सक्रिय संदर्भ, जो स्वाभाविक रूप से पीछे आएँ | फ़ोल्डर या फ़ाइल, पूर्ण स्थानांतरण |
| सामग्री | माइग्रेशन-लॉग-तालिका, उपयोग के साथ बढ़ती है | स्थिर मेटाडेटा, 1-3 पंक्तियाँ सादे पाठ में |
| जीवनकाल | जब तक लॉग दिखाए कि कोई नई प्रविष्टि नहीं | जब तक `remove_when` पूरा न हो |

### नाम, स्थान, अनिवार्य फ़ील्ड

पूर्ण स्कीमा, उदाहरण और फ़ील्ड-अर्थ ellmos-टेम्पलेट `MOVED-STUB.md` में हैं
(`.TOPICS/.AI/_templates/project-docs/MOVED-STUB.md`, इस स्वतंत्र रेपो का हिस्सा नहीं —
यहाँ संक्षिप्त रूप पर्याप्त है):

- **नाम/स्थान:** `<alter-Name>.MOVED.md` वहीं रहता है जहाँ फ़ोल्डर/फ़ाइल **पहले** थी।
- **अनिवार्य फ़ील्ड** (`key: value`, इसी क्रम में): `moved_to`, `moved_on`, `ticket`,
  `reason`, `moved_by`, `remove_when` (डिफ़ॉल्ट: `90 Tage UND 0 lebende Referenzen`)।
- **उसके बाद** मनुष्यों के लिए 1-3 पंक्तियाँ सादे पाठ में। कोई लॉग नहीं, कोई तालिका नहीं, कोई इतिहास नहीं — वह
  संदर्भित टिकट में है।
- **निष्कासन:** स्टब को **हटाया** जाता है, कभी संग्रहीत नहीं।

### नीति

`.SYNC/_policies/library/P-017_umzugs-stub.md` के रूप में बाध्यकारी।

### जाँच-स्क्रिप्ट

`scripts/moved_stub_check.py` (इस स्किल-फ़ोल्डर में) एक मूल निर्देशिका के अंतर्गत सभी `*.MOVED.md`/`*.MIGRATED.md`-
स्टब्स सूचीबद्ध करती है, गायब अनिवार्य फ़ील्ड रिपोर्ट करती है और हटाने योग्य स्टब्स (`remove_when` दिनों से पुराने) चिह्नित करती है। आह्वान:

```bash
python scripts/moved_stub_check.py <wurzelverzeichnis>
```

---

## सफ़ाई

लगभग 30 दिनों के बाद या जब लॉग दिखाए कि कोई नई प्रविष्टि नहीं:
1. रैपर फ़ाइल को `_archive/deprecated/` में ले जाएँ
2. या पूरी तरह हटा दें (यदि कोई प्रविष्टि न बची हो)

---

## परिवर्तन-लॉग

### 1.1.0 (2026-09-06)
- खंड "MOVED-स्टब के साथ फ़ोल्डर-/फ़ाइल-स्थानांतरण" जोड़ा गया (टिकट T-20260906-688261413):
  पूरे फ़ोल्डरों/फ़ाइलों के संक्षिप्त स्थानांतरण-पॉइंटर को औपचारिक रूप दिया (मानक `<alter-Name>.MOVED.md`,
  अनिवार्य फ़ील्ड moved_to/moved_on/ticket/reason/moved_by/remove_when), ऊपर की रैपर-विधि से अलग किया गया। जाँच-स्क्रिप्ट `scripts/moved_stub_check.py` जोड़ी गई।

### 1.0.0 (2026-03-15)
- BACH v3.8.0 से पोर्ट किया गया

---

*BACH v3.8.0 से पोर्ट किया गया | स्वतंत्र संस्करण*
