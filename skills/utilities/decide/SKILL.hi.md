---
name: decide
version: 1.0.0
type: skill
author: Lukas Geiger
created: 2026-03-15
updated: 2026-03-15
description: "संरचित निर्णय लेना: Pro/Con मैट्रिक्स, भारित स्कोरिंग, निर्णय वृक्ष, परिदृश्य विश्लेषण और Eisenhower मैट्रिक्स।"
standalone: true
anthropic_compatible: true
bach_compatible: false
bach_origin: true
category: utilities
tags: [decision, evaluation, prioritization, framework]
language: hi
status: active
visibility: public
dependencies: {'tools': [], 'services': [], 'protocols': [], 'python': []}
provenance: {'origin': 'bach', 'origin_path': 'system/skills/_services/decide.md', 'origin_version': '1.0.0', 'origin_repo': 'github.com/ellmos-ai/bach', 'last_sync_from_origin': '2026-03-15', 'last_sync_to_origin': None, 'local_changes_since_sync': True}
translated_from_sha256: 1627b5e5d34c9cc5009de91ad5ce32eb203984c0416d715513c7f2489e5ca4f6
translator: "claude-haiku-5-5"
translated_at: "2026-10-15T16:29:01.217457+00:00"
---
<img src="banner.png" width="100%" alt="decide banner">

# Decide — संरचित निर्णय-निर्धारण

> संरचित ढाँचों और मूल्यांकन विधियों के माध्यम से तर्कसंगत निर्णय

---

## कब उपयोग करें?

- विकल्पों के बीच निर्णय लेना
- Pro/Con सूची की आवश्यकता हो
- बहु-मानदंड निर्णय
- महत्वपूर्ण निर्णयों में अनिश्चितता हो

**ट्रिगर-शब्द:** निर्णय लेना, चुनना, तुलना करना, मूल्यांकन करना, तौलना (entscheiden, waehlen, vergleichen, evaluieren, abwaegen)

---

## ढाँचे

### 1. Pro/Con मैट्रिक्स (सरल)

2 विकल्पों के बीच त्वरित निर्णय।

```
PRO A:                    CON A:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

PRO B:                    CON B:
- Vorteil 1               - Nachteil 1
- Vorteil 2               - Nachteil 2

Empfehlung: [A/B] weil [Begruendung]
```

---

### 2. भारित स्कोरिंग (जटिल)

भारांकन के साथ बहु-मानदंड निर्णय।

| मानदंड | भार | विकल्प A | स्कोर A | विकल्प B | स्कोर B |
|-----------|---------|----------|---------|----------|---------|
| मानदंड 1 | 30% | 8 | 2.4 | 6 | 1.8 |
| मानदंड 2 | 25% | 7 | 1.75 | 9 | 2.25 |
| कुल | 100% | - | X.XX | - | X.XX |

**प्रक्रिया:**
1. मानदंड एकत्र करें
2. भार निर्धारित करें (योग = 100%)
3. विकल्पों का मूल्यांकन करें (1-10 पैमाना)
4. स्कोर की गणना करें (मूल्यांकन x भार)
5. तुलना करें और सिफारिश करें

---

### 3. निर्णय वृक्ष (क्रमिक)

स्पष्ट यदि-तो पथों वाले निर्णय:
1. प्रारंभिक प्रश्न परिभाषित करें
2. पहली शाखा (सबसे महत्वपूर्ण मानदंड)
3. अगला स्तर (दूसरा सबसे महत्वपूर्ण)
4. अंतिम विकल्प तक

---

### 4. परिदृश्य विश्लेषण (अनिश्चितता)

```
Best Case (X% Wahrscheinlichkeit):
  Ergebnis: +Y Punkte -> Erwartungswert: +Z

Realistic Case (X%):
  Ergebnis: +Y -> Erwartungswert: +Z

Worst Case (X%):
  Ergebnis: -Y -> Erwartungswert: -Z

Gesamt-Erwartungswert: [Summe]
```

---

### 5. Eisenhower मैट्रिक्स (प्राथमिकता-निर्धारण)

```
              DRINGEND        NICHT DRINGEND
WICHTIG       1. TUN          2. PLANEN
NICHT WICHTIG 3. DELEGIEREN   4. ELIMINIEREN
```

---

## गुणवत्ता जाँच-सूची

अंतिम सिफारिश से पहले जाँचें:
- [ ] सभी प्रासंगिक मानदंड पहचाने गए?
- [ ] उपयोगकर्ता के मूल्यों पर विचार किया गया?
- [ ] दीर्घकालिक प्रभावों पर विचार किया गया?
- [ ] जोखिमों की पहचान और मूल्यांकन किया गया?
- [ ] पूर्वाग्रह-जाँच की गई?
- [ ] प्रतिवर्तनीयता की जाँच की गई?

---

## सर्वोत्तम अभ्यास

### मानदंड परिभाषित करना
- विशिष्ट और मापने योग्य
- बहुत अधिक नहीं (3-7 आदर्श)
- एक-दूसरे से स्वतंत्र

### भारांकन
- योग = 100%
- सबसे महत्वपूर्ण मानदंड >= 25%
- कोई भी भार < 5% नहीं

### सिफारिश
- स्पष्ट और तर्कसंगत
- विकल्पों का उल्लेख करें
- जोखिमों का नाम लें
- प्रतिवर्तनीयता का ध्यान रखें

---

## कार्यप्रवाह

```
1. User Request
2. Entscheidung verstehen
3. Optionen identifizieren (2-5)
4. Framework waehlen
5. Kriterien sammeln
6. Framework anwenden
7. Bias-Check (optional)
8. Empfehlung aussprechen
9. Reasoning dokumentieren
```

---

## परिवर्तन-सूची

### 1.0.0 (2026-03-15)
- BACH v3.8.0 से पोर्ट किया गया

---

*BACH v3.8.0 से पोर्ट किया गया | स्टैंडअलोन संस्करण*

**यह भी देखें:** [think](../think/SKILL.md) (विश्लेषण, मूल कारण, SWOT) | [brainstorm](../brainstorm/SKILL.md) (रचनात्मक विधियाँ, विचार-खोज) | [decision-shot](../decision-shot/SKILL.md) (इस विश्लेषण के आउटपुट को सिफारिश और पूर्ण संस्करण के लिंक के साथ एक कार्यकारी संक्षिप्त रूप में संघनित करें)
